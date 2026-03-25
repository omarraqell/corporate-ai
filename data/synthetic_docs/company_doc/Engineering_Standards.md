# Engineering Standards

## Language and Framework Standards
- **Backend**: Python (FastAPI) or Go for performance-critical services
- **Frontend**: TypeScript + Next.js (React)
- **Mobile**: React Native
- **Infrastructure**: Terraform for IaC, Kubernetes for orchestration
- **Database**: PostgreSQL (primary), Redis (cache), Elasticsearch (search)
- **Message Queue**: Apache Kafka

## Code Standards
- All code must pass linting (ruff for Python, ESLint for TypeScript)
- Type hints required for all Python function signatures
- 80% minimum test coverage for new code
- No commented-out code in production branches
- Use conventional commits for commit messages

## API Standards
- RESTful design for external APIs
- GraphQL for internal frontend-backend communication
- All endpoints require authentication (except health checks)
- Rate limiting on all public endpoints
- Request/response validation using Pydantic (Python) or Zod (TypeScript)

## Security Standards
- No secrets in code — use environment variables or vault
- All data encrypted at rest (AES-256) and in transit (TLS 1.3)
- SQL parameterized queries only — no string concatenation
- OWASP Top 10 review for all web-facing features
- Dependency scanning in CI (Snyk or Dependabot)

## Deployment
- GitOps workflow: merge to main triggers deploy to staging
- Staging → Production promotion requires QA sign-off
- Blue-green deployment strategy
- Automated rollback on health check failure
- Feature flags for all new features (LaunchDarkly)
