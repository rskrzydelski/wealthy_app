import React, { Component } from 'react'
import Axios from 'axios'
import { Table } from '../Table'
import gold_img from '../../static/gold_bars.jpg'
import silver_img from '../../static/silver_bars.jpg'

import { 
    metalsUrl,
    metalsGold999Url, 
    metalsGold585Url, 
    metalsGold333Url,
    metalsSilver999Url,
    metalsSilver800Url,
    accountUrl,
    refreshTokenUrl
} from '../endpoints'

import { SubmitButton, Form, TextInput, TextArea, SelectInput } from './css/metals'
import { ListTitle, TableWrapper, DelButton, MetalImage } from './css/metals'


export default class Metals extends Component {
    constructor (props) {
      super(props)
      let name;
      if (this.props.resource === 'gold') {
          name = 'gold999'
      } else if (this.props.resource === 'silver') {
          name = 'silver999'
      }
      this.state = {
          MetalList: [],
          resource: {
              name: name,
              bought_price: '',
              bought_price_currency: '',
              amount: '',
              unit: 'oz',
              date_of_bought: '',
              description: ''
          },
          my_currency: '',
      }
    }

    componentDidMount () {
        this.collectMetals(this.props.resource)
        this.getCurrency()
    }

    getCurrency = async () => {
        try {
            const res = await Axios.get(accountUrl, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
            const state = this.state
            state.resource['bought_price_currency'] = res.data.my_currency
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

    collectMetals = async (resource) => {
      try {
        if (resource === 'gold') {
            const metalsGold999Promise = Axios(metalsGold999Url, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
            const metalsGold585Promise = Axios(metalsGold585Url, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
            const metalsGold333Promise = Axios(metalsGold333Url, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
            
            const res = await Promise.all([metalsGold999Promise, metalsGold585Promise, metalsGold333Promise])
            const MetalList = [...this.state.MetalList, ...res[0].data, ...res[1].data, ...res[2].data]
            this.setState({MetalList})
        } else if (resource === 'silver') {
            const metalsSilver999Promise = Axios(metalsSilver999Url, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
            const metalsSilver800Promise = Axios(metalsSilver800Url, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
            
            const res = await Promise.all([metalsSilver999Promise, metalsSilver800Promise])
            const MetalList = [...this.state.MetalList, ...res[0].data, ...res[1].data]
            this.setState({MetalList})
        }
        } catch (error) {
            if (error.response.status === 401) {
                const res = await Axios.post(refreshTokenUrl, {refresh: localStorage.getItem('refresh')})
                localStorage.setItem('access', res.data.access)
                this.collectMetals(resource)
              }
        }
    }

    onSubmitDel = async (e, id) => {
        e.preventDefault()
        try {
            const res = await Axios.delete(metalsUrl + '/' + id, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
            this.setState({MetalList: []})
            this.collectMetals(this.props.resource)
        } catch (error) {
            if (error.response.status === 401) {
                const res = await Axios.post(refreshTokenUrl, {refresh: localStorage.getItem('refresh')})
                localStorage.setItem('access', res.data.access)
                this.onSubmitDel(e, id)
              }
        }
      }

    onSubmitAdd = async (e) => {
        e.preventDefault()
        try {
            const res = await Axios.post(metalsUrl, this.state.resource, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
            this.setState({MetalList: []})
            this.collectMetals(this.props.resource)
        } catch (error) {
            if (error.response.status === 401) {
                const res = await Axios.post(refreshTokenUrl, {refresh: localStorage.getItem('refresh')})
                localStorage.setItem('access', res.data.access)
                this.onSubmitAdd(e)
              }
        }
    }

    handleFormInput = (event) => {
        const res = this.state.resource
        res[event.target.name] = event.target.value
        this.setState({ resource: res })
    }

    ble = (val) => {
      console.log("sdasdsa")
      console.log(val)
    }

    render() {
        let options;
        let image;
        if (this.props.resource === 'gold') {
            options = <React.Fragment>
               <option value="gold999">gold999</option>
               <option value="gold585">gold585</option>
               <option value="gold333">gold333</option>
             </React.Fragment>
             image = gold_img
        } else if (this.props.resource === 'silver') {
            options = <React.Fragment>
              <option value="silver999">silver999</option>
              <option value="silver800">silver800</option>
             </React.Fragment>
             image = silver_img
        }

        const columns = [
          {
            Header: this.props.resource,
            columns: [
              {
                Header: 'id',
                accessor: 'id',
              },
              {
                Header: 'resource',
                accessor: 'name',
              },
              {
                Header: 'amount',
                accessor: 'amount',
              },
              {
                Header: 'unit',
                accessor: 'unit',
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

        const data = this.state.MetalList.map((metal) => (
              {
                id: metal.id,
                name: metal.name,
                amount: metal.amount,
                unit: metal.unit,
                bought_price: metal.bought_price,
                date_of_bought: metal.date_of_bought.slice(0, 10),
                delete: "    "
              }))

        return (
          <>
            <ListTitle>List of your {this.props.resource}:</ListTitle>
            <MetalImage image={image}></MetalImage>
            <TableWrapper>
              <Table columns={columns} data={data} />
            </TableWrapper>

                <ListTitle>Add new metal</ListTitle>
                <Form onSubmit={(e) => this.onSubmitAdd(e, this.state)}>
                      <SelectInput id="resource_name" name="name" onChange={this.handleFormInput}>
                        {options}
                      </SelectInput>
                      <SelectInput id="resource_unit" name="unit" onChange={this.handleFormInput}>
                        <option value="oz">ounce</option>
                        <option value="g">gram</option>
                        <option value="kg">kilogram</option>
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
                        min="1"
                        onChange={this.handleFormInput}
                      />
                      <TextInput
                        type='date'
                        name='date_of_bought'
                        placeholder='date of bought'
                        value={this.state.resource.date_of_bought}
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