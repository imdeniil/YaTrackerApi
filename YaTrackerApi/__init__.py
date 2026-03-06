"""
Yandex Tracker API Client

Модульная архитектура для работы с различными сущностями Yandex Tracker API.
"""

from .base import YandexTrackerClient
from .exceptions import (
    TrackerAPIError,
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    ConflictError,
    PreconditionFailedError,
    UnprocessableEntityError,
    LockedError,
    PreconditionRequiredError,
    TooManyRequestsError,
    ServerError,
)

__all__ = [
    'YandexTrackerClient',
    'TrackerAPIError',
    'BadRequestError',
    'UnauthorizedError',
    'ForbiddenError',
    'NotFoundError',
    'ConflictError',
    'PreconditionFailedError',
    'UnprocessableEntityError',
    'LockedError',
    'PreconditionRequiredError',
    'TooManyRequestsError',
    'ServerError',
]
