class Loger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def log(self, msg):
        self.logs.append(msg)

    def show_log(self):
        for log in self.logs:
            print(log)
