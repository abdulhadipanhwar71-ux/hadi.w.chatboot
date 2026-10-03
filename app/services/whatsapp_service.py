import logging
import httpx
from typing import Optional, Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)

class WhatsAppService:
    """Service to interact with Meta WhatsApp Cloud API."""

    def __init__(self):
        self.api_version = settings.WHATSAPP_API_VERSION
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.token = settings.WHATSAPP_TOKEN
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/messages"

    async def send_text_message(self, to_phone: str, message: str) -> Dict[str, Any]:
        """
        Send a regular plain text message to a WhatsApp user.
        If credentials are not configured, log and return simulation payload.
        """
        # Clean phone number (strip spaces, dashes, plus signs)
        clean_phone = to_phone.replace("+", "").replace("-", "").replace(" ", "")

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": clean_phone,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
            }
        }

        # Check if production credentials are provided
        if not self.token or not self.phone_number_id:
            logger.info(f"[SIMULATED/OFFLINE OUTGOING to {clean_phone}]:\n{message}")
            return {"status": "simulated", "to": clean_phone, "message": message}

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(self.base_url, headers=headers, json=payload)
                response_json = response.json()
                
                if response.status_code >= 400:
                    logger.error(f"WhatsApp API error ({response.status_code}): {response_json}")
                else:
                    logger.info(f"WhatsApp message sent successfully to {clean_phone}")
                
                return response_json
        except Exception as e:
            logger.error(f"Failed to communicate with WhatsApp API: {e}")
            return {"status": "error", "error": str(e)}

    def verify_webhook(self, mode: Optional[str], token: Optional[str], challenge: Optional[str]) -> Optional[str]:
        """
        Verify incoming Meta WhatsApp webhook subscription token.
        """
        if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
            logger.info("WhatsApp Webhook verified successfully.")
            return challenge
        logger.warning("WhatsApp Webhook verification failed: token mismatch.")
        return None

whatsapp_service = WhatsAppService()
