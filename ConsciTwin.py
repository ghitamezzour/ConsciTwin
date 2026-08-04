import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time # <--- This was likely missing!

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

    def update(self, distance):
        if distance < 8.0:
            self.trust = max(0, self.trust - 30)
        else:
            self.trust = min(100, self.trust + 5)
            
    def get_decision(self, coach_cmd):
        if self.risk > 0.8: return "Catenaccio (Physics Veto)"
        if self.trust < 40: return "Catenaccio (Trust Drop)"
        return coach_cmd

class AutonomicLayer:
    def execute(self, decision):
        if "Catenaccio" in decision: return 2.0
        elif "False Nine" in decision: return 5.0
        return 3.5

# ==========================================
# STREAMLIT DASHBOARD
# ==========================================
st.set_page_config(layout="wide")
st.title("ConsciTwin: Online 3D MVP")

# Sidebar: The Control Panel (Layer 1 & 2)
st.sidebar.header("The Coach (Layer 1)")
strategy = st.sidebar.selectbox("Select Tactic:", ["Balanced", "Catenaccio (Defensive)", "False Nine (Aggressive)"])

st.sidebar.header("The Environment (Layer 2)")
weather_risk = st.sidebar.slider("Weather / Physics Risk", 0.0, 1.0, 0.1)
swerve_trigger = st.sidebar.button("🚨 Trigger: Teammate Swerves")

# Initialize Logic
translator = Translator()
twin = CognitiveCore()
player = AutonomicLayer()

# ==========================================
# THE LIVE SIMULATION LOOP
# ==========================================
# Simulate distance
if swerve_trigger:
    distance = 3.0
else:
    distance = 12.0 + 3.0 * np.sin(time.time() * 0.5)

# Run the Twin
twin.update(distance)
coach_cmd = translator.set_strategy(strategy)
twin.risk = weather_risk
decision = twin.get_decision(coach_cmd)
speed = player.execute(decision)

# ==========================================
# 3D VISUALIZATION (Plotly)
# ==========================================
ego_z = 0
teammate_z = distance

# Determine color and label
if twin.trust > 75:
    color = "green"
    label = "Teammate (Trusted)"
elif twin.trust > 40:
    color = "yellow"
    label = "Teammate (Unreliable)"
else:
    color = "red"
    label = "Obstacle (Low Trust)"

# Force a default trace so the graph never fails
fig = go.Figure()
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers', marker=dict(size=1, color='white', opacity=0), 
    showlegend=False
))

# Draw the Road
fig.add_trace(go.Scatter3d(
    x=[0, 0], y=[0, 0], z=[-10, 20],
    mode='lines', line=dict(color='white', width=5), name='Road'
))

# Draw the Ego Car (Blue)
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[ego_z],
    mode='markers', marker=dict(size=15, color='blue'), name='Ego (ConsciTwin)'
))

# Draw the Teammate
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[teammate_z],
    mode='markers', marker=dict(size=15, color=color), name=label
))

fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(title="Distance (m)", range=[0, 20]),
        camera=dict(eye=dict(x=-1.5, y=1.5, z=0.5))
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    height=500
)

# ==========================================
# DISPLAY
# ==========================================
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric("Trust Meter", f"{twin.trust:.1f}%")
    st.metric("Distance", f"{distance:.1f} m")
    st.metric("Final Decision", decision)
    
    st.text_area("Live Audit Log", 
        f"Coach: {coach_cmd}\n"
        f"Trust: {twin.trust:.1f}%\n"
        f"Risk: {twin.risk*100:.0f}%\n"
        f"Decision: {decision}"
    )
