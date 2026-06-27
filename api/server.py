import os
import sys
from flask import Flask, jsonify, request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from Data.database_helper import DatabaseHelper
from Data.file_helper import FileDataHelper
from Business.LoginHelper import LoginHelper
from Business.exceptions import (
    AccountNotFoundError,
    InsufficientBalanceError,
    UserNotFoundError,
)

DB_MODE = os.getenv("PERSISTENCE", "db")

if DB_MODE == "file":
    _helper = FileDataHelper()
else:
    _helper = DatabaseHelper()

login = LoginHelper(_helper)
fixer = login.fixer_service

app = Flask(__name__)


@app.route("/monedas", methods=["GET"])
def obtener_monedas():
    try:
        rates = fixer.get_rates("USD,ARS,EUR,JPY,GBP,BRL,CLP,UYU")
        return jsonify({"monedas": list(rates.keys())})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/cotizacion", methods=["GET"])
def obtener_cotizacion():
    codigo = request.args.get("codigo")
    if not codigo:
        return jsonify({"error": "Tenes que pasarme el codigo"}), 400
    codigo = codigo.strip().upper()
    try:
        rates = fixer.get_rates(codigo)
        if codigo not in rates:
            return jsonify({"error": "Moneda no encontrada"}), 404
        return jsonify({"moneda": codigo, "cotizacion": rates[codigo]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/cotizacion", methods=["POST"])
def obtener_cotizacion_post():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Cuerpo requerido"}), 400
    codigo = body.get("codigo", "").strip().upper()
    if not codigo:
        return jsonify({"error": "Tenes que pasarme el codigo"}), 400
    try:
        rates = fixer.get_rates(codigo)
        if codigo not in rates:
            return jsonify({"error": "Moneda no encontrada"}), 404
        return jsonify({"moneda": codigo, "cotizacion": rates[codigo]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/usuarios", methods=["POST"])
def registrar_usuario():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Cuerpo requerido"}), 400
    username = body.get("username", "").strip()
    password = body.get("password", "")
    if not username or not password:
        return jsonify({"error": "Username y password requeridos"}), 400
    try:
        login.prepareAndStorePwd(username, password)
        return jsonify({"mensaje": "Usuario {} creado".format(username)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/usuarios/<username>/cuentas", methods=["GET"])
def listar_cuentas(username):
    try:
        cuentas = _helper.getCuentas(username)
        if not cuentas:
            return jsonify({"cuentas": []})
        resultado = [{"moneda": m, "saldo": float(s)} for m, s in cuentas.items()]
        return jsonify({"cuentas": resultado})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/usuarios/<username>/cuentas", methods=["POST"])
def abrir_cuenta(username):
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Cuerpo requerido"}), 400
    moneda = body.get("moneda", "").strip().upper()
    if not moneda:
        return jsonify({"error": "Moneda requerida"}), 400
    try:
        login.abrir_cuenta(username, moneda)
        return jsonify({"mensaje": "Cuenta en {} abierta".format(moneda)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/usuarios/<username>/cuentas/<moneda>", methods=["PUT"])
def depositar(username, moneda):
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Cuerpo requerido"}), 400
    monto = body.get("monto")
    if monto is None:
        return jsonify({"error": "Monto requerido"}), 400
    try:
        login.depositar(username, moneda, str(monto))
        return jsonify({"mensaje": "Depositados {} en {}".format(monto, moneda.upper())})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/usuarios/<username>/cuentas/<moneda>", methods=["DELETE"])
def cerrar_cuenta(username, moneda):
    try:
        cuentas = _helper.getCuentas(username)
        moneda = moneda.upper()
        if moneda not in cuentas:
            return jsonify({"error": "Cuenta en {} no existe".format(moneda)}), 404
        del cuentas[moneda]
        _helper.saveCuentas(username, cuentas)
        return jsonify({"mensaje": "Cuenta en {} eliminada".format(moneda)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/usuarios/<username>/comprar", methods=["POST"])
def comprar_moneda(username):
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Cuerpo requerido"}), 400
    hacia = body.get("hacia", "").strip().upper()
    monto = body.get("monto")
    desde = body.get("desde", "ARS").strip().upper()
    if not hacia or monto is None:
        return jsonify({"error": "hacia y monto requeridos"}), 400
    try:
        tasa, costo = login.comprar_moneda(username, hacia, str(monto), desde)
        return jsonify({
            "mensaje": "Compra de {} {} realizada".format(monto, hacia),
            "tasa": float(tasa),
            "costo": float(costo),
            "moneda_origen": desde,
        })
    except (AccountNotFoundError, InsufficientBalanceError, UserNotFoundError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/usuarios/<username>/pagar", methods=["POST"])
def pagar(username):
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Cuerpo requerido"}), 400
    metodo = body.get("metodo", "").strip()
    moneda = body.get("moneda", "").strip().upper()
    monto = body.get("monto")
    if not metodo or not moneda or monto is None:
        return jsonify({"error": "metodo, moneda y monto requeridos"}), 400
    try:
        login.procesar_pago(username, metodo, str(monto), moneda)
        return jsonify({"mensaje": "Pago realizado"})
    except (AccountNotFoundError, InsufficientBalanceError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("API corriendo en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
