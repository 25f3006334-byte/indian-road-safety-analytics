from io import BytesIO

import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Indian Road Safety Analytics",
    page_icon="🇮🇳",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

    :root {
        --canvas: #101817;
        --surface: #172321;
        --surface-raised: #1d2d2a;
        --border: #30433e;
        --ink: #eef5ef;
        --muted: #a2b4aa;
        --teal: #67d5be;
        --saffron: #f0bd62;
        --coral: #e99178;
    }

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
        letter-spacing: 0;
    }

    .stApp {
        color: var(--ink);
        background-color: var(--canvas);
        background-image: repeating-linear-gradient(
            135deg,
            rgba(103, 213, 190, 0.018) 0,
            rgba(103, 213, 190, 0.018) 1px,
            transparent 1px,
            transparent 14px
        );
    }

    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stAppViewContainer"] { background: transparent; }
    [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {
        display: none;
    }

    h1, h2, h3 { color: var(--ink); letter-spacing: 0; }
    h1 { font-weight: 700; }
    h2, h3 { font-weight: 600; }
    p, li { color: #d2ddd5; }
    [data-testid="stCaptionContainer"] { color: var(--muted); }

    .home-kicker {
        margin: 10px 0 8px;
        color: var(--teal);
        font-family: 'IBM Plex Mono', monospace;
        font-size: .76rem;
        text-transform: uppercase;
    }
    .home-title {
        max-width: 820px;
        margin: 0;
        color: #f4f5e9;
        font-size: 2.65rem;
        font-weight: 700;
        line-height: 1.08;
    }
    .home-intro {
        max-width: 790px;
        margin: 14px 0 26px;
        color: #adbbb2;
        font-size: 1rem;
        line-height: 1.65;
    }
    .section-heading {
        margin: 30px 0 5px;
        color: var(--ink);
        font-size: 1.25rem;
        font-weight: 600;
    }
    .section-note { margin: 0 0 14px; color: var(--muted); }

    .question-card {
        min-height: 124px;
        padding: 16px;
        border: 1px solid var(--border);
        border-top: 2px solid var(--teal);
        background: rgba(23, 35, 33, .94);
        box-shadow: 0 10px 30px rgba(0, 0, 0, .12);
        transition: border-color .18s ease, transform .18s ease;
    }
    .question-card:hover {
        transform: translateY(-2px);
        border-color: #52756b;
    }
    .question-icon { font-size: 1.35rem; }
    .question-title {
        margin-top: 6px;
        color: var(--saffron);
        font-weight: 700;
    }
    .question-text {
        margin-top: 4px;
        color: var(--muted);
        font-size: .82rem;
        line-height: 1.5;
    }

    .module-card {
        min-height: 95px;
        margin-bottom: 10px;
        padding: 15px;
        border: 1px solid var(--border);
        background: rgba(23, 35, 33, .92);
        box-shadow: 0 8px 24px rgba(0, 0, 0, .10);
        transition: border-color .18s ease, background-color .18s ease;
    }
    .module-card:hover {
        border-color: var(--teal);
        background-color: var(--surface-raised);
    }
    .module-name { color: var(--ink); font-weight: 600; }
    .module-desc {
        margin-top: 5px;
        color: var(--muted);
        font-size: .82rem;
        line-height: 1.45;
    }

    [data-testid="stMetric"] {
        padding: 14px 16px;
        border: 1px solid var(--border);
        border-top: 2px solid var(--teal);
        border-radius: 5px;
        background: var(--surface);
    }
    [data-testid="stMetricLabel"] { color: var(--muted) !important; }
    [data-testid="stMetricValue"] { color: var(--ink) !important; font-weight: 700 !important; }

    div[data-testid="stFileUploader"] {
        padding: 6px;
        border: 1px dashed #52756b;
        border-radius: 5px;
        background: rgba(23, 35, 33, .8);
    }
    .stButton > button, .stDownloadButton > button {
        border: 1px solid #52756b;
        border-radius: 4px;
        background: #213a34;
        color: var(--ink);
        font-weight: 600;
        transition: background-color .18s ease, border-color .18s ease;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        border-color: var(--teal);
        background: #29483f;
        color: white;
    }
    [data-testid="stDataFrame"] {
        overflow: hidden;
        border: 1px solid var(--border);
        border-radius: 5px;
    }
    [data-testid="stExpander"] {
        border: 1px solid var(--border);
        border-radius: 5px;
        background: var(--surface);
    }
    .stAlert { border-radius: 5px; }
    .stSelectbox > div > div, .stMultiSelect > div > div { border-radius: 4px; }
    .stSlider { padding-top: 5px; }

    .insight {
        min-height: 46px;
        padding: 12px 14px;
        border-radius: 4px;
        border-left: 3px solid var(--saffron);
        background: var(--surface);
        color: #d2ddd5;
        line-height: 1.45;
        box-shadow: 0 8px 24px rgba(0, 0, 0, .10);
    }
    .footer {
        margin-top: 34px;
        padding: 18px 0 8px;
        border-top: 1px solid var(--border);
        color: #87998f;
        font-family: 'IBM Plex Mono', monospace;
        font-size: .7rem;
        text-align: center;
    }

    .hero-panel {
        position: relative;
        display: flex;
        justify-content: space-between;
        gap: 28px;
        min-height: 260px;
        margin: 8px 0 18px;
        padding: 30px 32px;
        overflow: hidden;
        border: 1px solid #35534b;
        border-radius: 14px;
        background:
            linear-gradient(90deg, rgba(16, 33, 30, .97) 0%, rgba(16, 33, 30, .93) 57%, rgba(22, 42, 38, .88) 100%),
            repeating-linear-gradient(135deg, rgba(103, 213, 190, .08) 0 1px, transparent 1px 16px);
        box-shadow: 0 20px 48px rgba(0, 0, 0, .23);
    }
    .hero-content { position: relative; z-index: 1; max-width: 760px; }
    .hero-badge, .card-eyebrow {
        color: var(--teal);
        font-family: 'IBM Plex Mono', monospace;
        font-size: .7rem;
        font-weight: 500;
        letter-spacing: 0;
        text-transform: uppercase;
    }
    .hero-panel h1 {
        margin: 12px 0;
        color: #f7fbf5;
        font-size: 2.8rem;
        line-height: 1.05;
    }
    .hero-subtitle {
        max-width: 700px;
        margin: 0;
        color: #c1d0c7;
        font-size: 1rem;
        line-height: 1.65;
    }
    .hero-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 20px; }
    .hero-tags span {
        padding: 6px 10px;
        border: 1px solid #35564d;
        border-radius: 4px;
        background: rgba(11, 25, 22, .48);
        color: #dbe8df;
        font-size: .75rem;
    }
    .hero-side {
        position: relative;
        z-index: 1;
        align-self: center;
        width: 230px;
        flex: 0 0 230px;
        padding: 20px;
        border: 1px solid rgba(103, 213, 190, .32);
        border-radius: 8px;
        background: rgba(7, 20, 18, .58);
    }
    .hero-side-label { color: var(--saffron); font: 500 .67rem 'IBM Plex Mono', monospace; }
    .hero-side-title { margin-top: 10px; color: #eef5ef; font-size: 1.05rem; font-weight: 700; line-height: 1.35; }
    .hero-side-text { margin-top: 9px; color: #9fb1a7; font-size: .78rem; line-height: 1.55; }
    .snapshot-card {
        min-height: 106px;
        padding: 16px 18px;
        border: 1px solid #304b44;
        border-radius: 7px;
        background: linear-gradient(145deg, rgba(28, 45, 41, .96), rgba(20, 34, 31, .96));
        box-shadow: 0 10px 25px rgba(0, 0, 0, .14);
        transition: transform .18s ease, border-color .18s ease;
    }
    .snapshot-card:hover { transform: translateY(-2px); border-color: var(--teal); }
    .snapshot-value { color: #f5faf4; font-size: 1.55rem; font-weight: 700; }
    .snapshot-label { margin-top: 3px; color: var(--teal); font-size: .8rem; font-weight: 600; }
    .snapshot-caption { margin-top: 5px; color: #8fa39a; font-size: .69rem; }
    .objective-card, .source-card {
        height: 100%;
        padding: 20px;
        border: 1px solid #304b44;
        border-radius: 8px;
        background: linear-gradient(145deg, rgba(27, 43, 39, .98), rgba(20, 33, 30, .98));
        box-shadow: 0 10px 26px rgba(0, 0, 0, .14);
    }
    .objective-card { margin-top: 28px; }
    .objective-card h3, .source-card h3 { margin: 8px 0; color: #eef5ef; font-size: 1rem; }
    .objective-card p, .source-card p { margin: 0; color: #aebeb5; font-size: .8rem; line-height: 1.6; }
    .source-card a { display: inline-block; margin-top: 12px; color: var(--teal); text-decoration: none; font-size: .78rem; font-weight: 600; }
    .source-card a:hover { text-decoration: underline; }
    .source-highlight { border-color: rgba(240, 189, 98, .32); }
    .source-highlight .card-eyebrow { color: var(--saffron); }
    .compact-heading { margin-top: 28px; }
    .question-card-modern { position: relative; min-height: 136px; }
    .question-number { position: absolute; top: 10px; right: 12px; color: rgba(103, 213, 190, .42); font: 500 .66rem 'IBM Plex Mono', monospace; }
    .module-card-modern { min-height: 132px; border-radius: 7px; }
    .module-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
    .module-number { color: #82988d; font: 500 .68rem 'IBM Plex Mono', monospace; }
    .module-icon { font-size: 1.25rem; }
    .workflow-card {
        min-height: 118px;
        padding: 13px 9px;
        border: 1px solid #2f4942;
        border-radius: 7px;
        background: #172623;
        text-align: center;
        transition: transform .18s ease, border-color .18s ease;
    }
    .workflow-card:hover { transform: translateY(-2px); border-color: var(--teal); }
    .workflow-number { color: var(--saffron); font: 500 .65rem 'IBM Plex Mono', monospace; }
    .workflow-title { margin-top: 7px; color: #e9f2eb; font-size: .7rem; font-weight: 700; }
    .workflow-desc { margin-top: 7px; color: #91a69b; font-size: .64rem; line-height: 1.4; }
    .capability-card {
        display: flex;
        gap: 11px;
        min-height: 78px;
        margin-bottom: 10px;
        padding: 13px;
        border: 1px solid #2e4741;
        border-radius: 6px;
        background: rgba(23, 35, 33, .88);
    }
    .capability-icon { font-size: 1.1rem; }
    .capability-card b { color: #eaf3ec; font-size: .78rem; }
    .capability-text { margin-top: 4px; color: #8fa39a; font-size: .69rem; line-height: 1.4; }
    .insight-large { padding: 15px 17px; border-radius: 7px; }

    @media (max-width: 900px) {
        .home-title { font-size: 2.1rem; }
        .question-card { min-height: 110px; }
        .hero-panel { flex-direction: column; min-height: 0; padding: 24px 20px; }
        .hero-panel h1 { font-size: 2.1rem; }
        .hero-side { width: auto; flex-basis: auto; }
    }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { transition-duration: .01ms !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

PAGE_ROUTES = {
    "home": "🏠 Home Dashboard",
    "national": "National Analysis",
    "state-ut": "State/UT Analysis",
    "violations": "Cause / Violation Analysis",
    "collision": "Collision Type Analysis",
    "road-users": "Road User Analysis",
    "vehicle-interactions": "Vehicle Interaction Analysis",
    "risk-simulation": "Risk & Simulation Analysis",
}

page_key = st.query_params.get("view", "home")
if page_key not in PAGE_ROUTES:
    page_key = "home"
page = PAGE_ROUTES[page_key]


def navigate_to_page(route_key):
    st.query_params["view"] = route_key


if page != "🏠 Home Dashboard":
    st.button(
        "← Home dashboard",
        on_click=navigate_to_page,
        args=("home",),
        key="return_home",
    )


def read_uploaded_file(uploaded_file):
    file_bytes = uploaded_file.getvalue()

    try:
        if uploaded_file.name.lower().endswith(".csv"):
            df = None

            for encoding in ["utf-8-sig", "utf-8", "cp1252", "latin-1"]:
                try:
                    df = pd.read_csv(
                        BytesIO(file_bytes),
                        encoding=encoding,
                        sep=None,
                        engine="python",
                    )
                    break
                except Exception:
                    pass

            if df is None:
                st.error("Could not read this CSV file.")
                st.stop()
        else:
            workbook = pd.ExcelFile(BytesIO(file_bytes))
            sheet = st.selectbox("Choose worksheet", workbook.sheet_names)
            df = pd.read_excel(workbook, sheet_name=sheet)

        return df

    except Exception as error:
        st.error(f"Could not read the file: {error}")
        st.stop()


def remove_index_columns(df):
    df.columns = [str(column).strip() for column in df.columns]
    return df.loc[
        :,
        [
            column
            for column in df.columns
            if column.strip().lower() != "index"
            and not column.strip().lower().startswith("unnamed:")
        ],
    ]


def show_insight(title, message):
    st.markdown(
        f"<div class='insight'><b>{title}</b> {message}</div>",
        unsafe_allow_html=True,
    )


def safe_pct_change(current, previous):
    if previous is None or previous == 0 or pd.isna(previous):
        return None
    return (current - previous) / previous * 100


def render_plotly(fig, height=420):
    fig.update_layout(
        height=height,
        margin={"l": 10, "r": 10, "t": 56, "b": 12},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#dce8df", "family": "IBM Plex Sans, sans-serif"},
        title={"font": {"size": 17}},
        hoverlabel={"bgcolor": "#1d2d2a", "font_color": "#eef5ef"},
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(150,180,170,.12)")
    fig.update_yaxes(showgrid=False)
    st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})


def add_plotly_bar(data, category, value, title, horizontal=True):
    chart_data = data[[category, value]].dropna().copy()
    chart_data = chart_data.sort_values(value, ascending=horizontal)
    fig = px.bar(
        chart_data,
        x=value if horizontal else category,
        y=category if horizontal else value,
        orientation="h" if horizontal else "v",
        title=title,
        template="plotly_dark",
        color_discrete_sequence=["#67d5be"],
        hover_data={value: ":,.0f"},
    )
    render_plotly(fig, height=max(350, min(680, 120 + len(chart_data) * 30)))


def add_plotly_line(data, x, y_columns, title):
    fig = px.line(
        data,
        x=x,
        y=y_columns,
        markers=True,
        title=title,
        template="plotly_dark",
        color_discrete_sequence=["#67d5be", "#f0bd62", "#e99178"],
    )
    fig.update_layout(hovermode="x unified")
    render_plotly(fig, height=390)


# ============================================================
# HOME DASHBOARD
# ============================================================

if page == "🏠 Home Dashboard":
    st.markdown(
        """
        <div class="hero-panel">
            <div class="hero-content">
                <div class="hero-badge">🇮🇳 ECE-181 · CA2 PROJECT · PYTHON DATA ANALYTICS</div>
                <h1>Indian Road Safety Analytics</h1>
                <p class="hero-subtitle">
                    A connected analytical view of recorded road-accident data across India —
                    from national trends and State/UT patterns to violations, collisions,
                    road-user fatalities, vehicle interactions and hypothetical simulations.
                </p>
                <div class="hero-tags">
                    <span>📊 Data Analysis</span><span>🗺️ India-wide</span>
                    <span>🔎 Interactive</span><span>🧪 What-if Simulation</span>
                </div>
            </div>
            <div class="hero-side">
                <div class="hero-side-label">PROJECT FOCUS</div>
                <div class="hero-side-title">WHERE · WHAT · HOW · WHO</div>
                <div class="hero-side-text">Understand recorded patterns before drawing conclusions.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    snapshot = st.columns(4)
    snapshot_data = [
        ("7", "Analytical Layers", "Connected analysis modules"),
        ("India", "Primary Geography", "National + State/UT view"),
        ("2024", "Latest Dataset", "Current project data year"),
        ("What-if", "Simulation", "Hypothetical scenarios"),
    ]
    for column, (value, label, caption) in zip(snapshot, snapshot_data):
        with column:
            st.markdown(
                f"<div class='snapshot-card'><div class='snapshot-value'>{value}</div>"
                f"<div class='snapshot-label'>{label}</div><div class='snapshot-caption'>{caption}</div></div>",
                unsafe_allow_html=True,
            )

    left, right = st.columns([0.9, 1.8])
    with left:
        st.markdown(
            """
            <div class="objective-card">
                <div class="card-eyebrow">🎯 PROJECT OBJECTIVE</div>
                <h3>Turn recorded data into understandable evidence.</h3>
                <p>
                    Analyze Indian road-accident datasets, identify patterns across multiple
                    dimensions, visualize findings and demonstrate how hypothetical changes
                    affect recorded counts.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            "<div class='section-heading compact-heading'>The questions behind the analysis</div>"
            "<div class='section-note'>Each view is limited to what its source dataset actually records.</div>",
            unsafe_allow_html=True,
        )
        question_cards = [
            ("01", "🌐", "HOW BIG?", "What is the recorded national accident, fatality and injury burden?"),
            ("02", "🗺️", "WHERE?", "Which States/UTs have the largest recorded counts and changes?"),
            ("03", "🚦", "WHAT & HOW?", "What violation, collision and vehicle-interaction patterns are recorded?"),
            ("04", "🚶", "WHO?", "Which road-user categories account for recorded fatalities?"),
        ]
        for row_start in range(0, len(question_cards), 2):
            question_columns = st.columns(2)
            for column, (number, icon, title, description) in zip(
                question_columns, question_cards[row_start:row_start + 2]
            ):
                with column:
                    st.markdown(
                        f"<div class='question-card question-card-modern'><div class='question-number'>{number}</div>"
                        f"<div class='question-icon'>{icon}</div><div class='question-title'>{title}</div>"
                        f"<div class='question-text'>{description}</div></div>",
                        unsafe_allow_html=True,
                    )

    st.markdown(
        "<div class='section-heading'>Seven analytical layers</div>"
        "<div class='section-note'>Move from the national picture to detailed patterns and finally to a project-created simulation layer.</div>",
        unsafe_allow_html=True,
    )
    modules = [
        ("01", "🇮🇳", "National Analysis", "2020–2024 national accident, fatality and injury trends.", "national"),
        ("02", "🗺️", "State/UT Analysis", "Recorded counts, rankings, changes and individual state trends.", "state-ut"),
        ("03", "🚦", "Cause / Violation", "Accidents associated with recorded traffic-violation categories.", "violations"),
        ("04", "💥", "Collision Type", "Recorded accident patterns classified by collision type.", "collision"),
        ("05", "🚶", "Road User", "Recorded fatalities across road-user categories.", "road-users"),
        ("06", "🚗", "Vehicle Interaction", "Victim-vehicle × crime-vehicle interaction patterns.", "vehicle-interactions"),
        ("07", "📈", "Risk & Simulation", "Custom analytical indicator and hypothetical what-if scenarios.", "risk-simulation"),
    ]
    for row_start in range(0, len(modules), 3):
        columns = st.columns(3)
        for column, module in zip(columns, modules[row_start:row_start + 3]):
            number, icon, name, description, route_key = module
            with column:
                st.markdown(
                    f"<div class='module-card module-card-modern'>"
                    f"<div class='module-top'><span class='module-number'>{number}</span><span class='module-icon'>{icon}</span></div>"
                    f"<div class='module-name'>{name}</div><div class='module-desc'>{description}</div></div>",
                    unsafe_allow_html=True,
                )
                st.button(
                    "Explore analysis →",
                    on_click=navigate_to_page,
                    args=(route_key,),
                    key=f"open_{route_key}",
                    use_container_width=True,
                )

    st.markdown(
        "<div class='section-heading'>Project workflow</div>"
        "<div class='section-note'>One connected path from dataset upload to interpreted findings.</div>",
        unsafe_allow_html=True,
    )
    workflow = [
        ("01", "DATA", "Upload source files"),
        ("02", "CLEAN", "Validate and prepare"),
        ("03", "ANALYZE", "Find patterns"),
        ("04", "VISUALIZE", "Compare results"),
        ("05", "INDICATOR", "Custom project measure"),
        ("06", "SIMULATE", "Hypothetical scenarios"),
        ("07", "INTERPRET", "Review limitations"),
    ]
    workflow_columns = st.columns(7)
    for column, (number, title, description) in zip(workflow_columns, workflow):
        with column:
            st.markdown(
                f"<div class='workflow-card'><div class='workflow-number'>{number}</div>"
                f"<div class='workflow-title'>{title}</div><div class='workflow-desc'>{description}</div></div>",
                unsafe_allow_html=True,
            )

    capabilities = [
        ("📁", "Upload CSV / Excel", "Each analysis accepts its compatible dataset."),
        ("🧹", "Clean & validate", "Columns and numeric values are checked."),
        ("📊", "Interactive charts", "Explore trends, rankings and comparisons."),
        ("🔍", "Drill down", "Select a State/UT or data category."),
        ("🚗", "Vehicle matrix", "Compare recorded vehicle interactions."),
        ("🧪", "What-if scenarios", "Explore hypothetical numerical reductions."),
    ]
    st.markdown("<div class='section-heading'>What the dashboard can do</div>", unsafe_allow_html=True)
    for row_start in range(0, len(capabilities), 3):
        capability_columns = st.columns(3)
        for column, (icon, title, description) in zip(
            capability_columns, capabilities[row_start:row_start + 3]
        ):
            with column:
                st.markdown(
                    f"<div class='capability-card'><span class='capability-icon'>{icon}</span>"
                    f"<div><b>{title}</b><div class='capability-text'>{description}</div></div></div>",
                    unsafe_allow_html=True,
                )

    st.markdown(
        "<div class='section-heading'>Interpretation & limitations</div>"
        "<div class='insight insight-large'><b>Important:</b> this application analyzes recorded road-accident data. "
        "Its analytical indicator is a project-created measure, not an official government risk rating or accident probability. "
        "The what-if simulations are hypothetical numerical scenarios, not forecasts. Higher recorded counts should not be treated "
        "as proof of higher true accident probability without exposure data such as traffic volume, population, road length or travel distance.</div>",
        unsafe_allow_html=True,
    )

    source_left, source_right = st.columns([2.2, 1])
    with source_left:
        st.markdown(
            "<div class='source-card'><div class='card-eyebrow'>📚 DATA SOURCE</div>"
            "<h3>Road Accidents in India 2024</h3>"
            "<p>Datasets used in this project were obtained from OpenCity's Road Accidents in India 2024 collection.</p>"
            "<a href='https://data.opencity.in/dataset/road-accidents-in-india-2024' target='_blank'>Open dataset collection →</a></div>",
            unsafe_allow_html=True,
        )
    with source_right:
        st.markdown(
            "<div class='source-card source-highlight'><div class='card-eyebrow'>🚀 READY TO EXPLORE?</div>"
            "<h3>Start with National Analysis</h3>"
            "<p>Upload the annual dataset and follow the analysis from national trends to simulations.</p></div>",
            unsafe_allow_html=True,
        )
        st.button(
            "Open National Analysis →",
            on_click=navigate_to_page,
            args=("national",),
            key="home_national_cta",
            use_container_width=True,
        )


# ============================================================
# NATIONAL ANALYSIS
# ============================================================

elif page == "National Analysis":
    st.title("🇮🇳 Indian Road Safety Analytics")
    st.caption("National annual trends | 2020–2024")

    uploaded = st.file_uploader(
        "Upload the annual road-accidents CSV or Excel file",
        type=["csv", "xlsx", "xls"],
        key="national_file",
    )

    if uploaded is None:
        st.info("Upload the annual dataset to view the analysis.")
        st.stop()

    df = remove_index_columns(read_uploaded_file(uploaded))

    if len(df.columns) != 7:
        st.error(
            f"Expected 7 data columns after removing the index column, "
            f"but found {len(df.columns)}."
        )
        st.write("Columns found:", list(df.columns))
        st.stop()

    df.columns = [
        "Year",
        "Accidents",
        "Accident change (%)",
        "Fatalities",
        "Fatality change (%)",
        "Persons injured",
        "Injury change (%)",
    ]

    count_columns = ["Accidents", "Fatalities", "Persons injured"]
    for column in count_columns:
        df[column] = pd.to_numeric(
            df[column].astype(str).str.replace(",", "", regex=False),
            errors="coerce",
        )

    percent_columns = [
        "Accident change (%)",
        "Fatality change (%)",
        "Injury change (%)",
    ]
    for column in percent_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"] + count_columns).sort_values("Year")

    if df.empty:
        st.error("No usable annual data rows were found.")
        st.stop()

    df["Year"] = df["Year"].astype(int)
    latest = df.iloc[-1]

    st.subheader(f"India overview: {int(latest['Year'])}")
    a, b, c = st.columns(3)
    a.metric("Accidents", f"{int(latest['Accidents']):,}")
    b.metric("Fatalities", f"{int(latest['Fatalities']):,}")
    c.metric("Persons injured", f"{int(latest['Persons injured']):,}")

    if len(df) >= 2:
        previous = df.iloc[-2]
        accident_change = safe_pct_change(latest["Accidents"], previous["Accidents"])
        fatality_change = safe_pct_change(latest["Fatalities"], previous["Fatalities"])
        accident_text = f"{accident_change:.2f}%" if accident_change is not None else "N/A"
        fatality_text = f"{fatality_change:.2f}%" if fatality_change is not None else "N/A"
        show_insight(
            "Key insight ·",
            f"From {int(previous['Year'])} to {int(latest['Year'])}, recorded accidents changed by "
            f"{accident_text} and fatalities changed by {fatality_text}.",
        )

    st.subheader("Annual trends")
    left, right = st.columns(2)
    with left:
        st.markdown("**Recorded accidents**")
        add_plotly_line(df, "Year", ["Accidents"], "National accident trend")
    with right:
        st.markdown("**Fatalities and persons injured**")
        add_plotly_line(
            df,
            "Year",
            ["Fatalities", "Persons injured"],
            "Fatalities and injuries trend",
        )

    st.subheader("Reported burden per 100 recorded accidents")
    rates = df[["Year"]].copy()
    rates["Fatalities per 100 accidents"] = (
        df["Fatalities"] / df["Accidents"] * 100
    )
    rates["Injuries per 100 accidents"] = (
        df["Persons injured"] / df["Accidents"] * 100
    )
    add_plotly_line(
        rates,
        "Year",
        ["Fatalities per 100 accidents", "Injuries per 100 accidents"],
        "Reported burden per 100 accidents",
    )

    st.subheader("Year-over-year changes")
    st.dataframe(
        df[
            [
                "Year",
                "Accident change (%)",
                "Fatality change (%)",
                "Injury change (%)",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Hypothetical fatality-reduction scenario")
    st.write(
        "This scenario applies a chosen reduction percentage to the latest "
        "year's reported fatalities. It is an illustration, not a prediction "
        "or estimate of the effect of a specific intervention."
    )
    reduction = st.slider(
        "Hypothetical reduction (%)",
        min_value=5,
        max_value=30,
        value=10,
        step=5,
        key="national_reduction",
    )
    estimated_avoided = round(int(latest["Fatalities"]) * reduction / 100)
    st.metric("Illustrative fatalities avoided", f"{estimated_avoided:,}")
    st.caption(
        f"Baseline: {int(latest['Fatalities']):,} reported fatalities "
        f"in {int(latest['Year'])}."
    )

    st.subheader("Data and source")
    st.write("Annual national totals for accidents, fatalities, and injuries.")
    st.markdown(
        "[Dataset page: OpenCity — Road Accidents in India 2024]"
        "(https://data.opencity.in/dataset/road-accidents-in-india-2024)"
    )
    st.caption(
        "Original data publisher/source still needs verification from the "
        "dataset documentation."
    )

# ============================================================
# STATE / UT ANALYSIS
# ============================================================

elif page == "State/UT Analysis":
    st.title("🗺️ State/UT Road Accident Analysis")
    st.caption("State-wise accident comparison | 2020–2024")

    uploaded = st.file_uploader(
        "Upload the State-wise Road Accidents 2020–2024 CSV",
        type=["csv", "xlsx", "xls"],
        key="state_file",
    )

    if uploaded is None:
        st.info("Upload the State-wise Road Accidents 2020–2024 CSV to begin.")
        st.stop()

    df = remove_index_columns(read_uploaded_file(uploaded))

    expected_columns = [
        "Sl No",
        "State",
        "2020 Accidents",
        "2021 Accidents",
        "2022 Accidents",
        "2023 Accidents",
        "2024 Accidents",
        "Change from 2023 to 2024",
        "% change from 2023 to 2024",
        "2020 Ranking",
        "2021 Ranking",
        "2022 Ranking",
        "2023 Ranking",
        "2024 Ranking",
    ]
    missing_columns = [column for column in expected_columns if column not in df.columns]

    if missing_columns:
        st.error("This does not appear to be the expected State-wise Road Accidents dataset.")
        st.write("Missing columns:", missing_columns)
        st.write("Columns found:", list(df.columns))
        st.stop()

    accident_columns = [
        "2020 Accidents",
        "2021 Accidents",
        "2022 Accidents",
        "2023 Accidents",
        "2024 Accidents",
    ]
    for column in accident_columns:
        df[column] = pd.to_numeric(
            df[column].astype(str).str.replace(",", "", regex=False),
            errors="coerce",
        )

    df["Change from 2023 to 2024"] = pd.to_numeric(
        df["Change from 2023 to 2024"], errors="coerce"
    )
    df["% change from 2023 to 2024"] = pd.to_numeric(
        df["% change from 2023 to 2024"], errors="coerce"
    )
    ranking_columns = [
        "2020 Ranking",
        "2021 Ranking",
        "2022 Ranking",
        "2023 Ranking",
        "2024 Ranking",
    ]
    for column in ranking_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["State"] = df["State"].astype(str).str.strip()
    df = df[
        df["State"].ne("")
        & df["State"].str.lower().ne("nan")
        & df["2024 Accidents"].notna()
    ]

    if df.empty:
        st.error("No usable State/UT rows with 2024 accident data were found.")
        st.stop()

    st.subheader("2024 State/UT accident overview")
    total_2024 = df["2024 Accidents"].sum()
    states_count = df["State"].nunique()
    col1, col2 = st.columns(2)
    col1.metric("States/UTs in dataset", states_count)
    col2.metric("Total recorded accidents in 2024", f"{int(total_2024):,}")

    st.subheader("States/UTs by recorded accidents in 2024")
    top_states = (
        df[["State", "2024 Accidents"]]
        .sort_values("2024 Accidents", ascending=False)
        .head(10)
    )
    add_plotly_bar(
        top_states,
        "State",
        "2024 Accidents",
        "Top 10 States/UTs by recorded accidents in 2024",
    )

    st.subheader("State-wise accident data")
    display_columns = [
        "State",
        "2020 Accidents",
        "2021 Accidents",
        "2022 Accidents",
        "2023 Accidents",
        "2024 Accidents",
        "Change from 2023 to 2024",
        "% change from 2023 to 2024",
        "2024 Ranking",
    ]
    top_state = top_states.iloc[0]
    share = top_state["2024 Accidents"] / total_2024 * 100 if total_2024 else 0
    show_insight(
        "Key insight ·",
        f"{top_state['State']} has the largest recorded accident count in 2024 in this dataset "
        f"({int(top_state['2024 Accidents']):,}), about {share:.1f}% of its recorded total.",
    )
    st.dataframe(
        df[display_columns].sort_values("2024 Accidents", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Individual State/UT trend")
    selected_state = st.selectbox(
        "Choose a State/UT", sorted(df["State"].dropna().unique())
    )
    selected = df[df["State"] == selected_state].iloc[0]
    state_trend = pd.DataFrame(
        {
            "Year": [2020, 2021, 2022, 2023, 2024],
            "Accidents": [selected[column] for column in accident_columns],
        }
    )
    add_plotly_line(state_trend, "Year", ["Accidents"], f"Recorded accidents · {selected_state}")

    a, b, c = st.columns(3)
    a.metric("2024 accidents", f"{int(selected['2024 Accidents']):,}")
    ranking = selected["2024 Ranking"]
    b.metric("2024 ranking", f"{int(ranking)}" if pd.notna(ranking) else "N/A")
    percentage = selected["% change from 2023 to 2024"]
    c.metric("Change from 2023", f"{percentage:.2f}%" if pd.notna(percentage) else "N/A")

    st.subheader("Change in recorded accidents: 2023 → 2024")
    change_data = (
        df[["State", "% change from 2023 to 2024"]]
        .dropna()
        .sort_values("% change from 2023 to 2024", ascending=False)
    )
    if change_data.empty:
        st.info("No usable 2023–2024 percentage-change values were found.")
    else:
        add_plotly_bar(
            change_data,
            "State",
            "% change from 2023 to 2024",
            "2023 to 2024 change by State/UT",
        )

    st.info(
        "Interpretation note: a higher number of recorded accidents does not "
        "by itself mean that a State/UT has a higher accident risk. Traffic "
        "volume, population, road length, vehicle population and exposure "
        "would also be needed for a normalized risk comparison."
    )

    st.subheader("Data source")
    st.write("State-wise accident data for 2020–2024.")
    st.markdown(
        "[OpenCity — Road Accidents in India 2024]"
        "(https://data.opencity.in/dataset/road-accidents-in-india-2024)"
    )
    st.caption(
        "The dataset is based on road-accident statistics published by MoRTH. "
        "Verify the dataset documentation for the exact original source and definitions."
    )

# ============================================================
# CAUSE / VIOLATION ANALYSIS
# ============================================================

elif page == "Cause / Violation Analysis":
    st.title("🚦 Cause & Traffic Violation Analysis")
    st.caption("Road accidents by type of traffic violation | 2023–2024")

    uploaded = st.file_uploader(
        "Upload the Road Accidents by Type of Violation CSV",
        type=["csv", "xlsx", "xls"],
        key="violation_file",
    )

    if uploaded is None:
        st.info(
            "Upload the Road Accidents by Type of Violation CSV to begin."
        )
        st.stop()

    df = remove_index_columns(read_uploaded_file(uploaded))

    expected_columns = [
        "Category",
        "2023-Accidents",
        "2023-Killed",
        "2023-injured",
        "2024-Accidents",
        "2024-Killed",
        "2024-injured",
        "%Change-Accidents",
        "%Change-killed",
        "%Change-Injured",
    ]
    missing_columns = [
        column for column in expected_columns if column not in df.columns
    ]

    if missing_columns:
        st.error(
            "This does not appear to be the expected traffic-violation dataset."
        )
        st.write("Missing columns:", missing_columns)
        st.write("Columns found:", list(df.columns))
        st.stop()

    df["Category"] = df["Category"].astype("string").str.strip()
    df = df.dropna(subset=["Category"])
    df = df[df["Category"].ne("")].copy()

    numeric_columns = expected_columns[1:]
    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("%", "", regex=False),
            errors="coerce",
        )

    for word in ["total", "% share", "percentage share"]:
        df = df[
            ~df["Category"].str.lower().str.contains(word, na=False)
        ]

    df = df.dropna(subset=["2024-Accidents"])
    if df.empty:
        st.error("No usable traffic-violation category rows were found.")
        st.stop()

    st.subheader("2024 traffic-violation overview")
    total_accidents = df["2024-Accidents"].sum()
    total_killed = df["2024-Killed"].sum()
    total_injured = df["2024-injured"].sum()
    col1, col2, col3 = st.columns(3)
    col1.metric("Recorded accidents", f"{int(total_accidents):,}")
    col2.metric("People killed", f"{int(total_killed):,}")
    col3.metric("People injured", f"{int(total_injured):,}")

    st.subheader("Recorded accidents by traffic violation")
    accident_chart = df[["Category", "2024-Accidents"]].sort_values(
        "2024-Accidents", ascending=False
    )
    leading_violation = accident_chart.iloc[0]
    show_insight(
        "Key insight ·",
        f"{leading_violation['Category']} has the highest recorded 2024 accident count "
        f"({int(leading_violation['2024-Accidents']):,}) in this dataset.",
    )
    add_plotly_bar(accident_chart, "Category", "2024-Accidents", "Accidents by recorded violation")

    st.subheader("Fatalities by traffic violation")
    killed_chart = df[["Category", "2024-Killed"]].sort_values(
        "2024-Killed", ascending=False
    )
    add_plotly_bar(killed_chart, "Category", "2024-Killed", "Fatalities by recorded violation")

    st.subheader("Persons injured by traffic violation")
    injured_chart = df[["Category", "2024-injured"]].sort_values(
        "2024-injured", ascending=False
    )
    add_plotly_bar(injured_chart, "Category", "2024-injured", "People injured by recorded violation")

    st.subheader("2023 vs 2024 accident comparison")
    comparison = df[
        ["Category", "2023-Accidents", "2024-Accidents"]
    ].set_index("Category")
    comparison_chart = px.bar(
        comparison.reset_index(),
        x="Category",
        y=["2023-Accidents", "2024-Accidents"],
        barmode="group",
        title="Recorded accidents by violation · 2023 vs 2024",
        template="plotly_dark",
        color_discrete_sequence=["#f0bd62", "#67d5be"],
    )
    render_plotly(comparison_chart, height=460)

    st.subheader("Change in recorded accidents: 2023 → 2024")
    change_chart = (
        df[["Category", "%Change-Accidents"]]
        .dropna()
        .sort_values("%Change-Accidents", ascending=False)
    )
    if change_chart.empty:
        st.info("No usable percentage-change values were found for accidents.")
    else:
        add_plotly_bar(
            change_chart,
            "Category",
            "%Change-Accidents",
            "2023 to 2024 change by recorded violation",
        )

    st.subheader("Explore a traffic-violation category")
    selected_violation = st.selectbox(
        "Select category",
        df["Category"].tolist(),
        key="selected_violation_category",
    )
    selected = df[df["Category"] == selected_violation].iloc[0]

    a, b, c = st.columns(3)
    a.metric("2024 accidents", f"{int(selected['2024-Accidents']):,}")
    b.metric("2024 killed", f"{int(selected['2024-Killed']):,}")
    c.metric("2024 injured", f"{int(selected['2024-injured']):,}")

    for label, column in [
        ("accident", "%Change-Accidents"),
        ("killed", "%Change-killed"),
        ("injured", "%Change-Injured"),
    ]:
        value = selected[column]
        display = f"{value:.2f}%" if pd.notna(value) else "N/A"
        st.write(f"**2023 → 2024 {label} change:** {display}")

    st.subheader("Traffic violation dataset")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.info(
        "Interpretation note: these figures represent accidents associated "
        "with recorded traffic violations. They should not be interpreted as "
        "proof that a particular violation independently caused every accident "
        "in that category."
    )

    st.subheader("Data source")
    st.markdown(
        "[OpenCity — Road Accidents in India 2024]"
        "(https://data.opencity.in/dataset/road-accidents-in-india-2024)"
    )
    st.caption("Dataset: Road Accidents by Type of Violation, 2024.")

# ============================================================
# PAGE 4 — COLLISION TYPE ANALYSIS
# ============================================================

elif page == "Collision Type Analysis":
    st.title("💥 Collision Type Analysis")
    st.caption("Analysis of road accidents by type of collision | 2023–2024")

    uploaded = st.file_uploader(
        "Upload the Road Accidents by Type of Collision CSV",
        type=["csv", "xlsx", "xls"],
        key="collision_file",
    )

    if uploaded is None:
        st.info("Upload the Road Accidents by Type of Collision CSV to begin.")
        st.stop()

    df = read_uploaded_file(uploaded)
    df.columns = [str(column).strip() for column in df.columns]
    df = df.loc[
        :,
        [
            column
            for column in df.columns
            if column.strip().lower() != "index"
            and not column.strip().lower().startswith("unnamed:")
        ],
    ]

    category_column = None
    preferred_category_names = [
        "Type of collision",
        "Collision Type",
        "Type",
        "Category",
        "Collision",
    ]
    for candidate in preferred_category_names:
        if candidate in df.columns:
            category_column = candidate
            break

    if category_column is None:
        for column in df.columns:
            column_lower = column.lower()
            if any(word in column_lower for word in ["collision", "category", "type"]):
                category_column = column
                break

    if category_column is None:
        st.error("Could not identify the collision-type column.")
        st.write("Columns found:", list(df.columns))
        st.stop()

    def find_collision_measure(possible_names):
        for column in df.columns:
            column_lower = column.lower()
            if any(name.lower() in column_lower for name in possible_names):
                return column
        return None

    accident_2024 = find_collision_measure(["2024-Accidents", "2024 Accidents"])
    killed_2024 = find_collision_measure(["2024-Killed", "2024 Killed"])
    injured_2024 = find_collision_measure(
        ["2024-injured", "2024 injured", "2024-Injured"]
    )
    accident_2023 = find_collision_measure(["2023-Accidents", "2023 Accidents"])
    killed_2023 = find_collision_measure(["2023-Killed", "2023 Killed"])
    injured_2023 = find_collision_measure(
        ["2023-injured", "2023 injured", "2023-Injured"]
    )

    if accident_2024 is None:
        st.error("Could not identify the 2024 accident column.")
        st.write("Columns found:", list(df.columns))
        st.stop()

    numeric_columns = [
        accident_2024,
        killed_2024,
        injured_2024,
        accident_2023,
        killed_2023,
        injured_2023,
    ]
    numeric_columns = [column for column in numeric_columns if column is not None]
    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("%", "", regex=False),
            errors="coerce",
        )

    df[category_column] = df[category_column].astype("string").str.strip()
    df = df.dropna(subset=[category_column])
    category_labels = df[category_column].str.lower()
    df = df[
        df[category_column].ne("")
        & ~category_labels.str.contains("% share", na=False)
    ].copy()
    df = df.dropna(subset=[accident_2024])

    if df.empty:
        st.error("No usable collision categories with 2024 accident data were found.")
        st.stop()

    st.subheader("2024 collision overview")
    total_accidents = df[accident_2024].sum()
    total_killed = df[killed_2024].sum() if killed_2024 is not None else None
    total_injured = df[injured_2024].sum() if injured_2024 is not None else None

    metrics = [("Recorded accidents", total_accidents)]
    if total_killed is not None:
        metrics.append(("People killed", total_killed))
    if total_injured is not None:
        metrics.append(("People injured", total_injured))

    metric_columns = st.columns(len(metrics))
    for metric_column, (label, value) in zip(metric_columns, metrics):
        metric_column.metric(label, f"{int(value):,}")

    st.subheader("Recorded accidents by collision type")
    accident_chart = df[[category_column, accident_2024]].sort_values(
        accident_2024, ascending=False
    )
    add_plotly_bar(accident_chart, category_column, accident_2024, "Accidents by collision type")

    if killed_2024 is not None:
        st.subheader("Fatalities by collision type")
        killed_chart = df[[category_column, killed_2024]].sort_values(
            killed_2024, ascending=False
        )
        add_plotly_bar(killed_chart, category_column, killed_2024, "Fatalities by collision type")

    if injured_2024 is not None:
        st.subheader("Persons injured by collision type")
        injured_chart = df[[category_column, injured_2024]].sort_values(
            injured_2024, ascending=False
        )
        add_plotly_bar(injured_chart, category_column, injured_2024, "People injured by collision type")

    if accident_2023 is not None:
        st.subheader("2023 vs 2024 accident comparison")
        comparison = df[
            [category_column, accident_2023, accident_2024]
        ].set_index(category_column)
        comparison_chart = px.bar(
            comparison.reset_index(),
            x=category_column,
            y=[accident_2023, accident_2024],
            barmode="group",
            title="Recorded accidents by collision type · 2023 vs 2024",
            template="plotly_dark",
            color_discrete_sequence=["#f0bd62", "#67d5be"],
        )
        render_plotly(comparison_chart, height=460)

    st.subheader("Explore a collision type")
    selected_collision = st.selectbox(
        "Select collision type",
        df[category_column].tolist(),
        key="selected_collision_type",
    )
    selected = df[df[category_column] == selected_collision].iloc[0]

    selected_metrics = [("2024 accidents", selected[accident_2024])]
    if killed_2024 is not None:
        selected_metrics.append(("2024 killed", selected[killed_2024]))
    if injured_2024 is not None:
        selected_metrics.append(("2024 injured", selected[injured_2024]))

    metric_columns = st.columns(len(selected_metrics))
    for metric_column, (label, value) in zip(metric_columns, selected_metrics):
        metric_column.metric(label, f"{int(value):,}" if pd.notna(value) else "N/A")

    st.subheader("Collision dataset")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.info(
        "Interpretation note: the figures describe accidents recorded under "
        "each collision category. They should not be interpreted as proof that "
        "a particular collision type independently caused every accident in "
        "that category."
    )

    st.subheader("Data source")
    st.markdown(
        "[OpenCity — Road Accidents in India 2024]"
        "(https://data.opencity.in/dataset/road-accidents-in-india-2024)"
    )
    st.caption("Dataset: Road Accidents Classified by Type of Collision, 2024.")

# ============================================================
# PAGE 5 — ROAD USER ANALYSIS
# ============================================================

elif page == "Road User Analysis":
    st.title("🚶 Road User Fatality Analysis")
    st.caption(
        "Analysis of road accident fatalities by road-user category | 2023–2024"
    )

    uploaded = st.file_uploader(
        "Upload the Road Crash Fatalities by Road Users CSV",
        type=["csv", "xlsx", "xls"],
        key="road_user_file",
    )

    if uploaded is None:
        st.info("Upload the Road Crash Fatalities by Road Users CSV to begin.")
        st.stop()

    df = read_uploaded_file(uploaded)
    df.columns = [str(column).strip() for column in df.columns]
    df = df.loc[
        :,
        [
            column
            for column in df.columns
            if column.strip().lower() != "index"
            and not column.strip().lower().startswith("unnamed:")
        ],
    ]

    category_column = None
    killed_2023 = None
    killed_2024 = None
    change_column = None

    for column in df.columns:
        column_lower = column.lower()
        if "road-user" in column_lower or "road user" in column_lower:
            category_column = column
            break

    for column in df.columns:
        column_lower = column.lower()
        if "2023" in column_lower and (
            "killed" in column_lower or "fatal" in column_lower
        ):
            killed_2023 = column
            break

    for column in df.columns:
        column_lower = column.lower()
        if "2024" in column_lower and (
            "killed" in column_lower or "fatal" in column_lower
        ):
            killed_2024 = column
            break

    for column in df.columns:
        column_lower = column.lower()
        if "change" in column_lower and "%" in column_lower:
            change_column = column
            break

    missing = []
    if category_column is None:
        missing.append("road-user category")
    if killed_2023 is None:
        missing.append("2023 fatalities")
    if killed_2024 is None:
        missing.append("2024 fatalities")

    if missing:
        st.error("Could not identify the required columns.")
        st.write("Missing:", missing)
        st.write("Columns found:", list(df.columns))
        st.stop()

    df[category_column] = df[category_column].astype("string").str.strip()
    category_labels = df[category_column].str.lower()
    df = df[
        df[category_column].notna()
        & df[category_column].ne("")
        & ~category_labels.str.contains("share in total", na=False)
    ].copy()

    numeric_columns = [killed_2023, killed_2024, change_column]
    numeric_columns = [column for column in numeric_columns if column is not None]
    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("%", "", regex=False),
            errors="coerce",
        )

    df = df.dropna(subset=[killed_2023, killed_2024])
    if df.empty:
        st.error("No usable road-user fatality rows were found.")
        st.stop()

    st.subheader("Road-user fatality overview")
    total_2023 = df[killed_2023].sum()
    total_2024 = df[killed_2024].sum()
    overall_change = (
        (total_2024 - total_2023) / total_2023 * 100
        if total_2023 != 0
        else 0
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Recorded fatalities — 2023", f"{int(total_2023):,}")
    col2.metric("Recorded fatalities — 2024", f"{int(total_2024):,}")
    col3.metric("Overall change", f"{overall_change:.2f}%")

    st.subheader("2024 fatalities by road-user category")
    chart_2024 = df[[category_column, killed_2024]].sort_values(
        killed_2024, ascending=False
    )
    highest_user = chart_2024.iloc[0]
    show_insight(
        "Key insight ·",
        f"{highest_user[category_column]} has the highest recorded fatalities in 2024 "
        f"({int(highest_user[killed_2024]):,}) among the listed road-user categories.",
    )
    add_plotly_bar(chart_2024, category_column, killed_2024, "2024 fatalities by road-user category")

    st.subheader("2023 vs 2024 fatalities")
    comparison = df[[category_column, killed_2023, killed_2024]].set_index(
        category_column
    )
    comparison_chart = px.bar(
        comparison.reset_index(),
        x=category_column,
        y=[killed_2023, killed_2024],
        barmode="group",
        title="Road-user fatalities · 2023 vs 2024",
        template="plotly_dark",
        color_discrete_sequence=["#f0bd62", "#67d5be"],
    )
    render_plotly(comparison_chart, height=460)

    if change_column is not None:
        st.subheader("Change in fatalities: 2023 → 2024")
        change_chart = (
            df[[category_column, change_column]]
            .dropna()
            .sort_values(change_column, ascending=False)
        )
        if change_chart.empty:
            st.info("No usable percentage-change values were found.")
        else:
            add_plotly_bar(change_chart, category_column, change_column, "Fatality change by road-user category")

    st.subheader("Explore a road-user category")
    selected_user = st.selectbox(
        "Select road-user category",
        df[category_column].tolist(),
        key="selected_road_user",
    )
    selected = df[df[category_column] == selected_user].iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("2023 fatalities", f"{int(selected[killed_2023]):,}")
    col2.metric("2024 fatalities", f"{int(selected[killed_2024]):,}")
    if change_column is not None:
        selected_change = selected[change_column]
        col3.metric(
            "Change",
            f"{selected_change:.2f}%" if pd.notna(selected_change) else "N/A",
        )

    st.subheader("Road-user fatality dataset")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.info(
        "Interpretation note: this dataset measures fatalities by road-user "
        "category. It does not provide accident counts or injury counts by "
        "road-user category, so those measures are not inferred here."
    )

    st.subheader("Data source")
    st.markdown(
        "[OpenCity — Road Accidents in India 2024]"
        "(https://data.opencity.in/dataset/road-accidents-in-india-2024)"
    )
    st.caption("Dataset: Road Crash Fatalities by Road Users, 2024.")

# ============================================================
# PAGE 6 — VEHICLE INTERACTION ANALYSIS
# ============================================================

elif page == "Vehicle Interaction Analysis":
    st.title("🚗 Vehicle Interaction Analysis")
    st.caption("Analysis of victim vehicles and crime vehicles in road accidents")

    uploaded = st.file_uploader(
        "Upload the Victim Vehicle × Crime Vehicle CSV",
        type=["csv", "xlsx", "xls"],
        key="vehicle_interaction_file",
    )

    if uploaded is None:
        st.info("Upload the Victim Vehicle × Crime Vehicle CSV to begin.")
        st.stop()

    df = read_uploaded_file(uploaded)
    df.columns = [str(column).strip() for column in df.columns]
    df = df.loc[
        :,
        [
            column
            for column in df.columns
            if column.strip().lower() != "index"
            and not column.strip().lower().startswith("unnamed:")
        ],
    ]

    if df.shape[1] < 2:
        st.error("The uploaded file needs a victim-vehicle column and at least one crime-vehicle column.")
        st.stop()

    victim_column = df.columns[0]
    ignored_labels = {"total", "<-- crime vehicle", "<--- crime vehicle"}
    crime_vehicle_columns = [
        column
        for column in df.columns[1:]
        if column.strip().lower() not in ignored_labels
    ]

    if not crime_vehicle_columns:
        st.error("Could not identify any crime-vehicle columns in this file.")
        st.write("Columns found:", list(df.columns))
        st.stop()

    df[victim_column] = df[victim_column].astype("string").str.strip()
    category_labels = df[victim_column].str.lower()
    df = df[
        df[victim_column].notna()
        & df[victim_column].ne("")
        & ~category_labels.str.contains("% share", na=False)
        & ~category_labels.isin({"total", "victim vehicle(column above)"})
    ].copy()

    for column in crime_vehicle_columns:
        df[column] = pd.to_numeric(
            df[column]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("%", "", regex=False),
            errors="coerce",
        )

    df = df.dropna(subset=crime_vehicle_columns, how="all")
    if df.empty:
        st.error("No usable vehicle interaction rows were found.")
        st.stop()

    st.subheader("Vehicle interaction overview")
    total_interactions = df[crime_vehicle_columns].sum().sum()
    col1, col2, col3 = st.columns(3)
    col1.metric("Recorded vehicle interactions", f"{int(total_interactions):,}")
    col2.metric("Victim vehicle categories", len(df))
    col3.metric("Crime vehicle categories", len(crime_vehicle_columns))

    st.subheader("Recorded cases by victim vehicle")
    victim_totals = df[crime_vehicle_columns].sum(axis=1)
    victim_summary = pd.DataFrame(
        {"Victim Vehicle": df[victim_column], "Recorded Cases": victim_totals}
    ).sort_values("Recorded Cases", ascending=False)
    add_plotly_bar(victim_summary, "Victim Vehicle", "Recorded Cases", "Recorded cases by victim vehicle")

    st.subheader("Recorded cases by crime vehicle")
    crime_totals = df[crime_vehicle_columns].sum(axis=0)
    crime_summary = pd.DataFrame(
        {"Crime Vehicle": crime_totals.index, "Recorded Cases": crime_totals.values}
    ).sort_values("Recorded Cases", ascending=False)
    add_plotly_bar(crime_summary, "Crime Vehicle", "Recorded Cases", "Recorded cases by crime vehicle")

    st.subheader("Victim vehicle × crime vehicle matrix")
    matrix = df[[victim_column] + crime_vehicle_columns].copy().set_index(victim_column)
    st.dataframe(matrix, use_container_width=True)

    st.subheader("Vehicle interaction intensity")
    st.caption(
        "Higher values indicate more recorded interactions between the "
        "corresponding victim and crime vehicle categories."
    )
    st.dataframe(
        matrix.style.background_gradient(axis=None),
        use_container_width=True,
    )

    st.subheader("Most frequently recorded vehicle interaction")
    long_data = matrix.reset_index().melt(
        id_vars=victim_column,
        var_name="Crime Vehicle",
        value_name="Recorded Cases",
    )
    long_data = long_data.dropna(subset=["Recorded Cases"])
    if long_data.empty:
        st.info("No numeric vehicle interactions are available to compare.")
    else:
        top_interaction = long_data.loc[long_data["Recorded Cases"].idxmax()]
        show_insight(
            "Key insight ·",
            f"The largest recorded interaction is {top_interaction[victim_column]} × "
            f"{top_interaction['Crime Vehicle']} "
            f"({int(top_interaction['Recorded Cases']):,} cases).",
        )
        col1, col2, col3 = st.columns(3)
        col1.metric("Victim vehicle", str(top_interaction[victim_column]))
        col2.metric("Crime vehicle", str(top_interaction["Crime Vehicle"]))
        col3.metric("Recorded cases", f"{int(top_interaction['Recorded Cases']):,}")

    st.subheader("Explore a victim vehicle")
    selected_victim = st.selectbox(
        "Select victim vehicle",
        df[victim_column].tolist(),
        key="selected_victim_vehicle",
    )
    selected_row = df[df[victim_column] == selected_victim].iloc[0]
    selected_crime = pd.DataFrame(
        {
            "Crime Vehicle": crime_vehicle_columns,
            "Recorded Cases": [selected_row[column] for column in crime_vehicle_columns],
        }
    ).dropna(subset=["Recorded Cases"])
    selected_crime = selected_crime.sort_values("Recorded Cases", ascending=False)
    add_plotly_bar(
        selected_crime,
        "Crime Vehicle",
        "Recorded Cases",
        f"Crime vehicles associated with {selected_victim}",
    )

    st.subheader("Explore a crime vehicle")
    selected_crime_vehicle = st.selectbox(
        "Select crime vehicle",
        crime_vehicle_columns,
        key="selected_crime_vehicle",
    )
    selected_victim_data = pd.DataFrame(
        {
            "Victim Vehicle": df[victim_column],
            "Recorded Cases": df[selected_crime_vehicle].values,
        }
    ).dropna(subset=["Recorded Cases"])
    selected_victim_data = selected_victim_data.sort_values(
        "Recorded Cases", ascending=False
    )
    add_plotly_bar(
        selected_victim_data,
        "Victim Vehicle",
        "Recorded Cases",
        f"Victim vehicles associated with {selected_crime_vehicle}",
    )

    st.subheader("Vehicle interaction dataset")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.info(
        "Interpretation note: this dataset represents recorded vehicle "
        "interactions classified by victim vehicle and crime vehicle. The term "
        "'crime vehicle' follows the terminology used in the source dataset. "
        "These figures should not be interpreted as proof that a vehicle "
        "category independently caused an accident."
    )

    st.subheader("Data source")
    st.markdown(
        "[OpenCity — Road Accidents in India 2024]"
        "(https://data.opencity.in/dataset/road-accidents-in-india-2024)"
    )
    st.caption("Dataset: Victim Vehicle and Crime Vehicle, 2024.")

# ============================================================
# PAGE 7 — RISK & SIMULATION ANALYSIS
# ============================================================

elif page == "Risk & Simulation Analysis":
    st.title("📈 Risk & Simulation Analysis")
    st.caption(
        "Custom analytical indicator and hypothetical what-if simulation "
        "using State/UT accident data"
    )

    uploaded = st.file_uploader(
        "Upload the State/UT Road Accidents CSV",
        type=["csv", "xlsx", "xls"],
        key="risk_state_file",
    )

    if uploaded is None:
        st.info("Upload the same State/UT accident dataset used in State/UT Analysis.")
        st.stop()

    df = read_uploaded_file(uploaded)
    df.columns = [str(column).strip() for column in df.columns]
    df = df.loc[
        :,
        [
            column
            for column in df.columns
            if column.strip().lower() != "index"
            and not column.strip().lower().startswith("unnamed:")
        ],
    ]

    state_column = next(
        (column for column in df.columns if column.lower() == "state"),
        None,
    )
    if state_column is None:
        state_column = next(
            (column for column in df.columns if "state" in column.lower()),
            None,
        )

    accident_2024 = next(
        (
            column
            for column in df.columns
            if "2024" in column.lower() and "accident" in column.lower()
        ),
        None,
    )
    change_percent = next(
        (
            column
            for column in df.columns
            if "change" in column.lower() and "%" in column.lower()
        ),
        None,
    )

    missing = []
    if state_column is None:
        missing.append("State")
    if accident_2024 is None:
        missing.append("2024 accidents")
    if change_percent is None:
        missing.append("percentage change")

    if missing:
        st.error("Could not identify the required columns.")
        st.write("Missing:", missing)
        st.write("Columns found:", list(df.columns))
        st.stop()

    df[state_column] = df[state_column].astype("string").str.strip()
    df[accident_2024] = pd.to_numeric(
        df[accident_2024]
        .astype(str)
        .str.replace(",", "", regex=False),
        errors="coerce",
    )
    df[change_percent] = pd.to_numeric(
        df[change_percent]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", "", regex=False),
        errors="coerce",
    )

    df = df.dropna(subset=[state_column, accident_2024, change_percent]).copy()
    state_labels = df[state_column].str.lower()
    df = df[
        df[state_column].ne("")
        & ~state_labels.str.contains("total|share", na=False)
    ].copy()

    if df.empty:
        st.error("No usable State/UT rows with 2024 accidents and percentage change were found.")
        st.stop()

    min_accidents = df[accident_2024].min()
    max_accidents = df[accident_2024].max()
    if max_accidents == min_accidents:
        df["Accident Burden Score"] = 0.0
    else:
        df["Accident Burden Score"] = (
            (df[accident_2024] - min_accidents)
            / (max_accidents - min_accidents)
            * 100
        )

    min_change = df[change_percent].min()
    max_change = df[change_percent].max()
    if max_change == min_change:
        df["Change Score"] = 0.0
    else:
        df["Change Score"] = (
            (df[change_percent] - min_change)
            / (max_change - min_change)
            * 100
        )

    df["Analytical Risk Indicator"] = (
        0.70 * df["Accident Burden Score"] + 0.30 * df["Change Score"]
    )

    st.subheader("Custom Analytical Risk Indicator")
    st.write(
        "This indicator combines the relative 2024 recorded accident burden "
        "with the relative 2023→2024 change in recorded accidents."
    )
    st.write("**Formula:** 70% Accident Burden Score + 30% Change Score")
    st.info(
        "Important: this is a custom analytical indicator created for this "
        "project. It is not an official government risk rating and does not "
        "represent accident probability. Traffic volume, vehicle population, "
        "and road length are not included because they are unavailable here."
    )

    st.subheader("Dataset overview")
    total_accidents = df[accident_2024].sum()
    highest_state = df.loc[df[accident_2024].idxmax(), state_column]
    col1, col2, col3 = st.columns(3)
    col1.metric("States/UTs analysed", len(df))
    col2.metric("Recorded accidents — 2024", f"{int(total_accidents):,}")
    col3.metric("Highest recorded accident count", str(highest_state))

    st.subheader("Analytical Risk Indicator by State/UT")
    risk_chart = df[[state_column, "Analytical Risk Indicator"]].sort_values(
        "Analytical Risk Indicator", ascending=False
    )
    add_plotly_bar(
        risk_chart,
        state_column,
        "Analytical Risk Indicator",
        "Custom analytical indicator by State/UT",
    )

    st.subheader("Accident burden vs yearly change")
    scatter_fig = px.scatter(
        df,
        x=accident_2024,
        y=change_percent,
        hover_name=state_column,
        size="Analytical Risk Indicator",
        title="Recorded accident burden vs year-on-year change",
        template="plotly_dark",
        color_discrete_sequence=["#67d5be"],
    )
    scatter_fig.update_layout(hovermode="closest")
    render_plotly(scatter_fig, height=440)
    st.caption(
        "Each point represents a State/UT. The horizontal axis represents "
        "recorded 2024 accidents and the vertical axis represents percentage "
        "change from 2023 to 2024."
    )

    st.subheader("Explore a State/UT")
    selected_state = st.selectbox(
        "Select State/UT",
        df[state_column].tolist(),
        key="risk_selected_state",
    )
    selected = df[df[state_column] == selected_state].iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("2024 accidents", f"{int(selected[accident_2024]):,}")
    col2.metric("2023→2024 change", f"{selected[change_percent]:.2f}%")
    col3.metric(
        "Analytical indicator",
        f"{selected['Analytical Risk Indicator']:.2f}/100",
    )
    show_insight(
        "Selected-state insight ·",
        f"{selected_state} records {int(selected[accident_2024]):,} accidents in 2024, with a "
        f"{selected[change_percent]:.2f}% change from 2023. Its custom indicator is "
        f"{selected['Analytical Risk Indicator']:.2f}/100 within this dataset.",
    )

    st.subheader("🧪 What-if Accident Reduction Simulation")
    st.write(
        "Choose a hypothetical reduction in recorded accidents and observe "
        "the resulting simulated accident count."
    )
    reduction = st.slider(
        "Assumed accident reduction (%)",
        min_value=0,
        max_value=50,
        value=10,
        step=5,
        key="accident_reduction",
    )
    baseline_accidents = selected[accident_2024]
    simulated_accidents = baseline_accidents * (1 - reduction / 100)
    avoided_accidents = baseline_accidents - simulated_accidents

    col1, col2, col3 = st.columns(3)
    col1.metric("Baseline accidents", f"{int(baseline_accidents):,}")
    col2.metric("Simulated accidents", f"{int(simulated_accidents):,}")
    col3.metric("Hypothetical reduction", f"{int(avoided_accidents):,}")

    simulation_data = pd.DataFrame(
        {
            "Scenario": ["Baseline", "Simulated"],
            "Accidents": [baseline_accidents, simulated_accidents],
        }
    )
    add_plotly_bar(
        simulation_data,
        "Scenario",
        "Accidents",
        "Baseline vs simulated accidents",
        horizontal=False,
    )

    st.subheader("India-wide hypothetical simulation")
    national_reduction = st.slider(
        "Assumed India-wide accident reduction (%)",
        min_value=0,
        max_value=50,
        value=10,
        step=5,
        key="national_accident_reduction",
    )
    national_baseline = df[accident_2024].sum()
    national_simulated = national_baseline * (1 - national_reduction / 100)
    national_avoided = national_baseline - national_simulated

    col1, col2, col3 = st.columns(3)
    col1.metric("Baseline recorded accidents", f"{int(national_baseline):,}")
    col2.metric("Simulated accidents", f"{int(national_simulated):,}")
    col3.metric("Hypothetically avoided", f"{int(national_avoided):,}")

    st.subheader("Analytical results")
    display_columns = [
        state_column,
        accident_2024,
        change_percent,
        "Accident Burden Score",
        "Change Score",
        "Analytical Risk Indicator",
    ]
    st.dataframe(
        df[display_columns].sort_values(
            "Analytical Risk Indicator", ascending=False
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("How to interpret this analysis")
    st.write(
        "A higher analytical indicator means that the State/UT has a higher "
        "combination of relative recorded accident burden and relative "
        "year-on-year change within this dataset."
    )
    st.write(
        "The simulation is hypothetical. It demonstrates the numerical effect "
        "of an assumed reduction; it does not predict future accident counts."
    )

    st.subheader("Limitations")
    st.warning(
        "The indicator does not account for population, registered vehicles, "
        "traffic volume, road length, travel distance, weather exposure, or "
        "other exposure variables. Do not use it to conclude that one State/UT "
        "has a higher true accident probability than another."
    )

    st.subheader("Data source")
    st.markdown(
        "[OpenCity — Road Accidents in India 2024]"
        "(https://data.opencity.in/dataset/road-accidents-in-india-2024)"
    )
    st.caption("Analysis based on the State/UT road accident dataset used in this project.")


st.markdown(
    "<div class='footer'>🇮🇳 Indian Road Safety Analytics · ECE-181 CA2 · "
    "Interactive Python Dashboard</div>",
    unsafe_allow_html=True,
)
