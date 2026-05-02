// Auth utilities
function isLoggedIn() {
    return !!localStorage.getItem('token');
}

function getCurrentUser() {
    const u = localStorage.getItem('user');
    return u ? JSON.parse(u) : null;
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login.html';
}

function requireAuth() {
    if (!isLoggedIn()) {
        window.location.href = '/login.html';
        return false;
    }
    return true;
}

function redirectIfLoggedIn() {
    if (isLoggedIn()) {
        window.location.href = '/index.html';
    }
}
