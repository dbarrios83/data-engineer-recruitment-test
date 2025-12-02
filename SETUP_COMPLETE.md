# Exercise Setup Complete! ✅

## What Was Created

### 📁 Main Documentation
1. **`QUICK_START.md`** - Your starting point (read this first!)
2. **`INTERVIEW_EXERCISES.md`** - Complete problem statements with model answers
3. **`INTERVIEWER_GUIDE.md`** - Comprehensive guide for conducting interviews
4. **Updated `README.md`** - Now points to all exercise materials

### 📂 Exercise Directories

#### 1. Batch Level 1: Country Revenue by Signup Month
**Location**: `exercises/batch_level_1/`

Files created:
- ✅ `README.md` - Problem details and expected output
- ✅ `users.csv` - Sample user data (7 users)
- ✅ `payments.csv` - Sample payment data (8 transactions)
- ✅ `solution_pseudocode.txt` - Template for candidates
- ✅ `reference_solution.py` - Working Python implementation

**Key concepts**: Data joins, null handling, aggregation

---

#### 2. Batch Level 2: Incremental Daily Build with Idempotency
**Location**: `exercises/batch_level_2/`

Files created:
- ✅ `README.md` - Problem details and expected output
- ✅ `events_2025-03-01.csv` - Initial event file
- ✅ `events_2025-03-02.csv` - Second day events
- ✅ `events_2025-03-02_resent.csv` - Resent file (demonstrates duplicates)
- ✅ `solution_pseudocode.txt` - Template for candidates
- ✅ `reference_solution.py` - Working Python implementation with idempotency

**Key concepts**: Idempotency, deduplication, merge/upsert, incremental processing

---

#### 3. Streaming Level 1: Rolling Device Stats
**Location**: `exercises/streaming_level_1/`

Files created:
- ✅ `README.md` - Problem details and expected output
- ✅ `sensor_stream_sample.csv` - Sample sensor data (19 events with duplicates)
- ✅ `solution_pseudocode.txt` - Template for candidates
- ✅ `reference_solution.py` - Batch simulation of streaming concepts

**Key concepts**: Watermarking, sliding windows, state management, event time

---

## 🚀 Next Steps

### For Interviewers

1. **Read the documentation** (30 min)
   ```powershell
   # Open and read in this order:
   code QUICK_START.md
   code INTERVIEW_EXERCISES.md
   code INTERVIEWER_GUIDE.md
   ```

2. **Explore the exercises** (15 min)
   ```powershell
   # Browse each scenario:
   cd exercises/batch_level_1
   cat README.md
   
   cd ../batch_level_2
   cat README.md
   
   cd ../streaming_level_1
   cat README.md
   ```

3. **Run reference solutions** (optional)
   ```powershell
   # Install dependencies first (if needed):
   pip install pandas

   # Run each example:
   python exercises/batch_level_1/reference_solution.py
   python exercises/batch_level_2/reference_solution.py
   python exercises/streaming_level_1/reference_solution.py
   ```

4. **Practice** (30 min)
   - Practice giving the interview to a colleague
   - Use the grading rubrics in `INTERVIEWER_GUIDE.md`
   - Calibrate on what constitutes "strong" vs "weak"

### For Candidates (Take-Home)

1. **Start with the Quick Start**
   ```powershell
   code QUICK_START.md
   ```

2. **Work through exercises in order**
   - Start with Batch Level 1 (easier warmup)
   - Move to Batch Level 2 (most important)
   - Try Streaming Level 1 if time permits

3. **Use the templates**
   - Write pseudocode in `solution_pseudocode.txt` files
   - Focus on logic, not syntax
   - Add comments explaining your reasoning

4. **Check reference solutions** (after attempting)
   - Compare your approach
   - Understand different ways to solve problems

---

## 📊 File Structure Summary

```
data-engineer-recruitment-test/
│
├── QUICK_START.md              ← START HERE!
├── INTERVIEW_EXERCISES.md      ← Problem statements
├── INTERVIEWER_GUIDE.md        ← How to interview
├── README.md                   ← Updated with links
│
├── exercises/
│   ├── batch_level_1/
│   │   ├── README.md
│   │   ├── users.csv
│   │   ├── payments.csv
│   │   ├── solution_pseudocode.txt
│   │   └── reference_solution.py
│   │
│   ├── batch_level_2/
│   │   ├── README.md
│   │   ├── events_2025-03-01.csv
│   │   ├── events_2025-03-02.csv
│   │   ├── events_2025-03-02_resent.csv
│   │   ├── solution_pseudocode.txt
│   │   └── reference_solution.py
│   │
│   └── streaming_level_1/
│       ├── README.md
│       ├── sensor_stream_sample.csv
│       ├── solution_pseudocode.txt
│       └── reference_solution.py
│
└── [original project files remain unchanged]
    ├── config/
    ├── data/
    ├── sql/
    ├── src/
    └── tests/
```

---

## 🎓 What Each Exercise Tests

### Batch Level 1 (Warmup - 15 min)
**Tests**: Basic data manipulation
- ✅ Combining datasets (joins)
- ✅ Handling null/missing data
- ✅ Basic aggregations
- ✅ Partitioned output

**Pass criteria**: Correct join logic, handles unknowns

---

### Batch Level 2 (Core - 20 min) ⭐ MOST IMPORTANT
**Tests**: Production pipeline design
- ✅ Idempotency (safe to re-run)
- ✅ Incremental processing
- ✅ Deduplication strategies
- ✅ Merge/upsert patterns
- ✅ Reprocessing windows

**Pass criteria**: Idempotent design, explicit dedup, merge logic

---

### Streaming Level 1 (Optional - 15 min)
**Tests**: Real-time processing concepts
- ✅ Watermarking (late data)
- ✅ Window types (sliding vs tumbling)
- ✅ State management
- ✅ Event time vs processing time
- ✅ Output modes

**Pass criteria**: Correct watermark + window, deduplication

---

## 📈 Interview Flow

Recommended 60-minute structure:

```
[0-5 min]   Introduction & setup
[5-20 min]  Batch Level 1 (warmup)
[20-40 min] Batch Level 2 (main assessment) ⭐
[40-55 min] Streaming Level 1 (if time/appropriate)
[55-60 min] Wrap-up & questions
```

**Key point**: Batch Level 2 is your primary signal!

---

## ✨ Key Features

### For Each Exercise You Get:

1. **Problem Statement** - Exact prompt to use
2. **Sample Data** - Realistic CSV files with edge cases
3. **Expected Output** - What correct solution produces
4. **Solution Template** - Starting point for candidates
5. **Reference Implementation** - Working Python code
6. **Grading Rubric** - Objective scoring criteria

### Edge Cases Built In:

- ✅ Null values (missing countries)
- ✅ Unknown references (payments from unknown users)
- ✅ Duplicate events (same event_id in multiple files)
- ✅ Out-of-order data (late arrivals)
- ✅ File replays (idempotency testing)

---

## 🎯 What Makes These Exercises Good

1. **Language-agnostic** - Focus on concepts, not syntax
2. **Production-focused** - Real problems data engineers face
3. **Scalable difficulty** - Easy to adjust for junior/senior
4. **Clear evaluation** - Rubrics remove subjectivity
5. **Comprehensive** - Tests breadth of DE knowledge

---

## 🔍 Quick Testing

Want to verify everything works?

```powershell
# Quick test - run one reference solution:
cd exercises/batch_level_1
python reference_solution.py

# Should output:
# Country Revenue by Signup Month Report
# ======================================================================
# country signup_month  total_revenue  unique_payers  report_date
#      SE      2025-01            325              2   2025-03-10
# ...
```

---

## 💡 Pro Tips

### For Interviewers:
- 🎤 **Let them talk** - Silence is okay, let them think
- ❓ **Ask "why"** - Understand their reasoning
- 🎯 **Focus on concepts** - Not specific tools/syntax
- 📊 **Use rubrics** - Consistent evaluation
- 🔄 **Calibrate** - Practice with team first

### For Candidates:
- 💬 **Think aloud** - Explain your reasoning
- ❓ **Ask questions** - Clarify before coding
- 🎯 **Start simple** - Basic solution first, then enhance
- ⚠️ **Consider edge cases** - Nulls, duplicates, failures
- ⚖️ **Discuss trade-offs** - No perfect solution exists

---

## 📞 Questions?

Review these in order:
1. `QUICK_START.md` - Overview and getting started
2. `INTERVIEW_EXERCISES.md` - Problem details
3. `INTERVIEWER_GUIDE.md` - Detailed guidance
4. Scenario-specific `README.md` files
5. Run `reference_solution.py` examples

---

## ✅ Verification Checklist

Before your first interview, confirm:

- [ ] Read `QUICK_START.md`
- [ ] Read `INTERVIEWER_GUIDE.md`
- [ ] Reviewed all three problem statements
- [ ] Understand the grading rubrics
- [ ] Practiced with a colleague (recommended)
- [ ] Can explain what makes a "strong" answer

---

**Everything is ready to go!** 🎉

Start with `QUICK_START.md` and you'll be conducting great interviews in no time.

Good luck! 🚀
