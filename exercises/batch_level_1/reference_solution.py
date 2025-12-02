"""
Batch Level 1: Country Revenue by Signup Month
Reference implementation using pandas (for illustration purposes)
"""

import pandas as pd
from datetime import datetime


def build_daily_country_signup_report(run_date: str, users_path: str, payments_path: str):
    """
    Build daily report of revenue by country and signup month.
    
    Args:
        run_date: Report date in YYYY-MM-DD format
        users_path: Path to users CSV file
        payments_path: Path to payments CSV file
    
    Returns:
        DataFrame with aggregated results
    """
    # Step 1: Load users and extract signup month
    users = pd.read_csv(users_path)
    users['signup_date'] = pd.to_datetime(users['signup_date'])
    users['signup_month'] = users['signup_date'].dt.strftime('%Y-%m')
    users = users[['user_id', 'country', 'signup_month']]
    
    # Step 2: Load payments
    payments = pd.read_csv(payments_path)
    payments['ts'] = pd.to_datetime(payments['ts'])
    payments['pay_date'] = payments['ts'].dt.date
    
    # Step 3: Left join payments with users (keep all payments)
    mapped = payments.merge(users, on='user_id', how='left')
    
    # Step 4: Handle missing values
    mapped['country'] = mapped['country'].fillna('UNKNOWN')
    mapped['signup_month'] = mapped['signup_month'].fillna('UNKNOWN')
    
    # Step 5: Aggregate by country and signup month
    report = mapped.groupby(['country', 'signup_month']).agg(
        total_revenue=('amount', 'sum'),
        unique_payers=('user_id', 'nunique')
    ).reset_index()
    
    # Step 6: Add report metadata
    report['report_date'] = run_date
    
    return report


if __name__ == '__main__':
    # Example usage
    report = build_daily_country_signup_report(
        run_date='2025-03-10',
        users_path='users.csv',
        payments_path='payments.csv'
    )
    
    print("\nCountry Revenue by Signup Month Report")
    print("=" * 70)
    print(report.to_string(index=False))
    
    # Optionally write to partitioned output
    output_path = f"output/report_date={report['report_date'].iloc[0]}/report.csv"
    print(f"\nWriting to: {output_path}")
    # report.to_csv(output_path, index=False)
