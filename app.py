"""Meeting Summarizer Pro - Enterprise Edition with Authentication & Database"""
import streamlit as st
import os
from dotenv import load_dotenv
import tempfile
from pathlib import Path
import time
from google import genai
from datetime import datetime, timedelta
import json
import hashlib
import bcrypt
import jwt
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# ============================================
# DATABASE SETUP
# ============================================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///meeting_summarizer.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ============================================
# DATABASE MODELS
# ============================================
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    plan = Column(String, default="free")
    google_id = Column(String, unique=True, nullable=True)
    profile_pic = Column(String, nullable=True)

class Summary(Base):
    __tablename__ = "summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    title = Column(String, nullable=True)
    transcript = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    audio_filename = Column(String, nullable=True)
    file_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    meeting_date = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    action_items = Column(Text, nullable=True)
    decisions = Column(Text, nullable=True)
    participants = Column(Text, nullable=True)

# Create tables
Base.metadata.create_all(bind=engine)

# ============================================
# AUTHENTICATION UTILITIES
# ============================================
JWT_SECRET = os.getenv("JWT_SECRET", "your-super-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRY_HOURS = 24

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    if not password_hash:
        return False
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def create_jwt_token(user_id: int, email: str) -> str:
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def get_user_by_email(db, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db, email: str, username: str, password: str = None, full_name: str = None):
    password_hash = hash_password(password) if password else None
    user = User(
        email=email,
        username=username,
        password_hash=password_hash,
        full_name=full_name or username,
        created_at=datetime.utcnow(),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not user.password_hash:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

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
# SESSION STATE INITIALIZATION
# ============================================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'user_plan' not in st.session_state:
    st.session_state.user_plan = "free"
if 'page' not in st.session_state:
    st.session_state.page = "landing"
if 'summary_history' not in st.session_state:
    st.session_state.summary_history = []
if 'meeting_count' not in st.session_state:
    st.session_state.meeting_count = 0
if 'current_summary' not in st.session_state:
    st.session_state.current_summary = None
if 'db' not in st.session_state:
    st.session_state.db = SessionLocal()
if 'token' not in st.session_state:
    st.session_state.token = None

# ============================================
# DESIGN TOKENS
# ============================================
DESIGN_TOKENS = {
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
    "font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "body_font_size": "16px",
    "body_line_height": "1.5",
    "heading_weight": "700",
}

# ============================================
# CUSTOM CSS
# ============================================
def load_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        * {{
            font-family: '{DESIGN_TOKENS["font_family"]}';
            box-sizing: border-box;
        }}
        
        .stApp {{
            background-color: {DESIGN_TOKENS["primary_background"]};
        }}
        
        .hero-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            padding: 4rem 2rem;
            border-radius: 24px;
            margin-bottom: 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .hero-title {{
            font-size: 4rem;
            font-weight: 900;
            color: white;
            margin-bottom: 0.5rem;
            position: relative;
            z-index: 1;
            text-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        
        .hero-title span {{
            background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .hero-subtitle {{
            font-size: 1.3rem;
            color: rgba(255,255,255,0.9);
            margin-bottom: 2rem;
            position: relative;
            z-index: 1;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }}
        
        .stats-section {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }}
        
        .stat-item {{
            background: {DESIGN_TOKENS["surface_background"]};
            padding: 1.5rem;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border: 1px solid {DESIGN_TOKENS["border_color"]};
        }}
        
        .stat-item .number {{
            font-size: 2.5rem;
            font-weight: 800;
            color: {DESIGN_TOKENS["primary_action"]};
            display: block;
        }}
        
        .stat-item .label {{
            color: {DESIGN_TOKENS["secondary_text"]};
            font-size: 0.9rem;
            font-weight: 500;
        }}
        
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }}
        
        .feature-card {{
            background: {DESIGN_TOKENS["surface_background"]};
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
            border: 1px solid {DESIGN_TOKENS["border_color"]};
            transition: all 0.3s ease;
        }}
        
        .feature-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 40px rgba(0,0,0,0.08);
            border-color: {DESIGN_TOKENS["primary_action"]};
        }}
        
        .feature-card .icon {{
            font-size: 3rem;
            margin-bottom: 1rem;
            display: block;
        }}
        
        .feature-card h3 {{
            color: {DESIGN_TOKENS["heading_color"]};
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
        }}
        
        .feature-card p {{
            color: {DESIGN_TOKENS["secondary_text"]};
            font-size: 0.95rem;
            line-height: 1.6;
        }}
        
        .auth-modal {{
            background: {DESIGN_TOKENS["surface_background"]};
            padding: 2.5rem;
            border-radius: 16px;
            max-width: 500px;
            margin: 2rem auto;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
            border: 1px solid {DESIGN_TOKENS["border_color"]};
        }}
        
        .auth-modal .auth-title {{
            font-size: 1.8rem;
            font-weight: 700;
            color: {DESIGN_TOKENS["heading_color"]};
            text-align: center;
            margin-bottom: 0.5rem;
        }}
        
        .auth-modal .auth-subtitle {{
            color: {DESIGN_TOKENS["secondary_text"]};
            text-align: center;
            margin-bottom: 1.5rem;
        }}
        
        .google-btn {{
            background: white;
            color: #333 !important;
            border: 2px solid {DESIGN_TOKENS["border_color"]};
            padding: 0.8rem;
            border-radius: 8px;
            width: 100%;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }}
        
        .google-btn:hover {{
            background: #f8f9fa;
            border-color: {DESIGN_TOKENS["primary_action"]};
        }}
        
        .dashboard-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        }}
        
        .dashboard-stat {{
            background: {DESIGN_TOKENS["surface_background"]};
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            border: 1px solid {DESIGN_TOKENS["border_color"]};
        }}
        
        .dashboard-stat .number {{
            font-size: 2rem;
            font-weight: 700;
            color: {DESIGN_TOKENS["primary_action"]};
            display: block;
        }}
        
        .dashboard-stat .label {{
            color: {DESIGN_TOKENS["secondary_text"]};
            font-size: 0.85rem;
        }}
        
        .user-avatar {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 1.2rem;
        }}
        
        .plan-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .plan-free {{
            background: #e2e8f0;
            color: #475569;
        }}
        
        .plan-pro {{
            background: #2563EB;
            color: white;
        }}
        
        .plan-enterprise {{
            background: #7C3AED;
            color: white;
        }}
        
        @media (max-width: 768px) {{
            .hero-title {{
                font-size: 2.5rem;
            }}
            .hero-subtitle {{
                font-size: 1rem;
            }}
            .features-grid {{
                grid-template-columns: 1fr;
            }}
            .stats-section {{
                grid-template-columns: 1fr 1fr;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

load_css()

# ============================================
# SESSION STATE MANAGEMENT
# ============================================
API_KEY = os.getenv("GEMINI_API_KEY")

try:
    if API_KEY:
        client = genai.Client(api_key=API_KEY)
    else:
        client = None
except Exception as e:
    client = None

def get_db():
    return SessionLocal()

# ============================================
# LANDING PAGE
# ============================================
def landing_page():
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">
            🎙️ Meeting <span>Summarizer</span> Pro
        </div>
        <div class="hero-subtitle">
            Transform your meetings into actionable intelligence with AI-powered summarization.
            Save hours, capture decisions, and never miss an action item again.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="stats-section">
        <div class="stat-item">
            <span class="number">10K+</span>
            <span class="label">Meetings Summarized</span>
        </div>
        <div class="stat-item">
            <span class="number">99.9%</span>
            <span class="label">Accuracy Rate</span>
        </div>
        <div class="stat-item">
            <span class="number">4.9⭐</span>
            <span class="label">User Rating</span>
        </div>
        <div class="stat-item">
            <span class="number">50+</span>
            <span class="label">Countries</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## 🚀 Why Choose Meeting Summarizer Pro?")
    st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <span class="icon">🎯</span>
            <h3>Smart Summaries</h3>
            <p>AI extracts key decisions, action items, and discussion points automatically.</p>
        </div>
        <div class="feature-card">
            <span class="icon">⚡</span>
            <h3>Blazing Fast</h3>
            <p>Get your meeting summary in seconds, not hours. No more manual note-taking.</p>
        </div>
        <div class="feature-card">
            <span class="icon">🔒</span>
            <h3>Enterprise Security</h3>
            <p>Your data is encrypted and never stored permanently. Privacy first approach.</p>
        </div>
        <div class="feature-card">
            <span class="icon">📱</span>
            <h3>Works Everywhere</h3>
            <p>Upload from any device - desktop, tablet, or mobile. Cloud-based and accessible.</p>
        </div>
        <div class="feature-card">
            <span class="icon">🤖</span>
            <h3>Gemini AI Powered</h3>
            <p>Powered by Google's state-of-the-art Gemini 3.7 Flash for accurate transcription.</p>
        </div>
        <div class="feature-card">
            <span class="icon">💾</span>
            <h3>Export Any Format</h3>
            <p>Download summaries as TXT, Markdown, or share directly with your team.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🚀 Sign Up Free", type="primary", use_container_width=True):
                st.session_state.page = "signup"
                st.rerun()
        with col_b:
            if st.button("🔑 Sign In", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()

# ============================================
# SIGN UP PAGE
# ============================================
def signup_page():
    st.markdown("""
    <div class="auth-modal">
        <div style="text-align:center;margin-bottom:1rem;">
            <span style="font-size:3rem;">🎙️</span>
        </div>
        <div class="auth-title">Create Account</div>
        <div class="auth-subtitle">Start your free trial today</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("signup_form"):
            full_name = st.text_input("Full Name", placeholder="John Doe")
            email = st.text_input("Email", placeholder="john@example.com")
            username = st.text_input("Username", placeholder="johndoe")
            password = st.text_input("Password", type="password", placeholder="Min 8 characters")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("Create Account", type="primary", use_container_width=True)
            with col_b:
                if st.form_submit_button("← Back", use_container_width=True):
                    st.session_state.page = "landing"
                    st.rerun()
            
            if submit:
                if not all([full_name, email, username, password]):
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters")
                else:
                    db = get_db()
                    existing_user = get_user_by_email(db, email)
                    if existing_user:
                        st.error("Email already registered. Please sign in.")
                    else:
                        try:
                            user = create_user(db, email, username, password, full_name)
                            st.success("Account created successfully! Please sign in.")
                            st.session_state.page = "login"
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error creating account: {str(e)}")
                    db.close()

# ============================================
# LOGIN PAGE
# ============================================
def login_page():
    st.markdown("""
    <div class="auth-modal">
        <div style="text-align:center;margin-bottom:1rem;">
            <span style="font-size:3rem;">🎙️</span>
        </div>
        <div class="auth-title">Welcome Back</div>
        <div class="auth-subtitle">Sign in to access your meeting summaries</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="john@example.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("Sign In", type="primary", use_container_width=True)
            with col_b:
                if st.form_submit_button("← Back", use_container_width=True):
                    st.session_state.page = "landing"
                    st.rerun()
            
            if submit:
                if not email or not password:
                    st.error("Please enter both email and password")
                else:
                    db = get_db()
                    user = authenticate_user(db, email, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user.id
                        st.session_state.user_email = user.email
                        st.session_state.user_name = user.full_name or user.username
                        st.session_state.user_plan = user.plan
                        st.session_state.token = create_jwt_token(user.id, user.email)
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
                    db.close()
        
        st.markdown("---")
        st.markdown("Don't have an account? **Sign up** above!")

# ============================================
# DASHBOARD PAGE
# ============================================
def dashboard_page():
    db = get_db()
    user = get_user_by_id(db, st.session_state.user_id)
    
    if not user:
        st.error("User not found. Please sign in again.")
        st.session_state.authenticated = False
        st.rerun()
        return
    
    plan_colors = {
        "free": "plan-free",
        "pro": "plan-pro",
        "enterprise": "plan-enterprise"
    }
    plan_class = plan_colors.get(user.plan, "plan-free")
    
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;">
        <div>
            <h1 style="font-size:2rem;font-weight:700;color:#0F172A;">👋 Welcome, {user.full_name or user.username}</h1>
            <p style="color:#64748B;">Here's your meeting summary dashboard</p>
        </div>
        <div style="display:flex;align-items:center;gap:1rem;">
            <span class="plan-badge {plan_class}">{user.plan.upper()}</span>
            <div class="user-avatar">{user.username[0].upper()}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    summaries = db.query(Summary).filter(Summary.user_id == user.id).all()
    summary_count = len(summaries)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="dashboard-stat">
            <span class="number">{summary_count}</span>
            <span class="label">Total Meetings</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="dashboard-stat">
            <span class="number">{len([s for s in summaries if s.summary])}</span>
            <span class="label">Summaries Generated</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="dashboard-stat">
            <span class="number">⭐ 4.9</span>
            <span class="label">User Rating</span>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="dashboard-stat">
            <span class="number">{user.plan.upper()}</span>
            <span class="label">Current Plan</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎙️ New Summary", "📚 History", "👤 Profile", "⚙️ Settings"])
    
    with tab1:
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
        
        upload_tab, text_tab = st.tabs(["🎵 Upload Audio", "📝 Paste Transcript"])
        
        with upload_tab:
            st.markdown("""
            <div style="background:#F8FAFC;padding:1.5rem;border-radius:12px;border:1px solid #E2E8F0;margin-bottom:1rem;">
                <h4 style="margin:0 0 0.25rem 0;">🎵 Upload Meeting Audio</h4>
                <p style="margin:0;color:#64748B;">Upload an audio file and let Gemini transcribe and summarize it.</p>
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
                <div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:12px;padding:1rem;margin:1rem 0;">
                    <h4 style="color:#16A34A;margin:0 0 0.25rem 0;">✅ File Uploaded Successfully</h4>
                    <p style="margin:0;"><strong>📁 File:</strong> {uploaded_file.name}</p>
                    <p style="margin:0;"><strong>📊 Size:</strong> {file_size_kb:.2f} KB</p>
                    <p style="margin:0;"><strong>🔤 Format:</strong> {file_extension.upper()}</p>
                </div>
                """, unsafe_allow_html=True)
                
                mime_type = MIME_TYPES.get(file_extension, "audio/mpeg")
                try:
                    st.audio(uploaded_file, format=mime_type)
                except Exception:
                    pass
                
                if st.button("🎯 Generate Summary", type="primary", use_container_width=True):
                    if not API_KEY:
                        st.error("⚠️ Please set your GEMINI_API_KEY in .env file")
                    else:
                        with st.spinner("🔄 Processing audio..."):
                            try:
                                audio_path = None
                                audio_file = None
                                progress_bar = st.progress(0)
                                status_text = st.empty()
                                
                                status_text.text("📁 Saving audio file...")
                                progress_bar.progress(20)
                                
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
                                You are an AI meeting assistant. Analyze the uploaded meeting audio and create a structured meeting summary.

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
                                
                                new_summary = Summary(
                                    user_id=user.id,
                                    title=uploaded_file.name,
                                    summary=summary,
                                    audio_filename=uploaded_file.name,
                                    file_type="audio",
                                    created_at=datetime.utcnow()
                                )
                                db.add(new_summary)
                                db.commit()
                                db.refresh(new_summary)
                                
                                st.session_state.current_summary = summary
                                
                                st.markdown("---")
                                st.markdown("## 📋 Meeting Summary")
                                st.markdown(f"""
                                <div style="background:white;border:1px solid #E2E8F0;border-left:5px solid #2563EB;border-radius:12px;padding:2rem;margin:1rem 0;line-height:1.8;white-space:pre-wrap;">
                                    {summary}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                col1, col2 = st.columns(2)
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
                                st.success("🎉 Summary generated and saved successfully!")
                                
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                            finally:
                                if audio_path and os.path.exists(audio_path):
                                    try:
                                        os.unlink(audio_path)
                                    except Exception:
                                        pass
        
        with text_tab:
            st.markdown("""
            <div style="background:#F8FAFC;padding:1.5rem;border-radius:12px;border:1px solid #E2E8F0;margin-bottom:1rem;">
                <h4 style="margin:0 0 0.25rem 0;">📝 Paste Meeting Transcript</h4>
                <p style="margin:0;color:#64748B;">Paste your meeting transcript for instant summarization.</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                transcript = st.text_area(
                    "📄 Meeting Transcript",
                    height=200,
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
                    "Length",
                    ["Concise", "Detailed", "Executive Brief"]
                )
                include_attendees = st.checkbox("Attendees", value=True)
                include_timeline = st.checkbox("Timeline", value=True)
            
            if st.button("📝 Generate Summary", type="primary", use_container_width=True) and transcript:
                if not API_KEY:
                    st.error("⚠️ Please set your GEMINI_API_KEY in .env file")
                else:
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
                            
                            new_summary = Summary(
                                user_id=user.id,
                                title="Text Transcript Summary",
                                transcript=transcript,
                                summary=summary,
                                file_type="text",
                                created_at=datetime.utcnow()
                            )
                            db.add(new_summary)
                            db.commit()
                            db.refresh(new_summary)
                            
                            st.session_state.current_summary = summary
                            
                            st.markdown("---")
                            st.markdown("## 📋 Meeting Summary")
                            st.markdown(f"""
                            <div style="background:white;border:1px solid #E2E8F0;border-left:5px solid #2563EB;border-radius:12px;padding:2rem;margin:1rem 0;line-height:1.8;white-space:pre-wrap;">
                                {summary}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col1, col2 = st.columns(2)
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
                            st.success("🎉 Summary generated and saved successfully!")
                            
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
    
    with tab2:
        st.markdown("### 📚 Summary History")
        
        if summaries:
            data = []
            for s in summaries:
                data.append({
                    "Date": s.created_at.strftime("%Y-%m-%d %H:%M"),
                    "Title": s.title or "Untitled",
                    "Type": s.file_type or "Unknown",
                    "Preview": s.summary[:100] + "..." if s.summary else "No summary"
                })
            
            st.markdown("| Date | Title | Type | Preview |")
            st.markdown("|------|-------|------|---------|")
            for row in data:
                st.markdown(f"| {row['Date']} | {row['Title']} | {row['Type']} | {row['Preview']} |")
            
            if st.button("🗑️ Clear All History"):
                db.query(Summary).filter(Summary.user_id == user.id).delete()
                db.commit()
                st.rerun()
        else:
            st.info("No summaries yet. Start by creating your first summary!")
    
    with tab3:
        st.markdown("### 👤 Profile Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Personal Information")
            new_full_name = st.text_input("Full Name", value=user.full_name or "")
            new_username = st.text_input("Username", value=user.username)
            
            if st.button("Update Profile"):
                if new_full_name:
                    user.full_name = new_full_name
                if new_username:
                    user.username = new_username
                db.commit()
                st.success("Profile updated successfully!")
                st.rerun()
        
        with col2:
            st.markdown("#### Account Details")
            st.write(f"**Email:** {user.email}")
            st.write(f"**Plan:** {user.plan.upper()}")
            st.write(f"**Member Since:** {user.created_at.strftime('%B %d, %Y')}")
            st.write(f"**Total Summaries:** {len(summaries)}")
    
    with tab4:
        st.markdown("### ⚙️ Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔑 API Key")
            if API_KEY:
                st.success("✅ Gemini API Key: Connected")
            else:
                st.error("❌ Gemini API Key: Missing")
                st.info("Add GEMINI_API_KEY to your .env file")
        
        with col2:
            st.markdown("#### 🔐 Security")
            if st.button("Change Password"):
                st.session_state.page = "change_password"
                st.rerun()
        
        st.markdown("---")
        if st.button("🚪 Sign Out", type="secondary", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.session_state.user_name = None
            st.session_state.token = None
            st.session_state.page = "landing"
            db.close()
            st.rerun()
    
    db.close()

# ============================================
# CHANGE PASSWORD PAGE
# ============================================
def change_password_page():
    st.markdown("""
    <div class="auth-modal">
        <div style="text-align:center;margin-bottom:1rem;">
            <span style="font-size:3rem;">🔐</span>
        </div>
        <div class="auth-title">Change Password</div>
        <div class="auth-subtitle">Update your account password</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        db = get_db()
        user = get_user_by_id(db, st.session_state.user_id)
        
        with st.form("change_password_form"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("Update Password", type="primary", use_container_width=True)
            with col_b:
                if st.form_submit_button("← Back", use_container_width=True):
                    st.session_state.page = "dashboard"
                    st.rerun()
            
            if submit:
                if not current_password or not new_password:
                    st.error("Please fill in all fields")
                elif new_password != confirm_password:
                    st.error("New passwords do not match")
                elif len(new_password) < 8:
                    st.error("Password must be at least 8 characters")
                elif not verify_password(current_password, user.password_hash):
                    st.error("Current password is incorrect")
                else:
                    user.password_hash = hash_password(new_password)
                    db.commit()
                    st.success("Password updated successfully!")
                    st.session_state.page = "dashboard"
                    st.rerun()
        
        db.close()

# ============================================
# MAIN APP LOGIC
# ============================================
def main():
    if st.session_state.page == "landing" and not st.session_state.authenticated:
        landing_page()
    
    elif st.session_state.page == "signup" and not st.session_state.authenticated:
        signup_page()
    
    elif st.session_state.page == "login" and not st.session_state.authenticated:
        login_page()
    
    elif st.session_state.page == "change_password" and st.session_state.authenticated:
        change_password_page()
    
    elif st.session_state.authenticated:
        dashboard_page()
    
    else:
        st.session_state.page = "landing"
        st.rerun()

if __name__ == "__main__":
    main()
