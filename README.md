 🎙️ Meeting Summarizer Pro

[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit_Cloud-FF4B4B?style=for-the-badge\&logo=streamlit)](https://meetingsummarizerpro.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square\&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.62.0-red?style=flat-square\&logo=streamlit)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Gemini-Google_AI-4285F4?style=flat-square\&logo=google)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

>  AI-powered meeting summarization using Google Gemini AI with a modern and accessible Streamlit interface. 

---

## 🌐 Live Demo

🚀  Try Meeting Summarizer Pro: 

 https://meetingsummarizerpro.streamlit.app 

Upload a meeting recording or paste a transcript and generate a structured, actionable summary within seconds.

---

## 📌 Overview

 Meeting Summarizer Pro  is an AI-powered web application that converts meeting audio and transcripts into concise, structured summaries using  Google Gemini AI .

Instead of manually going through lengthy meeting recordings or transcripts, users can upload their audio or paste text and automatically extract:

* 📄 Meeting overview
* 💬 Key discussion points
* ✅ Decisions made
* 📋 Action items
* 👤 Participants
* ⏰ Deadlines
* ➡️ Next steps

The application is designed to help students, project managers, researchers, business teams, and professionals save time and improve meeting productivity.

---

## 🎯 Problem Statement

Meetings often generate a large amount of information, making it difficult to identify what actually matters.

### Common Problems

* ❌ Important decisions can be forgotten.
* ❌ Action items become buried inside long discussions.
* ❌ Reviewing hours of recordings takes significant time.
* ❌ Meeting notes are often inconsistent or incomplete.
* ❌ Responsibilities and deadlines may not be clearly tracked.

---

## 💡 Solution

Meeting Summarizer Pro uses  Google Gemini AI  to analyze meeting audio or transcripts and transform them into structured information.

### Workflow

```text
Meeting Audio / Transcript
          ↓
     User Uploads File
          ↓
      Gemini AI Processing
          ↓
   Content Understanding
          ↓
     Information Extraction
          ↓
 ┌─────────────────────────┐
 │ Meeting Overview        │
 │ Key Discussion Points   │
 │ Decisions              │
 │ Action Items           │
 │ Participants           │
 │ Next Steps              │
 └─────────────────────────┘
          ↓
   Downloadable Summary
```

---

## ✨ Key Features

| Feature                           | Description                                                                 |
| --------------------------------- | --------------------------------------------------------------------------- |
| 🎵  Audio Upload                | Upload MP3, WAV, M4A, OGG, FLAC, AAC and other supported formats.           |
| 📝  Transcript Input            | Paste an existing meeting transcript directly into the application.         |
| 🤖  Gemini AI                   | Uses Google's Gemini AI for intelligent content analysis and summarization. |
| 📊  Structured Summary          | Converts unstructured discussions into organized meeting insights.          |
| ✅  Decision Extraction          | Identifies important decisions made during the meeting.                     |
| 📋  Action Items                | Extracts tasks, owners and deadlines when available.                        |
| 👥  Participant Identification  | Identifies participants mentioned in the meeting content.                   |
| 💾  Export                      | Download generated summaries as TXT or Markdown files.                      |
| 🎨  Modern UI                   | Clean and professional Streamlit interface.                                 |
| ♿  Accessible UI                | Designed with accessibility and keyboard navigation in mind.                |
| 🔒  Privacy Focused             | No permanent application-level storage of uploaded meeting content.         |

---

## 🎯 Use Cases

### 👨‍💼 Project Managers

Quickly identify:

* Project decisions
* Assigned tasks
* Deadlines
* Follow-up activities

### 👩‍💻 Development Teams

Convert technical meetings into structured development tasks and decisions.

### 🎓 Students

Summarize:

* Lectures
* Group discussions
* Project meetings
* Study sessions

### 🔬 Researchers

Extract important information from:

* Interviews
* Focus groups
* Research discussions
* Academic meetings

### 📊 Business Analysts

Generate structured meeting notes for reports, stakeholders and project documentation.

---

## 🛠️ Tech Stack

| Component                  | Technology      |
| -------------------------- | --------------- |
|  Programming Language    | Python 3.10+    |
|  Frontend                | Streamlit       |
|  Backend                 | Python          |
|  AI Model                | Google Gemini   |
|  Environment Management  | python-dotenv   |
|  Version Control         | Git & GitHub    |
|  Deployment              | Streamlit Cloud |

---

## 📁 Project Structure

```text
meeting-summarizer/
│
├── app.py
│   └── Main Streamlit application
│
├── requirements.txt
│   └── Python dependencies
│
├── README.md
│   └── Project documentation
│
├── LICENSE
│   └── MIT License
│
├── .gitignore
│   └── Ignored files and secrets
│
├── .env
│   └── Local API credentials
│
└── .streamlit/
    └── config.toml
        └── Optional Streamlit configuration
```

> ⚠️ Never commit `.env` or API keys to GitHub.

---

# 🚀 Getting Started

## Prerequisites

Make sure you have:

* Python  3.10 or higher 
* pip
* Git
* Google Gemini API key

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/Srishtikumari510/meeting-summarizer.git
```

```bash
cd meeting-summarizer
```

---

## 2️⃣ Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Gemini API

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

You can obtain a Gemini API key from Google's AI platform.

---

## 5️⃣ Run the Application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

# 🎨 How to Use

## Option 1 — Upload Meeting Audio

1. Open the application.
2. Select  Upload Audio .
3. Upload your meeting recording.
4. Wait for Gemini AI to process the content.
5. Review the generated summary.
6. Download the summary as TXT or Markdown.

### Supported Audio Formats

```text
MP3
WAV
M4A
OGG
FLAC
AAC
```

---

## Option 2 — Paste Transcript

1. Open the  Paste Transcript  section.
2. Paste your meeting transcript.
3. Select your preferred summary style.
4. Choose optional information such as attendees or timeline.
5. Click  Generate Summary .
6. Review the results.
7. Download the summary.

---

# 📄 Generated Summary

The application can generate sections such as:

```markdown
# Meeting Overview

## Key Discussion Points

## Decisions Made

## Action Items

| Task | Owner | Deadline |
|------|-------|----------|
| Complete frontend | Alex | Aug 27 |
| Get design feedback | Maria | Aug 24 |
| Send announcement | Sarah | Aug 25 |

## Participants

## Next Steps
```

---

# 🎨 UI & Accessibility

The application follows a clean design system focused on usability and accessibility.

### Design Principles

* High contrast text
* Clear visual hierarchy
* Consistent spacing
* Responsive layout
* Visible interaction states
* Keyboard-friendly controls
* Clear error and success messages

### Color System

| Token              | Value     |
| ------------------ | --------- |
| Primary Background | `#F8F9FA` |
| Surface            | `#FFFFFF` |
| Primary Text       | `#212529` |
| Secondary Text     | `#64748B` |
| Primary Action     | `#2563EB` |
| Hover Action       | `#1D4ED8` |
| Border             | `#E2E8F0` |
| Success            | `#16A34A` |
| Error              | `#DC2626` |
| Heading            | `#0F172A` |

---

# 🔐 Privacy & Security

Meeting content can contain sensitive information, so privacy is an important consideration.

The application is designed so that:

* 🔒 API communication uses secure connections.
* 🚫 API keys are stored through environment variables.
* 🚫 `.env` files are excluded from Git.
* 🗑️ Uploaded content is not intentionally stored permanently by the application.
* 🔑 API credentials should never be committed to the repository.

>  Important:  Users should avoid uploading confidential or sensitive meeting information unless they are comfortable with the applicable third-party AI processing terms.

---

# 📈 Development Roadmap

## ✅ Completed

* [x] Streamlit web interface
* [x] Audio upload
* [x] Transcript input
* [x] Gemini AI integration
* [x] Structured meeting summaries
* [x] Decision extraction
* [x] Action-item extraction
* [x] TXT export
* [x] Markdown export
* [x] Modern UI
* [x] Streamlit Cloud deployment

## 🚧 In Progress

* [ ] Batch audio processing
* [ ] Custom summary templates
* [ ] Summary history
* [ ] Improved speaker identification

## 🔮 Future Plans

* [ ] Real-time meeting recording
* [ ] Multi-language transcription
* [ ] Automatic translation
* [ ] Google Calendar integration
* [ ] Microsoft Outlook integration
* [ ] Team collaboration
* [ ] User authentication
* [ ] Meeting analytics dashboard
* [ ] Mobile application

---

# 🤝 Contributing

Contributions are welcome!

### 1. Fork the Repository

Click the  Fork  button on GitHub.

### 2. Clone Your Fork

```bash
git clone https://github.com/yourusername/meeting-summarizer.git
```

```bash
cd meeting-summarizer
```

### 3. Create a Feature Branch

```bash
git checkout -b feature/AmazingFeature
```

### 4. Make Your Changes

```bash
git add .
```

```bash
git commit -m "Add AmazingFeature"
```

### 5. Push Your Changes

```bash
git push origin feature/AmazingFeature
```

### 6. Create a Pull Request

Open your repository on GitHub and create a  Pull Request .

---

# 📜 License

This project is licensed under the  MIT License .

See the `LICENSE` file for more information.

---

# 🙏 Acknowledgments

This project was built using:

*  Google Gemini AI  — AI-powered meeting analysis
*  Streamlit  — Web application framework
*  Python  — Application development
*  GitHub  — Version control and collaboration
*  Streamlit Cloud  — Application deployment

---

# 👩‍💻 Author

## Srishti Kumari

🎓 MCA Student
💻 AI / ML & Software Development Enthusiast

### 🔗 Project Links

*  GitHub:  https://github.com/Srishtikumari510
*  Repository:  https://github.com/Srishtikumari510/meeting-summarizer
*  Live Demo:  https://meetingsummarizerpro.streamlit.app

---

# ⭐ Support the Project

If you find  Meeting Summarizer Pro  useful:

⭐ Star the repository
🍴 Fork the project
🐛 Report bugs
💡 Suggest new features
📢 Share it with others

---

<div align="center">

### 🎙️ Turn Meetings Into Actionable Insights

 Built with ❤️ using Python, Streamlit & Google Gemini AI 

</div>
