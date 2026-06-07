import requests
from Data import conexion
from Data.models import User, Account

class DataHelper:

    def __init__(self):
        User.createTable(ifNotExists=True)
        Account.createTable(ifNotExists=True)

    def addUsuario(self, username, hashedPwd):
        User(username=username, password_hash=hashedPwd)

    def GetUsers(self, username):
        users = list(User.selectBy(username=username))
        if not users:
            return None
        return users[0].password_hash

    def getCuentas(self, username):
        users = list(User.selectBy(username=username))
        if not users:
            return {}
        user = users[0]
        cuentas = {}
        for acc in Account.selectBy(user=user):
            cuentas[acc.currency] = acc.balance
        return cuentas

    def saveCuentas(self, username, cuentas):
        users = list(User.selectBy(username=username))
        if not users:
            return
        user = users[0]
        Account.deleteBy(user=user)
        for moneda, saldo in cuentas.items():
            Account(user=user, currency=moneda, balance=str(saldo))

    API_KEY = "4f73f7de235a09288e8c1988da9b6fcf"
    FIXER_URL = "http://data.fixer.io/api"

    def get_rates(self, symbols="USD,ARS,EUR"):
        url = "{}/latest?access_key={}&symbols={}".format(self.FIXER_URL, self.API_KEY, symbols)
        resp = requests.get(url)
        data = resp.json()
        if not data.get("success"):
            raise Exception("Error al obtener cotizaciones de Fixer.io")
        return data["rates"]
