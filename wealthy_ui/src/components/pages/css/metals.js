import styled from 'styled-components'

export const DelButton = styled.button`
  display: block;
  cursor: pointer;
  font-size: 12px;
  color: white;
  background: #111519;
`

export const ListTitle = styled.h1`
  margin: 10px;
  text-align: center;
  font-size: 14px;
  font-family: 'Saira', sans-serif;
  @media (min-width: 640px) {
    font-size: 16px;
  }
  @media (min-width: 1024px) {
    font-size: 20px;
  }
`

export const MetalImage = styled.div`
  width: 100%;
  height: 100px;
  background-image: url(${(props) => props.image});
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
  margin: 0 auto;
  }
`

export const TableWrapper = styled.div`
  margin-top: 20px;
  table {
    margin: 0 auto;
    width: 98%;
    border-spacing: 0;
    border: 1px solid gold;
    tr {
      :last-child {
        td {
          border-bottom: 0;
        }
      }
      :nth-child(n + 1) {
        td {
          :last-child {
            
            }
          }
        }
      }
    }
    th,
    td {
      padding: 1px;
      border-bottom: 1px solid gold;
      border-right: 1px solid gold;
  
      text-align: center;
      font-family: 'Saira', sans-serif;
      font-size: 12px;
      @media (min-width: 414px) {
        font-size: 14px;
      }
      @media (min-width: 768px) {
        font-size: 18px;
      }
      :last-child {
        border-right: 0;
      }
    }
  }
`

// form
export const Form = styled.form`
  border: 1px solid gold;
  border-radius: 14px;
  margin: 30px 40px;
  @media (min-width: 640px) {

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
