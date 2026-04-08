import { useState } from 'react'
import { AiOutlineArrowRight } from "react-icons/ai";
import { BiReset } from "react-icons/bi";

function App() {
    const [conv, setConv] = useState([])
    const handleSubmit = (event) => {
        event.preventDefault()
        if (event.target[0].value!==""){
            const data = event.target[0].value
            console.log("PROMPT:", data)
            setConv([...conv, [data,0]])
            event.target.reset();

            const msg = "http://localhost:8000/?msg="

            console.log(msg+data)
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
            <div className='h-[70vh] w-[60vw] mx-auto my-[5vh] overflow-y-scroll rounded-4xl border-2 border-white bg-[#111111]' style={{scrollbarWidth: "none", scrollBehavior: "smooth"}}>

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
        <form className='w-[63vw] mx-auto flex justify-center items-center gap-2 border-2 border-white rounded-full overflow-hidden bg-[#515151] text-white my-[8vh]' onSubmit={handleSubmit}  >
            <input name="prompt" id="prompt" type="text" className='w-full h-[8vh] text-xl p-8 overflow-x-scroll focus:outline-none'/>

            <button className='border-2 border-white rounded-full h-[8vh] w-[8vh] m-2 bg-blue-400' type='submit'> <AiOutlineArrowRight className='text-2xl ml-3 text-white'/> </button>
        </form>
    </>
    )
}

export default App
