# Publication capability and decision record

Observed 2026-09-07 UTC. This is a read-only capability assessment and a reviewable path, not a publication receipt. No Tanduna or GitHub objects, votes, messages, configuration, branches, tags or releases were written by this assessment.

## Current evidence

- Repository: [thepianistdirector/grid-horizons](https://github.com/thepianistdirector/grid-horizons), public, default branch `main`. Authenticated GitHub CLI identity `thepianistdirector` (ID 78630787) has `ADMIN` repository permission. GitHub returned no releases and no tags at observation time. This permits preparing a concrete release route; it is not release authorization or proof that a local commit was pushed.
- Existing public Tanduna project ID: `prj_d7ab70af9e4710ae50d34c3c7317d1e9`; slug `grid-horizons`. Public tasks/roadmap inspection found no public tasks or published plan. Private maintainer drafts were not inspected.
- Existing public proposal ID: `prp_a4d6702934d41230599d6ed6f3c00c88`, revision 1, discussion state, “Initial research roadmap — eight waves for Grid Horizons”. Its body refers to 24 draft tasks and offers Yes/No. It does not describe the expanded 243-task, 28-wave candidate. Read current server-returned option keys before binding any plan; labels are not keys.
- The current client exposes no callable Tanduna tool. A scoped check of the standard Codex MCP configuration found no Tanduna entry; the documented `TANDUNA_ACCESS_TOKEN` environment variable was absent. No credentials were read, copied or expanded. Therefore maintainer role, private draft count, saved task IDs, draft revision, review-provider status and authenticated plan readback remain unverified.
- Exact public schemas are saved in `runs/research/publication-schemas.json` (local ignored research evidence). The complete official reference and guide snapshots are under `runs/research/publication-*`; `runs/research/publication-observations.json` records GitHub observations and source hashes.

## Supported native task-plan route

The [official full reference](https://tanduna.com/llms-full.txt) documents `https://tanduna.com/api/mcp`; authenticated `tools/list` is the authority for tools actually available to the connected client. Public documentation is not proof of connection.

| Step | Supported capability | Required input and semantics |
|---|---|---|
| Read project | `tanduna.projects.get` | `projectSlug`; includes saved story, channels and members. |
| Read drafts/tasks | `tanduna.tasks.list`, `tanduna.tasks.get` | List with `projectSlug`; get with `projectSlug`, returned `taskId`. Do not infer private task state from the public task list. |
| Read poll | `tanduna.proposals.list`, `tanduna.proposals.get` | `projectSlug`; get also needs returned `proposalId`. Use actual option keys and saved state. |
| Create task | `tanduna.tasks.create` | `projectSlug`, complete `fields` object below. Creates an unpublished maintainer draft. |
| Set planning requirements | `tanduna.tasks.set_requirements` | `projectSlug`, `taskId`, mandatory `expectedRevision`, `requirements` (complete object or null). Editable maintainer drafts only; a conflict requires a fresh read. |
| Read preparation | `tanduna.task_plans.get_draft` | `projectSlug`, `proposalId`; returns saved poll-bound preparation and revision, or null. |
| Save preparation | `tanduna.task_plans.save_draft` | `projectSlug`, `proposalId`, `expectedRevision`, `plan`. Use null revision only for create-if-absent; otherwise use the last read revision. Saves preparation only. |
| Submit exact candidate | `tanduna.task_plans.submit_draft` | `projectSlug`, `proposalId`, `expectedDraftRevision`. No unsaved payload accepted. Freezes the saved plan and queues textual review after explicit agreement to that exact candidate. |
| Open poll | `tanduna.proposals.open_vote` | `projectSlug`, `proposalId`; linked plans require actual passing textual review first. Freezes roster and weights irreversibly. |
| Cast ballot | `tanduna.proposals.vote` | `projectSlug`, `proposalId`, actual `optionKey`. Records/replaces the signed-in user's vote; a ballot is separate from a maintainer decision. Do not cast without concrete authorization. |
| Record decision / publish | Web workspace | Maintainer approves the exact reviewed linked option. The public MCP reference exposes no decision or direct-publication tool. Do not invent an endpoint. |
| Verify publication | `tanduna.task_plans.list_published` | `projectSlug`, optional `limit` (1–25, default 10), optional opaque `cursor`. Follow `nextCursor` with the same project/limit. Each result is a separate immutable plan with recorded review and approval evidence. |

A new discussion proposal can be prepared with `tanduna.proposals.create`: required `projectSlug`, `title` (1–300 characters), `body` (1–100000). Supply `pollOptions` explicitly: at least two `{key, label, explanation, risks}` objects, where key is a stable letters/digits/underscore/hyphen string of 1–64 characters, label 1–300, explanation 1–5000, and each risk 1–2000. Creating one is an external write requiring the concrete action to be authorized. This assessment creates none.

### Complete task fields

All of these fields are required, including nullable values and empty arrays where permitted:

```text
title: string[1..300]
goal: string[1..20000]
body: Markdown string[1..100000]
acceptanceCriteria: nonempty array of string[1..2000]
repositoryId: saved Tanduna repository identifier string[max500] | null
baseSha: saved base commit string[max200] | null
allowedPaths: array of nonempty string[max2000]
prohibitedPaths: array of nonempty string[max2000]
requiredCommands: array of nonempty string[max2000]
networkPolicy: "none" | "restricted" | "full"
secretScope: array of nonempty string[max2000]
maxExecutionPermissions: array of nonempty string[max2000]
expectedArtifactType: string[max500] | null
```

`repositoryId` is a saved Tanduna identifier, not an invented GitHub name. A project repository connection does not fill execution fields automatically. `tasks.update` replaces the complete fields object and creates a new revision; use `expectedRevision` to reject stale writes. A local roadmap JSON object is not automatically a valid `tasks.create` request.

Structured requirements are a separate complete object with required keys `schemaVersion` (1), `repository`, `models`, `deliverable`, `verification`, `acceptanceWorkflow`, and `requiredSkills`; their exact nested schema is in the saved JSON. Model descriptors use `{provider, model, effort}`; effort enum is `low`, `medium`, `high`, `xhigh`, `max`. Contributor instructions must retain Lucas's GPT-6 Astra rule. Host-supplied model observations are not caller fields or proof of actual execution. Do not place a forbidden fallback model into requirements.

### Exact plan shape and limits

```json
{
  "projectSlug": "grid-horizons",
  "proposalId": "<returned proposal ID for the agreed candidate>",
  "expectedRevision": null,
  "plan": {
    "optionKey": "<returned saved option key, or null while preparing>",
    "waves": [
      {"name": "<wave name>", "taskIds": ["<returned task ID>"]}
    ],
    "unassignedTaskIds": [],
    "dependencies": [
      {"taskId": "<returned task ID>", "dependsOnTaskIds": ["<returned prerequisite ID>"]}
    ]
  }
}
```

This is an explanatory template, not a runnable payload. Null expected revision is correct only after a read returned no draft. On updates include each existing server-issued wave `id` exactly as returned. Wave IDs and ordering belong to this poll; do not make a global wave registry.

The public input schema allows at most 32 waves, names of 1–80 characters, at most 1000 unique task IDs per wave, at most 1000 unique unassigned task IDs, at most 1000 dependency records, and at most 1000 unique prerequisite IDs per dependency record. Task/wave IDs in this plan are 1–160 characters. All declared objects reject additional properties. A saved option is required before submission.

The candidate's 28 waves and 243 tasks fit those advertised cardinality limits, provided its dependency records and names fit too. The docs do not state a separate aggregate task count limit, a bulk task-creation operation, a guaranteed review time, or whether all 243 candidate tasks satisfy server eligibility. Do not infer those guarantees from the per-array limits. Validate the complete candidate locally, create/read each native draft using returned IDs, then validate the server-saved plan. Do not upload local task IDs as if they were server IDs.

## Review, vote and immutable history gates

The [start-a-project guide](https://tanduna.com/guide/start-a-project) describes ordered named waves, dependencies and the saved-revision submission workflow. The review queue is configured to run about every five minutes; long reviews may delay a sweep. A disabled reviewer leaves a submission pending. Read actual status; elapsed time is not a passing review. Technical failures can use “Retry queued review” in the task workspace. Requested textual changes require new draft task versions and a new poll; the frozen record remains history.

The [review checklist](https://tanduna.com/guide/task-review-checklist) requires observable acceptance, reproducible QA or a concrete manual procedure, bounded paths/prerequisites, repository/base, model requirements and authorized instructions. Its application reviewer requests Astra Low at normal speed. That request does not attest contributor execution, and a passing text review does not mean the code was run, accepted or safe for real-grid operation.

The [voting guide](https://tanduna.com/guide/how-voting-works) separates ballots from the maintainer's recorded decision. Opening voting freezes eligible membership and weights and cannot be undone. A member has one replaceable ballot while voting remains open. Only approval of the exact reviewed linked option publishes its task plan. A majority tally, a recommendation, a different approved option, a draft save, or a passing review alone does not publish it. A rejected submission stays unpublished.

Preserve the existing eight-wave proposal and any submitted or published plans. Read private state before deciding whether existing task drafts are editable. Since the expanded candidate describes materially different scope, a fresh clearly labeled proposal and draft task set is the reviewable default, subject to the owner's concrete decision. Do not relabel the historical proposal as approving 28 waves. Published plans stay separate in readback; historical tasks do not become completed merely because replacement tasks exist. Only after replacement publication may an unclaimed legacy task be marked superseded through the web workspace, preserving the old brief and replacement link. No bulk delete or destructive history operation is part of this path.

## Authentication and remaining concrete actions

[Connect through MCP](https://tanduna.com/guide/connect-through-mcp) documents a local login helper, downloaded here for inspection only. It normally runs on the same computer as the user's browser and launches a new client with a short-lived token after email/password entry in the terminal or GitHub consent. The helper can add a compatible Codex MCP entry; running it is therefore beyond this read-only check. Direct Codex MCP OAuth is not a supported substitute. No owner should paste credentials into chat, and no second account, shared config rewrite or alternate provider should be used to bypass the missing connection.

1. Finish the local release candidate, complete its evidence and task export, and present the exact candidate and proposed public action to Lucas. Verify current authorization before requesting any additional decision; this report does not itself authorize platform writes.
2. Establish/obtain the documented authenticated Tanduna capability through the owner's existing session, without altering accounts or consent. Verify actual `tools/list`, then read `projects.get`, proposals, tasks, draft revisions and separate published plans. Confirm maintainer rights and reconcile any private 24-task drafts before creating anything.
3. Agree the concrete expanded proposal, option, task bodies, wave order and dependencies. Convert local IDs through a recorded local-to-server mapping; preserve the old proposal and frozen records. Save native draft tasks and structured requirements using verified repository/base values, then save the poll-bound plan and read it back. Stop on conflicts and compare saved state before retrying.
4. Present the exact saved candidate revision for explicit submission agreement when not already authorized. Submit that revision, observe actual textual review, and address findings through the supported workflow. Do not fabricate review, approve a poll, or cast the user's ballot to clear a gate.
5. With the owner's concrete governance decision, open voting and use the web maintainer decision flow to approve the exact reviewed option. Record receipt, option, draft/submission/review revisions and publication time. Verify `list_published`, public roadmap/tasks and saved task briefs against the candidate.
6. Independently prepare the GitHub release from the tested immutable candidate commit: exact version/tag, release notes and checksummed distributable assets. Existing GitHub authentication and public repository visibility are available, but no version/tag/assets or release action is authorized by this assessment. After the applicable owner release approval, push/tag/create the release using authorized GitHub tooling, read back the release and assets, and record actual URLs. GitHub remains authoritative for code and releases; Tanduna's MCP does not write GitHub.

The available local preparation can proceed while native authentication or owner governance is pending. Report those unverified gates separately from the implemented software and never label a local export “published”.
