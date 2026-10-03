import logging
from fastapi import APIRouter, Request, Response, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.whatsapp_service import whatsapp_service
from app.services.bot_engine import bot_engine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["WhatsApp Webhook"])

@router.get("")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    """
    Webhook verification endpoint for Meta WhatsApp Cloud API setup.
    """
    challenge = whatsapp_service.verify_webhook(hub_mode, hub_verify_token, hub_challenge)
    if challenge:
        return Response(content=challenge, media_type="text/plain", status_code=status.HTTP_200_OK)
    return Response(content="Verification failed", status_code=status.HTTP_403_FORBIDDEN)


@router.post("")
async def receive_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Receive incoming messages and status events from WhatsApp Cloud API.
    """
    try:
        body = await request.json()
        logger.info(f"Incoming Webhook Payload: {body}")

        # Validate structure from Meta WhatsApp
        entries = body.get("entry", [])
        for entry in entries:
            changes = entry.get("changes", [])
            for change in changes:
                value = change.get("value", {})
                messages = value.get("messages", [])
                
                for msg in messages:
                    from_phone = msg.get("from")
                    msg_type = msg.get("type")
                    text_body = ""

                    if msg_type == "text":
                        text_body = msg.get("text", {}).get("body", "")
                    elif msg_type == "interactive":
                        # Handle button reply or list reply
                        interactive = msg.get("interactive", {})
                        if interactive.get("type") == "button_reply":
                            text_body = interactive.get("button_reply", {}).get("id", "")
                        elif interactive.get("type") == "list_reply":
                            text_body = interactive.get("list_reply", {}).get("id", "")

                    if from_phone and text_body:
                        # Process message through bot engine
                        reply_text = bot_engine.process_incoming_message(db, from_phone, text_body)
                        
                        # Send response via WhatsApp API
                        await whatsapp_service.send_text_message(from_phone, reply_text)

        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error handling webhook: {e}")
        return {"status": "error", "message": str(e)}
