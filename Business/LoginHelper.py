import bcrypt
from decimal import Decimal
from tabulate import tabulate
from Data.dataHelper import DataHelper
from Business.Logger import Loger
from Business.factorys import Cardfactory, Mpfactory, Paypalfactory
from Business.payhelper import checkout

class LoginHelper:

    def __init__(self):
        self.dataHelper = DataHelper()
        self.loger = Loger()

    def sanitize(self, text):
        return text.strip()
    
    def CheckEqPwd(self, pwd1, pwd2):
        if pwd1 == pwd2:
            return
        else: 
            raise ValueError("Los passwords No son iguales, no coiciden")
        
    def prepareAndStorePwd(self, username, pwd):
        codePwd = pwd.encode('utf-8')
        hashedPwd = bcrypt.hashpw(codePwd,bcrypt.gensalt())
        self.dataHelper.addUsuario(username, hashedPwd.decode('utf-8'))
        self.loger.log("Usuario {} registrado correctamente".format(username))

    def checkUserAndPwd(self, username, pwd):
        hashedpwd = self.dataHelper.GetUsers(username)
        if hashedpwd is None:
            raise ValueError("Usuario/Contraseña inexistente")
        if bcrypt.checkpw(pwd.encode('utf-8'), hashedpwd.encode('utf-8')) == False:
            raise ValueError("Password Incorrecto")
        self.loger.log("Usuario {} inició sesión".format(username))

    def abrir_cuenta(self, username, moneda):
        
        #Esto verifica que este el usuario ingresado
        if self.dataHelper.GetUsers(username) is None:
            raise ValueError("El usuario no existe")

        #Esto valida que la moneda tenga las 3 letras
        moneda = moneda.strip().upper()
        if len(moneda) != 3 or not moneda.isalpha():
            raise ValueError("La moneda debe tener exactamente 3 letras (Ej: USD, ARS, EUR)")

        #Acá cargamo o creamos el archivo del usuario
        cuentas = self.dataHelper.getCuentas(username)

        #Esto verifica que ya haya una cuenta abierta con esa moneda
        if moneda in cuentas:
            raise ValueError("Ya existe una cuenta en {}".format(moneda))

        #Esto crea la cuenta en 0 con Decimal
        cuentas[moneda] = str(Decimal(0))

        #Esto ultimo guarda la cuenta y el registro qeu hicimos
        self.dataHelper.saveCuentas(username, cuentas)
        self.loger.log("Usuario {} abrió cuenta en {}".format(username, moneda))

    def listar_cuentas(self, username):
        cuentas = self.dataHelper.getCuentas(username)

        if not cuentas:
            print("No tenés cuentas abiertas todavía.")
            return

        tabla = [
            [moneda, Decimal(saldo)]
            for moneda, saldo in cuentas.items()
        ]
        print(tabulate(tabla, headers=["Moneda", "Saldo"], tablefmt="grid"))
            
    def depositar(self, username, moneda, monto):
        moneda = moneda.strip().upper()
    
        #Valiidamos que el monto que quiera ingresar esa positivo
        monto = Decimal(monto)
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")
    
        #Cargamos las cuentas
        cuentas = self.dataHelper.getCuentas(username)
    
        #Si no existe la cuenta, la crea automáticamente
        if moneda not in cuentas:
            print("No tenías cuenta en {}, se creó automáticamente.".format(moneda))
    
        #Sumamos el monto a lo que ya tiene o si no tiene nada usamos a 0
        cuentas[moneda] = str(Decimal(cuentas[moneda]) + monto)
    
        #Guardamos
        self.dataHelper.saveCuentas(username, cuentas)
        self.loger.log("Usuario {} depositó {} en {}".format(username, monto, moneda))

    def procesar_pago(self, username, metodo, monto):
        moneda = input("¿Desde qué cuenta querés pagar? (Ej: USD, ARS): \n").strip().upper()

        cuentas = self.dataHelper.getCuentas(username)
        if moneda not in cuentas:
            raise ValueError("No tenés una cuenta en {}".format(moneda))

        monto = Decimal(monto)
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        if Decimal(cuentas[moneda]) < monto:
            raise ValueError("Saldo insuficiente en {}".format(moneda))

        factory_map = {
            '1': Cardfactory,
            '2': Mpfactory,
            '3': Paypalfactory,
        }

        if metodo not in factory_map:
            raise ValueError("Método de pago inválido")

        factory = factory_map[metodo]()
        checkout(factory, monto)

        cuentas[moneda] = str(Decimal(cuentas[moneda]) - monto)
        self.dataHelper.saveCuentas(username, cuentas)
        self.loger.log("Usuario {} pagó {} con método {} desde cuenta {}".format(
            username, monto, metodo, moneda))

    def convertir_moneda(self, username, desde, hacia, monto):
        desde = desde.strip().upper()
        hacia = hacia.strip().upper()

        monto = Decimal(monto)
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        cuentas = self.dataHelper.getCuentas(username)
        if desde not in cuentas:
            raise ValueError("No tenés una cuenta en {}".format(desde))
        if Decimal(cuentas[desde]) < monto:
            raise ValueError("Saldo insuficiente en {}".format(desde))

        rates = self.dataHelper.get_rates()
        if desde not in rates:
            raise ValueError("Moneda {} no soportada por Fixer.io".format(desde))
        if hacia not in rates:
            raise ValueError("Moneda {} no soportada por Fixer.io".format(hacia))

        # Fixer.io usa EUR como base, calculamos la tasa entre las dos monedas
        tasa = Decimal(rates[hacia]) / Decimal(rates[desde])
        convertido = (monto * tasa).quantize(Decimal('.01'))

        cuentas[desde] = str(Decimal(cuentas[desde]) - monto)
        cuentas[hacia] = str(Decimal(cuentas.get(hacia, 0)) + convertido)
        self.dataHelper.saveCuentas(username, cuentas)

        self.loger.log("Usuario {} convirtió {} {} a {} {}".format(
            username, monto, desde, convertido, hacia))
        return tasa, convertido



        