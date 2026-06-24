from abc import ABC, abstractmethod

class IDataHelper(ABC):

    @abstractmethod
    def addUsuario(self, username, hashedPwd):
        pass

    @abstractmethod
    def GetUsers(self, username):
        pass

    @abstractmethod
    def getCuentas(self, username):
        pass

    @abstractmethod
    def saveCuentas(self, username, cuentas):
        pass
