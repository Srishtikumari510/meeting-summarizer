"""Meeting Summarizer Pro - Enterprise Edition with Authentication & Landing Page"""
import streamlit as st
import os
from dotenv import load_dotenv
import tempfile
from pathlib import Path
import time
from google import genai
from datetime import datetime
import json
import hashlib
import base64
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
import pandas as pd

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
# SESSION STATE INITIALIZATION
# ============================================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'page' not in st.session_state:
    st.session_state.page = "landing"
if 'summary_history' not in st.session_state:
    st.session_state.summary_history = []
if 'meeting_count' not in st.session_state:
    st.session_state.meeting_count = 0
if 'current_summary' not in st.session_state:
    st.session_state.current_summary = None

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
# CUSTOM CSS - COMPLETE LANDING PAGE STYLES
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
        
        /* ==========================================
           LANDING PAGE - HERO SECTION
           ========================================== */
        .hero-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            padding: 4rem 2rem;
            border-radius: 24px;
            margin-bottom: 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .hero-section::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at 30% 50%, rgba(255,255,255,0.1) 0%, transparent 50%);
            animation: shimmer 8s ease-in-out infinite;
        }}
        
        @keyframes shimmer {{
            0%, 100% {{ transform: translate(0, 0); }}
            50% {{ transform: translate(10%, 10%); }}
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
        
        .hero-buttons {{
            display: flex;
            gap: 1rem;
            justify-content: center;
            position: relative;
            z-index: 1;
            flex-wrap: wrap;
        }}
        
        .hero-buttons .primary-btn {{
            background: white;
            color: #667eea !important;
            padding: 0.8rem 2.5rem;
            border-radius: 50px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            text-decoration: none;
            display: inline-block;
        }}
        
        .hero-buttons .primary-btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.2);
        }}
        
        .hero-buttons .secondary-btn {{
            background: rgba(255,255,255,0.2);
            color: white !important;
            padding: 0.8rem 2.5rem;
            border-radius: 50px;
            font-weight: 600;
            border: 2px solid rgba(255,255,255,0.3);
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }}
        
        .hero-buttons .secondary-btn:hover {{
            background: rgba(255,255,255,0.3);
            transform: translateY(-3px);
        }}
        
        /* Stats Section */
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
        
        /* Feature Cards */
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
        
        /* Testimonial Section */
        .testimonial-section {{
            background: {DESIGN_TOKENS["surface_background"]};
            padding: 3rem 2rem;
            border-radius: 16px;
            margin: 2rem 0;
            border: 1px solid {DESIGN_TOKENS["border_color"]};
        }}
        
        .testimonial-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }}
        
        .testimonial-card {{
            padding: 1.5rem;
            border-radius: 12px;
            background: {DESIGN_TOKENS["primary_background"]};
            border-left: 4px solid {DESIGN_TOKENS["primary_action"]};
        }}
        
        .testimonial-card .quote {{
            font-style: italic;
            color: {DESIGN_TOKENS["primary_text"]};
            margin-bottom: 0.5rem;
        }}
        
        .testimonial-card .author {{
            font-weight: 600;
            color: {DESIGN_TOKENS["heading_color"]};
        }}
        
        .testimonial-card .role {{
            color: {DESIGN_TOKENS["secondary_text"]};
            font-size: 0.85rem;
        }}
        
        /* Pricing Section */
        .pricing-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }}
        
        .pricing-card {{
            background: {DESIGN_TOKENS["surface_background"]};
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
            border: 2px solid {DESIGN_TOKENS["border_color"]};
            transition: all 0.3s ease;
        }}
        
        .pricing-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        }}
        
        .pricing-card.featured {{
            border-color: {DESIGN_TOKENS["primary_action"]};
            background: linear-gradient(135deg, #f8faff, #eef2ff);
        }}
        
        .pricing-card .price {{
            font-size: 2.5rem;
            font-weight: 800;
            color: {DESIGN_TOKENS["heading_color"]};
        }}
        
        .pricing-card .price span {{
            font-size: 1rem;
            font-weight: 400;
            color: {DESIGN_TOKENS["secondary_text"]};
        }}
        
        .pricing-card .plan-name {{
            font-size: 1.2rem;
            font-weight: 600;
            color: {DESIGN_TOKENS["heading_color"]};
            margin-bottom: 0.5rem;
        }}
        
        .pricing-card ul {{
            list-style: none;
            padding: 0;
            text-align: left;
            margin: 1rem 0;
        }}
        
        .pricing-card ul li {{
            padding: 0.5rem 0;
            color: {DESIGN_TOKENS["primary_text"]};
            border-bottom: 1px solid {DESIGN_TOKENS["border_color"]};
        }}
        
        .pricing-card ul li::before {{
            content: '✅ ';
        }}
        
        /* Auth Modal */
        .auth-modal {{
            background: {DESIGN_TOKENS["surface_background"]};
            padding: 2.5rem;
            border-radius: 16px;
            max-width: 400px;
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
        
        .auth-modal .google-btn {{
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
        
        .auth-modal .google-btn:hover {{
            background: #f8f9fa;
            border-color: {DESIGN_TOKENS["primary_action"]};
        }}
        
        .auth-modal .divider {{
            text-align: center;
            margin: 1rem 0;
            color: {DESIGN_TOKENS["secondary_text"]};
            position: relative;
        }}
        
        .auth-modal .divider::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 1px;
            background: {DESIGN_TOKENS["border_color"]};
        }}
        
        .auth-modal .divider span {{
            background: white;
            padding: 0 1rem;
            position: relative;
            z-index: 1;
        }}
        
        /* Dashboard */
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
        
        /* Responsive */
        @media (max-width: 768px) {{
            .hero-title {{
                font-size: 2.5rem;
            }}
            .hero-subtitle {{
                font-size: 1rem;
            }}
            .hero-buttons {{
                flex-direction: column;
                align-items: center;
            }}
            .features-grid {{
                grid-template-columns: 1fr;
            }}
            .pricing-grid {{
                grid-template-columns: 1fr;
            }}
            .stats-section {{
                grid-template-columns: 1fr 1fr;
            }}
        }}
        
        /* User Avatar */
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
    </style>
    """, unsafe_allow_html=True)

load_css()

# ============================================
# SESSION STATE MANAGEMENT
# ============================================
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
try:
    if API_KEY:
        client = genai.Client(api_key=API_KEY)
except Exception as e:
    client = None

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
        <div class="hero-buttons">
            <button class="primary-btn" onclick="document.querySelector('[data-testid=baseButton-secondary]').click()">
                🚀 Get Started Free
            </button>
            <button class="secondary-btn" onclick="document.querySelector('[data-testid=baseButton-secondary]').click()">
                🎥 Watch Demo
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Section
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
    
    # Features Section
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
    
    # Testimonials
    st.markdown("## 💬 What Our Users Say")
    st.markdown("""
    <div class="testimonial-section">
        <div class="testimonial-grid">
            <div class="testimonial-card">
                <div class="quote">"This tool saved our team 10+ hours per week. We never miss action items anymore!"</div>
                <div class="author">Sarah Johnson</div>
                <div class="role">Product Manager, TechCorp</div>
            </div>
            <div class="testimonial-card">
                <div class="quote">"The accuracy is incredible. Even with background noise, the summaries are perfect."</div>
                <div class="author">Michael Chen</div>
                <div class="role">CTO, StartupHub</div>
            </div>
            <div class="testimonial-card">
                <div class="quote">"I use it for all my client meetings. It's like having a personal assistant!"</div>
                <div class="author">Emily Rodriguez</div>
                <div class="role">Consultant, Global Partners</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Pricing Section
    st.markdown("## 💎 Simple Pricing")
    st.markdown("""
    <div class="pricing-grid">
        <div class="pricing-card">
            <div class="plan-name">Free</div>
            <div class="price">$0 <span>/month</span></div>
            <ul>
                <li>5 meetings per month</li>
                <li>Audio upload up to 10MB</li>
                <li>Text transcript summarization</li>
                <li>Basic export options</li>
            </ul>
            <button class="primary-btn" style="width:100%;">Get Started</button>
        </div>
        <div class="pricing-card featured">
            <div class="plan-name">Pro</div>
            <div class="price">$29 <span>/month</span></div>
            <ul>
                <li>Unlimited meetings</li>
                <li>Audio upload up to 100MB</li>
                <li>Advanced summarization</li>
                <li>Export all formats</li>
                <li>Priority support</li>
            </ul>
            <button class="primary-btn" style="width:100%;background:#2563EB;">Try Pro Free</button>
        </div>
        <div class="pricing-card">
            <div class="plan-name">Enterprise</div>
            <div class="price">Custom</div>
            <ul>
                <li>All Pro features</li>
                <li>Team collaboration</li>
                <li>Custom integrations</li>
                <li>Dedicated support</li>
                <li>SLA guarantee</li>
            </ul>
            <button class="primary-btn" style="width:100%;">Contact Sales</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("""
    <div style="text-align:center;background:linear-gradient(135deg,#667eea,#764ba2);padding:3rem 2rem;border-radius:16px;margin:2rem 0;">
        <h2 style="color:white;font-size:2rem;margin-bottom:0.5rem;">Ready to Transform Your Meetings?</h2>
        <p style="color:rgba(255,255,255,0.9);font-size:1.1rem;margin-bottom:1.5rem;">
            Join thousands of professionals who use Meeting Summarizer Pro daily.
        </p>
        <button class="primary-btn" onclick="document.querySelector('[data-testid=baseButton-secondary]').click()" 
                style="background:white;color:#667eea !important;font-size:1.1rem;padding:0.8rem 3rem;">
            🚀 Get Started Free
        </button>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# AUTHENTICATION
# ============================================
def auth_page():
    st.markdown("""
    <div class="auth-modal">
        <div style="text-align:center;margin-bottom:1rem;">
            <span style="font-size:3rem;">🎙️</span>
        </div>
        <div class="auth-title">Welcome Back</div>
        <div class="auth-subtitle">Sign in to access your meeting summaries</div>
        
        <button class="google-btn">
            <svg width="20" height="20" viewBox="0 0 48 48">
                <path fill="#FFC107" d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20c11.045,0,20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z"/>
                <path fill="#FF3D00" d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z"/>
                <path fill="#4CAF50" d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z"/>
                <path fill="#1976D2" d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z"/>
            </svg>
            Sign in with Google
        </button>
        
        <div class="divider"><span>or continue with email</span></div>
        
        <div style="margin-top:1rem;">
            <input type="email" placeholder="Email address" 
                   style="width:100%;padding:0.8rem;border:2px solid #E2E8F0;border-radius:8px;margin-bottom:0.5rem;font-size:1rem;">
            <input type="password" placeholder="Password" 
                   style="width:100%;padding:0.8rem;border:2px solid #E2E8F0;border-radius:8px;margin-bottom:1rem;font-size:1rem;">
            <button style="width:100%;padding:0.8rem;background:#2563EB;color:white;border:none;border-radius:8px;font-weight:600;font-size:1rem;cursor:pointer;">
                Sign In
            </button>
        </div>
        
        <div style="text-align:center;margin-top:1rem;color:#64748B;font-size:0.9rem;">
            Don't have an account? <a href="#" style="color:#2563EB;text-decoration:none;font-weight:600;">Sign up free</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple email/password auth for demo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("---")
        st.markdown("### 🔑 Demo Login")
        email = st.text_input("Email", placeholder="demo@example.com")
        password = st.text_input("Password", type="password", placeholder="password")
        
        if st.button("Sign In", type="primary", use_container_width=True):
            if email and password:
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.session_state.user_name = email.split('@')[0].title()
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Please enter email and password")
        
        st.caption("💡 Demo: Use any email and password to try the app")

# ============================================
# DASHBOARD PAGE
# ============================================
def dashboard_page():
    # User greeting
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;">
        <div>
            <h1 style="font-size:2rem;font-weight:700;color:#0F172A;">👋 Welcome, {st.session_state.user_name}</h1>
            <p style="color:#64748B;">Here's your meeting summary dashboard</p>
        </div>
        <div class="user-avatar">{st.session_state.user_name[0].upper()}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="dashboard-stat">
            <span class="number">{st.session_state.meeting_count}</span>
            <span class="label">Total Meetings</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="dashboard-stat">
            <span class="number">{len(st.session_state.summary_history)}</span>
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
        st.markdown("""
        <div class="dashboard-stat">
            <span class="number">🎯</span>
            <span class="label">Pro Plan</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main App Tabs
    tab1, tab2, tab3 = st.tabs(["🎙️ New Summary", "📚 History", "⚙️ Settings"])
    
    with tab1:
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
                                st.session_state.current_summary = summary
                                st.session_state.meeting_count += 1
                                st.session_state.summary_history.append({
                                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "name": uploaded_file.name,
                                    "type": "Audio",
                                    "summary": summary[:200] + "..."
                                })
                                
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
                                st.success("🎉 Summary generated successfully!")
                                
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
                            
                            st.session_state.current_summary = summary
                            st.session_state.meeting_count += 1
                            st.session_state.summary_history.append({
                                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "name": "Transcript",
                                "type": "Text",
                                "summary": summary[:200] + "..."
                            })
                            
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
                            st.success("🎉 Summary generated successfully!")
                            
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
    
    with tab2:
        st.markdown("### 📚 Summary History")
        
        if st.session_state.summary_history:
            history_df = pd.DataFrame(st.session_state.summary_history)
            st.dataframe(
                history_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "date": "Date",
                    "name": "File Name",
                    "type": "Type",
                    "summary": "Preview"
                }
            )
            
            if st.button("🗑️ Clear History"):
                st.session_state.summary_history = []
                st.rerun()
        else:
            st.info("No summaries generated yet. Start by creating your first summary!")
    
    with tab3:
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
            st.markdown("#### 👤 Profile")
            st.write(f"**Name:** {st.session_state.user_name}")
            st.write(f"**Email:** {st.session_state.user_email}")
            st.write(f"**Plan:** Pro")
        
        st.markdown("---")
        st.markdown("#### 🎨 Theme Preferences")
        theme = st.selectbox("Theme", ["Light", "Dark"], index=0)
        st.caption("💡 Dark theme coming soon!")
        
        st.markdown("---")
        if st.button("🚪 Sign Out", type="secondary"):
            st.session_state.authenticated = False
            st.session_state.user_email = None
            st.session_state.user_name = None
            st.session_state.page = "landing"
            st.rerun()

# ============================================
# MAIN APP LOGIC
# ============================================
def main():
    # Check authentication
    if st.session_state.page == "landing" and not st.session_state.authenticated:
        landing_page()
        
        # Hidden auth trigger
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Get Started", type="primary", use_container_width=True):
                st.session_state.page = "auth"
                st.rerun()
    
    elif st.session_state.page == "auth" and not st.session_state.authenticated:
        auth_page()
    
    elif st.session_state.authenticated:
        dashboard_page()
    
    else:
        st.session_state.page = "landing"
        st.rerun()

if __name__ == "__main__":
    main()
