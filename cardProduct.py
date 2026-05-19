from product import FraudValidator, PaymentProcessor, ReceiptGenerator

class CardPaymentProcessor(PaymentProcessor):

    def pay(self, amount):
        print("Procesando el pago con la tajeta: ${}".format(amount))

class CardFraudValidator(FraudValidator):

    def validator(self, amount):
        print("validando el pago con tarjeta")
        return True
    
class CardReciptGenerator(ReceiptGenerator):

    def generate(self, amount):
        print("Recibo de Tajerta Generado por ${}".format(amount))