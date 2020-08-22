""" common q_service deque """
from collections import deque

from .freemt_services import FREEMT_SERVICES  # type: ignore

Q_SERVICES = deque(FREEMT_SERVICES)
q_services = Q_SERVICES  # pylint: disable=invalid-name
