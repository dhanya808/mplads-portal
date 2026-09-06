import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="MPLADS AI Monitor | Government Portal", layout="wide")

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
        .login-header { text-align: center; color: #0f172a; font-weight: 700; margin-bottom: 5px; }
        .login-subheader { text-align: center; color: #64748b; font-size: 13px; margin-bottom: 25px; }
        .secure-badge { text-align: center; color: #16a34a; font-size: 12px; font-weight: 600; margin-top: 15px; }
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
            
            st.markdown("---")
            selected_role = st.selectbox("Demo Role Selector (Persona)", ["MoSPI", "State Nodal Authority", "District Authority", "MP (Varanasi Constituency)"])
            
            submit = st.form_submit_button("Sign In Securely", use_container_width=True)
            
            if submit:
                st.session_state.logged_in = True
                st.session_state.user_role = selected_role
                st.rerun()

        st.markdown('<p class="secure-badge">🔒 256-Bit SSL Encrypted Government Gateway</p>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-size: 11px; color: #94a3b8; margin-top: 20px;">Authorized Access Only • National Informatics Centre (NIC)</p>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MAIN ANALYTICS COMMAND CENTER & DASHBOARD
# ---------------------------------------------------------
else:
    st.markdown("""
        <style>
        .stApp { background-color: #f8fafc; }
        .filter-card {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 24px;
        }
        .filter-label { font-weight: 600; color: #1e293b; font-size: 14px; margin-bottom: 8px; }
        .subtext-contrast { color: #334155; font-weight: 500; }
        </style>
    """, unsafe_allow_html=True)

    nav_col1, nav_col2 = st.columns([4, 1])
    with nav_col1:
        st.markdown(f"## MPLADS AI Monitor | {st.session_state.user_role} Command Center")
        st.caption("Active Scope: National Oversight & Automated AI Risk Triage Engine")
    with nav_col2:
        if st.button("Sign Out"):
            st.session_state.logged_in = False
            st.rerun()

    @st.cache_data
    def load_realistic_data():
        np.random.seed(42)
        n_projects = 200
        
        # Fixing Risk Skewness: Only 15 critical cases out of 200 instead of 96%
        risk_levels = np.random.choice(["Low", "Medium", "High", "Critical"], n_projects, p=[0.5, 0.25, 0.17, 0.08])
        
        # Fixing Risk Score Uniformity: Scatter scores across a realistic range
        risk_scores = [np.random.randint(85, 99) if r=="Critical" else np.random.randint(60, 84) if r=="High" else np.random.randint(35, 59) for r in risk_levels]
        
        # Fixing Uniform Cost Deviation Hazard: Introduce diverse synthetic variances
        cost_devs = np.random.choice([12.5, 24.0, 45.5, 68.0, 85.2, 110.0, 145.5, 210.3, 315.4], n_projects)

        data = {
            'Project_ID': [f"MPLAD-{1000+i}" for i in range(n_projects)],
            'Title': [f"Infrastructure & Utility Development Work at Ward {i}" for i in range(n_projects)],
            'Location': np.random.choice(["Varanasi", "Rohania", "Salem", "Coimbatore", "Pune", "Thane"], n_projects),
            'Sector': np.random.choice(["Roads & Pathways", "Drinking Water Infrastructure", "Community Facilities", "Education & Schools", "Healthcare", "Energy & Solar"], n_projects),
            'Status': np.random.choice(["Ongoing", "Completed", "Delayed", "Pending"], n_projects, p=[0.55, 0.2, 0.15, 0.1]),
            'Risk_Level': risk_levels,
            'Risk_Score': risk_scores,
            'Cost_Deviation': cost_devs,
            'Sanctioned': np.random.randint(10, 80, n_projects) * 100000,
            'Revised': np.random.randint(12, 95, n_projects) * 100000,
            'Actual': np.random.randint(8, 90, n_projects) * 100000,
            'Progress': np.random.randint(20, 98, n_projects)
        }
        return pd.DataFrame(data)

    df = load_realistic_data()

    # Top KPI Metrics Row
    total_active = len(df[df['Status'] == 'Ongoing'])
    total_outlay = f"₹{df['Sanctioned'].sum() / 10000000:.2f} Cr"
    critical_count = len(df[df['Risk_Level'] == 'Critical'])
    delayed_count = len(df[df['Status'] == 'Delayed'])

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TOTAL ACTIVE PROJECTS", len(df))
    m2.metric("SANCTIONED OUTLAY", total_outlay)
    m3.metric("CRITICAL RISK WORKS", critical_count)
    m4.metric("STAGNANT / DELAYED", delayed_count)

    st.markdown("---")

    # 4-Column Horizontal Filter Card Component
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

    # Filter Logic
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

    # TOP ANALYTICS ROW
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

    # BOTTOM ANALYTICS ROW
    b_left, b_right = st.columns(2)

    with b_left:
        st.markdown("### Recent AI Anomaly Detections")
        st.caption("Automated Audit Feed")
        
        for idx, row in filtered_df.head(4).iterrows():
            st.markdown(f"""
                <div style="border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; margin-bottom: 10px; background: white;">
                    <span style="color: {'red' if row['Risk_Level']=='Critical' else 'orange'}; font-weight: bold;">● {row['Risk_Level']} Risk</span> <b>{row['Project_ID']}</b><br>
                    <span class="subtext-contrast"><b>{row['Title']}</b> ({row['Location']} • {row['Sector']})</span><br>
                    <small style="color: #64748b;">Cost Deviation: +{row['Cost_Deviation']}% | AI Score: {row['Risk_Score']}/100 | Progress: {row['Progress']}%</small><br>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Inspect", key=f"inspect_{row['Project_ID']}"):
                st.success(f"Opening audit record dossier for {row['Project_ID']}...")

    with b_right:
        st.markdown("### Milestone Schedule & Target Deadlines")
        st.caption("Upcoming Completion Targets & Geotagged Verification")
        
        st.markdown("""
            <div style="border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; margin-bottom: 10px; background: white;">
                <b>Construction of 2.4 km CC Road with RCC Drain & Solar Lighting</b><br>
                <small class="subtext-contrast">Target: 2025-02-15 | Contractor: Ganga Valley Engineering Associates</small><br>
                <span style="border: 1px solid red; color: red; padding: 1px 4px; border-radius: 4px; font-size: 11px;">142d Delayed</span> 
                <span style="float: right; font-weight: bold;">38% Done</span>
            </div>
            <div style="border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; margin-bottom: 10px; background: white;">
                <b>Geotagged Photo Anomaly Card (Roadmap Feature)</b><br>
                <small class="subtext-contrast">GPS Mismatch: High similarity score (94.2%) with previous site submission MPLAD-1006.</small><br>
                <span style="border: 1px solid orange; color: orange; padding: 1px 4px; border-radius: 4px; font-size: 11px;">Action Required</span> 
                <span style="float: right; font-weight: bold;">Verification Pending</span>
            </div>
        """, unsafe_allow_html=True)