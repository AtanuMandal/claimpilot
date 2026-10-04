# ClaimPilot — Requirements

**Goal:** take a motor or health insurance claim from submission to decision.
Low-risk claims are settled automatically; risky or high-value claims go to a human adjuster.

## 1. Users

| Role | Needs |
|---|---|
| Claimant | Submit a claim, upload documents, answer follow-up questions, track status |
| Adjuster | Review escalated claims; approve, edit or reject with a full case summary |
| Admin | Configure thresholds; view metrics, cost and audit trail |

## 2. Functional requirements

| ID | Requirement |
|---|---|
| FR-1 | A claimant can submit a claim: policy number, incident type, date, description, amount and documents |
| FR-2 | If information is missing, the system asks the claimant and **waits** for the answer (minutes or days) |
| FR-3 | Documents (bills, photos) are read and key fields extracted — amount, date, provider, vehicle number — each with a **confidence score** |
| FR-4 | Coverage check: policy is active, incident is covered, deductible and limits applied |
| FR-5 | Fraud check: a risk score from 0 to 1, using rules and the claimant's history |
| FR-6 | Coverage and fraud checks run **in parallel** |
| FR-7 | Settlement: payout is calculated and a decision letter drafted |
| FR-8 | **Human review** is required when any threshold rule fires (section 3) |
| FR-9 | An adjuster can **approve**, **edit** (amount or reason) or **reject**; processing resumes from where it paused |
| FR-10 | The claimant is notified of the outcome (email / SMS — mocked in this project) |
| FR-11 | Every claim is durable: survives restarts, status can be queried at any time, history can be replayed |
| FR-12 | Long-term memory: claimant profile, prior claims, fraud signals and adjuster feedback |
| FR-13 | Live progress is streamed to the user interface |

## 3. Human-in-the-loop rules

A claim is escalated to an adjuster if **any** rule fires.

| Rule | Default |
|---|---|
| Claim amount | > ₹1,00,000 |
| Fraud score | ≥ 0.7 |
| Document extraction confidence | < 0.8 |
| Coverage decision | Unclear |

- Thresholds are **configuration**, not prompts — changeable without code changes.
- Rules are plain functions with unit tests, so decisions are predictable and auditable.

## 4. Non-functional requirements

| Area | Requirement |
|---|---|
| LLM | Google Gemini by default; switchable to OpenAI or Anthropic Claude through configuration only |
| Cost | Per-claim token and cost budget with a hard stop |
| Reliability | Retries with back-off, model fallback, timeouts, idempotent APIs |
| Privacy | Personal data (names, phone, Aadhaar, PAN) redacted before it reaches the LLM |
| Security | Authentication with claimant / adjuster / admin roles; secrets never in code |
| Audit | Every model call, tool call and decision recorded |
| Observability | Tracing of every agent step; structured logs; latency and cost per claim |
| Quality | Unit and integration tests; an evaluation dataset with automated scoring; quality gate in CI |
| Delivery | Docker images; CI/CD with GitHub Actions; production on AWS (ECS Fargate, RDS, ElastiCache, CloudFront) defined with AWS CDK |
| Environments | local, staging, production |

## 5. Technology

Python 3.12 · uv · LangChain · LangGraph · Pydantic · FastAPI · PostgreSQL + pgvector · Redis ·
Langfuse · Angular · Docker · GitHub Actions · AWS CDK

## 6. Out of scope (v1)

- Real payment processing
- A commercial OCR service (a vision-capable LLM is used instead)
- Multi-tenancy (one insurer)
- Mobile apps
