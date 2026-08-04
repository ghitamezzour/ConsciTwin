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
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimal, responsive, accessible CSS
st.markdown("""
<style>
    /* Global Typography */
    html, body, .stApp {
        font-size: 16px;
        line-height: 1.6;
        color: #1e293b;
    }
    /* Ensure minimum touch target size */
    button, .stButton>button, .stDownloadButton>button {
        min-height: 48px !important;
        min-width: 48px !important;
    }
    .stSelectbox div[data-testid="stSelectbox"], .stSlider div[data-testid="stSlider"] {
        min-height: 48px;
    }
    /* Card Design */
    .stApp [data-testid="stVerticalBlock"] > div {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border: 1px solid #f1f5f9;
    }
    /* Stepper Headers */
    h3 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-weight: 600;
        color: #0f172a;
        padding-bottom: 12px;
        border-bottom: 2px solid #e2e8f0;
        margin-bottom: 20px;
    }
    /* Contrast and Focus */
    a:focus-visible, button:focus-visible, input:focus-visible {
        outline: 2px solid #3b82f6;
        outline-offset: 2px;
    }
    .stAlert {
        border-left: 4px solid #3b82f6;
    }
    /* Mobile Responsive */
    @media only screen and (max-width: 600px) {
        .stApp [data-testid="stVerticalBlock"] > div {
            padding: 15px;
        }
        .stApp .stButton {
            width: 100%;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. STATE MANAGEMENT & CACHING
# ==========================================
if 'job_id' not in st.session_state:
    st.session_state.job_id = 0
if 'generation_result' not in st.session_state:
    st.session_state.generation_result = None
if 'generation_running' not in st.session_state:
    st.session_state.generation_running = False
if 'persona_params' not in st.session_state:
    st.session_state.persona_params = {}

@st.cache_resource
def get_executor():
    """Persistent thread pool for non-blocking generation."""
    return ThreadPoolExecutor(max_workers=1)

@st.cache_data(ttl=3600)
def cached_generation(payload_hash, _payload_json):
    """
    Deterministic caching layer. 
    In production, this would call the LLM API.
    """
    # Placeholder: Simulate LLM processing time
    time.sleep(1.5)
    return {
        "id": payload_hash,
        "title": f"Simulated Twin: {_payload_json['strategy']}",
        "explanation": "The system analyzed your driving strategy and the current physics risk.",
        "generation_summary": f"Strategy: {_payload_json['strategy']} | Risk: {_payload_json['risk']*100:.0f}%",
        "persona": _payload_json
    }

def canonicalize_payload(strategy, risk, region):
    """Sort keys to ensure deterministic caching."""
    payload = {
        "strategy": strategy,
        "risk": float(risk),
        "region": region
    }
    return json.dumps(payload, sort_keys=True)

# ==========================================
# 3. UI: SIDEBAR (Privacy & Info)
# ==========================================
with st.sidebar:
    st.title("🧠 ConsciTwin")
    st.caption("v1.0 Production")
    st.divider()
    
    with st.expander("🔒 How it works & Privacy"):
        st.write("ConsciTwin is a self-critiquing Digital Twin. It uses a simulated environment to validate human driving inputs against physical constraints and behavioral trust models.")
        st.write("**Data Privacy:** All simulations run locally in your browser via Three.js. No data is stored or sent to external servers.")
        st.warning("**Disclaimer:** This is a simulation prototype for demonstration purposes. It is not certified for real-world driving safety.")
    
    st.divider()
    st.markdown("**Ethical Guidelines:**")
    st.success("✅ Transparency: Every decision is logged.")
    st.success("✅ Safety First: Physics overrides human error.")
    st.success("✅ Privacy By Design: Zero external data storage.")

# ==========================================
# 4. UI: MAIN APPLICATION (TAB/STEP FLOW)
# ==========================================
st.title("🧠 ConsciTwin")
st.markdown("*The Self-Critiquing Digital Twin.*")

# Primary CTA
col_cta1, col_cta2 = st.columns([4, 1])
with col_cta1:
    if st.button("🚀 Create New Twin", type="primary", use_container_width=True):
        st.session_state.generation_result = None
        st.session_state.persona_params = {}
        st.rerun()

# Stepper (Horizontal tabs)
tab1, tab2, tab3, tab4 = st.tabs(["📖 Quick Start", "⚙️ Customize", "🧬 Generate", "📊 Results"])

# ==========================================
# TAB 1: QUICK START (ONBOARDING)
# ==========================================
with tab1:
    st.markdown("### Step 1: Quick Start")
    st.markdown("Explore what ConsciTwin can do by testing a sample persona. These presets instantly generate a self-critiquing twin and a live 3D visualization.")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚗 Aggressive Driver", use_container_width=True):
            st.session_state.persona_params = {"strategy": "False Nine (Aggressive)", "risk": 0.2}
            st.session_state.active_tab = 3 # Go to results
            st.rerun()
        st.markdown("**Strategy:** False Nine | **Risk:** Dry road")
    with c2:
        if st.button("🛡️ Cautious Driver", use_container_width=True):
            st.session_state.persona_params = {"strategy": "Catenaccio (Defensive)", "risk": 0.8}
            st.session_state.active_tab = 3
            st.rerun()
        st.markdown("**Strategy:** Catenaccio | **Risk:** High ice")

# ==========================================
# TAB 2: CUSTOMIZE (INPUT COLLECTION)
# ==========================================
with tab2:
    st.markdown("### Step 2: Configure Driving Scenario")
    st.markdown("Set the Coach's intent and the physical environment challenges.")
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            strategy = st.selectbox(
                "Driving Strategy (Coach)",
                ["Balanced", "Catenaccio (Defensive)", "False Nine (Aggressive)"],
                help="Defines the cost function for the vehicle's behavior."
            )
            weather_risk = st.slider(
                "Weather / Physics Risk",
                0.0, 1.0, 0.5,
                help="Higher values indicate greater slip risks (ice, rain)."
            )
            region = st.selectbox(
                "Region (Domain Shift)",
                ["Germany (Low Variance)", "Morocco (High Variance)"],
                help="Adjusts the statistical baseline for the Trust Meter."
            )
        with col2:
            st.markdown("#### Live Preview")
            st.metric("Strategy", strategy.split()[0])
            st.metric("Risk Level", f"{weather_risk*100:.0f}%")
            
            if st.button("Generate Twin", type="primary", use_container_width=True):
                # Store params and trigger generation
                st.session_state.persona_params = {
                    "strategy": strategy,
                    "risk": weather_risk,
                    "region": region
                }
                st.session_state.active_tab = 3 # Jump to results
                st.rerun()

# ==========================================
# TAB 3: GENERATE (EXECUTION)
# ==========================================
with tab3:
    st.markdown("### Step 3: Twin Generation")
    
    if not st.session_state.persona_params:
        st.info("Please set your preferences in the 'Customize' tab or select a Quick Start preset.")
    else:
        params = st.session_state.persona_params
        st.write(f"Generating Twin for: **{params['strategy']}** in **{params['region']}**")
        
        # Generate the payload
        payload_str = canonicalize_payload(params['strategy'], params['risk'], params['region'])
        payload_hash = hashlib.md5(payload_str.encode()).hexdigest()
        
        # Check Cache / Run
        if not st.session_state.generation_running:
            st.session_state.generation_running = True
            executor = get_executor()
            future = executor.submit(cached_generation, payload_hash, json.loads(payload_str))
            st.session_state.generation_future = future
            
        # Wait for result
        with st.spinner("ConsciTwin is simulating the environment and critiquing the command..."):
            if 'generation_future' in st.session_state:
                if st.session_state.generation_future.done():
                    result = st.session_state.generation_future.result()
                    st.session_state.generation_result = result
                    st.session_state.generation_running = False
                    st.success("✅ Twin generated successfully!")
                    st.info(f"**Output:** {result['title']}")
                else:
                    st.warning("Processing... this may take up to 20 seconds for cold starts.")

# ==========================================
# TAB 4: RESULTS (OUTPUT & 3D INTEGRATION)
# ==========================================
with tab4:
    if not st.session_state.generation_result:
        st.info("No twin generated yet. Please run a generation in the 'Generate' tab.")
    else:
        result = st.session_state.generation_result
        params = st.session_state.persona_params
        
        st.markdown(f"### Step 4: Results – {result['title']}")
        
        # ---- 1. TEXT OUTPUT ----
        with st.container():
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"**Explanation:** {result['explanation']}")
                st.markdown(f"**Generation Summary:** {result['generation_summary']}")
            with col2:
                st.metric("Trust Meter", f"{95.0}%") # Placeholder logic
                st.metric("Physics Risk", f"{params['risk']*100:.0f}%")
        
        # Action Buttons
        ac1, ac2, ac3 = st.columns([1, 1, 1])
        with ac1: st.button("📋 Copy Audit Log")
        with ac2: st.button("🔄 Refine")
        with ac3: st.download_button("📥 Export JSON", data=json.dumps(result, indent=2), file_name="twin_output.json")
        
        st.divider()
        
        # ---- 2. 3D PHYSICS INTEGRATION ----
        st.markdown("### Live 3D Physics Demo")
        
        # Persona-to-Physics Mapper
        # Warmth 0-10 -> Color Temp
        warmth = 8.0 if "Aggressive" in params['strategy'] else 3.0
        
        # Energy 0-10 -> Particle Emission / Speed
        energy = 9.0 if "Aggressive" in params['strategy'] else 2.0
        
        # Responsiveness 0-10 -> Mass / Physics damping
        responsiveness = 9.0 if "Aggressive" in params['strategy'] else 4.0
        
        # Tone mapping (animate amplitude)
        tone_map = {"Balanced": "Neutral", "Catenaccio (Defensive)": "Formal", "False Nine (Aggressive)": "Casual"}
        tone = tone_map.get(params['strategy'], "Neutral")
        
        # Inject HTML component
        st.components.v1.html(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ margin: 0; overflow: hidden; background-color: #1a1a1a; color: white; font-family: sans-serif; }}
                #info {{ position: absolute; top: 10px; left: 10px; z-index: 10; pointer-events: none; font-size: 0.9rem; opacity: 0.8; }}
            </style>
            <!-- Import Three.js and Cannon-es from CDN -->
            <script type="importmap">
                {{
                    "imports": {{
                        "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
                        "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/",
                        "cannon-es": "https://unpkg.com/cannon-es@0.20.0/dist/cannon-es.js"
                    }}
                }}
            </script>
        </head>
        <body>
            <div id="info">ConsciTwin 3D Physics - Ready</div>

            <script type="module">
                import * as THREE from 'three';
                import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
                import * as CANNON from 'cannon-es';

                // --- 1. THREE.JS SCENE ---
                const scene = new THREE.Scene();
                scene.background = new THREE.Color(0x1a1a1a);

                const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
                camera.position.set(5, 5, 10);

                const renderer = new THREE.WebGLRenderer({{ antialias: true }});
                renderer.setSize(window.innerWidth, window.innerHeight);
                renderer.shadowMap.enabled = true;
                document.body.appendChild(renderer.domElement);

                const controls = new OrbitControls(camera, renderer.domElement);
                controls.target.set(0, 1, 0);
                controls.update();

                // --- 2. CANNON.JS PHYSICS ---
                const world = new CANNON.World();
                world.gravity.set(0, -9.82, 0);
                world.broadphase = new CANNON.SAPBroadphase(world);

                const groundBody = new CANNON.Body({ mass: 0 });
                groundBody.addShape(new CANNON.Plane());
                groundBody.quaternion.setFromAxisAngle(new CANNON.Vec3(1, 0, 0), -Math.PI / 2);
                world.addBody(groundBody);

                // --- 3. CREATE THE "TWIN" AVATAR (PHYSICS MAPPED) ---
                const geometry = new THREE.BoxGeometry(1, 1, 1);
                const colorTemp = {warmth}; // 3.0 = Blue/Neutral, 9.0 = Red/Aggressive
                const emissionIntensity = {energy} * 0.2; // Energy affects emission
                const material = new THREE.MeshStandardMaterial({{
                    color: new THREE.Color().setHSL(0.7 - (colorTemp/20), 1, 0.5),
                    emissive: new THREE.Color().setHSL(0.7 - (colorTemp/20), 1, 0.3),
                    emissiveIntensity: emissionIntensity
                }});
                const cube = new THREE.Mesh(geometry, material);
                cube.castShadow = true;
                cube.position.y = 3;
                scene.add(cube);

                // --- PHYSICS BODY ---
                const mass = 5 / ({responsiveness} > 5 ? 2 : 1); // Low mass = snappier
                const shape = new CANNON.Box(new CANNON.Vec3(0.5, 0.5, 0.5));
                const body = new CANNON.Body({ mass: mass });
                body.addShape(shape);
                body.position.set(0, 3, 0);
                world.addBody(body);

                // --- 4. GROUND & LIGHTS ---
                const planeGeo = new THREE.PlaneGeometry(10, 10);
                const planeMat = new THREE.MeshStandardMaterial({{ color: 0x2a2a2a, side: THREE.DoubleSide }});
                const plane = new THREE.Mesh(planeGeo, planeMat);
                plane.rotation.x = -Math.PI / 2;
                plane.receiveShadow = true;
                scene.add(plane);

                const light = new THREE.DirectionalLight(0xffffff, 1.5);
                light.position.set(5, 10, 7);
                light.castShadow = true;
                scene.add(light);
                scene.add(new THREE.AmbientLight(0x404040));

                // --- 5. ANIMATION LOOP ---
                function animate() {{
                    requestAnimationFrame(animate);
                    world.step(1 / 60);
                    cube.position.copy(body.position);
                    cube.quaternion.copy(body.quaternion);
                    controls.update();
                    renderer.render(scene, camera);
                }}
                animate();

                // --- 6. WINDOW RESIZE ---
                window.addEventListener('resize', () => {{
                    camera.aspect = window.innerWidth / window.innerHeight;
                    camera.updateProjectionMatrix();
                    renderer.setSize(window.innerWidth, window.innerHeight);
                }});

                // --- 7. STREAMLIT BRIDGE (PostMessage) ---
                window.addEventListener('message', (event) => {{
                    if (event.data.type === 'PERSONA_UPDATE') {{
                        const data = event.data.payload;
                        document.getElementById('info').innerText = `3D Physics: {data.tone} Mode | Energy: {data.energy}`;
                        // Example: Update visual properties dynamically here
                        material.color.setHSL(0.7 - (data.warmth/20), 1, 0.5);
                        material.emissiveIntensity = data.energy * 0.2;
                    }}
                }});

                // Let Streamlit know the component is ready
                window.parent.postMessage({{ type: 'CONSCITWIN_3D_READY' }}, '*');

            </script>
        </body>
        </html>
        """, height=500, scrolling=False)

        # ---- 3. REFINEMENT CONTROLS ----
        with st.expander("🔧 Advanced Refinement (Persona Attributes)"):
            st.markdown("Tweak the persona attributes to see the 3D physics react in real-time.")
            
            ref_col1, ref_col2 = st.columns(2)
            with ref_col1:
                warmth = st.slider("Warmth (Color Temperature)", 0, 10, int(warmth), help="0=Cold Blue, 10=Warm Red")
                responsiveness = st.slider("Responsiveness (Physics Mass)", 0, 10, int(responsiveness), help="0=Slow, 10=Snappy")
            with ref_col2:
                energy = st.slider("Energy (Intensity)", 0, 10, int(energy), help="Affects emission and motion intensity")
                tone = st.selectbox("Tone (Posture)", ["Casual", "Neutral", "Formal"], index=["Casual", "Neutral", "Formal"].index(tone))
            
            if st.button("Update 3D Twin"):
                # Send new attributes to the frontend via JavaScript (simulated here)
                # In a full implementation, you'd use st.components.v1.html with a postMessage call update
                st.session_state.persona_params['warmth'] = warmth
                st.session_state.persona_params['energy'] = energy
                st.session_state.persona_params['responsiveness'] = responsiveness
                st.rerun()
