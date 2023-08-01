import React from 'react'
import Icon from '../Icons'
import Logo from '../Logo'


import {
  SidebarBackground,
  SidebarClose,
  SidebarTopLayer,
  SidebarLink,
  SidebarMenu,
  SidebarFavorites
} from './elements'

export function LogoutButton() {
  return (
    <button className='my-auto rounded-full p-2 hover:bg-gray-300'>
      <Icon name='logout' className='h-6 m-auto text-gray-500' />
    </button>
  )
}

export default function Sidebar() {
  return (
      <SidebarBackground>
        <SidebarTopLayer>
          <div className='mt-16'>
            <Logo href='/' title='Home' className='h-8' />
          </div>
          <SidebarClose />
        </SidebarTopLayer>

        <SidebarMenu>
          <SidebarLink href='/' title='Tarefas agendadas' icon='calendar'>
            Front Controler
          </SidebarLink> 
          <SidebarLink href='/search' title='search/execute' icon='search' >
            Search/Execute
          </SidebarLink> 
          <SidebarLink href='/docs' title='Documentações' icon='docs' >
            Documentation
          </SidebarLink> 
          <SidebarLink href='/operations' title='Operations' icon='menu' >
            Operations History
          </SidebarLink> 
          <SidebarLink href='/config' title='Configurations' icon='monitor' >
            Configuration
          </SidebarLink> 
          <SidebarLink href='/query' title='RawQuery' icon='search' >
            Raw SQL Query
          </SidebarLink> 
          
          <SidebarFavorites />
        </SidebarMenu>
      </SidebarBackground>
  )
}
