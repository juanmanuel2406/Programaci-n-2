def checkout(factory, amout):
    validator = factory.create_fraud_validator()

    if not validator.validator(amout): 
        raise Exception("Pago Rechazado")
    
    procesador = factory.create_payment_processor()
    procesador.pay(amout)

    recipt = factory.create_receipt_generator()
    recipt.generate(amout)