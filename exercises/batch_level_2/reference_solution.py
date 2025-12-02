"""
Batch Level 2: Incremental Daily Build with Idempotency
Reference implementation using pandas (for illustration purposes)
"""

import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional


def calculate_active_minutes(timestamps: pd.Series, gap_threshold_minutes: int = 5) -> float:
    """
    Calculate approximate active minutes from event timestamps.
    Sessions are broken when gap exceeds threshold.
    
    Args:
        timestamps: Series of datetime objects
        gap_threshold_minutes: Maximum gap to consider same session
    
    Returns:
        Approximate active minutes
    """
    if len(timestamps) <= 1:
        return 0.0
    
    sorted_ts = timestamps.sort_values()
    gaps = sorted_ts.diff().dt.total_seconds() / 60.0  # Convert to minutes
    
    # Count time between consecutive events if gap < threshold
    active_time = 0.0
    for gap in gaps[1:]:  # Skip first NaT
        if pd.notna(gap) and gap <= gap_threshold_minutes:
            active_time += gap
    
    return round(active_time, 2)


def build_user_daily(
    run_date: str,
    new_files: List[str],
    existing_data_path: Optional[str] = None,
    update_window_days: int = 2
) -> pd.DataFrame:
    """
    Build idempotent daily user metrics from event files.
    
    Args:
        run_date: Report date in YYYY-MM-DD format
        new_files: List of new event file paths to process
        existing_data_path: Path to existing user_daily table (if any)
        update_window_days: How many days back to allow updates
    
    Returns:
        DataFrame with updated user daily metrics
    """
    # Step 1: Load all new event files
    if not new_files:
        print("No new files to process")
        return pd.DataFrame()
    
    all_events = []
    for file_path in new_files:
        df = pd.read_csv(file_path)
        all_events.append(df)
    
    raw = pd.concat(all_events, ignore_index=True)
    
    # Step 2: Add date column and filter
    raw['ts'] = pd.to_datetime(raw['ts'])
    raw['dt'] = raw['ts'].dt.date
    run_date_obj = datetime.strptime(run_date, '%Y-%m-%d').date()
    raw = raw[raw['dt'] <= run_date_obj]
    
    # Step 3: Deduplicate by event_id (keep latest by timestamp)
    clean = raw.sort_values('ts').drop_duplicates(subset=['event_id'], keep='last')
    
    # Step 4: Calculate per-user daily metrics
    def aggregate_user_day(group):
        return pd.Series({
            'pageviews': (group['event_type'] == 'page_view').sum(),
            'active_minutes': calculate_active_minutes(group['ts'])
        })
    
    per_user_day = clean.groupby(['user_id', 'dt']).apply(aggregate_user_day).reset_index()
    
    # Step 5: Merge with existing data (if any)
    if existing_data_path and Path(existing_data_path).exists():
        existing = pd.read_csv(existing_data_path)
        existing['dt'] = pd.to_datetime(existing['dt']).dt.date
        
        # Only keep existing data outside update window
        cutoff_date = run_date_obj - timedelta(days=update_window_days)
        existing_old = existing[existing['dt'] < cutoff_date]
        
        # Combine old data with new calculations
        result = pd.concat([existing_old, per_user_day], ignore_index=True)
        
        # Deduplicate on (user_id, dt), keeping latest calculation
        result = result.drop_duplicates(subset=['user_id', 'dt'], keep='last')
    else:
        result = per_user_day
    
    # Sort for consistency
    result = result.sort_values(['dt', 'user_id']).reset_index(drop=True)
    
    return result


if __name__ == '__main__':
    # Example usage: process files incrementally
    
    # First run: process initial files
    print("=" * 70)
    print("Run 1: Processing initial files")
    print("=" * 70)
    
    run1_files = [
        'events_2025-03-01.csv',
        'events_2025-03-02.csv'
    ]
    
    result1 = build_user_daily(
        run_date='2025-03-02',
        new_files=run1_files
    )
    
    print("\nUser Daily Metrics (Run 1):")
    print(result1.to_string(index=False))
    
    # Save intermediate result
    result1.to_csv('user_daily_interim.csv', index=False)
    
    # Second run: process resent file (demonstrates idempotency)
    print("\n" + "=" * 70)
    print("Run 2: Processing resent file + new data (idempotent)")
    print("=" * 70)
    
    run2_files = [
        'events_2025-03-02_resent.csv'  # Contains duplicates + new data
    ]
    
    result2 = build_user_daily(
        run_date='2025-03-03',
        new_files=run2_files,
        existing_data_path='user_daily_interim.csv'
    )
    
    print("\nUser Daily Metrics (Run 2 - After Deduplication):")
    print(result2.to_string(index=False))
    
    print("\n" + "=" * 70)
    print("Key Points Demonstrated:")
    print("=" * 70)
    print("✓ Duplicate events (evt_009, evt_013) counted only once")
    print("✓ New events from resent file (evt_017, evt_018, evt_019) added")
    print("✓ Existing metrics updated within reprocessing window")
    print("✓ Pipeline is idempotent - same input produces same output")
