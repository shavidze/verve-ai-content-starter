# Scale-up architecture

## MVP
Claude Code (orchestrator) -> subagents -> local JSON plan + input video -> Python + FFmpeg -> output + QA report -> human publishing approval.

## Production options (later)
- Upload API and authorized identity/consent tracking
- Job queue, e.g. Redis + queue worker; durable job states
- Object storage per tenant with limited retention
- Transcript service that supports Georgian and manually verified timecodes
- Speaker/face track with review for auto crop
- Remotion component templates with branded, editable parameters
- Approval dashboard (original / v1 / v2 comparison)
- Signed URLs and media access audit
- API-based rendering and monitoring

Do not introduce LangGraph, a complex agent graph, or external MCP services for a local single-client pilot. Consider them only when persistent workflows, retries and external-system state justify the overhead.
