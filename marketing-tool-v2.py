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

if "leads_df" not in st.session_state:
    st.session_state.leads_df = pd.DataFrame(columns=[
        "Lead Name", "Company", "Source", "Inquiry Date", "Proposal Date",
        "Project Go Ahead Date", "Status", "Notes"
    ])

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
        "📋 Lead Tracking",
        "📣 Lead Generation Activities",
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
    col7.metric("Leads", len(st.session_state.leads_df))
    col8.metric("Activities", len(st.session_state.lead_activities_df))

# ====================== DATA INPUT ======================
elif page == "📝 Data Input":
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

# ====================== PROFILE (Single Column) ======================
elif page == "👤 Profile":
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

# ====================== AFFINITY (Single Column) ======================
elif page == "❤️ Affinity":
    st.header("❤️ Customer Affinity & Affiliations")
    st.caption("Map schools, churches, clubs, and employers for hyper-targeted outreach")

    with st.form("add_affinity_form", clear_on_submit=True):
        st.subheader("➕ Add Affinity Data")
        customer_name_aff = st.text_input("Customer / Persona Name*", placeholder="e.g., Sarah Thompson")

        grade_schools = st.text_input("Grade Schools", placeholder="e.g., Lincoln Elementary")
        high_schools = st.text_input("High Schools", placeholder="e.g., Roosevelt High")
        colleges = st.text_input("Colleges", placeholder="e.g., University of Michigan")
        advanced_degrees = st.text_input("Advanced Degree Programs", placeholder="e.g., MBA - Harvard")
        church = st.text_input("Church Affiliations", placeholder="e.g., First Baptist Church")
        fraternal = st.text_input("Fraternal Affiliations", placeholder="e.g., Kappa Sigma")
        service = st.text_input("Service Affiliations", placeholder="e.g., Rotary Club")
        clubs = st.text_input("Clubs", placeholder="e.g., Book Club, Golf Club")
        community = st.text_input("Community Groups", placeholder="e.g., PTA")
        recreational = st.text_input("Recreational Teams", placeholder="e.g., YMCA Soccer")
        employers = st.text_input("Current / Past Employers", placeholder="e.g., Google")

        if st.form_submit_button("➕ Add Affinity Record", use_container_width=True):
            if customer_name_aff.strip():
                new_row = pd.DataFrame([{
                    "Customer": customer_name_aff.strip(),
                    "Grade Schools": grade_schools.strip(), "High Schools": high_schools.strip(),
                    "Colleges": colleges.strip(), "Advanced Degree Programs": advanced_degrees.strip(),
                    "Church Affiliations": church.strip(), "Fraternal Affiliations": fraternal.strip(),
                    "Service Affiliations": service.strip(), "Clubs": clubs.strip(),
                    "Community Groups": community.strip(), "Recreational Teams": recreational.strip(),
                    "Employers": employers.strip()
                }])
                st.session_state.affinity_df = pd.concat([st.session_state.affinity_df, new_row], ignore_index=True)
                st.success(f"Affinity data for **{customer_name_aff}** added!")
                if auto_save:
                    save_all_data()
            else:
                st.warning("Customer/Persona Name is required.")

    st.divider()
    st.subheader("📋 All Affinity Records")
    if not st.session_state.affinity_df.empty:
        edited_affinity = st.data_editor(st.session_state.affinity_df, use_container_width=True, num_rows="dynamic", key="affinity_editor")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Affinity Changes", use_container_width=True):
                st.session_state.affinity_df = edited_affinity.copy()
                st.success("Affinity records updated!")
                if auto_save:
                    save_all_data()
        with col2:
            if st.button("🗑️ Clear All Affinity", type="secondary"):
                st.session_state.affinity_df = pd.DataFrame(columns=st.session_state.affinity_df.columns)
                st.rerun()
    else:
        st.info("No affinity records yet.")

# ====================== LOCATION (Single Column) ======================
elif page == "📍 Location":
    st.header("📍 Customer Location & Classification")
    st.caption("Geographic and business classification for localized campaigns")

    with st.form("add_location_form", clear_on_submit=True):
        st.subheader("➕ Add Location Data")
        customer_name_loc = st.text_input("Customer / Persona Name*", placeholder="e.g., Sarah Thompson")

        block = st.text_input("Block / Street", placeholder="e.g., 1234 Maple Ave")
        carrier_route = st.text_input("Carrier Route", placeholder="e.g., C012")
        zip_code = st.text_input("Zip Code", placeholder="e.g., 90210")
        neighborhood = st.text_input("Neighborhood", placeholder="e.g., Beverly Hills")
        city = st.text_input("City", placeholder="e.g., Los Angeles")
        metro_area = st.text_input("Metro Area", placeholder="e.g., Greater LA")
        state = st.text_input("State", placeholder="e.g., CA")
        county = st.text_input("County", placeholder="e.g., Los Angeles County")
        country = st.text_input("Country", value="USA")
        sic_code = st.text_input("SIC Code (if business)", placeholder="e.g., 8742")
        business_type = st.text_input("Business Type", placeholder="e.g., Retail")
        customer_type = st.selectbox("Customer Type", ["Consumer", "Business", "B2B", "B2C", "Non-profit"])

        if st.form_submit_button("➕ Add Location Record", use_container_width=True):
            if customer_name_loc.strip():
                new_row = pd.DataFrame([{
                    "Customer": customer_name_loc.strip(), "Block": block.strip(),
                    "Carrier Route": carrier_route.strip(), "Zip Code": zip_code.strip(),
                    "Neighborhood": neighborhood.strip(), "City": city.strip(),
                    "Metro Area": metro_area.strip(), "State": state.strip(),
                    "County": county.strip(), "Country": country,
                    "SIC Code": sic_code.strip(), "Business Type": business_type.strip(),
                    "Customer Type": customer_type
                }])
                st.session_state.location_df = pd.concat([st.session_state.location_df, new_row], ignore_index=True)
                st.success(f"Location data for **{customer_name_loc}** added!")
                if auto_save:
                    save_all_data()
            else:
                st.warning("Customer/Persona Name is required.")

    st.divider()
    st.subheader("📋 All Location Records")
    if not st.session_state.location_df.empty:
        edited_location = st.data_editor(st.session_state.location_df, use_container_width=True, num_rows="dynamic", key="location_editor")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Location Changes", use_container_width=True):
                st.session_state.location_df = edited_location.copy()
                st.success("Location records updated!")
                if auto_save:
                    save_all_data()
        with col2:
            if st.button("🗑️ Clear All Locations", type="secondary"):
                st.session_state.location_df = pd.DataFrame(columns=st.session_state.location_df.columns)
                st.rerun()
    else:
        st.info("No location records yet.")

# ====================== CUSTOMER TYPE & ROLES (Single Column) ======================
elif page == "🧑‍💼 Customer Type & Roles":
    st.header("🧑‍💼 Customer Type & Roles")
    st.caption("Classify customers as Consumer vs Business and identify key roles")

    customer_type_options = ["Consumer", "Business", "B2B", "B2C", "Non-profit", "Government"]
    role_options = ["Decision Maker", "Gatekeeper", "Influencer", "Buyer", "End User", "Other"]

    with st.form("add_customer_type_form", clear_on_submit=True):
        st.subheader("➕ Add / Update Customer Classification")
        customer_name_ct = st.text_input("Customer / Persona Name*", placeholder="e.g., Sarah Thompson or Acme Corp")

        cust_type = st.selectbox("Customer Type", customer_type_options)
        role = st.selectbox("Role", role_options)
        notes = st.text_area("Notes (optional)", height=80, placeholder="e.g., Primary decision maker for IT purchases")

        if st.form_submit_button("➕ Add Classification", use_container_width=True):
            if customer_name_ct.strip():
                new_row = pd.DataFrame([{
                    "Customer": customer_name_ct.strip(),
                    "Customer Type": cust_type,
                    "Role": role,
                    "Notes": notes.strip()
                }])
                st.session_state.customer_type_df = pd.concat([st.session_state.customer_type_df, new_row], ignore_index=True)
                st.success(f"Classification added for **{customer_name_ct}**")
                if auto_save:
                    save_all_data()
            else:
                st.warning("Customer/Persona Name is required.")

    st.divider()
    st.subheader("📋 All Customer Classifications")
    if not st.session_state.customer_type_df.empty:
        edited_ct = st.data_editor(st.session_state.customer_type_df, use_container_width=True, num_rows="dynamic", key="ct_editor")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Changes", use_container_width=True):
                st.session_state.customer_type_df = edited_ct.copy()
                st.success("Classifications updated!")
                if auto_save:
                    save_all_data()
        with col2:
            if st.button("🗑️ Clear All Classifications", type="secondary"):
                st.session_state.customer_type_df = pd.DataFrame(columns=st.session_state.customer_type_df.columns)
                st.rerun()
    else:
        st.info("No classifications yet. Use the form above.")

# ====================== LEAD TRACKING ======================
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
                    "Proposal Date": str(proposal_date) if proposal_date else "",
                    "Project Go Ahead Date": str(go_ahead_date) if go_ahead_date else "",
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
        edited_leads = st.data_editor(st.session_state.leads_df, use_container_width=True, num_rows="dynamic", key="leads_editor")
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

# ====================== LEAD GENERATION ACTIVITIES ======================
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
            st.session_state.lead_activities_df = pd.concat([st.session_state.lead_activities_df, new_row], ignore_index=True)
            st.success(f"Activity **{activity}** recorded!")
            if auto_save:
                save_all_data()

    st.divider()
    st.subheader("📋 All Lead Generation Activities")
    if not st.session_state.lead_activities_df.empty:
        edited_acts = st.data_editor(st.session_state.lead_activities_df, use_container_width=True, num_rows="dynamic", key="activities_editor")
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

        total_budget = st.session_state.lead_activities_df["Budget"].sum()
        total_actual = st.session_state.lead_activities_df["Actual Spend"].sum()
        st.metric("Total Budget", f"${total_budget:,.2f}")
        st.metric("Total Actual Spend", f"${total_actual:,.2f}")
        if total_budget > 0:
            st.progress(min(total_actual / total_budget, 1.0))
    else:
        st.info("No activities tracked yet. Use the form above to start logging spend.")

# ====================== SWOT ANALYSIS ======================
elif page == "🛡️ SWOT Analysis":
    st.header("🛡️ SWOT Analysis & Competitor Intelligence")
    st.caption("Compare your company vs competitors with structured SWOT + key financial metrics")

    common_mistakes = [
        "Thinking marketing is advertising", "Lack of patience", "Fear of failure",
        "Diligent follow through", "Throwing money at problems that don't exist",
        "Resisting the use of a marketing plan", "Viewing marketing as a miracle cure",
        "Putting all your marketing eggs in one basket", "Doing it all in house",
        "Say one thing one day, say something different the next"
    ]

    with st.form("add_swot_form", clear_on_submit=True):
        st.subheader("➕ Add Competitor SWOT Entry")
        your_company = st.text_input("Your Company Name", value=st.session_state.company_name or "")
        competitor = st.text_input("Competitor Name*", placeholder="e.g., Acme Corp")

        strengths = st.text_area("Strengths", height=100, placeholder="What does this competitor do well?")
        weaknesses = st.text_area("Weaknesses", height=100, placeholder="Where does this competitor struggle?")
        opportunities = st.text_area("Opportunities", height=100, placeholder="Market gaps or trends...")
        threats = st.text_area("Threats", height=100, placeholder="Risks or challenges...")

        avoid_mistakes = st.multiselect("Avoid Common Mistakes (select all that apply)", common_mistakes, default=[])

        st.divider()
        st.subheader("Financial Metrics")
        total_sales = st.number_input("Total Sales", min_value=0.0, step=1000.0, format="%.2f")
        gross_profit = st.number_input("Total Gross Profit", min_value=0.0, step=1000.0, format="%.2f")
        net_profit = st.number_input("Total Net Profit", min_value=0.0, step=1000.0, format="%.2f")
        cogs = st.number_input("Cost of Goods Sold", min_value=0.0, step=1000.0, format="%.2f")
        staff_cost = st.number_input("Cost of Dedicated Staff", min_value=0.0, step=1000.0, format="%.2f")
        customer_profit = st.number_input("Total Customer Profit", min_value=0.0, step=1000.0, format="%.2f")
        customer_revenue = st.number_input("Customer Revenue", min_value=0.0, step=1000.0, format="%.2f")

        if st.form_submit_button("➕ Add SWOT Entry", use_container_width=True):
            if competitor.strip():
                new_row = pd.DataFrame([{
                    "Your Company": your_company.strip() or st.session_state.company_name,
                    "Competitor": competitor.strip(),
                    "Strengths": strengths.strip(), "Weaknesses": weaknesses.strip(),
                    "Opportunities": opportunities.strip(), "Threats": threats.strip(),
                    "Avoid Common Mistakes": ", ".join(avoid_mistakes),
                    "Total Sales": total_sales, "Total Gross Profit": gross_profit,
                    "Total Net Profit": net_profit, "Cost of Goods Sold": cogs,
                    "Cost of Dedicated Staff": staff_cost,
                    "Total Customer Profit": customer_profit,
                    "Customer Revenue": customer_revenue
                }])
                st.session_state.swot_df = pd.concat([st.session_state.swot_df, new_row], ignore_index=True)
                st.success(f"SWOT entry for **{competitor}** added!")
                if auto_save:
                    save_all_data()
            else:
                st.warning("Competitor Name is required.")

    st.divider()
    st.subheader("📋 All SWOT & Competitor Records")
    if not st.session_state.swot_df.empty:
        edited_swot = st.data_editor(st.session_state.swot_df, use_container_width=True, num_rows="dynamic", key="swot_editor")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save SWOT Changes", use_container_width=True):
                st.session_state.swot_df = edited_swot.copy()
                st.success("SWOT data updated!")
                if auto_save:
                    save_all_data()
        with col2:
            if st.button("🗑️ Clear All SWOT Data", type="secondary"):
                st.session_state.swot_df = pd.DataFrame(columns=st.session_state.swot_df.columns)
                st.rerun()

        st.divider()
        st.subheader("🔍 Detailed SWOT View")
        if not st.session_state.swot_df.empty:
            selected = st.selectbox("Select Competitor", st.session_state.swot_df["Competitor"].unique())
            row = st.session_state.swot_df[st.session_state.swot_df["Competitor"] == selected].iloc[0]
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🟢 Strengths**"); st.info(row["Strengths"] or "—")
                st.markdown("**🔵 Opportunities**"); st.info(row["Opportunities"] or "—")
            with col2:
                st.markdown("**🔴 Weaknesses**"); st.warning(row["Weaknesses"] or "—")
                st.markdown("**🟠 Threats**"); st.error(row["Threats"] or "—")
            if row["Avoid Common Mistakes"]:
                st.markdown("**⚠️ Common Mistakes to Avoid**")
                st.write(row["Avoid Common Mistakes"])
    else:
        st.info("No SWOT entries yet.")

# ====================== STRATEGIES ======================
elif page == "🎯 Strategies":
    st.header("🎯 Marketing Strategies")
    st.caption("Build powerful, action-oriented marketing strategies")

    st.subheader("Action-Oriented Strategy Starters")
    action_words = ["coordinate", "improve", "plan", "execute", "complete", "develop", "restructure",
                    "research", "investigate", "upgrade", "design", "acquire", "obtain", "quantify", "analyze"]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Recommended action words:**")
        st.write(", ".join([f"`{word}`" for word in action_words]))

    pricing_strategies = [
        "highest market price", "price in the highest tier", "price in the middle market tier",
        "price in the lowest market tier", "everyday low price", "zone pricing", "quantity pricing",
        "segmented by time of purchase", "product bundling", "loyalty customer pricing",
        "trial pricing", "price discounting", "trade dealing"
    ]

    with col2:
        st.markdown("**Pricing Strategies:**")
        for p in pricing_strategies:
            st.write(f"• {p}")

    st.divider()

    st.subheader("🛠️ Strategy Builder")
    col1, col2 = st.columns(2)
    with col1:
        selected_action = st.selectbox("Action Word", action_words, index=0)
    with col2:
        selected_pricing = st.selectbox("Pricing Strategy", pricing_strategies, index=0)

    objective = st.text_area("Strategy Objective / Description", placeholder="e.g., Increase market share in the premium segment by Q4", height=100)

    if st.button("➕ Add Strategy to My List", use_container_width=True):
        if objective.strip():
            new_strategy = pd.DataFrame([{
                "Action Verb": selected_action,
                "Pricing Strategy": selected_pricing,
                "Objective / Description": objective.strip(),
                "Date Added": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
            }])
            st.session_state.strategies_df = pd.concat([st.session_state.strategies_df, new_strategy], ignore_index=True)
            st.success("Strategy added successfully!")
            if auto_save:
                save_all_data()
        else:
            st.warning("Please add a short objective/description.")

    st.divider()
    st.subheader("📋 My Saved Strategies")
    if not st.session_state.strategies_df.empty:
        edited_strategies = st.data_editor(st.session_state.strategies_df, use_container_width=True, num_rows="dynamic", key="strategies_editor")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Changes to Strategies"):
                st.session_state.strategies_df = edited_strategies.copy()
                st.success("Strategies saved!")
                if auto_save:
                    save_all_data()
        with col2:
            if st.button("🗑️ Clear All Strategies", type="secondary"):
                st.session_state.strategies_df = pd.DataFrame(columns=st.session_state.strategies_df.columns)
                st.rerun()
    else:
        st.info("No strategies saved yet.")

# ====================== ANALYTICS ======================
elif page == "📈 Analytics":
    st.header("📈 Detailed Analytics")
    st.info("Analytics coming soon... (You can build charts here using the saved data)")

# ====================== EXPORT ======================
elif page == "📤 Export":
    st.header("📤 Export Data")
    st.info("You can export data from individual pages using the data editors. Use the sidebar 'Save All Data' button for full backup.")

# ====================== GLOBAL SAVE BUTTON ======================
st.sidebar.divider()
if st.sidebar.button("💾 Save All Data Now", use_container_width=True, type="primary"):
    save_all_data()

st.sidebar.caption("Marketing Dashboard v2 • Data is persisted in /data folder")
