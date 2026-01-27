#!/usr/bin/env python3
"""
Example: Complete Banking Application with Monitoring
Demonstrates all components working together
"""

import json
import sys
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_1_create_accounts():
    """Example 1: Create sample accounts"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Create Banking Accounts")
    print("="*60)
    
    import requests
    
    accounts = [
        {"holder": "Alice Johnson", "balance": 10000, "type": "savings"},
        {"holder": "Bob Smith", "balance": 5000, "type": "checking"},
        {"holder": "Carol Williams", "balance": 15000, "type": "money_market"},
    ]
    
    created_accounts = []
    
    for account in accounts:
        response = requests.post(
            'http://localhost:5000/api/accounts',
            json={
                'account_holder': account['holder'],
                'initial_balance': account['balance'],
                'account_type': account['type']
            }
        )
        
        if response.status_code == 201:
            data = response.json()
            created_accounts.append(data)
            print(f"✓ Created: {data['account_holder']} ({data['account_id']})")
            print(f"  Balance: ${data['balance']:,.2f}")
        else:
            print(f"✗ Failed to create account: {response.text}")
    
    return created_accounts


def example_2_transactions(accounts):
    """Example 2: Execute transactions and track metrics"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Execute Banking Transactions")
    print("="*60)
    
    import requests
    
    if len(accounts) < 2:
        print("Need at least 2 accounts")
        return
    
    # Transfer between accounts
    transfers = [
        {
            'from': accounts[0]['account_id'],
            'to': accounts[1]['account_id'],
            'amount': 500,
            'desc': 'Payment for consulting'
        },
        {
            'from': accounts[1]['account_id'],
            'to': accounts[2]['account_id'],
            'amount': 1000,
            'desc': 'Salary payment'
        },
        {
            'from': accounts[0]['account_id'],
            'to': accounts[2]['account_id'],
            'amount': 2000,
            'desc': 'Investment transfer'
        },
    ]
    
    for transfer in transfers:
        response = requests.post(
            'http://localhost:5000/api/transactions/transfer',
            json={
                'from_account': transfer['from'],
                'to_account': transfer['to'],
                'amount': transfer['amount'],
                'description': transfer['desc']
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Transfer: ${transfer['amount']:,.2f} - {data['status']}")
            print(f"  ID: {data['transaction_id']}")
        else:
            print(f"✗ Transfer failed: {response.text}")


def example_3_log_analysis():
    """Example 3: Analyze logs and detect patterns"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Log Analysis & Pattern Detection")
    print("="*60)
    
    from log_analysis.log_analyzer import LogAnalyzer
    
    # Create sample log data
    sample_logs = [
        "2024-01-19 10:00:45,123 - banking_app - INFO - Operation 'create_account' completed successfully",
        "2024-01-19 10:00:46,456 - banking_app - INFO - Operation 'transfer_funds' completed successfully",
        "2024-01-19 10:01:12,789 - banking_app - INFO - Operation 'transfer_funds' completed successfully",
        "2024-01-19 10:01:45,123 - banking_app - ERROR - Operation 'transfer_funds' failed",
        "2024-01-19 10:02:30,456 - banking_app - INFO - Operation 'get_balance' completed successfully",
    ]
    
    analyzer = LogAnalyzer()
    analyzer.load_logs(sample_logs)
    
    print(f"Total logs: {len(analyzer.entries)}")
    
    # Get error summary
    errors = analyzer.get_error_summary()
    print(f"Errors: {errors['total_errors']}")
    
    # Transaction analysis
    txn_stats = analyzer.analyze_transaction_patterns()
    print(f"\nTransactions:")
    print(f"  Count: {txn_stats['total_transactions']}")
    print(f"  Success rate: {txn_stats['success_rate']:.1%}")


def example_4_anomaly_detection():
    """Example 4: Detect anomalies in data"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Anomaly Detection")
    print("="*60)
    
    from analytics.anomaly_detector import AnomalyDetectionEngine
    
    engine = AnomalyDetectionEngine()
    
    # Simulate transaction amounts with an anomaly
    normal_amounts = [500, 520, 480, 510, 495, 505, 490, 515]
    anomaly_amount = [5000]  # Large outlier
    amounts = normal_amounts + anomaly_amount + [510, 500]
    
    print(f"Transaction amounts: {amounts}")
    
    # Detect anomalies
    anomalies = engine.detect_metric_anomalies(
        'transaction_amount',
        amounts
    )
    
    print(f"\nDetected {len(anomalies)} anomalies:")
    
    for anomaly in anomalies:
        print(f"\n✓ {anomaly.anomaly_type.value.upper()}")
        print(f"  Value: ${anomaly.value:,.2f}")
        print(f"  Expected: ${anomaly.expected_value:,.2f}")
        print(f"  Severity: {anomaly.severity}")
        print(f"  Description: {anomaly.description}")


def example_5_fraud_detection():
    """Example 5: Detect fraud patterns"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Fraud Pattern Detection")
    print("="*60)
    
    from analytics.anomaly_detector import ContextualAnomalyDetector
    from datetime import datetime, timedelta
    
    detector = ContextualAnomalyDetector()
    
    # Simulate rapid consecutive transactions (fraud pattern)
    now = datetime.now()
    suspicious_transactions = []
    
    for i in range(5):
        suspicious_transactions.append({
            'transaction_id': f'TXN-{i}',
            'from_account': 'ACC-FRAUD-TEST',
            'to_account': f'ACC-EXTERNAL-{i}',
            'amount': 1000 + (i * 100),
            'timestamp': (now + timedelta(seconds=i*20)).isoformat()
        })
    
    print(f"Simulating {len(suspicious_transactions)} rapid transactions...")
    
    # Detect fraud
    fraud_anomalies = detector.detect_fraud_patterns(suspicious_transactions)
    
    if fraud_anomalies:
        print(f"\n⚠️  FRAUD ALERT: {len(fraud_anomalies)} pattern(s) detected")
        for anomaly in fraud_anomalies:
            print(f"\n  Type: {anomaly.anomaly_type.value}")
            print(f"  Severity: {anomaly.severity}")
            print(f"  Description: {anomaly.description}")
            print(f"  Account: {anomaly.context.get('account_id')}")
    else:
        print("No fraud patterns detected")


def example_6_prometheus_metrics():
    """Example 6: View Prometheus metrics"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Prometheus Metrics")
    print("="*60)
    
    import requests
    
    try:
        response = requests.get('http://localhost:5000/metrics')
        metrics_lines = response.text.split('\n')
        
        # Show sample metrics
        active_metrics = [l for l in metrics_lines if l and not l.startswith('#')][:10]
        
        print(f"Total metric lines: {len(metrics_lines)}")
        print(f"\nSample metrics:")
        
        for metric in active_metrics:
            print(f"  {metric}")
            
    except Exception as e:
        print(f"Could not fetch metrics: {e}")
        print("Make sure the application is running on http://localhost:5000")


def example_7_time_series_analysis():
    """Example 7: Analyze time series trends"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Time Series Trend Analysis")
    print("="*60)
    
    from analytics.anomaly_detector import MovingAverageDetector, BehaviorAnalyzer
    
    # Simulate daily transaction counts over a month
    daily_transactions = [
        100, 105, 110, 108, 102,  # Week 1: Stable
        95, 90, 88, 85, 92,        # Week 2: Declining trend
        200, 205, 210, 220, 230,   # Week 3: SPIKE
        215, 210, 205, 200, 195,   # Week 4: High, stable
    ]
    
    print(f"Daily transactions (20 days): {daily_transactions}")
    
    # Detect trend changes
    ma_detector = MovingAverageDetector(window_size=5, sigma=2.0)
    ma_anomalies = ma_detector.detect(daily_transactions)
    
    print(f"\nMoving Average Anomalies: {len(ma_anomalies)} detected")
    for idx, deviation in ma_anomalies:
        print(f"  Day {idx}: Value={daily_transactions[idx]}, Deviation={deviation:.2f}")
    
    # Detect trend changes
    behavior = BehaviorAnalyzer()
    trend_changes = behavior.detect_trend_change(daily_transactions, window=5)
    
    print(f"\nTrend Changes: {len(trend_changes)} detected")
    for idx in trend_changes:
        print(f"  Day {idx}: Trend changed")
    
    # Detect level shifts
    level_shifts = behavior.detect_level_shift(daily_transactions, window=5, threshold=2.0)
    
    print(f"\nLevel Shifts: {len(level_shifts)} detected")
    for idx in level_shifts:
        print(f"  Day {idx}: Mean shifted significantly")


def example_8_comprehensive_report():
    """Example 8: Generate comprehensive monitoring report"""
    print("\n" + "="*60)
    print("EXAMPLE 8: Comprehensive Monitoring Report")
    print("="*60)
    
    import requests
    
    # Fetch health status
    try:
        health = requests.get('http://localhost:5000/api/health').json()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_health': health,
            'components': {
                'banking_app': 'healthy' if health['status'] == 'healthy' else 'degraded',
                'prometheus': 'checking...',
                'grafana': 'checking...',
                'log_analysis': 'ready'
            },
            'metrics': {
                'total_accounts': health.get('accounts_count', 0),
                'total_transactions': health.get('transactions_count', 0),
            }
        }
        
        print("\n📊 MONITORING REPORT")
        print(f"  Timestamp: {report['timestamp']}")
        print(f"  Status: {report['system_health']['status']}")
        print(f"  Accounts: {report['metrics']['total_accounts']}")
        print(f"  Transactions: {report['metrics']['total_transactions']}")
        
        print("\n🔧 Components:")
        for component, status in report['components'].items():
            emoji = "✓" if status == "healthy" else "⚠"
            print(f"  {emoji} {component}: {status}")
        
        print("\n📈 Next Steps:")
        print("  1. View Grafana Dashboard: http://localhost:3000")
        print("  2. Check Prometheus Metrics: http://localhost:9090")
        print("  3. Analyze Logs: http://localhost:5601")
        
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to application")
        print("  Make sure to run: docker-compose up -d")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("BANKING APPLICATION - MONITORING EXAMPLES")
    print("="*60)
    
    try:
        # Example 1: Create accounts
        accounts = example_1_create_accounts()
        
        # Example 2: Execute transactions
        if accounts:
            example_2_transactions(accounts)
        
        # Example 3: Log analysis
        example_3_log_analysis()
        
        # Example 4: Anomaly detection
        example_4_anomaly_detection()
        
        # Example 5: Fraud detection
        example_5_fraud_detection()
        
        # Example 6: Prometheus metrics
        example_6_prometheus_metrics()
        
        # Example 7: Time series analysis
        example_7_time_series_analysis()
        
        # Example 8: Comprehensive report
        example_8_comprehensive_report()
        
        print("\n" + "="*60)
        print("✓ ALL EXAMPLES COMPLETED")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Error running examples: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
