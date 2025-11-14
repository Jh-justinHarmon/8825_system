8825 × Joju — Dropbox Contribution Miner (Brainstorm Plan)
Date: 2025-11-09 21:41:22 (America/Chicago)

— Overview —
Point at any Dropbox folder to attribute who created and who last edited each Adobe Illustrator (.ai) (and other) file. Count contributions (files created, files modified, total touches) without double-counting. Export clean Joju-ready summaries and keep counts continuously updated via change monitoring.

— Goals —
1) Attribute creators and last editors for .ai (and other) files.
2) Produce contribution rollups: files created, files modified, total touches.
3) Prevent double-counting across renames, copies, and multi-save bursts.
4) Continuously monitor and update results.
5) Export Joju-ready JSON mining reports.

— Signals to Fuse (with Fallbacks) —
A) Dropbox content + change stream
   • List folder + cursor; longpoll or webhook to detect changes.
   • content_hash to de-dup across renames/copies.
   • Revisions per file for version history.
B) Attribution (who did what)
   • Business/Team: team_log/get_events for file add/edit actors (creator, editors).
   • Shared folders (non-Business): last modifier via revisions metadata when present.
C) Inside the file (Illustrator/XMP)
   • Parse XMP for dc:creator, xmp:CreatorTool, xmp:ModifyDate, and (when present) xmpMM:History steps using ExifTool.
   • Dropbox = actor of record; XMP = app-level authorship. Prefer Dropbox when both exist; use XMP as fallback/validator.

— Anti-double-count Rules —
1) Identity: resolve Dropbox account_id → person once; cache map.
2) File identity: prefer file id; also track content_hash to collapse duplicates across copies/renames.
3) Event collapse: count one "modify" per file per actor per revision (use list_revisions); multiple saves that roll into one revision count once.
4) Copy storms: if a file is copied N times with identical content_hash, credit creator once; modifications on each copy credit respective editors.

— Data Model (Joju-ready example) —
{
  "content_type": "mining_report",
  "target_focus": "joju",
  "metadata": {
    "source": "dropbox_contribution_miner",
    "timestamp": "2025-11-09T00:00:00Z",
    "folder_root": "/Team/Design/Brand"
  },
  "files": [
    {
      "file_id": "id:AbC123...",
      "path": "/Team/Design/Brand/logo.ai",
      "ext": "ai",
      "content_hash": "dbxhash...",
      "created_at": "2025-09-01T14:22:03Z",
      "created_by": {"account_id": "dbid:A1", "name": "Jh"},
      "last_revision": 42,
      "last_edit_at": "2025-10-05T18:11:22Z",
      "last_edit_by": {"account_id": "dbid:B2", "name": "Cam"},
      "xmp": {
        "dc_creator": ["Justin Harmon"],
        "modify_date": "2025-10-05T18:11:20Z",
        "creator_tool": "Adobe Illustrator 28"
      }
    }
  ],
  "contributors": [
    {
      "account_id": "dbid:A1",
      "name": "Jh",
      "files_created": 17,
      "files_modified": 29,
      "total_touches": 46
    }
  ]
}

— System Sketch (components) —
• Watcher
  - Input: folder path(s).
  - Uses files/list_folder + cursor + longpoll (or webhooks) for near-real-time changes.
• Ingestor
  - On change: fetch file metadata (id, path, content_hash), revisions, and (if Business) team_log events filtered by file + time window.
• XMP Parser (AI/PDF/PSD)
  - Shell out to ExifTool; read dc:creator, xmp:ModifyDate, xmpMM:* where present.
• Attribution Resolver
  - Merge Dropbox actor ↔ XMP names; prefer Dropbox actor when both present and timestamps align.
• Deduper + Scorer
  - Collapse by (file_id, revision, actor); handle content_hash duplicate logic.
• Aggregator + Exporter
  - Roll up counts per contributor; write Joju mining_report JSON to the 8825 inbox and library.

— Minimal PoC (Python sketch) —
# pip install dropbox
import json, subprocess, datetime as dt
import dropbox

DBX_TOKEN = "YOUR_TOKEN"
ROOT = "/Team/Design/Brand"
dbx = dropbox.Dropbox(DBX_TOKEN)

def list_all_with_cursor(path):
    res = dbx.files_list_folder(path, recursive=True, include_non_downloadable_files=False)
    yield from res.entries
    cursor = res.cursor
    while res.has_more:
        res = dbx.files_list_folder_continue(cursor)
        cursor = res.cursor
        yield from res.entries
    return cursor  # keep for longpoll

def xmp_for(path_local):
    # exiftool must be installed; returns dict of XMP fields if present
    out = subprocess.check_output(["exiftool", "-j", "-XMP:*", path_local])
    arr = json.loads(out.decode("utf-8"))
    return arr[0] if arr else {}

def head_for_file(md):  # md is dropbox.files.FileMetadata
    return {
        "file_id": md.id,
        "path": md.path_lower,
        "ext": (md.name.split(".")[-1] if "." in md.name else "").lower(),
        "content_hash": getattr(md, "content_hash", None),
        "server_modified": md.server_modified.isoformat()
    }

def revisions_for(path_id):
    # Example: get revisions & last editor hint (if available)
    revs = dbx.files_list_revisions(path_id, limit=10, mode=dropbox.files.ListRevisionsMode.path)
    return [(r.rev, getattr(r, "server_modified", None)) for r in revs.entries]

all_entries = [e for e in list_all_with_cursor(ROOT) if isinstance(e, dropbox.files.FileMetadata)]
heads = [head_for_file(e) for e in all_entries if e.name.lower().endswith(".ai")]

report = {
  "content_type": "mining_report",
  "target_focus": "joju",
  "metadata": {"source": "dropbox_contribution_miner", "timestamp": dt.datetime.utcnow().isoformat()},
  "files": heads,
  "contributors": []
}
print(json.dumps(report, indent=2))

— Continuous Monitoring Patterns —
• Longpoll + cursor for near-real-time updates (no server required).
• Webhooks if you want immediate callbacks and scale; still fetch details after notification.
• Team log cursors (Business): keep your own team_log/get_events cursor for incremental attribution pulls.

— Edge Cases & Guardrails —
• Non-Business accounts: you may not get full "who edited" via API; lean on revisions (when shared) + XMP + filename heuristics.
• AI without XMP: older exports or stripped metadata; treat XMP as optional.
• Clock skew: compare Dropbox server_modified vs xmp:ModifyDate; if drift > N minutes, prefer Dropbox.
• Copies vs renames: use file id first; cross-folder dupes caught via content_hash.

— Rollout (fast) —
1) PoC: one folder, list files, compute content_hash, capture basic counts, write Joju JSON to inbox.
2) Attribution: add team_log/get_events (if available) and parse XMP for .ai files.
3) Deduper + rules: implement (file_id, revision, actor) collapse + content_hash duplicate logic.
4) Monitor: add longpoll/webhook loop; nightly re-score sweep for drift.
5) Surface: export mining_report to joju_sandbox/libraries/... and project spaces.

— Placement in 8825 —
• Mode = Brainstorm (code + roadmap, no execution).
• Use inbox JSON shape + naming when you push reports (YYYYMMDD_HHMMSS_mining_report_joju.json).
• Integration targets (Joju library/projects) are pre-defined.

— Nice-to-haves (later) —
• Contribution score = 2x files_created + 1x files_modified (+ optional "assist" for comments/renames).
• Dashboard in Notion or Data Studio fed by the JSON.
• Per-asset lineage: show editor timeline (creator → editors) from team logs + XMP history.

End of brainstorm.