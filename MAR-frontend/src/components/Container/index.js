import React from 'react'

export default function Container({children}) {
  return (
    <div className='flex flex-col h-full container mx-auto px-6 pt-20 max-w-7xl'>
      {children}      
    </div>
  )
}
