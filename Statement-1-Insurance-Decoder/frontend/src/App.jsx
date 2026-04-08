import { useState } from 'react'
import { AiOutlineArrowRight } from "react-icons/ai";

function App() {
    const [conv, setConv] = useState([])

    const handleSubmit = (event) => {
        event.preventDefault()
        console.log(event.target[0].value)
        setConv([...conv, [event.target[0].value,0]])
    }

    const Message = ({msg,type}) => {
        let classes = "";
        if (type==1){
            classes = 'm-4 bg-[#515151] p-4 text-xl rounded-b-3xl rounded-r-3xl text-white'
        }
        else{
            classes = 'm-4 bg-blue-400 p-4 text-xl rounded-b-3xl rounded-l-3xl text-white'
        }
        return (
            <div className={type ? "text-left" : "text-right"}>
                <span className={classes} style={{display: "inline-block"}}>{msg}</span>
            </div>
        )
    }

    const Conversation = () => {
        return(
        <div className='h-[70vh] w-[60vw] mx-auto my-[5vh] overflow-y-scroll' style={{scrollbarWidth: "none", scrollBehavior: "smooth"}}>

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
            <Conversation />
            <form className='w-[60vw] mx-auto flex justify-center items-center gap-2 border-2 border-black rounded-full overflow-hidden bg-[#515151] text-white my-[8vh]' onSubmit={handleSubmit}  >
                <input name="prompt" id="prompt" type="text" className='w-full h-[8vh] text-xl p-8 overflow-x-scroll focus:outline-none'/>

                <button className='border-2 border-black rounded-full h-[8vh] w-[8vh] m-2 bg-blue-400' type='submit'> <AiOutlineArrowRight className='text-2xl ml-3 text-white'/> </button>
            </form>
        </>
    )
}

export default App
