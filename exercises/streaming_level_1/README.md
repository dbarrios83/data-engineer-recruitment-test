# Streaming Level 1: Rolling Device Stats

## Problem Statement

A continuous feed of sensor readings arrives. Build a tiny table that shows, per device, the average temperature over the last five minutes, updated every minute. Some messages repeat.

## Input Stream

Continuous stream of sensor events with fields:
- `device_id` - Unique device identifier
- `ts` - Event timestamp (ISO-8601 format)
- `temperature` - Numeric reading (celsius)
- `humidity` - Numeric reading (percentage)
- `event_id` - Idempotency key (duplicates possible)

Sample file: `sensor_stream_sample.csv` (simulates streaming data)

## Expected Output

A continuously updated table with:
- device_id
- window_start (timestamp)
- window_end (timestamp)
- avg_temp (average temperature)

Updated every minute with 5-minute sliding windows.

## Sample Solution Location

Write your pseudocode solution in `solution_pseudocode.txt`

For reference implementation, see `reference_solution.py`

## Key Considerations

1. **Watermarking**: Handle late-arriving events (e.g., up to 10 minutes late)
2. **Deduplication**: Use `event_id` to remove duplicate messages
3. **Window Type**: Sliding window (5 minutes length, 1 minute slide)
4. **Output Mode**: Use 'update' mode to refresh aggregates as new data arrives
5. **State Management**: Keep state for active windows, clean up old state
6. **Event Time**: Use event timestamp (`ts`), not processing time

## Sliding Window Explanation

For a 5-minute window sliding every 1 minute:
- Window 1: [10:00 - 10:05) → Updated at 10:05, 10:06, 10:07, ...
- Window 2: [10:01 - 10:06) → Updated at 10:06, 10:07, 10:08, ...
- Window 3: [10:02 - 10:07) → Updated at 10:07, 10:08, 10:09, ...

Each event may contribute to multiple overlapping windows.

## Expected Output for Sample Data

Example windows for device_001:

```
device_id,window_start,window_end,avg_temp
device_001,2025-03-01T10:01:00Z,2025-03-01T10:06:00Z,22.86
device_001,2025-03-01T10:02:00Z,2025-03-01T10:07:00Z,23.02
```

Note:
- Duplicate event (sensor_002) should be counted only once
- Average calculated over events within each 5-minute window
- Out-of-order events (sensor_013 at 09:58) handled by watermark
- Windows update as new data arrives within watermark threshold

## Streaming vs Batch Comparison

| Aspect | Batch | Streaming |
|--------|-------|-----------|
| Processing | Periodic (hourly/daily) | Continuous (real-time) |
| Latency | Minutes to hours | Seconds to minutes |
| State | Stateless (recompute from scratch) | Stateful (maintain windows) |
| Completeness | Complete data at processing time | Watermarks define "complete enough" |
| Output | Append or replace partitions | Update/append mode |
