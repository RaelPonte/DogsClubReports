from typing import Dict, List, Optional, Union, BinaryIO
from pathlib import Path
import re
import base64
import os
import mimetypes


def load_template(template_name: str) -> str:
    """
    Carrega um template HTML a partir do disco.

    Args:
        template_name: Nome do template sem a extensão .html

    Returns:
        str: Conteúdo do template
    """
    templates_path = Path(__file__).parents[1] / "html"
    file_path = templates_path / f"{template_name}.html"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template não encontrado: {file_path}")


def replace_template_variables(template: str, variables: Dict[str, str]) -> str:
    """
    Substitui variáveis no template pelos valores fornecidos.

    Args:
        template: Template HTML com variáveis no formato {{nome_variavel}}
        variables: Dicionário com os valores das variáveis

    Returns:
        str: Template com as variáveis substituídas
    """
    for key, value in variables.items():
        pattern = r"\{\{" + key + r"\}\}"
        template = re.sub(pattern, str(value), template)
    return template


def encode_attachment(file_path: str) -> str:
    """
    Codifica um arquivo para base64 para uso em email.

    Args:
        file_path: Caminho do arquivo

    Returns:
        str: Arquivo codificado em base64
    """
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def prepare_attachment(
    content: Union[bytes, BinaryIO], filename: str, content_type: Optional[str] = None
) -> Dict:
    """
    Prepara um anexo para envio por email.

    Args:
        content: Conteúdo do arquivo em bytes ou objeto BinaryIO
        filename: Nome do arquivo
        content_type: Tipo de conteúdo MIME (opcional)

    Returns:
        Dict: Dicionário com informações do anexo
    """
    if not content_type:
        content_type, _ = mimetypes.guess_type(filename)
        if not content_type:
            content_type = "application/octet-stream"

    # Converter para bytes se for um objeto de arquivo
    if hasattr(content, "read"):
        content = content.read()

    # Retornar dados do anexo
    return {"name": filename, "content": content, "content_type": content_type}
