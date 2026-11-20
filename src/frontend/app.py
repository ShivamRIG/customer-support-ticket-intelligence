import json
from pathlib import Path
import requests
import streamlit as st

st.set_page_config(
    page_title="TRIAGE.AI — Autonomous Support Intelligence",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Load Tickets Dataset ---
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "tickets_dataset.json"
try:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        TICKETS_DATA = json.load(f)
except Exception:
    # Fallback dataset if file is missing
    TICKETS_DATA = [
        {
            "subject": "Production DB connection timeout (504)",
            "body": "Our primary Postgres pool is exhausted across EU-West nodes and webhooks are failing.",
            "answer": "Checked container logs; upstream database unresponsive."
        },
        {
            "subject": "Duplicate invoice charge on annual plan",
            "body": "We were billed twice on November 1st for our enterprise workspace renewal.",
            "answer": ""
        }
    ]

# Initialize session index for cycling tickets
if "ticket_index" not in st.session_state:
    st.session_state["ticket_index"] = 0

# Render the complete ORBAI-styled UI using st.html
st.html("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TRIAGE.AI — Autonomous Support Routing</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #070709;
    --surface: rgba(255, 255, 255, 0.03);
    --surface-hover: rgba(255, 255, 255, 0.06);
    --border: rgba(255, 255, 255, 0.09);
    --border-glow: rgba(139, 92, 246, 0.45);
    --text-main: #f4f4f6;
    --text-muted: #9ca3af;
    --accent-1: #6366f1;
    --accent-2: #a855f7;
    --success: #10b981;
    --danger: #ef4444;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  html {
    scroll-behavior: smooth;
    background-color: var(--bg);
    color: var(--text-main);
    font-family: 'Inter', sans-serif;
  }

  body {
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
    line-height: 1.6;
    padding-bottom: 4rem;
  }

  /* Architectural Grid Overlay */
  body::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(to right, rgba(255, 255, 255, 0.02) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
    background-size: 64px 64px;
    mask-image: radial-gradient(ellipse 80% 60% at 50% 20%, #000 40%, transparent 100%);
    pointer-events: none;
    z-index: 0;
  }

  /* Glowing Orbs */
  .orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(110px);
    opacity: 0.38;
    pointer-events: none;
    z-index: 0;
  }
  .orb-1 { width: 480px; height: 480px; background: var(--accent-1); top: -100px; left: 12%; }
  .orb-2 { width: 420px; height: 420px; background: var(--accent-2); top: 150px; right: 10%; }

  main {
    position: relative;
    z-index: 1;
    max-width: 1120px;
    margin: 0 auto;
    padding: 0 1.5rem;
  }

  /* Hero */
  .hero {
    min-height: 75vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding-top: 5rem;
    padding-bottom: 2rem;
  }

  .hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 1rem;
    border-radius: 999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #c4b5fd;
    background: rgba(139, 92, 246, 0.12);
    border: 1px solid rgba(139, 92, 246, 0.3);
    margin-bottom: 1.5rem;
  }

  .hero h1 {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: clamp(2.5rem, 5.5vw, 4.5rem);
    font-weight: 800;
    line-height: 1.08;
    letter-spacing: -0.04em;
    max-width: 820px;
    background: linear-gradient(180deg, #ffffff 30%, #9ca3af 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1.25rem;
  }

  .hero p {
    max-width: 580px;
    color: var(--text-muted);
    font-size: 1.05rem;
    margin-bottom: 2rem;
  }

  /* Bento Cards */
  .bento-card {
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.01) 100%);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 2rem;
    backdrop-filter: blur(14px);
    margin-bottom: 2.5rem;
  }

  .section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #a78bfa;
    margin-bottom: 0.5rem;
  }

  .section-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: clamp(1.75rem, 3vw, 2.4rem);
    font-weight: 700;
    letter-spacing: -0.03em;
    margin-bottom: 2rem;
  }

  .arch-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
  }

  @media (max-width: 800px) {
    .arch-grid { grid-template-columns: 1fr; }
  }

  .arch-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #c4b5fd;
    background: rgba(139, 92, 246, 0.14);
    border: 1px solid rgba(139, 92, 246, 0.3);
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 8px;
    margin-bottom: 0.85rem;
  }

  .bento-card h3 {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
  }

  .bento-card p {
    color: var(--text-muted);
    font-size: 0.92rem;
  }

  pre {
    background: #040406;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #d1d5db;
    overflow-x: auto;
    line-height: 1.6;
    margin-top: 1rem;
  }
</style>
</head>
<body>

<div class="orb orb-1"></div>
<div class="orb orb-2"></div>

<main>
  <div class="hero">
    <div class="hero-badge">Autonomous Support Intelligence • XGBoost + MiniLM-L6-v2</div>
    <h1>Route every support ticket with precision.</h1>
    <p>Real-time semantic embedding and dual-target gradient boosted classification engineered for high-throughput customer operations.</p>
  </div>
</main>

</body>
</html>
""")

# --- STREAMLIT NATIVE INTERACTIVE SECTIONS (Keeping Exact Order) ---

st.divider()

# Section 1: Live Triage Demo
st.markdown("### 01 / Live Ticket Triage Demo")
st.markdown("#### Interactive Inference Console")

col_input, col_output = st.columns([1.1, 1], gap="large")

with col_input:
    with st.container(border=True):
        st.caption("JSON Dataset Cycling")
        
        # Cycling button that steps through tickets_dataset.json
        if st.button("🔄 Load Next Ticket from JSON Dataset", use_container_width=True):
            current_idx = st.session_state["ticket_index"]
            ticket = TICKETS_DATA[current_idx]
            
            st.session_state["sub"] = ticket["subject"]
            st.session_state["bod"] = ticket["body"]
            st.session_state["ans"] = ticket.get("answer", "")
            
            # Advance index and loop back to start if at the end
            st.session_state["ticket_index"] = (current_idx + 1) % len(TICKETS_DATA)
            st.toast(f"Loaded ticket #{current_idx + 1} of {len(TICKETS_DATA)}", icon="📄")

        with st.form("triage_form"):
            subject = st.text_input("Ticket Subject *", value=st.session_state.get("sub", ""))
            body = st.text_area("Ticket Body *", value=st.session_state.get("bod", ""), height=120)
            answer = st.text_input("Agent Notes (Optional)", value=st.session_state.get("ans", ""))
            submitted = st.form_submit_button("Run Triage Analysis →", type="primary", use_container_width=True)

with col_output:
    with st.container(border=True):
        st.markdown("##### Inference Output")
        if submitted:
            if not subject.strip() or not body.strip():
                st.error("Please enter both a ticket subject and body.")
            else:
                with st.status("Running AI Triage Pipeline...", expanded=True) as status:
                    st.write("Encoding text into 384-D semantic vector...")
                    prog = st.progress(35)
                    st.write("Evaluating dual XGBoost queue & priority classifiers...")
                    prog.progress(80)

                    try:
                        res = requests.post(
                            "http://127.0.0.1:8000/predict/triage",
                            json={"subject": subject, "body": body, "answer": answer},
                            timeout=10,
                        )
                        res.raise_for_status()
                        data = res.json()
                        prog.progress(100)
                        status.update(label="Classification Complete", state="complete", expanded=False)

                        mc1, mc2 = st.columns(2)
                        q_conf = f"{data.get('queue_confidence', 0)*100:.1f}%" if data.get('queue_confidence') else "N/A"
                        p_conf = f"{data.get('priority_confidence', 0)*100:.1f}%" if data.get('priority_confidence') else "N/A"
                        mc1.metric("Suggested Queue", data.get("suggested_queue", "Unknown"), q_conf)
                        mc2.metric("Suggested Priority", data.get("suggested_priority", "Unknown"), p_conf)

                        with st.expander("View Raw JSON"):
                            st.json(data)
                    except Exception as e:
                        status.update(label="Inference Failed", state="error", expanded=True)
                        st.error(f"Could not reach FastAPI backend: {e}")
        else:
            st.info("Click **🔄 Load Next Ticket from JSON Dataset** above and click **Run Triage Analysis →**.")

st.divider()

# Section 2: Architecture
st.markdown("### 02 / Architecture")
st.markdown("#### Built for High-Throughput Support Queues")
a1, a2, a3 = st.columns(3)
with a1:
    with st.container(border=True):
        st.markdown("`STEP 01`\n### Semantic Encoding")
        st.write("Ticket subject, body, and agent notes are transformed into 384-dimensional dense vectors using `all-MiniLM-L6-v2`.")
with a2:
    with st.container(border=True):
        st.markdown("`STEP 02`\n### Dual XGBoost Routing")
        st.write("Class-balanced histogram gradient boosters independently predict the target department queue and urgency tier.")
with a3:
    with st.container(border=True):
        st.markdown("`STEP 03`\n### Container Inference")
        st.write("Stateless FastAPI microservice packaged in a slim Docker image for instant horizontal scaling.")

st.divider()

# Section 3: Cloud & REST API
st.markdown("### 03 / Cloud & REST API")
st.markdown("#### Containerized for AWS & REST Integration")
tab_aws, tab_rest = st.tabs(["AWS ECR / ECS", "REST API Payload"])
with tab_aws:
    st.code("""aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker build -t ticket-intelligence-api:slim .
docker tag ticket-intelligence-api:slim <account-id>.dkr.ecr.us-east-1.amazonaws.com/ticket-intelligence-api:slim
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ticket-intelligence-api:slim""", language="bash")
with tab_rest:
    st.code("""curl -X POST "http://127.0.0.1:8000/predict/triage" \\
  -H "Content-Type: application/json" \\
  -d '{
    "subject": "Database connection timeout",
    "body": "Primary Postgres pool exhausted returning 504 errors.",
    "answer": ""
  }'""", language="bash")