import os
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# ==========================================================
# CAMPUS DIGITAL TWIN FOR RESOURCE OPTIMIZATION
# RIT C BLOCK - HACKATHON PROTOTYPE
# ==========================================================

st.set_page_config(
    page_title="Campus Digital Twin",
    page_icon="🏫",
    layout="wide",
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.stApp {
    background-color: #07121f;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.2rem;
}

.hero {
    background: linear-gradient(
        135deg,
        #0b2037 0%,
        #123b5c 55%,
        #081827 100%
    );

    border: 1px solid #24577b;
    border-radius: 22px;

    padding: 28px;
    margin-bottom: 20px;
}

.hero h1 {
    color: #f5fbff;
    font-size: 2.2rem;
    margin-bottom: 5px;
}

.hero p {
    color: #a7bfd2;
    margin-top: 0;
}

.online {
    display: inline-block;

    background: #103c2d;
    color: #63e6ad;

    border: 1px solid #236a4d;
    border-radius: 999px;

    padding: 6px 13px;
    margin-top: 10px;

    font-size: 0.8rem;
    font-weight: bold;
}

.card {
    background: #0d1d2e;

    border: 1px solid #1e3c55;
    border-radius: 18px;

    padding: 20px;

    min-height: 160px;
}

.card-title {
    color: #cfe4f5;
    font-size: 1rem;
    font-weight: 700;
}

.big-value {
    color: white;
    font-size: 2rem;
    font-weight: 800;

    margin-top: 8px;
}

.small {
    color: #849caf;
    font-size: 0.82rem;
}

.live {
    color: #55e3a5;
    font-weight: 700;
    font-size: 0.8rem;
    margin-top: 10px;
}

.demo {
    color: #ffc857;
    font-weight: 700;
    font-size: 0.8rem;
    margin-top: 10px;
}

.section {
    color: #e5f2ff;
    font-size: 1.2rem;
    font-weight: 800;

    margin-top: 25px;
    margin-bottom: 12px;
}

.good {
    background: #0d2b20;
    border: 1px solid #246b4d;

    color: #72e4b0;

    border-radius: 13px;

    padding: 13px;
    margin-bottom: 8px;
}

.warning {
    background: #2d210c;
    border: 1px solid #76591e;

    color: #ffd976;

    border-radius: 13px;

    padding: 13px;
    margin-bottom: 8px;
}

.twin {
    background: #081827;

    border: 1px solid #214761;

    border-radius: 18px;

    padding: 18px;
}

.floor {
    height: 32px;

    border-radius: 6px;

    margin: 5px 0;

    border: 1px solid #2d6287;

    background:
        linear-gradient(
            90deg,
            #123552,
            #1b557a,
            #123552
        );
}

.floor span {
    line-height: 32px;

    padding-left: 12px;

    color: #d9edff;

    font-size: 0.78rem;

    font-weight: 700;
}

.sensor {
    display: inline-block;

    padding: 7px 10px;

    border-radius: 9px;

    margin: 4px;

    font-size: 0.78rem;

    font-weight: 700;
}

.red {
    background: #411c1c;
    color: #ff9494;
    border: 1px solid #743c3c;
}

.blue {
    background: #102d49;
    color: #82c8ff;
    border: 1px solid #32648f;
}

.green {
    background: #123627;
    color: #74e6ad;
    border: 1px solid #2d6d4d;
}

.footer {
    color: #71899d;
    font-size: 0.8rem;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown("## 🏫 Campus Digital Twin")

    st.caption(
        "Resource Optimization • RIT C Block"
    )

    st.markdown("---")

    st.markdown("### Data Source")

    mode = st.radio(
        "Select mode",
        [
            "Demo Mode",
            "ESP32 Live Mode"
        ]
    )

    st.markdown("---")

    st.markdown("### Prototype Controls")

    electricity = st.slider(
        "⚡ Electricity Current (A)",
        min_value=0.0,
        max_value=10.0,
        value=2.84,
        step=0.01
    )

    water_flow = st.slider(
        "💧 Water Flow (L/min)",
        min_value=0.0,
        max_value=6.0,
        value=2.31,
        step=0.01
    )

    tank_level = st.slider(
        "🚰 Tank Level (%)",
        min_value=0,
        max_value=100,
        value=73
    )

    st.markdown("---")

    st.info(
        """
        **Prototype safety**

        Building 240 V AC is NOT directly
        connected to this prototype.

        Electricity is currently represented
        using demo/replay data.

        YF-S401 and HC-SR04 can later
        provide live ESP32 readings.
        """
    )


# ==========================================================
# CALCULATIONS
# ==========================================================

power = electricity * 230

if electricity > 8:
    electricity_status = "HIGH"
else:
    electricity_status = "NORMAL"


if water_flow < 0.2:
    flow_status = "LOW"
else:
    flow_status = "NORMAL"


if tank_level < 25:
    tank_status = "LOW"

elif tank_level < 50:
    tank_status = "WATCH"

else:
    tank_status = "NORMAL"


# ==========================================================
# HEADER
# ==========================================================

st.markdown("""
<div class="hero">

<h1>
🏫 Campus Digital Twin for Resource Optimization
</h1>

<p>
RIT C Block • G+7 Building • Energy & Water Infrastructure
</p>

<span class="online">
● DIGITAL TWIN ONLINE
</span>

</div>
""", unsafe_allow_html=True)


# ==========================================================
# MAIN KPI CARDS
# ==========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(f"""
    <div class="card">

        <div class="card-title">
        ⚡ Electricity
        </div>

        <div class="big-value">
        {electricity:.2f} A
        </div>

        <div class="small">
        Estimated power: {power:.0f} W
        </div>

        <div class="{'demo' if mode == 'Demo Mode' else 'live'}">
        {'● DEMO DATA' if mode == 'Demo Mode'
         else '● ESP32 INPUT'}
        </div>

    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown(f"""
    <div class="card">

        <div class="card-title">
        💧 Water Flow
        </div>

        <div class="big-value">
        {water_flow:.2f} L/min
        </div>

        <div class="small">
        YF-S401 flow sensor
        </div>

        <div class="{'demo' if mode == 'Demo Mode' else 'live'}">
        {'● DEMO DATA' if mode == 'Demo Mode'
         else '● ESP32 INPUT'}
        </div>

    </div>
    """, unsafe_allow_html=True)


with col3:

    st.markdown(f"""
    <div class="card">

        <div class="card-title">
        🚰 Tank Level
        </div>

        <div class="big-value">
        {tank_level}%
        </div>

        <div class="small">
        HC-SR04 ultrasonic sensor
        </div>

        <div class="{'demo' if mode == 'Demo Mode' else 'live'}">
        {'● DEMO DATA' if mode == 'Demo Mode'
         else '● ESP32 INPUT'}
        </div>

    </div>
    """, unsafe_allow_html=True)


with col4:

    st.markdown("""
    <div class="card">

        <div class="card-title">
        🏢 Building
        </div>

        <div class="big-value">
        G + 7
        </div>

        <div class="small">
        8 monitored levels
        </div>

        <div class="live">
        ● MODEL ONLINE
        </div>

    </div>
    """, unsafe_allow_html=True)


# ==========================================================
# SYSTEM HEALTH
# ==========================================================

st.markdown(
    '<div class="section">System Health</div>',
    unsafe_allow_html=True
)

h1, h2, h3 = st.columns(3)


with h1:

    if electricity_status == "HIGH":

        st.markdown(
            """
            <div class="warning">
            ⚠ High electrical current detected.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="good">
            ✓ Electrical load within threshold.
            </div>
            """,
            unsafe_allow_html=True
        )


with h2:

    if flow_status == "LOW":

        st.markdown(
            """
            <div class="warning">
            ⚠ Low/no water flow detected.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="good">
            ✓ Water flow detected.
            </div>
            """,
            unsafe_allow_html=True
        )


with h3:

    if tank_status == "LOW":

        st.markdown(
            """
            <div class="warning">
            🚨 Tank level critically low.
            </div>
            """,
            unsafe_allow_html=True
        )

    elif tank_status == "WATCH":

        st.markdown(
            """
            <div class="warning">
            ⚠ Tank level approaching low range.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="good">
            ✓ Tank level normal.
            </div>
            """,
            unsafe_allow_html=True
        )


# ==========================================================
# DIGITAL TWIN
# ==========================================================

st.markdown("## 🏢 C Block Digital Twin")

twin_image = os.path.join(
    os.path.dirname(__file__),
    "c_block_twin.png"
)

if os.path.exists(twin_image):
    st.image(
        twin_image,
        caption="RIT C Block — Campus Digital Twin",
        use_container_width=True
    )
else:
    st.error("c_block_twin.png not found.")

left, right = st.columns([1.25, 1])


# ---------------- BUILDING ----------------

with left:

    st.markdown(
        '<div class="twin">',
        unsafe_allow_html=True
    )

    st.markdown(
        "### RIT C Block — Resource Map"
    )

    for floor in range(7, -1, -1):

        if floor == 0:

            name = "GROUND FLOOR"

        else:

            name = f"FLOOR {floor}"

        st.markdown(
            f"""
            <div class="floor">

                <span>
                {name}
                &nbsp; • &nbsp;
                7 classrooms / infrastructure
                </span>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        """
        <div style="margin-top:12px;">

        <span class="sensor red">
        ⚡ INA219 / ENERGY
        </span>

        <span class="sensor blue">
        💧 YF-S401 / WATER FLOW
        </span>

        <span class="sensor green">
        🚰 HC-SR04 / TANK
        </span>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <p style="color:#849caf;font-size:.8rem;">
        Blender 3D C Block model will be connected
        as the visual twin layer in the next stage.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------- RESOURCE TABLE ----------------

with right:

    st.markdown(
        "### 📊 Current Resource Status"
    )

    resource_data = pd.DataFrame({

        "Resource": [
            "Electricity",
            "Water Flow",
            "Tank"
        ],

        "Reading": [
            f"{electricity:.2f} A",
            f"{water_flow:.2f} L/min",
            f"{tank_level}%"
        ],

        "Status": [
            electricity_status,
            flow_status,
            tank_status
        ]

    })

    st.dataframe(
        resource_data,
        use_container_width=True,
        hide_index=True
    )


    st.markdown(
        "### 🔄 Data Pipeline"
    )

    st.code(
        """
Physical Sensors
       ↓
    ESP32
       ↓
      Wi-Fi
       ↓
Data Processing
       ↓
Digital Twin
       ↓
Dashboard
        """,
        language="text"
    )

# =========================================================
# FLOOR-WISE DIGITAL TWIN
# =========================================================
# =========================================================
# FLOOR-WISE DIGITAL TWIN
# =========================================================

st.markdown("## 🏢 Floor-wise Digital Twin")

# ---------------------------------------------------------
# FLOOR DATA
# ---------------------------------------------------------

floor_data = {

    "Ground Floor": {
        "classrooms": 3,
        "restrooms": 1,
        "lifts": 2,
        "staircases": 3,
        "type": "Open / Activity Space + Classrooms"
    },

    "1st Floor": {
        "classrooms": 3,
        "restrooms": 1,
        "lifts": 2,
        "staircases": 3,
        "type": "Open / Activity Space + Classrooms"
    },

    "2nd Floor": {
        "classrooms": 7,
        "restrooms": 2,
        "lifts": 2,
        "staircases": 3,
        "type": "Classroom Floor"
    },

    "3rd Floor": {
        "classrooms": 7,
        "restrooms": 2,
        "lifts": 2,
        "staircases": 3,
        "type": "Classroom Floor"
    },

    "4th Floor": {
        "classrooms": 7,
        "restrooms": 2,
        "lifts": 2,
        "staircases": 3,
        "type": "Classroom Floor"
    },

    "5th Floor": {
        "classrooms": 7,
        "restrooms": 2,
        "lifts": 2,
        "staircases": 3,
        "type": "Classroom Floor"
    },

    "6th Floor": {
        "classrooms": 7,
        "restrooms": 2,
        "lifts": 2,
        "staircases": 3,
        "type": "Classroom Floor"
    },

    "7th Floor": {
        "classrooms": 7,
        "restrooms": 2,
        "lifts": 2,
        "staircases": 3,
        "type": "Classroom Floor"
    }
}

# ---------------------------------------------------------
# FLOOR SELECTION
# ---------------------------------------------------------

floor = st.selectbox(
    "Select Building Floor",
    options=list(floor_data.keys())
)

# ---------------------------------------------------------
# GET SELECTED FLOOR DATA
# ---------------------------------------------------------

data = floor_data.get(floor)

# ---------------------------------------------------------
# DISPLAY FLOOR INFORMATION
# ---------------------------------------------------------

if data:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Classrooms",
            value=data["classrooms"]
        )

    with col2:
        st.metric(
            label="Restrooms",
            value=data["restrooms"]
        )

    with col3:
        st.metric(
            label="Lifts",
            value=data["lifts"]
        )

    with col4:
        st.metric(
            label="Staircases",
            value=data["staircases"]
        )

    # Floor description
    st.info(
        f"**{floor}** — {data['type']}"
    )

else:

    st.error("Floor information unavailable.")
# ==========================================================
# RESOURCE TRENDS
# ==========================================================

st.markdown(
    '<div class="section">📈 Resource Trends</div>',
    unsafe_allow_html=True
)

x = np.arange(24)


flow_history = (
    water_flow
    + 0.15 * np.sin(x / 2)
)

tank_history = (
    tank_level
    - np.linspace(0, 2, 24)
    + 0.1 * np.sin(x / 2)
)

electricity_history = (
    electricity
    + 0.12 * np.sin(x / 2)
)


chart_data = pd.DataFrame({

    "Electricity (A)": electricity_history,

    "Water Flow (L/min)": flow_history,

    "Tank Level (%)": tank_history

})


st.line_chart(
    chart_data,
    height=300
)


# ==========================================================
# RESOURCE OPTIMIZATION
# ==========================================================

st.markdown(
    '<div class="section">💡 Resource Optimization Insights</div>',
    unsafe_allow_html=True
)

o1, o2, o3 = st.columns(3)


with o1:

    st.markdown(
        """
        <div class="card">

        <div class="card-title">
        ⚡ Energy Optimization
        </div>

        <div class="small">

        Monitor abnormal current patterns
        and identify periods of unusually
        high electrical demand.

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with o2:

    st.markdown(
        """
        <div class="card">

        <div class="card-title">
        💧 Water Optimization
        </div>

        <div class="small">

        Compare expected and measured
        water flow to identify possible
        leakage or abnormal consumption.

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with o3:

    st.markdown(
        """
        <div class="card">

        <div class="card-title">
        🚰 Tank Optimization
        </div>

        <div class="small">

        Monitor water availability and
        generate early warnings before
        the tank reaches a critical level.

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown(
    f"""
    <div class="footer">

    Campus Digital Twin for Resource Optimization
    • RIT C Block Prototype

    • Last update:
    {datetime.now().strftime("%d %b %Y, %I:%M:%S %p")}

    </div>
    """,
    unsafe_allow_html=True
)
