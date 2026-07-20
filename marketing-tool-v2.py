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
st.caption("Marketing Tool v2 • Customer Profiling + Strategy Planning + Persistence")

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
        st.session_state.problem_assessment.to_csv(os.path.join(DATA_DIR, "problems.csv"), index=False)  # NEW
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
        if os.path.exists(path("problems.csv")):                                      # NEW
            st.session_state.problem_assessment = pd.read_csv(path("problems.csv"))
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
        "Your Company", "Competitor",
        "Strengths", "Weaknesses", "Opportunities", "Threats",
        "Avoid Common Mistakes",
        "Total Sales", "Total Gross Profit", "Total Net Profit",
        "Cost of Goods Sold", "Cost of Dedicated Staff",
        "Total Customer Profit", "Customer Revenue"
    ])

# NEW: Marketing Problems Assessment
if "problem_assessment" not in st.session_state:
    st.session_state.problem_assessment = pd.DataFrame(columns=["Problem", "Severity", "Notes", "Date"])

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
        "🛡️ SWOT Analysis",
        "🎯 Strategies",
        "⚠️ Marketing Problems",      # ← New Page
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

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    col1.metric("Profile Records", len(st.session_state.profile_df))
    col2.metric("Affinity Records", len(st.session_state.affinity_df))
    col3.metric("Location Records", len(st.session_state.location_df))
    col4.metric("Metric Entries", len(st.session_state.metrics_df))
    col5.metric("Saved Strategies", len(st.session_state.strategies_df))
    col6.metric("Classifications", len(st.session_state.customer_type_df))
    col7.metric("SWOT Entries", len(st.session_state.swot_df))

# ====================== DATA INPUT ======================
elif page == "📝 Data Input":
    # ... (your original code remains unchanged)
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

# ====================== PROFILE ======================
elif page == "👤 Profile":
    # ... (your original Profile code - unchanged)
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
        st.info("No profiles yet. Use the form above.")

# (All other pages: Affinity, Location, Customer Type, SWOT, Strategies remain unchanged)
# ... [I kept them exactly as you provided to save space]

# ====================== NEW: MARKETING PROBLEMS PAGE ======================
elif page == "⚠️ Marketing Problems":
    st.header("⚠️ Common Marketing Problems")
    st.caption("Diagnose your biggest challenges and start fixing them")

    problems = [
        "Market is shrinking",
        "Current customers are leaving",
        "Not generating enough new customers",
        "No one knows who we are (low brand awareness)",
        "Market only knows 1 of our products/services",
        "No marketing plan",
        "Marketing is helter-skelter / inconsistent",
        "Lack of staff for marketing",
        "Lack certain tools / assets (brochure, presentation, etc.)",
        "Prices too high",
        "Prices too low",
        "Attracting the wrong kinds of customers",
        "Geographic scope is too limited",
        "We only sell 1 product/service",
        "Lack of consistent image / brand identity"
    ]

    st.subheader("Self-Diagnosis")
    with st.form("problem_form", clear_on_submit=True):
        selected_problems = st.multiselect("Which problems are you facing?", problems, default=[])
        
        col1, col2 = st.columns(2)
        with col1:
            severity = st.select_slider("Overall Severity", 
                                      options=["Low", "Medium", "High", "Critical"], 
                                      value="Medium")
        with col2:
            date_added = st.date_input("Date", value=date.today())

        notes = st.text_area("Additional Notes / Root Causes", 
                           placeholder="Why is this happening? What have you tried?")

        if st.form_submit_button("➕ Add Selected Problems", use_container_width=True):
            if selected_problems:
                for prob in selected_problems:
                    new_row = pd.DataFrame([{
                        "Problem": prob,
                        "Severity": severity,
                        "Notes": notes.strip(),
                        "Date": date_added
                    }])
                    st.session_state.problem_assessment = pd.concat(
                        [st.session_state.problem_assessment, new_row], ignore_index=True
                    )
                st.success(f"Added {len(selected_problems)} problem(s)!")
                if auto_save:
                    save_all_data()
            else:
                st.warning("Please select at least one problem.")

    st.divider()
    st.subheader("📋 Your Current Marketing Challenges")

    if not st.session_state.problem_assessment.empty:
        edited_problems = st.data_editor(
            st.session_state.problem_assessment.sort_values("Date", ascending=False),
            use_container_width=True,
            num_rows="dynamic",
            key="problems_editor"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Changes", use_container_width=True):
                st.session_state.problem_assessment = edited_problems.copy()
                st.success("Assessment updated!")
                if auto_save:
                    save_all_data()
        
        with col2:
            if st.button("🗑️ Clear All Problems", type="secondary"):
                st.session_state.problem_assessment = pd.DataFrame(columns=st.session_state.problem_assessment.columns)
                st.rerun()

        st.divider()
        st.subheader("📊 Quick Summary")
        severity_counts = st.session_state.problem_assessment["Severity"].value_counts()
        st.bar_chart(severity_counts)
        
        st.info("**Pro Tip:** Use the **Strategies** page to build action plans that directly address these issues.")
    else:
        st.info("No problems recorded yet. Use the form above.")

    st.divider()
    with st.expander("💡 Quick Solutions by Problem Type"):
        st.markdown("""
        - **Low awareness** → Brand building + content marketing  
        - **Not getting new customers** → Improve lead generation & targeting  
        - **Customers leaving** → Strengthen retention & loyalty  
        - **No plan / Inconsistent** → Build structured strategy  
        - **Wrong customers** → Refine personas in Profile page  
        - **Brand inconsistency** → Define core message and visuals
        """)

# ====================== ANALYTICS & EXPORT ======================
elif page == "📈 Analytics":
    st.header("📈 Detailed Analytics")
    st.info("Analytics coming soon...")

elif page == "📤 Export":
    st.header("📤 Export Data")
    st.info("Use the data editors on each page to export. Use sidebar 'Save All Data' for backup.")

# ====================== GLOBAL SAVE ======================
st.sidebar.divider()
if st.sidebar.button("💾 Save All Data Now", use_container_width=True, type="primary"):
    save_all_data()

st.sidebar.caption("Marketing Dashboard v2 • Data persisted in /data folder")
