"""
Log Analysis Engine - Parse, process, and analyze banking application logs
Supports trend detection and anomaly analysis
"""

import json
import re
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict, Counter
import statistics

logger = logging.getLogger(__name__)


class LogEntry:
    """Structured log entry"""
    
    def __init__(self, raw_log: str):
        self.raw_log = raw_log
        self.timestamp: Optional[datetime] = None
        self.level: str = "UNKNOWN"
        self.component: str = "unknown"
        self.message: str = ""
        self.metadata: Dict[str, Any] = {}
        self.parse()
    
    def parse(self):
        """Parse raw log string into structured components"""
        # Example format: 2024-01-19 10:30:45,123 - banking_app - INFO - Operation complete
        pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),(\d+) - ([\w_.]+) - (\w+) - (.*)'
        match = re.match(pattern, self.raw_log)
        
        if match:
            timestamp_str, ms, component, level, message = match.groups()
            try:
                self.timestamp = datetime.strptime(f"{timestamp_str}.{ms}", "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                self.timestamp = datetime.now()
            
            self.component = component
            self.level = level.upper()
            self.message = message
            
            # Extract JSON metadata if present
            try:
                if '{' in message and '}' in message:
                    json_part = message[message.find('{'):message.rfind('}')+1]
                    self.metadata = json.loads(json_part)
            except (json.JSONDecodeError, ValueError):
                pass
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'level': self.level,
            'component': self.component,
            'message': self.message,
            'metadata': self.metadata
        }


class LogAnalyzer:
    """Analyze logs for patterns, trends, and anomalies"""
    
    def __init__(self):
        self.entries: List[LogEntry] = []
        self.error_patterns: Dict[str, int] = defaultdict(int)
        self.transaction_stats: Dict[str, Any] = {}
    
    def load_logs(self, log_lines: List[str]):
        """Load raw logs"""
        for line in log_lines:
            if line.strip():
                entry = LogEntry(line.strip())
                self.entries.append(entry)
        
        logger.info(f"Loaded {len(self.entries)} log entries")
    
    def load_logs_from_file(self, filepath: str):
        """Load logs from file"""
        try:
            with open(filepath, 'r') as f:
                self.load_logs(f.readlines())
        except IOError as e:
            logger.error(f"Error reading log file: {e}")
    
    def get_entries_by_level(self, level: str) -> List[LogEntry]:
        """Filter logs by level"""
        return [e for e in self.entries if e.level == level.upper()]
    
    def get_entries_by_timerange(self, start: datetime, end: datetime) -> List[LogEntry]:
        """Get logs within time range"""
        return [
            e for e in self.entries 
            if e.timestamp and start <= e.timestamp <= end
        ]
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get error summary"""
        errors = self.get_entries_by_level('ERROR')
        
        error_types = defaultdict(int)
        for error in errors:
            # Extract error type from message
            if 'error_type' in error.metadata:
                error_types[error.metadata['error_type']] += 1
            else:
                # Try to extract from message
                match = re.search(r'(\w+Error|\w+Exception)', error.message)
                if match:
                    error_types[match.group(1)] += 1
                else:
                    error_types['Unknown'] += 1
        
        return {
            'total_errors': len(errors),
            'error_breakdown': dict(error_types),
            'first_error': errors[0].timestamp.isoformat() if errors else None,
            'last_error': errors[-1].timestamp.isoformat() if errors else None
        }
    
    def analyze_transaction_patterns(self) -> Dict[str, Any]:
        """Analyze transaction-related logs"""
        transaction_logs = [
            e for e in self.entries 
            if 'transaction' in e.message.lower()
        ]
        
        transaction_types = defaultdict(int)
        amounts = []
        durations = []
        success_count = 0
        fail_count = 0
        
        for log in transaction_logs:
            if 'type' in log.metadata:
                transaction_types[log.metadata['type']] += 1
            
            if 'amount' in log.metadata:
                amounts.append(float(log.metadata['amount']))
            
            if 'duration_ms' in log.metadata:
                durations.append(log.metadata['duration_ms'])
            
            if 'status' in log.metadata:
                if log.metadata['status'] == 'success':
                    success_count += 1
                else:
                    fail_count += 1
        
        return {
            'total_transactions': len(transaction_logs),
            'by_type': dict(transaction_types),
            'success_count': success_count,
            'failure_count': fail_count,
            'success_rate': success_count / len(transaction_logs) if transaction_logs else 0,
            'amount_stats': self._get_stats(amounts),
            'duration_stats': self._get_stats(durations)
        }
    
    def analyze_user_activity(self) -> Dict[str, Any]:
        """Analyze user activity patterns"""
        user_activities = defaultdict(list)
        user_errors = defaultdict(int)
        
        for entry in self.entries:
            user_id = entry.metadata.get('user', 'unknown')
            
            if entry.level in ('ERROR', 'WARNING'):
                user_errors[user_id] += 1
            
            if entry.timestamp:
                user_activities[user_id].append(entry.timestamp)
        
        # Calculate activity metrics per user
        user_stats = {}
        for user_id, timestamps in user_activities.items():
            if timestamps:
                user_stats[user_id] = {
                    'activity_count': len(timestamps),
                    'error_count': user_errors[user_id],
                    'first_activity': min(timestamps).isoformat(),
                    'last_activity': max(timestamps).isoformat(),
                    'avg_gap_minutes': self._calculate_avg_gap(timestamps)
                }
        
        return {
            'total_users': len(user_stats),
            'user_stats': user_stats,
            'most_active_users': sorted(
                user_stats.items(),
                key=lambda x: x[1]['activity_count'],
                reverse=True
            )[:5]
        }
    
    def detect_anomalies(self) -> Dict[str, Any]:
        """Detect anomalous patterns in logs"""
        anomalies = {
            'error_rate_spikes': [],
            'unusual_response_times': [],
            'suspicious_accounts': [],
            'rate_anomalies': [],
            'pattern_violations': []
        }
        
        # 1. Error rate spikes
        hourly_errors = self._group_by_hour()
        error_rate_threshold = self._calculate_threshold(hourly_errors.values())
        
        for hour, count in hourly_errors.items():
            if count > error_rate_threshold:
                anomalies['error_rate_spikes'].append({
                    'hour': hour,
                    'error_count': count,
                    'threshold': error_rate_threshold
                })
        
        # 2. Unusual response times
        durations = [
            e.metadata.get('duration_ms', 0) 
            for e in self.entries 
            if 'duration_ms' in e.metadata
        ]
        
        if durations:
            mean_duration = statistics.mean(durations)
            std_duration = statistics.stdev(durations) if len(durations) > 1 else 0
            threshold = mean_duration + (2 * std_duration)
            
            slow_requests = [d for d in durations if d > threshold]
            if slow_requests:
                anomalies['unusual_response_times'].append({
                    'count': len(slow_requests),
                    'threshold_ms': threshold,
                    'max_duration_ms': max(slow_requests)
                })
        
        # 3. Suspicious account activity
        account_errors = defaultdict(int)
        for entry in self.entries:
            if entry.level == 'ERROR' and 'account_id' in entry.metadata:
                account_errors[entry.metadata['account_id']] += 1
        
        avg_account_errors = statistics.mean(account_errors.values()) if account_errors else 0
        std_account_errors = statistics.stdev(account_errors.values()) if len(account_errors) > 1 else 0
        
        for account_id, error_count in account_errors.items():
            if error_count > avg_account_errors + (2 * std_account_errors):
                anomalies['suspicious_accounts'].append({
                    'account_id': account_id,
                    'error_count': error_count,
                    'average': avg_account_errors
                })
        
        return anomalies
    
    def detect_trends(self, window_hours: int = 24) -> Dict[str, Any]:
        """Detect trends over time"""
        now = datetime.now()
        past = now - timedelta(hours=window_hours)
        
        recent_entries = self.get_entries_by_timerange(past, now)
        
        trends = {
            'error_trend': self._calculate_trend(recent_entries, 'ERROR'),
            'warning_trend': self._calculate_trend(recent_entries, 'WARNING'),
            'transaction_trend': self._calculate_transaction_trend(recent_entries),
            'performance_trend': self._calculate_performance_trend(recent_entries)
        }
        
        return trends
    
    # ========== Helper Methods ==========
    
    @staticmethod
    def _get_stats(values: List[float]) -> Dict[str, float]:
        """Calculate statistics for a list"""
        if not values:
            return {}
        
        return {
            'count': len(values),
            'min': min(values),
            'max': max(values),
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'stdev': statistics.stdev(values) if len(values) > 1 else 0,
            'sum': sum(values)
        }
    
    def _group_by_hour(self) -> Dict[str, int]:
        """Group error entries by hour"""
        hourly = defaultdict(int)
        
        for entry in self.get_entries_by_level('ERROR'):
            if entry.timestamp:
                hour_key = entry.timestamp.strftime('%Y-%m-%d %H:00')
                hourly[hour_key] += 1
        
        return hourly
    
    @staticmethod
    def _calculate_threshold(values) -> float:
        """Calculate anomaly threshold using mean + 2*stdev"""
        values_list = list(values)
        if not values_list:
            return 0
        
        mean = statistics.mean(values_list)
        std = statistics.stdev(values_list) if len(values_list) > 1 else 0
        return mean + (2 * std)
    
    @staticmethod
    def _calculate_avg_gap(timestamps: List[datetime]) -> float:
        """Calculate average gap between timestamps"""
        if len(timestamps) < 2:
            return 0
        
        timestamps = sorted(timestamps)
        gaps = [
            (timestamps[i+1] - timestamps[i]).total_seconds() / 60 
            for i in range(len(timestamps) - 1)
        ]
        return statistics.mean(gaps) if gaps else 0
    
    def _calculate_trend(self, entries: List[LogEntry], level: str) -> Dict[str, Any]:
        """Calculate trend for a log level"""
        entries = [e for e in entries if e.level == level]
        
        if not entries:
            return {'count': 0, 'trend': 'stable'}
        
        # Split into two halves
        mid = len(entries) // 2
        first_half = len([e for e in entries[:mid] if e.level == level])
        second_half = len([e for e in entries[mid:] if e.level == level])
        
        trend = 'increasing' if second_half > first_half else ('decreasing' if second_half < first_half else 'stable')
        
        return {
            'count': len(entries),
            'trend': trend,
            'first_half': first_half,
            'second_half': second_half,
            'change_percent': ((second_half - first_half) / first_half * 100) if first_half > 0 else 0
        }
    
    def _calculate_transaction_trend(self, entries: List[LogEntry]) -> Dict[str, Any]:
        """Calculate transaction trend"""
        txn_entries = [e for e in entries if 'transaction' in e.message.lower()]
        
        if not txn_entries:
            return {'count': 0}
        
        total_amount = sum(
            float(e.metadata.get('amount', 0)) 
            for e in txn_entries 
            if 'amount' in e.metadata
        )
        
        return {
            'count': len(txn_entries),
            'total_amount': total_amount,
            'avg_transaction': total_amount / len(txn_entries) if txn_entries else 0
        }
    
    def _calculate_performance_trend(self, entries: List[LogEntry]) -> Dict[str, Any]:
        """Calculate performance trend"""
        durations = [
            e.metadata.get('duration_ms', 0) 
            for e in entries 
            if 'duration_ms' in e.metadata and e.metadata.get('duration_ms')
        ]
        
        if not durations:
            return {}
        
        return self._get_stats(durations)
