"""
Исключения для Yandex Tracker API Client
"""

from typing import Optional, Dict, Any, List


class TrackerAPIError(Exception):
    """Базовое исключение для ошибок Yandex Tracker API"""

    def __init__(
        self,
        status_code: int,
        message: str = "",
        errors: Optional[Dict[str, str]] = None,
        error_messages: Optional[List[str]] = None,
        url: str = "",
        method: str = ""
    ):
        self.status_code = status_code
        self.errors = errors or {}
        self.error_messages = error_messages or []
        self.url = url
        self.method = method

        parts = [f"{status_code}"]
        if message:
            parts.append(message)
        if self.error_messages:
            parts.append("; ".join(self.error_messages))
        if self.errors:
            field_errors = [f"{k}: {v}" for k, v in self.errors.items()]
            parts.append("; ".join(field_errors))

        super().__init__(" | ".join(parts))


class BadRequestError(TrackerAPIError):
    """400 — Неверные параметры запроса"""
    pass


class UnauthorizedError(TrackerAPIError):
    """401 — Пользователь не авторизован"""
    pass


class ForbiddenError(TrackerAPIError):
    """403 — Недостаточно прав"""
    pass


class NotFoundError(TrackerAPIError):
    """404 — Объект не найден"""
    pass


class ConflictError(TrackerAPIError):
    """409 — Конфликт при редактировании (неверная версия)"""
    pass


class PreconditionFailedError(TrackerAPIError):
    """412 — Конфликт версий при редактировании"""
    pass


class UnprocessableEntityError(TrackerAPIError):
    """422 — Ошибка валидации JSON"""
    pass


class LockedError(TrackerAPIError):
    """423 — Объект заблокирован (превышен лимит version)"""
    pass


class PreconditionRequiredError(TrackerAPIError):
    """428 — Не указаны обязательные условия запроса"""
    pass


class TooManyRequestsError(TrackerAPIError):
    """429 — Превышен лимит запросов"""
    pass


class ServerError(TrackerAPIError):
    """5xx — Ошибка на стороне сервера"""
    pass


# Маппинг код → класс исключения
STATUS_CODE_MAP = {
    400: BadRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    409: ConflictError,
    412: PreconditionFailedError,
    422: UnprocessableEntityError,
    423: LockedError,
    428: PreconditionRequiredError,
    429: TooManyRequestsError,
}


def raise_for_status(status_code: int, response_text: str, url: str = "", method: str = ""):
    """Выбросить типизированное исключение по коду ответа"""
    # Парсим JSON тело ошибки
    errors = {}
    error_messages = []
    message = response_text

    try:
        import json
        body = json.loads(response_text)
        if isinstance(body, dict):
            errors = body.get("errors", {})
            error_messages = body.get("errorMessages", [])
            message = response_text
    except (json.JSONDecodeError, ValueError):
        pass

    exc_class = STATUS_CODE_MAP.get(status_code)
    if exc_class is None:
        if status_code >= 500:
            exc_class = ServerError
        else:
            exc_class = TrackerAPIError

    raise exc_class(
        status_code=status_code,
        message=message,
        errors=errors,
        error_messages=error_messages,
        url=url,
        method=method
    )
