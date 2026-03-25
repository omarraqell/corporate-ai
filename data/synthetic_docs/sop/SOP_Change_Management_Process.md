# Change Management Process

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
