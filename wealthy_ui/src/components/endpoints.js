const serverUrl = 'http://127.0.0.1:8000'
// const serverUrl = 'http://192.168.1.3'

const apiEntry = '/api/v1/'

// authentication endpoints
export const loginUrl = `${serverUrl}${apiEntry}auth/jwt/create/`
export const refreshTokenUrl = `${serverUrl}${apiEntry}auth/jwt/refresh/`
export const registerUrl = `${serverUrl}${apiEntry}auth/users/`
export const accountUrl = `${serverUrl}${apiEntry}auth/users/me/`

// metals market prices
export const marketGold999ozUrl = `${serverUrl}${apiEntry}market/metals?name=gold999&unit=oz`
export const marketGold999gUrl = `${serverUrl}${apiEntry}market/metals?name=gold999&unit=g`
export const marketGold999kgUrl = `${serverUrl}${apiEntry}market/metals?name=gold999&unit=kg`

export const marketGold585ozUrl = `${serverUrl}${apiEntry}market/metals?name=gold585&unit=oz`
export const marketGold585gUrl = `${serverUrl}${apiEntry}market/metals?name=gold585&unit=g`
export const marketGold585kgUrl = `${serverUrl}${apiEntry}market/metals?name=gold585&unit=kg`

export const marketGold333ozUrl = `${serverUrl}${apiEntry}market/metals?name=gold333&unit=oz`
export const marketGold333gUrl = `${serverUrl}${apiEntry}market/metals?name=gold333&unit=g`
export const marketGold333kgUrl = `${serverUrl}${apiEntry}market/metals?name=gold333&unit=kg`

export const marketSilver999ozUrl = `${serverUrl}${apiEntry}market/metals?name=silver999&unit=oz`
export const marketSilver800gUrl = `${serverUrl}${apiEntry}market/metals?name=silver800&unit=g`

// crypto market prices
export const marketBtcUrl = `${serverUrl}${apiEntry}market/cryptos?name=btc`
export const marketBchUrl = `${serverUrl}${apiEntry}market/cryptos?name=bch`
export const marketEthUrl = `${serverUrl}${apiEntry}market/cryptos?name=eth`
export const marketXrpUrl = `${serverUrl}${apiEntry}market/cryptos?name=xrp`
export const marketLtcUrl = `${serverUrl}${apiEntry}market/cryptos?name=ltc`
export const marketDotUrl = `${serverUrl}${apiEntry}market/cryptos?name=dot`
export const marketNeoUrl = `${serverUrl}${apiEntry}market/cryptos?name=neo`
export const marketFlmUrl = `${serverUrl}${apiEntry}market/cryptos?name=flm`
export const marketThetaUrl = `${serverUrl}${apiEntry}market/cryptos?name=theta`


// wallets
// metal wallet
export const walletGold999Url = `${serverUrl}${apiEntry}wallet/metals/gold999`
export const walletGold585Url = `${serverUrl}${apiEntry}wallet/metals/gold585`
export const walletGold333Url = `${serverUrl}${apiEntry}wallet/metals/gold333`
export const walletSilver999Url = `${serverUrl}${apiEntry}wallet/metals/silver999`
export const walletSilver800Url = `${serverUrl}${apiEntry}wallet/metals/silver800`

// crypto wallet
export const walletBtcUrl = `${serverUrl}${apiEntry}wallet/crypto/btc`
export const walletBchUrl = `${serverUrl}${apiEntry}wallet/crypto/bch`
export const walletEthUrl = `${serverUrl}${apiEntry}wallet/crypto/eth`
export const walletXrpUrl = `${serverUrl}${apiEntry}wallet/crypto/xrp`
export const walletLtcUrl = `${serverUrl}${apiEntry}wallet/crypto/ltc`
export const walletDotUrl = `${serverUrl}${apiEntry}wallet/crypto/dot`
export const walletNeoUrl = `${serverUrl}${apiEntry}wallet/crypto/neo`
export const walletFlmUrl = `${serverUrl}${apiEntry}wallet/crypto/flm`
export const walletThetaUrl = `${serverUrl}${apiEntry}wallet/crypto/theta`

// cash wallet
export const walletCashUrl = `${serverUrl}${apiEntry}wallet/cash`

// all wallets
export const walletUrl = `${serverUrl}${apiEntry}wallet`

// resources
export const metalsUrl = `${serverUrl}${apiEntry}resources/metals`
export const metalsGold999Url = `${serverUrl}${apiEntry}resources/metals?name=gold999`
export const metalsGold585Url = `${serverUrl}${apiEntry}resources/metals?name=gold585`
export const metalsGold333Url = `${serverUrl}${apiEntry}resources/metals?name=gold333`
export const metalsSilver999Url = `${serverUrl}${apiEntry}resources/metals?name=silver999`
export const metalsSilver800Url = `${serverUrl}${apiEntry}resources/metals?name=silver800`
export const cashUrl = `${serverUrl}${apiEntry}resources/cash`
export const cryptoUrl = `${serverUrl}${apiEntry}resources/crypto`
