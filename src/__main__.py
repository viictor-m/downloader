"""Módulo principal da aplicação src."""
from src.baixar import baixar


if __name__ == "__main__":
    links = [
        "http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/HOURLY/2023/07/05/MERGE_CPTEC_2023070500.grib2",
        "http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/HOURLY/2023/07/05/MERGE_CPTEC_2023070501.grib2",
        "http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/HOURLY/2023/07/05/MERGE_CPTEC_2023070502.grib2",
        "http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/HOURLY/2023/07/05/MERGE_CPTEC_2023070503.grib2",
        "http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/HOURLY/2023/07/05/MERGE_CPTEC_2023070504.grib2",
        "http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/HOURLY/2023/07/05/MERGE_CPTEC_2023070505.grib2",
    ]

    baixar(links)
