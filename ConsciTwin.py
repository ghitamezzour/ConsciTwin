import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

# ==========================================
# CONSCITWIN LAYERS (The Ethical Logic)
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
        # ETHICAL CHECK 1: The Trust Meter
        # If the Teammate gets too close (< 10m), we treat it as swerving.
        if distance < 10.0:
            self.trust = max(0, self.trust - 25) # Trust drops
        else:
            self.trust = min(100, self.trust + 2) # Trust slowly recovers
            
    def get_decision(self, coach_cmd):
        # ETHICAL CHECK 2: The Priority Scheduler
        # Rule: Physics Risk > Trust Drop > Coach Command
        
        if self.risk > 0.8:
            return "OVERRIDE: Physics Veto (Ice Detected)"
        if self.trust < 40:
            return "OVERRIDE: Trust Drop (Swerve Detected)"
        
        # ETHICAL PASS: The Coach's command is safe
        return f"EXECUTE: {coach_cmd}"

class AutonomicLayer:
    def execute(self, decision):
        # The "Player" translates the ethical decision into physical speed
        if "OVERRIDE" in decision:
            return 20.0 # SLOW DOWN (Ethical override)
        elif "Catenaccio" in decision:
            return 35.0
        elif "False Nine" in decision:
            return 65.0
        return 45.0

# ==========================================
# STREAMLIT UI
# ==========================================
st.set_page_config(layout="wide")
st.title("ConsciTwin: Ethical Driving MVP")

st.markdown("""
**The Ethical Loop:** The Coach sets the strategy. The Twin checks the road. 
If the environment is unsafe (Swerve or Ice), **the Twin overrides the Coach** and slows the car down.
""")

# Sidebar: The Controls
st.sidebar.header("Layer 1: The Coach (Human)")
strategy = st.sidebar.selectbox("Select Driving Strategy:", ["Balanced", "Catenaccio (Defensive)", "False Nine (Aggressive)"])

st.sidebar.header("Layer 2: The Environment (Twin)")
weather_risk = st.sidebar.slider("Weather Risk (Ice / Rain)", 0.0, 1.0, 0.1)
swerve_trigger = st.sidebar.button("🚨 Simulate: Teammate Swerves")

# Initialize Logic
translator = Translator()
twin = CognitiveCore()
player = AutonomicLayer()

# ==========================================
# THE ETHICAL SIMULATION LOOP
# ==========================================
# Simulate the distance to the Teammate
if swerve_trigger:
    distance = 5.0  # Suddenly close (Swerve detected)
else:
    # A gentle sine wave representing normal driving distance
    distance = 15.0 + 2.0 * np.sin(time.time() * 0.3) 

# Run the Twin's Ethical Checks
twin.update(distance)
coach_cmd = translator.set_strategy(strategy)
twin.risk = weather_risk
decision = twin.get_decision(coach_cmd) # This is where the override happens
speed = player.execute(decision)        # This is where the car obeys the override

# ==========================================
# THE ROAD VISUALIZATION (Top-Down View)
# ==========================================
fig = go.Figure()

# 1. Draw the Road
fig.add_shape(type="rect", x0=-5, y0=-2, x1=5, y1=35,
              line=dict(color="White", width=2),
              fillcolor="rgba(50, 50, 50, 0.8)") # Dark road

# Draw Lane Lines
for y in range(0, 35, 5):
    fig.add_trace(go.Scatter(
        x=[-1, 1], y=[y, y+2],
        mode='lines', line=dict(color='white', width=1, dash='dash'),
        showlegend=False, hoverinfo='none'
    ))

# 2. Draw the Ego Car (Blue - Your ConsciTwin car)
# The Ego car is positioned near the bottom.
ego_y = 2.0
fig.add_trace(go.Scatter(
    x=[0], y=[ego_y],
    mode='markers+text',
    marker=dict(size=20, color='blue', symbol='square'),
    text=["Ego Car"], textposition="top center",
    name='Ego (ConsciTwin)'
))

# 3. Draw the Teammate (Red - The car ahead)
# The Teammate's position depends on the distance calculated above.
teammate_y = ego_y + distance
team_color = "green" if twin.trust > 60 else "red"
team_label = "Teammate (Safe)" if twin.trust > 60 else "Teammate (Swerving!)"

fig.add_trace(go.Scatter(
    x=[0], y=[teammate_y],
    mode='markers+text',
    marker=dict(size=20, color=team_color, symbol='square'),
    text=[team_label], textposition="top center",
    name='Teammate'
))

# 4. Draw a visual "Warning" banner if the system overrides the Coach
if "OVERRIDE" in decision:
    fig.add_annotation(
        x=0, y=18,
        text="⚠️ ETHICAL OVERRIDE: System vetoed the Coach!",
        showarrow=False,
        font=dict(color="red", size=16)
    )

# Style the chart
fig.update_layout(
    title="Live Road View (Top-Down)",
    xaxis=dict(range=[-5, 5], showgrid=False, zeroline=False, visible=False),
    yaxis=dict(range=[-2, 35], showgrid=False, zeroline=False, visible=False),
    height=600,
    plot_bgcolor='#1a1a1a',
    paper_bgcolor='#1a1a1a',
    font=dict(color='white'),
    showlegend=True,
    legend=dict(x=0.02, y=0.98, bgcolor='rgba(0,0,0,0.5)')
)

# ==========================================
# DISPLAY: THE DASHBOARD & AUDIT LOG
# ==========================================
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Live Ethical Audit Log")
    st.metric("Trust Meter", f"{twin.trust:.1f}%", delta_color="inverse")
    st.metric("Weather Risk", f"{twin.risk*100:.0f}%")
    st.metric("Current Speed", f"{speed:.0f} km/h")
    
    # The "Ethical Proof" Text
    st.info(f"**Coach Command:** {coach_cmd}")
    if "OVERRIDE" in decision:
        st.error(f"🚨 **SYSTEM OVERRIDE:** {decision}")
        st.success("✅ The Twin protected the car from an unsafe decision.")
    else:
        st.success(f"✅ **Safe Execution:** {decision}")
