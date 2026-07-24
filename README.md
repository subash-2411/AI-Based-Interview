# AI Interview Pro

An intelligent, AI-powered interview preparation platform that allows users to upload their resumes, receive ATS scores, and practice mock interviews (both HR/Technical and Coding rounds) with an AI interviewer. It supports both English and Tamil languages and provides detailed, actionable feedback and gamified scoring.

## 🚀 Features

*   **User Authentication**: Secure login and signup using Email or Google OAuth (powered by Django Allauth).
*   **Resume Parsing & ATS Scoring**: Upload resumes (PDF/DOCX). The system automatically extracts text, identifies key skills, and calculates an ATS (Applicant Tracking System) score using advanced NLP.
*   **AI Mock Interviews**:
    *   Dynamic, interactive interview sessions tailored specifically to the user's uploaded resume and selected difficulty level.
    *   Multilingual support, including English (`en-US`) and Tamil (`ta-IN`).
    *   Audio and Video processing integration via MediaPipe and OpenCV.
    *   Powered by Google Gemini for intelligent question generation and answer evaluation.
*   **Coding Rounds**: A dedicated IDE-like section for practicing coding problems with real-time code evaluation and scoring.
*   **User Dashboard & Gamification**: Tracks user history, total interviews taken, average scores, and awards XP and Levels to keep users engaged and motivated.

## 🛠️ Tech Stack

*   **Backend Framework**: Django 6.0, Django REST Framework
*   **Database**: SQLite (Development)
*   **AI & NLP Models**: Google Gemini API, SpaCy, NLTK, Scikit-learn, Sentence-Transformers
*   **Document Processing**: PyPDF2, pdfplumber, python-docx
*   **Computer Vision/Audio**: OpenCV, MediaPipe
*   **Authentication**: Django Allauth (Google OAuth integration)
*   **Production Server**: Gunicorn, Whitenoise (for static file handling)

## 📁 Project Structure

```text
AI_Interview_Project/
├── core/               # Main Django project settings and routing
├── accounts/           # User models, authentication, and history tracking
├── resume/             # Resume upload, NLP parsing, and ATS scoring logic
├── interview/          # Audio/Video AI interview sessions and evaluation
├── coding_round/       # Coding practice problems and submissions
├── dashboard/          # User interface for tracking progress
├── ai_engine/          # Core AI logic (Gemini integration, evaluation scripts)
├── media/              # User-uploaded files (resumes, profile pics, etc.)
├── templates/          # HTML templates for the frontend
└── static/             # CSS, JS, and image assets
```

## ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd AI_Interview_Project
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    
    # On Windows:
    venv\Scripts\activate
    
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: You may need to download SpaCy and NLTK language models separately depending on your system setup.*
    ```bash
    python -m spacy download en_core_web_sm
    ```

4.  **Environment Variables:**
    Create a `.env` file in the root directory and add the necessary API keys and credentials:
    ```env
    SECRET_KEY=your_django_secret_key
    DEBUG=True
    GEMINI_API_KEY=your_google_gemini_api_key
    ```

5.  **Run Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Create Superuser (Optional):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```
    Visit `http://127.0.0.1:8000/` in your browser to access the platform.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License
This project is licensed under the MIT License.
