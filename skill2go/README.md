#  Skill2Go
Skill2Go is a web application developed with Django that serves as a platform for skill-sharing. It enables users to connect with others who are offering or seeking specific skills, such as coding, design, or language learning. By facilitating skill exchange, Skill2Go aims to create a unique community where people can share their knowledge, learn new skills, and grow professionally and personally.

The platform allows users to create profiles, list skills they are willing to offer, and engage with others who may be looking for specific expertise. It also features an admin dashboard for managing users, skills, and content on the site. With an emphasis on easy discovery, skills can be categorized, tagged, and rated by users after each exchange.

## Purpose
The primary goal of Skill2Go is to create a collaborative environment where users can offer and learn new skills without barriers. Whether you're an experienced professional or someone looking to learn something new, Skill2Go allows you to engage with a community that shares your interest in personal and professional development.

## Key Features
1. User Profiles: Users can create and manage personal profiles, showcasing their expertise, skills, and experiences. Profiles help users build credibility and connect with others who are interested in their offerings.

2.Skill Listings: Users can list the skills they are offering along with detailed descriptions. Each skill can also have media such as images or videos attached (to be implemented3)to give others a better understanding of what is being shared.

3.Admin Dashboard: Admins have access to a dedicated dashboard to manage and oversee user activities, skill offerings, and platform content. This feature allows for easier moderation and content control.

4.User Feedback & Ratings (to be implemented): After each skill exchange, users can rate the session and provide feedback, ensuring the quality of interactions on the platform. This system helps build trust among users and enhances the learning experience.

5. Categories & Tags: Skills are categorized by type and tagged for better discoverability. This makes it easier for users to find the skills they need, improving the overall user experience and engagement.

6. Skill Matching: The platform provides matching features based on user profiles, making it easier for users to find the skills they are looking for. This feature helps to optimize user engagement and promotes skill-sharing among relevant parties.


## Tech Stack
1. Django
2. Python
3. SQLite
4. HTML/CSS/JavaScript
5. Bootstrap



Steps to set up the project:
### 1. Create a virtual environment and activate it
- Open the extracted folder in **VS Code**.
- In the terminal, create the virtual environment:
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


### 2. Install Django
Once inside the virtual environment, install Django:
```bash
pip install django
```
### 3. Install dependencies
Install dependencies with 
```bash
pip install -r requirements.txt
```

### 4.  Navigate to the Project Directory
MOve to the `core` directory where the `manage.py` file is located:
```bash
cd skill2go/
```
### 5. Migrate the Database
-Load the initial data to populate skill categories and sample records:  `python manage.py loaddata initial_data.json` 
-Migrate the database schema:  `python manage.py migrate` 

### 6. Create a superuser
To access the Django admin panel, create a superuser account:
```bash
   python manage.py createsuperuser
```
### 6. Start the Server
-Run python manage.py runserver
-Go to http://127.0.0.1:8000/, click on the sign-up button,create and account and then log in.

