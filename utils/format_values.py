def format_currency(valor, prefixo="R$ ", casas=2):
    """Formata um valor numérico para exibição monetária no padrão brasileiro"""
    if valor is None:
        return "Não disponível"
    return (
        f"{prefixo} {valor:,.{casas}f}".replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def format_percent(valor, casas=1):
    """Formata um valor para exibição como percentual"""
    if valor is None:
        return "Não disponível"
    return f"{valor:.{casas}f}%".replace(".", ",")


def format_time(minutos):
    """Converte minutos em formato hh:mm"""
    horas = minutos // 60
    min_restantes = minutos % 60
    return f"{horas:02d}:{min_restantes:02d}"
