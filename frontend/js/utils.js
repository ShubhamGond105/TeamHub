// Utility functions
function showToast(message, type = 'success') {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function formatDate(iso) {
    if (!iso) return '—';
    const d = new Date(iso);
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function isOverdue(dateStr) {
    if (!dateStr) return false;
    return new Date(dateStr) < new Date();
}

function getInitials(name) {
    if (!name) return '?';
    return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2);
}

function showLoading(container) {
    container.innerHTML = '<div class="loading"><div class="spinner"></div>Loading...</div>';
}

function showEmpty(container, icon, title, message, actionHtml = '') {
    container.innerHTML = `<div class="empty-state"><div class="icon">${icon}</div><h3>${title}</h3><p>${message}</p>${actionHtml}</div>`;
}

function openModal(id) { document.getElementById(id).classList.add('active'); }
function closeModal(id) { document.getElementById(id).classList.remove('active'); }

function buildNavbar(activePage) {
    const user = getCurrentUser();
    return `
    <header class="navbar">
        <div class="navbar-container">
            <div class="brand"><h2>Team<span>Hub</span></h2></div>
            <nav class="nav-links">
                <a href="/index.html" class="nav-link ${activePage === 'dashboard' ? 'active' : ''}">Dashboard</a>
                <a href="/projects.html" class="nav-link ${activePage === 'projects' ? 'active' : ''}">Projects</a>
                <a href="#" class="nav-link mobile-only" onclick="logout(); return false;">Logout</a>
            </nav>
            <div class="navbar-right">
                <div class="user-info">
                    <div class="user-avatar">${user ? getInitials(user.name) : '?'}</div>
                    <div class="user-name">${user ? user.name : ''}</div>
                </div>
                <button class="btn btn-secondary btn-sm" onclick="logout()">Logout</button>
            </div>
            <button class="mobile-toggle" onclick="document.querySelector('.nav-links').classList.toggle('open')">☰</button>
        </div>
    </header>`;
}

function getParams() {
    return Object.fromEntries(new URLSearchParams(window.location.search));
}
