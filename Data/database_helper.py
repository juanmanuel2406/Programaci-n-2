from Data import conexion
from Data.models import User, Account
from Data.data_interface import IDataHelper

class DatabaseHelper(IDataHelper):

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
