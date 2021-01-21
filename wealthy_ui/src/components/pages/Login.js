import React, { Component } from 'react'

import { loginUrl } from '../endpoints'
import { post } from '../api'
import Welcome from '../Welcome'

import { AuthWrapper, SubmitButton, Form, TextInput } from './css/auth'

export default class Login extends Component {
    constructor (props) {
      super(props)
      this.state = {
        credentials: { email: '', password: '' }
      }
    }

    Authenticate = (data) => {
      const { history } = this.props
      localStorage.setItem('access', data.access)
      localStorage.setItem('refresh', data.refresh)
      this.props.isAuthenticated(true)
      history.push('/')
    }

    loginUser = (email, password) => {
      post(loginUrl, {email: email, password: password}, this.Authenticate)
    }

    handleChange = (event) => {
        const cr = this.state.credentials
        cr[event.target.name] = event.target.value
        this.setState({ credentials: cr })
    }

    handleSubmit = (event) => {
      this.loginUser(this.state.credentials.email, this.state.credentials.password)
      this.setState({
          credentials: { email: '', password: '' }
        })
      event.preventDefault();
    }

    render() {
        return (
          <AuthWrapper>
            <Form onSubmit={this.handleSubmit}>
                <TextInput
                  type='email'
                  name='email'
                  placeholder='email'
                  value={this.state.credentials.email}
                  onChange={this.handleChange}
                />
                <TextInput
                  type='password'
                  name='password'
                  placeholder='password'
                  value={this.state.credentials.password}
                  onChange={this.handleChange}
                />
              <SubmitButton type="submit" value="Login" />
            </Form>
            <Welcome />
          </AuthWrapper>
        )
    }
}
