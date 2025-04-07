import os
import uuid
import time
from typing import Dict, Any, Optional, List
from handlers.dynamodb import DynamoDBHandler
from common.utils import get_timestamp, format_iso_date


class LeadHandler:
    """
    Handler para gerenciar leads do Dog's Club Reports
    """

    def __init__(self):
        """
        Inicializa o handler de leads.

        Args:
            table_name: Nome da tabela DynamoDB para armazenar os leads
        """
        self.dynamodb_handler = DynamoDBHandler(table=os.getenv("LEADS_TABLE"))

    def create_lead(
        self,
        name: str,
        email: str,
        whatsapp: str,
        petshop_name: str,
        message: str,
        source: str = "app",
    ) -> Dict[str, Any]:
        """
        Cria um novo lead no DynamoDB.

        Args:
            name: Nome do cliente
            email: Email do cliente
            whatsapp: Número de WhatsApp do cliente
            petshop_name: Nome do petshop
            message: Mensagem ou observações do cliente
            source: Fonte de onde o lead foi direcionado

        Returns:
            Dict: Dados do lead criado
        """
        lead_id = str(uuid.uuid4())
        current_timestamp = int(time.time())  # Timestamp EPOCH em segundos

        lead_data = {
            "lead_id": lead_id,
            "email": email.lower(),
            "name": name,
            "whatsapp": whatsapp,
            "petshop_name": petshop_name,
            "message": message,
            "source": source,
            "created_at": current_timestamp,
            "date_created": current_timestamp,
        }

        # Salvar no DynamoDB
        self.dynamodb_handler.put_item(lead_data)

        return lead_data

    def get_lead_by_id(self, lead_id: str) -> Dict[str, Any]:
        """
        Busca um lead pelo ID.

        Args:
            lead_id: ID do lead

        Returns:
            Dict: Dados do lead ou vazio se não encontrado
        """
        response = self.dynamodb_handler.get_item({"lead_id": lead_id})
        return response.get("Item", {})

    def get_lead_by_email(self, email: str) -> List[Dict[str, Any]]:
        """
        Busca leads pelo email.

        Args:
            email: Email do cliente

        Returns:
            List[Dict]: Lista de leads com o email fornecido
        """
        response = self.dynamodb_handler.query_using_gsi(
            index_name="email-index", partition_key={"email": email.lower()}
        )
        return response.get("Items", [])

    def get_leads_by_source(self, source: str) -> List[Dict[str, Any]]:
        """
        Busca leads pela fonte de origem.

        Args:
            source: Fonte de origem do lead (ex: "google", "facebook")

        Returns:
            List[Dict]: Lista de leads com a fonte fornecida
        """
        response = self.dynamodb_handler.query_using_gsi(
            index_name="source-index", partition_key={"source": source}
        )
        return response.get("Items", [])

    def update_lead_status(self, lead_id: str, status: str) -> Dict[str, Any]:
        """
        Atualiza o status de um lead.

        Args:
            lead_id: ID do lead
            status: Novo status do lead

        Returns:
            Dict: Resposta da operação de atualização
        """
        return self.dynamodb_handler.update_item(
            key={"lead_id": lead_id}, attributes_to_update={"entity_status": status}
        )

    def add_notes_to_lead(self, lead_id: str, notes: str) -> Dict[str, Any]:
        """
        Adiciona notas a um lead existente.

        Args:
            lead_id: ID do lead
            notes: Notas a serem adicionadas

        Returns:
            Dict: Resposta da operação de atualização
        """
        return self.dynamodb_handler.update_item(
            key={"lead_id": lead_id}, attributes_to_update={"notes": notes}
        )

    def get_all_leads(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Busca todos os leads ativos.

        Args:
            limit: Número máximo de leads a retornar

        Returns:
            List[Dict]: Lista de leads
        """
        scan_params = {
            "FilterExpression": "entity_status = :status",
            "ExpressionAttributeValues": {":status": "active"},
        }

        if limit:
            scan_params["Limit"] = limit

        response = self.dynamodb_handler.scan(**scan_params)
        return response.get("Items", [])
