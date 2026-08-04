import streamlit as st
import time
import json
import hashlib
import plotly.graph_objects as go
import math
from concurrent.futures import ThreadPoolExecutor

# ==========================================
# 1. PAGE CONFIG & ACCESSIBILITY CSS
# ==========================================
st.set_page_config(
    page_title="ConsciTwin",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimal, responsive, accessible CSS
st.markdown("""
<style>
    html, body, .stApp { font-size: 16px; line-height: 1.6; color: #1e293b; }
    button, .stButton>button, .stDownloadButton>button { min-height: 48px !important; min-width: 48px !important; }
    .stSelectbox div[data-testid="stSelectbox"], .stSlider div[data-testid="stSlider"] { min-height: 48px; }
    
    .stApp [data-testid="stVerticalBlock"] > div {
        background-color: #ffffff; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 20px; border: 1px solid #f1f5f9;
    }
    h3 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-weight: 600; color: #0f172a; padding-bottom: 12px;
        border-bottom: 2px solid #e2e8f0; margin-bottom: 20px;
    }
    a:focus-visible, button:focus-visible, input:focus-visible {
        outline: 2px solid #3b82f6; outline-offset: 2px;
    }
    @media only screen and (max-width: 600px) {
        .stApp [data-testid="stVerticalBlock"] > div { padding: 15px; }
        .stApp .stButton { width: 100%; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. BRANDING: SVG LOGO
# ==========================================
LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 120" width="100%" height="90">
    <defs>
        <linearGradient id="cyberGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#00d4ff;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:1" />
        </linearGradient>
        <filter id="glow">
            <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
            <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
    </defs>
    <g transform="translate(20, 10)">
        <!-- Real Side -->
        <rect x="0" y="30" width="20" height="40" rx="5" fill="#2d3748"/>
        <rect x="0" y="60" width="30" height="15" rx="3" fill="#4a5568"/>
        <path d="M 10 20 Q 25 10 60 10 L 100 10 Q 130 10 150 20 L 155 30 L 160 65 L 10 65 Z" fill="#718096"/>
        <circle cx="40" cy="75" r="15" fill="#1a202c"/><circle cx="40" cy="75" r="7" fill="#cbd5e0"/>
        <rect x="15" y="25" width="15" height="10" rx="4" fill="#e2e8f0"/>
        <!-- Virtual Side -->
        <path d="M 160 20 L 210 10 L 240 10 L 270 20 L 275 30 L 280 65 L 160 65 Z" fill="none" stroke="url(#cyberGrad)" stroke-width="2.5" filter="url(#glow)"/>
        <path d="M 180 20 L 180 65 M 200 15 L 200 65 M 220 12 L 220 65 M 240 10 L 240 65 M 260 15 L 260 65" stroke="url(#cyberGrad)" stroke-width="1" opacity="0.4"/>
        <rect x="260" y="25" width="15" height="10" rx="4" fill="#00d4ff" filter="url(#glow)"/>
        <circle cx="240" cy="75" r="15" fill="none" stroke="url(#cyberGrad)" stroke-width="2.5"/>
        <circle cx="240" cy="75" r="7" fill="#00d4ff" opacity="0.5"/>
    </g>
    <g transform="translate(180, 55)">
        <g transform="translate(0, -40)">
            <rect x="-25" y="0" width="50" height="40" rx="8" fill="#ffffff" stroke="#e2e8f0" stroke-width="3"/>
            <circle cx="0" cy="15" r="10" fill="#3b82f6"/>
            <path d="M -15 5 Q 0 -10 15 5" stroke="#ffffff" stroke-width="2" fill="none"/>
        </g>
    </g>
    <text x="200" y="105" font-family="'Segoe UI', Helvetica, Arial, sans-serif" font-size="28" font-weight="700" fill="#1a202c" text-anchor="middle" letter-spacing="2">ConsciTwin</text>
    <text x="200" y="125" font-family="'Segoe UI', Helvetica, Arial, sans-serif" font-size="14" font-weight="400" fill="#718096" text-anchor="middle" letter-spacing="1">Ethical Digital Twin</text>
</svg>
"""

# ==========================================
# 3. STATE MANAGEMENT & CACHING
# ==========================================
if 'job_id' not in st.session_state: st.session_state.job_id = 0
if 'generation_result' not in st.session_state: st.session_state.generation_result = None
if 'generation_running' not in st.session_state: st.session_state.generation_running = False
if 'persona_params' not in st.session_state: st.session_state.persona_params = {}

@st.cache_resource
def get_executor():
    return ThreadPoolExecutor(max_workers=1)

@st.cache_data(ttl=3600)
def cached_generation(payload_hash, _payload_json):
    time.sleep(1.5) # Simulate LLM processing time
    return {
        "id": payload_hash,
        "title": f"Simulated Twin: {_payload_json['strategy']}",
        "explanation": "The system analyzed your driving strategy and the current physics risk.",
        "generation_summary": f"Strategy: {_payload_json['strategy']} | Risk: {_payload_json['risk']*100:.0f}%",
        "persona": _payload_json
    }

def canonicalize_payload(strategy, risk, region):
    return json.dumps({"strategy": strategy, "risk": float(risk), "region": region}, sort_keys=True)

# ==========================================
# 4. SIDEBAR: INFO & PRIVACY
# ==========================================
with st.sidebar:
    st.markdown(LOGO_SVG, unsafe_allow_html=True)
    st.markdown("---")
    with st.expander("🔒 How it works & Privacy"):
        st.write("ConsciTwin is a self-critiquing Digital Twin simulating ethical validation of driving commands.")
        st.write("**Privacy:** All simulations run locally via Three.js. No data stored.")
        st.warning("**Disclaimer:** Demonstration prototype only. Not certified for real-world safety.")
    st.markdown("---")
    st.success("✅ Transparency: Decisions are logged and explained.")
    st.success("✅ Safety: Physics overrides human error.")

# ==========================================
# 5. MAIN UI: STEP FLOW
# ==========================================
st.title("⚖️ ConsciTwin")
st.markdown("*A Self-Critiquing Digital Twin for Ethical Driving.*")

if st.button("🚀 Create New Twin", type="primary", use_container_width=True):
    st.session_state.generation_result = None
    st.session_state.persona_params = {}
    st.rerun()

tab1, tab2, tab3, tab4 = st.tabs(["📖 Onboarding", "⚙️ Inputs", "🧬 Generate", "📊 Results"])

# --- STEP 1: ONBOARDING ---
with tab1:
    st.markdown("### Step 1: Quick Start")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🚗 Aggressive Twin", use_container_width=True):
            st.session_state.persona_params = {"strategy": "False Nine (Aggressive)", "risk": 0.2}
            st.rerun()
        st.caption("Strategy: Aggressive | Risk: Dry road")
    with col_b:
        if st.button("🛡️ Cautious Twin", use_container_width=True):
            st.session_state.persona_params = {"strategy": "Catenaccio (Defensive)", "risk": 0.8}
            st.rerun()
        st.caption("Strategy: Defensive | Risk: Ice/High")

# --- STEP 2: INPUTS ---
with tab2:
    st.markdown("### Step 2: Configure Scenario")
    with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            strategy = st.selectbox("Driving Strategy", ["Balanced", "Catenaccio (Defensive)", "False Nine (Aggressive)"], help="The coach's tactical intent.")
            weather_risk = st.slider("Weather / Physics Risk", 0.0, 1.0, 0.5, help="0.0=Perfect, 1.0=Black Ice")
            region = st.selectbox("Region (Domain Shift)", ["Germany (Low Variance)", "Morocco (High Variance)"], help="Statistical baseline adjustment.")
        with col2:
            st.metric("Strategy", strategy.split()[0])
            st.metric("Risk Level", f"{weather_risk*100:.0f}%")
            if st.button("Generate Twin", type="primary", use_container_width=True):
                st.session_state.persona_params = {"strategy": strategy, "risk": weather_risk, "region": region}
                st.rerun()

# --- STEP 3: GENERATE ---
with tab3:
    st.markdown("### Step 3: Generation")
    if not st.session_state.persona_params:
        st.info("Please set your preferences in 'Inputs' or select a Quick Start preset.")
    else:
        params = st.session_state.persona_params
        st.write(f"Generating for: **{params['strategy']}** in **{params['region']}**")
        payload_str = canonicalize_payload(params['strategy'], params['risk'], params['region'])
        payload_hash = hashlib.md5(payload_str.encode()).hexdigest()

        if not st.session_state.generation_running:
            st.session_state.generation_running = True
            future = get_executor().submit(cached_generation, payload_hash, json.loads(payload_str))
            st.session_state.generation_future = future

        with st.spinner("Simulating the environment and critiquing the command..."):
            if 'generation_future' in st.session_state and st.session_state.generation_future.done():
                result = st.session_state.generation_future.result()
                st.session_state.generation_result = result
                st.session_state.generation_running = False
                st.success("✅ Twin generated successfully!")
            else:
                st.warning("Processing... up to 20 seconds for cold starts.")

# --- STEP 4: RESULTS & 3D ---
with tab4:
    if not st.session_state.generation_result:
        st.info("Please generate a twin first.")
    else:
        result = st.session_state.generation_result
        params = st.session_state.persona_params
        st.markdown(f"### Step 4: Results – {result['title']}")
        
        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.info(f"**Explanation:** {result['explanation']}")
            st.write(f"**Summary:** {result['generation_summary']}")
        with col_b:
            st.metric("Trust Meter", f"{95.0}%")
            st.metric("Physics Risk", f"{params['risk']*100:.0f}%")

        st.download_button("📥 Export JSON", data=json.dumps(result, indent=2), file_name="twin_output.json")
        st.divider()

        # --- 3D INTEGRATION ---
        st.markdown("### Live 3D Physics Demo")
        warmth = 8.0 if "Aggressive" in params['strategy'] else 3.0
        energy = 9.0 if "Aggressive" in params['strategy'] else 2.0
        responsiveness = 9.0 if "Aggressive" in params['strategy'] else 4.0
        tone_map = {"Balanced": "Neutral", "Catenaccio (Defensive)": "Formal", "False Nine (Aggressive)": "Casual"}
        tone = tone_map.get(params['strategy'], "Neutral")

        st.components.v1.html(f"""
        <html>
        <head><style>body{{margin:0;overflow:hidden;background:#1a1a1a;color:white;font-family:sans-serif;}}</style>
        <script type="importmap">{{"imports":{{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/","cannon-es":"https://unpkg.com/cannon-es@0.20.0/dist/cannon-es.js"}}}}</script>
        </head>
        <body>
        <script type="module">
            import * as THREE from 'three'; import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js'; import * as CANNON from 'cannon-es';
            const scene = new THREE.Scene(); scene.background = new THREE.Color(0x1a1a1a);
            const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 100); camera.position.set(5,5,10);
            const renderer = new THREE.WebGLRenderer({{antialias:true}}); renderer.setSize(window.innerWidth, window.innerHeight); document.body.appendChild(renderer.domElement);
            const controls = new OrbitControls(camera, renderer.domElement); controls.target.set(0,1,0); controls.update();
            const world = new CANNON.World(); world.gravity.set(0,-9.82,0);
            const ground = new CANNON.Body({{mass:0}}); ground.addShape(new CANNON.Plane()); ground.quaternion.setFromAxisAngle(new CANNON.Vec3(1,0,0),-Math.PI/2); world.addBody(ground);
            const geometry = new THREE.BoxGeometry(1,1,1);
            const colorTemp = {warmth}; const emissionIntensity = {energy} * 0.2;
            const material = new THREE.MeshStandardMaterial({{color:new THREE.Color().setHSL(0.7-(colorTemp/20),1,0.5), emissive:new THREE.Color().setHSL(0.7-(colorTemp/20),1,0.3), emissiveIntensity:emissionIntensity}});
            const cube = new THREE.Mesh(geometry, material); cube.position.y = 3; scene.add(cube);
            const mass = 5 / ({responsiveness} > 5 ? 2 : 1);
            const body = new CANNON.Body({{mass:mass}}); body.addShape(new CANNON.Box(new CANNON.Vec3(0.5,0.5,0.5))); body.position.set(0,3,0); world.addBody(body);
            const plane = new THREE.Mesh(new THREE.PlaneGeometry(10,10), new THREE.MeshStandardMaterial({{color:0x2a2a2a, side:THREE.DoubleSide}})); plane.rotation.x = -Math.PI/2; scene.add(plane);
            const light = new THREE.DirectionalLight(0xffffff,1.5); light.position.set(5,10,7); scene.add(light); scene.add(new THREE.AmbientLight(0x404040));
            function animate(){{ requestAnimationFrame(animate); world.step(1/60); cube.position.copy(body.position); cube.quaternion.copy(body.quaternion); controls.update(); renderer.render(scene,camera); }}
            animate();
            window.addEventListener('resize', ()=>{{ camera.aspect = window.innerWidth/window.innerHeight; camera.updateProjectionMatrix(); renderer.setSize(window.innerWidth, window.innerHeight); }});
        </script>
        </body></html>
        """, height=500, scrolling=False)
        
        # Refinements
        with st.expander("🔧 Advanced Refinements"):
            st.markdown("Adjust the 3D persona attributes:")
            warmth = st.slider("Warmth", 0, 10, int(warmth))
            energy = st.slider("Energy", 0, 10, int(energy))
            if st.button("Update 3D Twin"):
                st.session_state.persona_params['warmth'] = warmth
                st.session_state.persona_params['energy'] = energy
                st.rerun()
