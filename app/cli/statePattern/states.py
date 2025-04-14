from abc import ABC, abstractmethod
import time
from datetime import datetime

class OrderState(ABC):
    @abstractmethod
    def get_status(self):
        pass

    @abstractmethod
    def next(self, order: 'Order'):
        pass

class Order:
    def __init__(self, order_id, total):
        self.order_id = order_id
        self.total = total
        self.created_at = datetime.now()
        self.state: OrderState = ProcessingState()
    
    def get_status(self):
        return self.state.get_status()
    
    def update_status(self):
        self.state.next(self)
    
    def track(self, interval: 5.0):
        print(f"\nОтслеживание заказа #{self.order_id} на сумму ${self.total}")
        while not isinstance(self.state, DeliveredState):
            print(f"\nТекущий статус: {self.get_status()}")
            time.sleep(interval)
            self.update_status()
        print("\nЗаказ успешно доставлен")

class ProcessingState(OrderState):
    def get_status(self):
        return "В обработке (сборка заказа)"

    def next(self, order: Order):
        order.state = ShippedState()

class ShippedState(OrderState):
    def get_status(self):
        return "В пути (доставка)"

    def next(self, order: Order):
        order.state = ReadyForPickupState()

class ReadyForPickupState(OrderState):
    def get_status(self) -> str:
        return "Ожидает получения (в пункте выдачи)"

    def next(self, order: Order):
        order.state = DeliveredState()

class DeliveredState(OrderState):
    def get_status(self):
        return "Получен (заказ закрыт)"

    def next(self, order: Order):
        pass
