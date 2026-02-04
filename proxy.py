class SOCKS5ProxyHandler:
    """
    Manages SOCKS5 proxy configuration with authentication support
    """
    def __init__(self, config):
        self.config = config['proxy']
        self.proxy_url = self._parse_proxy_url()
        
    def get_proxy_config(self):
        """Return proxy configuration for browser automation"""
        if not self.config['enabled']:
            return None
            
        return {
            'server': f'socks5://{self.proxy_url["host"]}:{self.proxy_url["port"]}',
            'username': self.proxy_url.get('username'),
            'password': self.proxy_url.get('password')
        }
    
    def rotate_proxy(self, new_proxy_url):
        """Dynamically update proxy configuration"""
        self.proxy_url = self._parse_proxy_url(new_proxy_url)
