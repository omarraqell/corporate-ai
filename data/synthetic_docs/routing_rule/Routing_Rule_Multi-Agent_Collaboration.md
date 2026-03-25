# Routing Rule: Multi-Agent Collaboration

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
