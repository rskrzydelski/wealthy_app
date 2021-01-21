#!/bin/bash

login() {
  echo $(http POST http://localhost:8000/api/v1/auth/login/ username=rafal email=rs@gmail.com password=rafael86 my_currency=USD | cut -d : -f 2 | cut -d , -f 1) | sed 's/"//' | sed 's/"//' | sed 's/}//'
}

TOKEN="$(login)"
echo $TOKEN
case $1 in
     register)
                 http POST http://localhost:8000/api/v1/auth/registration/ username="rafal" email="rs@gmail.com" password="rafael86" password2="rafael86" my_currency="CHF"
         ;;
     reset_password)
                 http POST http://localhost:8000/api/v1/users/password_reset/reset_password/ email="j@gmail.com"
         ;;
	 metals)
                 http GET http://localhost:8000/api/v1/resources/metals "Authorization: Token $TOKEN"
		 ;;
	 gold)
                 http GET http://localhost:8000/api/v1/resources/metals?name=gold "Authorization: Token $TOKEN"
		 ;;
     silver)
                 http GET http://localhost:8000/api/v1/resources/metals?name=silver "Authorization: Token $TOKEN"
		 ;;
	 silver_sum)
                 http GET http://localhost:8000/api/v1/resources/metals?name=silver\&sum=true "Authorization: Token $TOKEN"
		 ;;
	 gold_sum)
                 http GET http://localhost:8000/api/v1/resources/metals?name=gold\&sum=true "Authorization: Token $TOKEN"
		 ;;
     create_gold)
                 http POST http://localhost:8000/api/v1/resources/metals name="gold" bought_price="20000" amount="4" unit="oz" date_of_bought="2019-11-26T11:00:30Z" description="test gold create" "Authorization: Token $TOKEN"
		 ;;
	 create_gold_kg)
                 http POST http://localhost:8000/api/v1/resources/metals name="gold" bought_price="20000" amount="4" unit="kg" date_of_bought="2019-11-26T11:00:30Z" description="test gold create" "Authorization: Token $TOKEN"
		 ;;
	 metal_delete)
                 http DELETE http://localhost:8000/api/v1/resources/metals/4 "Authorization: Token $TOKEN"
		 ;;
	 currency)
                 http GET http://localhost:8000/api/v1/resources/currency "Authorization: Token $TOKEN"
		 ;;
	 usd)
                 http GET http://localhost:8000/api/v1/resources/currency?name=usd "Authorization: Token $TOKEN"
		 ;;
	 create_usd)
                 http POST http://localhost:8000/api/v1/resources/currency bought_currency="500" bought_currency_currency="USD" bought_price="2000" bought_price_currency="PLN" date_of_bought="2019-12-26T12:01:36Z" "Authorization: Token $TOKEN"
		 ;;
	 my_fortune)
                 http GET http://localhost:8000/api/v1/wallet "Authorization: Token $TOKEN"
		 ;;
	 metal_value)
                 http GET http://localhost:8000/api/v1/wallet/metal "Authorization: Token $TOKEN"
		 ;;
	 silver_value)
                 http GET http://localhost:8000/api/v1/wallet/metal/silver "Authorization: Token $TOKEN"
		 ;;
	 gold_value)
                 http GET http://localhost:8000/api/v1/wallet/metal/gold "Authorization: Token $TOKEN"
		 ;;
	 cash)
                 http GET http://localhost:8000/api/v1/wallet/cash "Authorization: Token $TOKEN"
		 ;;
	 currency_value)
                 http GET http://localhost:8000/api/v1/wallet/currency "Authorization: Token $TOKEN"
		 ;;
	 usd_value)
                 http GET http://localhost:8000/api/v1/wallet/currency/usd "Authorization: Token $TOKEN"
		 ;;
	 eur_value)
                 http GET http://localhost:8000/api/v1/wallet/currency/eur "Authorization: Token $TOKEN"
		 ;;
	 chf_value)
                 http GET http://localhost:8000/api/v1/wallet/currency/chf "Authorization: Token $TOKEN"
		 ;;
	 create_pln)
                 http POST http://localhost:8000/api/v1/resources/currency bought_currency="500" bought_currency_currency="PLN" bought_price="2000" bought_price_currency="PLN" date_of_bought="2019-12-26T12:01:36Z" "Authorization: Token $TOKEN"
		 ;;
	create_pln_pay_usd)
                 http POST http://localhost:8000/api/v1/resources/currency bought_currency="500" bought_currency_currency="PLN" bought_price="2000" bought_price_currency="USD" date_of_bought="2019-12-26T12:01:36Z" "Authorization: Token $TOKEN"
		 ;;
     *)
		 echo "Usage: test_client {metals|gold|silver|gold_sum|silver_sum|currency|usd|create_usd|my_fortune|metal_value|silver_value|gold_value|cash|currency_value|usd_value|eur_value|chf_value}"
		 ;;
 esac

 exit 0
