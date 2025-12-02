# 📚 Interview Exercise - Document Index

Quick reference for all exercise documentation.

## 🎯 Start Here

| Document | Purpose | Audience | Time |
|----------|---------|----------|------|
| **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** | Confirmation of what was set up | Interviewers | 2 min |
| **[QUICK_START.md](QUICK_START.md)** | Getting started guide | Everyone | 10 min |

## 📖 Main Documentation

| Document | Purpose | Audience | Time |
|----------|---------|----------|------|
| **[INTERVIEW_EXERCISES.md](INTERVIEW_EXERCISES.md)** | Complete problem statements with model answers | Interviewers & Candidates | 15 min |
| **[INTERVIEWER_GUIDE.md](INTERVIEWER_GUIDE.md)** | How to conduct interviews, grading rubrics | Interviewers only | 30 min |
| **[README.md](README.md)** | Repository overview | Everyone | 5 min |

## 📂 Exercise Directories

### Batch Level 1: Country Revenue by Signup Month
**Difficulty**: Warmup | **Time**: 15 min | **Location**: `exercises/batch_level_1/`

| File | Purpose |
|------|---------|
| `README.md` | Problem details, sample data explanation, expected output |
| `users.csv` | 7 sample users with countries and signup dates |
| `payments.csv` | 8 payment transactions (includes orphan payments) |
| `solution_pseudocode.txt` | Template for candidate to fill in |
| `reference_solution.py` | Working implementation with explanations |

**Tests**: Data joins, null handling, basic aggregation

---

### Batch Level 2: Incremental Daily Build with Idempotency
**Difficulty**: Core Assessment ⭐ | **Time**: 20 min | **Location**: `exercises/batch_level_2/`

| File | Purpose |
|------|---------|
| `README.md` | Problem details, idempotency requirements, expected output |
| `events_2025-03-01.csv` | Initial event file (14 events, includes 1 duplicate) |
| `events_2025-03-02.csv` | Second day events (8 events) |
| `events_2025-03-02_resent.csv` | Resent file (5 events, demonstrates file replay) |
| `solution_pseudocode.txt` | Template with discussion questions |
| `reference_solution.py` | Full implementation with idempotency logic |

**Tests**: Idempotency, deduplication, merge/upsert, incremental processing

---

### Streaming Level 1: Rolling Device Stats
**Difficulty**: Optional/Advanced | **Time**: 15 min | **Location**: `exercises/streaming_level_1/`

| File | Purpose |
|------|---------|
| `README.md` | Streaming concepts, window types, expected output |
| `sensor_stream_sample.csv` | 19 sensor readings (includes duplicates and out-of-order) |
| `solution_pseudocode.txt` | Template with streaming concept questions |
| `reference_solution.py` | Batch simulation of streaming with detailed explanations |

**Tests**: Watermarking, sliding windows, state management, event time

---

## 🎓 Reading Order by Role

### For Interviewers (First Time)
1. ✅ `SETUP_COMPLETE.md` - Verify what you have
2. ✅ `QUICK_START.md` - Overview and workflow
3. ✅ `INTERVIEW_EXERCISES.md` - Learn the problems
4. ✅ `INTERVIEWER_GUIDE.md` - How to conduct and grade
5. ✅ `exercises/batch_level_2/README.md` - Deep dive on main assessment
6. 🔄 Practice with a colleague

**Total prep time**: ~1.5 hours

---

### For Candidates (Take-Home)
1. ✅ `QUICK_START.md` - Understand the format
2. ✅ `exercises/batch_level_1/README.md` - Start here
3. ✅ Write solution in `solution_pseudocode.txt`
4. ✅ `exercises/batch_level_2/README.md` - Main challenge
5. ✅ Write solution in `solution_pseudocode.txt`
6. ✅ (Optional) `exercises/streaming_level_1/README.md`
7. 🔍 Review `reference_solution.py` files after attempting

**Total time**: 2-3 hours

---

### For Hiring Managers (Quick Review)
1. ✅ `QUICK_START.md` - Understand the exercises
2. ✅ `INTERVIEWER_GUIDE.md` - Review grading criteria
3. ✅ `INTERVIEW_EXERCISES.md` - See the problems

**Total time**: 30 minutes

---

## 🔍 Quick Reference

### Problem Statements (Exact Prompts)

**Batch Level 1**:
> "You receive two daily CSV drops. One contains people who created an account with their country and signup date. The other contains payments over time. Some payments come from accounts we do not recognize yet. Produce a daily report that shows, for each country and for the month when the account was created, how much money is associated with those people and how many payers there are."

**Batch Level 2**:
> "New event files land hourly in a dated path. Yesterday's files may be resent. We need a daily table of per-user metrics that can be safely re-run any time. Compute daily pageviews and total minutes active per user."

**Streaming Level 1**:
> "A continuous feed of sensor readings arrives. Build a tiny table that shows, per device, the average temperature over the last five minutes, updated every minute. Some messages repeat."

---

### Grading Quick Reference

| Scenario | Pass Threshold | Key Signals |
|----------|---------------|-------------|
| Batch Level 1 | ≥2.5/4 | Correct join, null handling |
| Batch Level 2 | ≥3.0/4 | Idempotent, dedup, merge |
| Streaming Level 1 | ≥2.5/4 | Watermark, sliding window |

**Overall Decision**:
- **Strong Hire**: 4/5 on most dimensions
- **Hire**: 3+/5 on most dimensions
- **Maybe**: 2.5-3/5 mixed
- **No Hire**: <2.5/5 average

---

### Running Reference Solutions

```powershell
# Install dependencies (if needed)
pip install pandas

# Run examples
python exercises/batch_level_1/reference_solution.py
python exercises/batch_level_2/reference_solution.py
python exercises/streaming_level_1/reference_solution.py
```

---

## 📊 Files by Type

### Documentation Files
- `SETUP_COMPLETE.md` - Setup confirmation
- `QUICK_START.md` - Getting started guide  
- `INTERVIEW_EXERCISES.md` - Problem statements
- `INTERVIEWER_GUIDE.md` - Interview guidance
- `INDEX.md` - This file
- `README.md` - Repository overview

### Data Files (CSV)
- `exercises/batch_level_1/users.csv`
- `exercises/batch_level_1/payments.csv`
- `exercises/batch_level_2/events_2025-03-01.csv`
- `exercises/batch_level_2/events_2025-03-02.csv`
- `exercises/batch_level_2/events_2025-03-02_resent.csv`
- `exercises/streaming_level_1/sensor_stream_sample.csv`

### Solution Templates
- `exercises/batch_level_1/solution_pseudocode.txt`
- `exercises/batch_level_2/solution_pseudocode.txt`
- `exercises/streaming_level_1/solution_pseudocode.txt`

### Reference Implementations
- `exercises/batch_level_1/reference_solution.py`
- `exercises/batch_level_2/reference_solution.py`
- `exercises/streaming_level_1/reference_solution.py`

### Scenario Documentation
- `exercises/batch_level_1/README.md`
- `exercises/batch_level_2/README.md`
- `exercises/streaming_level_1/README.md`

---

## 🎯 Common Questions

**Q: Which document should I read first?**  
A: Start with `QUICK_START.md`

**Q: Where are the grading rubrics?**  
A: `INTERVIEWER_GUIDE.md` - sections for each scenario

**Q: Can I see example solutions?**  
A: Yes, `reference_solution.py` in each exercise directory

**Q: How long does each exercise take?**  
A: Batch 1: 15 min, Batch 2: 20 min, Streaming: 15 min

**Q: Which exercise is most important?**  
A: Batch Level 2 - it's the core assessment

**Q: Do candidates write real code?**  
A: No, pseudocode only. Focus is on logic and reasoning.

**Q: What if I don't know Python?**  
A: That's okay! Pseudocode can be SQL-like, Python-like, or plain English

**Q: How do I practice interviewing?**  
A: Give the interview to a colleague using `INTERVIEWER_GUIDE.md`

---

## 🚀 Quick Actions

| I want to... | Go to... |
|--------------|----------|
| Start interviewing | `QUICK_START.md` → `INTERVIEWER_GUIDE.md` |
| Solve exercises | `QUICK_START.md` → `exercises/*/README.md` |
| See example answers | `reference_solution.py` files |
| Understand grading | `INTERVIEWER_GUIDE.md` (rubrics section) |
| Review problem statements | `INTERVIEW_EXERCISES.md` |
| Verify setup | `SETUP_COMPLETE.md` |

---

**Happy interviewing!** 🎉

For any questions, refer to the specific document above or check the scenario README files.
