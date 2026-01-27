"""
Banking Application with Azure Application Insights Integration
Demonstrates production-grade monitoring for transaction processing
"""

import os
import json
import logging
import uuid
from datetime import datetime
from functools import wraps
from typing import Dict, Any, Optional

from flask import Flask, request, jsonify
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler
from applicationinsights import TelemetryClient
from applicationinsights.channel import TelemetryChannel

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# ========== Azure Application Insights Setup ==========
class AppInsightsConfig:
    """Configuration for Application Insights"""
    
    def __init__(self):
        self.instrumentation_key = os.getenv(
            'APPINSIGHTS_INSTRUMENTATION_KEY',
            'YOUR_INSTRUMENTATION_KEY_HERE'
        )
        self.connection_string = os.getenv(
            'APPLICATIONINSIGHTS_CONNECTION_STRING',
            f'InstrumentationKey={self.instrumentation_key}'
        )
    
    @property
    def is_configured(self) -> bool:
        return self.instrumentation_key != 'YOUR_INSTRUMENTATION_KEY_HERE'


# Initialize Configuration
ai_config = AppInsightsConfig()

# Setup Azure Exporter with proper error handling
if ai_config.is_configured:
    exporter = AzureExporter(
        connection_string=ai_config.connection_string,
        sampler=ProbabilitySampler(rate=1.0)  # Log 100% for demo; use 0.1 for production
    )
    FlaskMiddleware(app, exporter=exporter)

# Setup Telemetry Client
tc = TelemetryClient(ai_config.instrumentation_key) if ai_config.is_configured else None

# Setup Logging with Application Insights
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if ai_config.is_configured:
    ai_handler = AzureLogHandler(connection_string=ai_config.connection_string)
    logger.addHandler(ai_handler)

console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


# ========== Banking Domain Models ==========
class BankAccount:
    """Represents a bank account"""
    
    def __init__(self, account_id: str, account_holder: str, balance: float, account_type: str):
        self.account_id = account_id
        self.account_holder = account_holder
        self.balance = balance
        self.account_type = account_type  # 'savings', 'checking', 'money_market'
        self.created_at = datetime.utcnow()
        self.is_active = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'account_id': self.account_id,
            'account_holder': self.account_holder,
            'balance': self.balance,
            'account_type': self.account_type,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }


class Transaction:
    """Represents a banking transaction"""
    
    def __init__(self, from_account: str, to_account: str, amount: float, 
                 transaction_type: str, description: str = ""):
        self.transaction_id = str(uuid.uuid4())
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount
        self.transaction_type = transaction_type  # 'transfer', 'deposit', 'withdrawal'
        self.description = description
        self.timestamp = datetime.utcnow()
        self.status = 'pending'
        self.details = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'transaction_id': self.transaction_id,
            'from_account': self.from_account,
            'to_account': self.to_account,
            'amount': self.amount,
            'type': self.transaction_type,
            'description': self.description,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status,
            'details': self.details
        }


# ========== In-Memory Data Store ==========
accounts_db: Dict[str, BankAccount] = {}
transactions_log: list = []


# ========== Monitoring Decorators ==========
def track_performance(operation_name: str):
    """Decorator to track operation performance and custom metrics"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.utcnow()
            
            try:
                result = func(*args, **kwargs)
                
                # Track successful operation
                duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
                
                custom_properties = {
                    'operation': operation_name,
                    'status': 'success',
                    'duration_ms': duration_ms,
                    'user': request.headers.get('X-User-ID', 'unknown'),
                    'client_ip': request.remote_addr
                }
                
                if tc:
                    tc.track_event(f'{operation_name}_success', properties=custom_properties)
                    tc.track_request(operation_name, url=request.url, 
                                   start_time=start_time, success=True)
                
                logger.info(
                    f"Operation '{operation_name}' completed successfully",
                    extra={'custom_dimensions': custom_properties}
                )
                
                return result
                
            except Exception as e:
                duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
                
                error_properties = {
                    'operation': operation_name,
                    'status': 'failed',
                    'duration_ms': duration_ms,
                    'error_type': type(e).__name__,
                    'error_message': str(e),
                    'user': request.headers.get('X-User-ID', 'unknown'),
                    'client_ip': request.remote_addr
                }
                
                if tc:
                    tc.track_event(f'{operation_name}_failure', properties=error_properties)
                    tc.track_exception()
                
                logger.error(
                    f"Operation '{operation_name}' failed: {str(e)}",
                    extra={'custom_dimensions': error_properties},
                    exc_info=True
                )
                
                raise
        
        return wrapper
    return decorator


# ========== Banking Endpoints ==========

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'accounts_count': len(accounts_db),
        'transactions_count': len(transactions_log)
    }), 200


@app.route('/api/accounts', methods=['POST'])
@track_performance('create_account')
def create_account():
    """Create a new bank account"""
    data = request.get_json()
    
    # Validation
    if not data or 'account_holder' not in data or 'initial_balance' not in data:
        raise ValueError("Missing required fields: account_holder, initial_balance")
    
    account_id = f"ACC-{uuid.uuid4().hex[:12].upper()}"
    account_type = data.get('account_type', 'checking')
    
    account = BankAccount(
        account_id=account_id,
        account_holder=data['account_holder'],
        balance=float(data['initial_balance']),
        account_type=account_type
    )
    
    accounts_db[account_id] = account
    
    # Track custom metric
    if tc:
        tc.track_event('account_created', {
            'account_type': account_type,
            'initial_balance': data['initial_balance']
        })
    
    return jsonify(account.to_dict()), 201


@app.route('/api/accounts/<account_id>', methods=['GET'])
@track_performance('get_account')
def get_account(account_id):
    """Get account details"""
    account = accounts_db.get(account_id)
    
    if not account:
        raise ValueError(f"Account not found: {account_id}")
    
    return jsonify(account.to_dict()), 200


@app.route('/api/accounts/<account_id>/balance', methods=['GET'])
@track_performance('get_balance')
def get_balance(account_id):
    """Get account balance"""
    account = accounts_db.get(account_id)
    
    if not account:
        raise ValueError(f"Account not found: {account_id}")
    
    return jsonify({
        'account_id': account_id,
        'balance': account.balance,
        'currency': 'USD',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/api/transactions/transfer', methods=['POST'])
@track_performance('transfer_funds')
def transfer_funds():
    """Transfer funds between accounts"""
    data = request.get_json()
    
    # Validation
    required_fields = ['from_account', 'to_account', 'amount']
    if not all(field in data for field in required_fields):
        raise ValueError(f"Missing fields: {', '.join(required_fields)}")
    
    from_acc_id = data['from_account']
    to_acc_id = data['to_account']
    amount = float(data['amount'])
    
    # Business logic validation
    if from_acc_id == to_acc_id:
        raise ValueError("Cannot transfer to the same account")
    
    if amount <= 0:
        raise ValueError("Transfer amount must be positive")
    
    if from_acc_id not in accounts_db or to_acc_id not in accounts_db:
        raise ValueError("One or both accounts not found")
    
    from_account = accounts_db[from_acc_id]
    to_account = accounts_db[to_acc_id]
    
    if from_account.balance < amount:
        raise ValueError("Insufficient balance")
    
    # Execute transfer
    from_account.balance -= amount
    to_account.balance += amount
    
    # Create transaction record
    transaction = Transaction(
        from_account=from_acc_id,
        to_account=to_acc_id,
        amount=amount,
        transaction_type='transfer',
        description=data.get('description', 'Fund transfer')
    )
    transaction.status = 'completed'
    transactions_log.append(transaction)
    
    # Track metrics
    if tc:
        tc.track_event('transfer_completed', {
            'from_account': from_acc_id,
            'to_account': to_acc_id,
            'amount': amount,
            'from_balance_after': from_account.balance,
            'to_balance_after': to_account.balance
        })
    
    logger.info(f"Transfer completed: {transaction.transaction_id}")
    
    return jsonify({
        'transaction_id': transaction.transaction_id,
        'status': 'completed',
        'timestamp': transaction.timestamp.isoformat()
    }), 200


@app.route('/api/transactions/<transaction_id>', methods=['GET'])
@track_performance('get_transaction')
def get_transaction(transaction_id):
    """Get transaction details"""
    for txn in transactions_log:
        if txn.transaction_id == transaction_id:
            return jsonify(txn.to_dict()), 200
    
    raise ValueError(f"Transaction not found: {transaction_id}")


@app.route('/api/transactions', methods=['GET'])
@track_performance('list_transactions')
def list_transactions():
    """List all transactions with optional filtering"""
    account_id = request.args.get('account_id')
    limit = int(request.args.get('limit', 100))
    
    filtered = transactions_log
    if account_id:
        filtered = [
            t for t in transactions_log 
            if t.from_account == account_id or t.to_account == account_id
        ]
    
    return jsonify({
        'total': len(filtered),
        'transactions': [t.to_dict() for t in filtered[-limit:]]
    }), 200


@app.route('/api/transactions/deposit', methods=['POST'])
@track_performance('deposit_funds')
def deposit_funds():
    """Deposit funds to an account"""
    data = request.get_json()
    
    if 'account_id' not in data or 'amount' not in data:
        raise ValueError("Missing fields: account_id, amount")
    
    account_id = data['account_id']
    amount = float(data['amount'])
    
    if account_id not in accounts_db:
        raise ValueError(f"Account not found: {account_id}")
    
    if amount <= 0:
        raise ValueError("Deposit amount must be positive")
    
    account = accounts_db[account_id]
    account.balance += amount
    
    # Create transaction record
    transaction = Transaction(
        from_account='system',
        to_account=account_id,
        amount=amount,
        transaction_type='deposit',
        description=data.get('description', 'Deposit')
    )
    transaction.status = 'completed'
    transactions_log.append(transaction)
    
    if tc:
        tc.track_event('deposit_completed', {
            'account_id': account_id,
            'amount': amount,
            'balance_after': account.balance
        })
    
    return jsonify({
        'transaction_id': transaction.transaction_id,
        'status': 'completed'
    }), 200


# ========== Error Handlers ==========
@app.errorhandler(ValueError)
def handle_value_error(error):
    """Handle validation errors"""
    if tc:
        tc.track_event('validation_error', {'error': str(error)})
    
    logger.warning(f"Validation error: {str(error)}")
    return jsonify({'error': str(error)}), 400


@app.errorhandler(Exception)
def handle_generic_error(error):
    """Handle generic errors"""
    if tc:
        tc.track_exception()
    
    logger.error(f"Unhandled exception: {str(error)}", exc_info=True)
    return jsonify({
        'error': 'Internal server error',
        'details': str(error)  # Include exception details for debugging
    }), 500


if __name__ == '__main__':
    logger.info("Starting Banking Application")
    app.run(debug=True, host='0.0.0.0', port=5050)
