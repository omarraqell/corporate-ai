# Routing Rule: General Inquiries

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
