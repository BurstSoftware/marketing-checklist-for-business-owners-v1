import streamlit as st
import pandas as pd
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="Marketing Dashboard v1",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Marketing Dashboard")
st.caption("Marketing Tool v1 • Customer Profiling + Strategy Planning")

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
        "🎯 Strategies",
        "📈 Analytics",
        "📤 Export"
    ],
    index=0
)

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

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Profile Records", len(st.session_state.profile_df))
    col2.metric("Affinity Records", len(st.session_state.affinity_df))
    col3.metric("Location Records", len(st.session_state.location_df))
    col4.metric("Metric Entries", len(st.session_state.metrics_df))
    col5.metric("Saved Strategies", len(st.session_state.strategies_df))

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

    st.divider()
    if not st.session_state.metrics_df.empty:
        edited = st.data_editor(st.session_state.metrics_df, use_container_width=True, num_rows="dynamic")
        if st.button("💾 Save Changes"):
            st.session_state.metrics_df = edited.copy()

# ====================== PROFILE ======================
elif page == "👤 Profile":
    st.header("👤 Customer Profile Data")
    st.caption("Build detailed customer personas for targeted marketing")

    with st.form("add_profile_form", clear_on_submit=True):
        st.subheader("➕ Add New Customer Profile")
        col1, col2 = st.columns(2)
        with col1:
            customer_name = st.text_input("Customer / Persona Name*", placeholder="e.g., Sarah Thompson")
            age = st.number_input("Age", min_value=18, max_value=100, value=35)
            gender = st.selectbox("Gender", ["Female", "Male", "Non-binary", "Prefer not to say"])
            marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed", "Partnered"])
            household_size = st.number_input("Household Size", min_value=1, max_value=10, value=3)
        with col2:
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
            else:
                st.warning("Customer/Persona Name is required.")

    st.divider()
    st.subheader("📋 All Customer Profiles")
    if not st.session_state.profile_df.empty:
        edited_profile = st.data_editor(
            st.session_state.profile_df, use_container_width=True, num_rows="dynamic", key="profile_editor"
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Profile Changes", use_container_width=True):
                st.session_state.profile_df = edited_profile.copy()
                st.success("Profiles updated!")
        with col2:
            if st.button("🗑️ Clear All Profiles", type="secondary"):
                st.session_state.profile_df = pd.DataFrame(columns=st.session_state.profile_df.columns)
                st.rerun()
    else:
        st.info("No profiles yet. Use the form above to start building personas.")

# ====================== AFFINITY ======================
elif page == "❤️ Affinity":
    st.header("❤️ Customer Affinity & Affiliations")
    st.caption("Map schools, churches, clubs, and employers for hyper-targeted outreach")

    with st.form("add_affinity_form", clear_on_submit=True):
        st.subheader("➕ Add Affinity Data")
        customer_name_aff = st.text_input("Customer / Persona Name*", placeholder="e.g., Sarah Thompson")

        col1, col2 = st.columns(2)
        with col1:
            grade_schools = st.text_input("Grade Schools", placeholder="e.g., Lincoln Elementary")
            high_schools = st.text_input("High Schools", placeholder="e.g., Roosevelt High")
            colleges = st.text_input("Colleges", placeholder="e.g., University of Michigan")
            advanced_degrees = st.text_input("Advanced Degree Programs", placeholder="e.g., MBA - Harvard")
        with col2:
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
            else:
                st.warning("Customer/Persona Name is required.")

    st.divider()
    st.subheader("📋 All Affinity Records")
    if not st.session_state.affinity_df.empty:
        edited_affinity = st.data_editor(
            st.session_state.affinity_df, use_container_width=True, num_rows="dynamic", key="affinity_editor"
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Affinity Changes", use_container_width=True):
                st.session_state.affinity_df = edited_affinity.copy()
                st.success("Affinity records updated!")
        with col2:
            if st.button("🗑️ Clear All Affinity", type="secondary"):
                st.session_state.affinity_df = pd.DataFrame(columns=st.session_state.affinity_df.columns)
                st.rerun()
    else:
        st.info("No affinity records yet.")

# ====================== LOCATION ======================
elif page == "📍 Location":
    st.header("📍 Customer Location & Classification")
    st.caption("Geographic and business classification for localized campaigns")

    with st.form("add_location_form", clear_on_submit=True):
        st.subheader("➕ Add Location Data")
        customer_name_loc = st.text_input("Customer / Persona Name*", placeholder="e.g., Sarah Thompson")

        col1, col2 = st.columns(2)
        with col1:
            block = st.text_input("Block / Street", placeholder="e.g., 1234 Maple Ave")
            carrier_route = st.text_input("Carrier Route", placeholder="e.g., C012")
            zip_code = st.text_input("Zip Code", placeholder="e.g., 90210")
            neighborhood = st.text_input("Neighborhood", placeholder="e.g., Beverly Hills")
            city = st.text_input("City", placeholder="e.g., Los Angeles")
        with col2:
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
            else:
                st.warning("Customer/Persona Name is required.")

    st.divider()
    st.subheader("📋 All Location Records")
    if not st.session_state.location_df.empty:
        edited_location = st.data_editor(
            st.session_state.location_df, use_container_width=True, num_rows="dynamic", key="location_editor"
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Location Changes", use_container_width=True):
                st.session_state.location_df = edited_location.copy()
                st.success("Location records updated!")
        with col2:
            if st.button("🗑️ Clear All Locations", type="secondary"):
                st.session_state.location_df = pd.DataFrame(columns=st.session_state.location_df.columns)
                st.rerun()
    else:
        st.info("No location records yet.")

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
        with col2:
            if st.button("🗑️ Clear All Strategies", type="secondary"):
                st.session_state.strategies_df = pd.DataFrame(columns=st.session_state.strategies_df.columns)
                st.rerun()
    else:
        st.info("No strategies saved yet.")

# ====================== ANALYTICS & EXPORT ======================
elif page == "📈 Analytics":
    st.header("📈 Detailed Analytics")
    st.info("Analytics coming soon...")

elif page == "📤 Export":
    st.header("📤 Export Data")
    st.info("You can export data from individual pages using the data editors.")

# ====================== FOOTER ======================
st.sidebar.divider()
st.sidebar.caption("Marketing Dashboard v1 • Strategy Planning Enabled")
