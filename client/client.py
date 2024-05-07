from lib import License

license_in = License()
if license_in.check_internet():
    print("client have internet connection")
    if license_in.initialize():
        print("client is ready to login")
        status = license_in.login("USER LICENSE HERE")
        if "valid" in status["status"]:
            print("Logged in")
        elif "suspended" in status["status"]:
            print("License has been suspended")
        elif "banned" in status["status"]:
            print("License has been banned")
        else:
            print("Invalid/tamperd response")
    else:
        print("client is not ready to login")
else:
    print("client doesn't have internet connection")
