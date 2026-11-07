# Switch deployment (back-office version)

## Local stack (as verified)
- Switch Console (macOS), with a native Switch gateway on localhost.
- Local Mattermost in Docker (`switchdash-local-mattermost-mattermost-1`), team `switch`.
- Five agents running OpenCode with `github-copilot/claude-haiku-4.5`. Auto mode is on,
  bypass is off and agent management is off.
- Intake: Google Form → Google Sheet → Zapier ("New row") → POST to the Mattermost
  incoming webhook of channel **New Orders**, exposed through an ngrok tunnel.

## Creating the agents
In Switch Console, create one OpenCode agent per folder in `agents/runtime/`:
`studiomate-studio_manager`, `studiomate-accounts_desk`, `studiomate-project_manager`,
`studiomate-creative_director`, `studiomate-customer_liaison`.
Paste each folder's `AGENTS.md` into the agent's **Instructions** setting and save it
(Cmd+S in the expanded editor). Only the Studio Manager needs permission to create
rooms and add members. Add the Studio Manager to **New Orders**.

## Verifying
1. Submit the Form, or add a Sheet row, and confirm that the post appears in New Orders.
2. Tag `@studiomate-studio_manager` in the thread and confirm that a room and an order card appear.
3. Confirm that the four specialists each reply once, tagging the Studio Manager, followed by
   one status summary.
4. Inspect posts:
   `docker exec switchdash-local-mattermost-mattermost-1 mmctl --local post list switch:<room> --number 30`

Use a fresh trial ID when reusing a room. Require a published ledger, milestone
plan, artist brief and unsent draft for that ID, not old outputs or runtime
notifications. A complete message chain proves transport, not content accuracy:
check factual consistency, human ownership of decisions, payment gates and any
non-English draft separately before treating the trial as passed.

## Troubleshooting
- Switch does not publish final assistant text. Specialists must execute
  `switch_send_targeted_message` to hand their deliverable back to Studio Manager;
  Studio Manager uses the same tool for requests and `switch_post_message` for
  its final summary. These are tool calls, not text to paste into a message.
  A "Worked" notification alone is not evidence that the deliverable was posted.
- If a specialist asks a question instead of delivering, its instructions are probably not saved.
  Re-check that its saved instructions include "Reply once, and start that reply with
  `@studiomate-studio_manager`" and "never ask Studio Manager for information before replying".
- If the flow stalls, inspect the runtime turn: distinguish an unpublished final
  answer, a failed tool call and a missing targeted recipient. Verify the saved
  publishing rule before retrying; a manual re-tag is recovery, not proof of an
  automatic sequence.
- If Zapier posts stop, check that the ngrok tunnel is up and that the zap uses the current URL.

## Safety
Do not commit tokens or webhook URLs. Payment, artist assignment and customer
contact always remain human actions.
