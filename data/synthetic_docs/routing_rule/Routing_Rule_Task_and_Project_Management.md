# Routing Rule: Task and Project Management

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
