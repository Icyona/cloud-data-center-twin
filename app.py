import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(
    page_title="Data Center Digital Twin",
    page_icon="☁️",
    layout="wide"
)

# ---------- DARK THEME ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080d19, #101a30);
    color: #e5e7eb;
}
[data-testid="stHeader"] {
    background: transparent;
}
.block-container {
    padding-top: 2rem;
    max-width: 1450px;
}
.metric-card {
    background: #131f35;
    border: 1px solid #263650;
    padding: 22px;
    border-radius: 15px;
    min-height: 135px;
}
.metric-label {
    color: #94a3b8;
    font-size: 13px;
    letter-spacing: 1px;
}
.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: #60a5fa;
    margin-top: 10px;
}
.section-title {
    color: #93c5fd;
    font-size: 22px;
    font-weight: 600;
    margin-top: 24px;
}
.alert-card {
    background: #251b2c;
    border-left: 4px solid #fb7185;
    border-radius: 9px;
    padding: 15px;
    margin: 8px 0;
}
.normal-card {
    background: #122b29;
    border-left: 4px solid #34d399;
    border-radius: 9px;
    padding: 15px;
    margin: 8px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------- SERVER DATA ----------
if "servers" not in st.session_state:
    st.session_state.servers = pd.DataFrame({
        "Server": ["Server 01", "Server 02", "Server 03",
                   "Server 04", "Server 05", "Server 06"],
        "CPU": [35, 92, 60, 25, 72, 45],
        "Memory": [40, 88, 65, 30, 70, 50],
        "Temperature": [45, 85, 60, 38, 68, 48],
        "Network": [30, 90, 50, 25, 75, 40],
        "Packet Loss": [0.1, 3.5, 0.2, 0.0, 1.2, 0.1]
    })

df = st.session_state.servers.copy()

# ---------- SIMPLE ANALYTICS ----------
def risk_score(row):
    score = 0
    if row["CPU"] > 85:
        score += 25
    if row["Memory"] > 85:
        score += 25
    if row["Temperature"] > 80:
        score += 30
    if row["Network"] > 85:
        score += 10
    if row["Packet Loss"] >= 2:
        score += 10
    return score

df["Risk Score"] = df.apply(risk_score, axis=1)

df["Status"] = df["Risk Score"].apply(
    lambda x: "HIGH RISK" if x >= 50
    else "MEDIUM RISK" if x >= 25
    else "NORMAL"
)

# ---------- SIDEBAR ----------
st.sidebar.markdown("## ☁️ DIGITAL TWIN")
st.sidebar.caption("CLOUD INFRASTRUCTURE")

st.sidebar.markdown("---")
st.sidebar.markdown("### Control Center")

import random

if st.sidebar.button("↻ Simulate New Readings",
                     use_container_width=True):

    for i in st.session_state.servers.index:
        st.session_state.servers.loc[i, "CPU"] = random.randint(20, 95)
        st.session_state.servers.loc[i, "Memory"] = random.randint(25, 95)
        st.session_state.servers.loc[i, "Temperature"] = random.randint(35, 90)
        st.session_state.servers.loc[i, "Network"] = random.randint(10, 95)
        st.session_state.servers.loc[i, "Packet Loss"] = round(
            random.uniform(0, 4), 1
        )

    st.rerun()

selected_server = st.sidebar.selectbox(
    "Inspect a server",
    ["All Servers"] + df["Server"].tolist()
)

st.sidebar.markdown("---")
st.sidebar.caption("Mode: Simulated Data")
st.sidebar.caption("Analytics: Threshold Based")

# ---------- HEADER ----------
st.markdown(
    "<div style='color:#60a5fa;letter-spacing:3px;"
    "font-size:12px;'>CLOUD INFRASTRUCTURE / MONITORING</div>",
    unsafe_allow_html=True
)

st.title("☁️ Data Center Digital Twin")

st.markdown(
    "Resource Optimization **·** Failure Risk Monitoring "
    "**·** Network Health"
)

st.markdown(
    "<span style='color:#34d399;'>● SYSTEM ONLINE</span>"
    " &nbsp; <span style='color:#64748b;'>"
    "SIMULATED ENVIRONMENT</span>",
    unsafe_allow_html=True
)

st.markdown("---")

# ---------- SUMMARY CARDS ----------
avg_cpu = df["CPU"].mean()
avg_memory = df["Memory"].mean()
high_risk = (df["Status"] == "HIGH RISK").sum()
warning_count = (df["Status"] != "NORMAL").sum()

metrics = [
    ("TOTAL SERVERS", str(len(df)), "Virtual infrastructure"),
    ("AVERAGE CPU", f"{avg_cpu:.1f}%", "Processor utilization"),
    ("AVERAGE MEMORY", f"{avg_memory:.1f}%", "Memory utilization"),
    ("HIGH RISK", str(high_risk), "Servers requiring attention")
]

cols = st.columns(4)

for col, (label, value, note) in zip(cols, metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div style="color:#94a3b8;font-size:12px;">
                {note}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------- FILTER ----------
if selected_server != "All Servers":
    view = df[df["Server"] == selected_server].copy()
else:
    view = df.copy()

# ---------- SERVER TABLE ----------
st.markdown(
    '<div class="section-title">01 / Server Infrastructure</div>',
    unsafe_allow_html=True
)

st.dataframe(
    view,
    use_container_width=True,
    hide_index=True,
    column_config={
        "CPU": st.column_config.ProgressColumn(
            "CPU Usage", min_value=0, max_value=100,
            format="%d%%"
        ),
        "Memory": st.column_config.ProgressColumn(
            "Memory Usage", min_value=0, max_value=100,
            format="%d%%"
        ),
        "Network": st.column_config.ProgressColumn(
            "Network Usage", min_value=0, max_value=100,
            format="%d%%"
        ),
        "Temperature": st.column_config.NumberColumn(
            "Temperature", format="%d °C"
        ),
        "Packet Loss": st.column_config.NumberColumn(
            "Packet Loss", format="%.1f%%"
        )
    }
)

# ---------- RESOURCE CHART ----------
st.markdown(
    '<div class="section-title">02 / Resource Utilization</div>',
    unsafe_allow_html=True
)

resource_data = view.melt(
    id_vars="Server",
    value_vars=["CPU", "Memory", "Network"],
    var_name="Resource",
    value_name="Usage"
)

fig = px.bar(
    resource_data,
    x="Server",
    y="Usage",
    color="Resource",
    barmode="group",
    template="plotly_dark",
    color_discrete_map={
        "CPU": "#60a5fa",
        "Memory": "#a78bfa",
        "Network": "#34d399"
    }
)

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#e2e8f0",
    yaxis=dict(range=[0, 100], title="Usage (%)"),
    xaxis_title="",
    legend_title="Resource",
    margin=dict(l=10, r=10, t=25, b=10),
    height=390
)

st.plotly_chart(fig, use_container_width=True)

# ---------- NETWORK HEALTH ----------
st.markdown(
    '<div class="section-title">03 / Network Health</div>',
    unsafe_allow_html=True
)

net_col1, net_col2 = st.columns(2)

with net_col1:
    network_fig = px.scatter(
        view,
        x="Network",
        y="Packet Loss",
        color="Server",
        size="CPU",
        hover_name="Server",
        template="plotly_dark",
        title="Network Utilization vs Packet Loss"
    )

    network_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        xaxis_title="Network Usage (%)",
        yaxis_title="Packet Loss (%)"
    )

    st.plotly_chart(network_fig, use_container_width=True)

with net_col2:
    risk_fig = px.bar(
        view,
        x="Server",
        y="Risk Score",
        color="Status",
        template="plotly_dark",
        title="Server Failure Risk Score",
        color_discrete_map={
            "NORMAL": "#34d399",
            "MEDIUM RISK": "#fbbf24",
            "HIGH RISK": "#fb7185"
        }
    )

    risk_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        yaxis_title="Risk Score",
        xaxis_title=""
    )

    st.plotly_chart(risk_fig, use_container_width=True)

# ---------- RECOMMENDATIONS ----------
st.markdown(
    '<div class="section-title">04 / System Recommendations</div>',
    unsafe_allow_html=True
)

for _, row in view.iterrows():
    recommendations = []

    if row["CPU"] > 85:
        recommendations.append(
            "High CPU usage: redistribute workloads or scale up resources."
        )

    if row["Memory"] > 85:
        recommendations.append(
            "High memory usage: free unused memory or increase capacity."
        )

    if row["Temperature"] > 75:
        recommendations.append(
            "High temperature: inspect cooling and airflow."
        )

    if row["Network"] > 80:
        recommendations.append(
            "High network usage: review traffic and balance network load."
        )

    if row["CPU"] < 30 and row["Memory"] < 40:
        recommendations.append(
            "Low utilization: consider consolidating workloads."
        )

    if not recommendations:
        recommendations.append(
            "Resource usage is within acceptable limits."
        )

    if row["Status"] == "HIGH RISK":
        recommendations.append(
            "High failure risk: investigate server health immediately."
        )

    recommendation = "<br><br>".join(
    f"• {item}" for item in recommendations
)

    css_class = (
        "alert-card" if row["Status"] != "NORMAL"
        else "normal-card"
    )

    st.markdown(f"""
    <div class="{css_class}">
        <b>{row['Server']}</b> &nbsp; | &nbsp; {row['Status']}
        <br><br>{recommendation}
    </div>
    """, unsafe_allow_html=True)

# ---------- DOWNLOAD SERVER REPORT ----------
st.markdown("### Export Analytics Report")

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Server Report",
    data=csv_data,
    file_name="cloud_server_report.csv",
    mime="text/csv"
)

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#64748b;padding:15px;'>"
    "<b style='color:#60a5fa;'>CLOUD DATA CENTER DIGITAL TWIN</b>"
    "<br>Resource Optimization & Failure Risk Monitoring"
    "<br>Simulated Data · Threshold-Based Analytics"
    "</div>",
    unsafe_allow_html=True
)

