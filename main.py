def main():
    from Business.login import Login
    running = True
    while running:
        print("\nSeleccion\u00e1 el m\u00e9todo de persistencia:")
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

        login = Login(data_helper)
        try:
            running = login.menu()
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break

if __name__ == "__main__":
    main()
