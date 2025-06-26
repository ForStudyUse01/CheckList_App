# 📝 Checklist App

A simple and modern checklist app built with Flask, REST API, and MySQL! 🚀

## ✨ Features
- 🔐 User Registration & Login
- ✅ Add, Edit, Delete, and Mark Tasks as Done
- 📦 REST API for all task operations
- 📊 Beautiful & Aesthetic Dashboard
- 🗄️ MySQL Database Integration

## 🛠️ Setup Instructions
1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/checklist-app.git
   cd checklist-app
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure MySQL:**
   - Create a database named `checklist_app`.
   - Update `db_config.py` with your MySQL credentials.
   - Run the following SQL to create the tables:
     ```sql
     CREATE TABLE users (
         id INT AUTO_INCREMENT PRIMARY KEY,
         username VARCHAR(150) UNIQUE NOT NULL,
         password_hash VARCHAR(255) NOT NULL
     );
     CREATE TABLE tasks (
         id INT AUTO_INCREMENT PRIMARY KEY,
         user_id INT NOT NULL,
         description TEXT NOT NULL,
         is_done BOOLEAN DEFAULT FALSE,
         FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
     );
     ```
4. **Run the app:**
   ```bash
   python app.py
   ```
5. **Open in browser:**
   - Go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 📚 Usage
- Register a new account.
- Login to your dashboard.
- Add, check, or delete your tasks!

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first.

## 📄 License
This project is licensed under the MIT License. 