"""Configurações do serviço."""
from pathlib import Path

from pydantic import BaseSettings


class Configuracoes(BaseSettings):
    """Configurações e parâmetros do serviço."""

    tarefas_download_simultaneas: int = 20
    diretorio_download: Path = Path("tmp")
    diretorio_download.mkdir(exist_ok=True, parents=True)


config = Configuracoes()
