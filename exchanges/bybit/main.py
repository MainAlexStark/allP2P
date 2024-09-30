import asyncio
import codecs
from exchanges.baseclass import base_exchange
from pybit.unified_trading import HTTP
import aiohttp
import hashlib
import hmac
import json
import time
from loguru import logger

class bybit(base_exchange):
    def __init__(self, API_KEY: str, API_SECRET: str) -> None:
        self._name = "bybit"
        self._url = "https://api.bybit.com"
        self._recv_window = str(5000)  # Инициализация recv_window
        
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        self.session = HTTP(api_key=API_KEY, api_secret=API_SECRET)
        super().__init__()

    async def get_p2p_offers(self, token: str = '', currency: str = '', side: bool = True, payment: list = [], size: str = '', amount: str = '') -> dict:
        if side == True: side_str = "Покупка" 
        else: side_str = "Продажа" 
        logger.debug(f"{self._name}:\t Получние p2p ордеров side:{side_str} token:{token} currency:{currency} payment:{payment} size:{size} amount:{amount}")
        
        try:
            url = "https://api2.bybit.com/fiat/otc/item/online"
            headers = {'Content-Type': 'application/json'}
            payload = {
                "userId": 104477147,
                "tokenId": token,
                "currencyId": currency,
                "payment": payment,
                "side": str(int(side)),
                "size": size,
                "amount": amount,
                "authMaker": False,
                "canTrade": False,
                "itemRegion": 2
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                                "status": "success",
                                "data": {
                                    "offers": data['result']['items'],
                                    "payments": payment,
                                    "fiat": currency,
                                    "amount": amount,
                                    "timestamp": int(time.time())
                                },
                                "error": None
                            }
                    else:
                        return {"status": "error", "data": None, "error": {"code": response.status, "message": "Failed to get offers"}}
        except Exception as e:
            return {"status": "error", "data": None, "error": {"code": -1, "message": str(e)}}

    async def allPaymentList(self) -> dict:
        logger.debug(f"{self._name}:\t Получние всех платежных методов и их номеров")
        
        try:
            url = "https://api2.bybit.com/fiat/otc/configuration/queryAllPaymentList"
            headers = {'Content-Type': 'application/json'}
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        payments = [{'name': item['paymentName'], 'num': int(item['paymentType'])} for item in data['result']['paymentConfigVo']]
                        return payments
                    else:
                        return {"status": "error", "data": None, "error": {"code": response.status, "message": "Failed to get payment list"}}
        except Exception as e:
            return {"status": "error", "data": None, "error": {"code": -1, "message": str(e)}}

    async def get_fiat(self) -> dict:
        logger.debug(f"{self._name}:\t Получние всех fiat по платежным методам")
        
        try:
            url = "https://api2.bybit.com/fiat/public/channel/common-config-batch?scene=fiat_service_support"
            headers = {'Content-Type': 'application/json'}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        fiat_list = [{'payment_method': item['payment_method'], 'fiat': item['fiat']} for item in data['result']['fiat_service_support']['list']]
                        return fiat_list
                    else:
                        return {"status": "error", "data": None, "error": {"code": response.status, "message": "Failed to get fiat list"}}
        except Exception as e:
            return {"status": "error", "data": None, "error": {"code": -1, "message": str(e)}}
        
    async def tickers(self, symbol:str = ''):
        logger.debug(f"{self._name}:\t Получние всех тикетов")

        try:
            # Получение баланса кошелька
            response = self.session.get_tickers(
                category='spot',
                symbol=symbol,
            )

            if response['retCode'] == 0:
                return response['result']['list']
            else:
                return {"error": response.get('retMsg')}
        except Exception as e:
            return {"error": str(e)}
        
    async def get_convert_coin_list(self, coin: str = '', side: int = 0) -> dict:
        logger.debug(f"{self._name}:\t Получние монет в которые можно конвертировать {coin}")
        
        """
        Получение списка монет для конвертации.

        :param coin: Монета, верхний регистр.
        :param side: 0 - список монет для конвертации (fromCoin), 1 - список монет для покупки (toCoin).
        :return: Список монет и их спецификаций.
        """
        try:
            endpoint = "/v5/asset/exchange/query-coin-list"
            params = {
                "coin": coin,
                "side": side,
                "accountType": 'eb_convert_funding'
            }

            # Преобразуем параметры в строку запроса
            query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
            
            # Генерация timestamp и подписи
            timestamp = str(int(time.time() * 1000))
            payload = timestamp + self.API_KEY + self._recv_window + query_string
            signature = hmac.new(self.API_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()

            headers = {
                'X-BAPI-API-KEY': self.API_KEY,
                'X-BAPI-SIGN': signature,
                'X-BAPI-SIGN-TYPE': '2',
                'X-BAPI-TIMESTAMP': timestamp,
                'X-BAPI-RECV-WINDOW': self._recv_window,
                'Content-Type': 'application/json'
            }

            # Выполняем запрос
            async with aiohttp.ClientSession() as session:
                async with session.get(self._url + endpoint + "?" + query_string, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "status": "success",
                            "data": data['result']['coins'],
                            "error": None
                        }
                    else:
                        return {
                            "status": f"error {response.status}",
                            "data": None,
                            "error": {
                                "code": response.status,
                                "message": "Failed to get convert coin list"
                            }
                        }
        except Exception as e:
            return {
                "status": "error",
                "data": None,
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }

    async def request_quote(self, from_coin: str, to_coin: str, request_coin: str, request_amount: str, param_value: str) -> dict:
        logger.debug(f"{self._name}:\t Запрос на конвертацию {request_amount} {from_coin} в {to_coin}")

        """
        Отправка запроса на конвертацию монеты.

        :param from_coin: Монета для конвертации.
        :param to_coin: Целевая монета.
        :param request_coin: Монета, которую запрашивают для обмена.
        :param request_amount: Сумма монеты для обмена.
        :param param_value: Значение параметра для "opFrom" (например, broker ID).
        :return: Ответ с результатами конвертации.
        """
        try:
            endpoint = "/v5/asset/exchange/quote-apply"
            params = {
                "requestId": f"convert-{int(time.time())}",  # Генерация уникального ID для запроса
                "fromCoin": from_coin,
                "toCoin": to_coin,
                "accountType": "eb_convert_funding",
                "requestCoin": request_coin,
                "requestAmount": request_amount,
                "paramType": "opFrom",
                "paramValue": param_value
            }

            # Генерация timestamp и подписи
            timestamp = str(int(time.time() * 1000))
            payload = timestamp + self.API_KEY + self._recv_window + json.dumps(params)
            signature = hmac.new(self.API_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()

            headers = {
                'X-BAPI-API-KEY': self.API_KEY,
                'X-BAPI-SIGN': signature,
                'X-BAPI-SIGN-TYPE': '2',
                'X-BAPI-TIMESTAMP': timestamp,
                'X-BAPI-RECV-WINDOW': self._recv_window,
                'Content-Type': 'application/json'
            }

            # Выполняем запрос
            async with aiohttp.ClientSession() as session:
                async with session.post(self._url + endpoint, headers=headers, json=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "status": "success",
                            "data": data['result'],
                            "error": None
                        }
                    else:
                        return {
                            "status": f"error {response.status}",
                            "data": None,
                            "error": {
                                "code": response.status,
                                "message": "Failed to apply coin conversion"
                            }
                        }
        except Exception as e:
            return {
                "status": "error",
                "data": None,
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }

    async def confirm_quote(self, quote_tx_id: str) -> dict:
        logger.debug(f"{self._name}:\t Выполнение конвертации с quoteTxId: {quote_tx_id}")

        """
        Выполнение конвертации монеты на основе полученного идентификатора транзакции.

        :param quote_tx_id: Идентификатор транзакции котировки (quoteTxId).
        :return: Ответ с результатами конвертации.
        """
        try:
            endpoint = "/v5/asset/exchange/convert-execute"
            params = {
                "quoteTxId": quote_tx_id
            }

            # Генерация timestamp и подписи
            timestamp = str(int(time.time() * 1000))
            payload = timestamp + self.API_KEY + self._recv_window + json.dumps(params)
            signature = hmac.new(self.API_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()

            headers = {
                'X-BAPI-API-KEY': self.API_KEY,
                'X-BAPI-SIGN': signature,
                'X-BAPI-SIGN-TYPE': '2',
                'X-BAPI-TIMESTAMP': timestamp,
                'X-BAPI-RECV-WINDOW': self._recv_window,
                'Content-Type': 'application/json'
            }

            # Выполняем запрос
            async with aiohttp.ClientSession() as session:
                async with session.post(self._url + endpoint, headers=headers, json=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "status": "success",
                            "data": data['result'],
                            "error": None
                        }
                    else:
                        return {
                            "status": f"error {response.status}",
                            "data": None,
                            "error": {
                                "code": response.status,
                                "message": "Failed to execute coin conversion"
                            }
                        }
        except Exception as e:
            return {
                "status": "error",
                "data": None,
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }

    async def get_convert_status(self, quote_tx_id: str) -> dict:
        logger.debug(f"{self._name}:\t Получение результата конвертации для quoteTxId: {quote_tx_id}")

        """
        Получение результата конвертации монеты на основе идентификатора транзакции.

        :param quote_tx_id: Идентификатор транзакции котировки (quoteTxId).
        :return: Ответ с результатами конвертации.
        """
        try:
            endpoint = "/v5/asset/exchange/convert-result-query"
            params = {
                "quoteTxId": quote_tx_id,
                "accountType": "eb_convert_funding"
            }

            # Преобразуем параметры в строку запроса
            query_string = '&'.join([f"{key}={value}" for key, value in params.items()])

            # Генерация timestamp и подписи
            timestamp = str(int(time.time() * 1000))
            payload = timestamp + self.API_KEY + self._recv_window + query_string
            signature = hmac.new(self.API_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()

            headers = {
                'X-BAPI-API-KEY': self.API_KEY,
                'X-BAPI-SIGN': signature,
                'X-BAPI-SIGN-TYPE': '2',
                'X-BAPI-TIMESTAMP': timestamp,
                'X-BAPI-RECV-WINDOW': self._recv_window,
                'Content-Type': 'application/json'
            }

            # Выполняем запрос
            async with aiohttp.ClientSession() as session:
                async with session.get(self._url + endpoint + "?" + query_string, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "status": "success",
                            "data": data['result'],
                            "error": None
                        }
                    else:
                        return {
                            "status": f"error {response.status}",
                            "data": None,
                            "error": {
                                "code": response.status,
                                "message": "Failed to get conversion result"
                            }
                        }
        except Exception as e:
            return {
                "status": "error",
                "data": None,
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }


    async def get_convert_history(self) -> dict:
        """
        Получние истории конвертации
        """
        
        logger.debug(f"{self._name}:\t Получение истории конвертации")

        try:
            endpoint = "/v5/asset/exchange/query-convert-history"
            params = {
                "accountType": 'eb_convert_funding'
            }

            # Преобразуем параметры в строку запроса
            query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
            
            # Генерация timestamp и подписи
            timestamp = str(int(time.time() * 1000))
            payload = timestamp + self.API_KEY + self._recv_window + query_string
            signature = hmac.new(self.API_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()

            headers = {
                'X-BAPI-API-KEY': self.API_KEY,
                'X-BAPI-SIGN': signature,
                'X-BAPI-SIGN-TYPE': '2',
                'X-BAPI-TIMESTAMP': timestamp,
                'X-BAPI-RECV-WINDOW': self._recv_window,
                'Content-Type': 'application/json'
            }

            # Выполняем запрос
            async with aiohttp.ClientSession() as session:
                async with session.get(self._url + endpoint + "?" + query_string, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "status": "success",
                            "data": data['result']['list'],
                            "error": None
                        }
                    else:
                        return {
                            "status": f"error {response.status}",
                            "data": None,
                            "error": {
                                "code": response.status,
                                "message": "Failed to get convert coin list"
                            }
                        }
        except Exception as e:
            return {
                "status": "error",
                "data": None,
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }


    async def get_balance(self, coin: str = None) -> dict:
        if coin == None: msg_coin = "все"
        logger.debug(f"{self._name}:\t Получение баланса кошелька coin: {msg_coin}")
        
        try:
            response = self.session.get_wallet_balance(
                accountType="UNIFIED",
                coin=coin,
            )
            if response['retCode'] == 0:
                return response['result']['list']
            else:
                return {"error": response.get('retMsg')}
        except Exception as e:
            return {"error": str(e)}


async def main():
    start_time = time.time()  # Замеряем время начала выполнения запроса

    ByBit = bybit(API_KEY='2wLA4pijamlJrcEoUH', API_SECRET='z3yRKDCafmLfvemYEcQkI9QBCIWwbGPTvnf6')
    #result = await ByBit.get_p2p_offers(payment=['581'], token="USDT", currency="RUB", size='1')
    result = await ByBit.get_balance()
    print(json.dumps(result, indent=4))
    
    #ByBit.print_methods()

    end_time = time.time()  # Замеряем время окончания выполнения запроса
    execution_time = end_time - start_time  # Вычисляем время выполнения
    print(f"Запрос выполнен за {execution_time:.4f} секунд")

asyncio.run(main())