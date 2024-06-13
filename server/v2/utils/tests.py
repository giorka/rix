from __future__ import annotations

import json
import logging

from django.core.handlers.wsgi import WSGIRequest
from rest_framework.test import APIClient


class LoggerAPIClient(APIClient):
    def generic(self, *args, **kwargs) -> WSGIRequest:
        response = super().generic(*args, **kwargs)

        logging.debug(json.loads(response.content))

        return response
