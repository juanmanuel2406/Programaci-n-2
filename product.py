from abc import ABC, abstractmethod

class PaymentProcessor(ABC):

    @abstractmethod
    def pay(self, amount):
        pass

class FraudValidator(ABC):

    @abstractmethod
    def validator(self, amount):
        pass    

class ReceiptGenerator(ABC):

    @abstractmethod
    def generate(self, amount):
        pass    