# AI Business OS

AI Business OS is a modular, business-agnostic platform designed to operate legitimate autonomous businesses through configurable Business Modules.

## Architecture

- **Control Dashboard**: Next.js (TypeScript) interface for human oversight, approvals, and observability.
- **AI CEO / Orchestrator**: High-level goal decomposition and specialist delegation.
- **Specialist Agents**: Modular agents (Research, Risk, Growth, Sales, Operations, Finance, Analytics, Engineering).
- **Tool Layer**: Governed tool execution with permission checks and autonomy levels.
- **Business Modules**: Pluggable modules implementing the standard `BusinessModule` interface.
- **Governance**: Human-in-the-loop approval workflows for sensitive and high-risk actions.
- **Audit Logging**: Append-only audit records for every significant action.

## Getting Started

### Backend
```powershell
uv venv .venv
uv pip install -e ".[dev]"
uv run uvicorn apps.api.main:app --reload
```

### Dashboard
```powershell
cd apps/dashboard
npm install
npm run dev
```

### Running Tests
```powershell
uv run pytest
```
