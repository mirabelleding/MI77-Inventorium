from __future__ import annotations

from getpass import getpass
from io import BytesIO
from pathlib import Path

import msoffcrypto


def unlock_excel(
    path: str | Path,
    *,
    password: str | None = None,
) -> BytesIO:

    with open(path, "rb") as source:
        file = msoffcrypto.OfficeFile(source)

        if not file.is_encrypted():
            source.seek(0)
            return BytesIO(source.read())

        buffer = BytesIO()

        file.load_key(
            password=password
            if password is not None
            else getpass("Excel password: ")
        )

        file.decrypt(buffer)

    buffer.seek(0)

    return buffer