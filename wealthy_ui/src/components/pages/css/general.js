import styled from 'styled-components'

export const Line = styled.hr`
  border-top: 1px solid gold;
  margin-bottom: 20px;
`

export const TextContainer = styled.div`
  background: #111519;
  margin: 30px 15px;
  @media (min-width: 640px) {
    width: 40%;
    float: left;
  }
`

export const Description = styled.p`
  padding: 0 10px;
  font-size: 12px;
  font-family: 'Saira', sans-serif;
  text-align: justify;
  word-spacing: 3px;
  line-height: 22px;
  @media (min-width: 768px) {
     margin-top: 5px;
     font-size: 16px;
  }
`
