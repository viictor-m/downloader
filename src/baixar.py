"""Módulo com função principal para baixar arquivos assíncronamente."""
import asyncio
from io import BytesIO

from typing import List

import httpx

from rich.console import Group
from rich.live import Live
from rich.progress import BarColumn
from rich.progress import MofNCompleteColumn
from rich.progress import Progress
from rich.progress import TaskID
from rich.progress import TextColumn
from rich.progress import TimeElapsedColumn
from src.config import config
from src.arquivo import Arquivo


limitador_tarefas = asyncio.Semaphore(config.tarefas_download_simultaneas)


# ? referências:
# https://github.com/Textualize/rich/blob/master/examples/dynamic_progress.py

prog_down = Progress()

prog_total = Progress(
    TextColumn("[blue]" + "{task.description}".ljust(37) + "[/blue]"),
    MofNCompleteColumn(),
    BarColumn(bar_width=50),
    TimeElapsedColumn(),
)

progresso = Group(prog_down, prog_total)


async def baixar_arquivo(arquivo: Arquivo, id_prog_total: TaskID) -> None:
    """
    Download assíncrono e upload (AWS S3) de um lead do modelo ETA.

    O conteúdo da resposta da URL é armazenado em memória visando reduzir tempo
    de escrita em disco. O upload para o S3 é feito diretamente do buffer.

    Parameters
    ----------
    id_prog_total : TaskID
        ID da barra de progresso total da rodada sendo coletada.

    Returns
    -------
    dict[str, Any]
        Metadados do Lead armazenado no S3.
    """
    with BytesIO() as buffer:
        async with limitador_tarefas:
            async with httpx.AsyncClient() as client:
                async with client.stream("GET", arquivo.url_fonte, timeout=None) as stream:
                    tamanho_conteudo = int(stream.headers["Content-Length"])
                    id_tarefa_down = prog_down.add_task(
                        "download",
                        filename=arquivo.nome_arquivo,
                        total=tamanho_conteudo,
                    )

                    async for chunk in stream.aiter_bytes():
                        prog_down.update(
                            id_tarefa_down,
                            completed=stream.num_bytes_downloaded,
                        )
                        buffer.write(chunk)

                    buffer.seek(0)
                    with open(arquivo.local, "wb") as file:
                        file.write(buffer.getbuffer())

                    prog_total.update(id_prog_total, advance=1)

                    prog_down.console.print(
                        (
                            "[bold green]✓[/bold green] "
                            f"[blue]{arquivo.nome_arquivo}[/blue] armazenado!"
                        )
                    )

                    prog_down.stop_task(id_tarefa_down)
                    prog_down.update(id_tarefa_down, visible=False)


def baixar(arquivos: List[str]) -> None:
    """
    Baixa uma lista de arquivos de forma assíncrona.

    Parameters
    ----------
    arquivos : List[str]
        Lista de links para download.
    """
    id_prog_total = prog_total.add_task("tarefas", total=len(arquivos))
    pendencias = list()
    for link in arquivos:
        arquivo = Arquivo(url_fonte=link)
        tarefa = baixar_arquivo(arquivo, id_prog_total)
        pendencias.append(tarefa)

    with Live(progresso):
        loop = asyncio.get_event_loop()
        tarefas = asyncio.gather(*pendencias, return_exceptions=False)
        loop.run_until_complete(tarefas)
        loop.close()
