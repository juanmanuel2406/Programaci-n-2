from product import FraudValidator, PaymentProcessor, ReceiptGenerator

class MpPaymentProcessor(PaymentProcessor):

    def pay(self, amount):
        print("Procesando el pago de Mercado Pago: ${}".format(amount))

class MpFraudValidator(FraudValidator):

    def validator(self, amount):
        print("validando el pago de Mercado Pago")
        return True
    
class MpReciptGenerator(ReceiptGenerator):

    def generate(self, amount):
        print("Recibo de Mercado Pago Generado por ${}".format(amount))