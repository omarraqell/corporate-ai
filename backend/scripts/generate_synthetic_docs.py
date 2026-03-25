"""
Generate synthetic company documents for the RAG knowledge base.

Uses deterministic templates so no LLM API key is required.
Run: python -m scripts.generate_synthetic_docs
"""

import json
from pathlib import Path

DATA_DIR = Path("data/synthetic_docs")

SOPS = [
    {
        "title": "SOP: Employee Onboarding Process",
        "content": """# Employee Onboarding Process

## Purpose
This SOP defines the standard process for onboarding new employees to ensure a consistent and thorough integration experience.

## Scope
Applies to all new hires across all departments.

## Procedure

### Step 1: Pre-Arrival (1 week before start date)
- HR sends welcome email with first-day instructions
- IT provisions laptop, email account, and system access
- Manager prepares onboarding schedule for first 2 weeks
- Assign a buddy/mentor from the same team

### Step 2: Day 1 — Orientation
- Welcome meeting with HR (company overview, policies, benefits)
- Office tour and introductions
- IT setup: laptop handoff, password creation, tool access
- Review and sign employment documents

### Step 3: Week 1 — Integration
- Daily check-ins with manager
- Complete mandatory compliance training
- Shadow team members on key workflows
- Access and review team documentation

### Step 4: Week 2-4 — Ramp Up
- Begin contributing to low-complexity tasks
- Attend all relevant team meetings
- Complete role-specific training modules
- First 1-on-1 with manager to set 30/60/90 day goals

### Step 5: 30-Day Review
- Manager conducts feedback session
- Review progress against initial goals
- Adjust onboarding plan if needed
- Buddy provides informal feedback

## Responsible Parties
- **HR**: Overall coordination, compliance training
- **IT**: System access and equipment
- **Hiring Manager**: Role-specific onboarding, goal setting
- **Buddy/Mentor**: Informal guidance and support
""",
    },
    {
        "title": "SOP: Incident Response Protocol",
        "content": """# Incident Response Protocol

## Purpose
Define the standard procedure for identifying, reporting, and resolving system incidents to minimize downtime and impact.

## Severity Levels

| Level | Description | Response Time | Example |
|-------|------------|---------------|---------|
| P1 - Critical | System down, all users affected | 15 minutes | Production database failure |
| P2 - High | Major feature broken, many users affected | 1 hour | Payment processing failure |
| P3 - Medium | Feature degraded, some users affected | 4 hours | Slow search performance |
| P4 - Low | Minor issue, workaround available | 24 hours | UI alignment bug |

## Procedure

### Step 1: Detection & Reporting
- Automated monitoring alerts trigger for P1/P2
- Any employee can report an incident via the #incidents Slack channel
- Reporter provides: description, severity estimate, affected systems, time first noticed

### Step 2: Triage (On-Call Engineer)
- Confirm severity level
- Create incident ticket in tracking system
- For P1/P2: immediately page the incident commander
- For P3/P4: assign to appropriate team during business hours

### Step 3: Response
- Incident commander assembles response team
- Establish communication channel (dedicated Slack thread)
- Post status updates every 30 minutes (P1) or 2 hours (P2)
- Focus on mitigation first, root cause second

### Step 4: Resolution
- Implement fix or workaround
- Verify resolution with affected users
- Update status page
- Close incident ticket with resolution details

### Step 5: Post-Mortem (within 48 hours for P1/P2)
- Document timeline of events
- Identify root cause
- List action items to prevent recurrence
- Share post-mortem with engineering team
- No blame — focus on systems and processes

## Escalation Path
1. On-Call Engineer → 2. Team Lead → 3. Engineering Manager → 4. VP Engineering → 5. CTO
""",
    },
    {
        "title": "SOP: Data Access Request Procedure",
        "content": """# Data Access Request Procedure

## Purpose
Ensure all access to sensitive data is authorized, logged, and compliant with data protection regulations.

## Scope
Applies to all employees, contractors, and third parties requesting access to company data systems.

## Data Classification
- **Public**: Marketing materials, blog posts, public documentation
- **Internal**: Internal communications, project plans, non-sensitive reports
- **Confidential**: Customer data, financial records, employee records
- **Restricted**: Encryption keys, authentication secrets, PII databases

## Procedure

### Step 1: Submit Request
- Requestor fills out Data Access Request form
- Required fields: data system, reason for access, duration needed, manager approval
- For Confidential/Restricted data: additional justification and VP approval required

### Step 2: Review
- Data steward reviews request within 2 business days
- Verifies business justification
- Checks compliance with data protection policies
- For Restricted data: security team review required

### Step 3: Approval & Provisioning
- Approved requests are provisioned by IT within 1 business day
- Access follows principle of least privilege
- Time-limited access preferred (auto-expires after stated duration)
- All access grants logged in audit system

### Step 4: Periodic Review
- All data access reviewed quarterly
- Unused access revoked automatically after 90 days of inactivity
- Annual recertification required for Confidential/Restricted access

## Compliance
- GDPR Article 25: Data protection by design and by default
- SOC 2 Type II: Access control requirements
- All access requests retained for 7 years for audit purposes
""",
    },
    {
        "title": "SOP: Client Escalation Workflow",
        "content": """# Client Escalation Workflow

## Purpose
Provide a structured process for handling client complaints and escalations to ensure timely resolution and client satisfaction.

## Escalation Tiers

### Tier 1: Support Agent
- First point of contact for all client issues
- Resolve within SLA: 4 hours for critical, 24 hours for standard
- Tools: Knowledge base, standard troubleshooting procedures
- Escalate if: issue cannot be resolved with available tools, client requests escalation, SLA at risk

### Tier 2: Senior Support / Team Lead
- Complex technical issues, billing disputes
- Resolve within: 8 hours for critical, 48 hours for standard
- Can offer service credits up to $500
- Escalate if: requires product change, credit exceeds authority, legal implications

### Tier 3: Department Manager
- Systemic issues, high-value client retention
- Resolve within: 24 hours
- Can offer service credits up to $5,000, custom SLA terms
- Escalate if: contract renegotiation needed, potential churn of enterprise client

### Tier 4: VP / Executive
- Strategic client relationships at risk
- Enterprise contract disputes
- Legal or regulatory implications
- No time limit — resolved as priority

## Communication Standards
- Acknowledge client within 1 hour of escalation
- Provide status updates at minimum every 4 hours during business hours
- Always communicate next steps and expected timeline
- Document all client interactions in CRM

## Post-Resolution
- Follow up with client within 48 hours
- Conduct internal review for Tier 3+ escalations
- Update knowledge base with resolution if applicable
- Track escalation metrics monthly
""",
    },
    {
        "title": "SOP: Code Review Process",
        "content": """# Code Review Process

## Purpose
Ensure all code changes meet quality, security, and maintainability standards before merging to production branches.

## Requirements
- All code changes require at least 1 approval before merge
- Changes to critical systems (auth, payments, data pipeline) require 2 approvals
- Self-merging is not allowed for production branches
- Reviews should be completed within 1 business day

## Reviewer Checklist
1. **Correctness**: Does the code do what the PR description claims?
2. **Testing**: Are there adequate tests? Do edge cases have coverage?
3. **Security**: No hardcoded secrets, SQL injection, XSS, or auth bypass
4. **Performance**: No N+1 queries, unnecessary loops, or memory leaks
5. **Readability**: Clear naming, appropriate comments, consistent style
6. **Architecture**: Follows established patterns, no unnecessary complexity

## PR Standards
- Title: Clear, concise description of the change
- Description: What changed, why, how to test, any migration steps
- Size: Aim for <400 lines changed. Split larger changes into stacked PRs
- Linked ticket: Every PR references the task/issue it addresses

## Merge Policy
- Squash merge for feature branches
- Merge commit for release branches
- All CI checks must pass before merge
- Branch protection enabled on main and release branches
""",
    },
    {
        "title": "SOP: Expense Reimbursement",
        "content": """# Expense Reimbursement

## Purpose
Define the process for submitting and approving business expense reimbursements.

## Eligible Expenses
- Business travel (flights, hotels, ground transport)
- Client meals and entertainment (with business justification)
- Professional development (conferences, courses, books)
- Home office equipment (up to $1,000/year)
- Software subscriptions required for role

## Submission Process
1. Submit expense report within 30 days of incurring the expense
2. Attach original receipt for all expenses over $25
3. Include: date, vendor, amount, business purpose, attendees (for meals)
4. Submit through expense management system

## Approval Thresholds
- Up to $500: Direct manager approval
- $500 - $2,000: Director approval
- $2,000 - $10,000: VP approval
- Over $10,000: CFO approval

## Reimbursement Timeline
- Approved expenses reimbursed within 10 business days
- Reimbursement via direct deposit to payroll account
- International expenses converted at date-of-transaction exchange rate

## Policy Violations
- Submitting personal expenses as business expenses
- Exceeding per-diem rates without prior approval
- Missing receipts for expenses over $25 (may be denied)
- Late submissions beyond 60 days (requires VP exception)
""",
    },
    {
        "title": "SOP: Quarterly Business Review Preparation",
        "content": """# Quarterly Business Review (QBR) Preparation

## Purpose
Standardize the process for preparing and conducting quarterly business reviews with key clients.

## Timeline
- **T-3 weeks**: Account manager initiates QBR prep, schedules client meeting
- **T-2 weeks**: Gather data (usage metrics, support tickets, feature adoption)
- **T-1 week**: Internal dry run with sales director, finalize deck
- **T-0**: Deliver QBR to client

## Required Data Points
1. Usage metrics vs. previous quarter
2. Support ticket volume and resolution times
3. Feature adoption rates for new releases
4. ROI metrics aligned to client's success criteria
5. Upcoming product roadmap items relevant to client
6. Contract renewal timeline and expansion opportunities

## Deck Structure
1. Executive Summary (1 slide)
2. Key Achievements This Quarter (2-3 slides)
3. Usage & Adoption Metrics (2-3 slides)
4. Support Summary (1 slide)
5. Roadmap Preview (1-2 slides)
6. Action Items & Next Steps (1 slide)

## Post-QBR
- Send meeting notes and action items within 24 hours
- Create follow-up tasks in CRM
- Update account health score
- Brief leadership on any risks or expansion signals
""",
    },
    {
        "title": "SOP: Security Vulnerability Disclosure",
        "content": """# Security Vulnerability Disclosure

## Purpose
Define the process for receiving, triaging, and resolving externally reported security vulnerabilities.

## Receiving Reports
- Security reports accepted via security@company.com
- Bug bounty program managed through HackerOne
- Auto-acknowledge receipt within 4 hours

## Triage Process
1. Security team reviews within 24 hours
2. Classify severity using CVSS v3.1 scoring
3. Critical (CVSS 9.0+): Immediate response team assembly
4. High (CVSS 7.0-8.9): Fix within 7 days
5. Medium (CVSS 4.0-6.9): Fix within 30 days
6. Low (CVSS 0.1-3.9): Fix within 90 days

## Resolution
- Develop and test fix in isolated environment
- Security team reviews the fix before deployment
- Deploy fix to production
- Verify fix resolves the vulnerability
- Notify reporter of resolution

## Disclosure
- Coordinate disclosure timeline with reporter (default: 90 days)
- Publish security advisory after fix is deployed
- Update CVE database if applicable
- Credit reporter (unless they prefer anonymity)

## Bug Bounty Rewards
- Critical: $5,000 - $15,000
- High: $2,000 - $5,000
- Medium: $500 - $2,000
- Low: $100 - $500
""",
    },
    {
        "title": "SOP: New Feature Release Process",
        "content": """# New Feature Release Process

## Purpose
Ensure consistent, safe, and well-communicated feature releases to production.

## Pre-Release Checklist
- [ ] All code reviewed and approved
- [ ] Automated tests passing (unit, integration, e2e)
- [ ] Performance benchmarks within acceptable range
- [ ] Security review completed (for features handling sensitive data)
- [ ] Documentation updated (API docs, user guides, changelog)
- [ ] Feature flag configured for gradual rollout
- [ ] Rollback plan documented

## Release Stages
1. **Internal Dogfood** (1-2 days): Enable for internal team
2. **Beta** (3-5 days): Enable for opt-in beta users (5-10%)
3. **Gradual Rollout** (5-7 days): 25% → 50% → 75% → 100%
4. **GA**: Feature flag removed, feature is default for all users

## Monitoring During Rollout
- Error rate: alert if >0.5% increase
- Latency: alert if p95 increases >20%
- User feedback: monitor support tickets and feedback channels
- Business metrics: track feature adoption and engagement

## Rollback Criteria
- Error rate spike >1% attributable to new feature
- P1 incident caused by feature
- Data integrity issue discovered
- Security vulnerability identified

## Post-Release
- Announce in #product-updates channel
- Send release notes to affected clients
- Monitor for 1 week post-GA
- Conduct release retrospective for major features
""",
    },
    {
        "title": "SOP: Vendor Evaluation and Procurement",
        "content": """# Vendor Evaluation and Procurement

## Purpose
Standardize the process for evaluating, selecting, and onboarding new vendors and SaaS tools.

## Request Process
1. Requestor submits vendor evaluation request
2. Include: business need, proposed vendor(s), estimated cost, alternatives considered
3. Requests over $10,000/year require RFP process

## Evaluation Criteria
- **Functionality**: Does it meet the stated requirements?
- **Security**: SOC 2 Type II, GDPR compliance, data encryption
- **Integration**: APIs, SSO support, existing tool compatibility
- **Cost**: Total cost of ownership including implementation
- **Support**: SLA guarantees, support channels, documentation quality
- **Scalability**: Can it grow with our needs over 3-5 years?

## Approval Process
- Under $5,000/year: Department manager
- $5,000 - $25,000/year: VP + Finance review
- $25,000 - $100,000/year: VP + CFO
- Over $100,000/year: Executive team + Board notification

## Security Review
Required for any vendor that will:
- Access company data
- Integrate with internal systems
- Store customer information
- Process payments

## Contract Requirements
- Data processing agreement (DPA) for any data access
- Right to audit clause
- Data portability and deletion upon termination
- SLA with financial penalties for downtime
""",
    },
    {
        "title": "SOP: Employee Offboarding",
        "content": """# Employee Offboarding

## Purpose
Ensure secure, compliant, and respectful separation of departing employees.

## Immediate Actions (within 24 hours of notice)
- HR schedules exit interview
- Manager notifies IT of departure date
- Finance calculates final pay and benefits

## IT Checklist (day of departure)
- Disable all system accounts (email, SSO, VPN, cloud services)
- Revoke API keys and access tokens
- Transfer ownership of shared documents and repositories
- Collect company equipment (laptop, phone, badges)
- Remove from all Slack/Teams channels and distribution lists
- Disable building access

## Knowledge Transfer (during notice period)
- Document ongoing projects and their status
- Transfer ownership of tasks and tickets
- Record key contacts and vendor relationships
- Update team documentation with any undocumented processes

## Final Steps
- Process final paycheck including unused PTO
- Provide COBRA/benefits continuation information
- Collect signed acknowledgment of confidentiality obligations
- Update org chart and team directory
- Conduct exit interview (HR)

## Post-Departure
- Monitor for unauthorized access attempts (30 days)
- Redirect email to manager for 90 days
- Archive, don't delete, departed employee's files
- Remove from vendor/partner contact lists
""",
    },
    {
        "title": "SOP: Change Management Process",
        "content": """# Change Management Process

## Purpose
Minimize risk from infrastructure and application changes through structured review and approval.

## Change Categories

### Standard Changes
- Pre-approved, low-risk changes with documented procedures
- Examples: dependency updates, config changes within approved ranges
- No CAB approval needed, just peer review

### Normal Changes
- Require Change Advisory Board (CAB) review
- Submit change request 3 business days in advance
- Examples: new service deployment, database migration, network changes

### Emergency Changes
- For active incidents or critical security patches
- Can bypass normal review process
- Requires post-implementation review within 48 hours
- Must be approved by on-call manager

## Change Request Requirements
- Description of change and business justification
- Risk assessment (impact and likelihood)
- Implementation plan with step-by-step instructions
- Rollback plan with estimated rollback time
- Testing evidence (staging environment results)
- Scheduled maintenance window (for Normal changes)

## CAB Review
- Meets twice weekly (Tuesday and Thursday)
- Reviews all pending Normal change requests
- Approves, requests modifications, or rejects
- Considers change collision (multiple changes same window)
""",
    },
    {
        "title": "SOP: Customer Data Deletion Request",
        "content": """# Customer Data Deletion Request (Right to Erasure)

## Purpose
Handle customer requests for data deletion in compliance with GDPR Article 17 and similar regulations.

## Process

### Step 1: Receive Request
- Customer submits request via support ticket, email, or in-app setting
- Log request in compliance tracking system
- Acknowledge receipt within 24 hours

### Step 2: Verify Identity
- Confirm requestor is the account owner or authorized representative
- Use existing authentication methods (email verification, security questions)
- For third-party requests: require written authorization from account owner

### Step 3: Assess Scope
- Identify all systems containing the customer's data
- Determine if any legal retention requirements apply
- Data that must be retained: financial records (7 years), legal holds, active contracts
- Inform customer of any data that cannot be deleted and the legal basis

### Step 4: Execute Deletion
- Remove data from primary databases
- Remove from backups within 30 days (or document exception)
- Remove from third-party processors (notify each processor)
- Remove from analytics and logging systems where feasible
- Anonymize data that cannot be fully deleted

### Step 5: Confirm
- Send deletion confirmation to customer within 30 days of request
- Record completion in compliance tracking system
- Retain deletion request record for audit purposes (metadata only)
""",
    },
    {
        "title": "SOP: Meeting Standards and Etiquette",
        "content": """# Meeting Standards and Etiquette

## Purpose
Ensure meetings are productive, inclusive, and respectful of everyone's time.

## Scheduling Standards
- All meetings must have a clear agenda shared at least 24 hours in advance
- Default meeting length: 25 minutes (not 30) or 50 minutes (not 60) to allow buffer
- No meetings before 9:00 AM or after 5:00 PM in any attendee's timezone
- "No Meeting Wednesday" — keep Wednesdays free for focused work
- Decline meetings without an agenda — it's encouraged, not rude

## During the Meeting
- Start on time, end on time
- Designate a note-taker at the start
- Follow the agenda — use a "parking lot" for off-topic items
- Encourage participation from all attendees
- Camera on is encouraged but not required

## Meeting Notes
- Shared within 2 hours of meeting end
- Include: decisions made, action items (with owners and deadlines), parking lot items
- Store in shared team space, not individual inboxes

## Recurring Meeting Hygiene
- Review all recurring meetings quarterly
- Cancel if the meeting consistently has no agenda or low attendance
- Every recurring meeting must have a designated owner
""",
    },
    {
        "title": "SOP: API Versioning and Deprecation",
        "content": """# API Versioning and Deprecation

## Purpose
Manage API lifecycle to ensure stability for consumers while allowing the platform to evolve.

## Versioning Strategy
- URL path versioning: `/api/v1/`, `/api/v2/`
- Major version bump for breaking changes only
- Minor/patch changes are backwards compatible within a version
- Maximum 2 major versions supported simultaneously

## Deprecation Process

### Step 1: Announce (T-6 months)
- Add `Sunset` header to deprecated endpoints
- Update API documentation with deprecation notice
- Email all registered API consumers
- Announce in developer changelog

### Step 2: Migration Support (T-6 to T-3 months)
- Publish migration guide with code examples
- Provide migration tooling where feasible
- Developer support team available for migration questions
- Track migration progress per consumer

### Step 3: Warning Phase (T-3 to T-1 month)
- Return `Warning` header on deprecated endpoint responses
- Increase frequency of deprecation reminders
- Reach out individually to consumers who haven't migrated

### Step 4: Sunset (T-0)
- Deprecated endpoints return 410 Gone
- Response body includes link to migration guide
- Monitor for unexpected breakage
- Keep 410 responses active for 6 months, then remove routes
""",
    },
]

ROUTING_RULES = [
    {
        "title": "Routing Rule: Technical and Code Requests",
        "content": """# Routing Rule: Technical and Code Requests

## Trigger Keywords
code, bug, error, fix, deploy, API, endpoint, database, migration, script, automate, debug, programming, function, server, docker, git, test, CI/CD, pipeline, infrastructure

## Route To
**Primary**: Code Dev Agent
**Secondary**: Data Analyst Agent (if involves data pipeline or query optimization)

## Decision Logic
- If the user asks to write, review, fix, or explain code → Code Dev
- If the query involves deployment, CI/CD, or infrastructure → Code Dev
- If it involves data transformation or SQL optimization → Code Dev + Data Analyst
- If it's a bug report with error logs → Code Dev (with Secretary logging the task)

## Context to Include
- Relevant codebase documentation from RAG
- Recent related tasks from Secretary's task log
- User's technical proficiency level from HR Memory

## Example Queries
- "Can you fix the authentication bug in the login endpoint?"
- "Write a Python script to process CSV files"
- "Help me set up Docker for the new microservice"
- "The API is returning 500 errors on the /users endpoint"
""",
    },
    {
        "title": "Routing Rule: Research and Investigation",
        "content": """# Routing Rule: Research and Investigation

## Trigger Keywords
research, investigate, find out, compare, analyze market, competitor, trends, best practices, industry, benchmark, explore, study, evaluate, assess

## Route To
**Primary**: Research Analyst Agent
**Secondary**: Writer Agent (for producing the final report)

## Decision Logic
- If the user wants information gathered or synthesized → Research Analyst
- If the research needs a formal report → Research Analyst → Writer
- If the research involves data analysis → Research Analyst + Data Analyst
- For competitive analysis → Research Analyst (with company docs context from RAG)

## Context to Include
- Company strategy documents from RAG
- Previous research reports (if any) from task history
- User's department and role for relevance filtering

## Example Queries
- "Research the top 5 competitors in our market segment"
- "What are the best practices for implementing SSO?"
- "Investigate the feasibility of expanding to the European market"
- "Compare AWS vs GCP vs Azure for our use case"
""",
    },
    {
        "title": "Routing Rule: Data Analysis Requests",
        "content": """# Routing Rule: Data Analysis Requests

## Trigger Keywords
data, analytics, metrics, dashboard, chart, graph, visualization, KPI, report numbers, statistics, trends, forecast, performance, conversion, revenue, growth, SQL, query

## Route To
**Primary**: Data Analyst Agent
**Secondary**: Writer Agent (for narrative reports)

## Decision Logic
- If the user wants data queried, analyzed, or visualized → Data Analyst
- If findings need a written narrative → Data Analyst → Writer
- If it involves building a dashboard → Data Analyst + Code Dev
- For financial analysis → Data Analyst (with financial docs from RAG)

## Context to Include
- Available data sources and schemas
- Previous analysis reports from task history
- Relevant company KPI definitions from RAG

## Example Queries
- "Analyze our user retention rates for Q4"
- "Create a chart showing monthly revenue growth"
- "What's our customer acquisition cost trend?"
- "Run a cohort analysis on users who signed up in January"
""",
    },
    {
        "title": "Routing Rule: Writing and Communication",
        "content": """# Routing Rule: Writing and Communication

## Trigger Keywords
write, draft, email, report, summary, document, proposal, presentation, blog, newsletter, announcement, memo, brief, press release, communication

## Route To
**Primary**: Writer Agent
**Secondary**: Research Analyst (if research is needed before writing)

## Decision Logic
- If the user wants content created from scratch → Writer
- If writing requires research or data → Research Analyst/Data Analyst first → Writer
- If it's a technical document → Code Dev provides input → Writer
- For client-facing communications → Writer (with client context from HR Memory)

## Context to Include
- Company brand and tone guidelines from RAG
- Client/recipient context from HR Memory
- Previous similar communications from task history
- Relevant company templates

## Example Queries
- "Draft a proposal for the new client project"
- "Write a summary of this week's team accomplishments"
- "Create an email announcing the new product feature"
- "Write documentation for the API endpoints"
""",
    },
    {
        "title": "Routing Rule: Task and Project Management",
        "content": """# Routing Rule: Task and Project Management

## Trigger Keywords
task, project, deadline, schedule, assign, priority, status, progress, track, plan, timeline, milestone, sprint, backlog, blocked, kanban, todo

## Route To
**Primary**: Secretary Agent
**Secondary**: None (Secretary handles directly)

## Decision Logic
- If the user asks about task status or project progress → Secretary
- If creating or assigning new tasks → Secretary
- If reorganizing priorities or timelines → Secretary
- If generating project reports → Secretary → Writer

## Context to Include
- Current task list and status from database
- Project timelines and milestones
- Team member assignments and availability

## Example Queries
- "What's the status of the website redesign project?"
- "Create a task to review the Q4 financial report by Friday"
- "Show me all tasks assigned to the engineering team"
- "What are the high-priority items for this sprint?"
""",
    },
    {
        "title": "Routing Rule: General Inquiries",
        "content": """# Routing Rule: General Inquiries

## Trigger Keywords
what is, how does, tell me about, explain, policy, procedure, where can I, who is responsible, company, team, department, HR, benefits, vacation, PTO

## Route To
**Primary**: Main Agent (CEO) handles directly using RAG
**Secondary**: None (answered from knowledge base)

## Decision Logic
- If the answer exists in company documents → CEO answers directly from RAG
- If it requires deeper investigation → route to Research Analyst
- If it's about task/project status → route to Secretary
- If the question is ambiguous → CEO asks clarifying question before routing

## Context to Include
- Full RAG search across all document types
- User's role and department from HR Memory
- Conversation history for context continuity

## Example Queries
- "What is our vacation policy?"
- "How does the expense reimbursement process work?"
- "Who should I contact about a billing issue?"
- "What are the company holidays this year?"
""",
    },
    {
        "title": "Routing Rule: Multi-Agent Collaboration",
        "content": """# Routing Rule: Multi-Agent Collaboration

## Trigger Keywords
(Complex queries that span multiple domains — detected by BERT classifier as "multi_agent")

## Route To
**Multiple agents in parallel**, determined by query analysis

## Common Multi-Agent Patterns

### Research + Write
- "Investigate X and write a report" → Research Analyst → Writer
- "Compare options and create a recommendation document" → Research Analyst → Writer

### Data + Write
- "Analyze Q4 data and create a presentation" → Data Analyst → Writer
- "Pull the metrics and write an executive summary" → Data Analyst → Writer

### Research + Data + Write
- "Full market analysis with data-backed recommendations" → Research + Data → Writer

### Code + Data
- "Build a dashboard for our sales metrics" → Code Dev + Data Analyst

### Any Agent + Secretary
- All multi-agent tasks automatically include Secretary for task tracking

## Orchestration Rules
1. Identify independent tasks → run in parallel
2. Identify dependent tasks → run sequentially (e.g., Research before Write)
3. Always pass intermediate results to downstream agents
4. Secretary logs all task assignments and completion
5. QA Reviewer evaluates the final combined output
""",
    },
    {
        "title": "Routing Rule: Escalation and Urgent Requests",
        "content": """# Routing Rule: Escalation and Urgent Requests

## Trigger Keywords
urgent, ASAP, emergency, critical, immediately, escalate, priority, deadline, overdue, blocking, incident, outage, down, broken

## Route To
**Primary**: Depends on content (analyzed after urgency detection)
**Elevated Priority**: All escalated tasks jump the queue

## Decision Logic
- Detect urgency first via BERT classifier ("escalation" label)
- Then analyze the actual content to determine the right agent(s)
- Flag the task as high priority in Secretary's tracking
- If it's a system incident → Code Dev (with incident SOP from RAG)
- If it's a client escalation → Research Analyst + Writer (with escalation SOP from RAG)

## Special Handling
- Escalated tasks get a faster QA review (streamlined, not skipped)
- CEO provides status updates to the user more frequently
- If resolution exceeds 1 hour, CEO proactively updates the user
- All escalations are logged for monthly review

## Example Queries
- "URGENT: The payment system is down!"
- "I need this report by end of day, it's for the board meeting"
- "Critical bug in production affecting all users"
- "Client X is threatening to cancel, need immediate action"
""",
    },
]

COMPANY_DOCS = [
    {
        "title": "Company Handbook: Our Culture and Values",
        "content": """# Our Culture and Values

## Mission
To empower businesses with intelligent automation that amplifies human capability, not replaces it.

## Core Values

### 1. Customer Obsession
Everything starts with the customer. We measure success by the value we deliver to the people who use our products. Every decision, feature, and priority should trace back to a customer need.

### 2. Radical Transparency
We share information openly — financials, strategy, challenges. Bad news travels fast; good news can wait. Everyone has the context they need to make good decisions.

### 3. Bias for Action
Perfect is the enemy of good. We prefer reversible decisions made quickly over perfect decisions made slowly. When in doubt, try it, measure it, learn from it.

### 4. Own the Outcome
Don't just do your part — own the result. If something falls through the cracks between teams, pick it up. Titles don't define scope; outcomes do.

### 5. Build for Scale
Think beyond today's problem. Our solutions should handle 10x the current load. Invest in foundations, not just features.

## Working Norms
- Default to async communication (Slack, docs) over meetings
- Document decisions, not just discussions
- "Disagree and commit" — healthy debate, unified execution
- No heroics — sustainable pace produces better outcomes than crunch
- Celebrate learning from failure as much as success
""",
    },
    {
        "title": "Product Overview: Platform Capabilities",
        "content": """# Product Overview

## What We Build
An AI-powered business automation platform that helps mid-market companies streamline operations, improve decision-making, and scale efficiently.

## Core Modules

### 1. Workflow Automation
- Visual workflow builder (drag-and-drop)
- Trigger-based automation (events, schedules, conditions)
- Integration with 200+ business tools (CRM, ERP, HRIS)
- Custom webhook support for proprietary systems

### 2. Intelligent Document Processing
- OCR and document classification
- Automated data extraction from invoices, contracts, forms
- Validation against business rules
- Human-in-the-loop review for low-confidence extractions

### 3. Analytics Dashboard
- Real-time business metrics and KPIs
- Custom report builder
- Automated report distribution (daily, weekly, monthly)
- Anomaly detection and alerting

### 4. Communication Hub
- Unified inbox for email, chat, and social
- AI-suggested responses
- Automated routing based on content analysis
- SLA tracking and escalation

## Technical Architecture
- Cloud-native (AWS primary, multi-cloud capable)
- Microservices architecture
- Event-driven processing (Kafka)
- GraphQL API for integrations
- SOC 2 Type II certified
- 99.9% uptime SLA

## Target Market
- Mid-market companies (100-5,000 employees)
- Industries: Financial Services, Healthcare, Manufacturing, Professional Services
- Decision makers: COO, CTO, VP Operations
""",
    },
    {
        "title": "Engineering Standards",
        "content": """# Engineering Standards

## Language and Framework Standards
- **Backend**: Python (FastAPI) or Go for performance-critical services
- **Frontend**: TypeScript + Next.js (React)
- **Mobile**: React Native
- **Infrastructure**: Terraform for IaC, Kubernetes for orchestration
- **Database**: PostgreSQL (primary), Redis (cache), Elasticsearch (search)
- **Message Queue**: Apache Kafka

## Code Standards
- All code must pass linting (ruff for Python, ESLint for TypeScript)
- Type hints required for all Python function signatures
- 80% minimum test coverage for new code
- No commented-out code in production branches
- Use conventional commits for commit messages

## API Standards
- RESTful design for external APIs
- GraphQL for internal frontend-backend communication
- All endpoints require authentication (except health checks)
- Rate limiting on all public endpoints
- Request/response validation using Pydantic (Python) or Zod (TypeScript)

## Security Standards
- No secrets in code — use environment variables or vault
- All data encrypted at rest (AES-256) and in transit (TLS 1.3)
- SQL parameterized queries only — no string concatenation
- OWASP Top 10 review for all web-facing features
- Dependency scanning in CI (Snyk or Dependabot)

## Deployment
- GitOps workflow: merge to main triggers deploy to staging
- Staging → Production promotion requires QA sign-off
- Blue-green deployment strategy
- Automated rollback on health check failure
- Feature flags for all new features (LaunchDarkly)
""",
    },
    {
        "title": "Marketing Guidelines",
        "content": """# Marketing Guidelines

## Brand Voice
- **Tone**: Professional but approachable. Smart, not stuffy.
- **Language**: Clear, concise, jargon-free. Explain complex concepts simply.
- **Personality**: Confident and helpful. We're experts who make you feel capable, not intimidated.

## Brand Assets
- Primary color: #2563EB (blue)
- Secondary color: #10B981 (green)
- Font: Inter for web, SF Pro for mobile
- Logo: Use SVG format, maintain clear space of 1x logo height on all sides

## Content Standards
- Blog posts: 800-1,500 words, one clear topic per post
- Case studies: Problem → Solution → Results format, include metrics
- Social media: Focus on value and insights, not product promotion
- Email: Subject lines under 50 characters, preview text under 90 characters

## SEO Guidelines
- Target 1-2 primary keywords per page
- Include keywords in title, H1, first paragraph, and meta description
- Internal linking: every page links to at least 2 other relevant pages
- Alt text on all images
- Page load time under 3 seconds

## Campaign Approval Process
1. Creative brief submitted to Marketing Director
2. Draft reviewed by Brand Manager
3. Legal review for claims, testimonials, compliance
4. Final approval from CMO for campaigns over $10,000
""",
    },
    {
        "title": "Q1 2026 Strategy Memo",
        "content": """# Q1 2026 Strategic Priorities

## Executive Summary
Q1 focuses on three pillars: product-led growth expansion, enterprise readiness, and operational efficiency. Our ARR target is $12M by end of Q1, representing 40% YoY growth.

## Priority 1: Product-Led Growth
**Owner**: VP Product
- Launch self-serve onboarding flow (reduce time-to-value from 14 days to 2 days)
- Implement usage-based pricing tier for SMB segment
- Build in-app upgrade prompts based on usage patterns
- Target: 500 new self-serve signups in Q1

## Priority 2: Enterprise Readiness
**Owner**: VP Engineering
- Complete SOC 2 Type II audit (audit scheduled for March)
- Implement SSO/SAML for enterprise clients
- Build admin console for multi-team management
- Achieve HIPAA compliance for healthcare vertical
- Target: Close 3 enterprise deals ($100K+ ARR each)

## Priority 3: Operational Efficiency
**Owner**: COO
- Reduce customer support response time from 4 hours to 1 hour
- Implement AI-assisted ticket routing (using our own platform)
- Automate 60% of onboarding tasks
- Reduce infrastructure costs by 20% through optimization

## Key Risks
1. SOC 2 audit delay could block enterprise pipeline
2. Self-serve flow requires significant engineering investment (6 engineers, full quarter)
3. Competitor X launching similar product in February — need differentiation messaging

## Budget Allocation
- Engineering: 55% (product development + infrastructure)
- Sales & Marketing: 25% (enterprise sales team + PLG campaigns)
- Operations: 15% (support tooling + process automation)
- Reserve: 5% (contingency)
""",
    },
    {
        "title": "Benefits and Compensation Overview",
        "content": """# Benefits and Compensation

## Compensation Philosophy
We pay at the 75th percentile of market rates for comparable roles in comparable markets. Compensation is reviewed annually in April, with mid-year adjustments for promotions or market corrections.

## Base Compensation
- Salary bands published internally for every level and role
- Annual merit increase pool: 3-5% of total compensation budget
- Promotion increases: typically 10-15% base salary adjustment

## Equity
- All full-time employees receive equity grants
- 4-year vesting schedule with 1-year cliff
- Refresh grants awarded annually based on performance
- Equity value updated quarterly with latest 409A valuation

## Benefits

### Health & Wellness
- Medical, dental, and vision insurance (company pays 90% of premiums)
- Mental health support: free therapy sessions (up to 12/year)
- $500/year wellness stipend (gym, fitness apps, ergonomic equipment)
- Paid parental leave: 16 weeks (all parents, regardless of gender)

### Time Off
- Unlimited PTO with 15-day minimum (we track to ensure people take time off)
- 11 company holidays
- 1 week company-wide shutdown in December
- Sick leave: no cap, no questions asked

### Professional Development
- $2,000/year learning budget (courses, conferences, books)
- Internal mentorship program
- Quarterly lunch-and-learn sessions
- Conference speaking opportunities supported

### Other
- Remote-first (optional offices in NYC and London)
- $1,000 home office setup stipend (one-time)
- $100/month internet and phone reimbursement
- 401(k) with 4% company match
""",
    },
    {
        "title": "Sales Playbook: Enterprise Deals",
        "content": """# Sales Playbook: Enterprise Deals

## Ideal Customer Profile
- Company size: 500-5,000 employees
- Industries: Financial Services, Healthcare, Manufacturing, Professional Services
- Pain points: Manual processes, data silos, slow decision-making, compliance burden
- Budget authority: VP+ level, $100K+ annual budget for automation tools
- Technology maturity: Has existing tech stack, looking to optimize not build from scratch

## Sales Process

### Stage 1: Discovery (Week 1-2)
- Identify key stakeholders: Economic Buyer, Technical Buyer, Champion, User
- Discovery call: understand current pain points, processes, and goals
- Map their buying process and timeline
- Qualify using MEDDIC framework

### Stage 2: Demo & Value Prop (Week 3-4)
- Tailored demo focused on their top 3 use cases
- ROI calculator: show projected time/cost savings
- Technical deep-dive with their IT/engineering team
- Provide customer references in their industry

### Stage 3: Pilot/POC (Week 5-8)
- Define success criteria upfront (measurable KPIs)
- Dedicated solutions engineer for implementation
- Weekly check-ins during pilot
- Document results vs. success criteria

### Stage 4: Negotiation (Week 9-10)
- Present pilot results to economic buyer
- Propose contract terms (annual preferred, multi-year discounted)
- Address procurement and legal requirements
- Security questionnaire and compliance documentation

### Stage 5: Close (Week 11-12)
- Final contract review and signature
- Transition to Customer Success team
- Schedule implementation kickoff
- Announce internally and celebrate

## Pricing Guidance
- Enterprise tier: $8-15 per user/month (volume discounts above 500 users)
- Implementation fee: $15,000-50,000 depending on complexity
- Multi-year discount: 10% for 2-year, 15% for 3-year
- Never discount more than 25% without VP Sales approval
""",
    },
    {
        "title": "Customer Success Playbook",
        "content": """# Customer Success Playbook

## Mission
Ensure every customer achieves their desired outcomes and becomes an advocate for our platform.

## Customer Lifecycle

### Onboarding (Month 1-2)
- Kick-off call within 3 days of contract signing
- Implementation plan with clear milestones
- Weekly check-ins during implementation
- Training sessions for admin users and end users
- Go-live support with dedicated engineer
- Success criteria defined and documented

### Adoption (Month 3-6)
- Monthly business reviews
- Track feature adoption metrics
- Identify and address low-adoption areas
- Share best practices and new use cases
- Introduce to customer community

### Growth (Month 6+)
- Quarterly Business Reviews (QBRs)
- Expansion opportunity identification
- New use case discovery and implementation
- Executive relationship building
- Reference and case study requests

## Health Score Components
- **Product Usage** (30%): Daily active users, feature breadth, API calls
- **Support** (20%): Ticket volume trend, satisfaction scores, time to resolution
- **Engagement** (25%): Meeting attendance, training completion, community participation
- **Business Outcomes** (25%): ROI achievement, stated goals progress

## Risk Indicators
- Usage drop >20% month-over-month
- Support tickets increasing with negative sentiment
- Champion leaves the organization
- No executive engagement for 2+ quarters
- Contract renewal <90 days with no expansion discussion

## Renewal Process
- Begin renewal conversation at T-120 days
- Present value delivered (metrics, ROI, success stories)
- Propose expansion if health score is high
- Escalate at-risk accounts to VP CS at T-90 days
""",
    },
    {
        "title": "Information Security Policy",
        "content": """# Information Security Policy

## Purpose
Protect company and customer data through comprehensive security controls, processes, and awareness.

## Data Handling

### Classification and Handling Requirements
- **Public**: No restrictions on sharing
- **Internal**: Share within company only, no external transmission without encryption
- **Confidential**: Need-to-know basis, encrypted at rest and in transit, access logged
- **Restricted**: Named individuals only, multi-factor access, full audit trail

### Data Retention
- Customer data: retained for duration of contract + 30 days
- Financial records: 7 years
- Employee records: duration of employment + 3 years
- System logs: 1 year
- Backup data: 90 days rolling

## Access Control
- Principle of least privilege for all systems
- Multi-factor authentication required for all internal systems
- Password requirements: 12+ characters, complexity enforced, 90-day rotation
- Privileged access requires separate admin accounts
- Access reviewed quarterly, revoked within 24 hours of role change

## Incident Response
- See SOP: Incident Response Protocol for detailed procedures
- All employees must report suspected security incidents immediately
- Security team on-call 24/7 via #security-urgent Slack channel

## Employee Responsibilities
- Complete annual security awareness training
- Lock screens when away from desk
- Report phishing attempts to security team
- Do not install unauthorized software on company devices
- Do not store company data on personal devices or accounts

## Compliance
- SOC 2 Type II (annual audit)
- GDPR (EU customer data)
- HIPAA (healthcare customers, in progress)
- Annual penetration testing by third-party firm
""",
    },
    {
        "title": "Remote Work Policy",
        "content": """# Remote Work Policy

## Overview
We are a remote-first company. All roles can be performed fully remote unless specifically designated as on-site. Offices in NYC and London are available for optional use.

## Expectations

### Availability
- Core hours: 10:00 AM - 3:00 PM in your local timezone (for synchronous collaboration)
- Outside core hours: flexible, as long as work is completed
- Update your calendar and Slack status to reflect availability
- Respond to messages within 4 hours during working hours

### Communication
- Default to async (Slack messages, Loom videos, shared docs)
- Use video calls for complex discussions, brainstorming, or sensitive topics
- Document all decisions and action items from calls
- Over-communicate context — remote colleagues don't have hallway conversations

### Workspace
- Maintain a dedicated, secure workspace
- Reliable internet connection (minimum 25 Mbps)
- Use company VPN when accessing internal systems
- Do not work from public WiFi without VPN
- Home office stipend: $1,000 one-time + $100/month for internet

## In-Person
- Team offsites: 2-3 times per year (company-funded travel)
- Company all-hands: annually (all expenses covered)
- Office use: optional, book a desk via the office app
- Co-working space reimbursement: up to $300/month (with manager approval)

## Performance
- Measured by outcomes, not hours online
- Regular 1-on-1s with manager (minimum biweekly)
- Participation in team rituals (standups, retros, planning)
- Proactive communication about blockers and progress
""",
    },
]


def generate_all():
    """Write all synthetic documents to disk."""
    categories = {
        "sop": SOPS,
        "routing_rule": ROUTING_RULES,
        "company_doc": COMPANY_DOCS,
    }

    total = 0
    for category, docs in categories.items():
        category_dir = DATA_DIR / category
        category_dir.mkdir(parents=True, exist_ok=True)

        for doc in docs:
            # Create a safe filename
            safe_title = doc["title"].replace(":", "").replace("/", "-").replace(" ", "_")
            file_path = category_dir / f"{safe_title}.md"
            file_path.write_text(doc["content"], encoding="utf-8")
            total += 1

    print(f"Generated {total} synthetic documents across {len(categories)} categories:")
    for category, docs in categories.items():
        print(f"  {category}: {len(docs)} documents")

    # Write manifest for easy reference
    manifest = {
        category: [d["title"] for d in docs]
        for category, docs in categories.items()
    }
    manifest_path = DATA_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Manifest written to {manifest_path}")


if __name__ == "__main__":
    generate_all()
