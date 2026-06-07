from Business.product import FraudValidator, PaymentProcessor, ReceiptGenerator

class CardPaymentProcessor(PaymentProcessor):

    def pay(self, amount):
        print("Procesando el pago con la tarjeta: ${}".format(amount))

class CardFraudValidator(FraudValidator):

    def validator(self, amount):
        print("Validando el pago con tarjeta")
        return True

class CardReciptGenerator(ReceiptGenerator):

    def generate(self, amount):
        print("Recibo de Tarjeta Generado por ${}".format(amount))
