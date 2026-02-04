async def main_workflow():
    """
    Complete automated workflow from scheduling to delivery
    """
    # 1. Initialize system
    config = ConfigManager()
    scheduler = DhakaTimezoneScheduler()
    proxy_handler = SOCKS5ProxyHandler(config)
    authenticator = InstagramAuthenticator(config, proxy_handler)
    
    # 2. Authentication (if needed)
    if not await authenticator.is_authenticated():
        await authenticator.authenticate()
    
    # 3. Load scheduled messages from database
    messages = await MessageQueue.load_pending_messages()
    
    # 4. Schedule each message
    for message in messages:
        job = MessageJob(
            recipient=message['recipient'],
            text=message['text'],
            image_path=message['image'],
            scheduled_time=message['scheduled_time']
        )
        scheduler.schedule_message(job)
    
    # 5. Start scheduler
    scheduler.start()
    
    # 6. Monitor and handle failures
    await monitor_and_recover()

class MessageJob:
    """Individual message job with execution logic"""
    async def execute(self):
        """Execute message sending at scheduled time"""
        logger.info(f"Executing message job {self.id} at {datetime.now()}")
        
        sender = InstagramMessageSender(authenticator)
        result = await sender.send_direct_message(
            recipient=self.recipient,
            message=self.text,
            image_path=self.image_path
        )
        
        # Update delivery status
        await self._update_delivery_status(result)
        
        # Optional: Send webhook notification
        if result['success']:
            await self._send_notification('delivered')
