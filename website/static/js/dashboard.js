fetch('/version')
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch API version');
        }
        return response.text();
    })
    .then(version => {
        API_VERSION = version;
        console.log('API_VERSION:', API_VERSION);
    })
    .catch(error => {
        console.error('Error fetching API version:', error);
    });

function calculateExpirationDate(expirationOption, customExpirationDate) {
    var expirationDate;
    switch (expirationOption) {
        case "1day":
            expirationDate = new Date();
            expirationDate.setDate(expirationDate.getDate() + 1);
            break;
        case "1week":
            expirationDate = new Date();
            expirationDate.setDate(expirationDate.getDate() + 7);
            break;
        case "1month":
            expirationDate = new Date();
            expirationDate.setMonth(expirationDate.getMonth() + 1);
            break;
        case "1year":
            expirationDate = new Date();
            expirationDate.setFullYear(expirationDate.getFullYear() + 1);
            break;
        default:
            expirationDate = new Date(customExpirationDate);
            break;
    }
    var formattedExpirationDate = expirationDate.getFullYear() + '-' +
        ('0' + (expirationDate.getMonth() + 1)).slice(-2) + '-' +
        ('0' + expirationDate.getDate()).slice(-2);

    return formattedExpirationDate;
}


document.addEventListener("DOMContentLoaded", function() {
    var openPopupButtons = document.querySelectorAll("[id^='popuphandler']");
    var closeButtons = document.querySelectorAll(".close-button");
    var popupContainer = document.getElementById("popupContainer");
    var deletelicensebtn = document.getElementById("deletelicensebtn");
    var loadingScreen = document.getElementById('loading-screen');
    var loadingSpinner = document.getElementById('loading-spinner');

    deletelicensebtn.addEventListener("click", function(event) {
        event.preventDefault();
        loadingScreen.style.display = 'block';
        loadingSpinner.style.display = 'block';
        delete_license();
        loadingScreen.style.display = 'none';
        loadingSpinner.style.display = 'none';
    });

    activelicensebtn.addEventListener("click", function(event) {
        event.preventDefault();
        loadingScreen.style.display = 'block';
        loadingSpinner.style.display = 'block';
        active_license();
        loadingScreen.style.display = 'none';
        loadingSpinner.style.display = 'none';
    });

    banlicensebtn.addEventListener("click", function(event) {
        event.preventDefault();
        loadingScreen.style.display = 'block';
        loadingSpinner.style.display = 'block';
        ban_license();
        loadingScreen.style.display = 'none';
        loadingSpinner.style.display = 'none';
    });

    suspendlicensebtn.addEventListener("click", function(event) {
        event.preventDefault();
        loadingScreen.style.display = 'block';
        loadingSpinner.style.display = 'block';
        suspend_license();
        loadingScreen.style.display = 'none';
        loadingSpinner.style.display = 'none';
    });

    document.getElementById("addlicense").addEventListener("submit", function(event) {
        loadingScreen.style.display = 'block';
        loadingSpinner.style.display = 'block';
        event.preventDefault();
        var form = event.target;
        var expirationOption = form['expiration'].value;
        var customExpirationDate = form['customExpiration'].value;

        var formattedExpirationDate = calculateExpirationDate(expirationOption, customExpirationDate);
        var formData = {
            hwid: form['hwid'].value,
            expiration: formattedExpirationDate,
            licenseOwner: form['licenseOwner'].value,
            status: form['status'].value
        };
        var controlPassword = document.getElementById("control_password").value;
        axios.post(`/api/${API_VERSION}/license/admin/add_license`, {
                control_password: controlPassword,
                hwid: formData.hwid,
                expiration: formData.expiration,
                licenseOwner: formData.licenseOwner,
                status: formData.status
            })
            .then(response => {
                if (response.status === 200) {
                    createNotification('success', 'License has been added');
                    fetch_licenses();
                }
            })
            .catch(error => {
                console.error('Error fetching license data:', error)
            });
        loadingScreen.style.display = 'none';
        loadingSpinner.style.display = 'none';
    });




    document.getElementById("expiration").addEventListener("change", function() {
        var selectedOption = this.value;
        var customExpirationInput = document.getElementById("customExpiration");

        if (selectedOption === "custom") {
            customExpirationInput.style.display = "inline";
            customExpirationInput.required = true;
        } else {
            customExpirationInput.style.display = "none";
            customExpirationInput.required = false;
        }
    });

    openPopupButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            var popupId = button.getAttribute("data-popup-id");
            var popup = document.getElementById(popupId);
            popupContainer.style.display = "block";
            popup.style.display = "block";
        });
    });

    closeButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            popupContainer.style.display = "none";
            var popups = document.querySelectorAll(".popup");
            popups.forEach(function(popup) {
                popup.style.display = "none";
            });
        });
    });
});


function active_license() {
    var controlPassword = document.getElementById("control_password").value;
    var licenseee = document.getElementById("licenseinputactive").value;
    axios.post(`/api/${API_VERSION}/license/admin/active_license`, {
            control_password: controlPassword,
            license: licenseee
        })
        .then(response => {
            if (response.status === 200) {
                createNotification('success', 'License has been activited');
                fetch_licenses();
            }
        })
        .catch(error => {
            console.error('Error fetching license data:', error)
        });
}

function suspend_license() {
    var controlPassword = document.getElementById("control_password").value;
    var licenseee = document.getElementById("licenseinputsuspend").value;
    axios.post(`/api/${API_VERSION}/license/admin/suspend_license`, {
            control_password: controlPassword,
            license: licenseee
        })
        .then(response => {
            if (response.status === 200) {
                createNotification('success', 'License has been suspended');
                fetch_licenses();
            }
        })
        .catch(error => {
            console.error('Error fetching license data:', error)
        });
}

function ban_license() {
    var controlPassword = document.getElementById("control_password").value;
    var licenseee = document.getElementById("licenseinputban").value;
    axios.post(`/api/${API_VERSION}/license/admin/ban_license`, {
            control_password: controlPassword,
            license: licenseee
        })
        .then(response => {
            if (response.status === 200) {
                createNotification('success', 'License has been banned');
                fetch_licenses();
            }
        })
        .catch(error => {
            console.error('Error fetching license data:', error)
        });
}


function delete_license() {
    var controlPassword = document.getElementById("control_password").value;
    var licenseee = document.getElementById("licenseinputdel").value;
    axios.post(`/api/${API_VERSION}/license/admin/delete_license`, {
            control_password: controlPassword,
            license: licenseee
        })
        .then(response => {
            if (response.status === 200) {
                createNotification('success', 'License has been deleted');
                fetch_licenses();
            }
        })
        .catch(error => {
            console.error('Error fetching license data:', error)
        });
}

function fetch_licenses() {
    document.getElementById("licenseContainer").innerHTML = "";
    var controlPassword = document.getElementById("control_password").value;

    axios.post(`/api/${API_VERSION}/license/admin/get_all_licenses`, {
            control_password: controlPassword
        })
        .then(response => {
            if (response.status === 200) {
                displayLicenseList(response.data);
            }
        })
        .catch(error => {
            console.error('Error fetching license data:', error);
            displayNoLicenseMessage();
        });
}

function displayLicenseList(licenses) {
    var licenseContainer = document.getElementById("licenseContainer");
    var table = document.createElement("table");
    table.classList.add("license-table");
    var headerRow = table.insertRow();
    headerRow.classList.add("header-row");
    ['ID', 'License Key', 'HWID', 'Expiration Date', 'Status', 'License Owner'].forEach(function(headerText) {
        var headerCell = document.createElement("th");
        headerCell.textContent = headerText;
        headerRow.appendChild(headerCell);
    });
    licenses.forEach(function(licenseData, index) {
        var rowColor = index % 2 === 0 ? "dark-row" : "white-row";
        var row = table.insertRow();
        row.classList.add(rowColor);
        var [id, licenseKey, hwid, expirationDate, status, licenseOwner] = licenseData;
        var idCell = row.insertCell();
        idCell.textContent = id;
        var licenseKeyCell = row.insertCell();
        licenseKeyCell.textContent = licenseKey;
        var hwidCell = row.insertCell();
        hwidCell.textContent = hwid || "N/A";
        var expirationDateCell = row.insertCell();
        expirationDateCell.textContent = expirationDate;
        var statusCell = row.insertCell();
        statusCell.textContent = status;
        var licenseOwnerCell = row.insertCell();
        licenseOwnerCell.textContent = licenseOwner || "N/A";
    });

    licenseContainer.appendChild(table);
}


function displayNoLicenseMessage() {
    var licenseContainer = document.getElementById("licenseContainer");
    licenseContainer.innerHTML = "<p>No licenses found.</p>";
}