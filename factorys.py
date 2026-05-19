from Abstractfactorys import PaymentFactory
from cardProduct import CardReciptGenerator, CardPaymentProcessor, CardFraudValidator
from mpProduct import MpFraudValidator, MpPaymentProcessor, MpReciptGenerator
from paypalProducts import PaypalFraudValidator, PaypalPaymentProcessor, PaypalReceiptGenerator

class Cardfactory(PaymentFactory):
    
    def create_receipt_generator(self):
        return CardReciptGenerator()
    
    def create_payment_processor(self):
        return CardPaymentProcessor()

    def create_fraud_validator(self):
        return CardFraudValidator()
    

class Mpfactory(PaymentFactory):
    
    def create_receipt_generator(self):
        return MpReciptGenerator()
    
    def create_payment_processor(self):
        return MpPaymentProcessor()

    def create_fraud_validator(self):
        return MpFraudValidator()
    
class Paypalfactory(PaymentFactory):

    def create_payment_processor(self):
        return PaypalPaymentProcessor()
    
    def create_fraud_validator(self):
        return PaypalFraudValidator()
    
    def create_receipt_generator(self):
        return PaypalReceiptGenerator()
        