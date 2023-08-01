import React, { useContext } from 'react'
import { NavLink } from 'react-router-dom'
import Icon from '../Icons'
import { NavbarContext } from '../Navbar/context'


export function SidebarBackground({children}) {
  const { isOpen, setIsOpen } = useContext(NavbarContext)
  return (
    <div 
      className={`fixed left-0 top-0 z-10 h-screen w-96 bg-gray-50 transition-all
      duration-300
      ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}
    >
      {children}
    </div>
  )
}

export function SidebarClose() {
  const { isOpen, setIsOpen } = useContext(NavbarContext)
  return (
      <button 
        onClick={() => setIsOpen(false)}
        className='flex items-center justify-center h-9 w-9 rounded-full'
      >
        <Icon name='x' className='h-8 text-gray-500' />
      </button>
  )
}

export function SidebarTopLayer({children}) {
  return (
    <div className='flex h-[10vh] items-center justify-between px-10'>
      {children}
    </div>
  )
}

export function SidebarLink({href, title, icon, children}) {
  return (
    <NavLink 
      to={href}
      title={title}
      className='flex my-2 px-5 py-1 text-gray-500 rounded items-center
      hover:text-primary hover:bg-gray-200 transition-colors 
      duration-300 group'
    >
      <Icon
        name={icon}
        className='h-5 mr-3 text-gray-500 transition-colors duration-300
      group-hover:text-primary' 
      />
      <p className='pt-[2px]'>
        {children}
      </p>
    </NavLink>
  )
}

export function SidebarMenu({children}) {
  return (
    <div className='h-[80vh] w-full p-6 mt-8'>
      {children}
    </div>
  )
}

function SidebarSubLink({href, title, icon, children}) {
  return (
    <NavLink 
      to={href}
      title={title}
      className='flex my-2 px-5 py-1 text-gray-500 rounded items-center
      hover:text-primary hover:bg-gray-200 transition-colors 
      duration-300 group'
    >
      <Icon
        name={icon}
        className='h-5 mr-3 text-gray-500 transition-colors duration-300
      group-hover:text-primary' 
      />
      <p className='pt-[2px]'>
        {children}
      </p>
    </NavLink>
  )
}

export function SidebarFavorites() {
  const favoritesJson = {

  }
  return (
    <div className='ml-5 overflow-auto h-[65vh] pr-2 '>
      {
      Object.keys(favoritesJson).map((project, index) =>
        <div key={index}>
          <p className='text-sm mt-6 text-gray-500'>{project}</p>
          {favoritesJson[project].map((tableName, index) =>
            <SidebarSubLink key={index} href={`/run/${tableName}`} title={tableName} icon='play'>
              {tableName}
            </SidebarSubLink>)}
        </div>
        )
      }
    </div>
  )
}