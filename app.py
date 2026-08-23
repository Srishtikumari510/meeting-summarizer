"""Meeting Summarizer Pro - WCAG AA Compliant UI/UX Design"""
import streamlit as st
import os
from dotenv import load_dotenv
import tempfile
from pathlib import Path
import time
from google import genai
from datetime import datetime

load_dotenv()

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Meeting Summarizer Pro",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# DESIGN TOKENS - WCAG AA COMPLIANT
# ============================================
DESIGN_TOKENS = {
    # Colors
    "primary_background": "#F8F9FA",
    "surface_background": "#FFFFFF",
    "primary_text": "#212529",
    "secondary_text": "#64748B",
    "primary_action": "#2563EB",
    "primary_action_hover": "#1D4ED8",
    "secondary_action": "#475569",
    "border_color": "#E2E8F0",
    "success_state": "#16A34A",
    "error_state": "#DC2626",
    "heading_color": "#0F172A",
    
    # Typography
    "font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "body_font_size": "16px",
    "body_line_height": "1.5",
    "heading_weight": "700",
    
    # Spacing
    "spacing_sm": "0.5rem",
    "spacing_md": "1rem",
    "spacing_lg": "2rem",
    "spacing_xl": "3rem",
}

# ============================================
# CUSTOM CSS - DESIGN TOKENS IMPLEMENTATION
# ============================================
st.markdown(f"""
<style>
    /* ==========================================
       FONTS & TYPOGRAPHY
       ========================================== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {{
        font-family: '{DESIGN_TOKENS["font_family"]}';
        box-sizing: border-box;
    }}
    
    /* ==========================================
       LAYOUT & BACKGROUNDS
       ========================================== */
    .main {{
        background-color: {DESIGN_TOKENS["primary_background"]};
        padding: 0;
    }}
    
    .stApp {{
        background-color: {DESIGN_TOKENS["primary_background"]};
    }}
    
    /* Main container */
    .main-container {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem 1.5rem;
    }}
    
    /* ==========================================
       HEADINGS - WCAG AA COMPLIANT
       ========================================== */
    .main-title {{
        font-size: 3rem;
        font-weight: {DESIGN_TOKENS["heading_weight"]};
        color: {DESIGN_TOKENS["heading_color"]};
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }}
    
    .main-title .highlight {{
        background: linear-gradient(135deg, {DESIGN_TOKENS["primary_action"]}, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .sub-title {{
        font-size: 1.2rem;
        font-weight: 400;
        color: {DESIGN_TOKENS["secondary_text"]};
        margin-bottom: 2.5rem;
        line-height: 1.6;
    }}
    
    .section-heading {{
        font-size: 1.5rem;
        font-weight: 600;
        color: {DESIGN_TOKENS["heading_color"]};
        margin-bottom: 1rem;
        letter-spacing: -0.01em;
    }}
    
    .card-heading {{
        font-size: 1.1rem;
        font-weight: 600;
        color: {DESIGN_TOKENS["heading_color"]};
        margin-bottom: 0.5rem;
    }}
    
    /* ==========================================
       BODY TEXT - 4.5:1 CONTRAST RATIO
       ========================================== */
    body, p, li, .body-text {{
        font-size: {DESIGN_TOKENS["body_font_size"]};
        line-height: {DESIGN_TOKENS["body_line_height"]};
        font-weight: 400;
        color: {DESIGN_TOKENS["primary_text"]};
    }}
    
    .secondary-text {{
        color: {DESIGN_TOKENS["secondary_text"]};
        font-size: 0.9rem;
    }}
    
    .caption {{
        color: {DESIGN_TOKENS["secondary_text"]};
        font-size: 0.8rem;
        font-weight: 400;
    }}
    
    /* ==========================================
       CARDS - PURE WHITE ELEVATION
       ========================================== */
    .card {{
        background: {DESIGN_TOKENS["surface_background"]};
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06), 0 1px 2px rgba(0, 0, 0, 0.04);
        border: 1px solid {DESIGN_TOKENS["border_color"]};
        margin-bottom: 1.5rem;
        transition: box-shadow 0.2s ease;
    }}
    
    .card:hover {{
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06), 0 2px 4px rgba(0, 0, 0, 0.04);
    }}
    
    .upload-card {{
        background: {DESIGN_TOKENS["surface_background"]};
        border: 2px dashed {DESIGN_TOKENS["border_color"]};
        border-radius: 12px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.25s ease;
        cursor: pointer;
    }}
    
    .upload-card:hover {{
        border-color: {DESIGN_TOKENS["primary_action"]};
        background: #F0F7FF;
    }}
    
    .upload-card .icon {{
        font-size: 3.5rem;
        display: block;
        margin-bottom: 1rem;
    }}
    
    .upload-card h3 {{
        color: {DESIGN_TOKENS["heading_color"]};
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.25rem;
    }}
    
    .upload-card p {{
        color: {DESIGN_TOKENS["secondary_text"]};
        font-size: 0.95rem;
        margin: 0;
    }}
    
    /* Success Card */
    .success-card {{
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 12px;
        padding: 1.25rem;
        margin: 1rem 0;
    }}
    
    .success-card h4 {{
        color: {DESIGN_TOKENS["success_state"]};
        font-weight: 600;
        margin-bottom: 0.25rem;
    }}
    
    .success-card p {{
        color: {DESIGN_TOKENS["primary_text"]};
        margin: 0.25rem 0;
    }}
    
    /* ==========================================
       SUMMARY BOX
       ========================================== */
    .summary-box {{
        background: {DESIGN_TOKENS["surface_background"]};
        border: 1px solid {DESIGN_TOKENS["border_color"]};
        border-left: 5px solid {DESIGN_TOKENS["primary_action"]};
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        line-height: 1.8;
        white-space: pre-wrap;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    }}
    
    .summary-box h1, .summary-box h2, .summary-box h3 {{
        color: {DESIGN_TOKENS["heading_color"]};
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }}
    
    .summary-box h1:first-child,
    .summary-box h2:first-child,
    .summary-box h3:first-child {{
        margin-top: 0;
    }}
    
    .summary-box ul, .summary-box ol {{
        padding-left: 1.5rem;
        margin: 0.5rem 0;
    }}
    
    .summary-box li {{
        margin: 0.25rem 0;
    }}
    
    /* ==========================================
       BUTTONS - CLEAR STATE SHIFTS
       ========================================== */
    .stButton > button {{
        background: {DESIGN_TOKENS["primary_action"]};
        color: #FFFFFF !important;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 500;
        border-radius: 8px;
        transition: all 0.2s ease;
        width: 100%;
        cursor: pointer;
        box-shadow: 0 1px 3px rgba(37, 99, 235, 0.2);
    }}
    
    /* Hover State */
    .stButton > button:hover {{
        background: {DESIGN_TOKENS["primary_action_hover"]};
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        transform: translateY(-1px);
    }}
    
    /* Active State */
    .stButton > button:active {{
        transform: translateY(0px);
        box-shadow: 0 1px 3px rgba(37, 99, 235, 0.2);
    }}
    
    /* Focus State - Accessibility */
    .stButton > button:focus-visible {{
        outline: 3px solid {DESIGN_TOKENS["primary_action"]};
        outline-offset: 2px;
    }}
    
    /* Secondary Button */
    .secondary-btn > button {{
        background: {DESIGN_TOKENS["secondary_action"]};
        box-shadow: none;
    }}
    
    .secondary-btn > button:hover {{
        background: #334155;
        box-shadow: 0 4px 12px rgba(71, 85, 105, 0.3);
    }}
    
    /* ==========================================
       FEATURE GRID
       ========================================== */
    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }}
    
    .feature-card {{
        background: {DESIGN_TOKENS["surface_background"]};
        border: 1px solid {DESIGN_TOKENS["border_color"]};
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.2s ease;
    }}
    
    .feature-card:hover {{
        border-color: {DESIGN_TOKENS["primary_action"]};
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    }}
    
    .feature-card .emoji {{
        font-size: 2.25rem;
        display: block;
        margin-bottom: 0.5rem;
    }}
    
    .feature-card h4 {{
        color: {DESIGN_TOKENS["heading_color"]};
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.25rem;
    }}
    
    .feature-card p {{
        color: {DESIGN_TOKENS["secondary_text"]};
        font-size: 0.85rem;
        margin: 0;
        line-height: 1.4;
    }}
    
    /* ==========================================
       SIDEBAR - WCAG AA COMPLIANT
       ========================================== */
    section[data-testid="stSidebar"] {{
        background: {DESIGN_TOKENS["surface_background"]};
        border-right: 1px solid {DESIGN_TOKENS["border_color"]};
        padding: 1.5rem 1rem;
    }}
    
    section[data-testid="stSidebar"] .sidebar-logo {{
        text-align: center;
        margin-bottom: 1.5rem;
    }}
    
    section[data-testid="stSidebar"] .sidebar-title {{
        font-size: 1.1rem;
        font-weight: 700;
        color: {DESIGN_TOKENS["heading_color"]};
        text-align: center;
        margin-bottom: 0.25rem;
    }}
    
    section[data-testid="stSidebar"] .sidebar-subtitle {{
        color: {DESIGN_TOKENS["secondary_text"]};
        font-size: 0.85rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }}
    
    section[data-testid="stSidebar"] .sidebar-divider {{
        border: none;
        border-top: 1px solid {DESIGN_TOKENS["border_color"]};
        margin: 1.25rem 0;
    }}
    
    /* ==========================================
       STAT CARDS
       ========================================== */
    .stat-card {{
        background: {DESIGN_TOKENS["surface_background"]};
        border: 1px solid {DESIGN_TOKENS["border_color"]};
        border-radius: 8px;
        padding: 0.75rem;
        text-align: center;
    }}
    
    .stat-card .number {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {DESIGN_TOKENS["primary_action"]};
        display: block;
        line-height: 1.2;
    }}
    
    .stat-card .label {{
        color: {DESIGN_TOKENS["secondary_text"]};
        font-size: 0.75rem;
        font-weight: 500;
    }}
    
    /* ==========================================
       INFO BOX - WCAG AA COMPLIANT
       ========================================== */
    .info-box {{
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    }}
    
    .info-box strong {{
        color: {DESIGN_TOKENS["primary_action"]};
    }}
    
    .info-box p {{
        margin: 0;
        color: {DESIGN_TOKENS["primary_text"]};
    }}
    
    /* ==========================================
       PROGRESS BAR
       ========================================== */
    .stProgress > div > div {{
        background: {DESIGN_TOKENS["primary_action"]};
        border-radius: 4px;
    }}
    
    .stProgress > div {{
        background: {DESIGN_TOKENS["border_color"]};
        border-radius: 4px;
        height: 6px !important;
    }}
    
    /* ==========================================
       TABS
       ========================================== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        border-bottom: 2px solid {DESIGN_TOKENS["border_color"]};
        padding-bottom: 0;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        color: {DESIGN_TOKENS["secondary_text"]};
        border-radius: 8px 8px 0 0;
        transition: all 0.2s ease;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        color: {DESIGN_TOKENS["primary_text"]};
        background: #F1F5F9;
    }}
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        color: {DESIGN_TOKENS["primary_action"]};
        border-bottom: 3px solid {DESIGN_TOKENS["primary_action"]};
        font-weight: 600;
    }}
    
    /* ==========================================
       FOOTER
       ========================================== */
    .footer {{
        text-align: center;
        color: {DESIGN_TOKENS["secondary_text"]};
        font-size: 0.85rem;
        margin-top: 3rem;
        padding: 1.5rem;
        border-top: 1px solid {DESIGN_TOKENS["border_color"]};
    }}
    
    .footer .heart {{
        color: #DC2626;
        display: inline-block;
    }}
    
    /* ==========================================
       RESPONSIVE DESIGN
       ========================================== */
    @media (max-width: 768px) {{
        .main-title {{
            font-size: 2rem;
        }}
        
        .sub-title {{
            font-size: 1rem;
        }}
        
        .feature-grid {{
            grid-template-columns: 1fr 1fr;
        }}
        
        .card {{
            padding: 1rem;
        }}
        
        .upload-card {{
            padding: 2rem 1rem;
        }}
    }}
    
    @media (max-width: 480px) {{
        .feature-grid {{
            grid-template-columns: 1fr;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR - CLEAN, ACCESSIBLE
# ============================================
API_KEY = os.getenv("GEMINI_API_KEY")

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span style="font-size: 3rem;">🎙️</span>
    </div>
    <div class="sidebar-title">Meeting Summarizer</div>
    <div class="sidebar-subtitle">AI-Powered Meeting Intelligence</div>
    """, unsafe_allow_html=True)
    
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    
    # Stats
    st.markdown("### 📊 Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="stat-card">
            <span class="number">∞</span>
            <span class="label">Meetings</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card">
            <span class="number">⚡</span>
            <span class="label">AI Powered</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    
    # Features
    st.markdown("### 🎯 Features")
    st.markdown("""
    - 🎵 **Audio Upload** - MP3, WAV, M4A
    - 📝 **Text Transcript** - Paste & summarize
    - 🤖 **Gemini AI** - State-of-the-art
    - 📊 **Structured Output** - Actionable insights
    - 💾 **Export** - TXT & Markdown
    """)
    
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    
    # Tips
    st.markdown("### 💡 Pro Tips")
    st.markdown("""
    1. Use **clear audio** recordings
    2. Keep meetings **under 60 mins**
    3. Include **speaker names** in transcripts
    4. Mention **action items** explicitly
    """)
    
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    
    # API Status
    if API_KEY:
        st.success("✅ API Key: Connected")
        st.caption("Gemini 3.7 Flash Ready")
    else:
        st.error("❌ API Key: Missing")
        st.caption("Please set GEMINI_API_KEY")

# ============================================
# MAIN CONTENT
# ============================================
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Title Section
st.markdown("""
<h1 class="main-title">
    🎙️ Meeting <span class="highlight">Summarizer</span>
</h1>
<p class="sub-title">
    Transform your meetings into actionable intelligence with AI-powered summarization
</p>
""", unsafe_allow_html=True)

# Feature Grid
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <span class="emoji">🎯</span>
        <h4>Smart Summaries</h4>
        <p>AI extracts key decisions and action items</p>
    </div>
    <div class="feature-card">
        <span class="emoji">⚡</span>
        <h4>Instant Processing</h4>
        <p>Get summaries in seconds, not hours</p>
    </div>
    <div class="feature-card">
        <span class="emoji">🔒</span>
        <h4>Privacy First</h4>
        <p>Your data is processed securely</p>
    </div>
    <div class="feature-card">
        <span class="emoji">📱</span>
        <h4>Works Anywhere</h4>
        <p>Upload from any device, anytime</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# CHECK API KEY
# ============================================
if not API_KEY:
    st.markdown("""
    <div class="info-box">
        <strong>⚠️ API Key Required</strong>
        <p>Please set your GEMINI_API_KEY in the .env file or paste it below.</p>
    </div>
    """, unsafe_allow_html=True)
    
    api_key_input = st.text_input("Paste your API key here:", type="password")
    if api_key_input:
        API_KEY = api_key_input
        st.success("✅ API Key set successfully!")
    else:
        st.markdown("""
        <div class="card" style="background:#F8FAFC; padding:1.25rem;">
            <p style="margin:0; font-size:0.95rem;">
                💡 <strong>Need an API Key?</strong><br>
                1. Go to <a href="https://aistudio.google.com/apikey" target="_blank">Google AI Studio</a><br>
                2. Sign in with your Google account<br>
                3. Click "Create API Key"<br>
                4. Copy and paste it above
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

# ============================================
# INITIALIZE GEMINI
# ============================================
try:
    client = genai.Client(api_key=API_KEY)
    st.success("✅ Gemini AI connected successfully! Ready to summarize.")
except Exception as e:
    st.error(f"❌ Failed to connect: {str(e)}")
    st.stop()

# MIME types for audio
MIME_TYPES = {
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".m4a": "audio/mp4",
    ".flac": "audio/flac",
    ".aac": "audio/aac",
    ".ogg": "audio/ogg",
    ".oga": "audio/ogg",
    ".opus": "audio/opus",
    ".wma": "audio/x-ms-wma"
}

# ============================================
# TABS
# ============================================
tab1, tab2 = st.tabs(["🎵 Upload Audio", "📝 Paste Transcript"])

# ============================================
# TAB 1: AUDIO UPLOAD
# ============================================
with tab1:
    st.markdown("""
    <div class="card">
        <h3 class="card-heading">🎵 Upload Meeting Audio</h3>
        <p class="secondary-text">Upload an audio file and let Gemini transcribe and summarize it for you.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=['mp3', 'wav', 'm4a', 'flac', 'aac', 'ogg', 'oga', 'opus', 'wma'],
        help="Supported formats: MP3, WAV, M4A, FLAC, AAC, OGG, OGA, OPUS, WMA (Max 50MB)",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        file_extension = Path(uploaded_file.name).suffix.lower()
        file_size_kb = uploaded_file.size / 1024
        
        st.markdown(f"""
        <div class="success-card">
            <h4>✅ File Uploaded Successfully</h4>
            <p><strong>📁 File:</strong> {uploaded_file.name}</p>
            <p><strong>📊 Size:</strong> {file_size_kb:.2f} KB</p>
            <p><strong>🔤 Format:</strong> {file_extension.upper()}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Audio player
        mime_type = MIME_TYPES.get(file_extension, "audio/mpeg")
        try:
            st.audio(uploaded_file, format=mime_type)
        except Exception:
            st.warning("⚠️ Audio preview not available, but processing will still work.")
        
        # Process button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            process_audio = st.button("🎯 Generate Summary", type="primary", use_container_width=True)
        
        if process_audio:
            with st.spinner("🔄 Processing audio..."):
                
                audio_path = None
                audio_file = None
                
                try:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Step 1
                    status_text.text("📁 Saving audio file...")
                    progress_bar.progress(20)
                    
                    if not file_extension:
                        raise Exception("Could not determine audio file format.")
                    
                    mime_type = MIME_TYPES.get(file_extension)
                    if not mime_type:
                        raise Exception(f"Unsupported audio format: {file_extension}")
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp:
                        tmp.write(uploaded_file.getvalue())
                        audio_path = tmp.name
                    
                    status_text.text("☁️ Uploading to Gemini AI...")
                    progress_bar.progress(40)
                    
                    audio_file = client.files.upload(
                        file=audio_path,
                        config={"mime_type": mime_type}
                    )
                    
                    status_text.text("⏳ Gemini is processing the audio...")
                    progress_bar.progress(60)
                    
                    while True:
                        file_status = client.files.get(name=audio_file.name)
                        state = file_status.state.name if file_status.state else ""
                        
                        if state == "ACTIVE":
                            break
                        elif state == "FAILED":
                            raise Exception("Gemini failed to process the audio.")
                        time.sleep(3)
                    
                    progress_bar.progress(80)
                    status_text.text("🤖 Generating meeting summary...")
                    
                    prompt = """
You are an AI meeting assistant.

Analyze the uploaded meeting audio and create a structured meeting summary.

## Meeting Overview
- Purpose of the meeting
- Overall outcome

## Key Discussion Points
- Important topics discussed

## Decisions Made
- Decisions that were actually made

## Action Items
For each action item provide:
- Task
- Responsible person (if mentioned)
- Deadline (if mentioned)

## Key Participants
- Names of participants mentioned

## Next Steps
- Follow-up activities

IMPORTANT:
- Do not invent names, deadlines, or decisions.
- If something is not mentioned, write "Not mentioned".
- If the audio is unclear, explicitly say so.
"""
                    
                    response = client.models.generate_content(
                        model="gemini-3.7-flash",
                        contents=[audio_file, prompt]
                    )
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Summary generated successfully!")
                    
                    summary = response.text
                    
                    # Display summary
                    st.markdown("---")
                    st.markdown("## 📋 Meeting Summary")
                    st.markdown(f"""
                    <div class="summary-box">
                        {summary}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Download buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.download_button(
                            label="💾 Download TXT",
                            data=summary,
                            file_name=f"meeting_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                    with col2:
                        st.download_button(
                            label="📄 Download MD",
                            data=f"# Meeting Summary\n\n{summary}",
                            file_name=f"meeting_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown"
                        )
                    
                    st.balloons()
                    st.success("🎉 Summary generated successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    
                finally:
                    if audio_path and os.path.exists(audio_path):
                        try:
                            os.unlink(audio_path)
                        except Exception:
                            pass

# ============================================
# TAB 2: TEXT TRANSCRIPT
# ============================================
with tab2:
    st.markdown("""
    <div class="card">
        <h3 class="card-heading">📝 Paste Meeting Transcript</h3>
        <p class="secondary-text">If you already have a transcript, paste it here for instant summarization.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        transcript = st.text_area(
            "📄 Meeting Transcript",
            height=250,
            placeholder="""Paste your meeting transcript here...

Example:
Meeting: Weekly Team Sync - August 23, 2026
Attendees: Sarah, Alex, Maria

Sarah: We need to focus on the user dashboard.
Alex: Backend API is complete.
Maria: Design review is done.

Decisions:
- Launch dashboard by August 30

Action Items:
- Alex: Complete frontend (Aug 27)
- Maria: Get feedback (Aug 24)""",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("### ⚙️ Options")
        summary_length = st.selectbox(
            "Summary Length",
            ["Concise", "Detailed", "Executive Brief"]
        )
        include_attendees = st.checkbox("Include attendees", value=True)
        include_timeline = st.checkbox("Include timeline", value=True)
    
    if st.button("📝 Generate Summary", type="primary") and transcript:
        with st.spinner("🤖 Generating summary..."):
            try:
                length_map = {
                    "Concise": "brief and concise (2-3 paragraphs)",
                    "Detailed": "comprehensive and detailed",
                    "Executive Brief": "executive-level summary with key takeaways"
                }
                
                prompt = f"""
                Please provide a {length_map[summary_length]} meeting summary from this transcript.
                
                Include:
                1. Meeting Overview
                2. Key Discussion Points
                3. Decisions Made
                4. Action Items (with responsibilities and deadlines)
                5. Next Steps
                """
                
                if include_attendees:
                    prompt += "\n6. Key Participants/Attendees"
                
                if include_timeline:
                    prompt += "\n7. Timeline and important dates"
                
                prompt += f"\n\nFormat with clear headings and bullet points.\n\nTranscript: {transcript}"
                
                response = client.models.generate_content(
                    model="gemini-3.7-flash",
                    contents=[prompt]
                )
                summary = response.text
                
                st.markdown("---")
                st.markdown("## 📋 Meeting Summary")
                st.markdown(f"""
                <div class="summary-box">
                    {summary}
                </div>
                """, unsafe_allow_html=True)
                
                # Download buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button(
                        label="💾 Download TXT",
                        data=summary,
                        file_name=f"meeting_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                with col2:
                    st.download_button(
                        label="📄 Download MD",
                        data=f"# Meeting Summary\n\n{summary}",
                        file_name=f"meeting_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
                
                st.balloons()
                st.success("🎉 Summary generated successfully!")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    Built with <span class="heart">❤️</span> using 
    <strong>Streamlit</strong> & 
    <strong>Google Gemini AI</strong>
    <br>
    <span style="font-size: 0.75rem; color: #94A3B8;">
        WCAG AA Compliant | © 2026 Meeting Summarizer Pro
    </span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)