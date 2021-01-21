import React, { useState } from 'react'
import { FaBars } from 'react-icons/fa'
import { Link } from 'react-router-dom'
import { MenuData, AuthMenuData } from './SidebarData'

import { Navbar, Hamburger, NavMenu, NavMenuItems, NavMenuItem, StyledBrand } from './pages/css/navbar'

function NavBar (props) {
  const isAuth = props.isAuth
  const [sidebar, setSidebar] = useState(false)
  const showSidebar = () => setSidebar(!sidebar)
  const data = isAuth ? AuthMenuData : MenuData

  return (
    <Navbar>
      <StyledBrand>Wealthy app</StyledBrand>
      <Hamburger>
        <FaBars onClick={showSidebar} />
      </Hamburger>
      <NavMenu sidebar={sidebar}>
        <NavMenuItems onClick={showSidebar}>
          {data.map((item, index) => {
            return <NavMenuItem key={index} className={item.cName}>
              <Link to={item.path}>
                <span>{item.title}</span>
              </Link>
            </NavMenuItem>
          })}
        </NavMenuItems>
      </NavMenu>
    </Navbar>
  )
}

export default NavBar
