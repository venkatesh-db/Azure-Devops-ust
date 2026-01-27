# Banking Application Monitoring with Azure & Prometheus

A comprehensive, production-ready learning project demonstrating:
- **Azure Monitor & Application Insights** integration
- **Prometheus** metrics collection
- **Grafana** visualization
- **Python** log analysis and anomaly detection
- **Banking domain** business logic

## 🏗️ Project Structure

```
banking-monitoring/
├── src/
│   ├── app/
│   │   └── banking_app.py          # Flask app with App Insights
│   ├── metrics/
│   │   └── prometheus_exporter.py  # Prometheus metrics
│   ├── analytics/
│   │   └── anomaly_detector.py     # ML-based anomaly detection
│   └── log_analysis/
│       └── log_analyzer.py         # Log parsing & trend detection
├── azure/
│   └── kql_queries.kusto           # Log Analytics KQL queries
├── grafana/
│   └── dashboard.json              # Pre-built dashboards
├── docker/
│   ├── docker-compose.yml          # Full stack deployment
│   ├── Dockerfile.app              # Application container
│   ├── prometheus.yml              # Prometheus config
│   └── alert_rules.yml             # Alert definitions
├── docs/
│   ├── SETUP.md                    # Setup instructions
│   ├── API.md                      # API documentation
│   ├── MONITORING.md               # Monitoring guide
│   └── ANOMALY_DETECTION.md        # Anomaly detection guide
└── requirements.txt                # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Azure subscription (optional, for cloud deployment)
- Git

### 1. Clone and Setup

```bash
cd banking-monitoring
pip install -r requirements.txt
```

### 2. Configure Azure (Optional)

```bash
export APPINSIGHTS_INSTRUMENTATION_KEY="your-key-here"
export APPLICATIONINSIGHTS_CONNECTION_STRING="InstrumentationKey=..."
```

### 3. Start the Stack

```bash
cd docker
docker-compose up -d
```

### 4. Access Services

- **Banking App**: http://localhost:5000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **Kibana**: http://localhost:5601
- **Pushgateway**: http://localhost:9091

## 📚 Learning Path

### Phase 1: Understand the Banking Application
1. Review [banking_app.py](src/app/banking_app.py)
2. Focus on:
   - Track performance decorator
   - Custom metric tracking
   - Error handling & logging
3. Test endpoints:
   ```bash
   curl -X POST http://localhost:5000/api/accounts \
     -H "Content-Type: application/json" \
     -d '{"account_holder": "John Doe", "initial_balance": 5000}'
   ```

### Phase 2: Metrics Collection (Prometheus)
1. Study [prometheus_exporter.py](src/metrics/prometheus_exporter.py)
2. Key concepts:
   - **Counters**: Total count (transactions, errors)
   - **Gauges**: Current value (balance, active users)
   - **Histograms**: Distribution (latency, amounts)
   - **Custom metrics**: Business KPIs
3. View metrics:
   ```bash
   curl http://localhost:5000/metrics
   ```

### Phase 3: Log Analysis with Python
1. Study [log_analyzer.py](src/log_analysis/log_analyzer.py)
2. Capabilities:
   - Parse structured logs
   - Extract patterns
   - Calculate statistics
   - Identify trends
3. Example usage:
   ```python
   from log_analysis.log_analyzer import LogAnalyzer
   
   analyzer = LogAnalyzer()
   analyzer.load_logs_from_file('app.log')
   
   # Get transaction patterns
   patterns = analyzer.analyze_transaction_patterns()
   print(f"Success rate: {patterns['success_rate']:.2%}")
   
   # Detect anomalies
   anomalies = analyzer.detect_anomalies()
   ```

### Phase 4: Anomaly Detection
1. Study [anomaly_detector.py](src/analytics/anomaly_detector.py)
2. Techniques:
   - **Z-Score**: Detect outliers
   - **IQR**: Box-plot method
   - **Moving Average**: Trend deviations
   - **Seasonality**: Pattern violations
   - **Behavioral**: Fraud patterns
3. Example usage:
   ```python
   from analytics.anomaly_detector import AnomalyDetectionEngine
   
   engine = AnomalyDetectionEngine()
   
   # Detect metric anomalies
   anomalies = engine.detect_metric_anomalies(
       'transaction_amount',
       [100, 105, 110, 150, 600, 120, 115]
   )
   
   # Detect transaction anomalies
   transaction_anomalies = engine.detect_all_anomalies(
       metrics_data={'amounts': amounts},
       transaction_data=transactions
   )
   ```

### Phase 5: Azure Log Analytics
1. Review [kql_queries.kusto](azure/kql_queries.kusto)
2. Key query patterns:
   - Transaction analysis
   - Error investigation
   - User activity tracking
   - Performance monitoring
   - Anomaly detection
   - Compliance auditing
3. Deploy to Azure:
   ```bash
   # Create Log Analytics Workspace
   az resource create \
     --resource-group myGroup \
     --name myWorkspace \
     --resource-type "Microsoft.OperationalInsights/workspaces"
   ```

### Phase 6: Visualization (Grafana)
1. Dashboard: [dashboard.json](grafana/dashboard.json)
2. Panels included:
   - Transaction breakdown
   - Success rate gauge
   - Throughput over time
   - API latency percentiles
   - Error trends
   - Network metrics
3. Import to Grafana:
   - Settings → Data Sources → Add Prometheus
   - Dashboards → Import → Upload JSON

## 🎓 Key Concepts

### Application Insights Integration
```python
from applicationinsights import TelemetryClient

tc = TelemetryClient(instrumentation_key)

# Track events
tc.track_event('transfer_completed', {
    'from_account': account_id,
    'amount': amount
})

# Track exceptions
tc.track_exception()

# Custom metrics
tc.track_metric('transaction_duration', duration_ms)
```

### Prometheus Metrics
```python
from prometheus_client import Counter, Gauge, Histogram

# Counter: Only increases
transaction_counter = Counter(
    'banking_transactions_total',
    'Total transactions',
    ['type', 'status']
)

# Gauge: Can go up or down
active_users = Gauge('banking_active_users', 'Active users')

# Histogram: Tracks distribution
latency = Histogram('banking_latency_seconds', 'Request latency')
```

### Log Analysis Pattern
```python
# 1. Parse logs
analyzer.load_logs(log_lines)

# 2. Filter by criteria
errors = analyzer.get_entries_by_level('ERROR')

# 3. Analyze patterns
patterns = analyzer.analyze_transaction_patterns()

# 4. Detect anomalies
anomalies = analyzer.detect_anomalies()

# 5. Identify trends
trends = analyzer.detect_trends(window_hours=24)
```

### Anomaly Detection Methods

| Method | Use Case | Parameters |
|--------|----------|-----------|
| Z-Score | Outliers | threshold (2.5-3.0) |
| IQR | Box plot | multiplier (1.5) |
| Moving Avg | Trends | window_size (7-30) |
| Seasonality | Patterns | period (hourly=24) |
| Contextual | Domain logic | Custom rules |

## 🔍 Banking Domain Examples

### Transaction Processing
```bash
# Create account
curl -X POST http://localhost:5000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "account_holder": "Jane Doe",
    "initial_balance": 10000,
    "account_type": "savings"
  }'

# Transfer funds
curl -X POST http://localhost:5000/api/transactions/transfer \
  -H "Content-Type: application/json" \
  -d '{
    "from_account": "ACC-xxxxx",
    "to_account": "ACC-yyyyy",
    "amount": 500,
    "description": "Payment for services"
  }'

# Get transaction history
curl http://localhost:5000/api/transactions?account_id=ACC-xxxxx
```

### Metrics Tracked
- Transaction count by type
- Transaction success rate
- Average transaction amount
- Transaction processing time
- Account balance distribution
- User activity per hour
- Error rates by type
- API response times

### Anomalies Detected
- **Large transactions** (> 3σ from mean)
- **Rapid consecutive** transfers (fraud pattern)
- **High error rates** (spike detection)
- **Unusual latencies** (performance)
- **Accounts with issues** (support priority)
- **Seasonal deviations** (pattern violations)

## 📊 KQL Queries Examples

### Get recent transactions
```kusto
traces
| where customDimensions.operation == "transfer_funds"
| where timestamp > ago(1h)
| project timestamp, amount, from_account, to_account
| order by timestamp desc
```

### Fraud pattern detection
```kusto
let transaction_times = traces
| where customDimensions.operation contains "transfer"
| project timestamp, user_id = customDimensions.user;
transaction_times
| extend prev_time = prev(timestamp, 1)
| where (timestamp - prev_time) < 1m
| summarize rapid_txn_count = count() by user_id
| where rapid_txn_count > 5
```

## 🛡️ Production Deployment

### To Azure Container Instances
```bash
az container create \
  --resource-group myGroup \
  --name banking-app \
  --image myregistry.azurecr.io/banking-app:latest \
  --cpu 2 --memory 4 \
  --environment-variables \
    APPINSIGHTS_INSTRUMENTATION_KEY=$KEY \
  --ports 5000
```

### To Azure App Service
```bash
az webapp create \
  --resource-group myGroup \
  --plan myPlan \
  --name banking-app
```

## 🔧 Troubleshooting

### Application Insights not receiving data
```bash
# Check connection
curl -v http://localhost:5000/api/health

# Verify key format
echo $APPINSIGHTS_INSTRUMENTATION_KEY

# Check logs
docker logs banking-app
```

### Prometheus not scraping metrics
```bash
# Verify endpoint
curl http://localhost:5000/metrics

# Check Prometheus config
docker exec prometheus cat /etc/prometheus/prometheus.yml

# View targets in Prometheus UI
# http://localhost:9090/targets
```

### Grafana datasource issues
```bash
# Restart Grafana
docker restart grafana

# Check datasource URL
# http://prometheus:9090 (internal docker network)
```

## 📈 Performance Tuning

### Application
- Use connection pooling
- Implement caching
- Batch database operations
- Optimize query patterns

### Metrics Collection
- Reduce sample rate for high-volume metrics
- Use appropriate bucket sizes
- Archive old data

### Log Analysis
- Process logs in batches
- Use streaming for large datasets
- Archive historical logs

## 🎯 Next Steps

1. **Integrate with Azure**: Deploy to Azure App Service/Container Instances
2. **Add Authentication**: Implement OAuth2/Azure AD
3. **Scale Out**: Use load balancers and multiple instances
4. **Advanced Analytics**: Add ML models for fraud detection
5. **Automation**: Create alert remediation workflows
6. **Integration**: Connect to incident management systems

## 📝 Additional Resources

- [Azure Monitor Documentation](https://learn.microsoft.com/en-us/azure/azure-monitor/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [Grafana Documentation](https://grafana.com/docs/)
- [KQL Query Language](https://learn.microsoft.com/en-us/kusto/query/)
- [Python logging](https://docs.python.org/3/library/logging.html)

## 📞 Support

For questions or issues, refer to:
- Individual module documentation in `docs/`
- Code comments in source files
- Inline examples in this README

---

**Created**: January 2024
**License**: MIT
**Author**: Devops-GenAI Learning Series

# Banking Monitoring Project

## Overview
This project is designed to monitor banking operations, analyze logs, and export metrics using Prometheus. It includes the following components:

- **Banking App**: A Flask-based application.
- **Log Analysis**: A script to analyze logs.
- **Prometheus Exporter**: A script to export metrics to Prometheus.

## Prerequisites

1. Python 3.14 or higher.
2. Virtual environment setup.
3. Required Python packages installed.
4. Docker (if using Dockerized setup).

## Setup Instructions

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd BankingProjects/datadriven/banking-monitoring
```

### Step 2: Set Up Python Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Banking App
```bash
python src/app/banking_app.py
```
The app will start running on `http://127.0.0.1:5000`.

### Step 5: Run the Log Analysis Script
```bash
python src/log_analysis/log_analyzer.py
```
This script will analyze logs and output the results in the terminal.

### Step 6: Run the Prometheus Exporter
```bash
python src/metrics/prometheus_exporter.py
```
This script will export metrics to Prometheus.

## Dockerized Setup (Optional)

### Step 1: Build the Docker Image
```bash
docker-compose build
```

### Step 2: Start the Services
```bash
docker-compose up
```

### Step 3: Access the Services
- Banking App: `http://127.0.0.1:5000`
- Prometheus: `http://127.0.0.1:9090`
- Grafana: `http://127.0.0.1:3000`

## Output Verification

1. **Banking App**: Open the browser and navigate to `http://127.0.0.1:5000` to interact with the app.
2. **Log Analysis**: Check the terminal for log analysis results.
3. **Prometheus Exporter**: Verify metrics in Prometheus at `http://127.0.0.1:9090`.

## Troubleshooting

- Ensure all dependencies are installed.
- Check if the virtual environment is activated.
- Verify Docker is running (if using Dockerized setup).

## License
This project is licensed under the MIT License.
