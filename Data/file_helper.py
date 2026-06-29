import os
import json
from Data.data_interface import IDataHelper

class FileDataHelper(IDataHelper):

    def __init__(self, base_path=None):
        if base_path is None:
            _base = os.path.dirname(os.path.abspath(__file__))
            base_path = os.path.join(_base, "user_data")
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def _user_path(self, username):
        return os.path.join(self.base_path, "{}.json".format(username))

    def _load(self, username):
        path = self._user_path(username)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, username, data):
        path = self._user_path(username)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def addUsuario(self, username, hashedPwd):
        data = {
            "password_hash": hashedPwd,
            "accounts": {}
        }
        self._save(username, data)

    def GetUsers(self, username):
        data = self._load(username)
        if data is None:
            return None
        return data["password_hash"]

    def getCuentas(self, username):
        data = self._load(username)
        if data is None:
            return {}
        return data.get("accounts", {})

    def saveCuentas(self, username, cuentas):
        data = self._load(username)
        if data is None:
            return
        data["accounts"] = cuentas
        self._save(username, data)
