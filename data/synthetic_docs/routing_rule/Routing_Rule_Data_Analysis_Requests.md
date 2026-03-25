# Routing Rule: Data Analysis Requests

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
