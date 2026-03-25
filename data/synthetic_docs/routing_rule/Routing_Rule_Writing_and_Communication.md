# Routing Rule: Writing and Communication

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
