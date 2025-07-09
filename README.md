# Skill2Go

Skill2Go is an advanced web application built with Django and integrated with a simulated Ethereum blockchain using Ganache. It is designed for efficient skill-sharing and skill-learning, connecting experts with learners in a secure, verified, and community-like environment.

## Overview

Skill2Go bridges the gap between people who wish to share their expertise and those eager to learn. Leveraging modern web technologies and blockchain for trust verification, the platform ensures that every skill exchange is recorded, secure, and transparent. In addition, an AI system enhances the learning experience by offering real-time conversational support in English, French and Spanish and personalized skill recommendations.

## Key Features

### Blockchain-Enabled Trust & Verification

**Blockchain Integration:**
Skill2Go utilizes Ganache to simulate an Ethereum network. A smart contract, deployed via Remix, securely stores the ABI and contract address within the blockchain module. This allows for immutable record-keeping of skill certifications and exchanges, ensuring trust and transparency.

**SHA-256 Encryption:**
Every document certification uploaded is secured with a SHA-256 hash, guaranteeing the authenticity and integrity of the provided credentials.

### AI-Powered Enhancements

**Conversational Assistant:**
Integrated with the Mixtral V8 model and Kokoro Text-To-Speech, the AI assistant provides users with interactive, real-time language practice (supporting French, English, and Spanish) and tailored advice to boost daily conversational skills.

**SkillMatch AI:**
Utilizing advanced reasoning capabilities of the Mixtral V8 model, Skill2Go intelligently recommends new skills based on a user's personality and interests, fostering continuous personal and professional development.

### Community & Usability

**Skill Exchange:**
Users can initiate and record skill exchanges on the blockchain, ensuring that every transaction is documented in a tamper-proof ledger.

**User Profiles & Listings:**
Create and manage detailed user profiles showcasing skills, expertise, and experiences. Skill listings include rich descriptions and illustrative content, making it easy to find the right match.

**Admin Dashboard:**
A robust dashboard provides administrators with tools for managing skill certifications, monitoring blockchain records of exchanges, and curating platform content to maintain high standards of quality and trust.

## Technical Architecture

### Tech Stack
- **Backend:** Django REST Framework, Python
- **Database:** SQLite (for lightweight local development)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Blockchain Simulation:** Ganache (simulating an Ethereum network)

### AI Models
- **Mixtral-8x7B-Instruct-v0.1:**
  - [Mixtral-8x7B-Instruct-v0.1 on Hugging Face](https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1)
- **Self-hosted Kokoro Text To Speech:**
  - [Kokoro on Hugging Face](https://huggingface.co/coqui/XTTS-v2)

## Setup Instructions

### 1. Environment Setup
- **Clone the Repository:** Open the project folder in VS Code.
- **Create a Virtual Environment:**
  ```bash
  python -m venv env
  ```
- **Activate the Virtual Environment:**
  - Windows:
    ```bash
    .\env\Scripts\activate.ps1
    ```
  - Mac/Linux:
    ```bash
    source env/bin/activate
    ```

### 2. Configure API Access
- **Hugging Face API Key:**
  Generate your API token at Hugging Face and create a .env file in the root directory with the following entry:
  ```bash
  HUGGINGFACE_API_KEY=YOURCREDENTIALS
  ```

### 3. Install Dependencies
- **Install Python Packages:**
  ```bash
  pip install -r requirements.txt
  ```

### 4. Install espeak-ng for AI Support
- **macOS:**
  ```bash
  brew install espeak-ng
  ```

### 4.1  Install a package manager for **Windows**
You'll need to install either *Chocolatey* or *Scoop* to manage the installation.
*Install Chocolatey:*
   -Open PowerShell as Administrator.
   -Run the following command to install Chocolatey:
  ```bash
   Set-ExecutionPolicy Bypass -Scope Process -Force; `
   [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
   iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```
   -Close and reopen PowerShell to apply changes.

*Install Scoop:*
   -Open PowerShell as Administrator.
   -Run the following command to install Scoop:
  ```bash
   iwr -useb get.scoop.sh | iex
```
   -Close and reopen PowerShell to apply changes.

- **Windows:**
  Install either Chocolatey or Scoop. Then install espeak-ng using:
  ```bash
  scoop install espeak-ng
  ```
  or
  ```bash
  choco install espeak-ng
  ```

### 5. Setup Blockchain Environment
- **Install Ganache CLI:**
  Open a new terminal and run:
  ```bash
  npm install -g ganache-cli
  ```
- **Start Ganache:**
  ```bash
  python scripts/start_ganache.py
  ```
- **Compile and deploy the contract:**
  ```bash
  python scripts/deploy.py
  ```


### 6. Project Initialization
- **Navigate to the Project Directory:**
  ```bash
  cd skill2go/
  ```
- **Populate the Database:**
  ```bash
  python load_db.py
  ```
- **Apply Migrations:**
  ```bash
  python manage.py migrate
  ```

### 7. Launch the Application
- **Start the Django Server:**
  ```bash
  python manage.py runserver
  ```
- **Access the App:**
  Open http://127.0.0.1:8000/ in your browser.

### 8. Registration and Security
- **User Registration:**
  Click on the 'Sign-Up' button in the navigation bar to create an account.
- **Password Requirements:**
  Ensure your password meets the following:
  - 8-12 characters minimum
  - A mix of uppercase, lowercase, numbers, and symbols
  - Avoid common or easily guessable passwords

## Additional Technologies
- **Smart Contract Deployment:** Remix


