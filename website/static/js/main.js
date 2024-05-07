var API_VERSION;

async function fetchApiVersion() {
    try {
        const response = await fetch('/version');
        if (!response.ok) {
            throw new Error('Failed to fetch API version');
        }
        const version = await response.text();
        API_VERSION = version;
    } catch (error) {
        console.error('Error fetching API version:', error);
    }
}

fetchApiVersion();

function signinfunc() {
    var usernameElement = document.getElementById('username');
    var passwordElement = document.getElementById('password');
    var loadingScreen = document.getElementById('loading-screen');
    var loadingSpinner = document.getElementById('loading-spinner');
    axios.post(`/api/${API_VERSION}/user/login`, {
            username: usernameElement.value,
            password: passwordElement.value,
        })
        .then(function(response) {
            if (response.status === 200) {
                loadingScreen.style.display = 'none';
                loadingSpinner.style.display = 'none';
                createNotification('success', 'Login successful');
                setTimeout(function() {
                    window.location.href = '/dashboard';
                }, 3000);
            } else {
                loadingScreen.style.display = 'none';
                loadingSpinner.style.display = 'none';
                createNotification('failure', response.data.error);
            }
        })
        .catch(function(error) {
            loadingScreen.style.display = 'none';
            loadingSpinner.style.display = 'none';
            createNotification('failure', error.response.data.error);
        });
}

var signinButton = document.getElementById('signinbtn');
if (signinButton) {
    signinButton.addEventListener('click', function() {
        var loadingScreen = document.getElementById('loading-screen');
        var loadingSpinner = document.getElementById('loading-spinner');
        loadingScreen.style.display = 'block';
        loadingSpinner.style.display = 'block';
        signinfunc();
    });
}

function createNotification(type, message) {
    const types = ["success", "failure", "warning", "checking"];
    const container = document.getElementById('notification-container');

    if (!types.includes(type) || container.childElementCount >= 5) {
        const firstNotification = container.firstElementChild;
        if (firstNotification) {
            container.removeChild(firstNotification);
        } else {
            return;
        }
    }

    var notification = document.createElement('div');
    var content = document.createElement('div');
    var progress = document.createElement('div');

    notification.className = 'notification-bar ' + type;
    content.className = 'notification-content';
    content.textContent = message;
    progress.className = 'notification-progress';
    notification.appendChild(content);
    notification.appendChild(progress);
    container.appendChild(notification);

    setTimeout(function() {
        notification.classList.add('show');
    }, 100);

    setTimeout(function() {
        notification.classList.remove('show');
        setTimeout(function() {
            container.removeChild(notification);
        }, 300);
    }, 5000);
}

function navigateTo(pageId) {
    var sections = Array.from(document.getElementsByTagName('section'));
    sections.forEach(function(section) {
        section.classList.remove('active');
    });
    document.getElementById(pageId).classList.add('active');
}