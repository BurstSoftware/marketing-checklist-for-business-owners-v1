import streamlit as st
import pandas as pd
from datetime import date
import os

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="Marketing Dashboard v2",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Marketing Dashboard v2")
st.caption("Marketing Tool v2 • Customer Profiling + Strategy Planning + Lead Tracking + Persistence")

# ====================== DATA DIRECTORY ======================
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# ====================== PERSISTENCE FUNCTIONS ======================
def save_all_data():
    try:
        st.session_state.profile_df.to_csv(os.path.join(DATA_DIR, "profiles.csv"), index=False)
        st.session_state.affinity_df.to_csv(os.path.join(DATA_DIR, "affinity.csv"), index=False)
        st.session_state.location_df.to_csv(os.path.join(DATA_DIR, "location.csv"), index=False)
        st.session_state.metrics_df.to_csv(os.path.join(DATA_DIR, "metrics.csv"), index=False)
        st.session_state.strategies_df.to_csv(os.path.join(DATA_DIR, "strategies.csv"), index=False)
        st.session_state.customer_type_df.to_csv(os.path.join(DATA_DIR, "customer_types.csv"), index=False)
        st.session_state.swot_df.to_csv(os.path.join(DATA_DIR, "swot.csv"), index=False)
        st.session_state.leads_df.to_csv(os.path.join(DATA_DIR, "leads.csv"), index=False)
        st.session_state.lead_activities_df.to_csv(os.path.join(DATA_DIR, "lead_activities.csv"), index=False)
        st.success("✅ All data saved successfully!")
    except Exception as e:
        st.error(f"Error saving data: {e}")

def load_all_data():
    try:
        path = lambda filename: os.path.join(DATA_DIR, filename)
        if os.path.exists(path("profiles.csv")):
            st.session_state.profile_df = pd.read_csv(path("profiles.csv"))
        if os.path.exists(path("affinity.csv")):
            st.session_state.affinity_df = pd.read_csv(path("affinity.csv"))
        if os.path.exists(path("location.csv")):
            st.session_state.location_df = pd.read_csv(path("location.csv"))
        if os.path.exists(path("metrics.csv")):
            st.session_state.metrics_df = pd.read_csv(path("metrics.csv"))
        if os.path.exists(path("strategies.csv")):
            st.session_state.strategies_df = pd.read_csv(path("strategies.csv"))
        if os.path.exists(path("customer_types.csv")):
            st.session_state.customer_type_df = pd.read_csv(path("customer_types.csv"))
        if os.path.exists(path("swot.csv")):
            st.session_state.swot_df = pd.read_csv(path("swot.csv"))
        if os.path.exists(path("leads.csv")):
            st.session_state.leads_df = pd.read_csv(path("leads.csv"))
        if os.path.exists(path("lead_activities.csv")):
            st.session_state.lead_activities_df = pd.read_csv(path("lead_activities.csv"))
    except Exception as e:
        st.warning(f"Could not load some saved data: {e}")

# ====================== SESSION STATE ======================
if "metrics_df" not in st.session_state:
    st.session_state.metrics_df = pd.DataFrame(columns=["Date", "Metric", "Value", "Notes"])

if "company_name" not in st.session_state:
    st.session_state.company_name = ""

if "profile_df" not in st.session_state:
    st.session_state.profile_df = pd.DataFrame(columns=[
        "Customer", "Age", "Gender", "Marital Status", "Household Size",
        "Has Children", "Children Ages", "Ethnic Group", "Education",
        "Occupation", "Religion", "Primary Language", "Home Ownership", "Car Type"
    ])

if "affinity_df" not in st.session_state:
    st.session_state.affinity_df = pd.DataFrame(columns=[
        "Customer", "Grade Schools", "High Schools", "Colleges", "Advanced Degree Programs",
        "Church Affiliations", "Fraternal Affiliations", "Service Affiliations",
        "Clubs", "Community Groups", "Recreational Teams", "Employers"
    ])

if "location_df" not in st.session_state:
    st.session_state.location_df = pd.DataFrame(columns=[
        "Customer", "Block", "Carrier Route", "Zip Code", "Neighborhood",
        "City", "Metro Area", "State", "County", "Country",
        "SIC Code", "Business Type", "Customer Type"
    ])

if "strategies_df" not in st.session_state:
    st.session_state.strategies_df = pd.DataFrame(columns=[
        "Action Verb", "Pricing Strategy", "Objective / Description", "Date Added"
    ])

if "customer_type_df" not in st.session_state:
    st.session_state.customer_type_df = pd.DataFrame(columns=[
        "Customer", "Customer Type", "Role", "Notes"
    ])

if "swot_df" not in st.session_state:
    st.session_state.swot_df = pd.DataFrame(columns=[
        "Your Company", "Competitor", "Strengths", "Weaknesses", "Opportunities", "Threats",
        "Avoid Common Mistakes", "Total Sales", "Total Gross Profit", "Total Net Profit",
        "Cost of Goods Sold", "Cost of Dedicated Staff", "Total Customer Profit", "Customer Revenue"
    ])

# NEW: Lead Tracking
if "leads_df" not in st.session_state:
    st.session_state.leads_df = pd.DataFrame(columns=[
        "Lead Name", "Company", "Source", "Inquiry Date", "Proposal Date",
        "Project Go Ahead Date", "Status", "Notes"
    ])

# NEW: Lead Generation Activities
if "lead_activities_df" not in st.session_state:
    st.session_state.lead_activities_df = pd.DataFrame(columns=[
        "Activity", "Budget", "Actual Spend", "Notes", "Date Added"
    ])

load_all_data()

# ====================== SIDEBAR NAVIGATION ======================
st.sidebar.title("🧭 Navigation")

page = st.sidebar.radio(
    "Go to page",
    [
        "🏠 Marketing Dashboard",
        "📝 Data Input",
        "👤 Profile",
        "❤️ Affinity",
        "📍 Location",
        "🧑‍💼 Customer Type & Roles",
        "📋 Lead Tracking",                    # NEW
        "📣 Lead Generation Activities",       # NEW
        "🛡️ SWOT Analysis",
        "🎯 Strategies",
        "📈 Analytics",
        "📤 Export"
    ],
    index=0
)

auto_save = st.sidebar.checkbox("Auto-save after changes", value=True)

# ====================== MARKETING DASHBOARD ======================
if page == "🏠 Marketing Dashboard":
    st.header("Marketing Dashboard")

    if not st.session_state.company_name:
        with st.form("company_setup"):
            company = st.text_input("Company Name")
            if st.form_submit_button("Save Company Name", use_container_width=True):
                if company.strip():
                    st.session_state.company_name = company.strip()
                    st.rerun()
    else:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.subheader(f"📊 {st.session_state.company_name}")
        with col2:
            if st.button("✏️ Change"):
                st.session_state.company_name = ""
                st.rerun()

    st.divider()

    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    col1.metric("Profiles", len(st.session_state.profile_df))
    col2.metric("Affinity", len(st.session_state.affinity_df))
    col3.metric("Locations", len(st.session_state.location_df))
    col4.metric("Metrics", len(st.session_state.metrics_df))
    col5.metric("Strategies", len(st.session_state.strategies_df))
    col6.metric("Classifications", len(st.session_state.customer_type_df))
    col7.metric("Leads", len(st.session_state.leads_df))           # NEW
    col8.metric("Activities", len(st.session_state.lead_activities_df))  # NEW

# ====================== DATA INPUT (unchanged) ======================
elif page == "📝 Data Input":
    # ... (keep original Data Input code) ...
    st.header("📝 Add Marketing Metrics")
    with st.form("add_entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            input_date = st.date_input("Date", value=date.today())
            metric = st.text_input("Metric Name")
        with col2:
            value = st.number_input("Value", min_value=0.0, step=0.01, format="%.2f")
            notes = st.text_area("Notes", height=80)

        if st.form_submit_button("➕ Add Entry", use_container_width=True):
            if metric.strip():
                new_row = pd.DataFrame({"Date": [input_date], "Metric": [metric.strip()],
                                        "Value": [value], "Notes": [notes.strip()]})
                st.session_state.metrics_df = pd.concat([st.session_state.metrics_df, new_row], ignore_index=True)
                st.success("Metric added!")
                if auto_save:
                    save_all_data()

    st.divider()
    if not st.session_state.metrics_df.empty:
        edited = st.data_editor(st.session_state.metrics_df, use_container_width=True, num_rows="dynamic")
        if st.button("💾 Save Changes"):
            st.session_state.metrics_df = edited.copy()
            if auto_save:
                save_all_data()

# ====================== PROFILE (Single Column - as before) ======================
elif page == "👤 Profile":
    # ... (keep the single-column version I gave you earlier) ...
    st.header("👤 Customer Profile Data")
    st.caption("Build detailed customer personas for targeted marketing")

    with st.form("add_profile_form", clear_on_submit=True):
        st.subheader("➕ Add New Customer Profile")
        customer_name = st.text_input("Customer / Persona Name*", placeholder="e.g., Sarah Thompson")
        age = st.number_input("Age", min_value=18, max_value=100, value=35)
        gender = st.selectbox("Gender", ["Female", "Male", "Non-binary", "Prefer not to say"])
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed", "Partnered"])
        household_size = st.number_input("Household Size", min_value=1, max_value=10, value=3)
        has_children = st.selectbox("Has Children", ["Yes", "No"])
        children_ages = st.text_input("Children Ages (if any)", placeholder="e.g., 5, 8")
        ethnic_group = st.text_input("Ethnic Group", placeholder="e.g., Caucasian, Hispanic, Asian")
        education = st.selectbox("Education", ["High School", "Some College", "Bachelor's", "Master's", "Doctorate", "Other"])
        occupation = st.text_input("Occupation", placeholder="e.g., Marketing Manager")
        religion = st.text_input("Religion", placeholder="e.g., Christian, None")
        primary_language = st.text_input("Primary Language", value="English")
        home_ownership = st.selectbox("Home Ownership", ["Own", "Rent", "Live with family"])
        car_type = st.text_input("Car Type", placeholder="e.g., Tesla Model Y, Toyota Camry")

        if st.form_submit_button("➕ Add Profile", use_container_width=True):
            if customer_name.strip():
                new_row = pd.DataFrame([{
                    "Customer": customer_name.strip(), "Age": age, "Gender": gender,
                    "Marital Status": marital_status, "Household Size": household_size,
                    "Has Children": has_children, "Children Ages": children_ages.strip(),
                    "Ethnic Group": ethnic_group.strip(), "Education": education,
                    "Occupation": occupation.strip(), "Religion": religion.strip(),
                    "Primary Language": primary_language, "Home Ownership": home_ownership,
                    "Car Type": car_type.strip()
                }])
                st.session_state.profile_df = pd.concat([st.session_state.profile_df, new_row], ignore_index=True)
                st.success(f"Profile for **{customer_name}** added!")
                if auto_save:
                    save_all_data()
            else:
                st.warning("Customer/Persona Name is required.")

    st.divider()
    st.subheader("📋 All Customer Profiles")
    if not st.session_state.profile_df.empty:
        edited_profile = st.data_editor(st.session_state.profile_df, use_container_width=True, num_rows="dynamic", key="profile_editor")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Profile Changes", use_container_width=True):
                st.session_state.profile_df = edited_profile.copy()
                st.success("Profiles updated!")
                if auto_save:
                    save_all_data()
        with col2:
            if st.button("🗑️ Clear All Profiles", type="secondary"):
                st.session_state.profile_df = pd.DataFrame(columns=st.session_state.profile_df.columns)
                st.rerun()
    else:
        st.info("No profiles yet.")

# ====================== AFFINITY, LOCATION, CUSTOMER TYPE (Single Column versions) ======================
# (Keep the single-column versions from previous response for these three pages)

elif page == "❤️ Affinity":
    # Paste the single-column Affinity code from my previous response here
    st.header("❤️ Customer Affinity & Affiliations")
    # ... (full single-column form + table as before)

elif page == "📍 Location":
    # Paste the single-column Location code from previous response
    st.header("📍 Customer Location & Classification")
    # ... (full single-column form + table)

elif page == "🧑‍💼 Customer Type & Roles":
    # Paste the single-column Customer Type code from previous response
    st.header("🧑‍💼 Customer Type & Roles")
    # ... (full single-column form + table)

# ====================== NEW: LEAD TRACKING ======================
elif page == "📋 Lead Tracking":
    st.header("📋 Lead Tracking")
    st.caption("Track leads from inquiry through project go-ahead")

    with st.form("add_lead_form", clear_on_submit=True):
        st.subheader("➕ Add New Lead")
        lead_name = st.text_input("Lead Name / Contact*", placeholder="e.g., John Smith")
        company = st.text_input("Company", placeholder="e.g., Acme Corp")
        source = st.text_input("Source", placeholder="e.g., Website, Referral, Trade Show, Cold Call")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            inquiry_date = st.date_input("Inquiry Date", value=date.today())
        with col2:
            proposal_date = st.date_input("Proposal Date", value=None)
        with col3:
            go_ahead_date = st.date_input("Project Go Ahead Date", value=None)

        status = st.selectbox("Status", ["New", "Qualified", "Proposal Sent", "Negotiation", "Won", "Lost", "On Hold"])
        notes = st.text_area("Notes", height=80, placeholder="Additional details...")

        if st.form_submit_button("➕ Add Lead", use_container_width=True):
            if lead_name.strip():
                new_row = pd.DataFrame([{
                    "Lead Name": lead_name.strip(),
                    "Company": company.strip(),
                    "Source": source.strip(),
                    "Inquiry Date": inquiry_date,
                    "Proposal Date": proposal_date if proposal_date else "",
                    "Project Go Ahead Date": go_ahead_date if go_ahead_date else "",
                    "Status": status,
                    "Notes": notes.strip()
                }])
                st.session_state.leads_df = pd.concat([st.session_state.leads_df, new_row], ignore_index=True)
                st.success(f"Lead for **{lead_name}** added!")
                if auto_save:
                    save_all_data()
            else:
                st.warning("Lead Name is required.")

    st.divider()
    st.subheader("📋 All Leads")
    if not st.session_state.leads_df.empty:
        edited_leads = st.data_editor(
            st.session_state.leads_df, use_container_width=True, num_rows="dynamic", key="leads_editor"
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Lead Changes", use_container_width=True):
                st.session_state.leads_df = edited_leads.copy()
                st.success("Leads updated!")
                if auto_save:
                    save_all_data()
        with col2:
            if st.button("🗑️ Clear All Leads", type="secondary"):
                st.session_state.leads_df = pd.DataFrame(columns=st.session_state.leads_df.columns)
                st.rerun()
    else:
        st.info("No leads tracked yet. Use the form above.")

# ====================== NEW: LEAD GENERATION ACTIVITIES ======================
elif page == "📣 Lead Generation Activities":
    st.header("📣 Lead Generation Activities")
    st.caption("Track budget and spend across all lead generation channels")

    activities_list = [
        "advertising", "brochures / flyers", "coop marketing programs", "direct mail programs",
        "directories", "email programs", "identity work (logo)", "packaging",
        "point of purchase materials", "postage", "premiums", "presentations",
        "promotions", "publicity", "sales kits", "marketing materials", "signage",
        "telemarketing", "trade show", "uniforms", "yellow pages", "website",
        "marketing personnel", "sales personnel", "travel / entertainment", "other"
    ]

    with st.form("add_activity_form", clear_on_submit=True):
        st.subheader("➕ Add / Update Activity Spend")
        activity = st.selectbox("Activity Type", activities_list)
        budget = st.number_input("Budget Allocated", min_value=0.0, step=100.0, format="%.2f")
        actual = st.number_input("Actual Spend", min_value=0.0, step=100.0, format="%.2f")
        notes = st.text_area("Notes", height=60, placeholder="Details or comments...")

        if st.form_submit_button("➕ Add Activity Record", use_container_width=True):
            new_row = pd.DataFrame([{
                "Activity": activity,
                "Budget": budget,
                "Actual Spend": actual,
                "Notes": notes.strip(),
                "Date Added": pd.Timestamp.now().strftime("%Y-%m-%d")
            }])
            st.session_state.lead_activities_df = pd.concat(
                [st.session_state.lead_activities_df, new_row], ignore_index=True
            )
            st.success(f"Activity **{activity}** recorded!")
            if auto_save:
                save_all_data()

    st.divider()
    st.subheader("📋 All Lead Generation Activities")
    if not st.session_state.lead_activities_df.empty:
        edited_acts = st.data_editor(
            st.session_state.lead_activities_df, use_container_width=True, num_rows="dynamic", key="activities_editor"
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Activity Changes", use_container_width=True):
                st.session_state.lead_activities_df = edited_acts.copy()
                st.success("Activities updated!")
                if auto_save:
                    save_all_data()
        with col2:
            if st.button("🗑️ Clear All Activities", type="secondary"):
                st.session_state.lead_activities_df = pd.DataFrame(columns=st.session_state.lead_activities_df.columns)
                st.rerun()

        # Quick summary
        total_budget = st.session_state.lead_activities_df["Budget"].sum()
        total_actual = st.session_state.lead_activities_df["Actual Spend"].sum()
        st.metric("Total Budget", f"${total_budget:,.2f}")
        st.metric("Total Actual Spend", f"${total_actual:,.2f}")
        if total_budget > 0:
            st.progress(min(total_actual / total_budget, 1.0))
    else:
        st.info("No activities tracked yet. Use the form above to start logging spend.")

# ====================== SWOT, STRATEGIES, ANALYTICS, EXPORT (keep as before) ======================
elif page == "🛡️ SWOT Analysis":
    # ... (keep the full SWOT page from previous response)

elif page == "🎯 Strategies":
    # ... (keep original Strategies code)

elif page == "📈 Analytics":
    st.header("📈 Detailed Analytics")
    st.info("Analytics coming soon...")

elif page == "📤 Export":
    st.header("📤 Export Data")
    st.info("Use data editors on each page. Sidebar 'Save All Data' for full backup.")

# ====================== GLOBAL SAVE BUTTON ======================
st.sidebar.divider()
if st.sidebar.button("💾 Save All Data Now", use_container_width=True, type="primary"):
    save_all_data()

st.sidebar.caption("Marketing Dashboard v2 • All data persisted in /data folder")
