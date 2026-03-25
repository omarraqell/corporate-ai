# API Versioning and Deprecation

## Purpose
Manage API lifecycle to ensure stability for consumers while allowing the platform to evolve.

## Versioning Strategy
- URL path versioning: `/api/v1/`, `/api/v2/`
- Major version bump for breaking changes only
- Minor/patch changes are backwards compatible within a version
- Maximum 2 major versions supported simultaneously

## Deprecation Process

### Step 1: Announce (T-6 months)
- Add `Sunset` header to deprecated endpoints
- Update API documentation with deprecation notice
- Email all registered API consumers
- Announce in developer changelog

### Step 2: Migration Support (T-6 to T-3 months)
- Publish migration guide with code examples
- Provide migration tooling where feasible
- Developer support team available for migration questions
- Track migration progress per consumer

### Step 3: Warning Phase (T-3 to T-1 month)
- Return `Warning` header on deprecated endpoint responses
- Increase frequency of deprecation reminders
- Reach out individually to consumers who haven't migrated

### Step 4: Sunset (T-0)
- Deprecated endpoints return 410 Gone
- Response body includes link to migration guide
- Monitor for unexpected breakage
- Keep 410 responses active for 6 months, then remove routes
