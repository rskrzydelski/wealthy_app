import styled from 'styled-components'
import { GiGoldBar, GiBigDiamondRing, GiFlamingo } from 'react-icons/gi'
import { FaEthereum } from 'react-icons/fa'
import { SiBitcoin, SiLitecoin } from 'react-icons/si'

export const MarketContainer = styled.div`
  alignt-text: center;
  margin: 10px;
  height: 50%;
  &::after {
      content: "";
      clear: both;
      display: block;
    }
`

export const MarketItem = styled.div`
  width: 50%;
  padding: 2px 1px;
  float: left;
  font-size: 19px;
  &::after {
      content: "";
      clear: both;
      display: block;
    }
  @media (min-width: 360px) {
    font-size: 20px;
  }
  @media (min-width: 768px) {
    font-size: 25px;
    padding: 2px 20px;
  }
`

export const MarketText = styled.div`
  text-align: center;
  font-family: 'Saira', sans-serif;
  margin-top: 2%;
  margin-left: 10px;
  float: left;
  font-size: 9px;
  @media (min-width: 360px) {
    font-size: 10px;
  }
  @media (min-width: 768px) {
      font-size: 17px;
  }
`

export const Gold999Icon = styled(GiGoldBar)`
    color: gold;
    float: left;
`

export const Gold585Icon = styled(GiBigDiamondRing)`
    color: gold;
    float: left;
`

export const Silver999Icon = styled(GiGoldBar)`
    color: #e6e6e6;
    float: left;
`

export const Silver800Icon = styled(GiBigDiamondRing)`
    color: #e6e6e6;
    float: left;
`

export const FlmIcon = styled(GiFlamingo)`
     color: pink;
     float: left;
`

export const EthIcon = styled(FaEthereum)`
    color: #6346E1;
    float: left;
`

export const LtcIcon = styled(SiLitecoin)`
    float: left;
`

export const BtnIcon = styled(SiBitcoin)`
    color: blue;
    float: left;
`

export const TextSpan = styled.span`
  margin-right: 5px;
`
