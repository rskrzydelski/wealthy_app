import React, { Component } from 'react'

import { accountUrl } from '../endpoints'
import { get } from '../api'

import { Line } from './css/general'
import { UserCard, CardText } from './css/account'

export default class Account extends Component {
  constructor (props) {
    super(props)
      this.state = {
        username: '',
        my_currency: '',
        email: '',
      }
      this.getUserData()
  }

  collectUserData = (data) => {
    this.setState({username: data.username, my_currency: data.my_currency, email: data.email})  
  }

  getUserData = () => {
    get(accountUrl, this.collectUserData)
  }

  render() {
    return (
      <UserCard>
        <CardText>Your account data:<br/></CardText>
          <Line />
          <CardText>username: {this.state.username}<br/></CardText>
          <CardText>your currency: {this.state.my_currency}<br/></CardText>
          <CardText>email: {this.state.email}<br/></CardText>
      </UserCard>
    )
  }
}
