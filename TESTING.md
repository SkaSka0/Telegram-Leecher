# Testing Log

Manual testing notes and progress, tracked separately from
[`PROGRESS.md`](./PROGRESS.md) (task checklist) and
[`ROADMAP.md`](./ROADMAP.md) (reasoning/context).

Use this file to record **what has been tested, what scenario, and the
result** for each item before its checkbox in `PROGRESS.md` is updated.
An item's checkbox may only move to `[TESTED & CONFIRMED]` once every
scenario below for that item is marked `Pass` and the user has
confirmed it.

## Status Legend

- `Not started` — no testing attempted yet
- `In progress` — some scenarios tested, others pending
- `Pass` — scenario behaved as expected, confirmed by user
- `Fail` — scenario did not behave as expected (see Notes)
- `Blocked` — cannot currently be tested (see Notes for reason)

---

## Phase 1, Item 2 — `token.pickle` refresh logic (`gdrive.py` → `build_service`)

**Overall status:** In progress — Scenarios 1–2 passed; Scenarios 3–5 failed due
to a `cancelTask()` bug, now patched and pending retest.

| # | Scenario | Result | Notes |
|---|----------|--------|-------|
| 1 | Happy path — token valid, not expired | Pass | No refresh log line present, as expected. |
| 2 | Token expired, refresh_token valid | Pass | `"Google Drive token refreshed and saved."` logged; `token.pickle` re-written with new `expiry` confirmed. |
| 3 | Refresh_token revoked/invalid | Fail → Retest pending | Expected `cancelTask()` message never reached Telegram; traceback (`asyncio.exceptions.CancelledError`) only appeared after manually interrupting the cell. Root cause: `cancelTask()` called `BOT.TASK.cancel()` *before* sending the notification — cancelling itself mid-flight. Patched in `handler.py` (cancel moved to last step). **Needs retest.** |
| 4 | `token.pickle` in old (oauth2client) format | Fail → Retest pending | Same root cause as Scenario 3 — "outdated format" message never sent before patch. **Needs retest.** |
| 5 | `token.pickle` file missing | Fail → Retest pending | Same root cause as Scenario 3 — "NOT FOUND" message never sent before patch. **Needs retest.** |

**Retest steps (after `cancelTask()` patch):**

1. Repeat Scenarios 3, 4, and 5 exactly as before.
2. Confirm the `#TASK_STOPPED` message reaches the OWNER chat on Telegram
   *without* needing to manually interrupt the cell.
3. Confirm `Paths.WORK_PATH` is removed after each run.
4. Regression check: trigger the manual "Cancel ❌" button mid-task and
   confirm the `"User Cancelled !"` message still sends correctly.
5. Regression check: trigger `cancelTask()` from a non-Google-Drive
   source (e.g. a broken Terabox or aria2 link) to confirm the fix
   doesn't only work for the Google Drive path.

---

## Phase 1, Item 1 — `gDownloadFile` append bug (`gdrive.py`)

**Overall status:** Not started

_No scenarios logged yet. Suggested scenarios once testing begins:_

| # | Scenario | Result | Notes |
|---|----------|--------|-------|
| 1 | Fresh download, no pre-existing file | Not started | Verify file size / checksum matches source. |
| 2 | Retry with same filename after a partial/interrupted download | Not started | This is the scenario the original bug affected — confirm no byte accumulation (compare final file size/checksum against source, not just "it downloaded"). |

---

## Bugs Found During Testing (not yet in PROGRESS.md / ROADMAP.md)

Use this section as a holding area for bugs discovered while testing an
item above. Once confirmed, promote them to a proper entry in
`PROGRESS.md` (and `ROADMAP.md` if reasoning/context is needed) before
removing them from here.

| Found while testing | Bug | Status | Notes |
|----------------------|-----|--------|-------|
| Phase 1, Item 2 (Scenarios 3–5) | `cancelTask()` in `handler.py` calls `BOT.TASK.cancel()` before the cleanup/notification steps run, so the coroutine is cancelled mid-flight and the user never receives the failure message | `[PATCHED, UNTESTED]` | Fix moves `.cancel()` to the very last line of `cancelTask()`; also wraps the delete/send steps in their own try/except so one failing doesn't block the other. Needs the retest steps above before checkboxing anywhere. |
