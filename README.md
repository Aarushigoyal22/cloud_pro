# 🌥️ Cloud Notes API  
A lightweight, cloud-ready REST API for creating and managing notes.  
Built using **Python Flask**, **Docker**, and ready to deploy on **AWS EC2 / ECS / ECR**.

This project is part of the *Cloud (UCT512)* course and focuses on DevOps & Cloud workflow rather than frontend UI.

---

## 📌 Features
- Create, read, update and delete notes  
- JSON file–based storage (no DB setup required)  
- Fully containerized using Docker  
- Health check endpoint  
- Ready for deployment on EC2 or ECS  
- CI/CD compatible (GitHub Actions → ECR → ECS)  
- Thread-safe storage layer (supports multiple workers)