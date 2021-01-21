# wealth api

## endpoints

<b>1. api/v1/users</b><br>
   - api/v1/users/\<pk\><br>
     - description: user details
     - allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
     - query params: None
     - e.g. response:<br>
     ```json
     {
       "id": 1,
       "username": "Rafael",
       "my_currency": "PLN"
     }
     ```
<b>2. api/v1/auth/</b><br>
   - description: external lib: django-rest-auth

<b>3. api/v1/resources</b>
   - api/v1/resources/metals
     - description: list all metals, with query specify particular metal name to get list only with those metal, 
       with particular name you can add sum param to achieve summary 
       of all particular metal (all oz and cash spend)
     - allow: GET, POST, HEAD, OPTIONS
     - query params: name=<gold/silver>, sum=<true> 
     - e.g. response without query params (chunk of list):<br>
     ```json
     {
       "name": "silver",
       "amount": "120",
       "unit": "oz",
       "bought_price": "9240.00",
       "date_of_bought": "2019-03-20T08:28:53Z"
     }
     ```
     - e.g. response with query param ?name=silver&sum=true:<br>
     ```json
     {
       "name": "silver",
       "unit": "oz",
       "total_amount": "202",
       "total_cash_spend": "16188.65"
     }
     ```
   - api/v1/resources/metals\<pk\></b>
     - description: metal detail
     - allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
     - query params: None
     - e.g. response:<br>
     ```json
     {
       "owner": 1,
       "name": "silver",
       "bought_price": "808.40 zł",
       "amount": "10",
       "unit": "oz",
       "date_of_bought": "2019-11-22T08:30:51Z",
       "description": ""
     }
     ```
   - api/v1/resources/metals/currency</b>
     - description: list all currencies with query specify particular currency name to get list only with those currency, 
       with particular name you can add sum param to achieve summary 
     - allow: GET, POST, HEAD, OPTIONS
     - query params: name=<usd/eur/chf/pln>, sum=<true>
     - e.g. response:<br>
     ```json
     {
       "currency": "CHF",
       "bought_currency": "250.00",
       "bought_price": "1000.00",
       "date_of_bought": "2020-02-19T21:13:45Z"
     },
     {
       "currency": "CHF",
       "bought_currency": "170.00",
       "bought_price": "800.00",
       "date_of_bought": "2020-02-19T21:14:26Z"
     }
     ```
     - e.g. response with query param ?name=chf&sum=true:<br>
     ```json
     {
       "currency": "CHF",
       "total_currency": "420"
     }
     ```
   - api/v1/resources/metals/currency/\<pk\></b>
     - description: currency detail
     - allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
     - query params: None
     - e.g. response:<br>
     ```json
     {
       "currency": "CHF",
       "bought_currency": "250.00",
       "bought_price": "1000.00",
       "date_of_bought": "2020-02-19T21:13:45Z"
     }
     ```
   - api/v1/resources/cash</b>
     - description: list all saved cash with query specify, you can add sum param to achieve summary of your cash 
     - allow: GET, POST, HEAD, OPTIONS
     - query params: sum=<true>
     - e.g. response:<br>
     ```json
     {
       "my_currency": "PLN",
       "save_date": "2020-02-20T14:00:16Z",
       "my_cash": "1000.00"
     },
     {
       "my_currency": "PLN",
       "save_date": "2020-02-20T14:00:24Z",
       "my_cash": "23090.00"
     }
     ```
     - e.g. response with query param ?name=chf&sum=true:<br>
     ```json
     {
       "my_currency": "PLN",
       "total_cash": "24090"
     }
     ```
   - api/v1/resources/cash/\<pk\><br>
     - description: cash detail
     - allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
     - query params: None
     - e.g. response:<br>
     ```json
     {
       "owner": 1,
       "save_date": "2020-02-20T14:00:16Z",
       "my_cash": "1000.00"
     }
     ```

<b>4. api/v1/wallet</b>
   - api/v1/wallet</b>
     - description: summary of all assets (result in your currency)
     - allow: 
     - query params: None
     - e.g. response:<br>
     ```json
     {
       "title": "Summary of my all assets in my currency",
       "my_fortune": "24090.00"
     }
     ```
   - api/v1/wallet/metals</b>
     - description: summary of all metals value
     - allow:
     - query params: None
     - e.g. response:<br>
     ```json
     {
       "name": "All metals",
       "my_currency": "PLN",
       "total_cash": "21043.84",
       "total_cash_spend": "22156.54",
       "profit": "-1112.70"
     }
     ```
   - api/v1/wallet/metals/gold</b>
     - description: summary of all gold value
     - allow:
     - query params: None
     - e.g. response:<br>
     ```json
     {
       "name": "gold",
       "my_currency": "PLN",
       "total_cash": "6405.07",
       "total_cash_spend": "5967.89",
       "profit": "437.18"
     }
     ```
   - api/v1/wallet/metals/silver</b>
     - description: summary of all silver value
     - allow:
     - query params: None
     - e.g. response:<br>
     ```json
     {
       "name": "silver",
       "my_currency": "PLN",
       "total_cash": "14639.58",
       "total_cash_spend": "16188.65",
       "profit": "-1549.07"
     }
     ```
   - api/v1/wallet/cash</b>
     - description: summary of all cash
     - allow:
     - query params: None
     - e.g. response:<br>
     ```json
     {
       "my_currency": "PLN",
       "cash": "24090.00"
     }
     ```
   - api/v1/wallet/currency</b>
     - description: value of all currences
     - allow:
     - query params: None
     - e.g. response:<br>
     ```json
     {
       "total_value": "0.00",
       "currency_name": "All currences"
     }
     ```
   - api/v1/wallet/currency/chf</b>
     - description: value of chf
     - allow:
     - query params: None
     - e.g. response:<br>
     ```json
     {
       "total_value": "0.00",
       "currency_name": "chf"
     }
     ```
   - api/v1/wallet/currency/usd</b>
     - description: value of usd
     - allow:
     - query params: None
     - e.g. response:<br>
     ```json
     {
       "total_value": "0.00",
       "currency_name": "usd"
     }
     ```
   - api/v1/wallet/currency/eur</b>
     - description: value of eur
     - allow:
     - query params: None
     - e.g. response:<br>
     ```json
     {
       "total_value": "0.00",
       "currency_name": "eur"
     }
     ```
   - api/v1/wallet/currency/pln</b>
     - description: value of pln
     - allow:
     - query params: None
     - e.g. response:<br>
     ```json
     {
       "total_value": "0.00",
       "currency_name": "pln"
     }
     ```