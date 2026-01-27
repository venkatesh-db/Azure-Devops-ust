"""
Anomaly Detection Engine
Advanced statistical and ML-based anomaly detection for banking metrics
"""

import numpy as np
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum
import statistics

logger = logging.getLogger(__name__)


class AnomalyType(Enum):
    """Types of anomalies detected"""
    STATISTICAL = "statistical"
    BEHAVIORAL = "behavioral"
    SEASONAL = "seasonal"
    CONTEXTUAL = "contextual"


@dataclass
class Anomaly:
    """Represents a detected anomaly"""
    timestamp: datetime
    metric_name: str
    value: float
    expected_value: float
    anomaly_type: AnomalyType
    severity: str  # low, medium, high, critical
    description: str
    context: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp.isoformat(),
            'metric': self.metric_name,
            'value': self.value,
            'expected': self.expected_value,
            'type': self.anomaly_type.value,
            'severity': self.severity,
            'description': self.description,
            'context': self.context
        }


class ZScoreDetector:
    """Z-Score based anomaly detection"""
    
    def __init__(self, threshold: float = 2.5):
        """
        Initialize with z-score threshold.
        threshold=2.5 means values beyond 2.5 standard deviations are anomalies
        """
        self.threshold = threshold
    
    def detect(self, values: List[float], labels: List[str] = None) -> List[Tuple[int, float]]:
        """
        Detect anomalies using z-score
        Returns list of (index, z_score) for anomalous values
        """
        if len(values) < 2:
            return []
        
        mean = statistics.mean(values)
        stdev = statistics.stdev(values)
        
        if stdev == 0:
            return []
        
        anomalies = []
        for i, value in enumerate(values):
            z_score = abs((value - mean) / stdev)
            if z_score > self.threshold:
                anomalies.append((i, z_score))
        
        return anomalies


class IQRDetector:
    """Interquartile Range based anomaly detection"""
    
    def __init__(self, multiplier: float = 1.5):
        """
        Initialize with IQR multiplier
        multiplier=1.5 is standard for box plot whiskers
        """
        self.multiplier = multiplier
    
    def detect(self, values: List[float]) -> List[Tuple[int, str]]:
        """
        Detect outliers using IQR method
        Returns list of (index, outlier_type)
        """
        if len(values) < 4:
            return []
        
        sorted_values = sorted(values)
        q1 = statistics.quantiles(sorted_values, n=4)[0]
        q3 = statistics.quantiles(sorted_values, n=4)[2]
        iqr = q3 - q1
        
        lower_bound = q1 - self.multiplier * iqr
        upper_bound = q3 + self.multiplier * iqr
        
        anomalies = []
        for i, value in enumerate(values):
            if value < lower_bound:
                anomalies.append((i, 'low_outlier'))
            elif value > upper_bound:
                anomalies.append((i, 'high_outlier'))
        
        return anomalies


class MovingAverageDetector:
    """Moving Average based anomaly detection"""
    
    def __init__(self, window_size: int = 7, sigma: float = 2.0):
        """
        Initialize with window size and standard deviation multiplier
        """
        self.window_size = window_size
        self.sigma = sigma
    
    def detect(self, values: List[float]) -> List[Tuple[int, float]]:
        """
        Detect anomalies by comparing value to moving average
        Returns list of (index, deviation)
        """
        if len(values) < self.window_size:
            return []
        
        anomalies = []
        
        for i in range(self.window_size, len(values)):
            window = values[i - self.window_size:i]
            ma = statistics.mean(window)
            
            # Calculate moving standard deviation
            variance = statistics.variance(window)
            std = statistics.stdev(window) if variance > 0 else 0
            
            current_value = values[i]
            deviation = abs(current_value - ma)
            
            if std > 0 and deviation > self.sigma * std:
                anomalies.append((i, deviation))
        
        return anomalies


class SeasonalityDetector:
    """Detect seasonal patterns and deviations"""
    
    def __init__(self, period: int = 24):
        """
        Initialize with season period
        period=24 for hourly data (daily seasonality)
        """
        self.period = period
    
    def detect(self, values: List[float], timestamps: List[datetime] = None) -> List[Anomaly]:
        """
        Detect seasonality violations
        """
        if len(values) < self.period * 2:
            return []
        
        anomalies = []
        
        # Group by season
        seasons = {}
        for i, value in enumerate(values):
            season_idx = i % self.period
            if season_idx not in seasons:
                seasons[season_idx] = []
            seasons[season_idx].append(value)
        
        # Find anomalies in each season
        for season_idx, season_values in seasons.items():
            if len(season_values) < 2:
                continue
            
            mean = statistics.mean(season_values)
            stdev = statistics.stdev(season_values)
            
            # Find indices that belong to this season
            for i in range(season_idx, len(values), self.period):
                value = values[i]
                if stdev > 0:
                    z_score = abs((value - mean) / stdev)
                    if z_score > 2.5:
                        anomalies.append(Anomaly(
                            timestamp=timestamps[i] if timestamps else datetime.now(),
                            metric_name=f'metric_index_{i}',
                            value=value,
                            expected_value=mean,
                            anomaly_type=AnomalyType.SEASONAL,
                            severity='medium',
                            description=f'Deviation from seasonal pattern (z-score: {z_score:.2f})',
                            context={'season_index': season_idx, 'z_score': z_score}
                        ))
        
        return anomalies


class BehaviorAnalyzer:
    """Analyze behavioral patterns and detect changes"""
    
    @staticmethod
    def detect_trend_change(values: List[float], window: int = 10) -> List[int]:
        """
        Detect when trend changes direction
        """
        if len(values) < window * 2:
            return []
        
        change_points = []
        
        for i in range(window, len(values) - window):
            before = values[i - window:i]
            after = values[i:i + window]
            
            before_trend = 1 if after[0] > before[0] else -1
            after_trend = 1 if after[-1] > after[0] else -1
            
            if before_trend != after_trend:
                change_points.append(i)
        
        return change_points
    
    @staticmethod
    def detect_level_shift(values: List[float], window: int = 10, threshold: float = 2.0) -> List[int]:
        """
        Detect sudden shifts in mean level
        """
        if len(values) < window * 2:
            return []
        
        shift_points = []
        
        for i in range(window, len(values) - window):
            before = values[i - window:i]
            after = values[i:i + window]
            
            mean_before = statistics.mean(before)
            mean_after = statistics.mean(after)
            
            combined_std = statistics.stdev(before + after) if len(before + after) > 1 else 1
            
            if combined_std > 0:
                shift = abs(mean_after - mean_before) / combined_std
                if shift > threshold:
                    shift_points.append(i)
        
        return shift_points


class ContextualAnomalyDetector:
    """Detect anomalies based on context"""
    
    @staticmethod
    def detect_transaction_anomalies(transactions: List[Dict[str, Any]]) -> List[Anomaly]:
        """
        Detect anomalous transactions based on context
        """
        anomalies = []
        
        if not transactions:
            return anomalies
        
        # Extract amounts
        amounts = [t.get('amount', 0) for t in transactions]
        if not amounts:
            return anomalies
        
        # Calculate statistics
        mean_amount = statistics.mean(amounts)
        stdev_amount = statistics.stdev(amounts) if len(amounts) > 1 else 0
        
        # Detect large transactions
        for i, txn in enumerate(transactions):
            amount = txn.get('amount', 0)
            
            if stdev_amount > 0:
                z_score = (amount - mean_amount) / stdev_amount
                
                # Large transaction
                if z_score > 3.0:
                    anomalies.append(Anomaly(
                        timestamp=datetime.fromisoformat(txn.get('timestamp', datetime.now().isoformat())),
                        metric_name='transaction_amount',
                        value=amount,
                        expected_value=mean_amount,
                        anomaly_type=AnomalyType.CONTEXTUAL,
                        severity='high',
                        description=f'Unusually large transaction: ${amount:,.2f}',
                        context={
                            'transaction_id': txn.get('transaction_id'),
                            'from_account': txn.get('from_account'),
                            'z_score': z_score
                        }
                    ))
        
        return anomalies
    
    @staticmethod
    def detect_fraud_patterns(transactions: List[Dict[str, Any]]) -> List[Anomaly]:
        """
        Detect potential fraud patterns
        """
        anomalies = []
        
        if not transactions:
            return anomalies
        
        # Pattern 1: Multiple rapid transactions from same account
        account_txns = {}
        for txn in transactions:
            account_id = txn.get('from_account', 'unknown')
            if account_id not in account_txns:
                account_txns[account_id] = []
            account_txns[account_id].append(txn)
        
        for account_id, txns in account_txns.items():
            if len(txns) >= 5:
                # Check time gaps
                sorted_txns = sorted(txns, key=lambda x: x.get('timestamp', ''))
                
                for i in range(1, min(5, len(sorted_txns))):
                    try:
                        t1 = datetime.fromisoformat(sorted_txns[i-1].get('timestamp', ''))
                        t2 = datetime.fromisoformat(sorted_txns[i].get('timestamp', ''))
                        gap = (t2 - t1).total_seconds()
                        
                        if gap < 60:  # Less than 60 seconds
                            anomalies.append(Anomaly(
                                timestamp=t2,
                                metric_name='transaction_frequency',
                                value=gap,
                                expected_value=300,  # 5 minutes expected
                                anomaly_type=AnomalyType.BEHAVIORAL,
                                severity='critical',
                                description='Rapid consecutive transactions detected',
                                context={
                                    'account_id': account_id,
                                    'gap_seconds': gap
                                }
                            ))
                    except ValueError:
                        pass
        
        return anomalies


class AnomalyDetectionEngine:
    """Main anomaly detection engine combining multiple detectors"""
    
    def __init__(self):
        self.zscore_detector = ZScoreDetector(threshold=2.5)
        self.iqr_detector = IQRDetector(multiplier=1.5)
        self.ma_detector = MovingAverageDetector(window_size=7, sigma=2.0)
        self.seasonality_detector = SeasonalityDetector(period=24)
        self.behavior_analyzer = BehaviorAnalyzer()
        self.contextual_detector = ContextualAnomalyDetector()
    
    def detect_metric_anomalies(self, metric_name: str, values: List[float], 
                               timestamps: List[datetime] = None) -> List[Anomaly]:
        """
        Detect anomalies in metric data using multiple methods
        """
        anomalies = []
        
        if len(values) < 3:
            return anomalies
        
        # Z-Score detection
        zscore_results = self.zscore_detector.detect(values)
        for idx, z_score in zscore_results:
            anomalies.append(Anomaly(
                timestamp=timestamps[idx] if timestamps else datetime.now(),
                metric_name=metric_name,
                value=values[idx],
                expected_value=statistics.mean(values),
                anomaly_type=AnomalyType.STATISTICAL,
                severity='high' if z_score > 3.5 else 'medium',
                description=f'Z-score anomaly: {z_score:.2f}',
                context={'z_score': z_score, 'index': idx}
            ))
        
        # IQR detection
        iqr_results = self.iqr_detector.detect(values)
        for idx, outlier_type in iqr_results:
            anomalies.append(Anomaly(
                timestamp=timestamps[idx] if timestamps else datetime.now(),
                metric_name=metric_name,
                value=values[idx],
                expected_value=statistics.median(values),
                anomaly_type=AnomalyType.STATISTICAL,
                severity='medium',
                description=f'IQR-based outlier: {outlier_type}',
                context={'outlier_type': outlier_type, 'index': idx}
            ))
        
        # Moving Average detection
        ma_results = self.ma_detector.detect(values)
        for idx, deviation in ma_results:
            anomalies.append(Anomaly(
                timestamp=timestamps[idx] if timestamps else datetime.now(),
                metric_name=metric_name,
                value=values[idx],
                expected_value=statistics.mean(values),
                anomaly_type=AnomalyType.STATISTICAL,
                severity='medium',
                description=f'Moving average deviation: {deviation:.2f}',
                context={'deviation': deviation, 'index': idx}
            ))
        
        return anomalies
    
    def detect_all_anomalies(self, metrics_data: Dict[str, List[float]],
                            transaction_data: List[Dict[str, Any]] = None) -> Dict[str, List[Anomaly]]:
        """
        Detect all types of anomalies in data
        """
        all_anomalies = {}
        
        # Metric anomalies
        for metric_name, values in metrics_data.items():
            all_anomalies[metric_name] = self.detect_metric_anomalies(metric_name, values)
        
        # Transaction anomalies
        if transaction_data:
            all_anomalies['transactions'] = (
                self.contextual_detector.detect_transaction_anomalies(transaction_data) +
                self.contextual_detector.detect_fraud_patterns(transaction_data)
            )
        
        return all_anomalies
