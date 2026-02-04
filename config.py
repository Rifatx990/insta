class ConfigManager:
    """
    Secure configuration handler with environment variable support
    and encrypted storage for sensitive data
    """
    def __init__(self):
        self.config = {
            'instagram': {
                'username': os.getenv('INSTAGRAM_USERNAME'),
                'password': os.getenv('INSTAGRAM_PASSWORD'),
                'cookies_path': 'secured/cookies.json.enc',
                'session_path': 'secured/session.enc'
            },
            'proxy': {
                'enabled': bool(os.getenv('USE_PROXY')),
                'socks5_url': os.getenv('SOCKS5_PROXY'),
                'username': os.getenv('PROXY_USER'),
                'password': os.getenv('PROXY_PASS')
            },
            'scheduler': {
                'timezone': 'Asia/Dhaka',
                'max_retries': 3,
                'retry_delay': 30  # seconds
            },
            'security': {
                'encryption_key': os.getenv('ENCRYPTION_KEY') or Fernet.generate_key()
            }
        }
