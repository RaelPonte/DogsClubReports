import boto3
from common.utils import get_timestamp
from typing import Dict, Any
from boto3.dynamodb.conditions import Key, Attr
from boto3.dynamodb.types import TypeDeserializer

from common.enums import EntityStatus, FilterOperator
from typing import Optional, Dict, Union, List, Tuple


class DynamoDBHandler:
    def __init__(self, table: str) -> None:
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(table)

    def put_item(self, item: Dict):
        self.table.put_item(Item=item)

    def get_item(self, key_expression: Dict):
        if len(key_expression) < 1 or len(key_expression) > 2:
            raise ValueError(
                "Only PartitionKey or PartitionKey and SortKey are required"
            )

        response = self.table.get_item(Key=key_expression)
        return response

    def query_using_gsi(
        self,
        index_name: str,
        partition_key: Dict[str, Any],
        filter_conditions: Optional[Dict[str, Dict[str, any]]] = None,
        limit: Optional[int] = None,
        exclusive_start_key: Optional[Dict] = None,
    ):
        """
        Executa uma query usando GSI com suporte a filtros dinâmicos e paginação

        Args:
            index_name: Nome do índice GSI
            partition_key: Dicionário com chave de partição no formato:
                        {"attribute_name": value}
            filter_conditions: Dicionário com condições de filtro no formato:
                            {"attribute_name": {"operator": "between", "value": [min, max]}}
            limit: Número máximo de itens a retornar
            exclusive_start_key: Chave para começar a busca a partir de um ponto específico (paginação)

        Returns:
            Dict: Resposta do DynamoDB
        """
        if not partition_key:
            raise ValueError("PartitionKey is required")

        key_condition_expression = None
        filter_expression = None

        # Processar chave de partição
        for attr_name, value in partition_key.items():
            expr = Key(attr_name)

            if key_condition_expression is None:
                key_condition_expression = expr.eq(value)
            else:
                key_condition_expression &= expr.eq(value)

        # Processar condições de filtro
        if filter_conditions:
            for attr_name, condition in filter_conditions.items():
                operator = condition.get("operator", "eq")
                value = condition["value"]

                current_expr = self._build_filter_expression(attr_name, operator, value)

                if filter_expression is None:
                    filter_expression = current_expr
                else:
                    filter_expression &= current_expr

        # Preparar parâmetros da consulta
        query_params = {
            "IndexName": index_name,
            "KeyConditionExpression": key_condition_expression,
        }

        # Adicionar expressão de filtro se existir
        if filter_expression is not None:
            query_params["FilterExpression"] = filter_expression

        # Adicionar limit se fornecido
        if limit is not None:
            query_params["Limit"] = limit

        # Adicionar chave de início exclusiva para paginação
        if exclusive_start_key is not None:
            query_params["ExclusiveStartKey"] = exclusive_start_key

        # Executar a consulta
        response = self.table.query(**query_params)
        return response

    def query_by_partition_key(self, partition_key: str, value: str):
        response = self.table.query(KeyConditionExpression=Key(partition_key).eq(value))
        return response

    def query_by_partition_key_and_more_keys(
        self, partition_key: str, partition_key_value: str, more_keys: Dict
    ):
        key_condition_expression = Key(partition_key).eq(partition_key_value)
        filter_expression = None
        for key, value in more_keys.items():
            if filter_expression is None:
                filter_expression = Attr(key).eq(value)
            else:
                filter_expression &= Attr(key).eq(value)

        response = self.table.query(
            KeyConditionExpression=key_condition_expression,
            FilterExpression=filter_expression,
        )
        return response

    def delete_item(self, key: Dict, force_delete: bool = True):
        if force_delete:
            response = self.table.delete_item(Key=key)
        else:
            response = self.update_item(
                key=key,
                attributes_to_update={
                    "entity_status": EntityStatus.DELETED.value,
                    "deleted_at": get_timestamp(),
                },
            )
        return response

    def update_item(
        self,
        key: Dict,
        attributes_to_update: Dict,
        condition_expression: Optional[str] = None,
        condition_values: Optional[Dict] = None,
    ):
        """
        Atualiza um item na tabela do DynamoDB com suporte a expressões de condição.

        Args:
            key: Dicionário com a chave primária do item
            attributes_to_update: Dicionário com os atributos a serem atualizados
            condition_expression: Expressão de condição para a atualização (opcional)
            condition_values: Valores para a expressão de condição (opcional)

        Returns:
            Dict: Resposta do DynamoDB
        """
        update_at = get_timestamp()

        # Preparar partes da expressão de atualização
        update_parts = []
        expression_attribute_values = {}

        # Processar todos os atributos a serem atualizados
        for field, value in attributes_to_update.items():
            field_placeholder = field
            update_parts.append(f"{field_placeholder} = :{field}")
            expression_attribute_values[f":{field}"] = value

        # Adicionar timestamp de atualização
        update_parts.append("updated_at = :updated_at")
        expression_attribute_values[":updated_at"] = update_at

        # Criar a expressão de atualização
        update_expression = "SET " + ", ".join(update_parts)

        # Preparar parâmetros para a chamada de update_item
        update_params = {
            "Key": key,
            "UpdateExpression": update_expression,
            "ExpressionAttributeValues": expression_attribute_values,
            "ReturnValues": "UPDATED_NEW",
        }

        # Adicionar expressão de condição se fornecida
        if condition_expression:
            update_params["ConditionExpression"] = condition_expression

            # Adicionar valores de condição aos valores de expressão existentes
            if condition_values:
                for k, v in condition_values.items():
                    if k not in expression_attribute_values:
                        expression_attribute_values[k] = v

        # Executar a atualização
        try:
            response = self.table.update_item(**update_params)
            return response
        except Exception as e:
            raise Exception(f"Failed to update item: {str(e)}")

    def scan(
        self,
        filter_expression: Optional[Attr] = None,
        expression_attribute_values: Optional[Dict] = None,
        **kwargs,
    ) -> Dict:
        """
        Realiza uma busca por todos os items da tabela

        Args:
            filter_expression: Expressão de filtro do DynamoDB
            expression_attribute_values: Valores para substituição na expressão de filtro
            kwargs: Parâmetros adicionais para a busca

        Returns:
            Dict: Resultado da operação scan com itens da tabela
        """
        try:
            scan_params = {}

            if filter_expression:
                scan_params["FilterExpression"] = filter_expression

            if expression_attribute_values:
                scan_params["ExpressionAttributeValues"] = expression_attribute_values

            scan_params.update(kwargs)

            response = self.table.scan(**scan_params)
            return response
        except Exception as e:
            raise Exception(f"Failed to scan table: {str(e)}")

    def _build_filter_expression(
        self, attr_name: str, operator: str, value: Union[str, int, float, List, Tuple]
    ) -> Attr:
        """
        Constrói a expressão de filtro baseada no operador fornecido

        Args:
            attr_name: Nome do atributo
            operator: Operador a ser usado (ex: 'eq', 'between')
            value: Valor ou valores para o filtro

        Returns:
            Attr: Expressão de filtro do DynamoDB
        """
        attr = Attr(attr_name)

        operator = operator.lower()
        if operator == FilterOperator.EQ.value:
            return attr.eq(value)
        elif operator == FilterOperator.BETWEEN.value:
            if not isinstance(value, (list, tuple)) or len(value) != 2:
                raise ValueError(
                    "BETWEEN operator requires a list or tuple with exactly 2 values"
                )
            return attr.between(value[0], value[1])
        elif operator == FilterOperator.BEGINS_WITH.value:
            return attr.begins_with(value)
        elif operator == FilterOperator.CONTAINS.value:
            return attr.contains(value)
        elif operator == FilterOperator.GT.value:
            return attr.gt(value)
        elif operator == FilterOperator.GTE.value:
            return attr.gte(value)
        elif operator == FilterOperator.LT.value:
            return attr.lt(value)
        elif operator == FilterOperator.LTE.value:
            return attr.lte(value)
        elif operator == FilterOperator.NE.value:
            return attr.ne(value)
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    def convert_item_to_dict(self, item: Dict) -> Dict:
        deserializer = TypeDeserializer()
        return {k: deserializer.deserialize(v) for k, v in item.items()} if item else {}
