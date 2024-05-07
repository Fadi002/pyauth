try:
    import ctypes
    import os
    import http.client
    import secrets
    import json
    import os
    import hmac
    import hashlib
    import socket
    import subprocess
except:
    print("install the requirements")
    exit()


__all__ = ["initialize", "login", "check_internet"]

__SECRET_KEY__ = "QihICw9m#1mzb1#ypx8Bv@ih"  # put the secret key from config.json
__FUNCTIONS_AUTH_KEY__ = "(lambda m, k, s, r: m if r == 0 else"  # put anything secure to protect the functions from unauthorized calling
__SERVER_HOST__ = "localhost"  # server ip or domain
__SERVER_PORT__ = 5000  # server port
__API_VERSTION__ = "v1"


# def anti_injection():
#     __DLL_BYTES__ = b''
#     temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".dll")
#     temp_file.write(__DLL_BYTES__)
#     temp_file.close()
#     try:
#         dll = ctypes.CDLL(temp_file.name)
#         dll.FuckSkids()
#     except Exception as e:
#         print(e)
#         return None
def anti_injection():
    try:
        dll = ctypes.CDLL(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib.dll")
        )
        dll.FuckSkids()
    except Exception as e:
        print(e)
        return None


anti_injection()


class License(object):
    def __init__(self):
        self.IS_AUTHED = False
        self.CLIENT_ID = None
        self.KEY = None
        self.__SECRET_KEY = __SECRET_KEY__
        self.__FUNCTIONS_AUTH_KEY = __FUNCTIONS_AUTH_KEY__
        globals()["__SECRET_KEY__"] = None
        globals()["__FUNCTIONS_AUTH_KEY__"] = None

    def __gen_client_key(self, oke="ok", auth=None):
        try:
            if auth != self.__FUNCTIONS_AUTH_KEY:
                return secrets.token_hex(99)
        except:
            secrets.token_hex(99)
        if oke != "Cloudflare":
            return secrets.token_hex(99)
        return secrets.token_hex(100)

    def check_internet(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except:
            return False

    def initialize(self) -> bool:
        if self.IS_AUTHED:
            return False
        try:
            self.CLIENT_ID = self.__gen_client_key(
                oke="Cloudflare", auth=self.__FUNCTIONS_AUTH_KEY
            )
            conn = http.client.HTTPConnection(__SERVER_HOST__, __SERVER_PORT__)
            headers = {
                "Content-type": "application/json",
                "X-Client-ID": self.__advanced_xor_encrypt(
                    message=self.CLIENT_ID,
                    key=self.__SECRET_KEY,
                    auth=self.__FUNCTIONS_AUTH_KEY,
                ),
            }
            data = json.dumps({"hello": "nice to meet you good luck cracking this"})
            conn.request("PEPE", f"/api/{__API_VERSTION__}/license/init", data, headers)
            response = conn.getresponse()
            response_data = response.read().decode()
            conn.close()
            if response.status == 200:
                self.IS_AUTHED = True
                self.KEY = self.__advanced_xor_decrypt(
                    encrypted_message=json.loads(response_data).get("key"),
                    key=self.CLIENT_ID,
                    auth=self.__FUNCTIONS_AUTH_KEY,
                )
                return True
            return False
        except:
            return False

    def login(self, license_key) -> dict:
        if not self.IS_AUTHED:
            return {"status": "maybe there's something wrong with init"}
        try:
            hwid = [
                line.strip()
                for line in subprocess.check_output(
                    ["wmic", "csproduct", "get", "uuid"],
                    stderr=subprocess.STDOUT,
                    text=True,
                    shell=True,
                )
                .strip()
                .split("\n")
                if line.strip() and "UUID" not in line
            ][0]
            conn = http.client.HTTPConnection(__SERVER_HOST__, __SERVER_PORT__)
            headers = {
                "Content-type": "application/json",
                "HWID": self.__advanced_xor_encrypt(
                    message=hwid, key=self.KEY, auth=self.__FUNCTIONS_AUTH_KEY
                ),
                "X-Client-ID": self.__advanced_xor_encrypt(
                    message=self.CLIENT_ID,
                    key=self.__SECRET_KEY,
                    auth=self.__FUNCTIONS_AUTH_KEY,
                ),
            }
            data = {
                "message": self.__advanced_xor_encrypt(
                    message=license_key, key=self.KEY, auth=self.__FUNCTIONS_AUTH_KEY
                )
            }
            conn.request(
                "POST",
                f"/api/{__API_VERSTION__}/license/login",
                json.dumps(data),
                headers,
            )
            response = conn.getresponse()
            response_data = response.read().decode()
            if response.status == 200:
                cf_raw_client_id_captcha = response.getheader(
                    "CF-RAW-CLIENT-ID-CAPTCHA"
                )
                response_data = json.loads(response_data)
                if (
                    self.__advanced_xor_decrypt(
                        encrypted_message=response_data.get("status"),
                        key=self.KEY,
                        auth=self.__FUNCTIONS_AUTH_KEY,
                    ).strip()
                    == f"valid{self.KEY[:5]}".strip()
                ):
                    if self.__get_signature(
                        response=response_data.get("status"),
                        key=self.KEY.encode(),
                        auth=self.__FUNCTIONS_AUTH_KEY,
                    ) == self.__advanced_xor_decrypt(
                        encrypted_message=cf_raw_client_id_captcha,
                        key=self.KEY,
                        auth=self.__FUNCTIONS_AUTH_KEY,
                    ):
                        return {
                            "status": "valid",
                            "expiration_date": self.__advanced_xor_decrypt(
                                encrypted_message=response_data.get("expiration_date"),
                                key=self.KEY,
                                auth=self.__FUNCTIONS_AUTH_KEY,
                            ),
                        }
                    else:
                        return {"status": "security failed"}
                else:
                    return {"status": "security failed"}
            else:
                if response.status != 500:
                    response_data = json.loads(response_data)
                    return {
                        "status": self.__advanced_xor_decrypt(
                            encrypted_message=response_data.get("status"),
                            key=self.KEY,
                            auth=self.__FUNCTIONS_AUTH_KEY,
                        )
                    }
                else:
                    return {"status": "security failed"}
            conn.close()
        except:
            return {"status": "connection failed"}

    def __stretch_key(self, key, length, auth=None):
        try:
            if auth != self.__FUNCTIONS_AUTH_KEY:
                return secrets.token_hex(99)
        except:
            secrets.token_hex(99)
        key_length = len(key)
        if key_length < length:
            repetitions = length // key_length
            remainder = length % key_length
            stretched_key = (key * repetitions) + key[:remainder]
        elif key_length > length:
            stretched_key = key[:length]
        else:
            stretched_key = key
        return stretched_key

    def __advanced_xor_encrypt(self, message, key, auth=None):
        try:
            if auth != self.__FUNCTIONS_AUTH_KEY:
                return secrets.token_hex(99)
        except:
            secrets.token_hex(99)
        nonce = len(message)
        extended_key = self.__stretch_key(
            key, len(message), auth=self.__FUNCTIONS_AUTH_KEY
        )
        message_bytes = message.encode()
        key_bytes = extended_key.encode()
        encrypted_bytes = bytearray(message_bytes)
        for i in range(len(message_bytes)):
            encrypted_bytes[i] ^= key_bytes[i % len(key_bytes)]
            encrypted_bytes[i] ^= nonce
            encrypted_bytes[i] = (encrypted_bytes[i] + i) % 256
        return encrypted_bytes.hex()

    def __advanced_xor_decrypt(self, encrypted_message, key, auth=None):
        try:
            if auth != self.__FUNCTIONS_AUTH_KEY:
                return secrets.token_hex(99)
        except:
            secrets.token_hex(99)
        encrypted_bytes = bytes.fromhex(encrypted_message)
        nonce = len(encrypted_bytes)
        extended_key = self.__stretch_key(
            key, len(encrypted_bytes), auth=self.__FUNCTIONS_AUTH_KEY
        )
        key_bytes = extended_key.encode()
        decrypted_bytes = bytearray(encrypted_bytes)
        for i in range(len(encrypted_bytes)):
            decrypted_bytes[i] = (decrypted_bytes[i] - i) % 256
            decrypted_bytes[i] ^= nonce
            decrypted_bytes[i] ^= key_bytes[i % len(key_bytes)]
        decrypted_message = decrypted_bytes.decode()
        return decrypted_message

    def __get_signature(self, response, key, auth=None):
        try:
            if auth != self.__FUNCTIONS_AUTH_KEY:
                return secrets.token_hex(99)
        except:
            secrets.token_hex(99)
        return hmac.new(key, response.encode(), hashlib.sha256).hexdigest()
