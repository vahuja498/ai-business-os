export const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export interface DashboardSummary {
  metrics: {
    active_businesses: number;
    open_opportunities: number;
    pending_approvals: number;
    simulated_revenue: number;
    simulated_expenses: number;
    system_health: string;
  };
  guardrails: {
    max_daily_spend: number;
    max_transaction_amount: number;
    max_monthly_spend: number;
    min_margin: number;
  };
  recent_runs: Array<{
    id: string;
    agent_id: string;
    final_status: string;
    started_at: string;
    completed_at: string | null;
  }>;
  pending_approvals: Array<{
    id: string;
    business_id: string;
    action_type: string;
    description: string;
    risk_level: string;
    amount: number | null;
    requested_at: string;
  }>;
  recent_opportunities: Array<{
    id: string;
    title: string;
    margin: number;
    risk_level: string;
    status: string;
  }>;
}

export interface BusinessItem {
  id: string;
  name: string;
  description: string;
  status: string;
  module_name: string;
  created_at: string;
}

export interface ApprovalItem {
  id: string;
  business_id: string;
  agent_id: string;
  task_id: string | null;
  action_type: string;
  description: string;
  risk_level: string;
  amount: number | null;
  reason: string | null;
  evidence: any[];
  status: string;
  requested_at: string;
  approved_at: string | null;
  approved_by: string | null;
  rejection_reason: string | null;
}

export interface OpportunityItem {
  id: string;
  business_id: string | null;
  title: string;
  opportunity_family: string;
  customer?: string;
  problem?: string;
  solution?: string;
  description: string;
  target_market: string;
  revenue_model: string;
  estimated_startup_cost: number;
  estimated_customer_value: number;
  estimated_acquisition_cost: number;
  estimated_fulfilment_cost: number;
  estimated_margin: number;
  automation_potential: string;
  time_to_first_revenue: string;
  recurring_potential?: string;
  competition?: string;
  geography?: string[];
  regulatory_complexity: string;
  platform_dependency: string;
  uncertainty: string;
  evidence_quality: string;
  risk_level: string;
  evidence: any[];
  findings?: any[];
  assumptions: any[];
  unknowns?: string[];
  failure_modes?: string[];
  contradicting_evidence?: any[];
  automation_breakdown?: {
    ai_automation?: string;
    software_automation?: string;
    human_only?: string;
  };
  disintermediation_analysis?: string;
  regulatory_considerations?: string;
  evidence_for?: string[];
  evidence_against?: string[];
  sources?: Array<{
    source_title: string;
    source_url: string;
    source_domain?: string;
    publication_date?: string;
    classification?: string;
    confidence?: number;
  }>;
  pursue_status?: string;
  do_not_pursue_reason?: string;
  reality_check?: Record<string, { dimension: string; status: string; notes: string }>;
  recommended_experiment?: {
    hypothesis: string;
    validation: string;
    budget: number;
    duration: string;
    success_metric: string;
    failure_metric: string;
    data_required: string[];
    human_approvals_required: boolean;
  };
  status: string;
  created_at: string;
}

export interface AuditItem {
  id: string;
  actor: string;
  agent_id: string | null;
  business_id: string | null;
  action: string;
  target: string | null;
  result: string;
  approval_id: string | null;
  metadata: Record<string, any>;
  created_at: string;
}

export interface ValidationPlanItem {
  id: string;
  opportunity_id: string;
  opportunity_title: string;
  opportunity_family: string;
  customer: string | null;
  status: string;
  confidence_score: number;
  total_budget_allocated: number;
  total_budget_spent: number;
  material_assumptions_count: number;
  high_risk_assumptions_count: number;
  completed_experiments_count: number;
  regulatory_approval_required: boolean;
  created_at: string | null;
}

export interface AssumptionItem {
  id: string;
  category: string;
  statement: string;
  classification: string;
  risk_level: string;
  is_highest_risk: boolean;
  evidence_notes: string;
  initial_classification: string;
}

export interface ValidationExperimentItem {
  id: string;
  validation_plan_id: string;
  opportunity_id: string;
  opportunity_title: string;
  opportunity_family?: string;
  assumption_id: string | null;
  title: string;
  hypothesis: string;
  methodology: string;
  pass_criteria: string;
  fail_criteria: string;
  inconclusive_criteria: string;
  budget: number;
  duration_days: number;
  required_evidence: string[];
  automated_tasks: string;
  human_tasks: string;
  regulatory_requirements: string;
  approval_status: string;
  execution_status: string;
  is_simulation: boolean;
  created_at?: string | null;
  results?: Array<{
    id: string;
    outcome: string;
    metric_observed: string;
    cost_spent: number;
    notes: string;
    simulated: boolean;
    executed_at: string | null;
  }>;
}

export interface ExperimentResultItem {
  id: string;
  experiment_id: string;
  experiment_title: string;
  opportunity_id: string;
  opportunity_title: string;
  outcome: string;
  metric_observed: string;
  evidence_artifacts: any[];
  cost_spent: number;
  notes: string;
  simulated: boolean;
  executed_at: string | null;
}

export interface ValidationApprovalItem {
  id: string;
  validation_plan_id: string;
  opportunity_id: string;
  opportunity_title: string;
  experiment_id: string | null;
  approval_type: string;
  description: string;
  risk_level: string;
  status: string;
  requested_amount: number | null;
  approved_by: string | null;
  approved_at: string | null;
  rejection_reason: string | null;
  created_at: string | null;
}

export interface ValidationPlanDetail {
  id: string;
  opportunity: {
    id: string;
    title: string;
    opportunity_family: string;
    customer: string | null;
    problem: string | null;
    solution: string | null;
    revenue_model: string | null;
    estimated_startup_cost: number;
    estimated_margin: number;
    automation_potential: string;
    time_to_first_revenue: string;
    regulatory_complexity: string;
    platform_dependency: string;
    pursue_status: string;
  };
  plan: {
    status: string;
    confidence_score: number;
    summary: string;
    total_budget_allocated: number;
    total_budget_spent: number;
    material_assumptions_count: number;
    high_risk_assumptions_count: number;
    completed_experiments_count: number;
    regulatory_approval_required: boolean;
    regulatory_approval_notes: string;
    created_at: string | null;
  };
  budget: {
    max_budget: number;
    allocated_amount: number;
    spent_amount: number;
    currency: string;
    is_locked: boolean;
  } | null;
  assumptions: AssumptionItem[];
  experiments: ValidationExperimentItem[];
  approvals: ValidationApprovalItem[];
  audit_trail: Array<{
    id: string;
    actor: string;
    action: string;
    entity_type: string;
    details: any;
    timestamp: string | null;
  }>;
}

export const api = {
  async getDashboardSummary(): Promise<DashboardSummary> {
    const res = await fetch(`${API_BASE}/dashboard/summary`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch dashboard summary");
    return res.json();
  },

  async getBusinesses(): Promise<BusinessItem[]> {
    const res = await fetch(`${API_BASE}/businesses`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch businesses");
    return res.json();
  },

  async createBusiness(payload: { name: string; description: string; module_name: string }): Promise<BusinessItem> {
    const res = await fetch(`${API_BASE}/businesses`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to create business");
    return res.json();
  },

  async executeObjective(businessId: string, objective: string): Promise<any> {
    const res = await fetch(`${API_BASE}/businesses/${businessId}/objectives`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ objective }),
    });
    if (!res.ok) throw new Error("Failed to execute objective");
    return res.json();
  },

  async getApprovals(status?: string): Promise<ApprovalItem[]> {
    const url = status ? `${API_BASE}/approvals?status=${status}` : `${API_BASE}/approvals`;
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch approvals");
    return res.json();
  },

  async approve(approvalId: string, actor: string = "HUMAN_OPERATOR"): Promise<any> {
    const res = await fetch(`${API_BASE}/approvals/${approvalId}/approve`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ actor }),
    });
    if (!res.ok) throw new Error("Failed to approve request");
    return res.json();
  },

  async reject(approvalId: string, reason: string = "Manual rejection"): Promise<any> {
    const res = await fetch(`${API_BASE}/approvals/${approvalId}/reject`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ reason }),
    });
    if (!res.ok) throw new Error("Failed to reject request");
    return res.json();
  },

  async getOpportunities(family?: string): Promise<OpportunityItem[]> {
    const url = family ? `${API_BASE}/opportunities?opportunity_family=${family}` : `${API_BASE}/opportunities`;
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch opportunities");
    return res.json();
  },

  async getOpportunityReport(family?: string): Promise<{ count: number; markdown_report: string; opportunities: any[] }> {
    const url = family ? `${API_BASE}/opportunities/report?opportunity_family=${family}` : `${API_BASE}/opportunities/report`;
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch opportunity report");
    return res.json();
  },

  async triggerOpportunityResearch(payload: {
    objective?: string;
    capital_limit?: number;
    geography?: string[];
    time_horizon_days?: number;
    opportunity_families?: string[];
    business_id?: string;
  }): Promise<any> {
    const res = await fetch(`${API_BASE}/opportunities/research`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to trigger opportunity research");
    return res.json();
  },

  async requestExperimentApproval(opportunityId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/opportunities/${opportunityId}/experiment/approve`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    if (!res.ok) throw new Error("Failed to request experiment approval");
    return res.json();
  },

  async getAgents(): Promise<any[]> {
    const res = await fetch(`${API_BASE}/agents`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch agents");
    return res.json();
  },

  async getTasks(): Promise<any[]> {
    const res = await fetch(`${API_BASE}/tasks`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch tasks");
    return res.json();
  },

  async getAuditLogs(): Promise<AuditItem[]> {
    const res = await fetch(`${API_BASE}/audit`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch audit logs");
    return res.json();
  },

  // --- Phase 5: Validation Engine Methods ---
  async getValidationPlans(family?: string, status?: string): Promise<ValidationPlanItem[]> {
    const params = new URLSearchParams();
    if (family && family !== "ALL") params.append("family", family);
    if (status && status !== "ALL") params.append("status", status);
    const qs = params.toString() ? `?${params.toString()}` : "";
    const res = await fetch(`${API_BASE}/validation${qs}`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch validation plans");
    return res.json();
  },

  async syncValidationPlans(): Promise<any> {
    const res = await fetch(`${API_BASE}/validation/sync`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    if (!res.ok) throw new Error("Failed to sync validation plans");
    return res.json();
  },

  async getValidationPlanByOpportunity(opportunityId: string): Promise<ValidationPlanDetail> {
    const res = await fetch(`${API_BASE}/validation/${opportunityId}`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch validation plan detail");
    return res.json();
  },

  async getValidationExperiments(planId?: string, executionStatus?: string): Promise<ValidationExperimentItem[]> {
    const params = new URLSearchParams();
    if (planId) params.append("plan_id", planId);
    if (executionStatus && executionStatus !== "ALL") params.append("execution_status", executionStatus);
    const qs = params.toString() ? `?${params.toString()}` : "";
    const res = await fetch(`${API_BASE}/validation/experiments${qs}`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch validation experiments");
    return res.json();
  },

  async getValidationExperiment(experimentId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/validation/experiments/${experimentId}`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch validation experiment");
    return res.json();
  },

  async runValidationExperiment(experimentId: string, payload: any): Promise<any> {
    const res = await fetch(`${API_BASE}/validation/experiments/${experimentId}/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({ detail: "Failed to execute experiment" }));
      throw new Error(errData.detail || "Failed to execute experiment");
    }
    return res.json();
  },

  async getValidationApprovals(status?: string): Promise<ValidationApprovalItem[]> {
    const qs = status && status !== "ALL" ? `?status=${status}` : "";
    const res = await fetch(`${API_BASE}/validation/approvals${qs}`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch validation approvals");
    return res.json();
  },

  async decideValidationApproval(
    approvalId: string,
    action: "APPROVE" | "REJECT",
    decidedBy: string = "HumanReviewer",
    rejectionReason?: string
  ): Promise<any> {
    const res = await fetch(`${API_BASE}/validation/approvals/${approvalId}/decide`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action, decided_by: decidedBy, rejection_reason: rejectionReason }),
    });
    if (!res.ok) throw new Error("Failed to submit approval decision");
    return res.json();
  },

  async getValidationResults(): Promise<ExperimentResultItem[]> {
    const res = await fetch(`${API_BASE}/validation/results`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch validation results");
    return res.json();
  },

  async submitValidationResult(payload: any): Promise<any> {
    const res = await fetch(`${API_BASE}/validation/results`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({ detail: "Failed to submit result" }));
      throw new Error(errData.detail || "Failed to submit result");
    }
    return res.json();
  },
};
