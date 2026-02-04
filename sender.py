class InstagramMessageSender:
    """
    Handles DM delivery with text and images in correct order
    """
    def __init__(self, authenticator):
        self.authenticator = authenticator
        self.browser = authenticator.browser
        
    async def send_direct_message(self, recipient, message, image_path=None):
        """Send text followed by image to specified recipient"""
        try:
            # 1. Navigate to recipient's DM
            await self._navigate_to_recipient(recipient)
            
            # 2. Send text message
            await self._send_text_message(message)
            
            # 3. Send image if provided
            if image_path:
                await self._send_image_attachment(image_path)
                
            # 4. Verify delivery
            return await self._verify_delivery()
            
        except Exception as e:
            await self._handle_send_error(e)
    
    async def _send_text_message(self, message):
        """Send text message to active DM thread"""
        text_area = await self.browser.wait_for_selector(
            'div[contenteditable="true"][aria-label="Message"]'
        )
        await text_area.fill(message)
        await text_area.press('Enter')
        
        # Wait for message to be sent
        await self.browser.wait_for_timeout(2000)
    
    async def _send_image_attachment(self, image_path):
        """Attach and send image file"""
        # Click attachment button
        attachment_btn = await self.browser.wait_for_selector(
            'input[accept="image/*,video/mp4,video/quicktime"]'
        )
        
        # Upload image
        await attachment_btn.set_input_files(image_path)
        
        # Wait for upload and send
        await self.browser.wait_for_selector('svg[aria-label="Share"]')
        send_btn = await self.browser.query_selector('svg[aria-label="Share"]')
        await send_btn.click()
