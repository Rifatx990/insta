class DhakaTimezoneScheduler:
    """
    APScheduler-based scheduler locked to Asia/Dhaka timezone
    """
    def __init__(self):
        self.timezone = pytz.timezone('Asia/Dhaka')
        self.scheduler = BackgroundScheduler(timezone=self.timezone)
        
    def schedule_message(self, message_job):
        """Schedule a message for exact delivery in BD time"""
        # Convert user input to timezone-aware datetime
        scheduled_time = self._parse_scheduled_time(
            message_job.scheduled_time_str,
            message_job.scheduled_date_str
        )
        
        # Add job to scheduler
        self.scheduler.add_job(
            func=message_job.execute,
            trigger='date',
            run_date=scheduled_time,
            id=message_job.id,
            replace_existing=True,
            timezone=self.timezone
        )
    
    def _parse_scheduled_time(self, time_str, date_str):
        """Parse and convert to Asia/Dhaka timezone"""
        # Example: "08 October, 12:00 AM"
        naive_datetime = datetime.strptime(
            f"{date_str}, {time_str}",
            "%d %B, %I:%M %p"
        ).replace(year=datetime.now().year)
        
        # Localize to Asia/Dhaka
        return self.timezone.localize(naive_datetime)
