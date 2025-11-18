# OCR Routing Rules Specification

**Version:** 1.0.0  
**Date:** November 17, 2025  
**Status:** Production

---

## Purpose

Defines the JSON schema for user-specific OCR routing rules. These rules determine how OCR results are transformed and routed to destination systems (Calendar, Sheets, FigJam, 8825 ingest, etc.).

---

## Rules File Structure

```json
{
  "user_id": "jh",
  "version": "1.0.0",
  "confidence_threshold": 0.7,
  "dry_run_log_path": "~/.8825/ocr_routing_log.jsonl",
  
  "routes": [ /* array of route objects */ ],
  
  "fallback": { /* fallback route */ },
  
  "low_confidence_action": { /* manual review config */ }
}
```

---

## Route Object Schema

```json
{
  "id": "unique_route_id",
  "match": {
    "doc_type": "bill" | "receipt" | "note" | "sticky_note" | "document",
    "keywords": ["optional", "keyword", "list"]
  },
  "target": "calendar" | "sheets" | "figjam" | "8825" | "archive",
  "transforms": [
    {
      "type": "transform_function_name",
      "param1": "value1",
      "param2": "value2"
    }
  ],
  "actions": [
    {
      "type": "action_function_name",
      "param1": "value1"
    }
  ],
  "confidence_boost": 0.0
}
```

---

## Match Criteria

### `doc_type` (string, optional)
Match documents of specific type:
- `bill` - Bills and invoices
- `receipt` - Purchase receipts
- `note` - General notes
- `sticky_note` - Short sticky notes
- `document` - Formal documents
- `unknown` - Unclassified documents

### `keywords` (array, optional)
Additional keywords to match in text. If any keyword found, route matches.

**Example:**
```json
{
  "match": {
    "doc_type": "note",
    "keywords": ["basketball", "PHJH", "game"]
  }
}
```

---

## Transform Actions

Transforms extract structured data from OCR results **before** routing.

### Available Transforms

#### `extract_bill_fields`
**Purpose:** Extract due date, amount, vendor from bills

**Parameters:**
```json
{
  "type": "extract_bill_fields",
  "patterns": ["due date:", "payment due:", "pay by:"]
}
```

**Output:**
```json
{
  "due_date": "12/01/2025",
  "amount": "125.00",
  "vendor": "AT&T"
}
```

#### `extract_receipt_amounts`
**Purpose:** Extract store, date, amounts from receipts

**Parameters:**
```json
{
  "type": "extract_receipt_amounts",
  "exclude_tax_and_tip": false,
  "include_total": true
}
```

**Output:**
```json
{
  "store_name": "Walmart",
  "purchase_date": "11/17/2025",
  "amounts": ["10.99", "5.50", "16.49"],
  "total": "16.49"
}
```

#### `combine_page_text`
**Purpose:** Combine multi-page text into single string

**Parameters:**
```json
{
  "type": "combine_page_text",
  "join_with": "\n\n"
}
```

**Output:**
```json
{
  "full_text": "Page 1 text\n\nPage 2 text",
  "page_count": 2
}
```

#### `group_text_by_color`
**Purpose:** Group sticky notes by color (future: requires color detection)

**Parameters:**
```json
{
  "type": "group_text_by_color",
  "group_strategy": "color_clusters",
  "max_notes_per_group": 50
}
```

**Output:**
```json
{
  "groups": [
    {
      "color": "yellow",
      "text": "Note text",
      "notes_count": 1
    }
  ]
}
```

#### `extract_basketball_schedule`
**Purpose:** Extract game dates and locations

**Parameters:**
```json
{
  "type": "extract_basketball_schedule",
  "team": "7th grade B team",
  "location_mappings": {
    "@ PHJH": "Parkhill Junior High",
    "@ FMMS": "Forrest Meadows Middle School"
  }
}
```

**Output:**
```json
{
  "games": [
    {
      "date": "11/17",
      "location": "Parkhill Junior High",
      "location_code": "PHJH"
    }
  ],
  "game_count": 1
}
```

---

## Route Actions

Actions execute after transforms, sending data to destination systems.

### Available Actions

#### `create_calendar_event`
**Purpose:** Create calendar event

**Parameters:**
```json
{
  "type": "create_calendar_event",
  "calendar_name": "Bills",
  "event_title_template": "Pay: {vendor}",
  "reminder_days_before": 3
}
```

**Output:** JSON file in `~/Downloads/8825_inbox/pending/calendar_event_*.json`

#### `add_sheet_row`
**Purpose:** Add row to Google Sheet

**Parameters:**
```json
{
  "type": "add_sheet_row",
  "sheet_name": "Expenses 2025",
  "columns": ["Date", "Vendor", "Amount", "Category"]
}
```

**Output:** JSON file in `~/Downloads/8825_inbox/pending/expense_row_*.json`

#### `upload_to_figjam`
**Purpose:** Upload to FigJam board

**Parameters:**
```json
{
  "type": "upload_to_figjam",
  "board_name": "JH Brain Dump",
  "position": "auto"
}
```

**Output:** JSON file in `~/Downloads/8825_inbox/pending/figjam_staging/*.json`

#### `save_to_8825_inbox`
**Purpose:** Save to 8825 brain inbox

**Parameters:**
```json
{
  "type": "save_to_8825_inbox",
  "category": "notes",
  "format": "markdown"
}
```

**Output:** JSON file in `~/Downloads/8825_inbox/pending/ocr_*.json`

#### `log_to_8825`
**Purpose:** Log routing decision

**Parameters:**
```json
{
  "type": "log_to_8825",
  "category": "bills"
}
```

**Output:** Entry in `~/.8825/ocr_routing_log.jsonl`

---

## Confidence Boost

Routes can boost confidence for better matching:

```json
{
  "confidence_boost": 0.2
}
```

**Effect:** Adds 0.2 to OCR confidence when this route matches.

**Use Cases:**
- High-value routes (basketball schedule: +0.2)
- Specific document types (bills: +0.1)
- Generic fallbacks (notes: +0.0)

---

## Fallback Route

Handles documents that don't match any route:

```json
{
  "fallback": {
    "target": "archive",
    "action": "move_to_archive",
    "archive_path": "~/Downloads/8825_inbox/archive/ocr_unknown/"
  }
}
```

---

## Low Confidence Action

Handles documents below confidence threshold:

```json
{
  "low_confidence_action": {
    "target": "manual_review",
    "log_path": "~/.8825/ocr_manual_review.jsonl"
  }
}
```

**Threshold:** Defined in `confidence_threshold` (default: 0.7)

---

## Complete Example

```json
{
  "user_id": "jh",
  "version": "1.0.0",
  "confidence_threshold": 0.7,
  "dry_run_log_path": "~/.8825/ocr_routing_log.jsonl",
  
  "routes": [
    {
      "id": "bill_to_calendar",
      "match": {
        "doc_type": "bill"
      },
      "target": "calendar",
      "transforms": [
        {
          "type": "extract_bill_fields",
          "patterns": ["due date:", "payment due:"]
        }
      ],
      "actions": [
        {
          "type": "create_calendar_event",
          "calendar_name": "Bills",
          "event_title_template": "Pay: {vendor}",
          "reminder_days_before": 3
        },
        {
          "type": "log_to_8825",
          "category": "bills"
        }
      ],
      "confidence_boost": 0.1
    },
    {
      "id": "receipt_to_sheets",
      "match": {
        "doc_type": "receipt"
      },
      "target": "sheets",
      "transforms": [
        {
          "type": "extract_receipt_amounts",
          "include_total": true
        }
      ],
      "actions": [
        {
          "type": "add_sheet_row",
          "sheet_name": "Expenses 2025",
          "columns": ["Date", "Vendor", "Amount"]
        }
      ],
      "confidence_boost": 0.05
    }
  ],
  
  "fallback": {
    "target": "archive",
    "action": "move_to_archive",
    "archive_path": "~/Downloads/8825_inbox/archive/ocr_unknown/"
  },
  
  "low_confidence_action": {
    "target": "manual_review",
    "log_path": "~/.8825/ocr_manual_review.jsonl"
  }
}
```

---

## Route Precedence

Routes evaluated in order:

1. **First match wins** - Routes checked top to bottom
2. **Keyword boost** - If keywords match, confidence boosted
3. **Confidence check** - If total confidence < threshold → manual review
4. **Fallback** - If no routes match → fallback route

---

## Execution Modes

### Dry Run (Default)
- No side effects
- All decisions logged
- Safe for testing

**Usage:**
```json
{
  "mode": "dry_run"
}
```

### Execute
- Creates output files
- Performs actions
- Production mode

**Usage:**
```json
{
  "mode": "execute"
}
```

---

## Output Locations

### Calendar Events
`~/Downloads/8825_inbox/pending/calendar_event_*.json`

### Expense Rows
`~/Downloads/8825_inbox/pending/expense_row_*.json`

### FigJam Staging
`~/Downloads/8825_inbox/pending/figjam_staging/sticky_*.json`

### 8825 Brain
`~/Downloads/8825_inbox/pending/ocr_*.json`

### Archive
`~/Downloads/8825_inbox/archive/ocr_unknown/ocr_archive_*.json`

---

## Logging

### Routing Log
**Path:** `~/.8825/ocr_routing_log.jsonl`

**Format:**
```json
{
  "timestamp": "2025-11-17T20:00:00Z",
  "doc_type": "bill",
  "confidence": 0.85,
  "matched_rule": "bill_to_calendar",
  "target": "calendar",
  "mode": "execute"
}
```

### Manual Review Log
**Path:** `~/.8825/ocr_manual_review.jsonl`

**Format:**
```json
{
  "timestamp": "2025-11-17T20:00:00Z",
  "doc_type": "unknown",
  "confidence": 0.45,
  "reason": "Below confidence threshold (0.7)",
  "text_preview": "First 100 chars..."
}
```

---

## Adding Custom Transforms

1. **Create transform function** in `transforms.py`:
```python
def my_custom_transform(ocr_result: Dict, params: Dict) -> Dict:
    # Extract data
    return {"extracted_data": "value"}
```

2. **Register in TRANSFORMS dict**:
```python
TRANSFORMS = {
    'my_custom_transform': my_custom_transform
}
```

3. **Use in routing rules**:
```json
{
  "transforms": [
    {
      "type": "my_custom_transform",
      "param1": "value"
    }
  ]
}
```

---

## Validation

### Required Fields
- `user_id` (string)
- `version` (string)
- `routes` (array, can be empty)

### Route Validation
- `id` must be unique
- `match` must have `doc_type` OR `keywords`
- `target` must be valid target
- `actions` must be non-empty array

### JSON Validation
```bash
jq empty routing_rules.json
```

---

## See Also

- `OCR_UNIVERSAL_PROTOCOL.md` - OCR output specification
- `OCR_MCP_SYSTEM_COMPLETE.md` - Complete system documentation
- `transforms.py` - Transform function implementations
- `action_executor.py` - Action function implementations
