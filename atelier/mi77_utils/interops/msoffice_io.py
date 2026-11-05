from __future__ import annotations

from getpass import getpass
from io import BytesIO
from os import replace
from pathlib import Path
from tempfile import NamedTemporaryFile

from msoffcrypto import OfficeFile
from msoffcrypto.format.ooxml import OOXMLFile


def decrypt_msoffice(
    path: str | Path,
    *,
    password: str | None = None,
    save_to: str | Path | None = None,
) -> BytesIO:

    with open(path, "rb") as source:
        file = OfficeFile(source)

        if not file.is_encrypted():
            source.seek(0)
            return BytesIO(source.read())

        stream = BytesIO()

        file.load_key(
            password=password
            if password is not None
            else getpass(f"Password for {Path(path).name}: ")
        )

        file.decrypt(stream)

    stream.seek(0)

    if save_to:
        save_stream(stream, save_to)

    return stream


def encrypt_msoffice(
    path: str | Path,
    *,
    password: str | None = None,
    save_to: str | Path | None = None,
) -> BytesIO:

    with open(path, "rb") as source:
        file = OOXMLFile(source)
        stream = BytesIO()

        file.encrypt(
            password
            if password is not None
            else getpass(f"Password for {Path(path).name}: "),
            stream,
        )

    stream.seek(0)

    if save_to:
        save_stream(stream, save_to)

    return stream


def save_stream(
    stream: BytesIO,
    path: str | Path,
) -> Path:
    """
    Save an in-memory binary stream to a file.

    Write the contents to a temporary file in the destination directory,
    then atomically commit it to the destination, replacing any existing file.
    Unlike direct writes, which truncate an existing file before writing,
    atomic replacement preserves the original file if writing fails.

    Note: Atomic replacement does not guarantee durability against power loss.
    """
    path = Path(path)
    temporary = None

    try:
        with NamedTemporaryFile(
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as file:
            temporary = Path(file.name)
            file.write(stream.getbuffer())

        replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)

    return path