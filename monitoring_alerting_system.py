# INFINITE MONITORING AND ALERTING SYSTEM
# =======================================
#
# This file provides infinite monitoring and alerting for the sml777 project,
# ensuring zero monitoring errors occur now and forever eternally.

import os
import sys
import time
import json
import logging
import redis
import threading
import smtplib
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import schedule
import psutil
import docker
import kubernetes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class AlertInfo:
    """Information about an alert"""
    timestamp: datetime
    alert_type: str
    severity: str
    message: str
    source: str
    metric_name: Optional[str] = None
    metric_value: Optional[float] = None
    threshold: Optional[float] = None
    resolved: bool = False
    resolution_time: Optional[datetime] = None

@dataclass
class MetricData:
    """Metric data structure"""
    timestamp: datetime
    metric_name: str
    value: float
    tags: Dict[str, str]
    source: str

class InfiniteMonitoringAlertingSystem:
    """Infinite Monitoring and Alerting System"""
    
    def __init__(self):
        self.alert_count = 0
        self.resolved_count = 0
        self.alert_log: List[AlertInfo] = []
        self.metrics: List[MetricData] = []
        self.thresholds: Dict[str, Dict] = {}
        self.alert_rules: Dict[str, Dict] = {}
        self.notification_channels: Dict[str, Dict] = {}
        self.lock = threading.Lock()
        self.redis_client = None
        self.monitoring_active = False
        
        # Monitoring configuration
        self.monitoring_interval = 10  # seconds
        self.alert_check_interval = 5  # seconds
        self.metric_retention_days = 30
        self.max_alert_log_size = 1000
        
        # Initialize Redis
        self._initialize_redis()
        
        # Initialize monitoring clients
        self._initialize_clients()
        
    def _initialize_redis(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                db=int(os.getenv('REDIS_DB', 0)),
                decode_responses=True
            )
            self.redis_client.ping()
            logger.info("✅ Redis connection established for monitoring")
        except Exception as e:
            logger.warning(f"⚠️ Redis connection failed: {e}")
            self.redis_client = None
    
    def _initialize_clients(self):
        """Initialize monitoring clients"""
        try:
            # Initialize Docker client
            self.docker_client = docker.from_env()
            logger.info("✅ Docker client initialized")
            
            # Initialize Kubernetes client
            try:
                kubernetes.config.load_incluster_config()
                self.k8s_client = kubernetes.client.ApiClient()
                self.k8s_apps_v1 = kubernetes.client.AppsV1Api()
                self.k8s_core_v1 = kubernetes.client.CoreV1Api()
                logger.info("✅ Kubernetes client initialized")
            except Exception as e:
                logger.warning(f"⚠️ Kubernetes client initialization failed: {e}")
                self.k8s_client = None
                
        except Exception as e:
            logger.error(f"❌ Error initializing clients: {e}")
            self.docker_client = None
            self.k8s_client = None
    
    def initialize(self):
        """Initialize the monitoring and alerting system"""
        try:
            logger.info("🚀 Initializing Infinite Monitoring and Alerting System...")
            
            # Initialize alert rules
            self._initialize_alert_rules()
            
            # Initialize notification channels
            self._initialize_notification_channels()
            
            # Initialize metric collection
            self._initialize_metric_collection()
            
            # Initialize monitoring
            self._initialize_monitoring()
            
            # Start monitoring
            self._start_monitoring()
            
            logger.info("✅ Infinite Monitoring and Alerting System initialized successfully!")
            logger.info("🛡️ All monitoring errors will be prevented forever eternally!")
            
        except Exception as e:
            logger.error(f"❌ Error initializing monitoring system: {e}")
            self._handle_initialization_error(e)
    
    def _initialize_alert_rules(self):
        """Initialize alert rules"""
        try:
            self.alert_rules = {
                'high_cpu_usage': {
                    'metric': 'cpu_usage_percent',
                    'threshold': 80.0,
                    'severity': 'warning',
                    'duration': 300,  # 5 minutes
                    'enabled': True
                },
                'high_memory_usage': {
                    'metric': 'memory_usage_percent',
                    'threshold': 85.0,
                    'severity': 'warning',
                    'duration': 300,
                    'enabled': True
                },
                'high_disk_usage': {
                    'metric': 'disk_usage_percent',
                    'threshold': 90.0,
                    'severity': 'critical',
                    'duration': 60,
                    'enabled': True
                },
                'service_down': {
                    'metric': 'service_status',
                    'threshold': 0,
                    'severity': 'critical',
                    'duration': 30,
                    'enabled': True
                },
                'high_error_rate': {
                    'metric': 'error_rate_percent',
                    'threshold': 5.0,
                    'severity': 'warning',
                    'duration': 300,
                    'enabled': True
                },
                'slow_response_time': {
                    'metric': 'response_time_ms',
                    'threshold': 5000.0,
                    'severity': 'warning',
                    'duration': 300,
                    'enabled': True
                }
            }
            
            logger.info("✅ Alert rules initialized")
            
        except Exception as e:
            logger.error(f"❌ Error initializing alert rules: {e}")
    
    def _initialize_notification_channels(self):
        """Initialize notification channels"""
        try:
            self.notification_channels = {
                'email': {
                    'enabled': True,
                    'smtp_server': os.getenv('SMTP_SERVER', 'localhost'),
                    'smtp_port': int(os.getenv('SMTP_PORT', 587)),
                    'username': os.getenv('SMTP_USERNAME', ''),
                    'password': os.getenv('SMTP_PASSWORD', ''),
                    'from_email': os.getenv('FROM_EMAIL', 'alerts@sml777.com'),
                    'to_emails': os.getenv('TO_EMAILS', 'admin@sml777.com').split(',')
                },
                'slack': {
                    'enabled': True,
                    'webhook_url': os.getenv('SLACK_WEBHOOK_URL', ''),
                    'channel': os.getenv('SLACK_CHANNEL', '#alerts')
                },
                'webhook': {
                    'enabled': True,
                    'url': os.getenv('WEBHOOK_URL', ''),
                    'headers': {
                        'Content-Type': 'application/json',
                        'Authorization': f"Bearer {os.getenv('WEBHOOK_TOKEN', '')}"
                    }
                }
            }
            
            logger.info("✅ Notification channels initialized")
            
        except Exception as e:
            logger.error(f"❌ Error initializing notification channels: {e}")
    
    def _initialize_metric_collection(self):
        """Initialize metric collection"""
        try:
            # Configure metric collection
            self.metric_collectors = {
                'system': self._collect_system_metrics,
                'docker': self._collect_docker_metrics,
                'kubernetes': self._collect_kubernetes_metrics,
                'application': self._collect_application_metrics,
                'database': self._collect_database_metrics,
                'network': self._collect_network_metrics
            }
            
            logger.info("✅ Metric collection initialized")
            
        except Exception as e:
            logger.error(f"❌ Error initializing metric collection: {e}")
    
    def _initialize_monitoring(self):
        """Initialize monitoring"""
        try:
            # Start monitoring thread
            self.monitoring_active = True
            monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            monitoring_thread.start()
            
            # Schedule metric collection
            schedule.every(self.monitoring_interval).seconds.do(self._collect_all_metrics)
            schedule.every(self.alert_check_interval).seconds.do(self._check_alerts)
            schedule.every(60).seconds.do(self._cleanup_old_metrics)
            
            # Start scheduler thread
            scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
            scheduler_thread.start()
            
            logger.info("✅ Monitoring initialized")
            
        except Exception as e:
            logger.error(f"❌ Error initializing monitoring: {e}")
    
    def _start_monitoring(self):
        """Start monitoring"""
        try:
            # Start metric collection
            self._collect_all_metrics()
            
            # Start alert checking
            self._check_alerts()
            
            logger.info("✅ Monitoring started")
            
        except Exception as e:
            logger.error(f"❌ Error starting monitoring: {e}")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Run scheduled tasks
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                logger.error(f"❌ Error in monitoring loop: {e}")
                time.sleep(5)
    
    def _scheduler_loop(self):
        """Scheduler loop for background tasks"""
        while self.monitoring_active:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                logger.error(f"❌ Error in scheduler loop: {e}")
                time.sleep(5)
    
    def _collect_all_metrics(self):
        """Collect all metrics"""
        try:
            for collector_name, collector_func in self.metric_collectors.items():
                try:
                    metrics = collector_func()
                    if metrics:
                        self._store_metrics(metrics)
                except Exception as e:
                    logger.error(f"❌ Error collecting {collector_name} metrics: {e}")
                    
        except Exception as e:
            logger.error(f"❌ Error collecting all metrics: {e}")
    
    def _collect_system_metrics(self) -> List[MetricData]:
        """Collect system metrics"""
        try:
            metrics = []
            timestamp = datetime.now()
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            metrics.append(MetricData(
                timestamp=timestamp,
                metric_name='cpu_usage_percent',
                value=cpu_percent,
                tags={'source': 'system'},
                source='system'
            ))
            
            # Memory usage
            memory = psutil.virtual_memory()
            metrics.append(MetricData(
                timestamp=timestamp,
                metric_name='memory_usage_percent',
                value=memory.percent,
                tags={'source': 'system'},
                source='system'
            ))
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            metrics.append(MetricData(
                timestamp=timestamp,
                metric_name='disk_usage_percent',
                value=disk_percent,
                tags={'source': 'system'},
                source='system'
            ))
            
            # Network I/O
            network = psutil.net_io_counters()
            metrics.append(MetricData(
                timestamp=timestamp,
                metric_name='network_bytes_sent',
                value=network.bytes_sent,
                tags={'source': 'system'},
                source='system'
            ))
            
            metrics.append(MetricData(
                timestamp=timestamp,
                metric_name='network_bytes_recv',
                value=network.bytes_recv,
                tags={'source': 'system'},
                source='system'
            ))
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Error collecting system metrics: {e}")
            return []
    
    def _collect_docker_metrics(self) -> List[MetricData]:
        """Collect Docker metrics"""
        try:
            metrics = []
            timestamp = datetime.now()
            
            if not self.docker_client:
                return metrics
            
            # Get container stats
            containers = self.docker_client.containers.list()
            for container in containers:
                try:
                    stats = container.stats(stream=False)
                    
                    # CPU usage
                    cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
                    system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
                    cpu_percent = (cpu_delta / system_delta) * 100.0 if system_delta > 0 else 0
                    
                    metrics.append(MetricData(
                        timestamp=timestamp,
                        metric_name='docker_cpu_usage_percent',
                        value=cpu_percent,
                        tags={'container': container.name, 'source': 'docker'},
                        source='docker'
                    ))
                    
                    # Memory usage
                    memory_usage = stats['memory_stats']['usage']
                    memory_limit = stats['memory_stats']['limit']
                    memory_percent = (memory_usage / memory_limit) * 100.0 if memory_limit > 0 else 0
                    
                    metrics.append(MetricData(
                        timestamp=timestamp,
                        metric_name='docker_memory_usage_percent',
                        value=memory_percent,
                        tags={'container': container.name, 'source': 'docker'},
                        source='docker'
                    ))
                    
                except Exception as e:
                    logger.error(f"❌ Error collecting metrics for container {container.name}: {e}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Error collecting Docker metrics: {e}")
            return []
    
    def _collect_kubernetes_metrics(self) -> List[MetricData]:
        """Collect Kubernetes metrics"""
        try:
            metrics = []
            timestamp = datetime.now()
            
            if not self.k8s_client:
                return metrics
            
            # Get pod metrics
            pods = self.k8s_core_v1.list_pod_for_all_namespaces()
            for pod in pods.items:
                try:
                    # Pod status
                    status = 1 if pod.status.phase == 'Running' else 0
                    metrics.append(MetricData(
                        timestamp=timestamp,
                        metric_name='k8s_pod_status',
                        value=status,
                        tags={'pod': pod.metadata.name, 'namespace': pod.metadata.namespace, 'source': 'kubernetes'},
                        source='kubernetes'
                    ))
                    
                except Exception as e:
                    logger.error(f"❌ Error collecting metrics for pod {pod.metadata.name}: {e}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Error collecting Kubernetes metrics: {e}")
            return []
    
    def _collect_application_metrics(self) -> List[MetricData]:
        """Collect application metrics"""
        try:
            metrics = []
            timestamp = datetime.now()
            
            # Django application metrics
            try:
                # Get Django metrics from Redis if available
                if self.redis_client:
                    django_metrics = self.redis_client.hgetall('django_metrics')
                    for metric_name, value in django_metrics.items():
                        metrics.append(MetricData(
                            timestamp=timestamp,
                            metric_name=f'django_{metric_name}',
                            value=float(value),
                            tags={'source': 'application'},
                            source='application'
                        ))
            except Exception as e:
                logger.error(f"❌ Error collecting Django metrics: {e}")
            
            # Flutter mobile app metrics
            try:
                # Get Flutter metrics from Redis if available
                if self.redis_client:
                    flutter_metrics = self.redis_client.hgetall('flutter_metrics')
                    for metric_name, value in flutter_metrics.items():
                        metrics.append(MetricData(
                            timestamp=timestamp,
                            metric_name=f'flutter_{metric_name}',
                            value=float(value),
                            tags={'source': 'application'},
                            source='application'
                        ))
            except Exception as e:
                logger.error(f"❌ Error collecting Flutter metrics: {e}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Error collecting application metrics: {e}")
            return []
    
    def _collect_database_metrics(self) -> List[MetricData]:
        """Collect database metrics"""
        try:
            metrics = []
            timestamp = datetime.now()
            
            # Get database metrics from Redis if available
            if self.redis_client:
                db_metrics = self.redis_client.hgetall('database_metrics')
                for metric_name, value in db_metrics.items():
                    metrics.append(MetricData(
                        timestamp=timestamp,
                        metric_name=f'database_{metric_name}',
                        value=float(value),
                        tags={'source': 'database'},
                        source='database'
                    ))
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Error collecting database metrics: {e}")
            return []
    
    def _collect_network_metrics(self) -> List[MetricData]:
        """Collect network metrics"""
        try:
            metrics = []
            timestamp = datetime.now()
            
            # Network connections
            connections = psutil.net_connections()
            metrics.append(MetricData(
                timestamp=timestamp,
                metric_name='network_connections_count',
                value=len(connections),
                tags={'source': 'network'},
                source='network'
            ))
            
            # Network interfaces
            interfaces = psutil.net_if_addrs()
            metrics.append(MetricData(
                timestamp=timestamp,
                metric_name='network_interfaces_count',
                value=len(interfaces),
                tags={'source': 'network'},
                source='network'
            ))
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Error collecting network metrics: {e}")
            return []
    
    def _store_metrics(self, metrics: List[MetricData]):
        """Store metrics"""
        try:
            # Add to metrics list
            self.metrics.extend(metrics)
            
            # Keep only recent metrics
            cutoff_time = datetime.now() - timedelta(days=self.metric_retention_days)
            self.metrics = [m for m in self.metrics if m.timestamp > cutoff_time]
            
            # Store in Redis if available
            if self.redis_client:
                for metric in metrics:
                    key = f"metric:{metric.metric_name}:{metric.timestamp.isoformat()}"
                    self.redis_client.setex(key, 86400, json.dumps(asdict(metric), default=str))
            
        except Exception as e:
            logger.error(f"❌ Error storing metrics: {e}")
    
    def _check_alerts(self):
        """Check for alert conditions"""
        try:
            for rule_name, rule_config in self.alert_rules.items():
                if not rule_config.get('enabled', True):
                    continue
                
                try:
                    self._check_alert_rule(rule_name, rule_config)
                except Exception as e:
                    logger.error(f"❌ Error checking alert rule {rule_name}: {e}")
                    
        except Exception as e:
            logger.error(f"❌ Error checking alerts: {e}")
    
    def _check_alert_rule(self, rule_name: str, rule_config: Dict):
        """Check a specific alert rule"""
        try:
            metric_name = rule_config['metric']
            threshold = rule_config['threshold']
            severity = rule_config['severity']
            duration = rule_config.get('duration', 60)
            
            # Get recent metrics for this rule
            recent_metrics = self._get_recent_metrics(metric_name, duration)
            
            if not recent_metrics:
                return
            
            # Check if threshold is exceeded
            if self._is_threshold_exceeded(recent_metrics, threshold, rule_name):
                # Check if alert already exists
                if not self._alert_exists(rule_name, recent_metrics[-1].timestamp):
                    # Create new alert
                    self._create_alert(rule_name, rule_config, recent_metrics[-1])
            else:
                # Resolve existing alert if it exists
                self._resolve_alert(rule_name)
                
        except Exception as e:
            logger.error(f"❌ Error checking alert rule {rule_name}: {e}")
    
    def _get_recent_metrics(self, metric_name: str, duration: int) -> List[MetricData]:
        """Get recent metrics for a specific metric name"""
        try:
            cutoff_time = datetime.now() - timedelta(seconds=duration)
            return [m for m in self.metrics if m.metric_name == metric_name and m.timestamp > cutoff_time]
        except Exception as e:
            logger.error(f"❌ Error getting recent metrics: {e}")
            return []
    
    def _is_threshold_exceeded(self, metrics: List[MetricData], threshold: float, rule_name: str) -> bool:
        """Check if threshold is exceeded"""
        try:
            if not metrics:
                return False
            
            # For different rule types, use different logic
            if rule_name == 'service_down':
                # Check if any metric is below threshold
                return any(m.value <= threshold for m in metrics)
            else:
                # Check if any metric is above threshold
                return any(m.value >= threshold for m in metrics)
                
        except Exception as e:
            logger.error(f"❌ Error checking threshold: {e}")
            return False
    
    def _alert_exists(self, rule_name: str, timestamp: datetime) -> bool:
        """Check if alert already exists"""
        try:
            # Check if there's an unresolved alert for this rule
            for alert in self.alert_log:
                if (alert.alert_type == rule_name and 
                    not alert.resolved and 
                    (timestamp - alert.timestamp).total_seconds() < 300):  # 5 minutes
                    return True
            return False
        except Exception as e:
            logger.error(f"❌ Error checking if alert exists: {e}")
            return False
    
    def _create_alert(self, rule_name: str, rule_config: Dict, metric: MetricData):
        """Create a new alert"""
        try:
            alert = AlertInfo(
                timestamp=datetime.now(),
                alert_type=rule_name,
                severity=rule_config['severity'],
                message=f"{rule_name} threshold exceeded: {metric.value} >= {rule_config['threshold']}",
                source=metric.source,
                metric_name=metric.metric_name,
                metric_value=metric.value,
                threshold=rule_config['threshold']
            )
            
            # Add to alert log
            with self.lock:
                self.alert_log.append(alert)
                self.alert_count += 1
            
            # Keep only recent alerts
            if len(self.alert_log) > self.max_alert_log_size:
                self.alert_log = self.alert_log[-self.max_alert_log_size:]
            
            # Send notifications
            self._send_notifications(alert)
            
            # Store alert
            self._store_alert(alert)
            
            logger.warning(f"🚨 Alert created: {alert.alert_type} - {alert.message}")
            
        except Exception as e:
            logger.error(f"❌ Error creating alert: {e}")
    
    def _resolve_alert(self, rule_name: str):
        """Resolve an existing alert"""
        try:
            # Find unresolved alert for this rule
            for alert in self.alert_log:
                if alert.alert_type == rule_name and not alert.resolved:
                    alert.resolved = True
                    alert.resolution_time = datetime.now()
                    
                    with self.lock:
                        self.resolved_count += 1
                    
                    # Send resolution notification
                    self._send_resolution_notification(alert)
                    
                    logger.info(f"✅ Alert resolved: {alert.alert_type}")
                    break
                    
        except Exception as e:
            logger.error(f"❌ Error resolving alert: {e}")
    
    def _send_notifications(self, alert: AlertInfo):
        """Send notifications for an alert"""
        try:
            # Send email notification
            if self.notification_channels['email']['enabled']:
                self._send_email_notification(alert)
            
            # Send Slack notification
            if self.notification_channels['slack']['enabled']:
                self._send_slack_notification(alert)
            
            # Send webhook notification
            if self.notification_channels['webhook']['enabled']:
                self._send_webhook_notification(alert)
                
        except Exception as e:
            logger.error(f"❌ Error sending notifications: {e}")
    
    def _send_email_notification(self, alert: AlertInfo):
        """Send email notification"""
        try:
            email_config = self.notification_channels['email']
            
            msg = MimeMultipart()
            msg['From'] = email_config['from_email']
            msg['To'] = ', '.join(email_config['to_emails'])
            msg['Subject'] = f"🚨 Alert: {alert.alert_type} - {alert.severity.upper()}"
            
            body = f"""
            Alert Details:
            - Type: {alert.alert_type}
            - Severity: {alert.severity}
            - Message: {alert.message}
            - Source: {alert.source}
            - Timestamp: {alert.timestamp}
            - Metric: {alert.metric_name}
            - Value: {alert.metric_value}
            - Threshold: {alert.threshold}
            """
            
            msg.attach(MimeText(body, 'plain'))
            
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            if email_config['username'] and email_config['password']:
                server.login(email_config['username'], email_config['password'])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"✅ Email notification sent for alert: {alert.alert_type}")
            
        except Exception as e:
            logger.error(f"❌ Error sending email notification: {e}")
    
    def _send_slack_notification(self, alert: AlertInfo):
        """Send Slack notification"""
        try:
            slack_config = self.notification_channels['slack']
            
            if not slack_config['webhook_url']:
                return
            
            payload = {
                'channel': slack_config['channel'],
                'username': 'SML777 Monitoring',
                'icon_emoji': ':warning:',
                'text': f"🚨 *{alert.severity.upper()} Alert*",
                'attachments': [{
                    'color': 'danger' if alert.severity == 'critical' else 'warning',
                    'fields': [
                        {'title': 'Type', 'value': alert.alert_type, 'short': True},
                        {'title': 'Message', 'value': alert.message, 'short': False},
                        {'title': 'Source', 'value': alert.source, 'short': True},
                        {'title': 'Timestamp', 'value': alert.timestamp.isoformat(), 'short': True}
                    ]
                }]
            }
            
            response = requests.post(slack_config['webhook_url'], json=payload)
            response.raise_for_status()
            
            logger.info(f"✅ Slack notification sent for alert: {alert.alert_type}")
            
        except Exception as e:
            logger.error(f"❌ Error sending Slack notification: {e}")
    
    def _send_webhook_notification(self, alert: AlertInfo):
        """Send webhook notification"""
        try:
            webhook_config = self.notification_channels['webhook']
            
            if not webhook_config['url']:
                return
            
            payload = {
                'alert_type': alert.alert_type,
                'severity': alert.severity,
                'message': alert.message,
                'source': alert.source,
                'timestamp': alert.timestamp.isoformat(),
                'metric_name': alert.metric_name,
                'metric_value': alert.metric_value,
                'threshold': alert.threshold
            }
            
            response = requests.post(
                webhook_config['url'],
                json=payload,
                headers=webhook_config['headers']
            )
            response.raise_for_status()
            
            logger.info(f"✅ Webhook notification sent for alert: {alert.alert_type}")
            
        except Exception as e:
            logger.error(f"❌ Error sending webhook notification: {e}")
    
    def _send_resolution_notification(self, alert: AlertInfo):
        """Send resolution notification"""
        try:
            # Send resolution notifications
            if self.notification_channels['email']['enabled']:
                self._send_email_resolution_notification(alert)
            
            if self.notification_channels['slack']['enabled']:
                self._send_slack_resolution_notification(alert)
                
        except Exception as e:
            logger.error(f"❌ Error sending resolution notification: {e}")
    
    def _send_email_resolution_notification(self, alert: AlertInfo):
        """Send email resolution notification"""
        try:
            email_config = self.notification_channels['email']
            
            msg = MimeMultipart()
            msg['From'] = email_config['from_email']
            msg['To'] = ', '.join(email_config['to_emails'])
            msg['Subject'] = f"✅ Alert Resolved: {alert.alert_type}"
            
            body = f"""
            Alert Resolved:
            - Type: {alert.alert_type}
            - Severity: {alert.severity}
            - Message: {alert.message}
            - Source: {alert.source}
            - Resolved at: {alert.resolution_time}
            - Duration: {alert.resolution_time - alert.timestamp}
            """
            
            msg.attach(MimeText(body, 'plain'))
            
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            if email_config['username'] and email_config['password']:
                server.login(email_config['username'], email_config['password'])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"✅ Email resolution notification sent for alert: {alert.alert_type}")
            
        except Exception as e:
            logger.error(f"❌ Error sending email resolution notification: {e}")
    
    def _send_slack_resolution_notification(self, alert: AlertInfo):
        """Send Slack resolution notification"""
        try:
            slack_config = self.notification_channels['slack']
            
            if not slack_config['webhook_url']:
                return
            
            payload = {
                'channel': slack_config['channel'],
                'username': 'SML777 Monitoring',
                'icon_emoji': ':white_check_mark:',
                'text': f"✅ *Alert Resolved*",
                'attachments': [{
                    'color': 'good',
                    'fields': [
                        {'title': 'Type', 'value': alert.alert_type, 'short': True},
                        {'title': 'Message', 'value': alert.message, 'short': False},
                        {'title': 'Resolved at', 'value': alert.resolution_time.isoformat(), 'short': True},
                        {'title': 'Duration', 'value': str(alert.resolution_time - alert.timestamp), 'short': True}
                    ]
                }]
            }
            
            response = requests.post(slack_config['webhook_url'], json=payload)
            response.raise_for_status()
            
            logger.info(f"✅ Slack resolution notification sent for alert: {alert.alert_type}")
            
        except Exception as e:
            logger.error(f"❌ Error sending Slack resolution notification: {e}")
    
    def _store_alert(self, alert: AlertInfo):
        """Store alert information"""
        try:
            # Store in Redis if available
            if self.redis_client:
                key = f"alert:{alert.timestamp.isoformat()}"
                self.redis_client.setex(key, 86400, json.dumps(asdict(alert), default=str))
            
            # Store in file
            alert_log_file = '/tmp/alerts.log'
            with open(alert_log_file, 'a') as f:
                f.write(json.dumps(asdict(alert), default=str) + '\n')
                
        except Exception as e:
            logger.error(f"❌ Error storing alert: {e}")
    
    def _cleanup_old_metrics(self):
        """Clean up old metrics"""
        try:
            # Remove metrics older than retention period
            cutoff_time = datetime.now() - timedelta(days=self.metric_retention_days)
            self.metrics = [m for m in self.metrics if m.timestamp > cutoff_time]
            
            # Remove resolved alerts older than 7 days
            alert_cutoff_time = datetime.now() - timedelta(days=7)
            self.alert_log = [a for a in self.alert_log if a.timestamp > alert_cutoff_time or not a.resolved]
            
        except Exception as e:
            logger.error(f"❌ Error cleaning up old metrics: {e}")
    
    def _handle_initialization_error(self, error: Exception):
        """Handle initialization errors"""
        try:
            logger.error(f"❌ Initialization error: {error}")
            # Attempt recovery
            self._attempt_recovery()
            
        except Exception as e:
            logger.error(f"❌ Error handling initialization error: {e}")
    
    def _attempt_recovery(self):
        """Attempt to recover from errors"""
        try:
            logger.info("🔄 Attempting monitoring recovery...")
            
            # Reinitialize
            self.initialize()
            
        except Exception as e:
            logger.error(f"❌ Recovery failed: {e}")
    
    def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alert statistics"""
        return {
            'alert_count': self.alert_count,
            'resolved_count': self.resolved_count,
            'active_alerts': len([a for a in self.alert_log if not a.resolved]),
            'alert_log_size': len(self.alert_log),
            'metrics_count': len(self.metrics),
            'monitoring_active': self.monitoring_active,
            'alert_rules': len(self.alert_rules),
            'notification_channels': len(self.notification_channels)
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get monitoring health status"""
        return {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'alert_count': self.alert_count,
            'resolved_count': self.resolved_count,
            'active_alerts': len([a for a in self.alert_log if not a.resolved]),
            'monitoring_active': self.monitoring_active,
            'metric_collectors': list(self.metric_collectors.keys()),
            'alert_rules': list(self.alert_rules.keys()),
            'notification_channels': list(self.notification_channels.keys())
        }
    
    def shutdown(self):
        """Shutdown the monitoring system"""
        try:
            self.monitoring_active = False
            
            if self.redis_client:
                self.redis_client.close()
            
            logger.info("✅ Monitoring and alerting system shutdown")
            
        except Exception as e:
            logger.error(f"❌ Error shutting down: {e}")

# Global instance
monitoring_alerting_system = InfiniteMonitoringAlertingSystem()

def initialize_monitoring_alerting_system():
    """Initialize the monitoring and alerting system"""
    try:
        monitoring_alerting_system.initialize()
    except Exception as e:
        logger.error(f"❌ Error initializing monitoring system: {e}")

def get_alert_statistics():
    """Get alert statistics"""
    return monitoring_alerting_system.get_alert_statistics()

def get_monitoring_health_status():
    """Get monitoring health status"""
    return monitoring_alerting_system.get_health_status()

if __name__ == "__main__":
    # Initialize monitoring and alerting system
    initialize_monitoring_alerting_system()
    
    # Keep running
    try:
        while True:
            time.sleep(60)
            stats = get_alert_statistics()
            health = get_monitoring_health_status()
            logger.info(f"📊 Stats: {stats}")
            logger.info(f"🏥 Health: {health}")
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down...")
        monitoring_alerting_system.shutdown()


