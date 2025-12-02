# Interviewer Guide - Data Engineering Pseudocode Problems

## Overview

This guide helps interviewers conduct effective technical assessments using the three pseudocode scenarios. The goal is to evaluate a candidate's ability to design data pipelines, handle edge cases, and reason about production concerns.

---

## Interview Structure

### Recommended Timeline (60 minutes total)

1. **Introduction (5 min)** - Explain format, set expectations
2. **Batch Level 1 (15 min)** - Warmup problem, assess fundamentals
3. **Batch Level 2 (20 min)** - Core evaluation, assess production readiness
4. **Streaming Level 1 (15 min)** - Optional, assess streaming knowledge
5. **Questions & Wrap-up (5 min)** - Candidate questions, closing

### Flexibility

- **For junior candidates**: Focus on Batch Level 1, skip streaming
- **For senior candidates**: Spend less time on Level 1, deep dive on Level 2 and streaming
- **For specialists**: Adjust based on role (batch-heavy vs real-time focus)

---

## How to Use the Prompts

### Critical Rules

1. **Start with ONLY the exact prompt** - Don't mention technical terms like "join", "window", or "aggregation"
2. **Let candidates ask questions** - Great engineers clarify requirements before coding
3. **Don't lead** - If they're stuck, ask open-ended questions rather than giving hints
4. **Focus on reasoning** - Pseudocode syntax doesn't matter; logic and trade-offs do

### Example Good vs Bad Interviewing

❌ **Bad**: "So you'll need to do a left join between payments and users, right?"

✅ **Good**: "How would you combine information from both files?"

❌ **Bad**: "You should use a sliding window here."

✅ **Good**: "What kind of window would work for this requirement? Why?"

---

## Detailed Scenario Guidance

### Batch Level 1: Country Revenue by Signup Month

**Purpose**: Assess basic data manipulation and null handling

**Key Prompt**: *"You receive two daily CSV drops. One contains people who created an account with their country and signup date. The other contains payments over time. Some payments come from accounts we do not recognize yet. Produce a daily report that shows, for each country and for the month when the account was created, how much money is associated with those people and how many payers there are."*

#### What to Listen For

**Strong Signals** ✅
- Recognizes need to combine datasets (join/lookup)
- Explicitly handles unknown users (LEFT JOIN or similar logic)
- Mentions handling null countries
- Extracts signup month from signup date
- Groups by (country, signup_month)
- Partitions output by report date
- Asks about duplicate payments

**Weak Signals** ❌
- Uses INNER JOIN without justification (drops orphan payments)
- Ignores null handling entirely
- Doesn't ask clarifying questions
- No consideration for partitioning/incremental processing
- Unclear pseudocode that skips key steps

#### Probing Questions

If they're doing well:
- "What happens if a payment arrives before the user record?"
- "How would you make this idempotent?"
- "How would you handle multiple currencies?"

If they're struggling:
- "Walk me through what information you need about each payment."
- "What happens if you can't find a user_id in the users table?"

#### Grading Rubric

| Category | Weight | Excellent (4) | Good (3) | Fair (2) | Poor (1) |
|----------|--------|---------------|----------|----------|----------|
| **Data Combination** | 25% | Correct outer join with clear reasoning | Correct join type | Works but unclear approach | Incorrect or missing |
| **Null Handling** | 25% | Handles both missing users and null countries | Handles one case | Mentions issue but no solution | Ignores nulls |
| **Aggregation Logic** | 25% | Correct grouping and aggregations | Correct with minor issues | Partially correct | Incorrect approach |
| **Production Readiness** | 25% | Partitioning, idempotency, edge cases | Some prod considerations | Minimal considerations | None mentioned |

**Pass/Fail Threshold**: Average ≥ 2.5 for this scenario

---

### Batch Level 2: Incremental Daily Build with Idempotency

**Purpose**: Assess production pipeline design and idempotency understanding

**Key Prompt**: *"New event files land hourly in a dated path. Yesterday's files may be resent. We need a daily table of per-user metrics that can be safely re-run any time. Compute daily pageviews and total minutes active per user."*

#### What to Listen For

**Strong Signals** ✅
- Tracks which files have been processed (incremental)
- Deduplicates events using event_id
- Uses MERGE/UPSERT instead of append-only
- Defines limited reprocessing window (e.g., 2 days)
- Explains active minutes calculation approach
- Asks about scale and performance
- Considers monitoring and alerting

**Weak Signals** ❌
- Append-only writes (not idempotent)
- No deduplication strategy
- Reprocesses all historical data on every run
- Unclear about how to calculate active minutes
- No consideration for late-arriving data
- Can't explain trade-offs

#### Probing Questions

If they're doing well:
- "What's the trade-off in your reprocessing window size?"
- "How would you handle a week-old file suddenly appearing?"
- "How do you monitor this pipeline's health?"

If they're struggling:
- "What happens if you run this twice with the same input?"
- "How do you know which files are new since last run?"
- "Why might duplicate events appear?"

#### Advanced Discussion Topics
- Schema evolution and backward compatibility
- Handling skewed data (one user with millions of events)
- Cost optimization (partition pruning, Z-ordering)
- Data quality checks and validation

#### Grading Rubric

| Category | Weight | Excellent (4) | Good (3) | Fair (2) | Poor (1) |
|----------|--------|---------------|----------|----------|----------|
| **Idempotency** | 30% | Full idempotency with merge logic | Correct approach, minor gaps | Understands concept, incomplete | No idempotency |
| **Incremental Processing** | 25% | Tracks processed files, bounded window | One of the two | Mentions need but unclear how | Full reprocessing |
| **Deduplication** | 20% | Correct dedup on event_id | Correct with caveats | Mentions but unclear | No deduplication |
| **Calculation Logic** | 15% | Clear active minutes algorithm | Reasonable approach | Vague or incomplete | Incorrect |
| **Production Concerns** | 10% | Monitoring, alerting, performance | Some considerations | Minimal | None |

**Pass/Fail Threshold**: Average ≥ 3.0 for this scenario (this is the critical assessment)

---

### Streaming Level 1: Rolling Device Stats

**Purpose**: Assess real-time processing and streaming concepts

**Key Prompt**: *"A continuous feed of sensor readings arrives. Build a tiny table that shows, per device, the average temperature over the last five minutes, updated every minute. Some messages repeat."*

#### What to Listen For

**Strong Signals** ✅
- Mentions watermarking for late data
- Deduplicates using event_id
- Correctly identifies sliding window (5min window, 1min slide)
- Chooses appropriate output mode (UPDATE)
- Discusses state management and cleanup
- Understands event time vs processing time
- Mentions checkpointing for fault tolerance

**Weak Signals** ❌
- No watermark or late data handling
- Confuses sliding and tumbling windows
- No deduplication strategy
- Unclear about when results are emitted
- Can't explain state growth implications
- Confuses event time with processing time

#### Probing Questions

If they're doing well:
- "How would you handle a device that goes offline for an hour?"
- "What happens to state as time passes?"
- "How do you balance watermark delay with data completeness?"

If they're struggling:
- "What's the difference between a 5-minute tumbling window and a 5-minute sliding window?"
- "When should a window's results be updated?"
- "What happens to events that arrive very late?"

#### Common Misconceptions to Clarify
- **Tumbling vs Sliding**: Tumbling = non-overlapping, Sliding = overlapping
- **Watermark**: Not a fixed delay, but a threshold for "complete enough"
- **State**: Must be actively managed and cleaned up

#### Grading Rubric

| Category | Weight | Excellent (4) | Good (3) | Fair (2) | Poor (1) |
|----------|--------|---------------|----------|----------|----------|
| **Watermarking** | 25% | Clear watermark strategy with reasoning | Mentions watermark | Vague understanding | No concept |
| **Window Definition** | 25% | Correct sliding window params | Correct type, unclear params | Wrong type of window | No windowing |
| **Deduplication** | 20% | Dedup before aggregation | Mentions need | Unclear approach | No deduplication |
| **State & Semantics** | 20% | State management and output mode | One of the two | Vague understanding | No understanding |
| **Event Time** | 10% | Uses event time correctly | Mentions it | Unclear | Uses processing time |

**Pass/Fail Threshold**: Average ≥ 2.5 for this scenario (nice to have for most roles)

---

## Red Flags Across All Scenarios

Watch for these concerning patterns:

### Technical Red Flags 🚩
1. **No null handling** - Doesn't consider missing or null data
2. **Incorrect joins** - Uses inner join when outer is needed (or vice versa) without justification
3. **No idempotency** - Pipelines that break when re-run
4. **Ignoring duplicates** - When problem explicitly mentions them
5. **No partitioning strategy** - For data at scale
6. **Append-only mindset** - When updates/merges are needed

### Communication Red Flags 🚩
1. **Doesn't ask questions** - Jumps to solution without clarifying
2. **Can't explain trade-offs** - No reasoning behind choices
3. **Defensive about feedback** - Reacts poorly to probing questions
4. **Overcomplicates** - Adds unnecessary complexity
5. **Underspecifies** - Pseudocode too vague to evaluate

### Attitude Red Flags 🚩
1. **No production thinking** - Only considers happy path
2. **Ignores scale** - "It works on my laptop"
3. **No monitoring mindset** - Doesn't think about observability
4. **Rigid thinking** - Only knows one tool/approach

---

## Green Flags - Look for These!

### Technical Excellence ✨
- Asks about data volumes and SLAs before designing
- Mentions cost optimization (shuffle reduction, partition pruning)
- Discusses monitoring and alerting proactively
- Considers schema evolution
- Knows when approximate algorithms are acceptable (HyperLogLog, etc.)
- Understands CAP theorem trade-offs

### Strong Communication ✨
- Clarifies requirements before coding
- Explains reasoning for each decision
- Acknowledges limitations of their approach
- Open to feedback and alternative approaches
- Uses clear, precise language

### Production Mindset ✨
- Thinks about error handling and retries
- Considers operational burden
- Mentions data quality checks
- Discusses testing strategy
- Thinks about debugging and troubleshooting

---

## Calibration Examples

### Example 1: Strong Candidate (Hire)

**Scenario**: Batch Level 2

**Behavior**:
- Immediately asks: "What's the typical volume? How many users? Events per day?"
- Designs incremental processing with file tracking
- Uses MERGE with composite key (user_id, date)
- Deduplicates on event_id before aggregation
- Limits reprocessing to 2 days: "Balance between late data and cost"
- Suggests adding data quality checks: "Maybe alert if event count drops 50%"
- Discusses partitioning strategy for query performance

**Why Strong**: Production-ready thinking, asks right questions, explains trade-offs

---

### Example 2: Borderline Candidate (Maybe)

**Scenario**: Batch Level 1

**Behavior**:
- Uses LEFT JOIN correctly
- Handles null countries with COALESCE
- But: Doesn't ask about duplicate payments
- But: No mention of partitioning
- When asked about idempotency: "Oh, yes we should handle that" (adds it after prompting)

**Why Borderline**: Technically competent but needs prompting for production concerns. May be okay for junior role, concerning for senior.

---

### Example 3: Weak Candidate (No Hire)

**Scenario**: Batch Level 2

**Behavior**:
- Designs append-only pipeline
- When asked "what if this runs twice?": "We just won't run it twice"
- No deduplication: "Why would there be duplicates?"
- Loads all historical data on every run
- Can't explain how to calculate active minutes
- Defensive when asked probing questions

**Why Weak**: Lacks production experience, doesn't understand idempotency, poor problem-solving

---

## Post-Interview Checklist

After each interview, rate the candidate on:

- [ ] **Technical Correctness** - Did they get the core logic right?
- [ ] **Production Readiness** - Did they think about edge cases, scale, monitoring?
- [ ] **Communication** - Could they explain their thinking clearly?
- [ ] **Problem Solving** - How did they handle being stuck?
- [ ] **Learning Ability** - Did they incorporate feedback during the session?

### Decision Framework

**Strong Hire** (4/5 on most dimensions):
- Completes Batch 1 and 2 correctly with minimal prompting
- Demonstrates production thinking throughout
- Clear communication and good trade-off reasoning
- Handles probing questions well

**Hire** (3+/5 on most dimensions):
- Completes Batch 1 correctly, Batch 2 with some prompting
- Shows production awareness when asked
- Generally clear communication
- Can learn and adapt during interview

**Maybe** (2.5-3/5 mixed):
- Gets basic logic but misses edge cases
- Needs prompting for production concerns
- Communication could be clearer
- Consider for junior roles or with reservations

**No Hire** (<2.5/5 average):
- Struggles with core logic
- No production thinking even when prompted
- Poor communication or defensive
- Can't explain trade-offs

---

## Adapting for Different Levels

### Data Engineer I (Junior)
- Focus on Batch Level 1
- Expect guidance on edge cases
- Prioritize: correct logic, basic null handling
- Nice to have: partitioning, production concerns

### Data Engineer II (Mid-level)
- Focus on Batch Level 1 & 2
- Should handle edge cases with minimal prompting
- Prioritize: idempotency, incremental processing, deduplication
- Nice to have: streaming knowledge, cost optimization

### Senior Data Engineer
- All three scenarios
- Should proactively mention production concerns
- Prioritize: full production readiness, monitoring, trade-off reasoning
- Must have: deep understanding of idempotency, scale, streaming concepts

### Staff/Principal Data Engineer
- Deep dive on Batch Level 2 and Streaming
- Should drive the conversation
- Prioritize: architecture decisions, cost/performance trade-offs, team scalability
- Must have: can explain when NOT to use certain patterns

---

## Common Interviewer Mistakes to Avoid

1. **Leading the candidate** - Let them struggle a bit, it reveals their thinking
2. **Interrupting too quickly** - Give them time to think
3. **Focusing on syntax** - Pseudocode format doesn't matter
4. **Not probing enough** - Ask "why" to understand their reasoning
5. **Ignoring communication** - Technical skills alone aren't enough
6. **Being too rigid** - There are multiple correct approaches
7. **Not calibrating** - Use the rubrics and examples above

---

## Frequently Asked Questions

### "What if they use a technology I don't know?"

Focus on the concepts. If they mention "Spark's `merge` operation" but you don't know Spark, ask them to explain what merge does. The logic matters more than the tool.

### "What if they ask about production constraints I haven't specified?"

Great sign! Work with them: "Good question. Let's say [reasonable assumption]. How does that change your approach?"

### "They're using a completely different approach than the model answer. Is that okay?"

Maybe! If they can justify the trade-offs and handle edge cases, it might be better than the model answer. Evaluate the reasoning, not just the solution.

### "How technical should the pseudocode be?"

Anywhere from very abstract ("combine datasets") to specific syntax (SQL-like). What matters: is the logic clear and correct?

### "What if we run out of time?"

Batch Level 2 is the most important. If needed, skip streaming and do a deep dive on Level 2.

---

## Feedback Template

After the interview, provide structured feedback:

```
Candidate: [Name]
Role: Data Engineer [Level]
Date: [Date]

SCENARIO SCORES:
- Batch Level 1: [Score/4] - [Brief note]
- Batch Level 2: [Score/4] - [Brief note]  
- Streaming Level 1: [Score/4] - [Brief note]

STRENGTHS:
- [Specific example]
- [Specific example]

AREAS FOR IMPROVEMENT:
- [Specific example with evidence]
- [Specific example with evidence]

DECISION: [Strong Hire / Hire / Maybe / No Hire]

REASONING:
[2-3 sentences justifying decision with specific examples]

RED/GREEN FLAGS:
- [Any notable red or green flags observed]
```

---

## Additional Resources

- Review `INTERVIEW_EXERCISES.md` for complete scenario details
- Check `exercises/*/README.md` for scenario-specific guidance
- Run `reference_solution.py` files to see example implementations
- Practice giving this interview to teammates for calibration

Good luck with your interviews! 🚀
