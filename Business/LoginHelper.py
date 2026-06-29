import bcrypt
from decimal import Decimal
from tabulate import tabulate
from Data.data_interface import IDataHelper
from Business.fixer_service import FixerService
from Business.Logger import Loger
from Business.factorys import Cardfactory, Mpfactory, Paypalfactory
from Business.payhelper import checkout
from Business.exceptions import AccountNotFoundError, InsufficientBalanceError, CurrencyNotSupportedError, UserNotFoundError

class LoginHelper:

    def __init__(self, data_helper: IDataHelper, fixer_service: FixerService = None):
        self.dataHelper = data_helper
        self.fixer_service = fixer_service or FixerService()
        self.loger = Loger()

    def sanitize(self, text):
        return text.strip()

    def CheckEqPwd(self, pwd1, pwd2):
        if pwd1 == pwd2:
            return
        else:
            raise ValueError("Los passwords no son iguales, no coinciden")

    def prepareAndStorePwd(self, username, pwd):
        codePwd = pwd.encode('utf-8')
        hashedPwd = bcrypt.hashpw(codePwd, bcrypt.gensalt())
        self.dataHelper.addUsuario(username, hashedPwd.decode('utf-8'))
        self.loger.log("Usuario {} registrado correctamente".format(username))

    def checkUserAndPwd(self, username, pwd):
        hashedpwd = self.dataHelper.GetUsers(username)
        if hashedpwd is None:
            raise UserNotFoundError(username)
        if not bcrypt.checkpw(pwd.encode('utf-8'), hashedpwd.encode('utf-8')):
            raise ValueError("Password Incorrecto")
        self.loger.log("Usuario {} inici\u00f3 sesi\u00f3n".format(username))

    def abrir_cuenta(self, username, moneda):
        if self.dataHelper.GetUsers(username) is None:
            raise UserNotFoundError(username)

        moneda = moneda.strip().upper()
        if len(moneda) != 3 or not moneda.isalpha():
            raise ValueError("La moneda debe tener exactamente 3 letras (Ej: USD, ARS, EUR)")

        cuentas = self.dataHelper.getCuentas(username)
        if moneda in cuentas:
            raise ValueError("Ya existe una cuenta en {}".format(moneda))

        cuentas[moneda] = str(Decimal(0))
        self.dataHelper.saveCuentas(username, cuentas)
        self.loger.log("Usuario {} abri\u00f3 cuenta en {}".format(username, moneda))

    def listar_cuentas(self, username):
        cuentas = self.dataHelper.getCuentas(username)
        if not cuentas:
            print("No ten\u00e9s cuentas abiertas todav\u00eda.")
            return

        tabla = [
            [moneda, Decimal(saldo)]
            for moneda, saldo in cuentas.items()
        ]
        print(tabulate(tabla, headers=["Moneda", "Saldo"], tablefmt="grid"))

    def depositar(self, username, moneda, monto):
        moneda = moneda.strip().upper()
        monto = Decimal(monto)
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        cuentas = self.dataHelper.getCuentas(username)
        if moneda not in cuentas:
            raise AccountNotFoundError(moneda)

        cuentas[moneda] = str(Decimal(cuentas[moneda]) + monto)
        self.dataHelper.saveCuentas(username, cuentas)
        self.loger.log("Usuario {} deposit\u00f3 {} en {}".format(username, monto, moneda))

    def procesar_pago(self, username, metodo, monto, moneda):
        moneda = moneda.strip().upper()

        cuentas = self.dataHelper.getCuentas(username)
        if moneda not in cuentas:
            raise AccountNotFoundError(moneda)

        monto = Decimal(monto)
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        if Decimal(cuentas[moneda]) < monto:
            raise InsufficientBalanceError(moneda)

        factory_map = {
            '1': Cardfactory,
            '2': Mpfactory,
            '3': Paypalfactory,
        }

        if metodo not in factory_map:
            raise ValueError("M\u00e9todo de pago inv\u00e1lido")

        factory = factory_map[metodo]()
        checkout(factory, monto)

        cuentas[moneda] = str(Decimal(cuentas[moneda]) - monto)
        self.dataHelper.saveCuentas(username, cuentas)
        self.loger.log("Usuario {} pag\u00f3 {} con m\u00e9todo {} desde cuenta {}".format(
            username, monto, metodo, moneda))

    def convertir_moneda(self, username, desde, hacia, monto):
        desde = desde.strip().upper()
        hacia = hacia.strip().upper()

        monto = Decimal(monto)
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        cuentas = self.dataHelper.getCuentas(username)
        if desde not in cuentas:
            raise AccountNotFoundError(desde)
        if Decimal(cuentas[desde]) < monto:
            raise InsufficientBalanceError(desde)

        rates = self.fixer_service.get_rates()
        if desde not in rates:
            raise CurrencyNotSupportedError(desde)
        if hacia not in rates:
            raise CurrencyNotSupportedError(hacia)

        tasa = Decimal(rates[hacia]) / Decimal(rates[desde])
        convertido = (monto * tasa).quantize(Decimal('.01'))

        cuentas[desde] = str(Decimal(cuentas[desde]) - monto)
        cuentas[hacia] = str(Decimal(cuentas.get(hacia, 0)) + convertido)
        self.dataHelper.saveCuentas(username, cuentas)

        self.loger.log("Usuario {} convirti\u00f3 {} {} a {} {}".format(
            username, monto, desde, convertido, hacia))
        return tasa, convertido

    def comprar_moneda(self, username, hacia, monto_destino, desde="ARS"):
        desde = desde.strip().upper()
        hacia = hacia.strip().upper()

        monto_destino = Decimal(monto_destino)
        if monto_destino <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        cuentas = self.dataHelper.getCuentas(username)
        if desde not in cuentas:
            raise AccountNotFoundError(desde)

        rates = self.fixer_service.get_rates()
        if desde not in rates:
            raise CurrencyNotSupportedError(desde)
        if hacia not in rates:
            raise CurrencyNotSupportedError(hacia)

        tasa = Decimal(rates[hacia]) / Decimal(rates[desde])
        monto_origen = (monto_destino / tasa).quantize(Decimal('.01'))

        if Decimal(cuentas[desde]) < monto_origen:
            raise InsufficientBalanceError(desde)

        cuentas[desde] = str(Decimal(cuentas[desde]) - monto_origen)
        cuentas[hacia] = str(Decimal(cuentas.get(hacia, 0)) + monto_destino)
        self.dataHelper.saveCuentas(username, cuentas)

        self.loger.log("Usuario {} compr\u00f3 {} {} pagando {} {}".format(
            username, monto_destino, hacia, monto_origen, desde))
        return tasa, monto_origen
