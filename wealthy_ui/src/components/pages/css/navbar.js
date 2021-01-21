import styled from 'styled-components'
import { Link } from 'react-router-dom'

export const Navbar = styled.div`
  position: relative;
  background-color: black;
  height: 60px;
  display: flex;
  justify-content: flex-end;
  padding: 0;
  align-items: center;
  @media (min-width: 768px) {
    height: 70px;
  }
`

export const Hamburger = styled(Link)`
  margin-right: 2rem;
  color: gold;
  font-size: 2rem;
  text-decoration: none;
  margin: 20px 15px 10px 10px;
  @media (min-width: 768px) {
    display: none;
  }
`

export const NavMenu = styled.nav`
  background-color: rgba(0, 0, 0, 80%);
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  position: fixed;
  left: 0;
  top: ${props => props.sidebar ? '0' : '-100%'};
  transition: ${props => props.sidebar ? '350ms' : '850ms'};
  @media (min-width: 768px) {
    background-color: black;
    height: auto;
    top: 0;
  }
`

export const NavMenuItems = styled.ul`
  width: 100%;
  margin: 10px 40px;
  c {
    &::after {
      content: "";
      clear: both;
      display: block;
    }
  }
`

export const NavMenuItem = styled.li`
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px 8px;
    list-style: none;
    height: 60px;
    @media (min-width: 768px) {
      float: right;
      padding: 8px 10px;
    }
    a {
      font-size: 16px;
      font-family: Courgette, cursive;
      text-decoration: none;
      color: gold;
      @media (min-width: 360px) {
        font-size: 18px;
      }
      @media (min-width: 410px) {
        font-size: 20px;
      }
    }
`

export const StyledBrand = styled.h1`
    z-index: 1;
    position: absolute;
    color: white;
    margin: 35px 0px 0px 20px;
    text-align: left;
    font-family: 'Indie Flower', cursive;
    font-size: 18px;
    height: 100%;
    left: 0;
    @media (min-width: 768px) {
      font-size: 24px;
      margin: 45px 0px 0px 25px;

    }
    &:hover {
      color: gold;
    }
`
