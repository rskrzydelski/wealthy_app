import React, { Component } from 'react'
import Welcome from '../Welcome'

import { registerUrl } from '../endpoints'
import { post } from '../api'

import { AuthWrapper } from './css/auth'
import { SubmitButton, Form, TextInput, SelectInput } from './css/auth'

export default class Logout extends Component {
    constructor (props) {
      super(props)
      this.state = {
        data: { username: '', email: '', password: '', re_password: '', my_currency: '' }
      }
      console.log(this.state)
    }

    GoToLogin = (data) => {
      const { history } = this.props
      history.push('/login')
    }

    registerUser = (username, email, password, re_password, my_currency) => {
      post(
          registerUrl,
          {username: username, email: email, password: password, re_password: re_password, my_currency: my_currency},
          this.GoToLogin
          )
    }

    handleChange = (event) => {
        const data = this.state.data
        data[event.target.name] = event.target.value
        this.setState({ data: data })
    }

    handleSubmit = (event) => {
      this.registerUser(this.state.data.username, this.state.data.email, this.state.data.password, this.state.data.re_password, this.state.data.my_currency)
      this.setState({
          data: { username: '', email: '', password: '', re_password: '', my_currency: '' }
        })
      event.preventDefault();
    }

    render() {
        return (
          <AuthWrapper>
            <Form onSubmit={this.handleSubmit}>
                <TextInput
                  type='text'
                  name='username'
                  placeholder='username'
                  value={this.state.data.username}
                  onChange={this.handleChange}
                />
                <TextInput
                  type='email'
                  name='email'
                  placeholder='email'
                  value={this.state.data.email}
                  onChange={this.handleChange}
                />
                <TextInput
                  type='password'
                  name='password'
                  placeholder='password'
                  value={this.state.data.password}
                  onChange={this.handleChange}
                />
                  <TextInput
                    type='password'
                    name='re_password'
                    placeholder='re_password'
                    value={this.state.data.re_password}
                    onChange={this.handleChange}
                  />
                  <SelectInput id="currency" name="my_currency" onChange={this.handleChange}>
                    <option value="PLN">PLN</option>
                    <option value="USD">USD</option>
                    <option value="CHF">CHF</option>
                    <option value="EUR">EUR</option>
                  </SelectInput>
                  <SubmitButton type="submit" value="Register" />
              </Form>
              <Welcome />
            </AuthWrapper>
        )
    }
}
