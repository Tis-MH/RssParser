import datetime

from pydantic import BaseModel
from typing import Any, Generic, List, TypeVar, Union
from pydantic.generics import GenericModel


T = TypeVar("T")

class TResult(GenericModel, Generic[T]):
    code: int
    res: T