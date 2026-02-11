# SWEPRO – University Project Management System

## 📌 Description
SWEPRO is a university project management system built using a microservices-inspired architecture and MongoDB.  
The system allows students to create projects, manage team members, and handle join requests with role-based access.

## 🧱 Architecture
- User Service
- Project Service
- MongoDB (NoSQL)

Each service is independent and communicates via REST APIs.

## 👥 User Roles
- Owner: creates and manages the project
- Member: accepted team member
- Null: user without a project

## ✨ Main Features
- User registration and authentication
- Create and manage projects
- Send, accept, or reject join requests
- Maximum of 3 members per project
- One-time notification messages
- Prevent joining more than one project

## 🛠 Technologies
- Python (FastAPI)
- MongoDB
- REST APIs
- Git & GitHub

