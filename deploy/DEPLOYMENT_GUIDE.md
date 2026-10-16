# AI Business OS — Production Go-Live Deployment Guide

This guide describes how to deploy AI Business OS to production in the Indian market to start accepting real customer orders and generating revenue.

---

## 1. Architecture Overview

```
                      [ Customers / CAs / Indian SMEs ]
                                     |
                                     v
                       [ Next.js Storefront & Dashboard ]
                            (Vercel / Port 3000)
                                     |
                                     v
                           [ FastAPI Core Engine ]
                           (Render/Railway / Port 8000)
                            |                     |
                            v                     v
               [ PostgreSQL Database ]     [ Razorpay Payment Rails ]
               (Neon/Supabase Mumbai)        (UPI Intent, QR, Cards, GST)
```

---

## 2. Deployment Options

### Option A: Cloud Managed (Zero Infrastructure Maintenance) — Recommended
1. **Frontend (Next.js Dashboard & Storefront)**:
   - Deploy to **Vercel** with Root Directory set to `apps/dashboard`.
   - Set environment variable: `NEXT_PUBLIC_API_URL=https://api.yourdomain.com`.
   - Recommended Region: Mumbai, India (`bom1`) for < 20ms response time.

2. **Backend (FastAPI Core Engine)**:
   - Deploy to **Render** or **Railway** using `Dockerfile.api`.
   - Port: `8000`.
   - Set environment variables as listed in `.env.production.example`.

3. **Database (PostgreSQL)**:
   - Provision a PostgreSQL database on **Neon** or **Supabase** in AWS Asia Pacific (Mumbai) `ap-south-1`.
   - Set `DATABASE_URL=postgresql+asyncpg://user:password@host/database`.

---

### Option B: Single-Server VPS Docker Deployment (₹400–₹800/month)
Ideal for hosting on a single Hetzner, DigitalOcean Bangalore, or AWS EC2 Mumbai instance.

```bash
# 1. Clone repository on server
git clone <your-repo-url> ai-business-os
cd ai-business-os

# 2. Configure production environment
cp .env.production.example .env

# 3. Launch the full stack (Postgres + FastAPI + Next.js)
docker compose -f deploy/docker-compose.prod.yml up -d --build

# 4. Verify running services
docker compose -f deploy/docker-compose.prod.yml ps
```

---

## 3. Razorpay Live Payment Activation Checklist

1. **Create Merchant Account**:
   - Register at [https://razorpay.com](https://razorpay.com) with your Indian business PAN/GSTIN and bank account details.
2. **Generate API Keys**:
   - Go to `Settings -> API Keys` and generate a `Key ID` and `Key Secret`.
3. **Configure Webhook**:
   - In Razorpay Dashboard, go to `Settings -> Webhooks`.
   - Webhook URL: `https://api.yourdomain.com/webhooks/razorpay`
   - Secret: Set a strong random secret.
   - Active Events:
     - `payment.captured`
     - `order.paid`
4. **Update Production Environment Variables**:
   ```env
   PAYMENT_PROVIDER=razorpay
   PAYMENT_MODE=live
   RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxxxx
   RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
   RAZORPAY_WEBHOOK_SECRET=xxxxxxxxxxxxxxxxxxxx
   ```

---

## 4. Live Commercial Verification Test

1. Visit your live storefront: `https://yourdomain.com/store/msme-43bh`
2. Run the interactive 60-second tax disallowance calculator.
3. Place a live test order for ₹1,999 (Enterprise Starter) via UPI QR or Google Pay.
4. Verify instant digital delivery on `/store/success`:
   - Download the generated `.ZIP` compliance package.
   - Verify all 5 customized compliance documents are present.
5. Check the AI Business OS Control Dashboard:
   - Inflow transaction recorded in `/transactions`.
   - Audit trail recorded in `/audit`.
   - Order marked `FULFILLED` in database.
