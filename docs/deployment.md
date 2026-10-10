# ScamShield AI — Multi-Platform Deployment Guide

This guide covers deploying **ScamShield AI** to **GitHub**, **Render**, and **Vercel**.

---

## 1. Deploying to GitHub

### Step 1: Initialize Git and Commit
```bash
# In project root
git init
git add .
git commit -m "feat: complete ScamShield AI cybersecurity platform for RAKSHAM hackathon"
```

### Step 2: Create a New GitHub Repository
1. Go to [https://github.com/new](https://github.com/new)
2. Name the repository: `scamshield-ai`
3. Leave it Public or Private, do not add README/gitignore (already included)
4. Click **Create repository**

### Step 3: Link and Push
```bash
git remote add origin https://github.com/<YOUR-USERNAME>/scamshield-ai.git
git branch -M main
git push -u origin main
```

---

## 2. Deploying to Render (Recommended for Full Streamlit App)

Render runs Streamlit natively as a 24/7 web service with WebSocket support.

### Option A: Automatic Blueprint (1-Click via `render.yaml`)
1. Log in to [Render Dashboard](https://dashboard.render.com).
2. Click **New +** > **Blueprint**.
3. Connect your GitHub repository `scamshield-ai`.
4. Render will automatically detect `render.yaml` and configure:
   - **Environment**: Python 3.11.9
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
5. Click **Apply**. Your app will be live at `https://scamshield-ai.onrender.com`.

### Option B: Web Service / Docker Container
1. Click **New +** > **Web Service**.
2. Select **Docker** or **Python**.
3. Port is configured via `$PORT` (or `8501`).
4. Set Environment Variables (optional):
   - `STREAMLIT_SERVER_HEADLESS=true`
   - `STREAMLIT_BROWSER_GATHER_USAGE_STATS=false`

---

## 3. Deploying to Vercel (Serverless API & Static Platform)

Vercel specializes in serverless functions and frontend hosting.

### Option A: Using Vercel CLI
```bash
# Login to Vercel
npx vercel login

# Deploy to preview
npx vercel

# Deploy to production
npx vercel --prod
```

### Option B: Via Vercel Dashboard (GitHub Integration)
1. Go to [https://vercel.com/new](https://vercel.com/new).
2. Import your GitHub repository `scamshield-ai`.
3. Framework Preset: **Other**.
4. Root Directory: `./`.
5. Click **Deploy**.

Vercel automatically detects [`vercel.json`](file:///c:/Users/welle/.gemini/antigravity-ide/scratch/IITD/vercel.json) and routes requests to the Python serverless handler in [`api/index.py`](file:///c:/Users/welle/.gemini/antigravity-ide/scratch/IITD/api/index.py):
- `GET https://your-vercel-app.vercel.app/` &rarr; API health and service metadata.
- `POST https://your-vercel-app.vercel.app/api/analyze` &rarr; Real-time AI detection and XAI explanation JSON payload.

---

## 4. Verification & Testing Post-Deployment

After deployment, verify all services:
- **Render UI**: Visit the Render public URL and test Message Analysis and Workflow Explorer.
- **Vercel API**:
  ```bash
  curl -X POST https://your-vercel-app.vercel.app/api/analyze \
       -H "Content-Type: application/json" \
       -d '{"message": "Dear customer, your SBI account is blocked. Update KYC at http://sbi-kyc.xyz immediately."}'
  ```
- **Local Dev Server**:
  ```bash
  streamlit run app.py
  ```
