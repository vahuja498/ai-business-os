from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from agents.ceo.ceo_agent import CEOAgent
from apps.api.services.audit_service import AuditService
from database.models.business import Business
from database.models.task import Task
from database.models.opportunity import Opportunity
from database.models.approval import Approval
from database.models.agent import Agent, AgentRun


class OrchestrationService:
    @staticmethod
    async def ensure_agent_registered(db: AsyncSession, agent_name: str, description: str, capabilities: list[str]) -> Agent:
        stmt = select(Agent).where(Agent.name == agent_name)
        result = await db.execute(stmt)
        agent = result.scalar_one_or_none()
        if not agent:
            agent = Agent(
                name=agent_name,
                description=description,
                capabilities=capabilities,
                allowed_tools=["web_search", "database", "analytics"],
                execution_mode="AUTONOMOUS",
                risk_level="LOW",
                status="ACTIVE",
            )
            db.add(agent)
            await db.commit()
            await db.refresh(agent)
        return agent

    @classmethod
    async def execute_objective(
        cls,
        db: AsyncSession,
        business_id: str,
        objective: str,
    ) -> dict[str, Any]:
        # 1. Validate business exists
        biz_stmt = select(Business).where(Business.id == business_id)
        biz_res = await db.execute(biz_stmt)
        business = biz_res.scalar_one_or_none()
        if not business:
            raise ValueError(f"Business with id '{business_id}' not found.")

        # Ensure CEO agent model exists in DB
        ceo_db_agent = await cls.ensure_agent_registered(
            db,
            "CEOAgent",
            "Autonomous business orchestrator",
            ["strategic_orchestration", "goal_decomposition", "agent_delegation"],
        )

        # 2. Create parent objective task
        parent_task = Task(
            business_id=business_id,
            title=f"Strategic Objective: {objective}",
            description=objective,
            assigned_agent_id=ceo_db_agent.id,
            status="RUNNING",
            input_context={"objective": objective},
        )
        db.add(parent_task)
        await db.commit()
        await db.refresh(parent_task)

        # 3. Instantiate CEO and run vertical slice workflow
        ceo = CEOAgent()
        ceo_run = await ceo.run(
            input_data={"objective": objective},
            business_id=business_id,
            task_id=parent_task.id,
        )

        # 4. Record AgentRun in database
        db_agent_run = AgentRun(
            id=ceo_run.run_id,
            agent_id=ceo_db_agent.id,
            task_id=parent_task.id,
            business_id=business_id,
            input_data=ceo_run.input_data,
            actions=ceo_run.actions,
            tool_calls=ceo_run.tool_calls,
            outputs=ceo_run.outputs,
            errors=ceo_run.errors,
            approval_requests=ceo_run.approval_requests,
            final_status=ceo_run.final_status,
            started_at=ceo_run.started_at,
            completed_at=ceo_run.completed_at,
        )
        db.add(db_agent_run)

        # 5. Save decomposed tasks
        tasks_data = ceo_run.outputs.get("tasks", [])
        for t_info in tasks_data:
            subtask = Task(
                id=t_info.get("task_id"),
                business_id=business_id,
                parent_task_id=parent_task.id,
                title=t_info.get("title", "Subtask"),
                status=t_info.get("status", "COMPLETED"),
                input_context={"assigned_agent": t_info.get("assigned_agent")},
            )
            db.add(subtask)

        # 6. Save Opportunity in database
        opp_data = ceo_run.outputs.get("opportunity")
        saved_opportunity = None
        if opp_data:
            saved_opportunity = Opportunity(
                business_id=business_id,
                title=opp_data.get("title", "Discovered Opportunity"),
                description=opp_data.get("description"),
                target_market=opp_data.get("target_market"),
                revenue_model=opp_data.get("revenue_model"),
                estimated_startup_cost=opp_data.get("estimated_startup_cost", 0.0),
                estimated_customer_value=opp_data.get("estimated_customer_value", 0.0),
                estimated_acquisition_cost=opp_data.get("estimated_acquisition_cost", 0.0),
                estimated_fulfilment_cost=opp_data.get("estimated_fulfilment_cost", 0.0),
                estimated_margin=opp_data.get("estimated_margin", 0.0),
                automation_potential=opp_data.get("automation_potential", "HIGH"),
                regulatory_complexity=opp_data.get("regulatory_complexity", "LOW"),
                platform_dependency=opp_data.get("platform_dependency", "LOW"),
                risk_level=opp_data.get("risk_level", "LOW"),
                evidence=opp_data.get("evidence", []),
                assumptions=opp_data.get("assumptions", []),
                recommended_experiment=opp_data.get("recommended_experiment", {}),
                status=opp_data.get("status", "PENDING_APPROVAL"),
            )
            db.add(saved_opportunity)

        # 7. Save Approvals in database
        saved_approvals = []
        for req in ceo_run.approval_requests:
            approval = Approval(
                business_id=business_id,
                agent_id=ceo_db_agent.id,
                task_id=parent_task.id,
                action_type=req.get("action_type", "general_action"),
                description=req.get("description", ""),
                risk_level=req.get("risk_level", "HIGH"),
                amount=req.get("amount"),
                reason=req.get("reason"),
                evidence=req.get("evidence", []),
                status="PENDING",
            )
            db.add(approval)
            saved_approvals.append(approval)

        parent_task.status = "COMPLETED" if not saved_approvals else "PENDING_APPROVAL"
        await db.commit()

        if saved_opportunity:
            await db.refresh(saved_opportunity)

        # 8. Record audit log
        await AuditService.record_event(
            db=db,
            actor="CEOAgent",
            agent_id=ceo_db_agent.id,
            business_id=business_id,
            action="EXECUTE_OBJECTIVE",
            target=f"Task:{parent_task.id}",
            result=ceo_run.final_status,
            metadata={
                "objective": objective,
                "opportunity_id": saved_opportunity.id if saved_opportunity else None,
                "approvals_generated": len(saved_approvals),
            },
        )

        return {
            "task_id": parent_task.id,
            "business_id": business_id,
            "status": ceo_run.final_status,
            "opportunity": {
                "id": saved_opportunity.id if saved_opportunity else None,
                "title": saved_opportunity.title if saved_opportunity else None,
                "status": saved_opportunity.status if saved_opportunity else None,
                "margin": saved_opportunity.estimated_margin if saved_opportunity else None,
            } if saved_opportunity else None,
            "approvals": [
                {
                    "id": a.id,
                    "action_type": a.action_type,
                    "risk_level": a.risk_level,
                    "amount": a.amount,
                    "status": a.status,
                }
                for a in saved_approvals
            ],
            "decomposed_tasks_count": len(tasks_data),
        }
