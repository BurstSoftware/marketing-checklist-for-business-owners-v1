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
        "🎯 Strategies",           # ← NEW PAGE
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

    # Summary Cards (including new Strategies)
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Profile Records", len(st.session_state.profile_df))
    col2.metric("Affinity Records", len(st.session_state.affinity_df))
    col3.metric("Location Records", len(st.session_state.location_df))
    col4.metric("Metric Entries", len(st.session_state.metrics_df))
    col5.metric("Saved Strategies", len(st.session_state.strategies_df))

# ====================== DATA INPUT ======================
elif page == "📝 Data Input":
    st.header("📝 Add Marketing Metrics")
    # (unchanged from previous version for brevity)
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

# ====================== PROFILE, AFFINITY, LOCATION ======================
# (These pages remain exactly as in the previous version)

elif page == "👤 Profile":
    st.header("👤 Customer Profile Data")
    # ... (same code as last version)

elif page == "❤️ Affinity":
    st.header("❤️ Customer Affinity & Affiliations")
    # ... (same code as last version)

elif page == "📍 Location":
    st.header("📍 Customer Location & Classification")
    # ... (same code as last version)

# ====================== NEW: STRATEGIES PAGE ======================
elif page == "🎯 Strategies":
    st.header("🎯 Marketing Strategies")
    st.caption("Build powerful, action-oriented marketing strategies")

    # === Action Words ===
    st.subheader("Action-Oriented Strategy Starters")
    action_words = [
        "coordinate", "improve", "plan", "execute", "complete",
        "develop", "restructure", "research", "investigate",
        "upgrade", "design", "acquire", "obtain", "quantify", "analyze"
    ]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Recommended action words to start your strategies:**")
        st.write(", ".join([f"`{word}`" for word in action_words]))

    # === Pricing Strategies ===
    st.subheader("Pricing Strategies")
    pricing_strategies = [
        "highest market price",
        "price in the highest tier",
        "price in the middle market tier",
        "price in the lowest market tier",
        "everyday low price",
        "zone pricing",
        "quantity pricing",
        "segmented by time of purchase",
        "product bundling",
        "loyalty customer pricing",
        "trial pricing",
        "price discounting",
        "trade dealing"
    ]

    with col2:
        st.markdown("**Available pricing strategies:**")
        for p in pricing_strategies:
            st.write(f"• {p}")

    st.divider()

    # === Strategy Builder ===
    st.subheader("🛠️ Strategy Builder")

    col1, col2 = st.columns(2)
    with col1:
        selected_action = st.selectbox("Action Word", action_words, index=0)
    with col2:
        selected_pricing = st.selectbox("Pricing Strategy", pricing_strategies, index=0)

    objective = st.text_area(
        "Strategy Objective / Description",
        placeholder="e.g., Increase market share in the premium segment by Q4",
        height=100
    )

    if st.button("➕ Add Strategy to My List", use_container_width=True):
        if objective.strip():
            new_strategy = pd.DataFrame([{
                "Action Verb": selected_action,
                "Pricing Strategy": selected_pricing,
                "Objective / Description": objective.strip(),
                "Date Added": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
            }])
            st.session_state.strategies_df = pd.concat(
                [st.session_state.strategies_df, new_strategy], ignore_index=True
            )
            st.success("Strategy added successfully!")
        else:
            st.warning("Please add a short objective/description.")

    st.divider()

    # === My Saved Strategies ===
    st.subheader("📋 My Saved Strategies")

    if not st.session_state.strategies_df.empty:
        edited_strategies = st.data_editor(
            st.session_state.strategies_df,
            use_container_width=True,
            num_rows="dynamic",
            key="strategies_editor"
        )

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
        st.info("No strategies saved yet. Use the Strategy Builder above to create some.")

# ====================== ANALYTICS & EXPORT ======================
elif page == "📈 Analytics":
    st.header("📈 Detailed Analytics")
    # (same as before)

elif page == "📤 Export":
    st.header("📤 Export Data")
    st.info("You can export data from individual pages using the data editors.")

# ====================== FOOTER ======================
st.sidebar.divider()
st.sidebar.caption("Marketing Dashboard • Strategy Planning Enabled")
