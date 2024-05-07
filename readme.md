# Pyauth

## Website Setup

1. **Clone the Repository**: 
   ```
   git clone https://github.com/fadi002/pyauth
   ```
   
2. **Install Dependencies**: 
   ```
   cd python
   pip install -r requirements.txt
   ```

3. **Configuration**:
   - Generate a random secret key and admin control password. You can run the configuration script provided:
     ```
     python configure.py
     ```
   - Follow the prompts to generate the secret key and control password. Optionally, you can provide your own admin password.
   
4. **Database Initialization**:
   - If the database doesn't exist, it will be initialized automatically.
   
5. **Run the Application**:
   ```
   python main.py
   ```

6. **Access the Website**:
   - Once the application is running, you can access it in your web browser at `http://localhost:5000`.


## Client setup

1. **Initialization**
   - Initialize the `License` class instance:
     ```python
     license_in = License()
     ```

2. **Checking Internet Connectivity**
   - Use the `check_internet()` method to check if the client has an internet connection:
     ```python
     if license_in.check_internet():
         print("Client has an internet connection")
     else:
         print("Client doesn't have an internet connection")
     ```

3. **Initialization**
   - Initialize the license system using the `initialize()` method:
     ```python
     if license_in.initialize():
         print("License system initialized successfully")
     else:
         print("Failed to initialize the license system")
     ```

4. **Login**
   - Use the `login()` method to authenticate with a license key:
     ```python
     status = license_in.login("USER LICENSE HERE")
     if "valid" in status["status"]:
         print("Logged in successfully")
     elif "suspended" in status["status"]:
         print("License has been suspended")
     elif "banned" in status["status"]:
         print("License has been banned")
     else:
         print("Invalid or tampered response")
     ```

### Example

Here's an example demonstrating the usage of the license management system:


```python
from lib import License

# Initialize License class instance
license_in = License()

# Check internet connectivity
if license_in.check_internet():
    print("Client has an internet connection")
else:
    print("Client doesn't have an internet connection")

# Initialize license system
if license_in.initialize():
    print("License system initialized successfully")
else:
    print("Failed to initialize the license system")

# Login with license key
status = license_in.login("USER LICENSE HERE")
if "valid" in status["status"]:
    print("Logged in successfully")
elif "suspended" in status["status"]:
    print("License has been suspended")
elif "banned" in status["status"]:
    print("License has been banned")
else:
    print("Invalid or tampered response")
```

## Screenshots
<p float="left">
  <a href="#Screenshots"><img src="https://github.com/Fadi002/pyauth/blob/main/imgs/login.png?raw=true" width="400"></img></a>
  <a href="#Screenshots"><img src="https://github.com/Fadi002/pyauth/blob/main/imgs/home.png?raw=true" width="400"></img></a>
  <a href="#Screenshots"><img src="https://github.com/Fadi002/pyauth/blob/main/imgs/license.png?raw=true" width="400"></img></a>
</p>