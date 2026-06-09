CREATE EXTENSION IF NOT EXISTS vector;

CREATE OR REPLACE FUNCTION sample_embedding(seed INTEGER)
RETURNS VECTOR(768)
LANGUAGE SQL
IMMUTABLE
AS $$
    SELECT ('[' || string_agg(
        to_char(((sin((seed + i) * 12.9898) + 1) / 2), 'FM0.000000'),
        ','
        ORDER BY i
    ) || ']')::vector
    FROM generate_series(1, 768) AS i;
$$;

DELETE FROM documents
WHERE source_file IN (
    'hr/employee-handbook-2026.md',
    'it/vpn-access-guide.md',
    'security/incident-response-playbook.md',
    'finance/travel-expense-policy.md',
    'engineering/release-management.md',
    'engineering/on-call-guide.md'
);

DELETE FROM feedback
WHERE user_id IN ('sample.user', 'finance.tester');

INSERT INTO documents (source_file, title, chunk_text, metadata, embedding)
VALUES
(
    'hr/employee-handbook-2026.md',
    'Paid Time Off Policy',
    'Full-time employees accrue paid time off each pay period. PTO requests should be submitted in the HR portal at least five business days before the planned absence. Managers approve requests based on staffing needs and project coverage. Unused PTO may carry over up to 40 hours into the next calendar year.',
    '{"department":"HR","category":"policy","chunk_index":0,"access_groups":[],"effective_date":"2026-01-01","tags":["pto","time off","benefits"]}'::jsonb,
    sample_embedding(101)
),
(
    'hr/employee-handbook-2026.md',
    'Parental Leave',
    'Eligible employees may take up to twelve weeks of paid parental leave following the birth, adoption, or foster placement of a child. Employees should notify HR and their manager at least thirty days before leave when possible. Benefits remain active during approved parental leave.',
    '{"department":"HR","category":"policy","chunk_index":1,"access_groups":[],"effective_date":"2026-01-01","tags":["parental leave","benefits"]}'::jsonb,
    sample_embedding(102)
),
(
    'it/vpn-access-guide.md',
    'VPN Access Request',
    'Employees who need remote access to internal systems must request VPN access through the IT service portal. The request must include the business reason, manager approval, and expected access duration. New VPN users must enroll in multi-factor authentication before credentials are activated.',
    '{"department":"IT","category":"runbook","chunk_index":0,"access_groups":[],"service":"vpn","tags":["vpn","remote access","mfa"]}'::jsonb,
    sample_embedding(201)
),
(
    'it/vpn-access-guide.md',
    'VPN Troubleshooting',
    'If the VPN client fails to connect, confirm that the device clock is synchronized, the MFA prompt was approved, and the latest client version is installed. Persistent connection failures should be escalated to the IT service desk with the client log bundle attached.',
    '{"department":"IT","category":"runbook","chunk_index":1,"access_groups":[],"service":"vpn","tags":["vpn","troubleshooting"]}'::jsonb,
    sample_embedding(202)
),
(
    'security/incident-response-playbook.md',
    'Security Incident Severity',
    'Security incidents are classified as low, medium, high, or critical. Critical incidents include active data exfiltration, ransomware affecting production systems, or confirmed compromise of privileged credentials. Critical incidents require immediate notification of Security, Legal, and executive leadership.',
    '{"department":"Security","category":"playbook","chunk_index":0,"access_groups":["security-team"],"tags":["incident response","severity","critical"]}'::jsonb,
    sample_embedding(301)
),
(
    'security/incident-response-playbook.md',
    'Phishing Report Workflow',
    'Employees should report suspected phishing messages using the Report Phishing button in the mail client. The security operations team reviews submissions, quarantines confirmed malicious messages, and publishes follow-up guidance when a campaign targets multiple employees.',
    '{"department":"Security","category":"playbook","chunk_index":1,"access_groups":[],"tags":["phishing","email security"]}'::jsonb,
    sample_embedding(302)
),
(
    'finance/travel-expense-policy.md',
    'Travel Expense Reimbursement',
    'Travel expenses must be submitted within thirty days of trip completion. Receipts are required for lodging, airfare, rail travel, and any single expense over 25 dollars. Reimbursements are processed through payroll after manager approval and finance audit.',
    '{"department":"Finance","category":"policy","chunk_index":0,"access_groups":[],"tags":["travel","expenses","reimbursement"]}'::jsonb,
    sample_embedding(401)
),
(
    'finance/travel-expense-policy.md',
    'Corporate Card Usage',
    'Corporate cards may be used only for approved business expenses. Cardholders must upload receipts within five business days and reconcile transactions before the monthly close deadline. Personal purchases on a corporate card must be reported immediately.',
    '{"department":"Finance","category":"policy","chunk_index":1,"access_groups":["finance-team","managers"],"tags":["corporate card","expenses"]}'::jsonb,
    sample_embedding(402)
),
(
    'engineering/release-management.md',
    'Production Release Checklist',
    'Production releases require passing automated tests, completed code review, updated release notes, and an approved rollback plan. The release owner announces the maintenance window in the engineering channel and monitors service health for thirty minutes after deployment.',
    '{"department":"Engineering","category":"runbook","chunk_index":0,"access_groups":[],"tags":["release","deployment","rollback"]}'::jsonb,
    sample_embedding(501)
),
(
    'engineering/on-call-guide.md',
    'On-Call Escalation',
    'The primary on-call engineer acknowledges pages within ten minutes. If an incident cannot be mitigated within thirty minutes, the engineer escalates to the secondary on-call and incident commander. Customer-impacting incidents require status page updates every thirty minutes.',
    '{"department":"Engineering","category":"runbook","chunk_index":0,"access_groups":["engineering"],"tags":["on-call","incident","escalation"]}'::jsonb,
    sample_embedding(502)
);

INSERT INTO feedback (question, answer, rating, comment, user_id)
VALUES
(
    'How do I request VPN access?',
    'Submit a VPN access request in the IT service portal with a business reason, manager approval, and expected duration. MFA enrollment is required before activation.',
    5,
    'Accurate and cited the right IT guide.',
    'sample.user'
),
(
    'When should travel expenses be submitted?',
    'Travel expenses should be submitted within thirty days of trip completion.',
    4,
    'Helpful, but should mention receipts.',
    'finance.tester'
);

DROP FUNCTION sample_embedding(INTEGER);
