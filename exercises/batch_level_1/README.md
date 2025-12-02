# Batch Level 1: Country Revenue by Signup Month

## Problem Statement

You receive two daily CSV drops. One contains people who created an account with their country and signup date. The other contains payments over time. Some payments come from accounts we do not recognize yet. Produce a daily report that shows, for each country and for the month when the account was created, how much money is associated with those people and how many payers there are.

## Input Files

- `users.csv` - User account information with signup dates
- `payments.csv` - Payment transactions

## Expected Output

A report showing:
- Country
- Signup month (YYYY-MM format)
- Total revenue
- Number of unique payers

## Sample Solution Location

Write your pseudocode solution in `solution_pseudocode.txt`

For reference implementation, see `reference_solution.py`

## Key Considerations

1. **Missing Users**: Some payments may come from user_ids not in the users table
2. **Null Countries**: Some users may have null country values
3. **Date Handling**: Convert signup dates to month granularity
4. **Aggregation**: Sum revenue and count distinct payers per country/month combination
5. **Partitioning**: Output should be partitioned by report date for incremental processing

## Expected Output for Sample Data

```
country,signup_month,total_revenue,unique_payers
SE,2025-01,325,2
ES,2025-02,200,1
DE,2025-02,125,1
UNKNOWN,2025-01,80,1
UNKNOWN,UNKNOWN,300,1
```

Note: 
- U1 (SE, Jan) paid 175 total (100+75)
- U4 (SE, Jan) paid 150
- U2 (ES, Feb) paid 200
- U5 (DE, Feb) paid 125
- U6 (null country, Jan) paid 80
- U99 (unknown user) paid 300
