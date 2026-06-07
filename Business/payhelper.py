def checkout(factory, amount):
    validator = factory.create_fraud_validator()

    if not validator.validator(amount):
        raise Exception("Pago Rechazado")

    procesador = factory.create_payment_processor()
    procesador.pay(amount)

    recipt = factory.create_receipt_generator()
    recipt.generate(amount)
