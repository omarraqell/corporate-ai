# Routing Rule: Escalation and Urgent Requests

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
