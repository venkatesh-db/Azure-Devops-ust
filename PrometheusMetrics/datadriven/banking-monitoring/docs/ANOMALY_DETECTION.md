# Anomaly Detection Guide

## Overview
This guide covers the anomaly detection capabilities for detecting unusual patterns in banking operations, fraud, and system anomalies.

## Architecture

```
Data Sources
    ↓
[Anomaly Detection Engine]
    ├── [Z-Score Detector]
    ├── [IQR Detector]
    ├── [Moving Average Detector]
    ├── [Seasonality Detector]
    ├── [Behavior Analyzer]
    └── [Contextual Detector]
    ↓
[Anomalies with Severity]
    ↓
[Alerts → Notifications → Actions]
```

## Detection Methods

### 1. Z-Score Detection

**What it detects:** Statistical outliers

**Formula:** 
$$z = \frac{x - \mu}{\sigma}$$

Where:
- x = current value
- μ = mean
- σ = standard deviation

**Parameters:**
- `threshold`: 2.5-3.5 (higher = fewer alerts)
  - 2.5: ~1.2% anomalies in normal distribution
  - 3.0: ~0.3% anomalies
  - 3.5: ~0.05% anomalies

**Use Cases:**
- Large transaction detection
- API latency spikes
- Error rate increases
- Account balance anomalies

**Example:**
```python
from analytics.anomaly_detector import ZScoreDetector

detector = ZScoreDetector(threshold=2.5)
values = [100, 105, 110, 108, 102, 500, 101]
anomalies = detector.detect(values)
# Returns: [(5, 3.8)] - index 5 with z-score 3.8
```

### 2. IQR (Interquartile Range) Detection

**What it detects:** Box plot outliers

**Formula:**
```
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 - Q1
Lower Bound = Q1 - 1.5 * IQR
Upper Bound = Q3 + 1.5 * IQR
```

**Advantages:**
- Robust to extreme values
- Good for skewed distributions
- Less sensitive to outliers than z-score

**Example:**
```python
from analytics.anomaly_detector import IQRDetector

detector = IQRDetector(multiplier=1.5)
values = [10, 15, 20, 18, 22, 19, 200]
anomalies = detector.detect(values)
# Returns: [(6, 'high_outlier')]
```

### 3. Moving Average Detection

**What it detects:** Trend deviations

**How it works:**
1. Calculate moving average over window
2. Calculate moving standard deviation
3. Flag values beyond sigma threshold

**Parameters:**
- `window_size`: 7-30 data points
- `sigma`: 2.0-3.0 standard deviations

**Use Cases:**
- Performance degradation
- Throughput changes
- User activity patterns
- Daily/weekly cycles

**Example:**
```python
from analytics.anomaly_detector import MovingAverageDetector

detector = MovingAverageDetector(window_size=7, sigma=2.0)
daily_values = [100, 105, 110, 108, 102, 101, 99, 98, 97, 95, 150]
anomalies = detector.detect(daily_values)
```

### 4. Seasonality Detection

**What it detects:** Deviations from seasonal patterns

**Assumes:**
- Data has repeating patterns
- Period is known (hourly=24, daily=7)

**Use Cases:**
- Time-of-day patterns
- Day-of-week patterns
- Monthly/yearly patterns
- Working hours vs. off-hours

**Example:**
```python
from analytics.anomaly_detector import SeasonalityDetector

detector = SeasonalityDetector(period=24)  # Hourly data, daily pattern
hourly_data = [100] * 24 + [110] * 24 + [95] * 24 + [500] + [100] * 23
anomalies = detector.detect(hourly_data)
```

### 5. Behavioral Analysis

**Trend Change Detection:**
Identifies when direction changes
```python
# Uptrend → Downtrend
# [100, 110, 120] → [115, 105, 95]
change_points = analyzer.detect_trend_change(values, window=10)
```

**Level Shift Detection:**
Identifies sudden mean changes
```python
# Before: [100, 102, 101]
# After: [200, 202, 201]
shift_points = analyzer.detect_level_shift(values, threshold=2.0)
```

### 6. Contextual Anomaly Detection

**Transaction Anomalies:**
```python
anomalies = detector.detect_transaction_anomalies(transactions)
# Detects:
# - Unusually large amounts
# - Multiple large transactions
# - Unusual patterns for account
```

**Fraud Pattern Detection:**
```python
fraud_patterns = detector.detect_fraud_patterns(transactions)
# Detects:
# - Rapid consecutive transfers (< 60 seconds)
# - Multiple failed attempts
# - Cross-border patterns
# - Account abuse patterns
```

## Severity Levels

```
CRITICAL  → Immediate action required
          ├─ Fraud detected
          ├─ System failure
          └─ Massive anomaly

HIGH      → Urgent investigation
          ├─ Transaction spike
          ├─ Error rate surge
          └─ Security concern

MEDIUM    → Monitor & investigate
          ├─ Performance issue
          ├─ Pattern deviation
          └─ Unusual activity

LOW       → Informational
          └─ Minor deviations
```

## Implementation Examples

### Example 1: Detect Large Transactions

```python
from analytics.anomaly_detector import AnomalyDetectionEngine

engine = AnomalyDetectionEngine()

# Sample transaction amounts
transaction_amounts = [500, 520, 490, 510, 5000, 525, 480]

# Detect anomalies
anomalies = engine.detect_metric_anomalies(
    metric_name='transaction_amount',
    values=transaction_amounts
)

for anomaly in anomalies:
    print(f"Amount: ${anomaly.value}")
    print(f"Expected: ${anomaly.expected_value}")
    print(f"Severity: {anomaly.severity}")
    print(f"Description: {anomaly.description}")
```

### Example 2: Detect Fraudulent Pattern

```python
# Simulate rapid consecutive transactions
transactions = [
    {
        'transaction_id': 'TXN-1',
        'from_account': 'ACC-001',
        'to_account': 'ACC-999',
        'amount': 100,
        'timestamp': '2024-01-19T10:00:00'
    },
    {
        'transaction_id': 'TXN-2',
        'from_account': 'ACC-001',
        'to_account': 'ACC-998',
        'amount': 150,
        'timestamp': '2024-01-19T10:00:30'  # 30 seconds later
    },
    {
        'transaction_id': 'TXN-3',
        'from_account': 'ACC-001',
        'to_account': 'ACC-997',
        'amount': 200,
        'timestamp': '2024-01-19T10:00:45'  # 45 seconds after first
    }
]

# Detect fraud patterns
fraud_anomalies = detector.detect_fraud_patterns(transactions)

for anomaly in fraud_anomalies:
    if anomaly.severity == 'critical':
        print(f"⚠️ FRAUD ALERT: {anomaly.description}")
        print(f"Account: {anomaly.context['account_id']}")
        print(f"Gap: {anomaly.context['gap_seconds']} seconds")
```

### Example 3: Combine Multiple Detection Methods

```python
# Collect metrics over time
metrics_data = {
    'transaction_amounts': [100, 105, 110, 108, 102, 5000],
    'api_latency_ms': [50, 55, 48, 52, 3000, 45],
    'error_count': [0, 1, 0, 0, 25, 1]
}

transaction_data = [
    {'transaction_id': 'txn-1', 'amount': 100, 'timestamp': '...'},
    # ... more transactions
]

# Run comprehensive detection
all_anomalies = engine.detect_all_anomalies(
    metrics_data=metrics_data,
    transaction_data=transaction_data
)

# Process results by type
for metric_name, anomalies in all_anomalies.items():
    for anomaly in anomalies:
        # Severity-based routing
        if anomaly.severity in ('critical', 'high'):
            send_alert(anomaly)
        if anomaly.severity == 'critical':
            trigger_automatic_action(anomaly)
        
        # Log for analysis
        log_anomaly(anomaly)
```

## Integration with Log Analysis

```python
from log_analysis.log_analyzer import LogAnalyzer
from analytics.anomaly_detector import AnomalyDetectionEngine

# Load and analyze logs
analyzer = LogAnalyzer()
analyzer.load_logs_from_file('app.log')

# Get transaction statistics
txn_stats = analyzer.analyze_transaction_patterns()

# Extract metrics for anomaly detection
transaction_amounts = [
    float(t['metadata'].get('amount', 0))
    for t in analyzer.entries
    if 'amount' in t.metadata
]

# Detect anomalies in metrics
engine = AnomalyDetectionEngine()
anomalies = engine.detect_metric_anomalies(
    'transaction_amount',
    transaction_amounts
)

# Combine with trend analysis
trends = analyzer.detect_trends(window_hours=24)

# Generate report
report = {
    'transactions': txn_stats,
    'anomalies': [a.to_dict() for a in anomalies],
    'trends': trends
}
```

## Response Actions

### Alert Escalation
```
CRITICAL
  ↓
[Immediate Email + SMS]
[Create Incident]
[Notify On-Call Team]
[Trigger Remediation]

HIGH
  ↓
[Email Notification]
[Create Ticket]
[Monitor Closely]

MEDIUM
  ↓
[Log Entry]
[Dashboard Alert]
[Scheduled Review]

LOW
  ↓
[Log Only]
[Metrics Tracking]
```

### Remediation Examples

**For Fraud Pattern:**
1. Lock account
2. Alert compliance team
3. Notify customer
4. Halt similar transactions

**For Performance Anomaly:**
1. Auto-scale resources
2. Clear caches
3. Optimize queries
4. Page on-call engineer

**For Error Spike:**
1. Increase monitoring
2. Check dependencies
3. Review recent deployments
4. Rollback if necessary

## Tuning & Optimization

### Choosing Thresholds

```python
# Too sensitive (catches many false positives)
threshold = 1.5  # 6.7% of normal data flagged

# Balanced
threshold = 2.5  # 1.2% of normal data flagged

# Less sensitive (misses real anomalies)
threshold = 3.5  # 0.05% of normal data flagged
```

### Window Size Selection

```
Small window (7): Sensitive to recent changes, faster response
   ├─ Good for: Fraud, system alerts
   └─ Risk: More false positives

Medium window (30): Balanced approach
   ├─ Good for: Performance monitoring
   └─ Risk: Moderate response time

Large window (365): Seasonal patterns
   ├─ Good for: Yearly trends
   └─ Risk: Slow to detect changes
```

### Testing Your Detector

```python
# Create synthetic anomaly
normal_data = [100] * 100
anomaly_data = normal_data + [500]  # Add anomaly

# Test detection
anomalies = detector.detect(anomaly_data)

# Verify sensitivity
assert len(anomalies) > 0, "Detector failed to find anomaly"
assert anomalies[0][0] == 100, "Wrong index"

print("✓ Detector working correctly")
```

## Monitoring the Detectors

Track detector performance:
```python
metrics = {
    'true_positives': 5,      # Caught real anomalies
    'false_positives': 2,     # False alerts
    'false_negatives': 1,     # Missed anomalies
    'precision': 5/7,         # 71%
    'recall': 5/6,            # 83%
    'f1_score': 2*(5/7*5/6)/(5/7+5/6)
}
```

## Best Practices

1. ✅ Use multiple detection methods
2. ✅ Combine statistical and domain knowledge
3. ✅ Test with synthetic anomalies
4. ✅ Review false positives regularly
5. ✅ Adjust thresholds based on business impact
6. ✅ Alert on severity, not frequency
7. ✅ Provide context in alerts
8. ✅ Automate response where safe
9. ✅ Continuously tune and improve
10. ✅ Document decisions and rationale

## References

- [Z-Score Analysis](https://en.wikipedia.org/wiki/Standard_score)
- [IQR Outlier Detection](https://en.wikipedia.org/wiki/Interquartile_range)
- [Moving Average Convergence](https://en.wikipedia.org/wiki/MACD)
- [Seasonal Decomposition](https://en.wikipedia.org/wiki/Decomposition_of_time_series)
- [Anomaly Detection in Time Series](https://arxiv.org/abs/1211.6677)
