import streamlit as st
import pandas as pd
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="Marketing Dashboard v1",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Marketing Dashboard")
st.caption("Marketing Tool v1 • Track campaigns, revenue & performance")

# ====================== SESSION STATE ======================
if "metrics_df" not in st.session_state:
    st.session_state.metrics_df = pd.DataFrame(
        columns=["Date", "Metric", "Value", "Notes"]
    )

if "company_name" not in st.session_state:
    st.session_state.company_name = ""

# ====================== SIDEBAR NAVIGATION ======================
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio(
    "Go to page",
    ["🏠 Marketing Dashboard", "📝 Data Input", "📈 Analytics", "📤 Export"],
    index=0
)

# ====================== MARKETING DASHBOARD (FRONT PAGE) ======================
if page == "🏠 Marketing Dashboard":
    st.header("Marketing Dashboard")

    # === Company Name Setup ===
    if not st.session_state.company_name:
        st.subheader("👋 Welcome! Let's set up your dashboard")
        with st.form("company_setup"):
            company = st.text_input(
                "Company Name",
                placeholder="e.g. Acme Digital, Nova Labs, etc.",
                help="This will appear on your dashboard and reports"
            )
            if st.form_submit_button("Save Company Name", use_container_width=True):
                if company.strip():
                    st.session_state.company_name = company.strip()
                    st.success(f"Company set to **{st.session_state.company_name}**")
                    st.rerun()
                else:
                    st.error("Please enter a company name.")
    else:
        # Show company name + option to change it
        col1, col2 = st.columns([4, 1])
        with col1:
            st.subheader(f"📊 {st.session_state.company_name}")
        with col2:
            if st.button("✏️ Change Name", use_container_width=True):
                st.session_state.company_name = ""
                st.rerun()

        st.divider()

        # === Dashboard Content ===
        if st.session_state.metrics_df.empty:
            st.info("No data yet. Go to **Data Input** to start adding marketing metrics.")
        else:
            df = st.session_state.metrics_df.copy()
            df["Date"] = pd.to_datetime(df["Date"])

            # --- Marketing KPIs ---
            st.subheader("Key Marketing Metrics")

            def get_metric_total(metric_name):
                mask = df["Metric"].str.lower() == metric_name.lower()
                return df.loc[mask, "Value"].sum()

            col1, col2, col3, col4 = st.columns(4)

            revenue = get_metric_total("Revenue")
            clicks = get_metric_total("Clicks")
            impressions = get_metric_total("Impressions")
            conversions = get_metric_total("Conversions")

            col1.metric("Total Revenue", f"${revenue:,.2f}" if revenue > 0 else "—")
            col2.metric("Total Clicks", f"{int(clicks):,}" if clicks > 0 else "—")
            col3.metric("Total Impressions", f"{int(impressions):,}" if impressions > 0 else "—")
            col4.metric("Total Conversions", f"{int(conversions):,}" if conversions > 0 else "—")

            st.divider()

            # --- Overall Summary ---
            st.subheader("Metrics Overview")
            summary = df.groupby("Metric")["Value"].agg(["sum", "mean", "count"]).reset_index()
            summary.columns = ["Metric", "Total", "Average", "Entries"]
            st.dataframe(summary, use_container_width=True)

            st.divider()

            # --- Quick Trend Chart ---
            st.subheader("Quick Trend Visualization")
            available_metrics = df["Metric"].unique().tolist()
            selected_metric = st.selectbox("Select metric to visualize", available_metrics, key="main_dashboard_metric")

            metric_df = df[df["Metric"] == selected_metric].sort_values("Date")
            st.line_chart(
                metric_df.set_index("Date")["Value"],
                use_container_width=True,
                height=380
            )

            st.caption("💡 Add or edit more detailed entries in the **Data Input** page.")

# ====================== DATA INPUT PAGE ======================
elif page == "📝 Data Input":
    st.header("📝 Add & Manage Marketing Data")

    with st.form("add_entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            input_date = st.date_input("Date", value=date.today())
            metric = st.text_input(
                "Metric Name",
                placeholder="e.g. Revenue, Clicks, Impressions, Conversions, Leads, CTR"
            )

        with col2:
            value = st.number_input("Value", min_value=0.0, step=0.01, format="%.2f")
            notes = st.text_area("Notes (optional)", height=80)

        submitted = st.form_submit_button("➕ Add Entry", use_container_width=True)

        if submitted:
            if not metric.strip():
                st.error("Metric name cannot be empty!")
            else:
                new_row = pd.DataFrame({
                    "Date": [input_date],
                    "Metric": [metric.strip()],
                    "Value": [value],
                    "Notes": [notes.strip()]
                })
                st.session_state.metrics_df = pd.concat(
                    [st.session_state.metrics_df, new_row], ignore_index=True
                )
                st.success("Entry added successfully!")

    st.divider()

    # Edit existing data
    st.subheader("✏️ Edit or Manage Existing Data")

    if not st.session_state.metrics_df.empty:
        edited_df = st.data_editor(
            st.session_state.metrics_df,
            use_container_width=True,
            num_rows="dynamic",
            key="data_editor"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Changes", use_container_width=True):
                st.session_state.metrics_df = edited_df.copy()
                st.success("Changes saved successfully!")

        with col2:
            if st.button("🗑️ Clear All Data", type="secondary", use_container_width=True):
                st.session_state.metrics_df = pd.DataFrame(
                    columns=["Date", "Metric", "Value", "Notes"]
                )
                st.success("All data cleared!")
                st.rerun()
    else:
        st.info("No data to edit yet.")

    # Sample data
    st.divider()
    if st.button("🚀 Load Sample Marketing Data", use_container_width=True):
        sample = pd.DataFrame({
            "Date": pd.to_datetime(["2026-07-01", "2026-07-05", "2026-07-10", "2026-07-15", "2026-07-18"]),
            "Metric": ["Revenue", "Clicks", "Impressions", "Conversions", "Revenue"],
            "Value": [12500.50, 450, 12500, 85, 9800.00],
            "Notes": ["Launch campaign", "Social media ads", "High reach", "Email campaign", "Follow-up sales"]
        })
        st.session_state.metrics_df = pd.concat(
            [st.session_state.metrics_df, sample], ignore_index=True
        )
        st.success("Sample marketing data loaded!")
        st.rerun()

# ====================== ANALYTICS PAGE ======================
elif page == "📈 Analytics":
    st.header("📈 Detailed Analytics")

    if st.session_state.metrics_df.empty:
        st.warning("No data available. Please add entries in the Data Input page.")
    else:
        df = st.session_state.metrics_df.copy()
        df["Date"] = pd.to_datetime(df["Date"])

        # Summary cards
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Entries", len(df))
        col2.metric("Unique Metrics", df["Metric"].nunique())
        col3.metric("Date Range", f"{df['Date'].min().date()} → {df['Date'].max().date()}")

        st.divider()

        # Summary table
        st.subheader("Metrics Summary")
        summary = df.groupby("Metric")["Value"].agg(["sum", "mean", "count"]).reset_index()
        summary.columns = ["Metric", "Total", "Average", "Entries"]
        st.dataframe(summary, use_container_width=True)

        st.divider()

        # Visualization
        st.subheader("Trend Visualization")
        available_metrics = df["Metric"].unique().tolist()
        selected_metric = st.selectbox("Select metric to plot", available_metrics)

        metric_df = df[df["Metric"] == selected_metric].sort_values("Date")
        st.line_chart(
            metric_df.set_index("Date")["Value"],
            use_container_width=True,
            height=400
        )

# ====================== EXPORT PAGE ======================
elif page == "📤 Export":
    st.header("📤 Export Your Data")

    if st.session_state.metrics_df.empty:
        st.info("No data to export yet. Add some entries first.")
    else:
        df = st.session_state.metrics_df.copy()

        st.subheader("Data Preview")
        st.dataframe(df, use_container_width=True)

        st.divider()

        # CSV Export
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download as CSV",
            data=csv_data,
            file_name="marketing_metrics.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.divider()

        # Copy to Clipboard
        st.subheader("📋 Copy to Clipboard")
        csv_text = df.to_csv(index=False)
        st.code(csv_text, language="csv")

        st.divider()

        # PDF Export
        st.subheader("📄 Download as PDF")

        def create_pdf(dataframe):
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []

            company = st.session_state.get("company_name", "Your Company")

            # Title
            elements.append(Paragraph(f"{company} - Marketing Report", styles["Heading1"]))
            elements.append(Paragraph(f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
            elements.append(Spacer(1, 20))

            # Table
            table_data = [["Date", "Metric", "Value", "Notes"]] + dataframe.values.tolist()
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1f77b4")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f8f9fa")),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(table)

            doc.build(elements)
            buffer.seek(0)
            return buffer

        if st.button("Generate PDF", use_container_width=True):
            pdf_buffer = create_pdf(df)
            st.download_button(
                label="📥 Download PDF Now",
                data=pdf_buffer,
                file_name="marketing_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# ====================== FOOTER ======================
st.sidebar.divider()
st.sidebar.caption("Built for Marketing Teams • Python 3.14 Ready")
