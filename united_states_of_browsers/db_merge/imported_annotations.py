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

PathInfo = NewType('PathInfo', Union[Path, PathLike, Text, ByteString])
