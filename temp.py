import requests

def get_withdraw_methods(response_data):
    methods = response_data['result']['withdrawsSwitchConfigs']
    
    for method in methods:
        chain = method['chainName']
        fee = method['fee']
        min_withdraw = method['withdrawMin']
        max_withdraw = method['withdrawMax']
        recovery_time = method['withdrawSwitchRecoveryTime']
        
        print(f"Цепочка: {chain}")
        print(f"Комиссия: {fee} USDT")
        print(f"Минимальная сумма вывода: {min_withdraw} USDT")
        print(f"Максимальная сумма вывода: {max_withdraw} USDT")
        print(f"Время восстановления: {recovery_time}")
        print("-" * 30)

def fetch_bybit_coin_config():
    url = "https://api2.bybit.com/v3/private/cht/asset-withdraw/withdraw/coin-config?coin=USDT"
    
    # Заголовки
    headers = {
        "authority": "api2.bybit.com",
        "method": "GET",
        "path": "/v3/private/cht/asset-withdraw/withdraw/coin-config?coin=USDT",
        "scheme": "https",
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "guid": "b8b0ddf1-280b-ab3b-4b80-8d00aca61866",
        "origin": "https://www.bybit.com",
        "platform": "pc",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.bybit.com/",
        "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "traceparent": "00-3aa9ada6869933eca7fd4120cf82b527-d874784919ac7a2f-01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    
    # Новые куки
    cookies = {
        "_by_l_g_d": "a9f4f8d0-3cd5-4129-8a5e-4568b7a61877",
        "deviceId": "6057d48f-e76b-4b98-bf91-5696293df701",
        "_fwb": "209YjKtLRrNAaGkryPdvn8O.1825057894451",
        "_gcl_au": "1.1.7896254517.1825057901",
        "_ga": "GA1.2.907156272.1825057901",
        "tmr_lvid": "1270967856905e5d7a5835d12201aef7",
        "tmr_lvidTS": "1825057901055",
        "_fbp": "fb.1.1825057901078.123456789123456",
        "_tt_enable_cookie": "1",
        "_ttp": "89S-APX_LKpxzdBL9QDdWz4ksyw",
        "_ym_uid": "1825057901677721598",
        "_ym_d": "1825057901",
        "_gcl_gs": "2.1.k1$i182505790123",
        "_gcl_aw": "GCL.182505790213.Cj0KCQjw4an3BRD4ARIsAABAv8N3QDMo3deLV-58zAK_F8FiHMeVzpmzAS8Fm4wR3fJZLgAzz35ueZD0AAmRaEALw_wcB",
        "BYBIT_REG_REF_prod": '{"lang":"ru-RU","g":"a9f4f8d0-3cd5-4129-8a5e-4568b7a61877","referrer":"www.bing.com/","source":"bing.com","medium":"affiliate","affiliate_id":"RXH23WJ","group_id":"515015","group_type":"1","url":"https://www.bybit.com/en/invite/?affiliate_id=RXH23WJ&group_id=515015&group_type=1&ref_code=RXH23WJ&gad_source=1&gclid=Cj0KCQjw2nXhBhDSARIsAARKZy53FZ0NzzWjZzEaHmA9gpwG4ZZMkzJSasMx7slT4srmzKsTaUjvMDzYaakScEALw_wcB","last_refresh_time":"Wed, 20 Sep 2024 11:30:30 GMT"}',
        "_ym_isad": "2",
        "detection_time": "1827868000000",
        "secure-token": "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMDQ2OTUxODMsImIiOjAsInAiOjMsInVhIjoiIiwiZ2VuX3RzIjoxODI1MDU4MjE2LCJleHAiOjE4MjUwNTk0MDYsIm5zIjoiIiwiZXh0Ijp7IlN0YXRpb24tVHlwZSI6IiIsIm1jdCI6IjE2OTUyMTMwMDYiLCJzaWQiOiJCTFlCSVQifX0.oLmvYGSUMjz82qcQ5dNfSgqC87N3fyfHfn9bUVoMb9p51Uj9cqvQudZa0w91DRHkJwK15kjRm5xlPOB2asxUhw"
    }
    
    # Выполняем запрос
    response = requests.get(url, headers=headers, cookies=cookies)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
        print(get_withdraw_methods(data))
    else:
        print(f"Ошибка {response.status_code}: {response.text}")

# Вызов функции
fetch_bybit_coin_config()
