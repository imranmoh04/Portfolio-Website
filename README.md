# 🔐 Live Chat + Authentication Web App

## Overview

This project is a **secure, real-time chat web application** built with Flask and Socket.IO. It includes user authentication, session management, encrypted credentials, and asynchronous communication via WebSockets.

It was developed as part of a university-level web development course, with the primary goal of combining **security principles** (like encrypted login sessions) and **real-time features** (like group chat).

---

## ✨ Features

### ✅ Authentication System
- User login/logout functionality
- Password encryption using **Scrypt**
- Session management via Flask sessions
- Login-required route protection
- Role-based access (e.g., guest vs. owner)
- Login attempt counter with frontend feedback

### 💬 Real-Time Chat
- WebSocket-based group chat using **Flask-SocketIO**
- Live message broadcast to all connected users
- Dynamic entry/exit notifications
- Message styling based on user role
  - Blue messages: Owner
  - Grey messages: Guest
- Secure room access via login session

---

## 🔧 Technologies Used

- **Python + Flask** for backend logic
- **SQLite** for user and chat message persistence
- **Flask-SocketIO** for WebSocket communication
- **Jinja2** templating
- **HTML/CSS/JavaScript (AJAX + jQuery)** for frontend interactivity
- **Docker** for containerized local development

---

## 🖥️ Local Setup

Clone the repo and start the app with Docker:

```bash
git clone https://gitlab.com/your-username/chat-auth-app.git
cd chat-auth-app
docker-compose -f docker-compose.yml -p chat-app up
