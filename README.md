# Homebanking - Compra y Venta de Moneda Extranjera

Aplicaci\u00f3n de consola para operaciones bancarias con soporte de m\u00faltiples
monedas, m\u00e9todos de pago y dos implementaciones de persistencia intercambiables.

## Arquitectura

El sistema sigue una arquitectura en capas con inversi\u00f3n de dependencias:

```
Presentaci\u00f3n (login.py)  -->  Negocio (LoginHelper)  -->  Datos (IDataHelper)
                                         |                        |
                                    FixerService          DatabaseHelper / FileDataHelper
```

### Capas

- **Presentaci\u00f3n** (`Presentacion/`): Interfaz de consola. Solicita datos al
usuario y muestra resultados. Depende de la capa de negocio mediante una
instancia de `LoginHelper`.

- **Negocio** (`Business/`): Contiene la l\u00f3gica de la aplicaci\u00f3n
(`LoginHelper`), el servicio de cotizaciones (`FixerService`), el patr\u00f3n
Abstract Factory para m\u00e9todos de pago (`factorys.py`, `product.py`,
`cardProduct.py`, `mpProduct.py`, `paypalProducts.py`), y el Logger como
singleton (`Logger.py`).

- **Datos** (`Data/`): Define una interfaz abstracta `IDataHelper` que es
implementada por `DatabaseHelper` (SQLObject) y `FileDataHelper` (archivos
serializados). La capa de negocio recibe la implementaci\u00f3n por inyecci\u00f3n
de dependencias, lo que permite intercambiarlas sin modificar c\u00f3digo de
negocio ni presentaci\u00f3n.

## Persistencia: intercambio entre implementaciones

Ambas implementaciones cumplen la misma interfaz `IDataHelper`
(`Data/data_interface.py`) con los m\u00e9todos:
- `addUsuario(username, hashedPwd)`
- `GetUsers(username)` -> str or None
- `getCuentas(username)` -> dict {moneda: saldo}
- `saveCuentas(username, cuentas)`

### 1. Base de datos (SQLObject) - `DatabaseHelper`

Utiliza SQLite por defecto (configurable a MySQL v\u00eda `.env`). Los modelos
se definen en `Data/models.py` y la conexi\u00f3n en `Data/conexion.py`.

### 2. Archivos serializados - `FileDataHelper`

Guarda cada usuario en un archivo `.pkl` dentro de `Data/user_data/` usando
pickle de Python. Cada archivo contiene el hash de la contrase\u00f1a y un
diccionario de cuentas.

### Selecci\u00f3n en tiempo de ejecuci\u00f3n

Al ejecutar `main.py`, el programa pregunta qu\u00e9 implementaci\u00f3n usar:

```
Seleccion\u00e1 el m\u00e9todo de persistencia:
1. Base de datos (SQLObject)
2. Archivos serializados
```

La elecci\u00f3n determina qu\u00e9 clase concreta se instancia y se inyecta en
`Login`. Ni `Login` ni `LoginHelper` conocen los detalles de la
implementaci\u00f3n de persistencia.

## Funcionalidades

- Registro e inicio de sesi\u00f3n con contrase\u00f1as hasheadas (bcrypt)
- Apertura de cuentas en m\u00faltiples monedas (USD, ARS, EUR, etc.)
- Dep\u00f3sito en cuentas existentes (creaci\u00f3n autom\u00e1tica si no existe)
- Pago con m\u00e9todos: Tarjeta, Mercado Pago, PayPal (Abstract Factory)
- Conversi\u00f3n entre monedas usando cotizaciones de Fixer.io en tiempo real
- **Compra de moneda extranjera**: operaci\u00f3n dedicada para adquirir moneda
  (ej: comprar USD pagando con ARS) usando tasas vigentes de Fixer.io

## Manejo de errores

El sistema utiliza excepciones personalizadas (`Business/exceptions.py`):
- `AccountNotFoundError`: la cuenta no existe
- `InsufficientBalanceError`: saldo insuficiente para la operaci\u00f3n
- `CurrencyNotSupportedError`: moneda no soportada por Fixer.io
- `UserNotFoundError`: el usuario no existe en el sistema

## Instrucciones de ejecuci\u00f3n

### Requisitos

- Python 3.10+
- pip (gestor de paquetes)

### Instalaci\u00f3n

```bash
# Crear y activar entorno virtual
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install bcrypt tabulate requests sqlobject python-dotenv
```

### Configuraci\u00f3n

El archivo `Data/.env` contiene la configuraci\u00f3n:

```
DB_DRIVER=sqlite
DB_NAME=homebanking.db
FIXER_API_KEY=4f73f7de235a09288e8c1988da9b6fcf
```

Para usar MySQL, cambiar:
```
DB_DRIVER=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=homebanking
```

### Ejecutar

```bash
python main.py
```

Seleccionar persistencia y seguir el men\u00fa interactivo.
