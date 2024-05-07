from flask import (
    Flask,
    render_template,
    request,
    redirect,
    jsonify,
    make_response,
    abort,
    Blueprint,
    Response,
)
import os, hashlib, jwt, datetime, base64, secrets
from functools import wraps
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import sqlite3, json, hmac
from funcs import encryption, db

CONFIG = json.loads(open("config.json", "r", encoding="utf-8").read())

DB_PATH = "dbs/client_keys.db"
DB_PATH_LICENSE = "dbs/licenses.db"
API_VERSION = CONFIG.get("API_VERSION")


with open("private_key.pem", "rb") as f:
    private_key_pem = f.read()
with open("public_key.pem", "rb") as f:
    public_key_pem = f.read()


app = Flask(__name__, template_folder="templates", static_url_path="/static")
api_blueprint = Blueprint("api", __name__, url_prefix=f"/api/{API_VERSION}")
app.secret_key = CONFIG.get("secret_key")

@app.after_request
def add_header(response):
    response.headers['GITHUB_CREDITS'] = 'https://github.com/Fadi002'
    response.headers['CREDITS'] = '0xmrpepe'
    return response

@api_blueprint.after_request
def add_header(response):
    response.headers['GITHUB_CREDITS'] = 'https://github.com/Fadi002'
    response.headers['CREDITS'] = '0xmrpepe'
    return response


if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS client_keys
                 (client_id TEXT PRIMARY KEY, key TEXT)"""
    )
    conn.commit()
if not os.path.exists(DB_PATH_LICENSE):
    conn = sqlite3.connect(DB_PATH_LICENSE)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE licenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        license_key TEXT UNIQUE,
                        hwid TEXT,
                        expiration_date TEXT,
                        status TEXT,
                        license_owner TEXT)"""
    )
    conn.commit()

if not os.path.exists("database/users.db"):
    db.Users.init()


def change_license_status(license_key, new_status):
    conn = sqlite3.connect(DB_PATH_LICENSE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE licenses SET status = ? WHERE license_key = ?",
        (new_status, license_key),
    )
    conn.commit()
    conn.close()


@api_blueprint.route("/license/delete", methods=["PEPE"])
def delete():
    conn = sqlite3.connect(DB_PATH)
    client_id = request.headers.get("X-Client-ID")
    if not client_id:
        abort(500)
    c.execute("SELECT key FROM client_keys WHERE client_id=?", (client_id,))
    existing_key = c.fetchone()
    if not existing_key:
        return abort(500)
    c.execute("DELETE FROM client_keys WHERE client_id=?", (client_id,))
    conn.commit()
    return jsonify({"message": "Client deleted successfully"})


def grab_license(license_key):
    conn = sqlite3.connect(DB_PATH_LICENSE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM licenses WHERE license_key = ?", (license_key,))
    data = cursor.fetchone()
    conn.commit()
    return data


@api_blueprint.route("/license/admin/get_all_licenses", methods=["POST"])
def get_all_licenses():
    control_password = CONFIG.get("control_password")
    data = request.get_json()
    if control_password != data.get("control_password"):
        return jsonify({"error": "Invalid request"}), 400
    else:
        conn = sqlite3.connect(DB_PATH_LICENSE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM licenses")
        licenses = cursor.fetchall()
        if not licenses:
            result = Response(status=204)
        else:
            result = json.dumps(licenses)
        conn.close()
        return result


@api_blueprint.route("/license/admin/delete_license", methods=["POST"])
def delete_license_api():
    control_password = CONFIG.get("control_password")
    data = request.get_json()
    if control_password != data.get("control_password"):
        return jsonify({"error": "Invalid request"}), 400
    else:
        delete_license(data.get("license"))
        return Response(status=200)


@api_blueprint.route("/license/admin/active_license", methods=["POST"])
def active_license_api():
    control_password = CONFIG.get("control_password")
    data = request.get_json()
    if control_password != data.get("control_password"):
        return jsonify({"error": "Invalid request"}), 400
    else:
        change_license_status(data.get("license"), "active")
        return Response(status=200)


@api_blueprint.route("/license/admin/suspend_license", methods=["POST"])
def suspend_license_api():
    control_password = CONFIG.get("control_password")
    data = request.get_json()
    if control_password != data.get("control_password"):
        return jsonify({"error": "Invalid request"}), 400
    else:
        change_license_status(data.get("license"), "suspended")
        return Response(status=200)


@api_blueprint.route("/license/admin/ban_license", methods=["POST"])
def ban_license_api():
    control_password = CONFIG.get("control_password")
    data = request.get_json()
    if control_password != data.get("control_password"):
        return jsonify({"error": "Invalid request"}), 400
    else:
        change_license_status(data.get("license"), "banned")
        return Response(status=200)


@api_blueprint.route("/license/admin/add_license", methods=["POST"])
def add_license_api():
    control_password = CONFIG.get("control_password")
    data = request.get_json()
    if control_password != data.get("control_password"):
        return jsonify({"error": "Invalid request"}), 400
    else:
        license_key = secrets.token_hex(16)
        license_data = {
            "license_key": license_key,
            "expiration_date": data["expiration"],
            "status": data["status"],
            "hwid": data["hwid"],
            "license_owner": data["licenseOwner"],
        }
        db = sqlite3.connect(DB_PATH_LICENSE)
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO licenses (license_key, expiration_date, status, hwid, license_owner) VALUES (?, ?, ?, ?, ?)",
            (
                license_data["license_key"],
                license_data["expiration_date"],
                license_data["status"],
                license_data["hwid"],
                license_data["license_owner"],
            ),
        )
        db.commit()
        db.close()
        return Response(status=200)


@api_blueprint.route("/license/login", methods=["POST"])
def login():
    client_id = encryption.advanced_xor_decrypt(
        request.headers.get("X-Client-ID"), CONFIG.get("secret_key")
    )
    key = get_client_key(client_id)
    hwid = encryption.advanced_xor_decrypt(request.headers.get("HWID"), key)
    if not key:
        abort(500)
    if not hwid:
        return abort(500)
    encrypted_data = request.get_data()
    try:
        license_info = json.loads(encrypted_data.decode())
    except:
        return abort(500)
    license_key = encryption.advanced_xor_decrypt(license_info.get("message"), key)
    if not license_key:
        return abort(500)
    license_data = grab_license(license_key)
    if not license_data:
        return abort(500)
    if license_data[4] == "suspended":
        return (
            jsonify(
                {"status": encryption.advanced_xor_encrypt("License suspended", key)}
            ),
            403,
        )
    elif license_data[4] == "banned":
        return (
            jsonify({"status": encryption.advanced_xor_encrypt("License banned", key)}),
            403,
        )
    expiration_date_str = license_data[3]
    expiration_date = datetime.datetime.strptime(expiration_date_str, "%Y-%m-%d")
    current_date = datetime.datetime.now()
    if expiration_date < current_date:
        delete_license(license_key)
        return (
            jsonify(
                {"status": encryption.advanced_xor_encrypt("License expired", key)}
            ),
            403,
        )
    else:
        if license_data[2] is None:
            conn = sqlite3.connect(DB_PATH_LICENSE)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE licenses SET hwid = ? WHERE license_key = ?",
                (hwid, license_key),
            )
            conn.commit()
            return (
                jsonify(
                    {
                        "status": encryption.advanced_xor_encrypt(
                            f"valid{key[:5]}", key
                        ),
                        "expiration_date": encryption.advanced_xor_encrypt(
                            expiration_date_str, key
                        ),
                    }
                ),
                200,
            )
        elif license_data[2] != hwid:
            return abort(500)
        else:

            res_data = {
                "status": encryption.advanced_xor_encrypt(f"valid{key[:5]}", key),
                "expiration_date": encryption.advanced_xor_encrypt(
                    expiration_date_str, key
                ),
            }
            response = make_response(jsonify(res_data), 200)
            response.headers["CF-RAW-CLIENT-ID-CAPTCHA"] = (
                encryption.advanced_xor_encrypt(
                    get_signature(res_data.get("status"), key.encode()), key
                )
            )
            return response


@api_blueprint.route("/license/init", methods=["PEPE"])
def init():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    client_id = encryption.advanced_xor_decrypt(
        request.headers.get("X-Client-ID"), CONFIG.get("secret_key")
    )
    c.execute("SELECT key FROM client_keys WHERE client_id=?", (client_id,))
    existing_key = c.fetchone()
    if existing_key:
        return (
            jsonify(
                {
                    "status": encryption.advanced_xor_encrypt(
                        "Client already initialized", client_id
                    )
                }
            ),
            400,
        )
    key = gen_client_key()
    c.execute("INSERT INTO client_keys VALUES (?, ?)", (client_id, key))
    conn.commit()

    return jsonify({"key": encryption.advanced_xor_encrypt(key, client_id)})


@api_blueprint.route("/user/HELLO", methods=["GET", "POST"])
def hello():
    client_id = request.headers.get("X-Client-ID")
    key = get_client_key(client_id)
    if not key:
        return jsonify({"status": "Client not initialized"}), 400

    encrypted_response = xor_encryption("Hello, client!", key)
    return jsonify({"encrypted_response": encrypted_response})


def xor_encryption(data, key):
    encrypted = "".join(
        chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data)
    )
    return encrypted


def get_client_key(client_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT key FROM client_keys WHERE client_id=?", (client_id,))
    key = c.fetchone()
    conn.commit()
    if key:
        return key[0]
    return None


def gen_client_key():
    return secrets.token_hex(100)


def get_signature(response, key):
    return hmac.new(key, response.encode(), hashlib.sha256).hexdigest()


def delete_license(license_key):
    conn = sqlite3.connect(DB_PATH_LICENSE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM licenses WHERE license_key = ?", (license_key,))
    conn.commit()
    return None


######################### WEBSITE #########################


@app.route("/version", methods=["GET"])
def version():
    return API_VERSION


@app.route("/", methods=["GET"])
def signin():
    return render_template("index.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@api_blueprint.route("/user/login", methods=["POST"])
def userlogin():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Missing required fields"}), 400
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user = db.Users.check(username=username, password=hashed_password)
    if user:
        user_id = user[1]
        token = generate_auth_token(user_id, session_key=user[3])
        response = jsonify({"message": "Login successful"})
        response.set_cookie("auth_token", token, httponly=True)
        return response, 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401


def generate_auth_token(user_id, session_key):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        "session_key": session_key,
    }
    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
    encrypted_token = encrypt_jwt(token, public_key_pem)
    return encrypted_token


def encrypt_jwt(token, public_key):
    rsa_public_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(rsa_public_key)
    encrypted_token = base64.b64encode(cipher.encrypt(token.encode())).decode()
    return encrypted_token


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("auth_token")
        if not token:
            return make_response(redirect("/"))
        try:
            rsa_private_key = RSA.import_key(private_key_pem)
            cipher = PKCS1_OAEP.new(rsa_private_key)
            decrypted_token = cipher.decrypt(base64.b64decode(token.encode())).decode()
            payload = jwt.decode(
                decrypted_token, app.config["SECRET_KEY"], algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return make_response(redirect("/"))
        except jwt.InvalidTokenError:
            return make_response(redirect("/"))

        return func(*args, **kwargs)

    return wrapper


@app.route("/dashboard")
@auth_required
def dashboard():
    token = request.cookies.get("auth_token")
    rsa_private_key = RSA.import_key(private_key_pem)
    cipher = PKCS1_OAEP.new(rsa_private_key)
    decrypted_token = cipher.decrypt(base64.b64decode(token.encode())).decode()
    payload = jwt.decode(
        decrypted_token, app.config["SECRET_KEY"], algorithms=["HS256"]
    )
    user_data = db.Users.user_info(payload["session_key"])
    return render_template(
        "dashboard.html",
        username=user_data[1],
        licenses_amount=sqlite3.connect(DB_PATH_LICENSE)
        .execute("SELECT COUNT(*) FROM licenses")
        .fetchone()[0],
    )


@app.route("/logout", methods=["GET"])
@auth_required
def logout():
    response = make_response(redirect("/"))
    response.set_cookie("auth_token", "", expires=0)
    return response


app.register_blueprint(api_blueprint)
app.run(debug=True)
