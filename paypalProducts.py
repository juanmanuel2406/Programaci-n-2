from product import FraudValidator, ReceiptGenerator, PaymentProcessor

class PaypalPaymentProcessor(PaymentProcessor):
    def pay(self, amount):
        print("Procesando el pago con PayPal: ${}".format(amount))

class PaypalReceiptGenerator(ReceiptGenerator):
    def generate(self, amount):
        print("Recibo de PayPal Generado por ${}".format(amount))

class PaypalFraudValidator(FraudValidator):
    def validator(self, amount):
        print("Validando el pago con PayPal")
        return True