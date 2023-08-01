import React, {useContext, useState} from 'react'

import Sidebar from '../Sidebar'
import Logo from '../Logo'
import { Nav, NavbarOpenSidebar, } from './elements'
import { NavbarContextWrapper } from './context'


export default function Navbar() {

  return (
    <NavbarContextWrapper>
      <Nav>
        <div className='flex ml-8 w-24 justify-between'>
          <NavbarOpenSidebar />
          <Logo href='/' title='Home' className='h-7 my-auto' />
        </div>

        <div className='flex w-52 mr-10 items-center justify-between'>

        </div>
      </Nav>
      <Sidebar />
    </NavbarContextWrapper>
  )
}
