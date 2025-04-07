import os
import time
from typing import Dict, Any, Optional, List, Union, BinaryIO
from datetime import datetime
import pytz
from handlers.ses import SESHandler
from utils import load_template, replace_template_variables, format_currency
from common.enums import EmailContentType
from io import BytesIO


class EmailHandler:
    """
    Handler para gerenciar o envio de emails do Dog's Club Reports
    """

    def __init__(self, region_name: Optional[str] = None):
        """
        Inicializa o handler de emails.

        Args:
            region_name: Região AWS opcional
        """
        self.ses_handler = SESHandler(region_name=region_name)
        self.source_email = os.getenv("DOGS_CLUB_EMAIL")

    def send_pdf_report(
        self,
        nome: str,
        email: str,
        petshop_name: str,
        faturamento_nao_realizado: float,
        pdf_buffer: Union[BytesIO, BinaryIO],
        cc_emails: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Envia um email com o relatório PDF.

        Args:
            nome: Nome do cliente
            email: Email do cliente
            petshop_name: Nome do petshop
            faturamento_nao_realizado: Valor de faturamento não realizado mensal
            pdf_buffer: Buffer contendo o arquivo PDF
            cc_emails: Lista de emails em cópia

        Returns:
            Dict: Resposta do serviço de email
        """
        try:
            # Carregar o template de email
            template = load_template("pdf_report")

            # Formatar o valor do faturamento não realizado
            formatted_value = format_currency(faturamento_nao_realizado)

            # Timestamp atual em formato EPOCH
            current_timestamp = int(time.time())

            # Para o template, ainda precisamos de uma data formatada para legibilidade
            current_date = datetime.fromtimestamp(current_timestamp).strftime(
                "%d/%m/%Y"
            )

            # Substituir variáveis no template
            variables = {
                "nome": nome,
                "petshop_name": petshop_name,
                "faturamento_nao_realizado": formatted_value,
                "data": current_date,
            }

            email_content = replace_template_variables(template, variables)

            # Preparar o assunto do email
            subject = f"Análise Financeira - {petshop_name}"

            # Nome do arquivo usa timestamp EPOCH
            file_name = f"analise_{petshop_name.replace(' ', '_').lower()}_{current_timestamp}.pdf"

            # Enviar o email com o relatório em anexo
            response = self.ses_handler.send_email(
                source=self.source_email,
                destination=email,
                subject=subject,
                body=email_content,
                cc=cc_emails,
                content_type=EmailContentType.HTML,
                attachments=[
                    {
                        "name": file_name,
                        "content": pdf_buffer.getvalue(),
                        "content_type": "application/pdf",
                    }
                ],
            )

            return {
                "success": True,
                "message_id": response.get("MessageId"),
                "timestamp": current_timestamp,
            }

        except Exception as e:
            return {"success": False, "error": str(e), "timestamp": int(time.time())}

    def send_contact_confirmation(
        self,
        nome: str,
        email: str,
        petshop_name: str,
        mensagem: str,
    ) -> Dict[str, Any]:
        """
        Envia um email de confirmação após receber um contato.

        Args:
            nome: Nome do cliente
            email: Email do cliente
            petshop_name: Nome do petshop
            mensagem: Mensagem enviada pelo cliente

        Returns:
            Dict: Resposta do serviço de email
        """
        try:
            # Carregar o template de email
            template = load_template("contact_confirmation")

            # Timestamp atual em formato EPOCH
            current_timestamp = int(time.time())

            # Para o template, ainda precisamos de uma data formatada para legibilidade
            current_date = datetime.fromtimestamp(current_timestamp).strftime(
                "%d/%m/%Y às %H:%M"
            )

            # Substituir variáveis no template
            variables = {
                "nome": nome,
                "email": email,
                "petshop_name": petshop_name,
                "mensagem": mensagem,
                "data": current_date,
            }

            email_content = replace_template_variables(template, variables)

            # Preparar o assunto do email
            subject = "Recebemos sua mensagem - Dog's Club"

            # Enviar o email de confirmação
            response = self.ses_handler.send_email(
                source=self.source_email,
                destination=email,
                subject=subject,
                body=email_content,
                content_type=EmailContentType.HTML,
            )

            return {
                "success": True,
                "message_id": response.get("MessageId"),
                "timestamp": current_timestamp,
            }

        except Exception as e:
            return {"success": False, "error": str(e), "timestamp": int(time.time())}

    def send_internal_notification(
        self,
        nome: str,
        email: str,
        whatsapp: str,
        petshop_name: str,
        mensagem: str,
        fonte: str,
        internal_recipients: List[str],
    ) -> Dict[str, Any]:
        """
        Envia uma notificação interna para a equipe sobre um novo lead.

        Args:
            nome: Nome do cliente
            email: Email do cliente
            whatsapp: WhatsApp do cliente
            petshop_name: Nome do petshop
            mensagem: Mensagem enviada pelo cliente
            fonte: Fonte de onde o lead foi direcionado
            internal_recipients: Lista de emails internos para receber a notificação

        Returns:
            Dict: Resposta do serviço de email
        """
        try:
            # Timestamp atual em formato EPOCH
            current_timestamp = int(time.time())

            # Para o email, ainda precisamos de uma data formatada para legibilidade
            formatted_date = datetime.fromtimestamp(current_timestamp).strftime(
                "%d/%m/%Y às %H:%M"
            )

            # Carregar o template de email para notificação interna
            print("Carregando template de email para notificação interna")
            template = load_template("new_lead_notification")

            # Substituir variáveis no template
            variables = {
                "nome": nome,
                "email": email,
                "whatsapp": whatsapp,
                "petshop_name": petshop_name,
                "fonte": fonte,
                "data": formatted_date,
                "timestamp": str(current_timestamp),
                "mensagem": mensagem,
            }

            html_content = replace_template_variables(template, variables)
            # Preparar o assunto do email
            subject = f"[NOVO LEAD] {nome} - {petshop_name}"

            # Enviar o email interno
            response = self.ses_handler.send_email(
                source=self.source_email,
                destination=internal_recipients,
                subject=subject,
                body=html_content,
                content_type=EmailContentType.HTML,
                reply_to=email,  # Facilitar a resposta direta ao cliente
            )

            return {
                "success": True,
                "message_id": response.get("MessageId"),
                "timestamp": current_timestamp,
            }

        except Exception as e:
            print("ERRO AO ENVIAR EMAIL INTERNO")
            print("ERROR: ", e)
            return {"success": False, "error": str(e), "timestamp": int(time.time())}
