Flask Resume Analyzer
A Flask web application that analyzes resumes using Google's Gemini AI API.
Features

Upload and analyze resume files
AI-powered resume evaluation using Gemini API
Web-based interface for easy interaction
Secure file handling and processing

Prerequisites

Python 3.7 or higher
Google Gemini API key

Installation

Clone the repository
bashgit clone https://github.com/yourusername/flask-resume-analyzer.git
cd flask-resume-analyzer

Create a virtual environment
bashpython -m venv myenv

# On Windows
myenv\Scripts\activate

# On macOS/Linux
source myenv/bin/activate

Install dependencies
bashpip install -r requirements.txt

Set up environment variables

Create a .env file in the project root
Add your Gemini API key:

GEMINI_API_KEY=your_api_key_here

Create necessary directories
bashmkdir Uploaded_Resumes
mkdir instance


Usage

Run the application
bashpython project5.py

Open your browser

Navigate to http://localhost:5000
Upload a resume file and get AI-powered analysis



Project Structure
flask-resume-analyzer/
│
├── static/              # Static assets (CSS, JS, images)
├── templates/           # HTML templates
├── Logo/               # Application logo files
├── project5.py         # Main Flask application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in repo)
├── .gitignore         # Git ignore rules
└── README.md          # This file
API Configuration
This application uses the Google Gemini API. You'll need to:

Get a Gemini API key from Google AI Studio
Add it to your .env file as shown in the installation steps

Contributing

Fork the repository
Create a feature branch (git checkout -b feature/new-feature)
Commit your changes (git commit -am 'Add new feature')
Push to the branch (git push origin feature/new-feature)
Create a Pull Request