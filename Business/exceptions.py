class AccountNotFoundError(Exception):
    def __init__(self, currency):
        self.currency = currency
        super().__init__("La cuenta en {} no existe".format(currency))

class InsufficientBalanceError(Exception):
    def __init__(self, currency):
        self.currency = currency
        super().__init__("Saldo insuficiente en {}".format(currency))

class CurrencyNotSupportedError(Exception):
    def __init__(self, currency):
        self.currency = currency
        super().__init__("Moneda {} no soportada por Fixer.io".format(currency))

class UserNotFoundError(Exception):
    def __init__(self, username):
        self.username = username
        super().__init__("El usuario {} no existe".format(username))
