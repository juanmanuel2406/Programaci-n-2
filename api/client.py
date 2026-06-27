import requests

API = "http://127.0.0.1:5000"


def menu():
    print("\n--- CLIENTE API HOMEBAKING ---")
    print("1.  Listar monedas disponibles")
    print("2.  Cotizacion (GET)")
    print("3.  Cotizacion (POST)")
    print("4.  Registrar usuario")
    print("5.  Listar cuentas")
    print("6.  Abrir cuenta")
    print("7.  Depositar (PUT)")
    print("8.  Eliminar cuenta (DELETE)")
    print("9.  Comprar moneda")
    print("10. Pagar")
    print("0.  Salir")
    return input("Opcion: ").strip()


def main():
    while True:
        op = menu()
        match op:
            case "1":
                r = requests.get(API + "/monedas")
                print(r.status_code, r.json())

            case "2":
                code = input("Codigo de moneda: ").strip()
                r = requests.get(API + "/cotizacion", params={"codigo": code})
                print(r.status_code, r.json())

            case "3":
                code = input("Codigo de moneda: ").strip()
                r = requests.post(API + "/cotizacion", json={"codigo": code})
                print(r.status_code, r.json())

            case "4":
                user = input("Username: ").strip()
                pwd = input("Password: ").strip()
                r = requests.post(API + "/usuarios", json={"username": user, "password": pwd})
                print(r.status_code, r.json())

            case "5":
                user = input("Username: ").strip()
                r = requests.get(API + "/usuarios/{}/cuentas".format(user))
                print(r.status_code, r.json())

            case "6":
                user = input("Username: ").strip()
                moneda = input("Moneda (USD/ARS/EUR): ").strip()
                r = requests.post(API + "/usuarios/{}/cuentas".format(user),
                                  json={"moneda": moneda})
                print(r.status_code, r.json())

            case "7":
                user = input("Username: ").strip()
                moneda = input("Moneda: ").strip()
                monto = input("Monto: ").strip()
                r = requests.put(API + "/usuarios/{}/cuentas/{}".format(user, moneda),
                                 json={"monto": monto})
                print(r.status_code, r.json())

            case "8":
                user = input("Username: ").strip()
                moneda = input("Moneda a eliminar: ").strip()
                r = requests.delete(API + "/usuarios/{}/cuentas/{}".format(user, moneda))
                print(r.status_code, r.json())

            case "9":
                user = input("Username: ").strip()
                hacia = input("Moneda a comprar: ").strip()
                monto = input("Cantidad: ").strip()
                desde = input("Moneda de pago (Enter=ARS): ").strip() or "ARS"
                r = requests.post(API + "/usuarios/{}/comprar".format(user),
                                  json={"hacia": hacia, "monto": monto, "desde": desde})
                print(r.status_code, r.json())

            case "10":
                user = input("Username: ").strip()
                metodo = input("Metodo (1=Tarjeta, 2=MP, 3=PayPal): ").strip()
                moneda = input("Moneda de la cuenta: ").strip()
                monto = input("Monto: ").strip()
                r = requests.post(API + "/usuarios/{}/pagar".format(user),
                                  json={"metodo": metodo, "moneda": moneda, "monto": monto})
                print(r.status_code, r.json())

            case "0":
                break

            case _:
                print("Opcion invalida")


if __name__ == "__main__":
    main()
