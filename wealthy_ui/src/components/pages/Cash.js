import React, { Component } from 'react'
import Axios from 'axios'
import { Table } from '../Table'

import { SubmitButton, Form, TextInput } from './css/cash'
import { ListTitle, CashItem, DelButton, CashImage, TableWrapper } from './css/cash'
import cash from '../../static/franc.jpg'

import { 
    cashUrl,
    accountUrl,
    refreshTokenUrl
} from '../endpoints'

export default class Cash extends Component {
    constructor (props) {
      super(props)
      this.state = {
          CashList: [],
          cash: {
            my_cash: '',
            save_date: '',
        },
        my_currency: '',
      }
    }

    componentDidMount () {
      this.getCurrency()
      this.collectCash()
    }

    getCurrency = async () => {
      try {
          const res = await Axios.get(accountUrl, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
          if (res.data.my_currency === 'PLN') {
            this.setState({my_currency: 'zł'})
          } else if (res.data.my_currency === 'USD') {
            this.setState({my_currency: '$'})
          } else if (res.data.my_currency === 'EUR') {
            this.setState({my_currency: '€'})
          } else if (res.data.my_currency === 'CHF') {
            this.setState({my_currency: 'chf'})
          }
      } catch (error) {  
      }
    }

    collectCash = async () => {
      try {
            const res = await Axios.get(cashUrl, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
            console.log(res)
            const CashList = [...this.state.CashList, ...res.data]
            this.setState({CashList})
        } catch (error) {
            if (error.response.status === 401) {
                const res = await Axios.post(refreshTokenUrl, {refresh: localStorage.getItem('refresh')})
                localStorage.setItem('access', res.data.access)
                this.collectCash()
              }
        }
    }

    onSubmitDel = async (e, id) => {
      e.preventDefault()
      try {
          await Axios.delete(cashUrl + '/' + id, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
          this.setState({CashList: []})
          this.collectCash()
      } catch (error) {
          if (error.response.status === 401) {
              const res = await Axios.post(refreshTokenUrl, {refresh: localStorage.getItem('refresh')})
              localStorage.setItem('access', res.data.access)
              this.onSubmitDel(e, id)
            }
      }
    }

    handleSubmitAdd = async (e) => {
      e.preventDefault()
      try {
          await Axios.post(cashUrl, this.state.cash, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
          this.setState({CashList: []})
          this.collectCash()
      } catch (error) {
          if (error.response.status === 401) {
              const res = await Axios.post(refreshTokenUrl, {refresh: localStorage.getItem('refresh')})
              localStorage.setItem('access', res.data.access)
              this.onSubmitAdd(e)
            }
      }
    }

    handleFormInput = (event) => {
        const res = this.state.cash
        res[event.target.name] = event.target.value
        this.setState({ cash: res })
    }

    render() {
      const columns = [
        {
          Header: "My cash",
          columns: [
            {
              Header: 'id',
              accessor: 'id',
            },
            {
              Header: 'cash',
              accessor: 'cash',
            },
            {
              Header: 'currency',
              accessor: 'currency',
            },
            {
              Header: 'save_date',
              accessor: 'save_date',
            },
            {
              Header: 'action',
              accessor: 'delete',
              Cell: ({ cell }) => (
                <DelButton value={cell.row.values.name} onClick={(e) => this.onSubmitDel(e, cell.row.values.id)}>
                  delete
                </DelButton>)
            }
          ],
        },
      ]

      const data = this.state.CashList.map((cash) => (
            {
              id: cash.id,
              cash: cash.my_cash,
              currency: cash.my_currency,
              save_date: cash.save_date.slice(0, 10),
              delete: "    "
            }))

        return (
          <>
            <ListTitle>List of your cash:</ListTitle>
            <CashImage image={cash}></CashImage>
            <TableWrapper>
              <Table columns={columns} data={data} />
            </TableWrapper>
              <ListTitle>Add new cash</ListTitle>
                <Form onSubmit={this.handleSubmitAdd}>
                  <TextInput
                    type='number'
                    name='my_cash'
                    placeholder='my cash'
                    min="1"
                    onChange={this.handleFormInput}
                  />
                  <TextInput
                    type='date'
                    name='save_date'
                    placeholder='save date'
                    value={this.state.cash.save_date}
                    onChange={this.handleFormInput}
                  />
                  <SubmitButton type="submit" value="Add" />
                </Form>
          </>
        )
    }
}