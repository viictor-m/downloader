from pathlib import Path

from pydantic import BaseModel
from src.config import config


class Arquivo(BaseModel):
    """Classe contendo informações sobre arquivo a ser baixado."""

    url_fonte: str

    @property
    def nome_arquivo(self) -> str:
        """
        Retorna o nome do arquivo a partir da url.

        Returns
        -------
        str
            Nome do arquivo
        """
        return Path(self.url_fonte).name

    @property
    def local(self) -> Path:
        """
        Retorna o caminho local até onde o arquivo será armazenado.

        Returns
        -------
        Path
            Caminho local do arquivo.
        """
        return config.diretorio_download / self.nome_arquivo
