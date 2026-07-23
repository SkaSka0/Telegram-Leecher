# Progress Tracker

Quick-glance checklist for tracking implementation status. For the reasoning
behind each item (why it's prioritized, what risk it addresses, or how to
approach it), see [`ROADMAP.md`](./ROADMAP.md).

> **Note:** Only check an item once the fix is actually committed to the
> codebase — not just discussed or planned.

---

## Phase 0 — Documentation Sync

- [x] Update "Supported Links" table — mark Mega.nz as ✅
- [x] Update "Supported Links" table — mark Terabox as ✅ (add if missing)
- [x] Re-check "Codebase Structure" section for accuracy

---

## Phase 1 — High-Priority Bug Fixes

- [ ] Fix `gDownloadFile` append bug (`gdrive.py`) — delete pre-existing
      file before writing instead of using `"ab"` mode
      — **[PATCHED, UNTESTED]**
- [ ] Add `token.pickle` refresh logic when expired (`gdrive.py` →
      `build_service`)
- [ ] Remove unused `ProcessPoolExecutor()` in Mega branch (`manager.py`)
- [ ] Filter out Google Docs/Sheets shortcuts before `gDownloadFile` call
      (`gdrive.py` → `gDownloadFolder`)
- [ ] Replace silent `except Exception: pass` / bare `logging.error` with
      proper propagation or user-facing notification

---

## Phase 2 — Structural Refactor

- [ ] Decide: is multi-task support actually on the roadmap? (only then
      refactor `variables.py` into class-based namespaces)
- [ ] Split `Leech()` in `handler.py` into smaller single-responsibility
      functions
- [ ] Split `taskScheduler()` in `task_manager.py`
- [ ] Simplify `YouTubeDL()` in `ytdl.py` (nested function + threading +
      hooks)
- [ ] Standardize error-handling pattern (when to `cancelTask()`, when to
      log, when to retry)
- [ ] Simplify `get_Aria2c_Name` — replace double `aria2c` invocation with
      a direct HTTP `HEAD` request

---

## Phase 3 — Reliability & Observability

- [ ] Add consistent retry mechanism for network-dependent downloaders
      (Google Drive, Terabox, aria2)
- [ ] Add basic test coverage for pure functions in `helper.py`
      (`sizeUnit`, `getTime`, `speedETA`, `getIDFromURL`)
- [ ] Replace remaining `print()` calls with `logging`
      (`handler.py`, `manager.py`)

---

## Phase 4 — New Features

- [ ] GDTot/Sharer/short-link resolver module
- [ ] Automatic Google Drive token refresh (proper feature, builds on
      Phase 1 patch)
- [ ] More robust Mega progress parsing (replace fragile regex parsing
      in `mega.py`)

---

## Custom / Ad-hoc

*(Use this section for tasks not yet in ROADMAP.md, e.g. the video
caption feature.)*

- [ ] Design fixed caption format for video uploads (data sourced from
      external JSON, not parsed from the video file itself)
