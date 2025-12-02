# Data Engineering Interview Exercise - Quick Start Guide

## 🎯 Purpose

This repository contains three live pseudocode problems for data engineering interviews. These scenarios evaluate a candidate's ability to design data pipelines, handle edge cases, and think about production concerns.

## 📋 What's Included

### Documentation
- **`INTERVIEW_EXERCISES.md`** - Complete problem statements with model answers
- **`INTERVIEWER_GUIDE.md`** - Comprehensive guide for conducting interviews with grading rubrics
- **`exercises/*/README.md`** - Scenario-specific details and expected outputs

### Three Scenarios

1. **Batch Level 1: Country Revenue by Signup Month** (15 min)
   - Warmup problem testing data joins and null handling
   - Files: `exercises/batch_level_1/`

2. **Batch Level 2: Incremental Daily Build with Idempotency** (20 min)
   - Core assessment of production pipeline design
   - Files: `exercises/batch_level_2/`

3. **Streaming Level 1: Rolling Device Stats** (15 min - Optional)
   - Real-time processing with watermarks and windows
   - Files: `exercises/streaming_level_1/`

## 🚀 Quick Start for Interviewers

### Before the Interview

1. **Read the materials** (30 minutes)
   ```bash
   # Read these in order:
   - INTERVIEW_EXERCISES.md       # Problem statements
   - INTERVIEWER_GUIDE.md          # How to conduct and grade
   - exercises/batch_level_2/README.md  # Focus on this one
   ```

2. **Run the reference solutions** (optional but recommended)
   ```powershell
   cd exercises/batch_level_1
   python reference_solution.py
   
   cd ../batch_level_2
   python reference_solution.py
   
   cd ../streaming_level_1
   python reference_solution.py
   ```

### During the Interview (60 min total)

1. **Introduction** (5 min)
   - "We'll work through 2-3 pseudocode scenarios"
   - "Think aloud, ask questions, focus on logic not syntax"
   - "I may ask probing questions to understand your thinking"

2. **Batch Level 1** (15 min)
   - Use ONLY the exact prompt from `INTERVIEW_EXERCISES.md`
   - Let candidate ask clarifying questions
   - Take notes using grading rubric

3. **Batch Level 2** (20 min) - **Most Important**
   - This is your primary signal
   - Probe on: idempotency, deduplication, merge strategy
   - Watch for production thinking

4. **Streaming Level 1** (15 min) - **Optional**
   - For senior roles or if time permits
   - Skip for junior candidates

5. **Wrap-up** (5 min)
   - Candidate questions
   - Thank them for their time

## 📁 Repository Structure

```
.
├── INTERVIEW_EXERCISES.md          # Complete problem statements
├── INTERVIEWER_GUIDE.md            # How to interview and grade
├── README.md                       # This file
├── requirements.txt                # Python dependencies
│
├── exercises/
│   ├── batch_level_1/
│   │   ├── README.md               # Scenario details
│   │   ├── users.csv               # Sample data
│   │   ├── payments.csv            # Sample data
│   │   ├── solution_pseudocode.txt # Template for candidate
│   │   └── reference_solution.py   # Example implementation
│   │
│   ├── batch_level_2/
│   │   ├── README.md
│   │   ├── events_2025-03-01.csv
│   │   ├── events_2025-03-02.csv
│   │   ├── events_2025-03-02_resent.csv  # Demonstrates duplicates
│   │   ├── solution_pseudocode.txt
│   │   └── reference_solution.py
│   │
│   └── streaming_level_1/
│       ├── README.md
│       ├── sensor_stream_sample.csv
│       ├── solution_pseudocode.txt
│       └── reference_solution.py
│
├── config/                         # Original project config
├── data/                          # Original project data
├── sql/                           # Original project SQL
├── src/                           # Original project source
└── tests/                         # Original project tests
```

## 🎓 For Candidates (If Sharing Exercises for Take-Home)

### Setup

1. **Clone or download this repository**
   ```powershell
   git clone <repository-url>
   cd data-engineer-recruitment-test
   ```

2. **Install dependencies** (optional - only if running Python examples)
   ```powershell
   pip install -r requirements.txt
   ```

### Working on Exercises

Each exercise has:
- **Problem description** in `exercises/*/README.md`
- **Sample data** in CSV files
- **Solution template** in `solution_pseudocode.txt`
- **Reference implementation** in `reference_solution.py` (for learning)

### Guidelines

1. **Write pseudocode, not production code**
   - Focus on logic and data flow
   - Syntax doesn't matter (SQL-like, Python-like, or plain English)
   - Comment your reasoning

2. **Consider production concerns**
   - How would this run at scale?
   - What if the pipeline fails halfway?
   - How do you handle bad data?

3. **Ask questions** (even if take-home)
   - Add a "ASSUMPTIONS" section to your solution
   - Note what you'd clarify in a real scenario

### Example Pseudocode Format

```
// Good pseudocode is clear and logical:

FUNCTION process_data(input_date):
  // Step 1: Load data
  data <- read_csv(path + input_date)
  
  // Step 2: Clean and transform
  clean_data <- data
                 .filter(is_valid)
                 .deduplicate(key=id)
  
  // Step 3: Aggregate
  results <- clean_data
              .group_by(category)
              .aggregate(sum(amount))
  
  // Step 4: Write output
  write_partitioned(results, partition=input_date)
END

// Trade-offs:
// - Using deduplication adds processing time but ensures correctness
// - Partitioning by date enables incremental processing
```

## 🔍 What We're Looking For

### Technical Skills ✅
- Correct data combination logic (joins, lookups)
- Proper null and missing data handling
- Understanding of idempotency and deduplication
- Appropriate aggregation and windowing
- Partitioning and incremental processing

### Production Thinking ✅
- Edge case awareness
- Scalability considerations
- Monitoring and observability
- Cost optimization
- Error handling

### Communication ✅
- Clear pseudocode
- Explained reasoning
- Asks clarifying questions
- Acknowledges trade-offs

## 📊 Grading Criteria

See `INTERVIEWER_GUIDE.md` for detailed rubrics. Quick summary:

| Scenario | Focus Area | Pass Threshold |
|----------|-----------|----------------|
| Batch Level 1 | Data joins, null handling | ≥2.5/4 average |
| Batch Level 2 | Idempotency, incremental processing | ≥3.0/4 average |
| Streaming Level 1 | Windowing, watermarks, state | ≥2.5/4 average |

**Overall Decision**:
- **Strong Hire**: 4/5 on most dimensions, minimal prompting needed
- **Hire**: 3+/5 on most dimensions, solid with some guidance
- **Maybe**: 2.5-3/5, technically okay but concerns
- **No Hire**: <2.5/5 average, fundamental gaps

## 🛠️ Running Reference Solutions

Reference implementations use pandas for simplicity. In production, you'd use:
- **Batch**: Apache Spark, dbt, SQL (BigQuery/Snowflake)
- **Streaming**: Spark Streaming, Flink, Kafka Streams

To run examples:

```powershell
# Batch Level 1
cd exercises/batch_level_1
python reference_solution.py

# Expected output:
# Country Revenue by Signup Month Report
# ======================================================================
# country signup_month  total_revenue  unique_payers  report_date
#      SE      2025-01            325              2   2025-03-10
#      ES      2025-02            200              1   2025-03-10
# ...
```

## 🎯 Interview Tips

### For Interviewers
1. **Don't lead** - Let candidates discover edge cases
2. **Probe deeply** - Ask "why" to understand reasoning
3. **Focus on concepts** - Not specific tools or syntax
4. **Watch communication** - How they explain matters
5. **Use rubrics** - Consistent evaluation across candidates

### For Candidates
1. **Ask questions** - Clarify requirements before coding
2. **Think aloud** - Explain your reasoning
3. **Consider edge cases** - Null data, duplicates, failures
4. **Discuss trade-offs** - Every design has pros and cons
5. **Keep it simple** - Start with basic solution, then enhance

## 📞 Support

For questions about these exercises:
1. Review `INTERVIEWER_GUIDE.md` for detailed guidance
2. Check scenario-specific `README.md` files
3. Run `reference_solution.py` to see working examples

## 📝 License

See `LICENSE` file in repository root.

## 🔄 Version History

- **v1.0** - Initial release with three core scenarios
- Scenarios cover: batch processing, idempotency, streaming
- Includes comprehensive interviewer guide and grading rubrics

---

**Good luck with your interviews!** 🚀

Remember: Great data engineers combine technical skill with production thinking and clear communication. These exercises help you assess all three.
