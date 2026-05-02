# TaskFlow — Team Task Manager

A full-stack web application for managing projects, assigning tasks, and tracking progress with **role-based access control (Admin/Member)**.

## 🚀 Features

- **Authentication**: Signup/Login with JWT tokens
- **Project Management**: Create, edit, delete projects
- **Team Management**: Add/remove members, assign roles (Admin/Member)
- **Task Tracking**: Create tasks with priority, status, due dates, and assignees
- **Kanban Board**: Visual task board with Todo → In Progress → Done columns
- **Dashboard**: Aggregated stats, recent tasks, overdue task detection
- **Role-Based Access Control**:
  - **Admins**: Full CRUD on tasks, manage members
  - **Members**: View tasks, update status on assigned tasks only

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python / Flask |
| Database | SQLite (dev) / PostgreSQL (prod) |
| ORM | Flask-SQLAlchemy |
| Auth | JWT (PyJWT) + bcrypt |
| Frontend | Vanilla HTML/CSS/JavaScript |
| Deployment | Railway |

## 📁 Project Structure

```
task/
├── backend/
│   ├── app.py              # Flask app + static file serving
│   ├── config.py            # Configuration
│   ├── models.py            # Database models
│   ├── middleware.py         # JWT auth middleware
│   ├── routes/
│   │   ├── auth.py          # Register, Login, Profile
│   │   ├── projects.py      # Project CRUD
│   │   ├── members.py       # Team management
│   │   ├── tasks.py         # Task CRUD
│   │   └── dashboard.py     # Dashboard stats
│   ├── requirements.txt
│   └── Procfile
├── frontend/
│   ├── index.html           # Dashboard
│   ├── login.html           # Login page
│   ├── register.html        # Register page
│   ├── projects.html        # Projects list
│   ├── project.html         # Project detail + Kanban
│   ├── css/style.css        # Design system
│   └── js/                  # API client, auth, utilities
├── railway.json
└── README.md
```

## 🏃 Local Development

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000

## 🌐 Environment Variables (for Railway)

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string (auto-set by Railway) |
| `JWT_SECRET` | Secret key for JWT token signing |
| `PORT` | Server port (auto-set by Railway) |

## 📡 API Endpoints

### Auth
- `POST /api/auth/register` — Register new user
- `POST /api/auth/login` — Login
- `GET /api/auth/me` — Get profile

### Projects
- `GET /api/projects` — List projects
- `POST /api/projects` — Create project
- `GET/PUT/DELETE /api/projects/:id` — Get/Update/Delete project

### Members
- `GET /api/projects/:id/members` — List members
- `POST /api/projects/:id/members` — Add member
- `PUT /api/projects/:id/members/:uid` — Change role
- `DELETE /api/projects/:id/members/:uid` — Remove member

### Tasks
- `GET /api/projects/:id/tasks` — List tasks
- `POST /api/projects/:id/tasks` — Create task
- `GET/PUT/DELETE /api/tasks/:id` — Get/Update/Delete task

### Dashboard
- `GET /api/dashboard` — Aggregated stats

## 📝 License

MIT
