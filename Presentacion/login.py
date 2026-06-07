from Business.LoginHelper import LoginHelper
from getpass import getpass

class Login:

    def __init__(self):
        self.loginHelper = LoginHelper()
        self.usuarioLogueado = None  # guarda el username tras el login

    def registrarUsuario(self):
        try:
            username = input("Porfavor Ingrese el nombre de Usuario: \n")
            username = self.loginHelper.sanitize(username)
            pwd1 = getpass(prompt="Ingrese la contraseña: \n")
            pwd2 = getpass("Porfavor repita la contraseña")
            self.loginHelper.CheckEqPwd(pwd1, pwd2)
            self.loginHelper.prepareAndStorePwd(username,pwd1)
            print("Usuario {} creado correctamente.".format(username))
        except Exception as e:
            print("Error: {}".format(e.args[0]))

    def IniciarSesion(self):
        while True:
            try:
                username = input("Porfavor Ingrese el nombre de Usuario (0 para volver): \n")
                if username.strip() == '0':
                    return
                username = self.loginHelper.sanitize(username)
                pwd1 = getpass(prompt="Ingrese la contraseña: \n")
                self.loginHelper.checkUserAndPwd(username, pwd1)
                self.usuarioLogueado = username
                print("Bienvenido {}".format(username))
                rv = True
                while rv:
                    rv = self.menuCuentas()
                return
            except ValueError as e:
                print("Error: {}\n".format(e.args[0]))

    def deposito(self):
        try:
            moneda = input("¿En qué cuenta querés depositar? (Ej: USD, ARS): \n")
            monto = input("¿Cuánto querés depositar?: \n")
            confirmacion = input("¿Estás seguro que querés depositar {} en {}? (s/n): \n".format(monto, moneda.strip().upper()))
            if confirmacion.strip().lower() != 's':
                print("Depósito cancelado.")
                return
            self.loginHelper.depositar(self.usuarioLogueado, moneda, monto)
            print("Depósito realizado correctamente.")
        except ValueError as e:
            print("Error: {}".format(e.args[0]))

    def menuCuentas(self):
        print("\n" + 20*'-')
        print("Usuario: {}".format(self.usuarioLogueado))
        print("1. Abrir cuenta")
        print("2. Listar cuentas")
        print("3. Depositar")
        print("4. Pagar")
        print("5. Cambio de moneda")
        print("0. Cerrar sesion")
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
            case '0':
                self.usuarioLogueado = None
                print("Sesion cerrada.")
                return False
            case _:
                print("Opcion Incorrecta")
                return True

    def pagar(self):
        try:
            print("\nSeleccioná el método de pago:")
            print("1. Tarjeta")
            print("2. Mercado Pago")
            print("3. PayPal")
            metodo = input().strip()
            monto = input("¿Cuánto querés pagar?: \n")
            confirmacion = input("¿Estás seguro de pagar {}? (s/n): \n".format(monto))
            if confirmacion.strip().lower() != 's':
                print("Pago cancelado.")
                return
            self.loginHelper.procesar_pago(self.usuarioLogueado, metodo, monto)
            print("Pago realizado correctamente.")
        except ValueError as e:
            print("Error: {}".format(e.args[0]))

    def cambio(self):
        try:
            desde = input("¿De qué moneda querés convertir? (Ej: USD, ARS, EUR): \n")
            hacia = input("¿A qué moneda querés convertir? (Ej: USD, ARS, EUR): \n")
            monto = input("¿Cuánto querés convertir?: \n")
            tasa, convertido = self.loginHelper.convertir_moneda(
                self.usuarioLogueado, desde, hacia, monto)
            print("Tasa de cambio: 1 {} = {} {}".format(
                desde.strip().upper(), tasa, hacia.strip().upper()))
            print("Recibiste: {} {}".format(convertido, hacia.strip().upper()))
            print("Cambio realizado correctamente.")
        except ValueError as e:
            print("Error: {}".format(e.args[0]))
        except Exception as e:
            print("Error de conexión con Fixer.io: {}".format(e.args[0]))

    def abrirCuenta(self):
        try:
            moneda = input("Ingrese la moneda que quiera comprar (Ej: USD, ARS, EUR): \n")
            self.loginHelper.abrir_cuenta(self.usuarioLogueado, moneda)
            print("Cuenta en {} abierta correctamente.".format(moneda.strip().upper()))
        except ValueError as e:
            print("Error: {}".format(e.args[0]))

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





