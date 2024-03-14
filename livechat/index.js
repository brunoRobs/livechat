document.addEventListener('DOMContentLoaded', function () {
    var input = document.getElementById('username');
    var button = document.getElementById('button');

    input.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            button.click();
        }
    });
});

function login() {
    let username = document.getElementById('username').value
    if (username) {
        fetch('/login', {
            method: 'GET',
            headers: {
                'User': username,
            }
        }).then(response => {
            if (!response.ok) alert(response.statusText);
            else {
                localStorage.setItem('User', username)
                window.location.href = '/chat'
            }
        })
    } else alert('Username cannot be blank!!!')
}