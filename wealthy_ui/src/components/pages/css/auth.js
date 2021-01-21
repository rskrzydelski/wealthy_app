import styled from 'styled-components'

export const AuthWrapper = styled.div`
  @media (min-width: 640px) {
    &::after {
      content: "";
      clear: both;
      display: block;
    }
  }
`

export const Form = styled.form`
  border: 1px solid gold;
  border-radius: 14px;
  margin: 30px 40px;
  @media (min-width: 640px) {
    float: left;
    width: 40%;
  }
`

export const TextInput = styled.input`
  display: block;
  border-radius: 10px;
  background: #232632;
  padding: 5px;
  width: 80%;
  margin: 10px auto;
  font-size: 12px;
  text-align: center;
  font-family: 'Saira', sans-serif;
  color: gold;
  &::placeholder {
    color: gold;
  }
`

export const SelectInput = styled.select`
  display: block;
  background: #232632;
  border-radius: 10px;
  width: 80%;
  margin: 10px auto;
  padding: 5px;
  color: gold;
  font-size: 12px;
  text-align: center;
       option {
         color: gold;
         background: #232632;
         font-weight: small;
       }
`

export const SubmitButton = styled.input`
  display: block;
  width: 30%;
  height: 32px;
  margin: 15px auto;
  background: #232632;
  border: 1px solid gold;
  border-radius: 10px;
  color: gold;
  font-family: 'Saira', sans-serif;
  text-transform: uppercase;
  ${'' /* &:hover { background: black; } */}
`

export const TextArea = styled.textarea`
  display: block;
  background: #232632;
  border-radius: 10px;
  width: 80%;
  margin: 10px auto;
  padding: 5px;
  color: gold;
  font-size: 12px;
  text-align: center;
  &::placeholder {
    color: gold;
  }
`
