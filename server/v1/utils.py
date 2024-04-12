from __future__ import annotations

from uuid import UUID


def is_valid_uuid(string: str, version=4) -> bool:
    """
    Проверить, является ли string действительным UUID.

     Параметры
    ----------
    string: str
    version: {1, 2, 3, 4}

     Возврат
    -------
    «True», если string является допустимым UUID, в противном случае — «False».

     Примеры
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """

    try:
        uuid_obj = UUID(string, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == string
