# downloader

Repositório com código base para download assíncrono (com acompanhamento de bytes baixados por arquivo) de arquivos gerais.

### 🌎 Ativar ambiente

```bash
make python/ativar-ambiente
```

### 📝 Estilo de código

```bash
# Verifica e altera os arquivos (não inclui alertas Mypy)
make python/formatar-codigo
```

```bash
# Apenas verificar alertas (inclui Mypy)
make python/checar-codigo
```

### 🐳 Execução local

```python
from src.baixar import baixar

links = [
   "http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/HOURLY/2023/07/05/MERGE_CPTEC_2023070500.grib2",
   "http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/HOURLY/2023/07/05/MERGE_CPTEC_2023070501.grib2",
   "http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/HOURLY/2023/07/05/MERGE_CPTEC_2023070502.grib2",
   "http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/HOURLY/2023/07/05/MERGE_CPTEC_2023070503.grib2",
   "http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/HOURLY/2023/07/05/MERGE_CPTEC_2023070504.grib2",
   "http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/HOURLY/2023/07/05/MERGE_CPTEC_2023070505.grib2",
]
baixar(links)
```
