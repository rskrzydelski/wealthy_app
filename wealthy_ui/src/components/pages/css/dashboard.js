import styled from 'styled-components'

export const Profit = styled.span`
  color: ${props => props.profit >= 0 ? 'green' : 'red'}
`
export const Value = styled.span`
  color: skyblue;
`

export const Spend = styled.span`
  color: aqua;
`

export const TableWrapper = styled.div`
  margin-top: 15px;
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
