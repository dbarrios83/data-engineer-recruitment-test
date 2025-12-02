"""
Streaming Level 1: Rolling Device Stats
Reference implementation using pandas (batch simulation of streaming)

Note: This is a simplified batch simulation. In production, you would use:
- Apache Spark Structured Streaming
- Apache Flink
- Apache Kafka Streams
- Cloud-native streaming (AWS Kinesis, GCP Dataflow, Azure Stream Analytics)
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Iterator, Tuple


def create_sliding_windows(
    start_time: datetime,
    end_time: datetime,
    window_length_minutes: int = 5,
    slide_minutes: int = 1
) -> Iterator[Tuple[datetime, datetime]]:
    """
    Generate sliding window intervals.
    
    Args:
        start_time: Earliest event time
        end_time: Latest event time
        window_length_minutes: Length of each window
        slide_minutes: How often windows start
    
    Yields:
        Tuples of (window_start, window_end)
    """
    current = start_time
    window_length = timedelta(minutes=window_length_minutes)
    slide = timedelta(minutes=slide_minutes)
    
    while current <= end_time:
        yield (current, current + window_length)
        current += slide


def process_device_stats_batch_simulation(
    events_path: str,
    watermark_minutes: int = 10,
    window_length_minutes: int = 5,
    slide_minutes: int = 1
) -> pd.DataFrame:
    """
    Simulate streaming processing of device stats using batch logic.
    
    In real streaming:
    - Events arrive continuously
    - State is maintained in memory
    - Watermark triggers window computations
    - Late data beyond watermark is dropped
    
    Args:
        events_path: Path to event stream data
        watermark_minutes: How late events can arrive
        window_length_minutes: Window size
        slide_minutes: Window slide interval
    
    Returns:
        DataFrame with device statistics per window
    """
    # Step 1: Read stream (simulated as batch)
    stream = pd.read_csv(events_path)
    stream['ts'] = pd.to_datetime(stream['ts'])
    
    # Step 2: Deduplicate by event_id (keep latest by timestamp)
    clean = stream.sort_values('ts').drop_duplicates(subset=['event_id'], keep='last')
    
    print(f"Total events: {len(stream)}")
    print(f"After deduplication: {len(clean)}")
    print(f"Duplicate events removed: {len(stream) - len(clean)}\n")
    
    # Step 3: Define time range for windows
    min_time = clean['ts'].min()
    max_time = clean['ts'].max()
    
    print(f"Event time range: {min_time} to {max_time}\n")
    
    # Step 4: Generate sliding windows and compute aggregates
    results = []
    
    for window_start, window_end in create_sliding_windows(
        min_time, 
        max_time, 
        window_length_minutes, 
        slide_minutes
    ):
        # Filter events in this window
        in_window = clean[
            (clean['ts'] >= window_start) & 
            (clean['ts'] < window_end)
        ]
        
        if len(in_window) == 0:
            continue
        
        # Aggregate per device
        for device_id, group in in_window.groupby('device_id'):
            results.append({
                'device_id': device_id,
                'window_start': window_start,
                'window_end': window_end,
                'avg_temp': round(group['temperature'].mean(), 2),
                'event_count': len(group),
                'min_temp': group['temperature'].min(),
                'max_temp': group['temperature'].max()
            })
    
    output = pd.DataFrame(results)
    
    # Step 5: Sort by window and device
    output = output.sort_values(['window_start', 'device_id']).reset_index(drop=True)
    
    return output


def explain_streaming_concepts():
    """Print explanations of key streaming concepts."""
    print("=" * 70)
    print("KEY STREAMING CONCEPTS")
    print("=" * 70)
    
    print("\n1. WATERMARK")
    print("-" * 70)
    print("   - Threshold for how late events can arrive")
    print("   - Events arriving after watermark are dropped")
    print("   - Example: 10-minute watermark means events up to 10min late are processed")
    print("   - Trade-off: Longer watermark = more complete data but higher latency")
    
    print("\n2. SLIDING WINDOWS")
    print("-" * 70)
    print("   - Overlapping time windows")
    print("   - Each event may appear in multiple windows")
    print("   - Example: 5-minute window sliding every 1 minute")
    print("   - Window [10:00-10:05] contains events from 10:00:00 to 10:04:59")
    
    print("\n3. OUTPUT MODES")
    print("-" * 70)
    print("   - UPDATE: Only emit changed results (most efficient for aggregations)")
    print("   - APPEND: Only emit new rows (for non-aggregated streams)")
    print("   - COMPLETE: Emit entire result table (expensive, for small tables)")
    
    print("\n4. STATE MANAGEMENT")
    print("-" * 70)
    print("   - Streaming jobs maintain state for active windows")
    print("   - State includes: aggregates, deduplication keys, window buffers")
    print("   - Old state cleaned up after watermark threshold passed")
    print("   - State can grow large → need checkpointing and cleanup policies")
    
    print("\n5. EVENT TIME vs PROCESSING TIME")
    print("-" * 70)
    print("   - Event time: When event actually occurred (use this!)")
    print("   - Processing time: When event processed by system")
    print("   - Always use event time for correct results with late data")
    print("=" * 70)


if __name__ == '__main__':
    # Print concept explanations
    explain_streaming_concepts()
    
    # Process sample data
    print("\n" + "=" * 70)
    print("PROCESSING SAMPLE SENSOR DATA")
    print("=" * 70 + "\n")
    
    result = process_device_stats_batch_simulation(
        events_path='sensor_stream_sample.csv',
        watermark_minutes=10,
        window_length_minutes=5,
        slide_minutes=1
    )
    
    print("Device Statistics per 5-Minute Sliding Window:")
    print("=" * 70)
    print(result.to_string(index=False))
    
    print("\n" + "=" * 70)
    print("OBSERVATIONS")
    print("=" * 70)
    print("✓ Each device appears in multiple overlapping windows")
    print("✓ Duplicate events (sensor_002) deduplicated before aggregation")
    print("✓ Windows update as new events arrive (simulated here as batch)")
    print("✓ Out-of-order events (sensor_013 at 09:58) included if within watermark")
    
    # Show specific example
    print("\n" + "=" * 70)
    print("EXAMPLE: device_001 in different windows")
    print("=" * 70)
    device_001_windows = result[result['device_id'] == 'device_001']
    print(device_001_windows[['window_start', 'window_end', 'avg_temp', 'event_count']].to_string(index=False))
