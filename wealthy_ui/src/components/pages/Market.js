import React, { Component } from 'react'
import Axios from 'axios'

import { 
  marketGold999ozUrl,
  marketGold585gUrl,
  marketSilver999ozUrl,
  marketSilver800gUrl,
  marketBtcUrl,
  marketEthUrl,
  marketFlmUrl,
  marketLtcUrl,
  accountUrl,
  refreshTokenUrl
} from '../endpoints'

import { MarketContainer, MarketItem, MarketText, TextSpan } from './css/market'
import { Gold999Icon, Gold585Icon, Silver800Icon, Silver999Icon, FlmIcon, EthIcon, LtcIcon, BtnIcon } from './css/market'

export default class Market extends Component {
    constructor (props) {
        super(props)
        this.state = {
          market: {
            gold999oz: '',
            gold585g: '',
            silver999oz: '',
            silver800g: '',
            btc: '',
            eth: '',
            flm: '',
            ltc: '',
          },
            my_currency: ''
        }
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

  getMarketData = async () => {
    try {
      const gold999Promise = Axios(marketGold999ozUrl, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
      const gold585Promise = Axios(marketGold585gUrl, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
      const silver999Promise = Axios(marketSilver999ozUrl, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
      const silver800Promise = Axios(marketSilver800gUrl, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})

      const BtcPromise = Axios(marketBtcUrl, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
      const EthPromise = Axios(marketEthUrl, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
      const LtcPromise = Axios(marketLtcUrl, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})
      const FlmPromise = Axios(marketFlmUrl, {headers: {authorization: 'JWT ' + localStorage.getItem('access')}})

      const res = await Promise.all([gold999Promise, gold585Promise, silver999Promise, silver800Promise, BtcPromise, EthPromise, LtcPromise, FlmPromise])
      var market = {...this.state.market}
      market.gold999oz = res[0].data.price
      market.gold585g = res[1].data.price
      market.silver999oz = res[2].data.price
      market.silver800g = res[3].data.price
      market.btc = res[4].data.price
      market.eth = res[5].data.price
      market.ltc = res[6].data.price
      market.flm = res[7].data.price

      this.setState({market})
    } catch (error) {
      console.log(error)
      if (error.response.status === 401) {
        const res = await Axios.post(refreshTokenUrl, {refresh: localStorage.getItem('refresh')})
        localStorage.setItem('access', res.data.access)
        this.getMarketData()
      } 
    }
  }

  componentDidMount () {
    this.getMarketData()
    this.getCurrency()
    const timer = 60 * 1000
    this.myInterval = setInterval(this.getMarketData, timer)
  }

  componentWillUnmount() {
      clearInterval(this.myInterval)
  }

  render() {
    return (
        <MarketContainer>
            <MarketItem>
                <Gold999Icon />
                <MarketText>
                  <TextSpan>Gold 999 oz: </TextSpan>
                  <TextSpan>{this.state.market.gold999oz} {this.state.my_currency}</TextSpan>
                </MarketText>
            </MarketItem>
            <MarketItem>
                <Gold585Icon />
                <MarketText>
                  <TextSpan>Gold 585 g: </TextSpan>
                  <TextSpan>{this.state.market.gold585g} {this.state.my_currency}</TextSpan>
                </MarketText>
            </MarketItem>
            <MarketItem>
                <Silver999Icon />
                <MarketText>
                  <TextSpan>Silver 999 oz: </TextSpan>
                  <TextSpan>{this.state.market.silver999oz} {this.state.my_currency}</TextSpan>
                </MarketText>
            </MarketItem>
            <MarketItem>
                <Silver800Icon />
                <MarketText>
                  <TextSpan>Silver 800 g: </TextSpan>
                  <TextSpan>{this.state.market.silver800g} {this.state.my_currency}</TextSpan>
                </MarketText>
            </MarketItem>
            <MarketItem>
                <BtnIcon />
                <MarketText>
                  <TextSpan>BTC: </TextSpan>
                  <TextSpan>{this.state.market.btc} {this.state.my_currency}</TextSpan>
                </MarketText>
            </MarketItem>
            <MarketItem>
                <EthIcon />
                <MarketText>
                  <TextSpan>ETH: </TextSpan>
                  <TextSpan>{this.state.market.eth} {this.state.my_currency}</TextSpan>
                </MarketText>
            </MarketItem>
            <MarketItem>
                <FlmIcon />
                <MarketText>
                  <TextSpan>FLM: </TextSpan>
                  <TextSpan>{this.state.market.flm} {this.state.my_currency}</TextSpan>
                </MarketText>
            </MarketItem>
            <MarketItem>
                <LtcIcon />
                <MarketText>
                  <TextSpan>LTC: </TextSpan>
                  <TextSpan>{this.state.market.ltc} {this.state.my_currency}</TextSpan>
                </MarketText>
            </MarketItem>
          </MarketContainer>
    )
  }
}
