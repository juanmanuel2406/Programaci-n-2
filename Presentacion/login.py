from Business.LoginHelper import LoginHelper
from getpass import getpass

class Login:

    def __init__(self, data_helper):
        self.loginHelper = LoginHelper(data_helper)
        self.usuarioLogueado = None

    def registrarUsuario(self):
        try:
            username = input("Por favor Ingrese el nombre de Usuario: \n")
            username = self.loginHelper.sanitize(username)
            pwd1 = getpass(prompt="Ingrese la contrase\u00f1a: \n")
            pwd2 = getpass("Por favor repita la contrase\u00f1a: \n")
            self.loginHelper.CheckEqPwd(pwd1, pwd2)
            self.loginHelper.prepareAndStorePwd(username, pwd1)
            print("Usuario {} creado correctamente.".format(username))
        except Exception as e:
            print("Error: {}".format(e))

    def IniciarSesion(self):
        while True:
            try:
                username = input("Por favor Ingrese el nombre de Usuario (0 para volver): \n")
                if username.strip() == '0':
                    return
                username = self.loginHelper.sanitize(username)
                pwd1 = getpass(prompt="Ingrese la contrase\u00f1a: \n")
                self.loginHelper.checkUserAndPwd(username, pwd1)
                self.usuarioLogueado = username
                print("Bienvenido {}".format(username))
                rv = True
                while rv:
                    rv = self.menuCuentas()
                return
            except ValueError as e:
                print("Error: {}\n".format(e))

    def deposito(self):
        try:
            moneda = input("\u00bfEn qu\u00e9 cuenta quer\u00e9s depositar? (Ej: USD, ARS): \n")
            monto = input("\u00bfCu\u00e1nto quer\u00e9s depositar?: \n")
            confirmacion = input("\u00bfEst\u00e1s seguro que quer\u00e9s depositar {} en {}? (s/n): \n".format(monto, moneda.strip().upper()))
            if confirmacion.strip().lower() != 's':
                print("Dep\u00f3sito cancelado.")
                return
            self.loginHelper.depositar(self.usuarioLogueado, moneda, monto)
            print("Dep\u00f3sito realizado correctamente.")
        except ValueError as e:
            print("Error: {}".format(e))

    def menuCuentas(self):
        print("\n" + 20*'-')
        print("Usuario: {}".format(self.usuarioLogueado))
        print("1. Abrir cuenta")
        print("2. Listar cuentas")
        print("3. Depositar")
        print("4. Pagar")
        print("5. Cambio de moneda")
        print("6. Comprar moneda extranjera")
        print("0. Cerrar sesi\u00f3n")
        op = input().strip()
        match op:
            case '1':
                self.abrirCuenta()
                return True
            case '2':
                self.loginHelper.listar_cuentas(self.usuarioLogueado)
                return True
            case '3':
                self.deposito()
                return True
            case '4':
                self.pagar()
                return True
            case '5':
                self.cambio()
                return True
            case '6':
                self.comprar()
                return True
            case '0':
                self.usuarioLogueado = None
                print("Sesi\u00f3n cerrada.")
                return False
            case _:
                print("Opci\u00f3n Incorrecta")
                return True

    def pagar(self):
        try:
            print("\nSeleccion\u00e1 el m\u00e9todo de pago:")
            print("1. Tarjeta")
            print("2. Mercado Pago")
            print("3. PayPal")
            metodo = input().strip()
            monto = input("\u00bfCu\u00e1nto quer\u00e9s pagar?: \n")
            confirmacion = input("\u00bfEst\u00e1s seguro de pagar {}? (s/n): \n".format(monto))
            if confirmacion.strip().lower() != 's':
                print("Pago cancelado.")
                return
            self.loginHelper.procesar_pago(self.usuarioLogueado, metodo, monto)
            print("Pago realizado correctamente.")
        except ValueError as e:
            print("Error: {}".format(e))

    def cambio(self):
        try:
            desde = input("\u00bfDe qu\u00e9 moneda quer\u00e9s convertir? (Ej: USD, ARS, EUR): \n")
            hacia = input("\u00bfA qu\u00e9 moneda quer\u00e9s convertir? (Ej: USD, ARS, EUR): \n")
            monto = input("\u00bfCu\u00e1nto quer\u00e9s convertir?: \n")
            tasa, convertido = self.loginHelper.convertir_moneda(
                self.usuarioLogueado, desde, hacia, monto)
            print("Tasa de cambio: 1 {} = {} {}".format(
                desde.strip().upper(), tasa, hacia.strip().upper()))
            print("Recibiste: {} {}".format(convertido, hacia.strip().upper()))
            print("Cambio realizado correctamente.")
        except ValueError as e:
            print("Error: {}".format(e))
        except Exception as e:
            print("Error de conexi\u00f3n con Fixer.io: {}".format(e))

    def comprar(self):
        try:
            hacia = input("\u00bfQu\u00e9 moneda quer\u00e9s comprar? (Ej: USD, EUR): \n")
            monto = input("\u00bfCu\u00e1nto quer\u00e9s comprar?: \n")
            desde = input("\u00bfCon qu\u00e9 moneda vas a pagar? (Ej: ARS, USD): \n").strip().upper()
            if not desde:
                desde = "ARS"
            confirmacion = input("\u00bfEst\u00e1s seguro de comprar {} {}? (s/n): \n".format(monto, hacia.strip().upper()))
            if confirmacion.strip().lower() != 's':
                print("Compra cancelada.")
                return
            tasa, costo = self.loginHelper.comprar_moneda(
                self.usuarioLogueado, hacia, monto, desde)
            print("Tasa de cambio: 1 {} = {} {}".format(
                hacia.strip().upper(), tasa, desde.upper()))
            print("Te cost\u00f3: {} {}".format(costo, desde.upper()))
            print("Compra realizada correctamente.")
        except ValueError as e:
            print("Error: {}".format(e))
        except Exception as e:
            print("Error de conexi\u00f3n con Fixer.io: {}".format(e))

    def abrirCuenta(self):
        try:
            moneda = input("Ingrese la moneda de la cuenta (Ej: USD, ARS, EUR): \n")
            self.loginHelper.abrir_cuenta(self.usuarioLogueado, moneda)
            print("Cuenta en {} abierta correctamente.".format(moneda.strip().upper()))
        except ValueError as e:
            print("Error: {}".format(e))

    def menu(self):
        print(20*'#', 'Bienvenido a la Aplicacion', 20*'#')
        print("Ingrese una Opcion: ")
        print("1. Iniciar Sesion: ")
        print("2. Crear Usuario (Registrarse): ")
        print("0. Salir: ")
        op = input().lstrip().rstrip()
        match op:
            case '1':
                self.IniciarSesion()
                return True
            case '2':
                self.registrarUsuario()
                return True
            case '0':
                return False
            case _:
                print("Opcion Incorrecta")
                return True
