class ErrorHandler:
    """
    Comprehensive error detection and recovery system
    """
    ERROR_CODES = {
        'SESSION_EXPIRED': ['login_required', 'invalid_session'],
        'CHECKPOINT_REQUIRED': ['checkpoint_required', 'challenge_required'],
        'RATE_LIMITED': ['rate_limit', 'too_many_requests'],
        'NETWORK_ERROR': ['timeout', 'connection_error']
    }
    
    async def handle_error(self, error, context):
        """Determine error type and execute recovery strategy"""
        error_type = self._classify_error(error)
        
        if error_type in ['SESSION_EXPIRED', 'CHECKPOINT_REQUIRED']:
            return await self._reauthenticate()
        elif error_type == 'RATE_LIMITED':
            return await self._handle_rate_limit()
        elif error_type == 'NETWORK_ERROR':
            return await self._retry_with_backoff(context)
        
    async def _retry_with_backoff(self, context, max_retries=3):
        """Exponential backoff retry logic"""
        for attempt in range(max_retries):
            try:
                return await context['operation']()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                delay = (2 ** attempt) * self.config.retry_delay
                await asyncio.sleep(delay)
