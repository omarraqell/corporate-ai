# Incident Response Protocol

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
