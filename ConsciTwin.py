import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time
import math

# ==========================================
# 1. PAGE CONFIG & BRANDING
# ==========================================
st.set_page_config(
    page_title="ConsciTwin",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Modern, Minimal Design
st.markdown("""
<style>
    /* Main Container Styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Card Styling */
    .stApp [data-testid="stVerticalBlock"] > div {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 20px;
    }
    
    /* Step Headers */
    h3 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 600;
        color: #1e293b;
        padding-bottom: 10px;
        border-bottom: 2px solid #e2e8f0;
        margin-bottom: 20px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #f8fafc;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
    }
    
    /* Brand Colors */
    .brand-primary { color: #3b82f6; }
    .brand-secondary { color: #10b981; }
    .brand-accent { color: #f59e0b; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CONSCITWIN LOGIC ENGINE (CACHED)
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
            "Reason": "All systems nominal.",
            "Status": "Agreement"
        }
        if self.risk > 0.8:
            analysis["Decision"] = "Catenaccio (Physics Veto)"
            analysis["Reason"] = "Twin detected high ice risk. Physics safety margin exceeded."
            analysis["Status"] = "Override"
        elif self.trust < 40:
            analysis["Decision"] = "Catenaccio (Trust Drop)"
            analysis["Reason"] = "Twin detected swerving teammate. Reclassified as Obstacle."
            analysis["Status"] = "Override"
        self.analysis_log.append(analysis)
        return analysis

class AutonomicLayer:
    def execute(self, decision):
        if "Veto" in decision or "Trust Drop" in decision: return 20.0
        elif "Catenaccio" in decision: return 35.0
        elif "False Nine" in decision: return 65.0
        return 45.0

# ==========================================
# 3. SIDEBAR: HOW IT WORKS & TRUST
# ==========================================
with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=ConsciTwin", use_column_width=True)
    st.markdown("---")
    st.header("How ConsciTwin Works")
    st.info("ConsciTwin is a self-critiquing Digital Twin. It acts as a safety referee, analyzing the environment and overriding unsafe human commands.")
    
    st.markdown("---")
    st.header("Ethical Guidelines")
    st.success("✅ **Transparency:** Every decision is logged and explained.")
    st.success("✅ **Safety First:** Physics and Trust override human error.")
    st.success("✅ **Continuous Learning:** The system adapts to regional driving behaviors.")
    
    st.markdown("---")
    st.caption("🔒 Privacy Note: No real-world data is stored. All simulations are local.")

# ==========================================
# 4. MAIN APP: THE 5-STEP FLOW
# ==========================================
st.title("🧠 ConsciTwin")
st.markdown("*The Self-Critiquing Digital Twin for Ethical Driving.*")

# --- STEP 1: ONBOARDING ---
with st.container():
    st.markdown("### Step 1: Onboarding & Sample Personas")
    st.markdown("Welcome! ConsciTwin analyzes driving environments and automatically overrides unsafe human commands. Here are two sample scenarios to get you started:")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("**Persona A: The Aggressive Driver**\n\n- Strategy: False Nine (Aggressive)\n- Setting: Dry, clear highway.")
    with col_b:
        st.success("**Persona B: The Cautious Driver**\n\n- Strategy: Catenaccio (Defensive)\n- Setting: Rainy, unpredictable traffic.")

# --- STEP 2: INPUT COLLECTION ---
with st.container():
    st.markdown("### Step 2: Configure Your Driving Scenario")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        strategy = st.selectbox(
            "Select Driving Strategy:",
            ["Balanced", "Catenaccio (Defensive)", "False Nine (Aggressive)"],
            help="The Coach's intended driving style."
        )
        weather_risk = st.slider(
            "Weather / Physics Risk",
            0.0, 1.0, 0.2,
            help="0.0 = Dry road, 1.0 = Black ice."
        )
    with col2:
        st.markdown("**Environment Simulation**")
        st.metric("Current Speed", "65 km/h", delta="Normal")
        st.metric("Weather Risk", f"{weather_risk*100:.0f}%", delta="Incoming")

# --- STEP 3: CONSCITWIN GENERATION (The Simulation) ---
with st.container():
    st.markdown("### Step 3: Twin Generation & Self-Critique")
    
    if st.button("🚀 Run ConsciTwin Simulation", type="primary"):
        with st.spinner("ConsciTwin is analyzing the environment and critiquing its own decisions..."):
            time.sleep(1.5) # Simulate processing time
            
            # Initialize Logic
            translator = Translator()
            twin = CognitiveCore()
            player = AutonomicLayer()
            
            # Simulate Distance
            distance = 15.0 + 2.0 * math.sin(time.time() * 0.3)
            
            # Run the Twin
            twin.update(distance)
            coach_cmd = translator.set_strategy(strategy)
            twin.risk = weather_risk
            analysis = twin.get_decision(coach_cmd)
            speed = player.execute(analysis["Decision"])
            
            # Store in Session State for persistence
            st.session_state['analysis'] = analysis
            st.session_state['speed'] = speed
            st.session_state['distance'] = distance
            st.session_state['twin'] = twin
            
            st.success("✅ Simulation complete! Review the Twin's self-critique below.")
    else:
        st.info("Click the button above to generate a new simulation.")

# Display Output if it exists
if 'analysis' in st.session_state:
    analysis = st.session_state['analysis']
    twin = st.session_state['twin']
    speed = st.session_state['speed']
    
    # --- STEP 4: OUTPUT VISUALIZATION (The Tactical Grid) ---
    fig = go.Figure()
    fig.add_shape(type="rect", x0=-20, y0=-10, x1=20, y1=40,
                  line=dict(color="black", width=2), fillcolor="rgba(240, 240, 240, 1)")
    
    for y in range(-5, 40, 5):
        fig.add_trace(go.Scatter(x=[-15, 15], y=[y, y], mode='lines', 
                                 line=dict(color='white', width=2), showlegend=False))
    
    # Ego Car (Blue)
    fig.add_trace(go.Scatter(x=[-3], y=[2], mode='markers+text',
        marker=dict(size=35, color='royalblue', symbol='square', line=dict(width=2, color='black')),
        text=["EGO"], textposition="bottom center", textfont=dict(color='black', size=14), name='Ego Car'))
    
    # Teammate (Green/Red)
    team_y = 2.0 + st.session_state['distance']
    team_color = "#00CC00" if twin.trust > 60 else "#CC0000"
    team_label = "TEAMMATE" if twin.trust > 60 else "SWERVING!"
    fig.add_trace(go.Scatter(x=[3], y=[team_y], mode='markers+text',
        marker=dict(size=35, color=team_color, symbol='circle', line=dict(width=2, color='black')),
        text=[team_label], textposition="top center", textfont=dict(color='black', size=14), name='Teammate'))
    
    # Override Warning
    if analysis["Status"] == "Override":
        fig.add_annotation(x=0, y=25, text=f"⚠️ TWIN SELF-CRITIQUE: {analysis['Reason']}",
                           showarrow=False, font=dict(color="red", size=16))

    fig.update_layout(title="Live Tactical Grid", xaxis=dict(range=[-20, 20], visible=False),
                      yaxis=dict(range=[-10, 40], visible=False), height=500,
                      plot_bgcolor='white', paper_bgcolor='white', showlegend=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("**Output Summary**")
        st.markdown(f"**Title:** {analysis['Decision']}")
        st.markdown(f"**Explanation:** {analysis['Reason']}")
        st.markdown(f"**Generation Summary:** The Twin analyzed the distance to the Teammate ({st.session_state['distance']:.1f}m) and the Physics Risk ({twin.risk*100:.0f}%) to reach this decision.")
        st.metric("Current Speed", f"{speed:.0f} km/h")

# --- STEP 5: REFINEMENT & NEXT STEPS ---
with st.container():
    st.markdown("### Step 5: Refine & Export")
    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_a:
        st.button("📋 Copy Audit Log", help="Copy the Twin's reasoning to clipboard.")
    with col_b:
        st.button("🔄 Regenerate Simulation", help="Run the simulation again with different random variables.")
    with col_c:
        st.download_button("📥 Export as JSON", data="{}", file_name="consciTwin_log.json", mime="application/json")
    
    st.markdown("---")
    st.markdown("**What's next?**")
    st.markdown("- Try adjusting the **Weather Risk** slider and regenerate the simulation to see how the Twin reacts to extreme conditions.")
    st.markdown("- Switch to a different **Driving Strategy** to see if the Twin agrees or overrides.")
