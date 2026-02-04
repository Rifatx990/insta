class InstagramAuthenticator:
    """
    Handles secure login, session persistence, and challenge resolution
    """
    def __init__(self, config, proxy_handler):
        self.config = config
        self.proxy_handler = proxy_handler
        self.cookie_jar = EncryptedCookieJar(config)
        self.browser = None
        
    async def authenticate(self):
        """Main authentication flow with fallback mechanisms"""
        # 1. Try loading existing session
        if await self._load_persisted_session():
            if await self._validate_session():
                return True
        
        # 2. Perform fresh login
        return await self._perform_login()
    
    async def _perform_login(self):
        """Secure login with proxy support and checkpoint handling"""
        self.browser = await self._create_browser_with_proxy()
        
        # Navigate to Instagram
        await self.browser.goto('https://www.instagram.com/')
        
        # Fill credentials
        await self.browser.fill('input[name="username"]', self.config.username)
        await self.browser.fill('input[name="password"]', self.config.password)
        
        # Handle 2FA/checkpoint if present
        if await self._detect_checkpoint():
            await self._handle_checkpoint()
        
        # Save session securely
        await self._save_session()
        
    def _create_browser_with_proxy(self):
        """Create browser instance with SOCKS5 proxy configuration"""
        browser_args = {
            'headless': self.config.headless,
            'proxy': self.proxy_handler.get_proxy_config()
        }
        return playwright.chromium.launch(**browser_args)
