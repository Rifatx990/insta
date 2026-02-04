class SecureStorage:
    """Encrypted storage for credentials and sessions"""
    def __init__(self, encryption_key):
        self.cipher = Fernet(encryption_key)
    
    def encrypt_data(self, data):
        """Encrypt sensitive data before storage"""
        return self.cipher.encrypt(json.dumps(data).encode())
    
    def decrypt_data(self, encrypted_data):
        """Decrypt data for use"""
        return json.loads(self.cipher.decrypt(encrypted_data))
    
    def secure_cookie_storage(self, cookies):
        """Store cookies with encryption and expiration"""
        encrypted = self.encrypt_data({
            'cookies': cookies,
            'expires_at': datetime.now() + timedelta(days=7),
            'user_agent': self.browser.user_agent
        })
        with open(self.config.cookies_path, 'wb') as f:
            f.write(encrypted)
