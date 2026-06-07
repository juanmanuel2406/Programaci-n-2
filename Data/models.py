import sqlobject as SO

class User(SO.SQLObject):
    username = SO.StringCol(length=100, varchar=True, unique=True)
    password_hash = SO.StringCol(length=255, varchar=True)

class Account(SO.SQLObject):
    user = SO.ForeignKey('User')
    currency = SO.StringCol(length=3, varchar=True)
    balance = SO.StringCol(length=50, varchar=True)
