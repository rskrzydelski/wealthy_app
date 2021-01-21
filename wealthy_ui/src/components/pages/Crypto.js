import React, { Component } from 'react'
import Axios from 'axios'
import { Table } from '../Table'

import { SubmitButton, Form, TextInput, TextArea, SelectInput } from './css/metals'
import { ListTitle, DelButton, CashImage, TableWrapper } from './css/cash'
import crypto from '../../static/crypto.jpg'

import { 
    cryptoUrl,
    accountUrl,
    refreshTokenUrl
} from '../endpoints'

export default class Crypto extends Component {
    constructor (props) {
      super(props)
      this.state = {
        CryptoList: [],
        crypto: {
            name: "",
            bought_price: '',
            bought_price_currency: '',
            amount: '',
            date_of_bought: '',
            description: ''
        },
        my_currency: '',
    }
    }

    componentDidMount () {
        this.collectCrypto()
        this.getCurrency()
    }

    getCurrency = async () => {
      try {
          const res = await Axios.get(accountUrl, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
          const state = this.state
          state.crypto['bought_price_currency'] = res.data.my_currency
          if (res.data.my_currency === 'PLN') {
            state.my_currency = 'zł'
          } else if (res.data.my_currency === 'USD') {
            state.my_currency = '$'
          } else if (res.data.my_currency === 'EUR') {
            state.my_currency = '€'
          } else if (res.data.my_currency === 'CHF') {
            state.my_currency = 'chf'
          }
          this.setState({state})
      } catch (error) {
          if (error.response.status === 401) {
              const res = await Axios.post(refreshTokenUrl, {refresh: localStorage.getItem('refresh')})
              localStorage.setItem('access', res.data.access)
              this.getCurrency()
            }
      }
    }

    collectCrypto = async () => {
      try {
            const res = await Axios.get(cryptoUrl, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
            console.log(res)
            const CryptoList = [...this.state.CryptoList, ...res.data]
            this.setState({CryptoList})
        } catch (error) {
            if (error.response.status === 401) {
                const res = await Axios.post(refreshTokenUrl, {refresh: localStorage.getItem('refresh')})
                localStorage.setItem('access', res.data.access)
                this.collectCrypto()
              }
        }
    }

    onSubmitDel = async (e, id) => {
      e.preventDefault()
      try {
          await Axios.delete(cryptoUrl + '/' + id, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
          this.setState({CryptoList: []})
          this.collectCrypto()
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
          await Axios.post(cryptoUrl, this.state.crypto, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
          this.setState({CryptoList: []})
          this.collectCrypto()
      } catch (error) {
          if (error.response.status === 401) {
              const res = await Axios.post(refreshTokenUrl, {refresh: localStorage.getItem('refresh')})
              localStorage.setItem('access', res.data.access)
              this.onSubmitAdd(e)
            }
      }
    }

    handleFormInput = (event) => {
        const res = this.state.crypto
        res[event.target.name] = event.target.value
        this.setState({ crypto: res })
    }

    render() {
      const columns = [
        {
          Header: "My crypto",
          columns: [
            {
                Header: 'id',
                accessor: 'id',
              },
              {
                Header: 'name',
                accessor: 'name',
              },
              {
                Header: 'amount',
                accessor: 'amount',
              },
              {
                Header: 'bought price',
                accessor: 'bought_price',
              },
              {
                Header: 'date of bought',
                accessor: 'date_of_bought',
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

      const data = this.state.CryptoList.map((crypto) => (
            {
                id: crypto.id,
                name: crypto.name,
                amount: crypto.amount,
                bought_price: crypto.bought_price,
                date_of_bought: crypto.date_of_bought.slice(0, 10),
                delete: "    "
            }))

        return (
          <>
            <ListTitle>List of your crypto:</ListTitle>
            <CashImage image={crypto}></CashImage>
            <TableWrapper>
              <Table columns={columns} data={data} />
            </TableWrapper>
              <ListTitle>Add new crypto</ListTitle>
              <Form onSubmit={this.handleSubmitAdd}>
                <SelectInput id="crypto_name" name="name" onChange={this.handleFormInput}>
                  <option value="btc">bitcoin</option>
                  <option value="bch">bitcon cash</option>
                  <option value="eth">ethereum</option>
                  <option value="xrp">rippla</option>
                  <option value="ltc">litecoin</option>
                  <option value="dot">polkadot</option>
                  <option value="neo">neo</option>
                  <option value="flm">flamingo</option>
                  <option value="theta">theta</option>
                </SelectInput>
                <TextInput
                        type='number'
                        name='bought_price'
                        placeholder='bought price'
                        min="1"
                        onChange={this.handleFormInput}
                      />
                      <TextInput
                        type='number'
                        name='amount'
                        placeholder='amount'
                        step="0.0000000001"
                        onChange={this.handleFormInput}
                      />
                      <TextInput
                        type='date'
                        name='date_of_bought'
                        placeholder='date of bought'
                        value={this.state.crypto.date_of_bought}
                        onChange={this.handleFormInput}
                      />
                      <TextArea
                        name="description"
                        rows="4"
                        cols="50"
                        placeholder="description"
                        onChange={this.handleFormInput}
                      ></TextArea>
                  <SubmitButton type="submit" value="Add" />
                </Form>
          </>
        )
    }
}