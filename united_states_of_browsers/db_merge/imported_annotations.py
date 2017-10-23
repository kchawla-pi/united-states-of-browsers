# -*- encoding: utf-8 -*-

from pathlib import Path
from os import PathLike
from typing import (AnyStr,
                    ByteString,
                    Dict,
                    Generator,
                    Iterable,
                    List,
                    Optional,
                    Sequence,
                    SupportsInt,
                    Text, Tuple, Type, TypeVar,
                    Union,
                    NewType,
                    )

PathLike = NewType('PathLike', Union[Path, PathLike, Text, ByteString])
# False = NewType('False', bool)
