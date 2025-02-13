# Skill2Go

**Video Demo:** (https://youtu.be/AS7r_lhPPeQ) 

Skill2Go is a Django-based web application that facilitates skill-sharing and skill-learning.  It connects users who are offering specific skills with those seeking to learn them.  ***Skill2Go also helps users improve their daily conversational skills in French, English, or Spanish.***  The platform aims to build a community where individuals can share knowledge, acquire new skills, and grow both professionally and personally.

## Purpose

Skill2Go's primary goal is to create a collaborative environment where users can seamlessly offer and learn skills, breaking down traditional barriers to education and knowledge sharing.

## Key Features

* **User Profiles:** Users can create and manage profiles showcasing their expertise, skills, and experience.  Profiles enhance credibility and facilitate connections with others who share similar interests.
* **Skill Listings:** Users can list the skills they offer, providing detailed descriptions.  Future implementations will include the ability to attach media like images or videos to further illustrate the skills being shared.
* **Admin Dashboard:**  A dedicated admin dashboard allows administrators to manage user activities, skill offerings, and platform content, ensuring easy moderation and content control.
* **AI-Powered Conversational Assistant:**  An AI assistant helps users practice languages, providing real-time advice and feedback.

## Tech Stack

* Django rest framework
* Python
* SQLite
* HTML/CSS/JavaScript
* Bootstrap

## AI Models

* Mixtral-8x7B-Instruct-v0.1: https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1
* Kokoro: https://huggingface.co/hexgrad/Kokoro-82M

## Setup Instructions

### 1. Set up the Virtual Environment

1. Open the extracted project folder in VS Code.
2. Open the terminal.
3. Create a virtual environment:
   ```bash
   python -m venv env
   ```
- Activate the virtual environment (Windows):
   ```bash
   .\env\Scripts\activate.ps1
   ```

- Activate the virtual environment (Mac/Linux):
```bash
   source env/bin/activate
```


### 2. Install Dependencies
Install dependencies with 
```bash
pip install -r requirements.txt
```

### 4.  Navigate to the Project Directory
MOve to the `core` directory where the `manage.py` file is located:
```bash
cd skill2go/
```

### 4. Configure Hugging Face API Key
Create a .env file in the skill2go directory and add your Hugging Face API key:
```bash
HUGGINGFACE_API_KEY = YOURCREDENTIALS
```
### 5. Install espeak-ng (macOS): 
For multi-language support, install espeak-ng using Homebrew:
```bash
brew install espeak-ng for mac
```

### 6. Apply migrations: 
-Load the initial data to populate skill categories and sample records:  `sqlite3 db.sqlite3 < data-sqlite3.sql` 
-Apply the migrations:  `python manage.py makemigrations` 
-Migrate the database schema:  `python manage.py migrate` 

### 6. Register in the app
Create an account (since using the django model, your password must be):
✅Minimum length: At least 8-12 characters
✅ A mix of uppercase, lowercase, numbers, and symbols
✅ Do not use easy-to-guess passwords (e.g., password123)

OR just use a password manager: For auto-generated secure passwords

### 6. Start the Server
-Run python manage.py runserver
-Go to http://127.0.0.1:8000/ and then log in.
-Have fun

