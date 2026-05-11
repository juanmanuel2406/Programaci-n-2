#Cotizacion de Moneda 1: USD a Moneda 2: ARS ==> 1 USD = X ARS
from decimal import Decimal,getcontext,ROUND_UP
getcontext().prec = 28
USD = Decimal(1.17828)
ARS = Decimal(1641.533813)

X = (ARS / USD).quantize(Decimal('.01'), rounding=ROUND_UP)

print("Un dolar (USD) son {} ARS".format(X))