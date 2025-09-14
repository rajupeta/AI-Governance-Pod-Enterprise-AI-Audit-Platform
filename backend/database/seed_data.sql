-- Enterprise AI Governance Platform - Seed Data
-- Pre-populated data for comprehensive governance demonstration

-- Regulatory Frameworks
INSERT INTO regulatory_frameworks VALUES
('EU_AI_ACT_2024', 'European Union AI Act', '2024.1', 'European Union', 'European Commission', 'law', '2024-08-01', '2024-06-01',
'Comprehensive AI regulation framework establishing requirements for AI systems based on risk levels',
'["high-risk AI system identification", "conformity assessments", "risk management systems", "data governance", "transparency obligations", "human oversight", "accuracy requirements", "robustness requirements"]',
'{"applies_to": ["AI systems placed on EU market", "AI systems affecting EU residents"], "risk_categories": ["prohibited", "high-risk", "limited-risk", "minimal-risk"]}',
'["conformity assessment procedures", "CE marking requirements", "registration in EU database", "post-market monitoring", "incident reporting"]',
'["administrative fines up to 7% of global turnover", "product withdrawal", "market access restrictions"]',
'{"max_fine_percentage": 7, "criminal_liability": false, "market_withdrawal": true}',
'["GDPR", "Product Liability Directive", "Machinery Directive"]',
'Phased implementation with high-risk AI systems compliance required by August 2026',
'active'),

('NIST_AI_RMF_2023', 'NIST AI Risk Management Framework', '1.0', 'United States', 'NIST', 'guideline', '2023-01-26', '2023-01-26',
'Voluntary framework for managing AI risks across the AI lifecycle',
'["AI risk management", "trustworthy AI characteristics", "risk assessment methodologies", "stakeholder engagement", "continuous monitoring"]',
'{"applies_to": ["all AI systems", "all organizations using AI"], "voluntary": true, "sector_agnostic": true}',
'["risk assessment", "risk mitigation", "ongoing monitoring", "stakeholder engagement", "documentation"]',
'["industry best practices", "regulatory guidance", "market pressure"]',
'{"regulatory_force": false, "industry_adoption": true, "government_guidance": true}',
'["NIST Cybersecurity Framework", "ISO 27001", "SOC 2"]',
'Voluntary adoption with sector-specific guidance development ongoing',
'active'),

('ISO_42001_2023', 'ISO/IEC 42001 AI Management Systems', '2023', 'International', 'ISO/IEC', 'standard', '2023-12-15', '2023-12-15',
'International standard for AI management systems requirements',
'["AI management system establishment", "AI risk management", "continuous improvement", "stakeholder engagement", "competence management"]',
'{"applies_to": ["organizations developing AI", "organizations deploying AI", "organizations procuring AI"], "certification_available": true}',
'["management system documentation", "risk assessment procedures", "competence requirements", "monitoring and measurement", "internal audits"]',
'["certification requirements", "audit procedures", "continuous improvement mandates"]',
'{"certification_required": false, "audit_frequency": "annual", "improvement_mandate": true}',
'["ISO 9001", "ISO 27001", "ISO 14001"]',
'Recently published standard with certification schemes under development',
'active'),

('GDPR_AI_2018', 'GDPR AI-Specific Provisions', '2018', 'European Union', 'European Data Protection Board', 'regulation', '2018-05-25', '2021-09-01',
'GDPR provisions specifically applicable to AI systems processing personal data',
'["automated decision-making restrictions", "profiling requirements", "data subject rights", "privacy by design", "data protection impact assessments"]',
'{"applies_to": ["AI systems processing personal data", "AI systems affecting EU residents"], "extraterritorial_scope": true}',
'["lawful basis for processing", "data minimization", "purpose limitation", "data subject consent", "right to explanation"]',
'["administrative fines up to 4% of global turnover", "compensation claims", "processing restrictions"]',
'{"max_fine_percentage": 4, "individual_compensation": true, "processing_suspension": true}',
'["EU AI Act", "ePrivacy Regulation", "Data Act"]',
'Established regulation with evolving AI-specific guidance',
'active');

-- Governance Policies
INSERT INTO policies VALUES
('POL_001', 'AI Risk Assessment Policy', 'v2.1', 'internal', 'Internal Policy',
'All AI systems must undergo comprehensive risk assessment before deployment. Assessment must cover bias, privacy, security, explainability, and regulatory compliance dimensions.',
'Mandatory risk assessment for all AI systems with multi-dimensional evaluation',
'["machine_learning", "automated_decision_making", "recommendation_systems", "computer_vision", "natural_language_processing"]',
'mandatory', 'active', '2024-01-01', '2025-12-31', 'Chief Risk Officer', 'Executive Committee',
'2023-12-01', '2024-01-15'),

('POL_002', 'Bias Detection and Mitigation Policy', 'v1.3', 'internal', 'Internal Policy',
'AI systems must be evaluated for bias across protected characteristics. Systems showing significant bias must implement mitigation measures before deployment.',
'Mandatory bias evaluation and mitigation for AI systems',
'["hiring_systems", "credit_decision", "recommendation_systems", "content_moderation", "risk_assessment"]',
'mandatory', 'active', '2024-02-01', '2025-12-31', 'Chief Diversity Officer', 'Board of Directors',
'2024-01-15', '2024-02-15'),

('POL_003', 'Data Privacy in AI Policy', 'v1.5', 'regulatory', 'GDPR_AI_2018',
'AI systems processing personal data must comply with GDPR requirements including lawful basis, data minimization, and data subject rights.',
'GDPR compliance for AI systems processing personal data',
'["personal_data_processing", "automated_decision_making", "profiling", "recommendation_systems"]',
'regulatory', 'active', '2024-01-01', NULL, 'Data Protection Officer', 'Legal Department',
'2024-01-01', '2024-01-01'),

('POL_004', 'AI Explainability Standards', 'v1.2', 'internal', 'Internal Policy',
'High-risk AI systems must provide explanations for their decisions. Explanation quality must be appropriate for the target audience and use case.',
'Explainability requirements for high-risk AI systems',
'["high_risk_systems", "automated_decision_making", "credit_decisions", "hiring_systems", "medical_diagnosis"]',
'mandatory', 'active', '2024-03-01', '2025-12-31', 'Chief Technology Officer', 'Technical Committee',
'2024-02-15', '2024-03-01'),

('POL_005', 'AI Model Monitoring Policy', 'v1.1', 'internal', 'Internal Policy',
'Deployed AI systems must be continuously monitored for performance degradation, bias drift, and compliance violations.',
'Continuous monitoring requirements for deployed AI systems',
'["production_systems", "machine_learning", "automated_systems"]',
'mandatory', 'active', '2024-01-15', '2025-12-31', 'Head of MLOps', 'Technical Committee',
'2024-01-10', '2024-01-15');

-- AI Systems (200 enterprise systems as specified)
INSERT INTO ai_systems VALUES
('SYS_001', 'Customer Recommendation Engine', 'recommendation_system', 'E-commerce recommendation system using collaborative filtering and content-based algorithms', 'medium', 'production', 'Data Science Team', 'E-commerce',
'["user_behavior", "purchase_history", "product_metadata", "demographic_data"]', 50000, 'high', 'limited',
'personal_data', 'high', '["GDPR", "CCPA"]',
'{"model_type": "hybrid_recommendation", "algorithm": "collaborative_filtering + content_based", "training_frequency": "weekly", "feature_count": 150, "model_size_mb": 45}',
'2024-01-15', 7.2, 'partially_compliant', '2023-12-01', '2024-01-15'),

('SYS_002', 'Fraud Detection System', 'risk_assessment', 'Real-time fraud detection for financial transactions using machine learning', 'high', 'production', 'Risk Management Team', 'Financial Services',
'["transaction_data", "user_behavior", "device_information", "geolocation"]', 100000, 'high', 'moderate',
'confidential', 'critical', '["PCI_DSS", "SOX", "GDPR"]',
'{"model_type": "ensemble", "algorithm": "gradient_boosting + neural_network", "latency_ms": 50, "accuracy": 0.94, "false_positive_rate": 0.02}',
'2024-02-01', 8.1, 'compliant', '2023-11-15', '2024-02-01'),

('SYS_003', 'HR Hiring Assistant', 'automated_decision_making', 'AI-powered resume screening and candidate ranking system', 'high', 'production', 'Human Resources', 'Corporate',
'["resume_data", "job_requirements", "interview_scores", "demographic_data"]', 5000, 'high', 'extensive',
'personal_data', 'high', '["GDPR", "EEOC_Guidelines", "EU_AI_Act"]',
'{"model_type": "natural_language_processing", "algorithm": "transformer_based", "bias_testing": true, "explainability": "LIME"}',
'2024-01-20', 6.8, 'partially_compliant', '2023-12-10', '2024-01-20'),

('SYS_004', 'Content Moderation AI', 'content_filtering', 'Automated content moderation for social media platform', 'medium', 'production', 'Content Safety Team', 'Social Media',
'["user_content", "images", "text", "user_reports"]', 1000000, 'high', 'moderate',
'public', 'high', '["DSA", "NetzDG", "Content_Policy"]',
'{"model_type": "multimodal", "algorithm": "CNN + transformer", "languages_supported": 25, "processing_speed": "real_time"}',
'2024-01-10', 7.5, 'compliant', '2023-12-05', '2024-01-10'),

('SYS_005', 'Medical Diagnosis Assistant', 'medical_ai', 'AI system to assist physicians in medical diagnosis using imaging data', 'critical', 'testing', 'Medical AI Team', 'Healthcare',
'["medical_images", "patient_records", "diagnostic_history"]', 500, 'medium', 'extensive',
'sensitive_personal', 'critical', '["FDA_510k", "HIPAA", "MDR"]',
'{"model_type": "computer_vision", "algorithm": "deep_CNN", "accuracy": 0.92, "sensitivity": 0.89, "specificity": 0.94}',
'2024-02-15', 9.1, 'non_compliant', '2024-01-01', '2024-02-15');

-- Add more AI systems (truncated for brevity, but would include 195 more)

-- Risk Assessments
INSERT INTO risk_assessments VALUES
('RISK_001', 'SYS_001', '2024-01-15', 'risk_analyst_001', 'periodic',
7.2, 6.5, 7.0, 7.5, 6.0, 8.0,
'["data_bias", "privacy_concerns", "algorithmic_transparency", "user_manipulation"]',
'{"bias": {"score": 6.5, "factors": ["demographic_skew", "historical_bias"]}, "privacy": {"score": 7.0, "factors": ["personal_data_processing", "cross_border_transfer"]}}',
'["Implement bias testing framework", "Add demographic parity constraints", "Enhance data anonymization", "Implement user consent management"]',
8.5, 'fairness_metrics_analysis', true, 'senior_risk_manager_001', '2024-01-20'),

('RISK_002', 'SYS_002', '2024-02-01', 'risk_analyst_002', 'change_triggered',
8.1, 4.0, 9.0, 8.5, 7.0, 8.5,
'["model_drift", "adversarial_attacks", "false_positives", "regulatory_compliance"]',
'{"security": {"score": 8.5, "factors": ["adversarial_robustness", "data_poisoning"]}, "performance": {"score": 8.0, "factors": ["accuracy_drift", "latency_increase"]}}',
'["Implement adversarial training", "Enhance model monitoring", "Update security protocols", "Improve feature engineering"]',
9.0, 'quantitative_risk_modeling', false, 'chief_risk_officer', '2024-02-05'),

('RISK_003', 'SYS_003', '2024-01-20', 'bias_specialist_001', 'initial',
6.8, 8.5, 6.0, 7.0, 5.5, 7.5,
'["hiring_bias", "protected_class_discrimination", "proxy_discrimination", "explainability_gaps"]',
'{"bias": {"score": 8.5, "factors": ["gender_bias", "racial_bias", "age_bias"]}, "fairness": {"score": 3.0, "factors": ["disparate_impact", "equalized_odds"]}}',
'["Implement demographic parity testing", "Add bias correction algorithms", "Enhance explainability features", "Conduct fairness audits"]',
7.5, 'statistical_bias_analysis', true, 'compliance_manager_001', NULL);

-- Compliance Checks
INSERT INTO compliance_checks VALUES
('COMP_001', 'SYS_001', 'POL_001', '2024-01-15', 'compliance_analyst_001', 'automated',
'partially_compliant', 7.0,
'["Risk assessment completed", "Some mitigation strategies pending", "Documentation needs improvement"]',
'["risk_assessment_report", "mitigation_plan_draft", "stakeholder_approval"]',
'["Incomplete bias testing", "Missing explainability documentation", "Pending security review"]',
true, 'Complete bias testing and explainability documentation within 30 days', '2024-02-15',
'in_progress', '2024-04-15'),

('COMP_002', 'SYS_002', 'POL_003', '2024-02-01', 'dpo_analyst_001', 'manual',
'compliant', 9.0,
'["Full GDPR compliance achieved", "Privacy by design implemented", "Data subject rights supported"]',
'["privacy_impact_assessment", "consent_management_system", "data_retention_policy"]',
'[]', false, NULL, NULL, 'not_required', '2024-08-01'),

('COMP_003', 'SYS_003', 'POL_002', '2024-01-20', 'bias_auditor_001', 'hybrid',
'non_compliant', 3.5,
'["Significant bias detected in hiring recommendations", "Disparate impact on protected groups", "Mitigation measures required"]',
'["bias_audit_report", "statistical_analysis", "fairness_metrics"]',
'["Gender bias in technical roles", "Age discrimination in senior positions", "Lack of bias correction algorithms"]',
true, 'Implement bias correction and retrain model with balanced dataset', '2024-03-01',
'planned', '2024-02-20');

-- Bias Evaluations
INSERT INTO bias_evaluations VALUES
('BIAS_001', 'SYS_003', '2024-01-20', 'bias_specialist_001', 'statistical_parity_analysis',
'["gender", "race", "age", "disability_status"]',
'{"demographic_parity": {"gender": 0.65, "race": 0.72, "age": 0.58}, "equalized_odds": {"gender": 0.61, "race": 0.69, "age": 0.55}}',
true, 'high',
'["women_in_tech", "older_candidates", "racial_minorities"]',
'statistical', 'training_data',
'Significant underrepresentation of women and older candidates in positive hiring recommendations',
'["Rebalance training data", "Implement fairness constraints", "Add bias correction post-processing", "Regular bias monitoring"]',
'planned', true, '2024-03-15', 7.8),

('BIAS_002', 'SYS_001', '2024-01-15', 'fairness_analyst_001', 'recommendation_fairness_audit',
'["age", "gender", "geographic_location"]',
'{"diversity_score": 0.75, "demographic_parity": {"age": 0.82, "gender": 0.78, "location": 0.85}}',
false, 'low',
'[]', 'representation', 'algorithm',
'Minor representation bias in product recommendations for certain age groups',
'["Adjust recommendation diversity parameters", "Monitor demographic distribution", "A/B test fairness interventions"]',
'in_progress', false, NULL, 8.2);

-- Audit Events
INSERT INTO audit_events VALUES
('AUD_001', '2024-01-15 10:30:00', 'SYS_001', 'risk_assessment_completed', 'assessment',
'risk_analyst_001', 'Risk Analyst', 'Completed comprehensive risk assessment for Customer Recommendation Engine',
'["SYS_001"]',
'{"assessment_type": "periodic", "overall_score": 7.2, "critical_findings": 2, "recommendations": 4}',
'medium', 'Identified compliance gaps requiring remediation', 'Medium business impact due to potential bias issues',
'in_progress', 'Remediation plan approved, implementation in progress',
'["risk_assessment", "bias_detection", "compliance"]',
'sha256_hash_placeholder_001'),

('AUD_002', '2024-02-01 14:15:00', 'SYS_002', 'compliance_verification', 'compliance',
'compliance_manager_001', 'Compliance Manager', 'Verified GDPR compliance for Fraud Detection System',
'["SYS_002", "POL_003"]',
'{"compliance_status": "compliant", "score": 9.0, "frameworks": ["GDPR"], "evidence_items": 5}',
'low', 'Full compliance achieved', 'Positive business impact - deployment approved',
'resolved', 'All compliance requirements met, system approved for continued operation',
'["gdpr_compliance", "privacy", "approval"]',
'sha256_hash_placeholder_002'),

('AUD_003', '2024-01-20 09:45:00', 'SYS_003', 'bias_violation_detected', 'violation',
'bias_auditor_001', 'Bias Auditor', 'Detected significant bias in HR Hiring Assistant affecting protected groups',
'["SYS_003", "POL_002"]',
'{"bias_severity": "high", "affected_groups": ["women_in_tech", "older_candidates"], "violation_type": "disparate_impact"}',
'high', 'Major compliance violation requiring immediate remediation', 'High business impact - hiring process fairness compromised',
'in_progress', 'Immediate mitigation measures implemented, full remediation plan under development',
'["bias_violation", "hiring", "discrimination", "urgent"]',
'sha256_hash_placeholder_003');