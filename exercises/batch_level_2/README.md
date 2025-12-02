# Batch Level 2: Incremental Daily Build with Idempotency

## Problem Statement

New event files land hourly in a dated path. Yesterday's files may be resent. We need a daily table of per-user metrics that can be safely re-run any time. Compute daily pageviews and total minutes active per user.

## Input Files

Event files are organized by date with the possibility of:
- Multiple files per day (hourly drops)
- Files being resent (duplicates across files)
- Late-arriving data (events from previous days appearing in new files)

Sample files:
- `events_2025-03-01.csv` - Initial drop for March 1st
- `events_2025-03-02.csv` - Initial drop for March 2nd
- `events_2025-03-02_resent.csv` - Simulates file replay (contains duplicates)

## Expected Output

A daily table with:
- user_id
- date (dt)
- pageviews (count)
- active_minutes (approximate)

## Sample Solution Location

Write your pseudocode solution in `solution_pseudocode.txt`

For reference implementation, see `reference_solution.py`

## Key Considerations

1. **Idempotency**: Pipeline must produce same results when re-run
2. **Deduplication**: Use `event_id` to handle duplicate events across file replays
3. **Incremental Processing**: Only process new files since last successful run
4. **Merge Strategy**: Use upsert/merge instead of append to handle reprocessing
5. **Reprocessing Window**: Limit how far back you update (e.g., last 2 days)
6. **Active Minutes**: Calculate session-based activity with gap threshold (e.g., 5 minutes)

## Expected Output for Sample Data

After processing all files (with deduplication):

```
user_id,dt,pageviews,active_minutes
U1,2025-03-01,2,12
U2,2025-03-01,2,3
U3,2025-03-01,2,15
U1,2025-03-02,2,7
U2,2025-03-02,0,0
U3,2025-03-03,2,10
U4,2025-03-02,2,20
U5,2025-03-02,2,15
U6,2025-03-03,1,0
```

Note:
- Duplicate events (evt_009, evt_013) should only be counted once
- Active minutes calculated based on time gaps within a session
- Each run should merge/upsert into existing table, not append
