from typing import List, Optional, Dict, Any
from datetime import datetime
import httpx
from core.config import settings
from core.logging import get_logger
import json


logger = get_logger("notifications")


class EmailService:
    """Serviço para envio de emails via SendGrid"""
    
    def __init__(self):
        self.api_key = settings.SENDGRID_API_KEY
        self.base_url = "https://api.sendgrid.com/v3"
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        content: str,
        from_email: str = "noreply@tms.com",
        template_id: Optional[str] = None,
        template_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Enviar email"""
        
        if not self.api_key:
            logger.warning("SendGrid API key não configurada")
            return False
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "personalizations": [
                    {
                        "to": [{"email": to_email}],
                        "subject": subject
                    }
                ],
                "from": {"email": from_email},
                "content": [
                    {
                        "type": "text/html",
                        "value": content
                    }
                ]
            }
            
            if template_id and template_data:
                data["template_id"] = template_id
                data["personalizations"][0]["dynamic_template_data"] = template_data
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/mail/send",
                    headers=headers,
                    json=data
                )
                
                if response.status_code == 202:
                    logger.info("Email enviado com sucesso", to_email=to_email, subject=subject)
                    return True
                else:
                    logger.error("Erro ao enviar email", 
                               status_code=response.status_code, 
                               response=response.text)
                    return False
                    
        except Exception as e:
            logger.error("Erro ao enviar email", error=str(e))
            return False
    
    async def send_trip_status_notification(
        self,
        to_email: str,
        trip_id: int,
        status: str,
        client_name: str,
        estimated_arrival: datetime
    ) -> bool:
        """Enviar notificação de mudança de status de viagem"""
        
        subject = f"Atualização da Viagem #{trip_id} - {status.title()}"
        
        content = f"""
        <html>
        <body>
            <h2>Atualização da Viagem</h2>
            <p>Olá {client_name},</p>
            <p>A viagem #{trip_id} teve seu status atualizado para: <strong>{status.title()}</strong></p>
            <p>Chegada estimada: {estimated_arrival.strftime('%d/%m/%Y %H:%M')}</p>
            <p>Acompanhe sua viagem em tempo real através do nosso sistema.</p>
            <br>
            <p>Atenciosamente,<br>Equipe TMS</p>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, content)


class WhatsAppService:
    """Serviço para envio de mensagens WhatsApp via Twilio"""
    
    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.phone_number = settings.TWILIO_PHONE_NUMBER
    
    async def send_whatsapp(
        self,
        to_phone: str,
        message: str
    ) -> bool:
        """Enviar mensagem WhatsApp"""
        
        if not all([self.account_sid, self.auth_token, self.phone_number]):
            logger.warning("Twilio não configurado")
            return False
        
        try:
            url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json"
            
            data = {
                "From": f"whatsapp:{self.phone_number}",
                "To": f"whatsapp:{to_phone}",
                "Body": message
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    data=data,
                    auth=(self.account_sid, self.auth_token)
                )
                
                if response.status_code == 201:
                    logger.info("WhatsApp enviado com sucesso", to_phone=to_phone)
                    return True
                else:
                    logger.error("Erro ao enviar WhatsApp", 
                               status_code=response.status_code, 
                               response=response.text)
                    return False
                    
        except Exception as e:
            logger.error("Erro ao enviar WhatsApp", error=str(e))
            return False
    
    async def send_trip_status_whatsapp(
        self,
        to_phone: str,
        trip_id: int,
        status: str,
        client_name: str,
        estimated_arrival: datetime
    ) -> bool:
        """Enviar notificação WhatsApp de mudança de status de viagem"""
        
        message = f"""
🚛 Atualização da Viagem #{trip_id}

Olá {client_name}!

Status atualizado para: {status.title()}
Chegada estimada: {estimated_arrival.strftime('%d/%m/%Y %H:%M')}

Acompanhe sua viagem em tempo real através do nosso sistema.

Equipe TMS
        """
        
        return await self.send_whatsapp(to_phone, message)


class NotificationService:
    """Serviço principal de notificações"""
    
    def __init__(self):
        self.email_service = EmailService()
        self.whatsapp_service = WhatsAppService()
    
    async def send_trip_status_notification(
        self,
        trip_id: int,
        status: str,
        client_email: str,
        client_phone: str,
        client_name: str,
        estimated_arrival: datetime,
        send_email: bool = True,
        send_whatsapp: bool = True
    ) -> Dict[str, bool]:
        """Enviar notificação de mudança de status de viagem"""
        
        results = {}
        
        if send_email and client_email:
            results["email"] = await self.email_service.send_trip_status_notification(
                client_email, trip_id, status, client_name, estimated_arrival
            )
        
        if send_whatsapp and client_phone:
            results["whatsapp"] = await self.whatsapp_service.send_trip_status_whatsapp(
                client_phone, trip_id, status, client_name, estimated_arrival
            )
        
        return results
    
    async def send_maintenance_alert(
        self,
        vehicle_plate: str,
        maintenance_type: str,
        due_date: datetime,
        admin_emails: List[str]
    ) -> Dict[str, bool]:
        """Enviar alerta de manutenção"""
        
        subject = f"Alerta de Manutenção - Veículo {vehicle_plate}"
        content = f"""
        <html>
        <body>
            <h2>Alerta de Manutenção</h2>
            <p>O veículo <strong>{vehicle_plate}</strong> precisa de manutenção {maintenance_type}.</p>
            <p>Data limite: {due_date.strftime('%d/%m/%Y')}</p>
            <p>Acesse o sistema para agendar a manutenção.</p>
        </body>
        </html>
        """
        
        results = {}
        for email in admin_emails:
            results[email] = await self.email_service.send_email(email, subject, content)
        
        return results
    
    async def send_document_expiry_alert(
        self,
        document_type: str,
        document_number: str,
        expiry_date: datetime,
        admin_emails: List[str]
    ) -> Dict[str, bool]:
        """Enviar alerta de documento vencendo"""
        
        subject = f"Alerta de Documento - {document_type} vencendo"
        content = f"""
        <html>
        <body>
            <h2>Alerta de Documento</h2>
            <p>O documento <strong>{document_type}</strong> número <strong>{document_number}</strong> vence em {expiry_date.strftime('%d/%m/%Y')}.</p>
            <p>Renove o documento para evitar problemas operacionais.</p>
        </body>
        </html>
        """
        
        results = {}
        for email in admin_emails:
            results[email] = await self.email_service.send_email(email, subject, content)
        
        return results