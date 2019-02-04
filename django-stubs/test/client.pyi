from io import BytesIO
from typing import Any, Dict, List, Optional, Pattern, Tuple, Type, Union

from django.contrib.auth.models import User
from django.contrib.sessions.backends.base import SessionBase
from django.core.handlers.base import BaseHandler
from django.core.serializers.json import DjangoJSONEncoder
from django.http.cookie import SimpleCookie
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBase

CONTENT_TYPE_RE: Pattern

class RedirectCycleError(Exception):
    last_response: HttpResponseBase = ...
    redirect_chain: List[Tuple[str, int]] = ...
    def __init__(self, message: str, last_response: HttpResponseBase) -> None: ...

class FakePayload:
    read_started: bool = ...
    def __init__(self, content: Optional[Union[bytes, str]] = ...) -> None: ...
    def __len__(self) -> int: ...
    def read(self, num_bytes: int = ...) -> bytes: ...
    def write(self, content: Union[bytes, str]) -> None: ...

class ClientHandler(BaseHandler):
    enforce_csrf_checks: bool = ...
    def __init__(self, enforce_csrf_checks: bool = ..., *args: Any, **kwargs: Any) -> None: ...
    def __call__(self, environ: Dict[str, Any]) -> HttpResponseBase: ...

def encode_multipart(boundary: str, data: Dict[str, Any]) -> bytes: ...
def encode_file(boundary: str, key: str, file: Any) -> List[bytes]: ...

class RequestFactory:
    json_encoder: Type[DjangoJSONEncoder] = ...
    defaults: Dict[str, str] = ...
    cookies: SimpleCookie = ...
    errors: BytesIO = ...
    def __init__(self, *, json_encoder: Any = ..., **defaults: Any) -> None: ...
    def request(self, **request: Any) -> HttpRequest: ...
    def get(self, path: str, data: Any = ..., secure: bool = ..., **extra: Any) -> HttpRequest: ...
    def post(
        self, path: str, data: Any = ..., content_type: str = ..., secure: bool = ..., **extra: Any
    ) -> HttpRequest: ...
    def head(self, path: str, data: Any = ..., secure: bool = ..., **extra: Any) -> HttpRequest: ...
    def trace(self, path: str, secure: bool = ..., **extra: Any) -> HttpRequest: ...
    def options(
        self,
        path: str,
        data: Union[Dict[str, str], str] = ...,
        content_type: str = ...,
        secure: bool = ...,
        **extra: Any
    ) -> HttpRequest: ...
    def put(
        self, path: str, data: Any = ..., content_type: str = ..., secure: bool = ..., **extra: Any
    ) -> HttpRequest: ...
    def patch(
        self, path: str, data: Any = ..., content_type: str = ..., secure: bool = ..., **extra: Any
    ) -> HttpRequest: ...
    def delete(
        self, path: str, data: Any = ..., content_type: str = ..., secure: bool = ..., **extra: Any
    ) -> HttpRequest: ...
    def generic(
        self,
        method: str,
        path: str,
        data: Any = ...,
        content_type: Optional[str] = ...,
        secure: bool = ...,
        **extra: Any
    ) -> HttpRequest: ...

class Client:
    json_encoder: Type[DjangoJSONEncoder] = ...
    defaults: Dict[str, str] = ...
    cookies: SimpleCookie = ...
    errors: BytesIO = ...
    handler: ClientHandler = ...
    exc_info: None = ...
    def __init__(self, enforce_csrf_checks: bool = ..., **defaults: Any) -> None: ...
    def request(self, **request: Any) -> HttpResponse: ...
    def get(self, path: str, data: Any = ..., secure: bool = ..., **extra: Any) -> HttpResponse: ...
    def post(
        self, path: str, data: Any = ..., content_type: str = ..., secure: bool = ..., **extra: Any
    ) -> HttpResponse: ...
    def head(self, path: str, data: Any = ..., secure: bool = ..., **extra: Any) -> HttpResponse: ...
    def trace(self, path: str, secure: bool = ..., **extra: Any) -> HttpResponse: ...
    def options(
        self,
        path: str,
        data: Union[Dict[str, str], str] = ...,
        content_type: str = ...,
        secure: bool = ...,
        **extra: Any
    ) -> HttpResponse: ...
    def put(
        self, path: str, data: Any = ..., content_type: str = ..., secure: bool = ..., **extra: Any
    ) -> HttpResponse: ...
    def patch(
        self, path: str, data: Any = ..., content_type: str = ..., secure: bool = ..., **extra: Any
    ) -> HttpResponse: ...
    def delete(
        self, path: str, data: Any = ..., content_type: str = ..., secure: bool = ..., **extra: Any
    ) -> HttpResponse: ...
    def generic(
        self,
        method: str,
        path: str,
        data: Any = ...,
        content_type: Optional[str] = ...,
        secure: bool = ...,
        **extra: Any
    ) -> HttpResponse: ...
    def store_exc_info(self, **kwargs: Any) -> None: ...
    @property
    def session(self) -> SessionBase: ...
    def login(self, **credentials: Any) -> bool: ...
    def force_login(self, user: User, backend: Optional[str] = ...) -> None: ...
    def logout(self) -> None: ...

def conditional_content_removal(request: HttpRequest, response: HttpResponse) -> HttpResponse: ...
