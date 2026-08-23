\# 🎙️ Meeting Summarizer Pro



> AI-powered meeting summarization using Google Gemini AI with a modern, accessible UI



\[!\[Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)

\[!\[Streamlit](https://img.shields.io/badge/Streamlit-1.62.0-red.svg)](https://streamlit.io)

\[!\[Google Gemini](https://img.shields.io/badge/Google%20Gemini-2.19.0-orange.svg)](https://ai.google.dev)

\[!\[License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)



\## 📊 Overview



\*\*Meeting Summarizer Pro\*\* is a powerful web application that transforms meeting audio and transcripts into structured, actionable summaries using Google's Gemini AI. It helps teams save time, capture decisions, and track action items efficiently.



\### ✨ Key Features



| Feature | Description |

|---------|-------------|

| 🎵 \*\*Audio Upload\*\* | Upload MP3, WAV, M4A, OGG, and more |

| 📝 \*\*Text Input\*\* | Paste transcripts for instant summarization |

| 🤖 \*\*Gemini AI\*\* | Powered by Google's state-of-the-art Gemini 3.7 Flash |

| 📊 \*\*Structured Output\*\* | Actionable insights with decisions and action items |

| 💾 \*\*Export Options\*\* | Download as TXT or Markdown |

| ♿ \*\*Accessible\*\* | WCAG AA compliant with high contrast and focus states |

| 🎨 \*\*Modern UI\*\* | Clean, professional interface with design tokens |



\### 🎯 Perfect For



\- \*\*Remote Teams\*\* - Summarize virtual meetings

\- \*\*Project Managers\*\* - Track decisions and action items

\- \*\*Researchers\*\* - Extract insights from interviews

\- \*\*Students\*\* - Summarize lectures and group discussions



\## 🚀 Quick Start



\### Prerequisites



\- Python 3.10 or higher

\- Google Gemini API key (\[Get it here](https://aistudio.google.com/apikey))



\### Installation



```bash

\# Clone the repository

git clone https://github.com/yourusername/meeting-summarizer.git

cd meeting-summarizer



\# Create virtual environment

python -m venv venv



\# Activate virtual environment

\# Windows:

venv\\Scripts\\activate

\# Mac/Linux:

source venv/bin/activate



\# Install dependencies

pip install -r requirements.txt



\# Create .env file with your API key

echo GEMINI\_API\_KEY=your\_api\_key\_here > .env



\# Run the app

streamlit run app.py

"# meeting-summarizer" 
