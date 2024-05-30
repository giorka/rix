from __future__ import annotations

import logging
from time import sleep

from blomp_api import Blomp
from blomp_api import fso
from requests import exceptions


def get_storage(email: str, password: str) -> fso.Folder:
    try:
        storage = Blomp(email, password).get_root_directory()
    except exceptions.ConnectionError as reason:
        logging.critical(
            f'Storage Server Connection Canceled!\nBecause Of {reason}',
        )

        sleep(240)

        return get_storage(email=email, password=password)

    return storage
