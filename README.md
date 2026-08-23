  🎙️ Meeting Summarizer Pro 

  

> AI-powered meeting summarization using Google Gemini AI with a modern, accessible UI 

  

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org) 

[![Streamlit](https://img.shields.io/badge/Streamlit-1.62.0-red.svg)](https://streamlit.io) 

[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-2.19.0-orange.svg)](https://ai.google.dev) 

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) 

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com) 

[![Deployed](https://img.shields.io/badge/Deployed-Streamlit%20Cloud-brightgreen.svg)](https://share.streamlit.io) 

  

--- 

  

 📊 Overview 

  

  Meeting Summarizer Pro   is a powerful web application that transforms meeting audio and transcripts into structured, actionable summaries using Google's Gemini AI. It helps teams save time, capture decisions, and track action items efficiently. 

  

  🎯 The Problem 

  

Meetings are essential but often result in: 

- ❌   Information loss   - Critical decisions get forgotten 

- ❌   Unstructured notes   - Action items get lost in long transcripts 

- ❌   Wasted time   - Manually reviewing hours of recordings 

- ❌   Poor accountability   - Who was responsible for what? 

  

  💡 The Solution 

  

Meeting Summarizer Pro solves these problems by: 

- ✅   Automatically transcribing   meeting audio 

- ✅   Extracting key decisions   and discussion points 

- ✅   Identifying action items   with owners and deadlines 

- ✅   Generating structured summaries   in seconds 

- ✅   Providing downloadable formats   (TXT, Markdown) 

  

--- 

  

 ✨ Key Features 

  

| Feature | Description | 

|---------|-------------| 

| 🎵   Audio Upload   | Upload MP3, WAV, M4A, OGG, FLAC, AAC, and more | 

| 📝   Text Input   | Paste transcripts for instant summarization | 

| 🤖   Gemini AI   | Powered by Google's state-of-the-art Gemini 3.7 Flash | 

| 📊   Structured Output   | Actionable insights with decisions and action items | 

| 💾   Export Options   | Download as TXT or Markdown | 

| ♿   Accessible   | WCAG AA compliant with high contrast and focus states | 

| 🎨   Modern UI   | Clean, professional interface with design tokens | 

| ⚡   Fast Processing   | Get summaries in seconds, not hours | 

| 🔒   Privacy First   | Your data is processed securely, no permanent storage | 

  

--- 

  

 🎯 Perfect For 

  

| Use Case | Description | 

|----------|-------------| 

|   Remote Teams   | Summarize virtual meetings and video calls | 

|   Project Managers   | Track decisions and action items | 

|   Researchers   | Extract insights from interviews and focus groups | 

|   Students   | Summarize lectures and group discussions | 

|   Business Analysts   | Capture meeting outcomes for reports | 

|   Legal Professionals   | Summarize client consultations | 

  

--- 

  

 🚀 Quick Start 

  

  Prerequisites 

  

- Python 3.10 or higher 

- Google Gemini API key ([Get it here](https://aistudio.google.com/apikey)) 

  

  Installation 

  

 Step 1: Clone the Repository 

  

```bash 

git clone https://github.com/Srishtikumari510/meeting-summarizer.git 

cd meeting-summarizer 

Step 2: Create Virtual Environment 

bash 

  Windows 

python -m venv venv 

venv\Scripts\activate 

  

  Mac/Linux 

python3 -m venv venv 

source venv/bin/activate 

Step 3: Install Dependencies 

bash 

pip install -r requirements.txt 

Step 4: Set Up API Key 

Create a .env file in the project root: 

  

bash 

  Windows 

echo GEMINI_API_KEY=your_api_key_here > .env 

  

  Mac/Linux 

echo "GEMINI_API_KEY=your_api_key_here" > .env 

Step 5: Run the App 

bash 

streamlit run app.py 

The app will open automatically at http://localhost:8501 

  

🎨 Usage Guide 

Option 1: Upload Audio 

Click on "🎵 Upload Audio" tab 

  

Upload your meeting audio file (MP3, WAV, M4A, etc.) 

  

Wait for the audio to upload and process 

  

View the generated summary with: 

  

Meeting Overview 

  

Key Discussion Points 

  

Decisions Made 

  

Action Items 

  

Key Participants 

  

Next Steps 

  

Option 2: Paste Transcript 

Click on "📝 Paste Transcript" tab 

  

Paste your meeting transcript 

  

Select preferences: 

  

Summary Length: Concise, Detailed, or Executive Brief 

  

Include Attendees: Toggle on/off 

  

Include Timeline: Toggle on/off 

  

Click "Generate Summary" 

  

Download as TXT or Markdown 

  

🛠️ Tech Stack 

Component	Technology	Version 

Frontend & Backend	Streamlit	1.62.0 

AI Model	Google Gemini	3.7 Flash 

Language	Python	3.10+ 

Package Manager	pip	Latest 

Version Control	Git	Latest 

Hosting	Streamlit Cloud	Free Tier 

📁 Project Structure 

text 

meeting-summarizer/ 

├── app.py                   Main application 

├── requirements.txt         Python dependencies 

├── README.md               Project documentation 

├── LICENSE                 MIT License 

├── .gitignore              Git ignore rules 

├── .env                    API keys (gitignored) 

└── .streamlit/ 

    └── config.toml         Streamlit configuration (optional) 

🎨 Design Tokens 

The UI follows a comprehensive design system: 

  

Token	Value	Usage 

primary_background	 F8F9FA	Main app background 

surface_background	 FFFFFF	Cards, sidebar, modals 

primary_text	 212529	All body text 

secondary_text	 64748B	Captions, metadata 

primary_action	 2563EB	Buttons, highlights 

primary_action_hover	 1D4ED8	Button hover state 

secondary_action	 475569	Secondary buttons 

border_color	 E2E8F0	Card borders, dividers 

success_state	 16A34A	Success messages 

error_state	 DC2626	Error messages 

heading_color	 0F172A	All headings 

font_family	Inter	Modern sans-serif 

Accessibility (WCAG AA) 

✅ 4.5:1 minimum contrast ratio for all text 

  

✅ Clear focus states with visible outlines 

  

✅ Proper heading hierarchy (H1 → H2 → H3) 

  

✅ Screen reader friendly with semantic HTML 

  

✅ Keyboard navigable interactive elements 

  

📊 Sample Output 

Input (Transcript) 

text 

Meeting: Weekly Team Sync - August 23, 2026 

Attendees: Sarah (PM), Alex (Developer), Maria (Designer) 

  

Sarah: This week we need to focus on the user dashboard. 

Alex: I've completed the backend API. 

Maria: Design review is complete. 

  

Decisions: 

- Launch dashboard by August 30 

- Use dark theme by default 

  

Action Items: 

- Alex: Complete frontend (Aug 27) 

- Maria: Get feedback (Aug 24) 

Output (Summary) 

markdown 

 Meeting Overview 

-   Purpose:   Weekly team sync to review dashboard progress 

-   Outcome:   Dashboard launch date set, design finalized 

  

 Key Discussion Points 

- Dashboard layout and features finalized 

- API integration progress reviewed 

  

 Decisions Made 

- Launch dashboard by August 30 

- Use dark theme by default 

- Add user analytics section 

  

 Action Items 

| Task | Owner | Deadline | 

|------|-------|----------| 

| Complete frontend integration | Alex | Aug 27 | 

| Get design feedback | Maria | Aug 24 | 

| Send launch announcement | Sarah | Aug 25 | 

  

 Next Steps 

- Schedule follow-up meeting on August 28 

- Prepare demo for client 

🤝 Contributing 

Contributions are welcome! Here's how: 

  

1. Fork the Repository 

Click the "Fork" button on GitHub 

  

2. Clone Your Fork 

bash 

git clone https://github.com/yourusername/meeting-summarizer.git 

cd meeting-summarizer 

3. Create a Feature Branch 

bash 

git checkout -b feature/AmazingFeature 

4. Make Your Changes 

bash 

  Add your changes 

git add . 

git commit -m "Add AmazingFeature" 

git push origin feature/AmazingFeature 

5. Open a Pull Request 

Go to your fork on GitHub and click "New Pull Request" 

  

📝 Development Roadmap 

✅ Completed 

☑ Audio upload functionality 

☑ Text transcript input 

☑ Gemini AI integration 

☑ Structured summary output 

☑ Download as TXT and Markdown 

☑ WCAG AA compliant UI 

☑ Modern design system 

🚧 In Progress 

□ Batch processing (multiple files) 

□ Custom prompt templates 

□ Summary history 

🔜 Future Plans 

□ Real-time meeting recording 

□ Language translation support 

□ Integrate with calendars (Google, Outlook) 

□ Team collaboration features 

□ Mobile app version 

🔒 Privacy & Security 

No permanent storage: Audio files and transcripts are deleted after processing 

  

Secure API communication: All requests to Gemini are encrypted 

  

No tracking: We don't track user behavior or store analytics 

  

Open source: Full transparency in how the app works 

  

📄 License 

This project is licensed under the MIT License - see the LICENSE file for details. 

  

🙏 Acknowledgments 

Technology	Purpose 

Google Gemini AI	Powerful AI capabilities for audio processing and summarization 

Streamlit	Amazing web framework for rapid development 

Inter Font	Beautiful, clean typography 

Font Awesome	Icons (via Streamlit) 

📞 Contact & Support 

Author: Srishti Kumari 

  

GitHub: Srishtikumari510 

  

Project Links: 

  

GitHub Repository: https://github.com/Srishtikumari510/meeting-summarizer 

  

Live Demo: https://srishtikumari510-meeting-summarizer.streamlit.app (Coming soon) 

  

Support: 

  

Bugs/Issues: Report a bug 

  

Feature Requests: Suggest a feature 

  

⭐ Show Your Support 

If you find this project useful, please: 

  

⭐ Star the repository on GitHub 

  

🍴 Fork it to contribute 

  

📢 Share it with your network 

  

Built with ❤️ using Python & Google Gemini AI 
