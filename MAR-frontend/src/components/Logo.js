import React from 'react'
import { NavLink } from 'react-router-dom'

export default function Logo({href, title, className}) {
  return (
    <NavLink
      to={href}
      title={title}
    >
      <img className="ml-6 w-32" src={`${process.env.PUBLIC_URL}/logo.png`} alt="logo.png"/>
    </NavLink>
  )
}

