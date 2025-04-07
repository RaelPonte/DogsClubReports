import time
import datetime
import pytz
from typing import Optional


def get_timestamp(dt: Optional[datetime.datetime] = None) -> int:
    """
    Retorna o timestamp atual em milissegundos ou de uma data específica.

    Args:
        dt: Data opcional para converter em timestamp

    Returns:
        int: Timestamp em milissegundos
    """
    if dt is None:
        return int(time.time() * 1000)

    return int(dt.timestamp() * 1000)


def get_datetime_from_timestamp(timestamp: int) -> datetime.datetime:
    """
    Converte um timestamp em milissegundos para um objeto datetime.

    Args:
        timestamp: Timestamp em milissegundos

    Returns:
        datetime.datetime: Objeto datetime
    """
    return datetime.datetime.fromtimestamp(timestamp / 1000, tz=pytz.utc)


def format_iso_date(dt: Optional[datetime.datetime] = None) -> str:
    """
    Retorna a data atual ou uma data específica em formato ISO.

    Args:
        dt: Data opcional para formatar

    Returns:
        str: Data em formato ISO
    """
    if dt is None:
        dt = datetime.datetime.now(tz=pytz.utc)

    return dt.isoformat()
