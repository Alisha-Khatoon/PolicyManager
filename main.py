import streamlit as st
from components.dashboard import render_dashboard
from components.policy_viewer import render_policy_viewer
from components.search import render_search
from components.auth import render_auth
from components.policy_updates import render_policy_updates
from utils.document_manager import DocumentManager
from utils.ai_analyzer import AIAnalyzer
from utils.version_control import VersionControl
from models.database import db, User, Enterprise

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'

# Initialize components
doc_manager = DocumentManager()
ai_analyzer = AIAnalyzer()
version_control = VersionControl()

# Page configuration
st.set_page_config(
    page_title="Enterprise Policy Manager",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
with open('static/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Authentication check
if not st.session_state.user:
    render_auth()
else:
    # Sidebar navigation
    st.sidebar.title(f"Welcome, {st.session_state.user.username}")

    try:
        # Get user's enterprise
        enterprise = None
        if st.session_state.user.enterprise_id:
            enterprise = db.query(Enterprise).filter_by(id=st.session_state.user.enterprise_id).first()
            if enterprise:
                st.sidebar.text(f"Enterprise: {enterprise.name}")
            db.commit()
    except Exception as e:
        db.rollback()
        st.error("Error loading enterprise data")

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    navigation = st.sidebar.radio(
        "Navigate to:",
        ["Dashboard", "Policy Viewer", "Search", "Policy Updates"],
        key="navigation"
    )

    # Main content
    if navigation == "Dashboard":
        render_dashboard(doc_manager, ai_analyzer)
    elif navigation == "Policy Viewer":
        render_policy_viewer(doc_manager, version_control)
    elif navigation == "Policy Updates":
        render_policy_updates(doc_manager, ai_analyzer, enterprise)
    else:
        render_search(doc_manager)