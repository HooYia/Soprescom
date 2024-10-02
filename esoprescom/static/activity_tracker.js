// static/activity_tracker.js
let timer;

function resetTimer() {
    clearTimeout(timer);
    timer = setTimeout(logoutUser, 15 * 60 * 1000); // 15 minutes
}

function logoutUser() {
    // Make an AJAX call to log out the user
    fetch('logout/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for security
        },
    })
    .then(response => {
        if (response.ok) {
            window.location.href = 'sign_in/'; // Redirect to login page
        }
    });
}

console.log('Up and Working maan')

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the desired name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Event listeners for user activity
window.onload = resetTimer;
document.onmousemove = resetTimer;
document.onkeypress = resetTimer;
document.onclick = resetTimer;