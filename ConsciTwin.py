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
st.set_page_config(layout="wide", page_title="ConsciTwin")
st.title("ConsciTwin: The Self-Critiquing Digital Twin")

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
# THE TACTICAL GRID VISUALIZATION
# ==========================================
fig = go.Figure()

# 1. Bright Tactical Pitch Background (FORCED RANGE)
# We force the X-axis to go from -15 to 15, and Y-axis from -10 to 30
fig.add_shape(type="rect", x0=-15, y0=-10, x1=15, y1=30,
              line=dict(color="black", width=2),
              fillcolor="rgba(240, 240, 240, 1)") # Light Grey Background

# 2. Draw Tactical Grid Lines
for y in range(-5, 30, 5):
    fig.add_trace(go.Scatter(
        x=[-12, 12], y=[y, y],
        mode='lines', line=dict(color='white', width=2),
        showlegend=False, hoverinfo='none'
    ))

# 3. Draw the Ego Car (Blue - ConsciTwin)
ego_x = -2.0
ego_y = 2.0
fig.add_trace(go.Scatter(
    x=[ego_x], y=[ego_y],
    mode='markers+text',
    marker=dict(size=30, color='blue', symbol='square', line=dict(width=2, color='black')),
    text=["Ego"], textposition="bottom center", textfont=dict(color='black', size=14, family="Arial Black"),
    name='Ego (ConsciTwin)'
))

# 4. Draw the Teammate
team_x = 2.0
team_y = ego_y + distance
team_color = "#00CC00" if twin.trust > 60 else "#CC0000"
team_label = "Teammate" if twin.trust > 60 else "Teammate (SWERVING!)"

fig.add_trace(go.Scatter(
    x=[team_x], y=[team_y],
    mode='markers+text',
    marker=dict(size=30, color=team_color, symbol='circle', line=dict(width=2, color='black')),
    text=[team_label], textposition="top center", textfont=dict(color='black', size=14, family="Arial Black"),
    name='Teammate'
))

# 5. Override Warning Sign
if "Veto" in analysis["Decision"] or "Trust Drop" in analysis["Decision"]:
    fig.add_annotation(
        x=0, y=15,
        text=f"⚠️ TWIN OVERRIDE: {analysis['Reason']}",
        showarrow=False,
        font=dict(color="red", size=18, family="Arial Black")
    )

# 6. Final Styling (Explicitly forced ranges)
fig.update_layout(
    title="Live Tactical Grid",
    xaxis=dict(range=[-15, 15], showgrid=False, zeroline=False, visible=False),
    yaxis=dict(range=[-10, 30], showgrid=False, zeroline=False, visible=False), # <--- FORCED RANGE
    height=600,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='black'),
    showlegend=True,
    legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)')
)

# ==========================================
# DISPLAY
# ==========================================
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📋 Live Audit Log")
    st.metric("Trust Meter", f"{twin.trust:.1f}%")
    st.metric("Physics Risk", f"{twin.risk*100:.0f}%")
    
    st.info(f"👤 **Coach Command:** {analysis['Coach_Command']}")
    st.success(f"🧠 **Twin Analysis:** {analysis['Reason']}")
    st.warning(f"⚖️ **Twin Final Decision:** {analysis['Decision']}")
