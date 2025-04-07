import boto3
import re
import email.mime.multipart
import email.mime.text
import email.mime.application
import base64
from typing import Dict, Union, List, Optional, Any
from common.enums import EmailContentType, EmailPriority
from botocore.exceptions import ClientError
import os


class SESHandler:
    def __init__(self, region_name: Optional[str] = None):
        """
        Inicializa o handler do SES.

        Args:
            region_name: Região AWS opcional. Se não fornecida, usa a região padrão.
        """
        # Obter credenciais AWS das variáveis de ambiente
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        # Configurar o cliente SES com as credenciais obtidas do ambiente
        if region_name:
            self.ses_client = boto3.client(
                "ses",
                region_name=region_name,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            )
        else:
            self.ses_client = boto3.client(
                "ses",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            )

        self._email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def send_email(
        self,
        destination: Union[str, List[str]],
        subject: str,
        body: Union[str, Dict[str, str]],
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        reply_to: Optional[Union[str, List[str]]] = None,
        content_type: EmailContentType = EmailContentType.TEXT,
        priority: Optional[EmailPriority] = None,
        configuration_set: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        source: str = os.getenv("DOGS_CLUB_EMAIL"),
    ) -> Dict:
        """
        Envia um email usando o Amazon SES.

        Args:
            source: Email do remetente
            destination: Email(s) do(s) destinatário(s)
            subject: Assunto do email
            body: Corpo do email
            cc: Email(s) em cópia
            bcc: Email(s) em cópia oculta
            reply_to: Email(s) para resposta
            content_type: Tipo de conteúdo do email
            priority: Prioridade do email
            configuration_set: Nome do conjunto de configuração do SES
            attachments: Lista de anexos no formato [{"name": "file.pdf", "content": bytes, "content_type": "application/pdf"}]

        Returns:
            Dict: Resposta do AWS SES
        """
        # Valida emails
        self._validate_email(source)

        # Converte destinos únicos em listas
        to_addresses = [destination] if isinstance(destination, str) else destination
        cc_addresses = [cc] if isinstance(cc, str) else cc if cc else []
        bcc_addresses = [bcc] if isinstance(bcc, str) else bcc if bcc else []
        reply_addresses = (
            [reply_to] if isinstance(reply_to, str) else reply_to if reply_to else []
        )

        # Valida todos os emails
        self._validate_emails(to_addresses)
        self._validate_emails(cc_addresses) if cc_addresses else None
        self._validate_emails(bcc_addresses) if bcc_addresses else None
        self._validate_emails(reply_addresses) if reply_addresses else None

        # Se houver anexos, usar a API de mensagem MIME
        if attachments:
            message = self._build_mime_message(
                source,
                to_addresses,
                cc_addresses,
                bcc_addresses,
                subject,
                body,
                content_type,
                attachments,
                priority,
            )

            send_params = {
                "Source": source,
                "RawMessage": {"Data": message.as_string()},
            }

            if configuration_set:
                send_params["ConfigurationSetName"] = configuration_set

            try:
                response = self.ses_client.send_raw_email(**send_params)
                return response
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                error_message = e.response["Error"]["Message"]
                raise Exception(
                    f"Failed to send email. Error code: {error_code}. Message: {error_message}"
                )

        # Se não tiver anexos, usar a API padrão
        else:
            # Constrói a mensagem
            message = self._build_message(subject, body, content_type, priority)

            # Prepara o destino
            destination_dict = {"ToAddresses": to_addresses}
            if cc_addresses:
                destination_dict["CcAddresses"] = cc_addresses
            if bcc_addresses:
                destination_dict["BccAddresses"] = bcc_addresses

            # Prepara os parâmetros de envio
            send_params = {
                "Source": source,
                "Destination": destination_dict,
                "Message": message,
            }

            # Adiciona parâmetros opcionais
            if reply_addresses:
                send_params["ReplyToAddresses"] = reply_addresses
            if configuration_set:
                send_params["ConfigurationSetName"] = configuration_set
            if priority:
                tags = [{"Name": "X-Priority", "Value": priority.value}]
                send_params["Tags"] = tags

            try:
                response = self.ses_client.send_email(**send_params)
                return response
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                error_message = e.response["Error"]["Message"]
                raise Exception(
                    f"Failed to send email. Error code: {error_code}. Message: {error_message}"
                )

    def verify_email_identity(self, email: str) -> Dict:
        """
        Verifica uma identidade de email no SES.

        Args:
            email: Endereço de email para verificar
        """
        if not self._validate_email(email):
            raise ValueError(f"Invalid email address: {email}")

        try:
            response = self.ses_client.verify_email_identity(EmailAddress=email)
            return response
        except ClientError as e:
            raise Exception(f"Failed to verify email identity: {str(e)}")

    def get_send_quota(self) -> Dict:
        """Retorna as cotas de envio do SES."""
        try:
            return self.ses_client.get_send_quota()
        except ClientError as e:
            raise Exception(f"Failed to get send quota: {str(e)}")

    def get_send_statistics(self) -> Dict:
        """Retorna estatísticas de envio do SES."""
        try:
            return self.ses_client.get_send_statistics()
        except ClientError as e:
            raise Exception(f"Failed to get send statistics: {str(e)}")

    def send_bulk_templated_email(
        self,
        source: str,
        template_name: str,
        destinations: List[Dict[str, Union[List[str], Dict]]],
        configuration_set: Optional[str] = None,
    ) -> Dict:
        """
        Envia emails em massa usando um template.

        Args:
            source: Email do remetente
            template_name: Nome do template no SES
            destinations: Lista de destinos com seus dados
            configuration_set: Nome do conjunto de configuração do SES
        """
        self._validate_email(source)

        send_params = {
            "Source": source,
            "Template": template_name,
            "Destinations": destinations,
        }

        if configuration_set:
            send_params["ConfigurationSetName"] = configuration_set

        try:
            response = self.ses_client.send_bulk_templated_email(**send_params)
            return response
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            raise Exception(
                f"Failed to send bulk email. Error code: {error_code}. Message: {error_message}"
            )

    def create_template(
        self,
        template_name: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> Dict:
        """
        Cria um template de email no SES.

        Args:
            template_name: Nome do template
            subject: Linha de assunto do template
            html_content: Conteúdo HTML do template
            text_content: Conteúdo em texto plano do template (opcional)
        """
        template = {
            "TemplateName": template_name,
            "SubjectPart": subject,
            "HtmlPart": html_content,
        }

        if text_content:
            template["TextPart"] = text_content

        try:
            response = self.ses_client.create_template(Template=template)
            return response
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            raise Exception(
                f"Failed to create template. Error code: {error_code}. Message: {error_message}"
            )

    def _validate_email(self, email: str) -> bool:
        """Valida o formato do email."""
        return bool(re.match(self._email_regex, email))

    def _validate_emails(self, emails: List[str]) -> None:
        """Valida uma lista de emails."""
        invalid_emails = [email for email in emails if not self._validate_email(email)]
        if invalid_emails:
            raise ValueError(f"Invalid email addresses: {', '.join(invalid_emails)}")

    def _build_message(
        self,
        subject: str,
        body: Union[str, Dict[str, str]],
        content_type: EmailContentType = EmailContentType.TEXT,
        priority: Optional[EmailPriority] = None,
    ) -> Dict:
        """
        Constrói a estrutura da mensagem do email.

        Args:
            subject: Assunto do email
            body: Corpo do email (string para texto plano/html ou dict para ambos)
            content_type: Tipo de conteúdo do email
            priority: Prioridade do email (opcional)
        """
        message: Dict = {"Subject": {"Data": subject, "Charset": "UTF-8"}}

        body_content = {}

        if content_type == EmailContentType.BOTH:
            if not isinstance(body, dict) or not all(
                k in body for k in ["Text", "Html"]
            ):
                raise ValueError(
                    "For BOTH content type, body must be a dict with 'Text' and 'Html' keys"
                )
            body_content = {
                "Text": {"Data": body["Text"], "Charset": "UTF-8"},
                "Html": {"Data": body["Html"], "Charset": "UTF-8"},
            }
        else:
            content_key = content_type.value
            body_content = {content_key: {"Data": body, "Charset": "UTF-8"}}

        message["Body"] = body_content
        return message

    def _build_mime_message(
        self,
        source: str,
        to_addresses: List[str],
        cc_addresses: List[str],
        bcc_addresses: List[str],
        subject: str,
        body: Union[str, Dict[str, str]],
        content_type: EmailContentType = EmailContentType.TEXT,
        attachments: List[Dict[str, Any]] = None,
        priority: Optional[EmailPriority] = None,
    ) -> email.mime.multipart.MIMEMultipart:
        """
        Constrói uma mensagem MIME para envio com anexos.

        Args:
            source: Email do remetente
            to_addresses: Lista de destinatários
            cc_addresses: Lista de emails em cópia
            bcc_addresses: Lista de emails em cópia oculta
            subject: Assunto do email
            body: Corpo do email
            content_type: Tipo de conteúdo (texto ou HTML)
            attachments: Lista de anexos
            priority: Prioridade do email

        Returns:
            MIMEMultipart: Mensagem no formato MIME
        """
        # Criar a estrutura base da mensagem
        message = email.mime.multipart.MIMEMultipart()
        message["Subject"] = subject
        message["From"] = source
        message["To"] = ", ".join(to_addresses)

        if cc_addresses:
            message["Cc"] = ", ".join(cc_addresses)
        if bcc_addresses:
            message["Bcc"] = ", ".join(bcc_addresses)
        if priority:
            message["X-Priority"] = priority.value

        # Anexar o corpo da mensagem
        if content_type == EmailContentType.HTML:
            part = email.mime.text.MIMEText(body, "html", "utf-8")
            message.attach(part)
        elif content_type == EmailContentType.TEXT:
            part = email.mime.text.MIMEText(body, "plain", "utf-8")
            message.attach(part)
        elif content_type == EmailContentType.BOTH:
            if not isinstance(body, dict) or not all(
                k in body for k in ["Text", "Html"]
            ):
                raise ValueError(
                    "For BOTH content type, body must be a dict with 'Text' and 'Html' keys"
                )
            # Anexar parte texto
            part1 = email.mime.text.MIMEText(body["Text"], "plain", "utf-8")
            message.attach(part1)
            # Anexar parte HTML
            part2 = email.mime.text.MIMEText(body["Html"], "html", "utf-8")
            message.attach(part2)

        # Anexar os arquivos
        if attachments:
            for attachment in attachments:
                name = attachment["name"]
                content = attachment["content"]
                content_type = attachment.get(
                    "content_type", "application/octet-stream"
                )

                # Criar o anexo
                if isinstance(content, str) and content.startswith(
                    ("http://", "https://")
                ):
                    # Tratar URLs
                    import requests

                    response = requests.get(content)
                    part = email.mime.application.MIMEApplication(response.content)
                elif isinstance(content, bytes):
                    # Conteúdo já está em bytes
                    part = email.mime.application.MIMEApplication(content)
                else:
                    # Tentar converter para bytes
                    part = email.mime.application.MIMEApplication(bytes(content))

                # Adicionar cabeçalhos e anexar
                part.add_header("Content-Disposition", f"attachment; filename={name}")
                part.add_header("Content-Type", content_type)
                message.attach(part)

        return message
