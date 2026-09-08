import streamlit as st
import pandas as pd
import os
import altair as alt

# ============================================================
# CONFIGURATION
# ============================================================

DATA_FILE = "warehouse/final_bookings.csv"

st.set_page_config(
    page_title="Hotel Booking Analytics",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM UI STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: #0b0f17;
        color: #f5f7fa;
    }

    /* Main content */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* Dashboard title */
    .dashboard-title {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }

    .dashboard-subtitle {
        color: #8b95a7;
        font-size: 16px;
        margin-bottom: 30px;
    }

    /* Section headings */
    .section-title {
        font-size: 25px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* KPI cards */
    .kpi-card {
        background: linear-gradient(
            135deg,
            #151b27 0%,
            #10151f 100%
        );
        border: 1px solid #252d3a;
        border-radius: 14px;
        padding: 22px;
        min-height: 125px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.25);
    }

    .kpi-label {
        color: #8b95a7;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .kpi-value {
        color: #f5f7fa;
        font-size: 32px;
        font-weight: 800;
    }

    .kpi-accent-blue {
        border-left: 4px solid #4da3ff;
    }

    .kpi-accent-red {
        border-left: 4px solid #ff5c70;
    }

    .kpi-accent-yellow {
        border-left: 4px solid #f5c451;
    }

    .kpi-accent-green {
        border-left: 4px solid #37d69b;
    }

    /* Info banner */
    .pipeline-banner {
        background: linear-gradient(
            135deg,
            #102943,
            #132f4d
        );
        border: 1px solid #214d73;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 10px 0 25px 0;
        color: #8ec9ff;
        font-size: 15px;
    }

    /* Form card */
    div[data-testid="stForm"] {
        background: #10151f;
        border: 1px solid #252d3a;
        border-radius: 14px;
        padding: 20px;
    }

    /* Buttons */
    .stButton > button,
    .stFormSubmitButton > button {
        border-radius: 9px;
        font-weight: 700;
        border: 1px solid #3c82c6;
        background: #1769aa;
        color: white;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background: #2186d1;
        border-color: #5ba9e6;
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        border: 1px solid #252d3a;
        border-radius: 10px;
        overflow: hidden;
    }

    /* Divider */
    hr {
        border-color: #252d3a !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SESSION STATE
# ============================================================

if "pipeline_message" not in st.session_state:
    st.session_state.pipeline_message = None


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame()

    return pd.read_csv(DATA_FILE)


df = load_data()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">🏨 Hotel Booking Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Real-Time Hotel Booking Intelligence • ETL • Data Warehouse • Analytics'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# PIPELINE SUCCESS MESSAGE
# ============================================================

if st.session_state.pipeline_message:

    st.success(st.session_state.pipeline_message)

    st.session_state.pipeline_message = None


# ============================================================
# DATA CHECK
# ============================================================

if df.empty:
    st.warning("No processed booking data found.")
    st.stop()


# ============================================================
# KPI SECTION
# ============================================================

st.markdown(
    '<div class="section-title">📊 Key Performance Indicators</div>',
    unsafe_allow_html=True
)

total_bookings = len(df)

cancelled = (
    int(df["is_canceled"].sum())
    if "is_canceled" in df.columns
    else 0
)

cancellation_rate = (
    (cancelled / total_bookings) * 100
    if total_bookings > 0
    else 0
)

average_adr = (
    df["adr"].mean()
    if "adr" in df.columns
    else 0
)


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.markdown(
        f"""
        <div class="kpi-card kpi-accent-blue">
            <div class="kpi-label">TOTAL BOOKINGS</div>
            <div class="kpi-value">{total_bookings:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:
    st.markdown(
        f"""
        <div class="kpi-card kpi-accent-red">
            <div class="kpi-label">CANCELLED BOOKINGS</div>
            <div class="kpi-value">{cancelled:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:
    st.markdown(
        f"""
        <div class="kpi-card kpi-accent-yellow">
            <div class="kpi-label">CANCELLATION RATE</div>
            <div class="kpi-value">{cancellation_rate:.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:
    st.markdown(
        f"""
        <div class="kpi-card kpi-accent-green">
            <div class="kpi-label">AVERAGE DAILY RATE</div>
            <div class="kpi-value">{average_adr:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# BOOKING ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">📈 Booking Analysis</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# BOOKINGS BY HOTEL
# ------------------------------------------------------------

if "hotel" in df.columns:

    hotel_counts = (
        df["hotel"]
        .value_counts()
        .rename_axis("Hotel")
        .reset_index(name="Bookings")
    )

    hotel_chart = (
        alt.Chart(hotel_counts)
        .mark_bar(
            cornerRadiusTopLeft=7,
            cornerRadiusTopRight=7,
            size=55
        )
        .encode(
            x=alt.X(
                "Hotel:N",
                title=None,
                sort="-y"
            ),
            y=alt.Y(
                "Bookings:Q",
                title="Number of Bookings"
            ),
            color=alt.Color(
                "Hotel:N",
                scale=alt.Scale(
                    range=["#4da3ff", "#37d69b"]
                ),
                legend=None
            ),
            tooltip=[
                alt.Tooltip("Hotel:N"),
                alt.Tooltip("Bookings:Q")
            ]
        )
        .properties(
            height=330,
            title="Bookings by Hotel"
        )
    )

    with col1:
        st.altair_chart(
            hotel_chart,
            width="stretch"
        )


# ------------------------------------------------------------
# CANCELLATION DISTRIBUTION
# ------------------------------------------------------------

if "is_canceled" in df.columns:

    cancellation_counts = (
        df["is_canceled"]
        .map({
            0: "Not Cancelled",
            1: "Cancelled"
        })
        .value_counts()
        .rename_axis("Status")
        .reset_index(name="Bookings")
    )

    cancellation_chart = (
        alt.Chart(cancellation_counts)
        .mark_arc(
            innerRadius=70,
            outerRadius=125
        )
        .encode(
            theta=alt.Theta(
                "Bookings:Q"
            ),
            color=alt.Color(
                "Status:N",
                scale=alt.Scale(
                    domain=[
                        "Not Cancelled",
                        "Cancelled"
                    ],
                    range=[
                        "#37d69b",
                        "#ff5c70"
                    ]
                ),
                legend=alt.Legend(
                    title=None,
                    orient="bottom"
                )
            ),
            tooltip=[
                alt.Tooltip("Status:N"),
                alt.Tooltip("Bookings:Q")
            ]
        )
        .properties(
            height=330,
            title="Cancellation Distribution"
        )
    )

    with col2:
        st.altair_chart(
            cancellation_chart,
            width="stretch"
        )


# ============================================================
# MONTHLY BOOKING TREND
# ============================================================

if "arrival_date_month" in df.columns:

    st.markdown(
        '<div class="section-title">📅 Monthly Booking Trend</div>',
        unsafe_allow_html=True
    )

    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    monthly = (
        df.groupby("arrival_date_month")
        .size()
        .reindex(month_order)
        .fillna(0)
        .reset_index(name="Bookings")
    )

    monthly_chart = (
        alt.Chart(monthly)
        .mark_line(
            point=alt.OverlayMarkDef(
                filled=True,
                size=70
            ),
            strokeWidth=3
        )
        .encode(
            x=alt.X(
                "arrival_date_month:N",
                sort=month_order,
                title="Arrival Month"
            ),
            y=alt.Y(
                "Bookings:Q",
                title="Number of Bookings"
            ),
            tooltip=[
                alt.Tooltip(
                    "arrival_date_month:N",
                    title="Month"
                ),
                alt.Tooltip(
                    "Bookings:Q",
                    title="Bookings"
                )
            ]
        )
        .properties(
            height=360
        )
    )

    st.altair_chart(
        monthly_chart,
        width="stretch"
    )


# ============================================================
# MARKET SEGMENT + ADR
# ============================================================

st.markdown(
    '<div class="section-title">🎯 Market & Revenue Analysis</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# MARKET SEGMENT
# ------------------------------------------------------------

if "market_segment" in df.columns:

    segment_counts = (
        df["market_segment"]
        .value_counts()
        .rename_axis("Market Segment")
        .reset_index(name="Bookings")
    )

    segment_chart = (
        alt.Chart(segment_counts)
        .mark_bar(
            cornerRadiusEnd=7
        )
        .encode(
            x=alt.X(
                "Bookings:Q",
                title="Number of Bookings"
            ),
            y=alt.Y(
                "Market Segment:N",
                sort="-x",
                title=None
            ),
            color=alt.Color(
                "Bookings:Q",
                scale=alt.Scale(
                    range=[
                        "#315f91",
                        "#4da3ff"
                    ]
                ),
                legend=None
            ),
            tooltip=[
                alt.Tooltip(
                    "Market Segment:N"
                ),
                alt.Tooltip(
                    "Bookings:Q"
                )
            ]
        )
        .properties(
            height=350,
            title="Bookings by Market Segment"
        )
    )

    with col1:
        st.altair_chart(
            segment_chart,
            width="stretch"
        )


# ------------------------------------------------------------
# ADR BY HOTEL
# ------------------------------------------------------------

if "adr" in df.columns and "hotel" in df.columns:

    adr_summary = (
        df.groupby("hotel")["adr"]
        .mean()
        .reset_index()
    )

    adr_chart = (
        alt.Chart(adr_summary)
        .mark_bar(
            cornerRadiusTopLeft=7,
            cornerRadiusTopRight=7,
            size=60
        )
        .encode(
            x=alt.X(
                "hotel:N",
                title=None
            ),
            y=alt.Y(
                "adr:Q",
                title="Average ADR"
            ),
            color=alt.Color(
                "hotel:N",
                scale=alt.Scale(
                    range=[
                        "#9b7cff",
                        "#f5c451"
                    ]
                ),
                legend=None
            ),
            tooltip=[
                alt.Tooltip(
                    "hotel:N",
                    title="Hotel"
                ),
                alt.Tooltip(
                    "adr:Q",
                    title="Average ADR",
                    format=".2f"
                )
            ]
        )
        .properties(
            height=350,
            title="Average Daily Rate by Hotel"
        )
    )

    with col2:
        st.altair_chart(
            adr_chart,
            width="stretch"
        )


# ============================================================
# ADD NEW BOOKING
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">➕ Add New Booking</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="pipeline-banner">
        🔄 <b>Live ETL Flow:</b>
        Booking Input → Validation → Transformation →
        Warehouse → Dashboard
    </div>
    """,
    unsafe_allow_html=True
)


with st.form("booking_form"):

    col1, col2, col3 = st.columns(3)

    # --------------------------------------------------------
    # COLUMN 1
    # --------------------------------------------------------

    with col1:

        hotel = st.selectbox(
            "Hotel",
            ["City Hotel", "Resort Hotel"]
        )

        lead_time = st.number_input(
            "Lead Time",
            min_value=0,
            value=10
        )

        arrival_year = st.number_input(
            "Arrival Year",
            min_value=2015,
            max_value=2030,
            value=2026
        )

    # --------------------------------------------------------
    # COLUMN 2
    # --------------------------------------------------------

    with col2:

        arrival_month = st.selectbox(
            "Arrival Month",
            [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December"
            ]
        )

        arrival_day = st.number_input(
            "Arrival Day",
            min_value=1,
            max_value=31,
            value=15
        )

        adults = st.number_input(
            "Adults",
            min_value=0,
            value=2
        )

    # --------------------------------------------------------
    # COLUMN 3
    # --------------------------------------------------------

    with col3:

        children = st.number_input(
            "Children",
            min_value=0,
            value=0
        )

        babies = st.number_input(
            "Babies",
            min_value=0,
            value=0
        )

        adr = st.number_input(
            "ADR",
            min_value=0.0,
            value=100.0
        )

    submitted = st.form_submit_button(
        "🚀 Process Booking"
    )


# ============================================================
# PROCESS BOOKING
# ============================================================

if submitted:

    new_booking = {

        "hotel": hotel,

        "lead_time": lead_time,

        "arrival_date_year": arrival_year,

        "arrival_date_month": arrival_month,

        "arrival_date_day_of_month": arrival_day,

        "adults": adults,

        "children": children,

        "babies": babies,

        "adr": adr,

        "is_canceled": 0,

        "market_segment": "Direct"
    }

    try:

        from local_pipeline import run_pipeline

        success, message = run_pipeline(
            new_booking
        )

        if success:

            st.session_state.pipeline_message = (
                "✅ Booking successfully processed through "
                "the ETL pipeline! Dashboard updated."
            )

            load_data.clear()

            st.rerun()

        else:

            st.error(
                f"❌ Pipeline rejected the booking: {message}"
            )

    except Exception as e:

        st.error(
            f"❌ Pipeline error: {e}"
        )


# ============================================================
# PROCESSED DATA
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🗃️ Processed Booking Data</div>',
    unsafe_allow_html=True
)

st.dataframe(
    df.head(20),
    width="stretch",
    height=450
)

st.caption(
    f"Showing first 20 records out of "
    f"{len(df):,} processed records."
)