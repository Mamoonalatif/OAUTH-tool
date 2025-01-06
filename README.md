# OAUTH-tool
![image](https://github.com/user-attachments/assets/9568683a-6688-4913-821c-67a945213563)
![image](https://github.com/user-attachments/assets/d691c9d4-e4a6-41bb-a546-a8f9e5f8215b)
# Google OAuth 2.0 Flask Application
This is a Flask-based web application that implements Google OAuth 2.0 for user authentication. It allows users to log in using their Google account, manage their session, and store user information in an SQLite database.

## Features
- **Google OAuth 2.0 Authentication**: Log in securely using Google credentials.
- **SQLite Integration**: Store and update user information in a local database.
- **Session Management**: Maintain user sessions using Flask's session mechanism.
- **Account Deletion**: Revoke Google account access and remove user data.
- **User-Friendly Routes**: Intuitive navigation for login, logout, account deletion, and home page.

## Requirements
- Python 3.7+
- Flask
- SQLite
- Requests

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repository/google-oauth-flask-app.git
   cd google-oauth-flask-app
   ```

2. **Set Up Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Unix
   venv\Scripts\activate     # For Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**
   The script automatically creates and initializes the SQLite database (`userss.db`) upon startup.

5. **Update OAuth Credentials**
   Replace `CLIENT_ID` and `CLIENT_SECRET` in the script with your Google Cloud credentials. Make sure to update the `REDIRECT_URI` as well.

6. **Run the Application**
   ```bash
   python app.py
   ```

7. **Access the Application**
   Open your browser and navigate to `http://127.0.0.1:5000`.

## Directory Structure
```
.
├── app.py                   # Main application file
├── templates/
│   ├── home.html            # User dashboard page
│   ├── index.html           # Login page
├── userss.db                # SQLite database (auto-created)
├── requirements.txt         # Dependency file
└── README.md                # This file
```

## Routes
- `/`: Landing page, showing login or user dashboard.
- `/login`: Redirects users to Google for authentication.
- `/callback`: Handles OAuth callback and processes tokens.
- `/home`: Displays user information after login.
- `/logout`: Logs the user out and clears the session.
- `/delete_account`: Revokes Google access and deletes user data from the database.

## Notes
- Ensure the `REDIRECT_URI` in the code matches the URI configured in your Google Cloud project.
- Use a secure secret key for the Flask app in production to prevent session tampering.
