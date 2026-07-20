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
    page_title="Marketing Tool v1 - Business Metrics Tracker",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Metrics Tracker")
st.caption("App Version: marketing-tool-v1 | Python 3.14 Compatible")

# ====================== SESSION STATE ======================
if "metrics_df" not in st.session_state:
    st.session_state.metrics_df = pd.DataFrame(
        columns=["Date", "Metric", "Value", "Notes"]
    )

# ====================== SIDEBAR NAVIGATION ======================
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio(
    "Go to page",
    ["🏠 Home", "📝 Data Input", "📈 Dashboard", "📤 Export"],
    index=0
)

# ====================== HOME PAGE ======================
if page == "🏠 Home":
    st.header("Welcome to your Business Metrics Tracker")
    st.write("Track marketing campaigns, revenue, user engagement, and other key business metrics.")

    if st.session_state.metrics_df.empty:
        st.info("No data yet. Go to **Data Input** to start adding entries.")
    else:
        st.subheader("Latest 5 Entries")
        st.dataframe(st.session_state.metrics_df.tail(5), use_container_width=True)

# ====================== DATA INPUT PAGE ======================
elif page == "📝 Data Input":
    st.header("📝 Add New Metric Entry")

    with st.form("add_entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            input_date = st.date_input("Date", value=date.today())
            metric = st.text_input(
                "Metric Name",
                placeholder="e.g. Revenue, Clicks, Impressions, Conversions, Users"
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
    if st.button("🚀 Load Sample Data (Demo)", use_container_width=True):
        sample = pd.DataFrame({
            "Date": pd.to_datetime(["2026-07-01", "2026-07-05", "2026-07-10", "2026-07-15", "2026-07-18"]),
            "Metric": ["Revenue", "Clicks", "Impressions", "Conversions", "Revenue"],
            "Value": [12500.50, 450, 12500, 85, 9800.00],
            "Notes": ["Launch campaign", "Social media ads", "High reach", "Email campaign", "Follow-up sales"]
        })
        st.session_state.metrics_df = pd.concat(
            [st.session_state.metrics_df, sample], ignore_index=True
        )
        st.success("Sample data loaded! Go to Dashboard or Export.")
        st.rerun()

# ====================== DASHBOARD PAGE ======================
elif page == "📈 Dashboard":
    st.header("📈 Metrics Dashboard")

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

        # === CSV Export ===
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download as CSV",
            data=csv_data,
            file_name="business_metrics.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.divider()

        # === Copy to Clipboard ===
        st.subheader("📋 Copy to Clipboard")
        csv_text = df.to_csv(index=False)
        st.code(csv_text, language="csv")
        st.caption("Click the copy icon in the top-right corner of the code block.")

        st.divider()

        # === PDF Export with ReportLab ===
        st.subheader("📄 Download as PDF")

        def create_pdf(dataframe):
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []

            # Title
            elements.append(Paragraph("Business Metrics Tracker Report", styles["Heading1"]))
            elements.append(Paragraph(f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
            elements.append(Spacer(1, 20))

            # Table data
            table_data = [["Date", "Metric", "Value", "Notes"]] + dataframe.values.tolist()

            # Create table
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
                file_name="business_metrics_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# ====================== FOOTER ======================
st.sidebar.divider()
st.sidebar.caption("Built for Business Metrics Tracking • Python 3.14 Ready")
