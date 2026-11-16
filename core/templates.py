"""
Enterprise Meeting Templates for SyncOps AI
Provides realistic, high-fidelity transcripts for B2B onboarding, incident postmortems, and strategy syncs.
"""

TEMPLATES = {
    "B2B Enterprise SaaS Onboarding": {
        "title": "Fintech Global & CloudSync Enterprise Integration Kickoff",
        "description": "Enterprise customer kickoff call focusing on API security, SSO configuration, SLA commitments, and go-live timeline.",
        "participants": ["Priya Sharma (VP Solutions, CloudSync)", "Marcus Vance (Director of SecOps, Fintech Global)", "Elena Rostova (Lead Data Architect, Fintech Global)", "Alex Rivera (Customer Success Manager, CloudSync)"],
        "transcript": """[00:00] Alex Rivera: Good morning everyone. Welcome to the official integration kickoff for Fintech Global and CloudSync. On the line we have Priya from our solutions engineering side, and Marcus and Elena from Fintech Global. Our target go-live date is November 30th.
[00:45] Marcus Vance: Thanks Alex. From SecOps, our primary mandate is zero-trust architecture. We cannot allow plain API keys in environment files. All integrations must authenticate using mutual TLS (mTLS) with certificates rotated every 90 days, or via OAuth2 client credential grant with IP whitelisting.
[01:30] Priya Sharma: Completely aligned, Marcus. CloudSync supports OAuth2 with CIDR block IP whitelisting natively. We will whitelist Fintech Global's egress gateway IPs today. Marcus, can your team provision the static IP addresses by this Thursday, 5 PM EST?
[02:05] Marcus Vance: Yes, I will assign that to our infrastructure team by Thursday 5 PM. Elena will handle the data pipeline schema mapping.
[02:20] Elena Rostova: That's right. We have approximately 4.2 million transaction records stored in PostgreSQL that need daily delta synchronization into CloudSync's analytical lake. We need webhook callbacks for failed sync jobs so our PagerDuty alerts fire automatically.
[03:10] Priya Sharma: CloudSync provides standard Webhook v2 endpoints with HMAC-SHA256 signature verification. Elena, I will send you the Postman collection and JSON schema specs by tomorrow afternoon.
[03:45] Elena Rostova: Perfect. I will review the schema and build the ingestion staging tables by Monday next week.
[04:15] Alex Rivera: Excellent. Regarding governance and compliance: Fintech Global requires 99.95% uptime SLA with a 15-minute response window for P1 critical tickets. Priya, can we confirm the platinum support tier documentation?
[04:50] Priya Sharma: Confirmed. The Platinum SLA addendum is signed and active in our Salesforce portal.
[05:15] Marcus Vance: One blocker to flag: our legal team needs CloudSync's SOC2 Type II audit report renewed version before our final security review signoff on November 25th.
[05:40] Alex Rivera: I am taking that action item. I will upload the fresh SOC2 Type II compliance pack to your shared box folder by Friday.
[06:05] Priya Sharma: To summarize: Thursday static IPs from Marcus, Wednesday webhook schemas from me, Monday staging tables from Elena, Friday SOC2 report from Alex. Let's schedule our next sprint check-in for next Tuesday at 10 AM EST."""
    },
    "Critical Production Incident Postmortem": {
        "title": "INC-8902: Database Connection Pool Exhaustion & Checkout Outage Postmortem",
        "description": "Engineering postmortem review analyzing a 27-minute payment gateway outage, root cause analysis, and remediation SOPs.",
        "participants": ["Kavita Menon (Head of Site Reliability Engineering)", "Rohan Gupta (Principal Backend Engineer)", "Sarah Jenkins (Incident Commander / DevOps)", "David Zhao (Product Manager, Payments)"],
        "transcript": """[00:00] Sarah Jenkins: Let's begin the postmortem for incident INC-8902. On Sunday at 14:12 UTC, checkout latency spiked to 18 seconds, followed by 504 gateway timeouts across our EMEA and APAC clusters. Total degraded duration was 27 minutes, affecting roughly 14,000 checkout attempts.
[01:05] Rohan Gupta: I reviewed the telemetry and connection metrics. The root cause was an unindexed query introduced in release v2.41 on the discount redemption endpoint. Under peak Black Friday traffic, query execution time ballooned from 12ms to 4,200ms.
[01:45] Kavita Menon: Because the discount microservice didn't enforce a client-side execution timeout, database connections remained pinned indefinitely, exhausting the HikariCP connection pool on the primary read-replica cluster.
[02:30] Sarah Jenkins: Why didn't the circuit breaker trip automatically when database saturation exceeded 95%?
[02:50] Rohan Gupta: The resilience4j circuit breaker was misconfigured with a 30-second sliding evaluation window instead of a 5-second window, so it took too long to open the circuit and divert traffic to the fallback cache.
[03:30] David Zhao: What was the estimated financial and client impact?
[03:45] Sarah Jenkins: We estimate $38,000 in delayed transactions. Luckily, our transaction queue preserved failed orders, and 85% were reprocessed automatically within 2 hours once the hotfix deployed.
[04:20] Kavita Menon: Here are the mandatory corrective actions: First, Rohan must push a database migration adding composite indexes on `discount_codes(code, tenant_id, valid_until)` by tomorrow EOD.
[04:55] Rohan Gupta: Understood. I will also write a query performance regression test in our CI/CD pipeline so unindexed foreign key lookups fail the build.
[05:25] Sarah Jenkins: Second, SRE team will update the HikariCP connection pool configuration: reduce max connection lifetime to 10 minutes and add strict 1,500ms query timeouts across all downstream database clients by Wednesday.
[06:00] Kavita Menon: Third, we need a formal SOP for database pool degradation. When connection pool utilization breaches 85% for 60 seconds, automated read-replica scaling must trigger, and non-essential background reporting queries must be paused immediately.
[06:40] Sarah Jenkins: I will write and publish the new Incident SOP-DB-09 by Friday noon and schedule a tabletop drill with the on-call rotation next week."""
    },
    "Quarterly AI & Product Strategy Sync": {
        "title": "Q1 AI Copilot & Customer Support Automation Roadmap",
        "description": "Executive product sync establishing metrics, human-in-the-loop review guardrails, and sprint deliverables for enterprise AI deployment.",
        "participants": ["Vikramaditya Rao (Chief Product Officer)", "Ananya Sen (Lead AI Research Engineer)", "Tanya Becker (Director of Customer Support)", "Nikhil Patel (Engineering Lead)"],
        "transcript": """[00:00] Vikramaditya Rao: Team, today's objective is locking in our Q1 roadmap for our Customer Support AI Copilot. Our core mandate from leadership is deflecting 40% of tier-1 support tickets while improving CSAT from 86% to 92%.
[00:45] Tanya Becker: My support team is enthusiastic, but their main concern is hallucinations on refund policies. If an AI promises a customer a $500 refund against company policy, our agents take the heat. We cannot deploy without strict human-in-the-loop controls.
[01:30] Ananya Sen: Agreed, Tanya. Here is our architectural defense: Any AI-generated resolution involving refunds over $50 or account suspensions will be flagged with a 'Confidence: Human Review Needed' tag and held in a staging queue for agent approval.
[02:15] Nikhil Patel: In terms of latency, the response draft must render in Zendesk within 1.2 seconds so agents aren't waiting around. We evaluated Gemini 1.5 Flash and Claude 3.5 Sonnet. Gemini Flash is giving us 450ms time-to-first-token with 99.2% schema adherence.
[03:00] Vikramaditya Rao: Let's lock in Gemini 1.5 Flash as our default inference model for ticket summarization and draft responses. Ananya, what is your training and evaluation dataset status?
[03:40] Ananya Sen: We have cleaned 50,000 anonymized historical tickets with PII masking applied. I will complete the baseline benchmark eval against human agent responses by next Friday, Dec 5th.
[04:25] Nikhil Patel: On the infrastructure side, my team will build the Zendesk sidebar Chrome extension by Dec 15th. We need Tanya's team to designate 5 senior agents for closed alpha testing starting Dec 18th.
[05:00] Tanya Becker: I will select 5 senior tier-2 agents by next Tuesday and allocate 2 hours per day from their schedule for feedback logging.
[05:35] Vikramaditya Rao: Perfect. Key milestones: Dec 5th benchmark results from Ananya, Dec 15th extension build from Nikhil, Dec 18th alpha kickoff with Tanya's agents. Let's reconvene on Dec 8th for the evaluation review."""
    }
}
