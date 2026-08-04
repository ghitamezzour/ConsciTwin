import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

# ==========================================
# CONSCITWIN LAYERS
# ==========================================
class Translator:
    def set_strategy(self, user_input):
        if "Defensive" in user_input: return "Catenaccio"
        elif "Aggressive" in user_input: return "False Nine"
        return "Balanced"

class CognitiveCore:
    def __init__(self):
        self.trust = 90.0
        self.risk = 0.0
        self.analysis_log = []

    def update(self, distance):
        if distance < 10.0:
            self.trust = max(0, self.trust - 25)
        else:
            self.trust = min(100, self.trust + 2)
            
    def get_decision(self, coach_cmd):
        # The Twin's Analysis (The Self-Critique)
        analysis = {
            "Coach_Command": coach_cmd,
            "Trust_Meter": self.trust,
            "Physics_Risk": self.risk,
            "Decision": coach_cmd,
            "Reason": "All systems nominal."
        }
        
        if self.risk > 0.8:
            analysis["Decision"] = "Catenaccio (Physics Veto)"
            analysis["Reason"] = "Twin detected high ice risk. Physics safety margin exceeded."
        elif self.trust < 40:
            analysis["Decision"] = "Catenaccio (Trust Drop)"
            analysis["Reason"] = "Twin detected swerving teammate. Reclassified as Obstacle."
        
        self.analysis_log.append(analysis)
        return analysis

class AutonomicLayer:
    def execute(self, decision):
        if "Veto" in decision or "Trust Drop" in decision: return 20.0
        elif "Catenaccio" in decision: return 35.0
        elif "False Nine" in decision: return 65.0
        return 45.0

# ==========================================
# STREAMLIT UI
# ==========================================
st.set_page_config(layout="wide")
st.title("ConsciTwin: The Self-Critiquing Twin")

st.markdown("""
**The Real Value:** The Twin doesn't just drive. It **critiques itself** and shows you the math behind every decision.
""")

# Sidebar
st.sidebar.header("The Coach (Human)")
strategy = st.sidebar.selectbox("Select Strategy:", ["Balanced", "Catenaccio (Defensive)", "False Nine (Aggressive)"])

st.sidebar.header("The Environment")
weather_risk = st.sidebar.slider("Weather / Physics Risk", 0.0, 1.0, 0.1)
swerve_trigger = st.sidebar.button("🚨 Simulate: Teammate Swerves")

# Initialize
translator = Translator()
twin = CognitiveCore()
player = AutonomicLayer()

# Simulation Data
if swerve_trigger:
    distance = 5.0
else:
    distance = 15.0 + 2.0 * np.sin(time.time() * 0.3)

twin.update(distance)
coach_cmd = translator.set_strategy(strategy)
twin.risk = weather_risk
analysis = twin.get_decision(coach_cmd)
speed = player.execute(analysis["Decision"])

# ==========================================
# THE ROAD VISUALIZATION
# ==========================================
fig = go.Figure()

# Road
fig.add_shape(type="rect", x0=-5, y0=-2, x1=5, y1=35,
              line=dict(color="White", width=2),
              fillcolor="rgba(30, 30, 30, 0.8)")

# Lane lines
for y in range(0, 35, 5):
    fig.add_trace(go.Scatter(
        x=[-1, 1], y=[y, y+2],
        mode='lines', line=dict(color='white', width=1, dash='dash'),
        showlegend=False, hoverinfo='none'
    ))

# Ego Car (Blue)
ego_y = 2.0
fig.add_trace(go.Scatter(
    x=[0], y=[ego_y],
    mode='markers+text', marker=dict(size=20, color='blue', symbol='square'),
    text=["Ego"], textposition="bottom center",
    name='Ego Car (ConsciTwin)'
))

# Teammate (Red)
team_y = ego_y + distance
team_color = "green" if twin.trust > 60 else "red"
team_label = "Teammate (Normal)" if twin.trust > 60 else "Teammate (Swerving!)"

fig.add_trace(go.Scatter(
    x=[0], y=[team_y],
    mode='markers+text', marker=dict(size=20, color=team_color, symbol='circle'),
    text=[team_label], textposition="top center",
    name='Teammate'
))

# Self-Critique Banner
if "Veto" in analysis["Decision"] or "Trust Drop" in analysis["Decision"]:
    fig.add_annotation(
        x=0, y=18,
        text=f"🧠 TWIN SELF-CRITIQUE: {analysis['Reason']}",
        showarrow=False, font=dict(color="orange", size=14)
    )

fig.update_layout(
    title="Live Road View (The Twin's Perspective)",
    xaxis=dict(range=[-5, 5], showgrid=False, zeroline=False, visible=False),
    yaxis=dict(range=[-2, 35], showgrid=False, zeroline=False, visible=False),
    height=600,
    plot_bgcolor='#1a1a1a', paper_bgcolor='#1a1a1a',
    font=dict(color='white')
)

# ==========================================
# THE "SELF-CRITIQUE" DASHBOARD
# ==========================================
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("The Twin's Self-Critique")
    
    st.metric("Trust Meter", f"{twin.trust:.1f}%")
    st.metric("Physics Risk", f"{twin.risk*100:.0f}%")
    st.metric("Current Speed", f"{speed:.0f} km/h")
    
    st.info(f"**Coach Command:** {analysis['Coach_Command']}")
    st.success(f"**Twin Analysis:** {analysis['Reason']}")
    st.warning(f"**Twin Final Decision:** {analysis['Decision']}")
    
    st.markdown("---")
    st.subheader("📋 Live Audit Log")
    
    # Show the last 3 decisions
    for entry in twin.analysis_log[-3:]:
        st.caption(f"🕒 {time.strftime('%H:%M:%S')} - {entry['Reason']}")
        st.caption(f"   -> Final: {entry['Decision']}")
