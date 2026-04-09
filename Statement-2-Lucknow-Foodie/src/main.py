from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode, tools_condition
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

app = FastAPI();

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bge_embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5", #Using the base BGE embedding model
    model_kwargs={"device":"cpu"},
    encode_kwargs={"normalize_embeddings": True},
    query_encode_kwargs={"prompt": "Represent this sentence for searching relevant passages: "}
)

COLLECTION_NAME = "ST2_dataset"
MODEL="llama-3.3-70b-versatile"
vectorstore = QdrantVectorStore.from_existing_collection(
    collection_name=COLLECTION_NAME,
    embedding=bge_embeddings
)
retriever = vectorstore.as_retriever()

class RetrieveInput(BaseModel):
    query: str = Field(description="The specific search query or keywords to look up in the restaurant dataset.")

@tool(args_schema=RetrieveInput)
def retrieve_blog_posts(query: str) -> str:
    """Search and return info about restaurants CLOSEST TO IIIT Lucknow."""
    docs = retriever.invoke(query)
    formatted_docs = []
    for doc in docs:
        meta = doc.metadata
        header_info = f"[{meta.get('restaurant_name', '')} {meta.get('rating', '')} {meta.get('distance_km', '')} {meta.get('cuisines', '')}]"
        formatted_docs.append(f"{header_info}\n{doc.page_content}")
        
    return "\n\n---\n\n".join(formatted_docs)

tools = [retrieve_blog_posts]

llm = ChatGroq(model=MODEL, temperature=0)
llm_with_tools = llm.bind_tools(tools)

def generate_query_or_respond(state: MessagesState):
    """
    IMPORTANT: IF QUESTION NOT RELATED TO RESTAURANTS/CAFES/EATERIES, DO NOT RETRIEVE
    Call the model to generate a response based on the current state. Given
    the question, it will decide to retrieve using the retriever tool, or simply respond to the user.
    """
    sys_msg = SystemMessage(
        content=(
            """
            You are a helpful AI assistant for IIIT Lucknow Students..
            IMPORTANT: IF QUESTION NOT RELATED TO RESTAURANTS/CAFES/EATERIES, DO NOT RETRIEVE
            """
        )
    )
    messages  = [sys_msg] + state["messages"]
    response = (
        llm_with_tools.invoke(messages)
    )
    return {"messages": [response]}

GRADE_PROMPT = (
    "You are a grader assessing relevance of a retrieved document to a user question. \n "
    "Here is the retrieved document: \n\n {context} \n\n"
    "Here is the user question: {question} \n"
    "If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n"
    "Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."
)

class GradeDocuments(BaseModel):
    """Grade documents using a binary score for relevance check."""

    binary_score: str = Field(
        description="Relevance score: 'yes' if relevant, or 'no' if not relevant"
    )

grader_model = ChatGroq(model=MODEL, temperature=0)

def grade_documents(state: MessagesState) -> Literal["generate_answer", "rewrite_question", "no_docs_found"]:
    """Determine whether the retrieved documents are relevant to the question."""

    num_tool_calls = [msg for msg in state["messages"] if getattr(msg, 'type', '') == 'tool']
    if(len(num_tool_calls) > 2) : return "no_docs_found"

    question = [msg.content for msg in state["messages"] if isinstance(msg, HumanMessage)][-1]
    context = state["messages"][-1].content
    prompt = GRADE_PROMPT.format(question=question, context=context)
    response = (
        grader_model
        .with_structured_output(GradeDocuments).invoke(
            [{"role": "user", "content": prompt}]
        )
    )
    score = response.binary_score
    if score == "yes":
        return "generate_answer"
    else:
        return "rewrite_question"

REWRITE_PROMPT = (
    "IMPORTANT: IF QUESTION NOT RELATED TO RESTAURANTS/CAFES/EATERIES, DO NOT REWRITE"
    "Look at the input and try to reason about the underlying semantic intent / meaning.\n"
    "Here is the initial question:"
    "\n ------- \n"
    "{question}"
    "\n ------- \n"
    "Formulate an improved question:"
)

def no_docs_found(state: MessagesState):
    """Exit to prevent infinite looping"""
    final_text = "No information found related to Titan Secure docs."
    return {"messages" : state["messages"]+[SystemMessage(content=final_text)]}

def rewrite_question(state: MessagesState):
    """Rewrite the orignal user question"""
    question = [msg.content for msg in state["messages"] if isinstance(msg, HumanMessage)][-1]
    prompt = REWRITE_PROMPT.format(question=question)
    response = grader_model.invoke([{"role": "user", "content": prompt}])
    return {"messages": [HumanMessage(content=response.content)]}

GENERATE_PROMPT = (
    "IMPORTANT: ALWAYS SUGGEST RESTAURANTS CLOSEST TO IIIT LUCKNOW!!!"
    "IMPORTANT: If restaurant is very far away, DO NOT SUGGEST!!!"
    "IMPORTANT: If not related to Restaurants, cafes or eateries, do not retrieve data."
    "You are a RAG model that answers queries about restaurants, cafes and places to eat around IIIT Lucknow."
    "You must use a comprehensive dataset to answer specific, high-stakes user queries with 100% accuracy."
    "Keep the answer very simple and easy to understand.\n"
    "Question: {question} \n"
    "Context: {context}"
)

def generate_answer(state: MessagesState):
    """Generate an answer"""
    question = [msg.content for msg in state["messages"] if isinstance(msg, HumanMessage)][-1]
    context = state["messages"][-1].content
    prompt = GENERATE_PROMPT.format(question=question, context=context)
    response = grader_model.invoke([{"role" : "user", "content" : prompt}])
    return {"messages" : [response]}

workflow = StateGraph(MessagesState)
workflow.add_node(generate_query_or_respond)
workflow.add_node("retrieve", ToolNode(tools))
workflow.add_node(rewrite_question)
workflow.add_node(generate_answer)
workflow.add_node(no_docs_found)

workflow.add_edge(START, "generate_query_or_respond")
workflow.add_conditional_edges(
    "generate_query_or_respond",
    tools_condition,
    {
        "tools" : "retrieve",
        END: END,
    }
)
workflow.add_conditional_edges(
    "retrieve",
    grade_documents,
)
workflow.add_edge("no_docs_found", "generate_answer")
workflow.add_edge("generate_answer", END)
workflow.add_edge("rewrite_question", "generate_query_or_respond")
graph = workflow.compile()
graph.get_graph().draw_mermaid_png()

def contact_llm(msg: str):
    result = []
    for chunk in graph.stream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": msg,
                }
            ]
        }
    ):
        for node, update in chunk.items():
            result.append(update["messages"][-1])
    return result

@app.get("/")
def conn_mod(msg: str):
    return contact_llm(msg)
