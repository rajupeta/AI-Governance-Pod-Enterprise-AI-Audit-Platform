-- AI Governance Platform Database Schema
-- Enterprise-grade governance, compliance, and audit system

-- AI Systems Registry
CREATE TABLE ai_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_type TEXT NOT NULL,
    description TEXT,
    risk_category TEXT CHECK (risk_category IN ('low', 'medium', 'high', 'critical')),
    deployment_status TEXT CHECK (deployment_status IN ('development', 'testing', 'staging', 'production', 'deprecated')),
    owner_team TEXT NOT NULL,
    business_unit TEXT,
    data_types TEXT, -- JSON array of data types used
    users_affected INTEGER DEFAULT 0,
    decision_automation TEXT CHECK (decision_automation IN ('none', 'low', 'medium', 'high', 'full')),
    human_oversight TEXT CHECK (human_oversight IN ('none', 'limited', 'moderate', 'extensive', 'full')),
    data_sensitivity TEXT CHECK (data_sensitivity IN ('public', 'internal', 'confidential', 'personal_data', 'sensitive_personal')),
    business_impact TEXT CHECK (business_impact IN ('low', 'medium', 'high', 'critical')),
    regulatory_scope TEXT, -- JSON array of applicable regulations
    technical_details TEXT, -- JSON object with technical specifications
    last_assessment_date DATETIME,
    governance_score REAL CHECK (governance_score >= 0 AND governance_score <= 10),
    compliance_status TEXT CHECK (compliance_status IN ('compliant', 'partially_compliant', 'non_compliant', 'unknown')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Risk Assessments
CREATE TABLE risk_assessments (
    assessment_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    assessment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    assessor_id TEXT NOT NULL,
    assessment_type TEXT CHECK (assessment_type IN ('initial', 'periodic', 'change_triggered', 'incident_response')),
    overall_risk_score REAL CHECK (overall_risk_score >= 0 AND overall_risk_score <= 10),
    bias_risk_score REAL CHECK (bias_risk_score >= 0 AND bias_risk_score <= 10),
    privacy_risk_score REAL CHECK (privacy_risk_score >= 0 AND privacy_risk_score <= 10),
    security_risk_score REAL CHECK (security_risk_score >= 0 AND security_risk_score <= 10),
    explainability_risk_score REAL CHECK (explainability_risk_score >= 0 AND explainability_risk_score <= 10),
    regulatory_risk_score REAL CHECK (regulatory_risk_score >= 0 AND regulatory_risk_score <= 10),
    risk_factors TEXT, -- JSON array of identified risk factors
    risk_categories TEXT, -- JSON object with categorized risks
    mitigation_recommendations TEXT, -- JSON array of recommendations
    confidence_level REAL CHECK (confidence_level >= 0 AND confidence_level <= 10),
    methodology_used TEXT,
    review_required BOOLEAN DEFAULT FALSE,
    approved_by TEXT,
    approval_date DATETIME,
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

-- Governance Policies
CREATE TABLE policies (
    policy_id TEXT PRIMARY KEY,
    policy_name TEXT NOT NULL,
    policy_version TEXT NOT NULL,
    policy_type TEXT CHECK (policy_type IN ('internal', 'regulatory', 'industry_standard', 'best_practice')),
    regulatory_framework TEXT, -- e.g., 'EU_AI_Act', 'NIST_AI_RMF', 'GDPR'
    policy_content TEXT NOT NULL,
    policy_summary TEXT,
    applicable_systems TEXT, -- JSON array of system types/categories
    enforcement_level TEXT CHECK (enforcement_level IN ('advisory', 'recommended', 'mandatory', 'regulatory')),
    policy_status TEXT CHECK (policy_status IN ('draft', 'active', 'deprecated', 'superseded')),
    effective_date DATETIME,
    expiry_date DATETIME,
    policy_owner TEXT,
    approval_authority TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Compliance Checks
CREATE TABLE compliance_checks (
    check_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    policy_id TEXT NOT NULL,
    check_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    checker_id TEXT NOT NULL,
    check_type TEXT CHECK (check_type IN ('automated', 'manual', 'hybrid')),
    compliance_status TEXT CHECK (compliance_status IN ('compliant', 'partially_compliant', 'non_compliant', 'not_applicable')),
    compliance_score REAL CHECK (compliance_score >= 0 AND compliance_score <= 10),
    findings TEXT, -- JSON array of findings
    evidence TEXT, -- JSON array of evidence/artifacts
    gaps_identified TEXT, -- JSON array of compliance gaps
    remediation_required BOOLEAN DEFAULT FALSE,
    remediation_plan TEXT,
    remediation_deadline DATETIME,
    remediation_status TEXT CHECK (remediation_status IN ('not_required', 'planned', 'in_progress', 'completed', 'overdue')),
    next_check_date DATETIME,
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id),
    FOREIGN KEY (policy_id) REFERENCES policies(policy_id)
);

-- Audit Events and Trail
CREATE TABLE audit_events (
    event_id TEXT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    system_id TEXT,
    event_type TEXT NOT NULL,
    event_category TEXT CHECK (event_category IN ('assessment', 'compliance', 'remediation', 'monitoring', 'approval', 'violation')),
    actor_id TEXT NOT NULL,
    actor_role TEXT,
    action_taken TEXT NOT NULL,
    affected_entities TEXT, -- JSON array of affected systems/policies
    event_details TEXT, -- JSON object with detailed event information
    risk_level TEXT CHECK (risk_level IN ('low', 'medium', 'high', 'critical')),
    compliance_impact TEXT,
    business_impact TEXT,
    resolution_status TEXT CHECK (resolution_status IN ('open', 'in_progress', 'resolved', 'closed')),
    resolution_details TEXT,
    tags TEXT, -- JSON array of tags for categorization
    integrity_hash TEXT, -- For audit trail integrity
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

-- Bias Evaluations
CREATE TABLE bias_evaluations (
    evaluation_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    evaluation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    evaluator_id TEXT NOT NULL,
    evaluation_methodology TEXT,
    protected_attributes TEXT, -- JSON array of attributes analyzed
    fairness_metrics TEXT, -- JSON object with fairness metric results
    bias_detected BOOLEAN DEFAULT FALSE,
    bias_severity TEXT CHECK (bias_severity IN ('none', 'low', 'medium', 'high', 'critical')),
    affected_groups TEXT, -- JSON array of affected demographic groups
    bias_type TEXT, -- e.g., 'statistical', 'representation', 'measurement', 'evaluation'
    bias_source TEXT, -- e.g., 'training_data', 'algorithm', 'feature_selection', 'labeling'
    impact_assessment TEXT,
    mitigation_strategies TEXT, -- JSON array of recommended mitigations
    mitigation_status TEXT CHECK (mitigation_status IN ('not_required', 'planned', 'in_progress', 'implemented', 'verified')),
    retest_required BOOLEAN DEFAULT FALSE,
    retest_date DATETIME,
    confidence_score REAL CHECK (confidence_score >= 0 AND confidence_score <= 10),
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

-- Regulatory Frameworks
CREATE TABLE regulatory_frameworks (
    framework_id TEXT PRIMARY KEY,
    framework_name TEXT NOT NULL,
    framework_version TEXT,
    jurisdiction TEXT,
    regulatory_body TEXT,
    framework_type TEXT CHECK (framework_type IN ('law', 'regulation', 'standard', 'guideline', 'best_practice')),
    effective_date DATETIME,
    last_updated DATETIME,
    framework_summary TEXT,
    key_requirements TEXT, -- JSON array of key requirements
    applicability_criteria TEXT, -- JSON object defining when framework applies
    compliance_obligations TEXT, -- JSON array of specific obligations
    enforcement_mechanisms TEXT, -- JSON array of enforcement options
    penalties TEXT, -- JSON object describing potential penalties
    related_frameworks TEXT, -- JSON array of related/referenced frameworks
    implementation_guidance TEXT,
    status TEXT CHECK (status IN ('proposed', 'active', 'superseded', 'deprecated'))
);

-- Create indexes for performance
CREATE INDEX idx_ai_systems_risk_category ON ai_systems(risk_category);
CREATE INDEX idx_ai_systems_deployment_status ON ai_systems(deployment_status);
CREATE INDEX idx_ai_systems_governance_score ON ai_systems(governance_score);
CREATE INDEX idx_risk_assessments_system_id ON risk_assessments(system_id);
CREATE INDEX idx_risk_assessments_date ON risk_assessments(assessment_date);
CREATE INDEX idx_compliance_checks_system_id ON compliance_checks(system_id);
CREATE INDEX idx_compliance_checks_policy_id ON compliance_checks(policy_id);
CREATE INDEX idx_audit_events_system_id ON audit_events(system_id);
CREATE INDEX idx_audit_events_timestamp ON audit_events(timestamp);
CREATE INDEX idx_bias_evaluations_system_id ON bias_evaluations(system_id);

-- Monitoring Metrics
CREATE TABLE monitoring_metrics (
    metric_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    measurement_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    metric_type TEXT NOT NULL,
    metric_category TEXT CHECK (metric_category IN ('performance', 'bias', 'fairness', 'security', 'privacy', 'explainability', 'compliance')),
    metric_name TEXT NOT NULL,
    metric_value REAL,
    metric_unit TEXT,
    threshold_value REAL,
    threshold_type TEXT CHECK (threshold_type IN ('minimum', 'maximum', 'range')),
    threshold_status TEXT CHECK (threshold_status IN ('within_threshold', 'warning', 'critical', 'breach')),
    measurement_method TEXT,
    measurement_context TEXT, -- JSON object with measurement context
    alert_triggered BOOLEAN DEFAULT FALSE,
    alert_level TEXT CHECK (alert_level IN ('info', 'warning', 'critical')),
    remediation_triggered BOOLEAN DEFAULT FALSE,
    notes TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

CREATE INDEX idx_monitoring_metrics_system_id ON monitoring_metrics(system_id);
CREATE INDEX idx_monitoring_metrics_date ON monitoring_metrics(measurement_date);
CREATE INDEX idx_monitoring_metrics_threshold_status ON monitoring_metrics(threshold_status);
