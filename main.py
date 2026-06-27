def run_console():
    print("Seleccion\u00e1 el m\u00e9todo de persistencia:")
    print("1. Base de datos (SQLObject)")
    print("2. Archivos serializados")
    op = input().strip()

    if op == "2":
        from Data.file_helper import FileDataHelper
        data_helper = FileDataHelper()
        print("Usando persistencia basada en archivos serializados.")
    else:
        from Data.database_helper import DatabaseHelper
        data_helper = DatabaseHelper()
        print("Usando persistencia basada en base de datos (SQLObject).")

    from Presentacion.login import Login
    login = Login(data_helper)
    running = True
    while running:
        try:
            running = login.menu()
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break


def run_api():
    from api.server import app
    print("API corriendo en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)


def main():
    print("=== HOMEBAKING APP ===")
    print("1. Interfaz de consola")
    print("2. Servidor API REST")
    op = input().strip()

    if op == "2":
        run_api()
    else:
        run_console()


if __name__ == "__main__":
    main()
