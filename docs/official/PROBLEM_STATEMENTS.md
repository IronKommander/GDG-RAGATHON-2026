# GDG RAGATHON 2026

 Build high-performance Retrieval-Augmented Generation (RAG) systems to solve real-world data challenges.(7th April - 9th April)
 
### Challenge Structure & Scoring
You are not limited to one challenge. To maximize your chances of winning, you can attempt multiple problem statements to stack your points.

| **Challenge**   | **Difficulty** | **Points** | **Objective**                                                                  |
| --------------- | -------------- | ---------- | ------------------------------------------------------------------------------ |
| **Statement 1** | **Easy**       | 20         | Decode and simplify complex insurance policies with high-precision RAG.        |
| **Statement 2** | **Medium**     | 40         | Build a local restaurant recommender using custom datasets and hybrid search.  |
| **Statement 3** | **Hard**       | 70         | Predict placement readiness using LLM data extraction and regression modeling. |

**How it works:**
- **Total Possible Score:** 130 Points.    
- **Flexibility:** You can choose to do just the Hard one, all three, or any combination.    
- **Winning Criteria:** The participant with the **highest cumulative points** at the end of 5 days wins.

> [!Note on Evaluation]
> If two participants both score 180 points(130points+50bonus), the winner will be decided based on **Code Quality** and **Full-stack Integration** (Frontend + Backend).

---
# *Problem Statements*

### Easy: The "Fine Print Decoder" (20 Points)

**Goal:** Build a RAG system that simplifies complex "Terms & Conditions" or Policy documents. You must use a comprehensive document (_Titan Secure Health Insurance Policy) to answer specific, high-stakes user queries with 100% accuracy.

- **The Task:** Create a bot that helps users understand complex legal jargon and hidden clauses in insurance or policy documents.
    
- **The Workflow:**
    
    1. **Context Loading:** The bot should ingest a set of 3–5 official documents (e.g., Health Insurance Policy, Credit Card Agreement, or Rental Contract).
        
    2. **Smart Filtering:** The user should be able to ask for clarifications based on "coverage," "penalties," or "exclusions" (e.g., _"Does this policy cover injuries from extreme sports?"_ or _"What is the penalty for early cancellation?"_).
        
    3. **Hybrid Knowledge:** The bot must use **RAG** to retrieve specific clauses (Section and Page references) and explain them in simple "ELI5" (Explain Like I'm Five) language.


#### Easy Bonus Credits (+5 Points)
- **Source Attribution:** Earn extra points if your bot explicitly cites the **Section and Clause number** for every answer it provides to ensure transparency and trust.

---
### Medium: The "Lucknow Foodie Guide" (40 Points)

**Goal:** Build a context-aware restaurant recommendation engine for the local area.
You must manually collect or scrape data for at least **20–30 local eateries** (e.g., _Tunday Kababi, Royal Cafe, Sky Glass Brewing, or the cafes in Phoenix Palassio_).

- **The Task:** Create a bot that helps students find the best places to eat around **IIIT Lucknow **.

- **The Workflow:** 
1. **Context Loading:** The bot should have access to a dataset of local Lucknow food spots (e.g., _Tunday Kababi, Royal Cafe, Sky Glass Brewing, or the cafes in Phoenix Palassio_).

2. **Smart Filtering:** The user should be able to ask for recommendations based on specific "vibe" or "budget" or based on dishes/reviews/Veg/Nonveg etc...(e.g., _"Suggest a budget-friendly Biryani place near campus"_ or _"Where can I find the best basket chaat in Gomti Nagar?"_).

3. **Hybrid Knowledge:** The bot must use **RAG** to retrieve restaurant details (hours, signature dishes) 

---
### Hard: The "Placement Predictor & Mentor" (70 Points)
**Goal:** A hybrid system combining **Generative AI** (for profile extraction) and **Regression** (for score prediction).
- **The Workflow:**
    
    1. **Chat-Based Profiling:** The student chats with the bot to provide their details (CGPA, Tech Stack, Projects, Internships, Communication, Opensource experience).
        
    2. **Structured Extraction:** An LLM extracts these values into a JSON format.
        
    3. **The Regression Engine:** These values are fed into a **Regression Model** (trained on senior placement data) to generate a **Readiness Score (0–100)**.
        
    4. **Experience RAG:** Based on the user's tech stack, the system retrieves the most relevant **Senior Interview Experiences** from a vector database.

### Bonus Credits (Go the Extra Mile)
Participants can earn a total of **45 additional points** by implementing these advanced features:

#### 1. The "Resume Parser" (+15 Points)
- **Challenge:** Instead of the student typing their details, allow them to **upload their Resume (PDF/Docx)**.
    
- **Requirement:** The system must autonomously extract the CGPA, Skills, and Experience directly from the file to feed the Regression model.


#### 2. "Smart Experience Matcher" (+30 Points)
- **Challenge:** Integrate a database of **Senior Interview Experiences**.
    
- **Requirement:** Use **Cosine Similarity** to compare the student's extracted profile against the interview database.
    
- **Result:** Recommend the top 3 most relevant interview experiences (e.g., if a student knows Java/AWS, show them Amazon or Goldman Sachs interview reports).

---
**"Anything more creative is most welcome and would receive an extra edge."**

We encourage you to go beyond the baseline requirements. Whether it’s an exceptionally intuitive **UI/UX**, a unique **Data Visualization** of the regression results, or an innovative **Prompt Engineering** technique, creativity will be highly rewarded during the final evaluation.

Good luck with RAGATHON
GDG ML Wing

For any queries regarding the problem statements, evaluation, or technical hurdles, feel free to reach out to:
- **C Sai Sujit** (81056 26006)
- **Vedant Humbe** (99231 58762)
- **Abhinav Neema** (94257 02277)
