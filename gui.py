# Ultimate SPDI Streamlit App
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# App Config
st.set_page_config(page_title="SPDI Framework", layout="wide", page_icon="🏏")

st.markdown("""
# ⭐ Star Player Dependency Index (SPDI)
**Interactive Dashboard to Measure Team Dependency on Star Players in Cricket**
""")

# -----------------------------
# Sidebar Inputs
st.sidebar.header("Match Data Input")

# Batting
st.sidebar.subheader("Batting Contributions")
rb1 = st.sidebar.number_input("Star Batter 1 (Runs)", min_value=0, value=55)
rb2 = st.sidebar.number_input("Star Batter 2 (Runs)", min_value=0, value=48)
total_runs = st.sidebar.number_input("Team Total Runs", min_value=1, value=180)

# Bowling
st.sidebar.subheader("Bowling Contributions")
wb1 = st.sidebar.number_input("Star Bowler 1 (Wickets)", min_value=0, value=3)
wb2 = st.sidebar.number_input("Star Bowler 2 (Wickets)", min_value=0, value=2)
total_wickets = st.sidebar.number_input("Total Team Wickets", min_value=1, value=9)

# -----------------------------
# Validation
errors = []
if (rb1 + rb2) > total_runs:
    errors.append("Total runs by star batsmen cannot exceed team total!")
if (wb1 + wb2) > total_wickets:
    errors.append("Total wickets by star bowlers cannot exceed team total!")
if wb1 > 10 or wb2 > 10:
    errors.append("A bowler cannot take more than 10 wickets.")

if errors:
    st.error("\n".join(errors))
else:
    # -----------------------------
    # SPDI Calculations
    spdi_bat = (rb1 + rb2) / total_runs
    spdi_bowl = (wb1 + wb2) / total_wickets
    spdi_final = (spdi_bat + spdi_bowl) / 2

    # -----------------------------
    # Risk Classification
    if spdi_final >= 0.5:
        risk_level = "High Risk 🔴"
        risk_color = "#ef4444"
        risk_desc = "Dangerous over-dependency on star players. Coaches must distribute responsibilities."
    elif spdi_final >= 0.3:
        risk_level = "Medium Risk 🟡"
        risk_color = "#f59e0b"
        risk_desc = "Moderate dependency. Team has some balance but relies on key players."
    else:
        risk_level = "Low Risk 🟢"
        risk_color = "#10b981"
        risk_desc = "Balanced team contribution. Low structural risk."

    # -----------------------------
    # Layout
    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader("SPDI Metrics")
        st.markdown(f"<h1 style='color:{risk_color}; text-align:center'>{risk_level}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center'>Overall SPDI: {spdi_final:.3f}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center'>SPDI (Batsmen): {spdi_bat:.3f} | SPDI (Bowlers): {spdi_bowl:.3f}</p>", unsafe_allow_html=True)
        st.info(risk_desc)

        # Contribution bars for batting & bowling
        contrib_df = pd.DataFrame({
            "Player": ["Star Batter 1", "Star Batter 2", "Star Bowler 1", "Star Bowler 2"],
            "Contribution": [rb1/total_runs, rb2/total_runs, wb1/total_wickets, wb2/total_wickets],
            "Type": ["Batsman","Batsman","Bowler","Bowler"]
        })
        fig_bar = px.bar(contrib_df, x="Player", y="Contribution", color="Type",
                         text=contrib_df["Contribution"].apply(lambda x: f"{x*100:.1f}%"),
                         color_discrete_map={"Batsman":"#2563eb","Bowler":"#10b981"})
        fig_bar.update_layout(yaxis_title="Contribution Fraction", xaxis_title="Player", showlegend=True)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("Historical SPDI Trend")
        # Simulated historical SPDI
        history_data = pd.DataFrame({
            "Match": ["Match 1","Match 2","Match 3","Match 4","Live Match"],
            "SPDI": [0.53,0.34,0.22,0.45,spdi_final]
        })
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=history_data["Match"], y=history_data["SPDI"],
            mode='lines+markers+text',
            line=dict(color="#2563eb", width=3),
            marker=dict(size=12),
            text=history_data["SPDI"].apply(lambda x: f"{x:.2f}"),
            textposition="top center"
        ))
        fig_line.update_layout(
            yaxis=dict(range=[0,1], title="SPDI Value"),
            xaxis_title="Matches",
            title="Team SPDI Trend",
            template="plotly_white"
        )
        st.plotly_chart(fig_line, use_container_width=True)

# -----------------------------
st.markdown("""
---
**Author:** Saranyo Deyasi | Class 7, Asian International School  
**Note:** SPDI is a rule-based metric to analyze structural dependency on star players.  
Interactive Streamlit version developed for live testing and analysis.
""")
