from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount, **kwargs):
        pass

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount: float, **kwargs) -> bool:
        card_number = kwargs.get('card_number')
        expiry = kwargs.get('expiry_date')
        cvv = kwargs.get('cvv')
        
        print(f"Processing credit card payment: ${amount}")
        return True  # Заглушка
    
class SBPPayment(PaymentStrategy):
    def pay(self, amount, **kwargs) -> bool:
        phone = kwargs.get('phone')
        bank_id = kwargs.get('bank_id')
        
        # ...
        print(f"Processing SBP payment: ${amount}")
        return True
    
class CashPayment(PaymentStrategy):
    def pay(self, amount, **kwargs) -> bool:
        # ...
        print(f"Cash payment on delivery: ${amount}")
        return True
    
class PaymentContext:
    def __init__(self, strategy: PaymentStrategy = None):
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def execute_payment(self, amount, **kwargs) -> bool:
        if not self._strategy:
            raise ValueError("Payment strategy not set")
        return self._strategy.pay(amount, **kwargs)