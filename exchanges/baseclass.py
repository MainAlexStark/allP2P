from abc import ABC, abstractmethod

class base_exchange(ABC):
    """
    Базовый класс для работы с P2P биржами и API бирж.
    """

    @abstractmethod
    async def get_p2p_offers(self, token: str = '', currency: str = '', side: bool = True, payment: list = [], size: str = '', amount: str = '') -> dict:
        """
        Получение P2P предложений.
        Возвращаемый формат:
        {
            "status": "success",
            "data": {
                "offers": data['result']['items'],
                "payments": list,
                "fiat": currency,
                "amount": amount,
                "timestamp": int(time.time())
            },
            "error": None
        }
        """
        pass

    @abstractmethod
    async def allPaymentList(self) -> dict:
        """
        Получение списка всех доступных методов оплаты.
        Возвращаемый формат:
        [
            {
                "name": "Bank Transfer",
                "num": 14
            },
            {
                "name": "7-Eleven",
                "num": 4
            },
            {
                "name": "A-Bank",
                "num": 1
            },
            {
                "name": "ABN AMRO",
                "num": 136
            }
        ]
        """
        pass

    @abstractmethod
    async def get_fiat(self) -> dict:
        """
        Получение списка всех фиатных валют.
        Возвращаемый формат:
        [
            {
                "payment_method": "Echeck",
                "fiat": [
                    "JPY"
                ]
            },
            {
                "payment_method": "Credit Card",
                "fiat": [
                    "UAH",
                    "EUR",
                    "PLN",
                    "SEK",
                    "HUF",
                    "DKK",
                    "RON",
                    "BGN",
                    "CZK"
                ]
            }
        ]
        """
        pass
    
    @abstractmethod
    async def tickers(self, symbol:str = ''):
        """
        Запрос всех тикетов
        Возвращаемый формат:
        [
            {
                "symbol": "RATSUSDT",
                "bid1Price": "0.0001405",
                "bid1Size": "3556187.76",
                "ask1Price": "0.0001406",
                "ask1Size": "90985.2",
                "lastPrice": "0.0001406",
                "prevPrice24h": "0.0001458",
                "price24hPcnt": "-0.0357",
                "highPrice24h": "0.0001551",
                "lowPrice24h": "0.0001359",
                "turnover24h": "2968919.889616968",
                "volume24h": "20198390192.64"
            },
            {
                "symbol": "VELARUSDT",
                "bid1Price": "0.06876",
                "bid1Size": "2386.33",
                "ask1Price": "0.06903",
                "ask1Size": "145.14",
                "lastPrice": "0.06903",
                "prevPrice24h": "0.07877",
                "price24hPcnt": "-0.1237",
                "highPrice24h": "0.07898",
                "lowPrice24h": "0.068",
                "turnover24h": "94586.0675693",
                "volume24h": "1316957.17"
            }
        ]
        """
        pass
        
    @abstractmethod
    async def get_convert_coin_list(self, coin: str = '', side: int = 0, account_type: str = 'eb_convert_funding') -> dict:
        """
        Запрос котировки для обмена криптовалют.
        Возвращаемый формат:
        [
            {
                "coin": "AGLD",
                "fullName": "AGLD",
                "icon": "https://s1.bycsi.com/app/assets/token/71c30ccc0c343d2f6ab830262ac7a5f8.svg",
                "iconNight": "https://s1.bycsi.com/app/assets/token/8eb2f2348cc917081be4c28b797bd930.svg",
                "accuracyLength": 8,
                "coinType": "crypto",
                "balance": "",
                "uBalance": "",
                "timePeriod": 0,
                "singleFromMinLimit": "5",
                "singleFromMaxLimit": "30000",
                "singleToMinLimit": "0",
                "singleToMaxLimit": "0",
                "dailyFromMinLimit": "0",
                "dailyFromMaxLimit": "0",
                "dailyToMinLimit": "0",
                "dailyToMaxLimit": "0",
                "disableFrom": false,
                "disableTo": false
            },
            {
                "coin": "AGLA",
                "fullName": "AGLA",
                "icon": "https://s1.bycsi.com/app/assets/token/1857d5971bed49d9b411032f54243128.svg",
                "iconNight": "https://s1.bycsi.com/app/assets/token/5bc128beb4db5e6091b3c4211e7e4c4e.svg",
                "accuracyLength": 8,
                "coinType": "crypto",
                "balance": "",
                "uBalance": "",
                "timePeriod": 0,
                "singleFromMinLimit": "0.1",
                "singleFromMaxLimit": "4000",
                "singleToMinLimit": "0",
                "singleToMaxLimit": "0",
                "dailyFromMinLimit": "0",
                "dailyFromMaxLimit": "0",
                "dailyToMinLimit": "0",
                "dailyToMaxLimit": "0",
                "disableFrom": false,
                "disableTo": false
            }
        ]
        """
        pass

    @abstractmethod
    async def request_quote(self, from_coin, to_coin, request_coin, request_amount, account_type, param_type=None, param_value=None, request_id=None) -> dict:
        """
        Запрос котировки для обмена криптовалют.
        Возвращаемый формат:
        {
            "status": "success",
            "data": {
                "offers": [],
                "payments": [],
                "fiat": [],
                "quote": {...},
                "balance": [],
                "convert_status": {},
                "convert_history": [],
                "timestamp": int
            },
            "error": {"code": ..., "message": ...}
        }
        """
        pass

    @abstractmethod
    async def confirm_quote(self, quote_tx_id) -> dict:
        """
        Подтверждение котировки для обмена криптовалют.
        Возвращаемый формат:
        {
            "status": "success",
            "data": {
                "offers": [],
                "payments": [],
                "fiat": [],
                "quote": {},
                "balance": [],
                "convert_status": {...},
                "convert_history": [],
                "timestamp": int
            },
            "error": {"code": ..., "message": ...}
        }
        """
        pass

    @abstractmethod
    async def get_convert_status(self, quote_tx_id, account_type) -> dict:
        """
        Получение статуса обмена криптовалют.
        Возвращаемый формат:
        {
            "status": "success",
            "data": {
                "offers": [],
                "payments": [],
                "fiat": [],
                "quote": {},
                "balance": [],
                "convert_status": {...},
                "convert_history": [],
                "timestamp": int
            },
            "error": {"code": ..., "message": ...}
        }
        """
        pass

    @abstractmethod
    async def get_convert_history(self, account_type=None, index=1, limit=20) -> dict:
        """
        Получение истории обмена криптовалют.
        Возвращаемый формат:
        {
            "status": "success",
            "data": {
                "offers": [],
                "payments": [],
                "fiat": [],
                "quote": {},
                "balance": [],
                "convert_status": {},
                "convert_history": [...],
                "timestamp": int
            },
            "error": {"code": ..., "message": ...}
        }
        """
        pass

    @abstractmethod
    async def get_balance(self, coin: str = None) -> dict:
        """
        Получение баланса.
        Возвращаемый формат:
        {
            "status": "success",
            "data": {
                "offers": [],
                "payments": [],
                "fiat": [],
                "quote": {},
                "balance": [...],
                "convert_status": {},
                "convert_history": [],
                "timestamp": int
            },
            "error": {"code": ..., "message": ...}
        }
        """
        pass
