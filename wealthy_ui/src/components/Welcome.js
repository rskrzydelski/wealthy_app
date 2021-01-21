import React, { Component } from 'react'
import { Description, TextContainer } from './pages/css/general'

export default class Welcome extends Component {
  render () {
    return (
      <TextContainer>
        <Description>
          Wealth is application for store resources such as gold, silver, cash.
          You can add your gold, silver and cash, see current price, see how money you spend
          on particular resource or on all resources and finally see your profit or your lost.
          Currently you can choose following currencies: PLN, USD, CHF, EUR.
        </Description>
      </TextContainer>
    )
  }
}
