import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TRIAGE.AI — Customer Support Intelligence",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
    <style>
        #MainMenu, header, footer {visibility: hidden;}
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        iframe {
            border: none;
            width: 100%;
            display: block;
            overflow: hidden;
        }
    </style>
""", unsafe_allow_html=True)

html_app = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TRIAGE.AI — Intelligent Support Routing</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
    :root {
        --bg: #f3f3f0;
        --ink: #141413;
        --muted: #666660;
        --border: #dfdfd9;
        --card: #ffffff;
        --accent: #1d4ed8;
        --urgent: #dc2626;
    }

    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

    html {
        scroll-behavior: smooth;
    }

    body {
        background-color: var(--bg);
        color: var(--ink);
        font-family: 'Inter', sans-serif;
        overflow-x: hidden;
        line-height: 1.6;
    }

    nav {
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 100;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.25rem 3rem;
        background: rgba(243, 243, 240, 0.9);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid var(--border);
    }

    .logo {
        font-weight: 800;
        font-size: 1.1rem;
        letter-spacing: -0.03em;
    }

    .nav-links {
        display: flex;
        gap: 2.5rem;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .nav-links a {
        text-decoration: none;
        color: var(--muted);
        transition: color 0.2s;
    }

    .nav-links a:hover {
        color: var(--ink);
    }

    .status-pill {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        padding: 0.4rem 0.9rem;
        border-radius: 999px;
        background: var(--ink);
        color: #fff;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #22c55e;
    }

    .hero {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 9rem 2rem 5rem;
        position: relative;
    }

    .eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        color: var(--muted);
        margin-bottom: 1rem;
    }

    .hero-title {
        font-weight: 800;
        font-size: clamp(4rem, 12vw, 10rem);
        line-height: 0.9;
        letter-spacing: -0.04em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .hero-serif {
        font-family: 'Instrument Serif', serif;
        font-style: italic;
        font-size: clamp(2rem, 4vw, 3.5rem);
        line-height: 1.1;
        margin-bottom: 1.5rem;
    }

    .hero-desc {
        max-width: 540px;
        color: var(--muted);
        font-size: 1.05rem;
    }

    .float-item {
        position: absolute;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(8px);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.9rem 1.2rem;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.04);
        font-size: 0.8rem;
        text-align: left;
        z-index: 2;
    }

    .float-1 { top: 25%; left: 8%; transform: rotate(-3deg); }
    .float-2 { top: 28%; right: 8%; transform: rotate(2deg); }
    .float-3 { bottom: 15%; left: 10%; transform: rotate(1deg); }
    .float-4 { bottom: 18%; right: 10%; transform: rotate(-2deg); }

    .badge {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        background: #e5e7eb;
        margin-bottom: 0.3rem;
    }

    section {
        max-width: 1160px;
        margin: 0 auto;
        padding: 6rem 2rem;
        border-top: 1px solid var(--border);
    }

    .chapter-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: var(--muted);
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }

    .section-heading {
        font-size: clamp(2rem, 4vw, 3.2rem);
        font-weight: 700;
        letter-spacing: -0.03em;
        margin-bottom: 2.5rem;
    }

    .demo-grid {
        display: grid;
        grid-template-columns: 1.2fr 1fr;
        gap: 2rem;
    }

    @media (max-width: 850px) {
        .demo-grid { grid-template-columns: 1fr; }
        .float-item { display: none; }
    }

    .card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.03);
    }

    .field {
        margin-bottom: 1.25rem;
    }

    label {
        display: block;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--muted);
        margin-bottom: 0.45rem;
    }

    input, textarea {
        width: 100%;
        padding: 0.85rem 1rem;
        border: 1px solid var(--border);
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        background: #fafaf8;
        transition: border-color 0.2s, background 0.2s;
    }

    input:focus, textarea:focus {
        outline: none;
        border-color: var(--ink);
        background: #fff;
    }

    button.primary-btn {
        width: 100%;
        padding: 1rem;
        background: var(--ink);
        color: #fff;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.95rem;
        cursor: pointer;
        transition: opacity 0.2s;
    }

    button.primary-btn:hover { opacity: 0.9; }

    .result-box {
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
    }

    .metric-pair {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-top: 1.5rem;
    }

    .metric {
        background: #f8f8f6;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.5rem;
    }

    .metric-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        text-transform: uppercase;
        color: var(--muted);
    }

    .metric-val {
        font-size: 1.4rem;
        font-weight: 700;
        margin-top: 0.4rem;
    }

    .metric-conf {
        font-size: 0.8rem;
        color: var(--muted);
        margin-top: 0.25rem;
    }

    .tabs {
        display: flex;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }

    .tab-btn {
        padding: 0.6rem 1.2rem;
        border-radius: 999px;
        border: 1px solid var(--border);
        background: transparent;
        font-size: 0.85rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
    }

    .tab-btn.active {
        background: var(--ink);
        color: #fff;
        border-color: var(--ink);
    }

    pre {
        background: #141413;
        color: #e5e5e0;
        padding: 1.5rem;
        border-radius: 12px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        overflow-x: auto;
        margin-top: 1rem;
    }

    footer {
        text-align: center;
        padding: 4rem 2rem;
        border-top: 1px solid var(--border);
        color: var(--muted);
        font-size: 0.85rem;
    }
</style>
</head>
<body>

<nav>
    <div class="logo">TRIAGE.AI</div>
    <div class="nav-links">
        <a href="#companion">01 / Overview</a>
        <a href="#demo">02 / Live Demo</a>
        <a href="#cloud">03 / Cloud API</a>
    </div>
    <div class="status-pill"><span class="dot"></span> XGBoost v3.4.1</div>
</nav>

<div class="hero">
    <div class="float-item float-1">
        <span class="badge">QUEUE: IT SUPPORT</span>
        <div><strong>Jira 503 Gateway Error</strong></div>
    </div>
    <div class="float-item float-2">
        <span class="badge" style="background:#fee2e2;color:#991b1b;">PRIORITY: HIGH</span>
        <div><strong>Production DB Timeout</strong></div>
    </div>
    <div class="float-item float-3">
        <span class="badge">EMBEDDING: 384-D</span>
        <div><code>all-MiniLM-L6-v2</code></div>
    </div>
    <div class="float-item float-4">
        <span class="badge" style="background:#dcfce7;color:#166534;">LATENCY: 24ms</span>
        <div><strong>FastAPI Container</strong></div>
    </div>

    <div class="eyebrow">The art of intelligent routing</div>
    <h1 class="hero-title">TRIAGE.AI</h1>
    <div class="hero-serif">A little context. A lot of precision.</div>
    <p class="hero-desc">
        Automated support ticket classification powered by semantic sentence embeddings and dual-target gradient boosted decision trees.
    </p>
</div>

<section id="companion">
    <div class="chapter-tag">01 / The Architecture</div>
    <h2 class="section-heading">Built for high-throughput support queues.</h2>
    <div class="demo-grid" style="grid-template-columns: repeat(3, 1fr);">
        <div class="card">
            <div class="chapter-tag">Step 01</div>
            <h3 style="margin-bottom:0.75rem;">Semantic Encoding</h3>
            <p style="color:var(--muted); font-size:0.95rem;">
                Ticket subject, body, and agent notes are transformed into 384-dimensional dense vectors using <code>all-MiniLM-L6-v2</code>.
            </p>
        </div>
        <div class="card">
            <div class="chapter-tag">Step 02</div>
            <h3 style="margin-bottom:0.75rem;">Dual XGBoost Routing</h3>
            <p style="color:var(--muted); font-size:0.95rem;">
                Class-balanced histogram gradient boosters independently predict the target department queue and urgency tier.
            </p>
        </div>
        <div class="card">
            <div class="chapter-tag">Step 03</div>
            <h3 style="margin-bottom:0.75rem;">Container Inference</h3>
            <p style="color:var(--muted); font-size:0.95rem;">
                Stateless FastAPI microservice packaged in Docker for horizontal scaling across AWS ECS and Azure Container Apps.
            </p>
        </div>
    </div>
</section>

<section id="demo">
    <div class="chapter-tag">02 / Interactive Inference</div>
    <h2 class="section-heading">Live Ticket Triage Demo</h2>
    <div class="demo-grid">
        <div class="card">
            <div class="field">
                <label>FastAPI Endpoint URL</label>
                <input type="text" id="apiUrl" value="http://127.0.0.1:8000/predict/triage">
            </div>
            <div class="field">
                <label>Ticket Subject</label>
                <input type="text" id="subject" placeholder="e.g., Cannot access Jira after upgrading to 8.20">
            </div>
            <div class="field">
                <label>Ticket Body</label>
                <textarea id="body" rows="4" placeholder="e.g., The Jira service throws a 503 error after our recent upgrade."></textarea>
            </div>
            <div class="field">
                <label>Agent Notes (Optional)</label>
                <input type="text" id="answer" placeholder="e.g., Checked container logs, upstream unresponsive.">
            </div>
            <button class="primary-btn" onclick="runTriage()">Run Triage Analysis →</button>
        </div>

        <div class="card">
            <div class="result-box" id="resultBox">
                <div class="chapter-tag">Inference Output</div>
                <h3>Awaiting Ticket Input</h3>
                <p style="color:var(--muted); font-size:0.95rem; margin-top:0.5rem;">
                    Enter ticket details on the left and execute the model to inspect predicted routing queues and priority confidence scores.
                </p>
            </div>
        </div>
    </div>
</section>

<section id="cloud">
    <div class="chapter-tag">03 / Cloud & API Deployment</div>
    <h2 class="section-heading">Containerized for AWS & Azure</h2>
    <div class="card">
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('aws', this)">AWS ECS / Fargate</button>
            <button class="tab-btn" onclick="switchTab('azure', this)">Azure Container Apps</button>
            <button class="tab-btn" onclick="switchTab('rest', this)">REST API Payload</button>
        </div>

        <div id="tab-aws" class="tab-content">
            <p style="color:var(--muted);">Push the Docker container image to Amazon ECR and deploy behind an Application Load Balancer using serverless AWS Fargate.</p>
<pre>aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin &lt;account-id&gt;.dkr.ecr.us-east-1.amazonaws.com
docker build -t ticket-triage-api .
docker tag ticket-triage-api:latest &lt;account-id&gt;.dkr.ecr.us-east-1.amazonaws.com/ticket-triage-api:latest
docker push &lt;account-id&gt;.dkr.ecr.us-east-1.amazonaws.com/ticket-triage-api:latest</pre>
        </div>

        <div id="tab-azure" class="tab-content" style="display:none;">
            <p style="color:var(--muted);">Deploy to Azure Container Apps with external HTTP ingress on port 8000 and automatic scale-to-zero support.</p>
<pre>az containerapp create \\
  --name ticket-triage-api \\
  --resource-group support-ml-rg \\
  --environment triage-env \\
  --image &lt;acr-name&gt;.azurecr.io/ticket-triage-api:latest \\
  --target-port 8000 \\
  --ingress external</pre>
        </div>

        <div id="tab-rest" class="tab-content" style="display:none;">
            <p style="color:var(--muted);">Consume real-time predictions from Zendesk, Jira, or internal dashboards via standard HTTP POST.</p>
<pre>curl -X POST "http://127.0.0.1:8000/predict/triage" \\
  -H "Content-Type: application/json" \\
  -d '{
    "subject": "Database connection timeout",
    "body": "Primary Postgres pool exhausted returning 504 errors.",
    "answer": ""
  }'</pre>
        </div>
    </div>
</section>

<footer>
    TRIAGE.AI — Customer Support Ticket Intelligence System
</footer>

<script>
    function switchTab(tabId, btn) {
        document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
        document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
        document.getElementById('tab-' + tabId).style.display = 'block';
        btn.classList.add('active');
    }

    async function runTriage() {
        const url = document.getElementById('apiUrl').value;
        const subject = document.getElementById('subject').value.trim();
        const body = document.getElementById('body').value.trim();
        const answer = document.getElementById('answer').value.trim();
        const resultBox = document.getElementById('resultBox');

        if (!subject || !body) {
            resultBox.innerHTML = `<div style="color:#dc2626; font-weight:600;">Please enter both a ticket subject and body.</div>`;
            return;
        }

        resultBox.innerHTML = `<div style="color:var(--muted);">Running semantic embedding & XGBoost classification...</div>`;

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ subject, body, answer })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            const qConf = data.queue_confidence ? (data.queue_confidence * 100).toFixed(1) + '%' : 'N/A';
            const pConf = data.priority_confidence ? (data.priority_confidence * 100).toFixed(1) + '%' : 'N/A';

            resultBox.innerHTML = `
                <div class="chapter-tag" style="color:#16a34a;">● Classification Complete</div>
                <h3>Routing Recommendation</h3>
                <div class="metric-pair">
                    <div class="metric">
                        <div class="metric-label">Suggested Queue</div>
                        <div class="metric-val">${data.suggested_queue}</div>
                        <div class="metric-conf">Confidence: ${qConf}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Suggested Priority</div>
                        <div class="metric-val" style="color:#dc2626;">${data.suggested_priority}</div>
                        <div class="metric-conf">Confidence: ${pConf}</div>
                    </div>
                </div>
            `;
        } catch (err) {
            resultBox.innerHTML = `
                <div style="color:#dc2626; font-weight:600; margin-bottom:0.5rem;">Connection Error</div>
                <p style="color:var(--muted); font-size:0.9rem;">
                    Could not reach <code>${url}</code>. Ensure FastAPI is running with CORS enabled (<code>uvicorn src.api.main:app --reload</code>).
                </p>
            `;
        }
    }
</script>

</body>
</html>
"""

components.html(html_app, height=2200, scrolling=True)