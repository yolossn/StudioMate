# Operating flow and demo script

## 1. Intake
A customer fills in the Google Form. The new Sheet row triggers a Zapier zap, which posts the
order into the Mattermost **New Orders** channel through an incoming webhook. Form
text is treated as untrusted story input.

## 2. Kick-off (human)
A studio human replies in the order thread:
`@studiomate-studio_manager please take this order`

## 3. Room and order card (Studio Manager)
The Studio Manager:
- creates the private room `customer-YYYY-MM-DD`;
- adds the human and the four specialists;
- posts an Order Card with order ID `SO-ROW<n>`. Missing fields are marked "missing" and payment status is copied as stated.

## 4. Hand-off sequence (one at a time)
| Step | Studio Manager asks | Specialist returns (tagging the Studio Manager) |
|---|---|---|
| 1 | Accounts Desk | Payment status + what a human must verify |
| 2 | Project Manager | Milestone plan to the delivery date, risks |
| 3 | Creative Director | Artist brief + open questions |
| 4 | Customer Liaison | Customer acknowledgement, **DRAFT – not sent** |
| 5 | (Studio Manager) | Status summary: stage, next owner, deadline, blockers |

## 5. Human decisions
A human verifies payment in the real account, names the lyricist, musician and singer, and
approves or edits the draft before sending it themselves. They then tag the Studio Manager
again, and it posts an updated summary.

## Demo script (~3 min)
1. Show the Form submission arriving in New Orders.
2. Tag the Studio Manager and show the new room and order card.
3. Watch the four hand-offs, each from a different bot identity.
4. End on the status summary. Point out the human gates: UNVERIFIED payment,
   UNASSIGNED artists and the unsent draft.
5. Optional: post the synthetic "no money paid" screenshot and tag the Accounts
   Desk. It must refuse to call the order paid.

## Guardrails in the prompts
- Agents never invent people, payments, approvals or listening.
- Only the Studio Manager coordinates. Specialists reply once and tag only the Studio Manager.
- Agents never contact customers.
