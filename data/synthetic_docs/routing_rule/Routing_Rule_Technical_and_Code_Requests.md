# Routing Rule: Technical and Code Requests

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
