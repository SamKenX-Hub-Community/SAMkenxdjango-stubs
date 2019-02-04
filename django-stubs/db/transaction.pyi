from contextlib import ContextDecorator
from typing import Any, Callable, Optional, Union, Iterator, overload, ContextManager

from django.db import ProgrammingError

class TransactionManagementError(ProgrammingError): ...

def get_connection(using: Optional[str] = ...) -> Any: ...
def get_autocommit(using: Optional[str] = ...) -> bool: ...
def set_autocommit(autocommit: bool, using: None = ...) -> Any: ...
def commit(using: None = ...) -> Any: ...
def rollback(using: None = ...) -> Any: ...
def savepoint(using: None = ...) -> str: ...
def savepoint_rollback(sid: str, using: None = ...) -> None: ...
def savepoint_commit(sid: Any, using: Optional[Any] = ...) -> None: ...
def clean_savepoints(using: Optional[Any] = ...) -> None: ...
def get_rollback(using: None = ...) -> bool: ...
def set_rollback(rollback: bool, using: Optional[str] = ...) -> None: ...
def on_commit(func: Callable, using: None = ...) -> None: ...

class Atomic(ContextDecorator):
    using: Optional[str] = ...
    savepoint: bool = ...
    def __init__(self, using: Optional[str], savepoint: bool) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, exc_type: None, exc_value: None, traceback: None) -> None: ...

@overload
def atomic() -> Atomic: ...
@overload
def atomic(using: Optional[str] = ...,) -> ContextManager[Atomic]: ...
@overload
def atomic(using: Callable = ...) -> Callable: ...
@overload
def atomic(using: Optional[str] = ..., savepoint: bool = ...) -> ContextManager[Atomic]: ...
def non_atomic_requests(using: Callable = ...) -> Callable: ...
