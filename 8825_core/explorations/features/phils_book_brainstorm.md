Phil's Book — Brainstorm Mining Report
Date: 2025-11-09T21:38:20
Owner: Justin Harmon (Jh)
Mode: 8825 — Brainstorm

Summary:
- Single-file, privacy-first expense notebook named 'Phil's Book'.
- Working HTML prototype (v0.2) with Bills, Reconcile, Settings.
- Bank connectivity CSV-only for now; live linking later (Plaid/Finicity).
- Gmail/Calendar/Drive ingestion with CSV contract.
- Reconcile heuristics (±$0.01, ±7d, token-overlap), vendor normalization, rule builder.
- Near-term plan: vendor table, manual reconcile picker, month close, Gmail script template, budgets.

Artifacts:
- HTML: sandbox:/mnt/data/phils_book_v0_2.html
- Brainstorm TXT: sandbox:/mnt/data/phils_book_brainstorm_v01.txt

Full JSON mining_report below.

{
  "mining_report": {
    "meta": {
      "chat_id": "phils_book_brainstorm_session_2025-11-09",
      "mined_at": "2025-11-09T21:38:20",
      "subjects": [
        "Phil's Book single-file notebook",
        "Bills ingestion via Gmail/Calendar/Drive",
        "Bank CSV import and reconciliation",
        "Vendor normalization and rule builder",
        "UX and monthly workflows",
        "Feasibility of direct bank linking"
      ],
      "primary_project": "8825_finance_tools_phils_book.json",
      "owner": "Justin Harmon (Jh)"
    },
    "routing": {
      "primary": "8825_finance_tools.json",
      "confidence": 0.94,
      "reasoning": "All content pertains to a financial tracking notebook and ingestion automations under 8825."
    },
    "artifacts": [
      {
        "name": "Phil's Book v0.2 (single-file HTML)",
        "path": "sandbox:/mnt/data/phils_book_v0_2.html",
        "type": "html"
      },
      {
        "name": "Phil's Book \u2014 Brainstorm v0.1 (compact)",
        "path": "sandbox:/mnt/data/phils_book_brainstorm_v01.txt",
        "type": "txt"
      }
    ],
    "decisions": [
      {
        "what": "Rename Red Notebook to 'Phil's Book'",
        "why": "User preference; consistent branding."
      },
      {
        "what": "Keep local-only storage by default",
        "why": "Privacy; simplicity; offline capability."
      },
      {
        "what": "Bank linking deferred to CSV import",
        "why": "Feasibility and security; avoid aggregator until needed."
      }
    ],
    "data_model": {
      "record": [
        "id",
        "date",
        "vendor",
        "amount",
        "currency",
        "category",
        "subcategory",
        "note",
        "paid",
        "paid_date",
        "due_date",
        "account",
        "tags[]",
        "drive_url",
        "calendar_url",
        "source_doc_id",
        "ocr_text_hash",
        "month_key",
        "created_at",
        "updated_at",
        "bank_txn_id"
      ],
      "csv_headers": [
        "Date",
        "Vendor",
        "Amount",
        "Category",
        "Note",
        "DriveURL",
        "CalendarURL",
        "Paid",
        "DueDate",
        "PaidDate",
        "Account",
        "Tags",
        "Source",
        "BankTxnId"
      ]
    },
    "ingestion_pipeline": [
      {
        "step": "receive_new_scan",
        "via": "Drive upload or Gmail \u2192 Apps Script \u2192 Drive"
      },
      {
        "step": "run_ocr",
        "detect": "total_amount, due_date, vendor, account_ref"
      },
      {
        "step": "normalize_fields",
        "rules": "vendor canonicalization, currency parsing, category via keyword rules"
      },
      {
        "step": "deduplicate",
        "keys": "ocr_text_hash or (vendor+amount+date\u00b17d) or Drive file id"
      },
      {
        "step": "calendar_sync",
        "template": "BILL \u2022 {vendor} \u2014 {amount}; due_date preferred; reminders 3d/1d/same-day"
      },
      {
        "step": "export_csv_snapshot",
        "to": "Drive /PhilBook/exports/phils_book_YYYY-MM.csv"
      },
      {
        "step": "notify_optional",
        "channel": "email or mobile push with month summary"
      }
    ],
    "ui_ux_spec": {
      "layout": "Left sidebar months index with totals; main pane per-month bills table",
      "controls": [
        "search",
        "filters: category/paid/min/max",
        "copy month summary",
        "add new row"
      ],
      "table_columns": [
        "Date",
        "Vendor",
        "Category",
        "Amount",
        "Note",
        "Status",
        "Links",
        "Source",
        "Actions"
      ],
      "stats": [
        "Total",
        "Paid",
        "Unpaid",
        "Avg",
        "By-category rollups"
      ],
      "reconcile_tab": "Suggest matches and confirm; partial payments planned",
      "settings_tab": [
        "Inboxes (email labels)",
        "Bank accounts labels",
        "How-to connect notes"
      ],
      "style": "Red notebook aesthetic; keyboard month nav planned"
    },
    "reconciliation": {
      "heuristics": {
        "amount_tolerance": 0.01,
        "date_window_days": 7,
        "vendor_match": "token overlap",
        "scoring": "60 date closeness + 40 vendor overlap"
      },
      "actions": [
        "Confirm match \u2192 paid=true, paid_date=txn.date, bank_txn_id set",
        "Mark paid manually",
        "Ignore candidate placeholder"
      ],
      "future": [
        "manual picker search",
        "partial/installment support",
        "pull bank memo into Note"
      ]
    },
    "intelligence_rules": {
      "vendor_normalization": "Editable table, e.g., 'TXU' \u2192 'TXU Energy'",
      "rule_builder_examples": [
        "If vendor includes 'Spectrum' \u2192 Category=Internet; Paid=false; DueDate=+30d"
      ],
      "duplicate_guard": "Vendor+Amount\u00b1$0.01 within 7 days OR same Drive id OR OCR hash"
    },
    "reporting_budget": {
      "targets": "Monthly caps per category (chips change color when over)",
      "trend": "12-month trends total and by category",
      "tax": "Schedule C mapping + export tax_year_YYYY.csv",
      "cadence": "Detect missing usual bills for this month"
    },
    "security_privacy": [
      "LocalStorage persistence; no third-party calls in HTML app",
      "Optional PWA for offline caching",
      "Exports versioned CSV snapshots to Drive when desired"
    ],
    "integrations_feasibility": {
      "email": "Gmail labels + Apps Script export: feasible now",
      "calendar_drive": "Already in use; include URLs/ids in CSV",
      "banks": "CSV import now; live links later via Plaid/Finicity if server-side OAuth acceptable"
    },
    "edge_cases": [
      "refunds/credits (negative amounts)",
      "annual bills",
      "multi-profile households (Phil/Household/Business)"
    ],
    "build_next": [
      "Vendor table + Rule builder (light UI)",
      "Reconcile manual picker + partial payments",
      "Month close checklist (export snapshot; copy summary; mark rest unpaid)",
      "Gmail label export Apps Script template",
      "Budget caps + over/under chips"
    ],
    "open_questions": [
      "Use due_date vs invoice date as the primary table date? (lean due_date)",
      "Confirm paid via bank feed, calendar edit, or manual toggle priority?",
      "Need multi-currency or tax categories at MVP? (likely no)"
    ]
  }
}