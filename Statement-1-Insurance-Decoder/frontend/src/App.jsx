import { useState } from 'react'
import { AiOutlineArrowRight } from "react-icons/ai";
import { BiReset } from "react-icons/bi";

function App() {
    const [conv, setConv] = useState([])
    const [disabled, setDis] = useState(0)
    const handleSubmit = (event) => {
        event.preventDefault()
        if (event.target[0].value!==""){
            setDis(disabled => 1)
            const data = event.target[0].value
            console.log("PROMPT:", data)
            setConv([...conv, [data,0],["  .  .  .  ",1]])
            event.target.reset();

            const msg = "http://localhost:8000/?msg="

            console.log(msg+data)

            fetch(msg+data)
            .then(response => response.json())
            .then(data => {
                const len = data.length
                const cont = data[len-1].content
                setConv([...conv,[data,0],[cont,1]])
                setDis(disabled => 0)
            })
            .catch(error => {
                console.log(error)
                console.log("An error occured. Could not contact the model.")
                setConv([...conv,[data,0],["An error occured. Could not contact the model.",1]])
                setDis(disabled => 0)
            })
        }
    }

    const handleReset = () => {
        setConv([])
    }

    const ResetButton = () => {
        return(
            <button className='text-white text-6xl absolute left-10 hover:scale-110 duration-150' onClick={handleReset}>
                <BiReset/>
            </button>
        )
    }

    const Message = ({msg,type}) => {
        let classes = "";
        if (type==1){
            classes = 'm-4 bg-[#515151] p-4 text-lg rounded-b-3xl rounded-r-3xl text-white max-w-[50vw] max-h-[30vh] wrap-break-word overflow-y-scroll'
        }
        else{
            classes = 'm-4 bg-blue-400 p-4 text-lg rounded-b-3xl rounded-l-3xl text-white max-w-[50vw] max-h-[30vh] wrap-break-word overflow-y-scroll'
        }
        return (
            <div className={type ? "text-left" : "text-right"}>
                <span className={classes} style={{display: "inline-block", scrollBehavior: "smooth", scrollbarWidth: "none"}}>{msg}</span>
            </div>
        )
    }

    const Conversation = () => {
        return(
            <div className='h-[70vh] w-[70vw] mx-auto my-[5vh] overflow-y-scroll rounded-4xl border-2 border-white bg-[#111111]' style={{scrollbarWidth: "none", scrollBehavior: "smooth"}}>

            {
                conv.map((value,idx) => {
                    return(
                        <Message msg={value[0]} type={value[1]} key={idx}/>
                    )
                })
            }
            </div>
        )
    }

    return (
    <>
        <ResetButton />
        <Conversation />
        <form className='w-[73vw] mx-auto flex justify-center items-center gap-2 border-2 border-white rounded-full overflow-hidden bg-[#515151] text-white my-[8vh]' onSubmit={handleSubmit}  >
            <input name="prompt" id="prompt" type="text" className='w-full h-[8vh] text-xl p-8 overflow-x-scroll focus:outline-none'/>

            <button className='border-2 border-white rounded-full h-[8vh] w-[8vh] m-2 bg-blue-400' type='submit' disabled={disabled}> <AiOutlineArrowRight className='text-[4vh] ml-[1.5vh] text-white'/> </button>
        </form>
    </>
    )
}

export default App
