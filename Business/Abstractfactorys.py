from abc import ABC, abstractmethod

class PaymentFactory(ABC):

    @abstractmethod
    def create_payment_processor(self):
        pass

    @abstractmethod
    def create_fraud_validator(self):
        pass

    @abstractmethod
    def create_receipt_generator(self):
        pass
