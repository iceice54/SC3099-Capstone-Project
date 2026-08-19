"""
SAIV Instructor Dashboard - Module 4

This is the skeleton implementation for the Observability module.
Students must implement the instructor dashboard with session management,
attendance monitoring, and metrics visualization.
"""

import os

import streamlit as st


# Page configuration
st.set_page_config(
    page_title="SAIV Instructor Dashboard",
    page_icon="📊",
    layout="wide",
)

# Environment variables
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")

# Temporary login state until the backend authentication API is ready
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# Temporary instructor login
if not st.session_state.logged_in:
    st.title("SAIV Instructor Login")
    st.write("Sign in using your instructor credentials.")

    with st.form("login_form"):
        email = st.text_input(
            "Email",
            placeholder="instructor@ntu.edu.sg",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
        )

        login_submitted = st.form_submit_button(
            "Login",
            use_container_width=True,
        )

    if login_submitted:
        valid_email = email.strip().lower() == "instructor@ntu.edu.sg"
        valid_password = password == "SAIV-Instructor-Demo-2026!"

        if valid_email and valid_password:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid email or password.")

    st.stop()


# Sidebar
with st.sidebar:
    st.write("Signed in as")
    st.caption("instructor@ntu.edu.sg")

    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()


# Dashboard home page
st.title("SAIV Instructor Dashboard")
st.write("Welcome to the Secure Attendance & Identity Verification System")

# =============================================================================
# TODO: Implement the following pages/features
# =============================================================================

# -----------------------------------------------------------------------------
# Authentication
# -----------------------------------------------------------------------------
# - Replace temporary credentials with the backend login API
# - JWT token management
# - Session persistence
# - Instructor role verification

# -----------------------------------------------------------------------------
# Overview Page
# -----------------------------------------------------------------------------
# - Total sessions (active/inactive)
# - Total check-ins and success rate
# - Recent check-ins table
# - Check-ins by hour chart
# - Verification status pie chart

# -----------------------------------------------------------------------------
# Sessions Management
# -----------------------------------------------------------------------------
# - View all sessions with details
# - Create new sessions with geofence configuration
# - View check-ins per session
# - CSV export for gradebook

# -----------------------------------------------------------------------------
# Check-ins View
# -----------------------------------------------------------------------------
# - Filter by session and verification status
# - Real-time updates
# - CSV export for gradebook integration
# - Attendance data with all signals

# -----------------------------------------------------------------------------
# Audit Logs
# -----------------------------------------------------------------------------
# - Browse system events
# - Filter by event type, user and action
# - Colour-code events by severity
# - Export audit trail

# -----------------------------------------------------------------------------
# Metrics Dashboard
# -----------------------------------------------------------------------------
# - API response times (p95 latency)
# - Request rates
# - Success rates
# - Risk score distribution
# - High-risk alerts
# - System health status

# =============================================================================
# CSV Export Format
# =============================================================================
# Required columns:
# - Check-in ID
# - Student ID
# - Session ID
# - Timestamp
# - Verification Status
# - Risk Score
# - Liveness Score
# - Face Match Score
# - GPS Coordinates (latitude and longitude)

st.info("Dashboard content will be added after the backend APIs are available.")

