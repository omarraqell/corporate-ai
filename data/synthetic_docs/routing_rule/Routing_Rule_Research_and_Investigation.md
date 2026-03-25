# Routing Rule: Research and Investigation

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
