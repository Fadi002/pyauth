from Crypto.PublicKey import RSA
import os, shutil, secrets, json
from colorama import Fore, Style, init
from funcs.db import Users

init()

secret_key = None
control_password = None


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


clear_console()


def align(text: str) -> str:
    """
    credits : https://github.com/SirDank/dankware/blob/main/dankware/__init__.py
    """
    width = shutil.get_terminal_size().columns
    aligned = text
    for _ in tuple(vars(Fore).values()) + tuple(vars(Style).values()):
        aligned = aligned.replace(_, "")

    text = text.splitlines()
    aligned = aligned.splitlines()
    for _ in range(len(aligned)):
        aligned[_] = aligned[_].center(width).replace(aligned[_], text[_])
    return str("\n".join(aligned) + Style.RESET_ALL)


config_data = {"secret_key": None, "control_password": None, "API_VERSION": "v1"}


def make_rsa():
    key = RSA.generate(4096)
    public_key = key.public_key().export_key()
    private_key = key.export_key()
    with open("private_key.pem", "w") as f:
        f.write(private_key.decode())
    with open("public_key.pem", "w") as f:
        f.write(public_key.decode())


def generate_string(length=24):
    site_key = secrets.token_urlsafe(length)
    return site_key


def purplepink(text):
    os.system("")
    faded = ""
    red = 40
    for line in text.splitlines():
        faded += f"\033[38;2;{red};0;220m{line}\033[0m\n"
        if not red == 255:
            red += 15
            if red > 255:
                red = 255
    return faded


print(
    align(
        purplepink(
            """
██████╗ ██╗   ██╗ █████╗ ██╗   ██╗████████╗██╗  ██╗
██╔══██╗╚██╗ ██╔╝██╔══██╗██║   ██║╚══██╔══╝██║  ██║
██████╔╝ ╚████╔╝ ███████║██║   ██║   ██║   ███████║
██╔═══╝   ╚██╔╝  ██╔══██║██║   ██║   ██║   ██╔══██║
██║        ██║   ██║  ██║╚██████╔╝   ██║   ██║  ██║
╚═╝        ╚═╝   ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝
pyauth config script
"""
        )
    )
)

secret_key = generate_string()
control_password_i = input("generate random admin password? [y/n]: ")
if control_password_i.lower() == "y":
    control_password = generate_string()
else:
    control_password_2 = input("Please enter the password you want: ")
    control_password = control_password_2

print(f"secret_key = {secret_key}")
print(f"control password = {control_password}")

print("Please wait until the setup is complete this will take few seconds")
make_rsa()

config_data["secret_key"] = secret_key
config_data["control_password"] = control_password

with open("config.json", "w") as json_file:
    json.dump(config_data, json_file)
    json_file.close()

username = input("Enter admin username to register it: ")
password = input("Enter admin password to register it: ")
if not os.path.exists("database/users.db"):
    Users().init()
Users().add(username=username, passowrd=password, session_key=generate_string())

print("Setup finished.")
input("Press enter to exit\n")
