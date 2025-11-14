8825 — Low‑Friction Onboarding Brainstorm (Mined Doc)
Date: November 9, 2025 12:00 (America/Chicago)
Author: 8825 Assistant (mined from chat with Justin Harmon)

— SUMMARY —
Goal: Let non‑technical users get a first automation win in under 5 minutes, then safely “graduate” to deeper power via progressive permissions and optional concierge setup.

— CONTEXT —
• Mode: 8825 mode → brainstorm_mode
• Topic: Low‑friction onboarding for users who are not tech‑savvy; minimize API key handling; support OAuth and white‑glove options.
• Constraint: Many users won’t have “Windsurf crew” to wire connections; we need alternatives that still feel powerful and safe.
• North Star: Reduce thought/typing; avoid credential friction; prove value immediately.

— SCOPE —
Applies to individual users and small teams; extensible to org/IT setups through Concierge Lane & Admin Pack.

— THREE ONBOARDING LANES —
1) Zero‑Keys Lane (no IT required)
   • Magic inbound email per workspace: inbox@{workspace}.8825.ai → forward/attach; we OCR/route.
   • Watched folder via OAuth (Dropbox/Drive): drop files → auto‑process.
   • ICS‑only calendar: read‑only subscription for “quick wins” without write scopes.
   • Optional Slack DM: invite the 8825 bot; “/route bill” to process.

2) One‑Click OAuth Lane (Connections Hub)
   • Large provider buttons: Google / Microsoft / Dropbox / Notion / Slack.
   • Start READ‑ONLY; escalate per capability toggle (“Allow create calendar events”). 
   • Consent Receipt (plain‑English): downloadable PDF summarizing scopes & purposes.

3) Concierge Lane (White‑Glove)
   • 30‑min co‑browse checklist (no remote control required).
   • We run the Setup Script, verify flows, and deliver:
     – Keys & Scopes Map
     – Consent Receipt
     – 2‑week Health Check
   • Org Admin Pack: SSO/SAML notes, pre‑approved scopes, minimal IT checklist.

— FIRST‑WIN PATH (consistent across lanes) —
1) Pick a starter: “Bills → OCR → Calendar + Drive” (or “Inbox → Smart Filing”).
2) Connect one source (email OR folder OR Google account).
3) Run a test with a baked‑in sample bill/email.
4) Observe the result (draft calendar event, Drive PDF saved, Slack summary DM).
5) Turn it on (toggle: read‑only → assisted write → full auto; always support UNDO).

— CORE COMPONENTS (“BUILDING BLOCKS”) —
• Magic Link Sessions (PKCE): passwordless, device‑aware, resumable checklists.
• Scope Bundles: “Safe Read‑Only” / “Write Essentials” / “Advanced Admin” (clearly labeled).
• Health Monitor: connection tiles show last success + 1‑click re‑auth (“Fix it”).
• Consent Receipts & Audit Log: human‑readable action log, downloadable.
• Recovery Paths: device‑code flow for locked‑down envs; QR handoff laptop ↔ phone.

— NO‑API‑KEY ALTERNATIVES (so beginners never touch secrets) —
• Email‑only automation: plus‑address rules (e.g., payables+acme@…).
• Folder rules: drop into “Bills_2025/11” → auto‑parse, file, and propose calendar holds.
• Upload form page: drag‑and‑drop → receipt + next steps; no dashboard required.

— “PRO POWER” (opt‑in, without scaring beginners) —
• Vault choice: 8825 encrypted vault OR user‑owned encrypted bundle in Dropbox/Drive.
• Service Accounts / Domain Delegation for orgs (admin‑approved scopes, auto‑rotation).
• Read‑only bank data via aggregator (strictly opt‑in, separated connector).

— UX PRINCIPLES —
• Show value first; explain in plain English.
• Start read‑only; escalate on explicit toggle; always offer undo.
• Keep the checklist under 5 steps; seed with sample data for a guaranteed demo.
• Reflect trust: consent receipts, readable logs, visible status/health.

— COPY‑READY PLAYBOOK (embed as JSON when needed) —
onboarding_v01 = {
  "lanes": [
    {
      "id": "zero_keys",
      "pitch": "No IT needed. Start with email or a watched folder.",
      "steps": ["claim_magic_email", "connect_folder_oauth", "run_sample_test", "view_result", "toggle_autopilot"]
    },
    {
      "id": "oauth_hub",
      "pitch": "One-click connections with progressive permissions.",
      "steps": ["open_connections_hub", "connect_google_or_ms", "grant_readonly_scopes", "run_starter_flow", "offer_write_upgrade"]
    },
    {
      "id": "concierge",
      "pitch": "White-glove setup for non-technical teams.",
      "steps": ["schedule_call", "co_browse_checklist", "verify_flows", "deliver_consent_receipt", "2wk_health_check"]
    }
  ],
  "starters": [
    {
      "id": "bills_ocr_calendar",
      "name": "Bills → OCR → Calendar + Drive",
      "inputs": ["email", "watched_folder"],
      "outputs": ["calendar_event_draft", "drive_pdf", "slack_dm_summary"],
      "default_scopes": ["read:email", "read:drive"],
      "upgrade_scopes": ["write:calendar", "write:drive"]
    },
    {
      "id": "inbox_smart_filing",
      "name": "Inbox → Smart Filing",
      "inputs": ["email"],
      "outputs": ["drive_folder_structure", "daily_digest"],
      "default_scopes": ["read:email", "write:drive"]
    }
  ],
  "ux_rules": {
    "show_value_first": true,
    "start_readonly": true,
    "escalate_on_toggle": true,
    "explain_in_plain_english": true,
    "always_offer_undo": true
  }
}

— IMPLEMENTATION ROADMAP (MVP → next) —
MVP (ship first):
1) Connections Hub (Google + Dropbox + Slack; read‑only scopes first)
2) Starter Flow: “Bills → OCR → Calendar + Drive” with baked‑in sample
3) Consent Receipt generator (simple PDF)
4) Health Monitor (green/amber/red + 1‑click re‑auth)
5) Concierge Script (10‑step runbook)

V2 (expansion):
• Microsoft 365 Graph connectors; Notion; device‑code flow
• Admin Pack & SSO/SAML playbook
• User‑owned encrypted token bundle (Dropbox/Drive) + rotation policy
• Bank data connector (read‑only), isolated and optional

— OPEN QUESTIONS —
1) Should “Magic email” be workspace‑scoped or project‑scoped (risk: spam)?
2) Data residency options needed at onboarding?
3) What’s the default retention for logs and receipts (30/90/365 days)?
4) Where do we surface “UNDO” for auto actions (DM, email, or hub UI)?

— RISKS & MITIGATIONS —
• Risk: Users fear over‑permission.
  – Mitigation: Start read‑only; human‑readable consent receipts; granular toggles.
• Risk: OAuth decay/broken tokens.
  – Mitigation: Health Monitor + proactive re‑auth prompts; fallback email/folder.
• Risk: Demo fails due to weird sample.
  – Mitigation: Provide our own guaranteed‑pass sample + “replay last run.”
• Risk: Support burden for non‑tech users.
  – Mitigation: Concierge Lane, templated scripts, 2‑week check, self‑serve fixes.

— METRICS OF SUCCESS —
• Time‑to‑first‑value (TTFV): target < 5 minutes
• Task completion rate for Starter Flow: ≥ 85%
• Scope upgrade acceptance (read‑only → write): ≥ 40% by Day 7
• Re‑auth success within 24h: ≥ 90%
• NPS after first win: ≥ +40

— DECISIONS (from brainstorm) —
• Adopt progressive permissions with explicit capability toggles.
• Always provide a sample for a guaranteed demo run.
• Standardize Consent Receipt + Audit Log for every connection.
• Provide three lanes (Zero‑Keys, OAuth Hub, Concierge) to match user comfort.

— NEXT ACTIONS —
1) Spec Connections Hub MVP UI (copy + states + error fixes).
2) Build the Bills→OCR Starter Flow with replayable sample.
3) Implement PDF Consent Receipt generator.
4) Instrument Health Monitor tiles + re‑auth CTA.
5) Draft Concierge 10‑step runbook and Admin Pack outline.

— GLOSSARY —
• Progressive permissions: Start minimal; request additional scopes only when a feature needs them.
• PKCE: OAuth extension enabling secure, passwordless magic‑link sessions.
• Device‑code flow: Login path that doesn’t require a browser on the device.

(End of mined brainstorm)
