# Live Session Pseudocode Problems – Data Engineering

This document contains three live, language-agnostic problems for the interview's pseudocode stage. Each scenario includes the interviewer prompt, candidate deliverables, model answer outline, edge cases, and grading notes.

---

## Batch Level 1: Country Revenue by Signup Month

### Interviewer Prompt
**Say only this:**

> You receive two daily CSV drops. One contains people who created an account with their country and signup date. The other contains payments over time. Some payments come from accounts we do not recognize yet. Produce a daily report that shows, for each country and for the month when the account was created, how much money is associated with those people and how many payers there are.

### Input Datasets

#### users.csv
| Column | Description |
|--------|-------------|
| user_id | Unique identifier of the user |
| country | ISO country code (nullable) |
| signup_date | User signup date (YYYY-MM-DD) |

#### payments.csv
| Column | Description |
|--------|-------------|
| user_id | User identifier (may not exist in users) |
| amount | Payment amount (assume same currency) |
| ts | Payment timestamp (ISO-8601) |

### Candidate Deliverables
- Pseudocode to compute the report and write it partitioned by report_date
- Reasoning about handling missing users and data volume

### Model Answer Outline (Pseudocode)

```
FUNCTION build_daily_country_signup_report(run_date):
  users <- read_csv('/data/users/' + run_date)
            .with_column(signup_month := to_month(signup_date))
            .select(user_id, country, signup_month)
  
  pays  <- read_csv('/data/payments/' + run_date)
            .select(user_id, amount, ts)
            .with_column(pay_date := to_date(ts))
  
  mapped <- map_attributes(pays BY user_id -> users BY user_id)
            .with_column(country := coalesce(country, 'UNKNOWN'))
            .with_column(signup_month := signup_month OR 'UNKNOWN')
  
  agg <- mapped
          .group_by(country, signup_month)
          .agg({ 
            total_revenue := sum(amount), 
            unique_payers := approx_count_distinct(user_id) 
          })
  
  write_partitioned(agg, 
                    table='gold.country_signup_revenue', 
                    partition=[run_date])
```

### Edge Cases to Discuss
- Duplicate payments and idempotency
- Currency normalization if multiple currencies appear later
- Late arrival of users versus payments

### Grading Notes
- **Strong**: Correct mapping of payments to user attributes, explicit handling of unknown users, grouping on country and signup month, partitioned write
- **Weak**: Inner-only linkage that drops orphan payments without justification; ignores null handling

### Mini Sample and Expected Output

**users.csv**
```
U1,SE,2025-01-10
U2,ES,2025-02-05
```

**payments.csv**
```
U1,100,2025-03-01T10:00:00Z
U3,50,2025-03-02T12:00:00Z
```

**Expected Report**
```
SE,2025-01,100,1
UNKNOWN,UNKNOWN,50,1
```

---

## Batch Level 2: Incremental Daily Build with Idempotency

### Interviewer Prompt
**Say only this:**

> New event files land hourly in a dated path. Yesterday's files may be resent. We need a daily table of per-user metrics that can be safely re-run any time. Compute daily pageviews and total minutes active per user.

### Input Dataset

#### events
| Column | Description |
|--------|-------------|
| user_id | User identifier |
| ts | Event timestamp (ISO-8601) |
| event_type | Event type string (e.g., page_view) |
| event_id | Idempotency key; duplicates possible |

### Candidate Deliverables
- Pseudocode for an incremental, idempotent daily pipeline
- Reasoning about deduplication, small reprocessing window, and merge strategy

### Model Answer Outline (Pseudocode)

```
FUNCTION build_user_daily(run_date):
  new_files <- list_new_files('s3://events/raw/', 
                               since = last_success('build_user_daily'))
  
  raw <- read(new_files)
          .with_column(dt := to_date(ts))
  
  clean <- raw
            .where(dt <= run_date)
            .dedupe_on(event_id, keep = latest_by(ts))
  
  per_user_day <- clean
                   .group_by(user_id, dt)
                   .agg({
                     pageviews := count_if(event_type == 'page_view'),
                     active_minutes := approx_active_minutes(ts, gap = 5m)
                   })
  
  write_merge(table='silver.user_daily', 
              key=[user_id, dt], 
              df=per_user_day, 
              partition=dt, 
              update_window_days=2)
```

### Edge Cases to Discuss
- File replays and reprocessing horizon
- Skew in user activity
- Handling new event types and schema evolution

### Grading Notes
- **Strong**: Incremental file discovery, deduplication by event_id, merge/upsert to target, limited backfill window
- **Weak**: Append-only writes with no idempotency and no strategy for resent files

---

## Streaming Level 1 (Optional): Rolling Device Stats

### Interviewer Prompt
**Say only this:**

> A continuous feed of sensor readings arrives. Build a tiny table that shows, per device, the average temperature over the last five minutes, updated every minute. Some messages repeat.

### Input Stream

#### events
| Column | Description |
|--------|-------------|
| device_id | Unique device id |
| ts | Event time (ISO-8601) |
| temperature | Numeric reading |
| humidity | Numeric reading |
| event_id | Idempotency key; duplicates possible |

### Candidate Deliverables
- Streaming pseudocode with state and windowing
- Reasoning about watermarking, output mode, and deduplication

### Model Answer Outline (Pseudocode)

```
STREAM process_device_stats:
  src <- read_stream('events')
          .with_watermark(ts, 10m)
  
  clean <- src.dedupe_on(event_id)
  
  win <- clean
          .group_by(device_id, window(ts, length=5m, slide=1m))
          .agg(avg_temp := avg(temperature))
  
  write_stream(win, 
               table='realtime.device_5m_avg', 
               output_mode='update')
```

### Edge Cases to Discuss
- Out-of-order events up to 10 minutes late
- Choice of sliding versus tumbling windows
- State growth and retention policy

### Grading Notes
- **Strong**: Correct use of watermark, deduplication, and sliding window; clear write semantics
- **Weak**: No deduplication or watermarking; incorrect window definition

---

## Interview Guidance

### General Tips for Interviewers
1. **Start with the exact prompt** - Don't lead the candidate with technical terms
2. **Let them ask clarifying questions** - Good candidates will ask about edge cases
3. **Focus on reasoning** - The pseudocode syntax matters less than the logic
4. **Probe on production concerns** - Ask about scalability, monitoring, error handling
5. **Allow 15-20 minutes per problem** - Batch 1 is warmup, Batch 2 is core, Streaming is bonus

### Red Flags
- No consideration for null/missing data
- Ignoring duplicate handling when explicitly mentioned
- No partitioning strategy for large-scale data
- Unclear about idempotency in batch jobs
- Cannot explain trade-offs in their design

### Green Flags
- Asks about data volumes and SLAs
- Mentions monitoring and alerting
- Discusses cost optimization (shuffle, partition pruning)
- Considers schema evolution
- Understands when approximate algorithms are acceptable
