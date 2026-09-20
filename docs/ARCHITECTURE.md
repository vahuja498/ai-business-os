# AI Business OS - Architecture Documentation

## 1. Overview
AI Business OS is a modular platform built to operate legitimate, multi-industry autonomous businesses through standard **Business Modules**.

## 2. Layered Architecture

```
+-------------------------------------------------------------+
|                      CONTROL DASHBOARD                      |
|       Next.js 14 (TypeScript, Tailwind, Interactive UI)     |
+-------------------------------------------------------------+
                             |
                             v  (REST / WebSocket API)
+-------------------------------------------------------------+
|                     FASTAPI API GATEWAY                     |
|           Health, Metrics, Routers, Audit, Lifespan         |
+-------------------------------------------------------------+
                             |
                             v
+-------------------------------------------------------------+
|                   AI CEO / ORCHESTRATOR                     |
|     Goal Decomposition, Specialist Delegation, Risk Gate    |
+-------------------------------------------------------------+
       |                                              |
       v                                              v
+-----------------------+              +-----------------------+
|    RESEARCH AGENT     |              |      RISK AGENT       |
| Fact/Claim Separation |              | Anti-Fraud, Approvals |
+-----------------------+              +-----------------------+
       |                                              |
       +----------------------+-----------------------+
                              |
                              v
+-------------------------------------------------------------+
|                         TOOL LAYER                          |
|    ToolRegistry: Autonomy & Permission Checking, Mock Tools |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                      BUSINESS MODULES                       |
|   BusinessModule ABC: discover, acquire, qualify, sell, ... |
|   businesses/solar_leads/ (DRAFT status - Zero outreach)    |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                     DATA & AUDIT LAYER                      |
|   SQLAlchemy (PostgreSQL / SQLite fallback), Append-Only    |
|   AuditLog, Approvals, Opportunities, AgentRuns, Tasks      |
+-------------------------------------------------------------+
```

## 3. Core Principles Enforced
1. **Business-Agnostic Core**: Core agents and database models contain no business-specific logic.
2. **Strict Risk & Safety Gating**: Fraudulent patterns, fake identities, deceptive claims, and platform bypasses are blocked by `RiskEvaluator`.
3. **Human Approval Gates**: Budget expenditures and high-risk operations cannot execute without human sign-off.
4. **Append-Only Auditability**: All actions, approvals, and outcomes produce immutable audit entries.
5. **Autonomy Levels**: Structured escalation hierarchy (`LEVEL_0` to `LEVEL_3`) with no silent elevation.
