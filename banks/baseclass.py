from abc import ABC, abstractmethod

# Base class банка
class BankApi(ABC):
    
    @abstractmethod
    async def balance(self):
        pass
    
    @abstractmethod
    async def transfer(self, card_number: str, amount: float):
        pass
    
    @abstractmethod
    async def history(self, start_date=None, end_date=None):
        pass
    
    # Недостающие методы
    
    @abstractmethod
    async def get_card_details(self):
        """
        Получение деталей карты для перевода.
        """
        pass
    
    @abstractmethod
    async def get_transfer_fee(self, amount: float):
        """
        Получение комиссии за перевод на карту.
        """
        pass
