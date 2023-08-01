import React, { useContext } from "react"
import Icon from "../Icons"
import { PopUpContext } from "./context"

export default function PopUp({ children }) {
  const { openPopUp, setOpenPopUp } = useContext(PopUpContext)
  return (
    <div 
      className='fixed h-full w-full top-0 left-0 z-10 bg-black
      bg-opacity-60'
    >
      <div className='flex h-screen items-center justify-center'>
        <div style={{height: '95%', width: '95%'}} className='relative rounded z-10 bg-white p-4 my-auto'>
          <button className='absolute top-4 right-4' onClick={() => setOpenPopUp(false)}>
            <Icon name='x' className='h-5 text-gray-700' />
          </button>
          <br/>
          {children}
        </div>
      </div>
    </div>
  )
}