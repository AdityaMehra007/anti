/**
 * Windmill Production Script: Interactive Slack Approval Notifier
 * ===============================================================
 * Category: Human-in-the-Loop & Incident Response
 * Language: TypeScript / Deno (Windmill Native TS Runner)
 * 
 * Formats interactive Slack Block Kit payloads for human approvals in multi-step DAG flows.
 */

interface ApprovalRequest {
  workflow_id: string;
  step_name: string;
  requester: string;
  summary: string;
  amount_inr?: number;
  callback_url: string;
}

interface SlackBlock {
  type: string;
  text?: { type: string; text: string; emoji?: boolean };
  fields?: Array<{ type: string; text: string }>;
  accessory?: any;
  elements?: any[];
}

export async function main(
  req: ApprovalRequest = {
    workflow_id: "DAG-ONBOARD-2026-004",
    step_name: "Executive Treasury Sign-Off",
    requester: "Autonomous Agent Fleet Alpha",
    summary: "Authorization required for vendor invoice settlement exceeding ₹5,00,000 threshold.",
    amount_inr: 720000.0,
    callback_url: "http://localhost:8002/api/flows/resume?job=DAG-ONBOARD-2026-004"
  }
) {
  const blocks: SlackBlock[] = [
    {
      type: "header",
      text: {
        type: "plain_text",
        text: `🚨 Approval Required: ${req.step_name}`,
        emoji: true,
      },
    },
    {
      type: "section",
      fields: [
        { type: "mrkdwn", text: `*Workflow ID:*\n\`${req.workflow_id}\`` },
        { type: "mrkdwn", text: `*Requester:*\n${req.requester}` },
        { type: "mrkdwn", text: `*Amount:*\n₹${req.amount_inr?.toLocaleString("en-IN") ?? "N/A"}` },
        { type: "mrkdwn", text: `*Status:*\n⏸️ *SUSPENDED (Awaiting Action)*` },
      ],
    },
    {
      type: "section",
      text: {
        type: "mrkdwn",
        text: `*Description:*\n${req.summary}`,
      },
    },
    {
      type: "actions",
      elements: [
        {
          type: "button",
          text: { type: "plain_text", text: "✅ Approve & Resume", emoji: true },
          style: "primary",
          value: `approve_${req.workflow_id}`,
          url: `${req.callback_url}&action=approve`,
        },
        {
          type: "button",
          text: { type: "plain_text", text: "❌ Reject & Terminate", emoji: true },
          style: "danger",
          value: `reject_${req.workflow_id}`,
          url: `${req.callback_url}&action=reject`,
        },
      ],
    },
  ];

  return {
    success: true,
    workflow_id: req.workflow_id,
    slack_blocks: blocks,
    rendered_payload: JSON.stringify({ blocks }),
    dispatched_at: new Date().toISOString(),
  };
}
