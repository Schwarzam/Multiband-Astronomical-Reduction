import React, { useContext } from 'react'
import { NavLink } from 'react-router-dom'

import { NavbarContext } from './context'
import Icon from '../Icons'


export function NavbarOpenSidebar({onClick}) {
  const { isOpen, setIsOpen } = useContext(NavbarContext)
  return (
      <button onClick={() => setIsOpen(true)} >
        <Icon name='menu' className='h-8' />
      </button>
  )
}

export function Nav({children}) {
  return (
    <nav className='sticky w-full border-b bg-white border-gray-200'>
      <div className='flex h-20 items-center justify-between'>
        {children}
      </div>
    </nav>
  )

}
