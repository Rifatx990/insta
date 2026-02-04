class StructuredLogger:
    """JSON-structured logging for monitoring and debugging"""
    def __init__(self):
        self.logger = logging.getLogger('instagram_dm_bot')
        
    def log_event(self, event_type, data, level='info'):
        """Log structured events for easy parsing"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'timezone': 'Asia/Dhaka',
            'event': event_type,
            'data': data,
            'level': level
        }
        
        # Write to file
        with open('logs/instagram_dm.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
        
        # Optional: Send to monitoring service
        if self.config.monitoring_webhook:
            await self._send_to_webhook(log_entry)
