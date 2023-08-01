import React, { useState, createContext } from 'react'

export const PopUpContext = createContext()

export default function PopUpProvider({children}) {
  const [ openPopUp, setOpenPopUp ] = useState(false)
  return (
    <PopUpContext.Provider value={{ openPopUp, setOpenPopUp }}>
      {children}
    </PopUpContext.Provider>
  )
}

