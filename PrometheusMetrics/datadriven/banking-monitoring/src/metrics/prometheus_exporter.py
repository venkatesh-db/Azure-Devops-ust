"""
Prometheus Metrics Exporter for Banking Application
Exports custom metrics for transactions, accounts, and system health
"""

import os
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Any
from enum import Enum

from prometheus_client import Counter, Gauge, Histogram, Enum as PrometheusEnum
from prometheus_client import CollectorRegistry, generate_latest

logger = logging.getLogger(__name__)


class MetricsNamespace(Enum):
    """Metric namespaces"""
    BANKING = "banking"
    SYSTEM = "system"
    NETWORK = "network"


class BankingMetrics:
    """Banking domain metrics collection"""
    
    def __init__(self, registry: CollectorRegistry = None):
        """Initialize metrics with custom registry"""
        self.registry = registry or CollectorRegistry()
        self._setup_metrics()
    
    def _setup_metrics(self):
        """Setup all Prometheus metrics"""
        
        # ====== Transaction Metrics ======
        self.transactions_total = Counter(
            'banking_transactions_total',
            'Total number of transactions processed',
            ['type', 'status'],
            registry=self.registry
        )
        
        self.transaction_amount_total = Counter(
            'banking_transaction_amount_total',
            'Total amount of transactions in USD',
            ['type'],
            registry=self.registry
        )
        
        self.transaction_duration_seconds = Histogram(
            'banking_transaction_duration_seconds',
            'Transaction processing duration in seconds',
            ['type'],
            buckets=(0.1, 0.5, 1.0, 2.5, 5.0, 10.0),
            registry=self.registry
        )
        
        # ====== Account Metrics ======
        self.accounts_total = Gauge(
            'banking_accounts_total',
            'Total number of active accounts',
            ['account_type'],
            registry=self.registry
        )
        
        self.account_balance_total = Gauge(
            'banking_account_balance_total',
            'Total balance across all accounts in USD',
            ['account_type'],
            registry=self.registry
        )
        
        # ====== Error Metrics ======
        self.transaction_errors_total = Counter(
            'banking_transaction_errors_total',
            'Total number of failed transactions',
            ['error_type'],
            registry=self.registry
        )
        
        self.validation_errors_total = Counter(
            'banking_validation_errors_total',
            'Total validation errors',
            ['field'],
            registry=self.registry
        )
        
        # ====== User Activity Metrics ======
        self.active_users_gauge = Gauge(
            'banking_active_users',
            'Number of active users',
            registry=self.registry
        )
        
        self.user_sessions_total = Counter(
            'banking_user_sessions_total',
            'Total user sessions',
            ['session_status'],
            registry=self.registry
        )
        
        # ====== System Metrics ======
        self.api_requests_total = Counter(
            'banking_api_requests_total',
            'Total API requests',
            ['method', 'endpoint', 'status'],
            registry=self.registry
        )
        
        self.api_request_duration_seconds = Histogram(
            'banking_api_request_duration_seconds',
            'API request duration in seconds',
            ['method', 'endpoint'],
            buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 5.0),
            registry=self.registry
        )
        
        self.request_queue_length = Gauge(
            'banking_request_queue_length',
            'Current request queue length',
            registry=self.registry
        )
        
        # ====== Financial Risk Metrics ======
        self.large_transaction_count = Counter(
            'banking_large_transactions_total',
            'Transactions above threshold',
            ['threshold_level'],
            registry=self.registry
        )
        
        self.fraud_risk_score = Gauge(
            'banking_fraud_risk_score',
            'Current fraud risk score (0-1)',
            registry=self.registry
        )
        
        self.account_lockout_count = Counter(
            'banking_account_lockouts_total',
            'Number of locked accounts',
            ['reason'],
            registry=self.registry
        )
        
        # ====== Database Metrics ======
        self.database_query_duration_seconds = Histogram(
            'banking_database_query_duration_seconds',
            'Database query duration in seconds',
            ['query_type'],
            buckets=(0.001, 0.005, 0.01, 0.05, 0.1),
            registry=self.registry
        )
        
        self.database_connection_pool = Gauge(
            'banking_database_connections_active',
            'Active database connections',
            registry=self.registry
        )


class SystemMetrics:
    """System-level metrics (CPU, Memory, Network)"""
    
    def __init__(self, registry: CollectorRegistry = None):
        """Initialize system metrics"""
        self.registry = registry or CollectorRegistry()
        self._setup_metrics()
    
    def _setup_metrics(self):
        """Setup system metrics"""
        
        # ====== CPU Metrics ======
        self.cpu_usage_percent = Gauge(
            'system_cpu_usage_percent',
            'CPU usage percentage',
            ['core'],
            registry=self.registry
        )
        
        self.cpu_temperature_celsius = Gauge(
            'system_cpu_temperature_celsius',
            'CPU temperature in Celsius',
            registry=self.registry
        )
        
        # ====== Memory Metrics ======
        self.memory_usage_bytes = Gauge(
            'system_memory_usage_bytes',
            'Memory usage in bytes',
            ['type'],
            registry=self.registry
        )
        
        self.memory_usage_percent = Gauge(
            'system_memory_usage_percent',
            'Memory usage percentage',
            registry=self.registry
        )
        
        # ====== Disk Metrics ======
        self.disk_usage_bytes = Gauge(
            'system_disk_usage_bytes',
            'Disk usage in bytes',
            ['mount_point'],
            registry=self.registry
        )
        
        self.disk_iops = Gauge(
            'system_disk_iops',
            'Disk I/O operations per second',
            ['operation'],
            registry=self.registry
        )
        
        # ====== Network Metrics ======
        self.network_bytes_sent_total = Counter(
            'system_network_bytes_sent_total',
            'Total bytes sent',
            ['interface'],
            registry=self.registry
        )
        
        self.network_bytes_received_total = Counter(
            'system_network_bytes_received_total',
            'Total bytes received',
            ['interface'],
            registry=self.registry
        )
        
        self.network_connections_active = Gauge(
            'system_network_connections_active',
            'Active network connections',
            ['state'],
            registry=self.registry
        )
        
        self.network_packet_loss_percent = Gauge(
            'system_network_packet_loss_percent',
            'Network packet loss percentage',
            registry=self.registry
        )
        
        # ====== Process Metrics ======
        self.process_uptime_seconds = Gauge(
            'system_process_uptime_seconds',
            'Process uptime in seconds',
            registry=self.registry
        )
        
        self.process_threads_count = Gauge(
            'system_process_threads_count',
            'Number of process threads',
            registry=self.registry
        )


class MetricsCollector:
    """Centralized metrics collection and export"""

    def __init__(self):
        """Initialize collector with multiple metric types"""
        self.banking_metrics = BankingMetrics()
        self.system_metrics = SystemMetrics()
        self.start_time = time.time()

    def record_transaction(self, transaction_type: str, amount: float, 
                          duration: float, status: str = 'success'):
        """Record a transaction metric"""
        self.banking_metrics.transactions_total.labels(
            type=transaction_type,
            status=status
        ).inc()
        
        self.banking_metrics.transaction_amount_total.labels(
            type=transaction_type
        ).inc(amount)
        
        self.banking_metrics.transaction_duration_seconds.labels(
            type=transaction_type
        ).observe(duration)

    def record_account_stats(self, account_stats: Dict[str, Any]):
        """Record account-level statistics"""
        for account_type, count in account_stats.get('by_type', {}).items():
            self.banking_metrics.accounts_total.labels(
                account_type=account_type
            ).set(count)
        
        for account_type, balance in account_stats.get('balance_by_type', {}).items():
            self.banking_metrics.account_balance_total.labels(
                account_type=account_type
            ).set(balance)

    def record_error(self, error_type: str):
        """Record an error occurrence"""
        self.banking_metrics.transaction_errors_total.labels(
            error_type=error_type
        ).inc()

    def record_validation_error(self, field: str):
        """Record validation error for a field"""
        self.banking_metrics.validation_errors_total.labels(
            field=field
        ).inc()

    def record_api_request(self, method: str, endpoint: str, 
                          duration: float, status: int):
        """Record API request metrics"""
        status_category = f"{status // 100}xx"
        
        self.banking_metrics.api_requests_total.labels(
            method=method,
            endpoint=endpoint,
            status=status_category
        ).inc()
        
        self.banking_metrics.api_request_duration_seconds.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)

    def set_active_users(self, count: int):
        """Set active user count"""
        self.banking_metrics.active_users_gauge.set(count)

    def record_session(self, status: str):
        """Record user session"""
        self.banking_metrics.user_sessions_total.labels(
            session_status=status
        ).inc()

    def record_large_transaction(self, threshold_level: str):
        """Record large transaction"""
        self.banking_metrics.large_transaction_count.labels(
            threshold_level=threshold_level
        ).inc()

    def set_fraud_risk_score(self, score: float):
        """Set fraud risk score (0-1)"""
        self.banking_metrics.fraud_risk_score.set(max(0, min(1, score)))

    def record_account_lockout(self, reason: str):
        """Record account lockout"""
        self.banking_metrics.account_lockout_count.labels(
            reason=reason
        ).inc()

    def set_system_cpu_usage(self, core: str, usage_percent: float):
        """Set CPU usage for a core"""
        self.system_metrics.cpu_usage_percent.labels(core=core).set(usage_percent)

    def set_system_memory_usage(self, memory_type: str, usage_bytes: int):
        """Set memory usage"""
        self.system_metrics.memory_usage_bytes.labels(type=memory_type).set(usage_bytes)

    def set_system_memory_percent(self, percent: float):
        """Set memory usage percentage"""
        self.system_metrics.memory_usage_percent.set(percent)

    def record_network_bytes(self, interface: str, bytes_sent: int, bytes_received: int):
        """Record network metrics"""
        self.system_metrics.network_bytes_sent_total.labels(
            interface=interface
        ).inc(bytes_sent)
        
        self.system_metrics.network_bytes_received_total.labels(
            interface=interface
        ).inc(bytes_received)

    def set_network_connections(self, state: str, count: int):
        """Set active network connections"""
        self.system_metrics.network_connections_active.labels(state=state).set(count)

    def get_metrics_output(self) -> bytes:
        """Get all metrics in Prometheus text format"""
        # Combine registries (workaround for multiple registries)
        metrics = []
        metrics.append(generate_latest(self.banking_metrics.registry).decode('utf-8'))
        metrics.append(generate_latest(self.system_metrics.registry).decode('utf-8'))
        
        return '\n'.join(metrics).encode('utf-8')


# Global collector instance
metrics_collector = MetricsCollector()


def get_metrics() -> bytes:
    """Get all metrics for Prometheus scraping"""
    return metrics_collector.get_metrics_output()
