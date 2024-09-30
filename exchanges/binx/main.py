import aiohttp
import asyncio
from exchanges.baseclass import P2PApi

class binx(P2PApi):
    async def online(self):
        url = "https://api-app.qq-os.com/api/c2c/v1/advert/list"
    
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "app_version": "8.5.10",
            "appid": "30004",
            "appsiteid": "0",
            "authorization": "Bearer eyJicyI6MCwiYWlkIjoxMDAwOSwicGlkIjoiMzAiLCJzaWQiOiJlMTA0MGVmY2U1MDg0MDk4MDIwNzIwOGJkOWMxODllMyIsImFsZyI6IkhTNTEyIn0.eyJzdWIiOiIxMjk5NTUwNjQ2OTMwOTU2MjkyIiwiZXhwIjoxNzI2MDczMjA3LCJqdGkiOiIzYzhmYWQxOS04ZDk1LTQyZWEtOTkzZi0xN2FhZTFkYzM1YjIifQ.YlHch7Ft_HknqjWmsHykbLch3ZzEU2CA4PzYtvt43MCBCg3CO6eCRnRIQesMXggxkgPw_HtB-Hn9wXbIVtbGzQ",
            "cache-control": "no-cache",
            "channel": "official",
            "cookie": "__cf_bm=3n5pzKrDnBjYOT5vzQjc.pFl6HMBKYfvVp_vreAXCA8-1725641150-1.0.1.1-yPMPi6M9j9yooBNj8543nZ0cJC8oPC_hIwO87pzS.SLcXaCqCsryiJ9vd6JtWepcU5VhDCN4rlz3vGz4NITCfA",
            "device_brand": "Windows 10_Chrome_128.0.0.0",
            "device_id": "f384f0957e694095bbc82e0f0c2bffdb",
            "lang": "ru-RU",
            "mainappid": "10009",
            "origin": "https://bingx.paycat.com",
            "platformid": "30",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://bingx.paycat.com/",
            "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "sign": "8169AEEC3D5D4B61579595A3D9187628CEBFBBA3B5B4E0D819235D3166EFFE0F",
            "timestamp": "1725641262386",
            "timezone": "3",
            "traceid": "5477deb18e3e468d971ffeb12f5b71ab",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

        params = {
            "type": "1",
            "fiat": "RUB",
            "asset": "USDT",
            "amount": "",
            "hidePaymentInfo": "",
            "payMethodId": "",
            "isUserMatchCondition": "false"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    print(data["data"]["dataList"][1])  # Выводим результат
                else:
                    print(f"Ошибка: {response.status}")
    

# Запуск асинхронной функции
BinX = binx()
asyncio.run(BinX.online())