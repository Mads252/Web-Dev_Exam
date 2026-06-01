# Socia

A full-stack social media platform built as a 1st semester exam project for Web Development at KEA.

## Features

- User registration and login with password hashing
- Posts, likes and comments
- Follow/unfollow system
- User profiles with avatar uploads
- Admin panel
- Internationalization (i18n) — Danish and English
- Email validation

## Tech Stack

- **Backend:** Python, Flask
- **Database:** MySQL (via Docker)
- **Templating:** Jinja2
- **Containerization:** Docker + Docker Compose
- **Auth:** Session-based with Werkzeug password hashing

## Project Structure

```
socia/
├── app.py              # Application entry point
├── db.py               # Database connection
├── routes/             # Route handlers (auth, posts, users, likes, comments, follow, admin)
├── services/           # Business logic
├── templates/          # Jinja2 HTML templates
├── static/             # CSS, JS, images
└── sql/                # Database schema
```

## Getting Started

```bash
docker-compose up --build
```

The app runs on `http://localhost:80`.

## Built by

Mads Toft Eriksen — [github.com/Mads252](https://github.com/Mads252)
