import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="MPLADS AI Monitor | Government Portal", layout="wide")

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = "MoSPI"

# ---------------------------------------------------------
# LOGIN PAGE
# ---------------------------------------------------------
if not st.session_state.logged_in:
    st.markdown("""
        <style>
        .login-container {
            max-width: 420px;
            margin: 60px auto;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        .login-header {
            text-align: center;
            color: #0f172a;
            font-weight: 700;
            margin-bottom: 5px;
        }
        .login-subheader {
            text-align: center;
            color: #64748b;
            font-size: 13px;
            margin-bottom: 25px;
        }
        .secure-badge {
            text-align: center;
            color: #16a34a;
            font-size: 12px;
            font-weight: 600;
            margin-top: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h2 class="login-header">🏛️ MPLADS AI Monitor</h2>', unsafe_allow_html=True)
        st.markdown('<p class="login-subheader">Ministry of Statistics and Programme Implementation (MoSPI)</p>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            user_id = st.text_input("Email / User ID", placeholder="officer.mospi@gov.in")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            
            c1, c2 = st.columns(2)
            with c1:
                remember = st.checkbox("Remember me")
            with c2:
                st.markdown("<p style='text-align: right; font-size: 12px; margin-top: 4px;'><a href='#' target='_self'>Forgot password?</a></p>", unsafe_allow_html=True)
            
            # Demo Role Selector for Hackathon Presentation
            st.markdown("---")
            selected_role = st.selectbox("Demo Role Selector (Prototype)", ["MoSPI", "State Nodal Authority", "District Authority", "MP"])
            
            submit = st.form_submit_button("Sign In Securely", use_container_width=True)
            
            if submit:
                st.session_state.logged_in = True
                st.session_state.user_role = selected_role
                st.rerun()

        st.markdown('<p class="secure-badge">🔒 256-Bit SSL Encrypted Government Gateway</p>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-size: 11px; color: #94a3b8; margin-top: 20px;">Authorized Access Only • National Informatics Centre (NIC)</p>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MAIN DASHBOARD (Only visible after login)
# ---------------------------------------------------------
else:
    st.markdown(f"""
        <style>
        .stApp {{ background-color: #f8fafc; }}
        .filter-card {{
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 24px;
        }
        .filter-label {{ font-weight: 600; color: #1e293b; font-size: 14px; margin-bottom: 8px; }}
        </style>
    """, unsafe_allow_html=True)

    # Top Navigation / Profile Bar
    nav_col1, nav_col2 = st.columns([4, 1])
    with nav_col1:
        st.markdown(f"## MPLADS AI Monitor | {st.session_state.user_role} Portal")
        st.caption("Active Scope: National Oversight & Automated Risk Triage")
    with nav_col2:
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()

    @st.cache_data
    def load_data():
        np.random.seed(42)
        data = {
            'Project_ID': [f"MPLAD-{1000+i}" for i in range(50)],
            'Title': [f"Development Work at Ward {i} in Salem/Coimbatore" for i in range(50)],
            'Location': np.random.choice(["Salem", "Coimbatore", "Rohania", "Chennai", "Madurai"], 50),
            'Sector': np.random.choice(["Roads & Pathways", "Drinking Water", "Community Facilities", "Education & Schools", "Healthcare"], 50),
            'Status': np.random.choice(["Ongoing", "Completed", "Delayed", "Pending"], 50, p=[0.5, 0.2, 0.2, 0.1]),
            'Risk_Level': np.random.choice(["Low", "Medium", "High", "Critical"], 50, p=[0.4, 0.3, 0.2, 0.1]),
            'Risk_Score': np.random.randint(45, 99, 50),
            'Cost_Deviation': np.random.choice([12.5, 24.0, 45.5, 85.2, 120.4, 210.3, 315.4], 50),
            'Sanctioned': np.random.randint(5, 50, 50) * 100000,
            'Revised': np.random.randint(6, 60, 50) * 100000,
            'Actual': np.random.randint(4, 55, 50) * 100000,
            'Progress': np.random.randint(20, 95, 50)
        }
        return pd.DataFrame(data)

    df = load_data()

    total_active = len(df[df['Status'] == 'Ongoing'])
    total_outlay = f"₹{df['Sanctioned'].sum() / 10000000:.2f} Cr"
    critical_count = len(df[df['Risk_Level'] == 'Critical'])
    delayed_count = len(df[df['Status'] == 'Delayed'])

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TOTAL ACTIVE PROJECTS", total_active)
    m2.metric("SANCTIONED OUTLAY", total_outlay)
    m3.metric("CRITICAL RISK WORKS", critical_count)
    m4.metric("STAGNANT / DELAYED", delayed_count)

    st.markdown("---")

    # Filter Component
    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns(4)

    with f1:
        st.markdown('<p class="filter-label">Project Status</p>', unsafe_allow_html=True)
        status_opts = ["All Statuses (Ongoing & Completed)"] + sorted(df['Status'].unique().tolist())
        selected_status = st.selectbox("Status", status_opts, label_visibility="collapsed")

    with f2:
        st.markdown('<p class="filter-label">Block / Location</p>', unsafe_allow_html=True)
        loc_opts = ["All Locations"] + sorted(df['Location'].unique().tolist())
        selected_loc = st.selectbox("Location", loc_opts, label_visibility="collapsed")

    with f3:
        st.markdown('<p class="filter-label">Sector / Project Type</p>', unsafe_allow_html=True)
        sector_opts = ["All Sectors"] + sorted(df['Sector'].unique().tolist())
        selected_sector = st.selectbox("Sector", sector_opts, label_visibility="collapsed")

    with f4:
        st.markdown('<p class="filter-label">AI Risk Level</p>', unsafe_allow_html=True)
        risk_opts = ["All Risk Tiers", "Low", "Medium", "High", "Critical"]
        selected_risk = st.selectbox("Risk", risk_opts, label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)

    filtered_df = df.copy()
    if selected_status != "All Statuses (Ongoing & Completed)":
        filtered_df = filtered_df[filtered_df['Status'] == selected_status]
    if selected_loc != "All Locations":
        filtered_df = filtered_df[filtered_df['Location'] == selected_loc]
    if selected_sector != "All Sectors":
        filtered_df = filtered_df[filtered_df['Sector'] == selected_sector]
    if selected_risk != "All Risk Tiers":
        filtered_df = filtered_df[filtered_df['Risk_Level'] == selected_risk]

    if st.button("Clear Filters"):
        st.rerun()

    st.markdown("---")

    # Charts Row
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### Financial Utilization vs Allocation")
        st.caption("Sanctioned vs Actual Expenditure across Key Works (₹ in Lakhs)")
        fin_chart_data = filtered_df[['Sanctioned', 'Revised', 'Actual']].sum() / 100000
        st.bar_chart(fin_chart_data)

    with col_right:
        st.markdown("### Constituency Sector Distribution")
        st.caption("Share of MPLADS funds by sector category")
        sector_counts = filtered_df['Sector'].value_counts()
        st.bar_chart(sector_counts)

    st.markdown("---")

    # Bottom Row: Anomaly Feed & Milestones
    b_left, b_right = st.columns(2)

    with b_left:
        st.markdown("### Recent AI Anomaly Detections")
        st.caption("Automated Audit Feed")
        
        for idx, row in filtered_df.head(3).iterrows():
            st.markdown(f"""
                <div style="border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; margin-bottom: 10px; background: white;">
                    <span style="color: {'red' if row['Risk_Level']=='Critical' else 'orange'}; font-weight: bold;">● {row['Risk_Level']} Risk</span> <b>{row['Project_ID']}</b><br>
                    <b>Cost Deviation:</b> +{row['Cost_Deviation']}% | <b>Score:</b> {row['Risk_Score']}/100<br>
                    <small style="color: #64748b;">{row['Title']} ({row['Location']}) - Progress: {row['Progress']}%</small><br>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Inspect", key=f"inspect_{row['Project_ID']}"):
                st.success(f"Opening audit record for {row['Project_ID']}...")

    with b_right:
        st.markdown("### Milestone Schedule & Target Deadlines")
        st.caption("Upcoming Completion Targets")
        
        st.markdown("""
            <div style="border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; margin-bottom: 10px; background: white;">
                <b>Construction of 2.4 km CC Road with RCC Drain</b><br>
                <small>Target: 2025-02-15 | Contractor: Ganga Valley Engineering Associates</small><br>
                <span style="border: 1px solid red; color: red; padding: 1px 4px; border-radius: 4px; font-size: 11px;">142d Delayed</span> 
                <span style="float: right; font-weight: bold;">38% Done</span>
            </div>
            <div style="border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; margin-bottom: 10px; background: white;">
                <b>Solar Street Lighting Installation Phase 2</b><br>
                <small>Target: 2026-06-30 | Contractor: Apex Infra Solutions</small><br>
                <span style="border: 1px solid orange; color: orange; padding: 1px 4px; border-radius: 4px; font-size: 11px;">On Track</span> 
                <span style="float: right; font-weight: bold;">75% Done</span>
            </div>
        """, unsafe_allow_html=True)