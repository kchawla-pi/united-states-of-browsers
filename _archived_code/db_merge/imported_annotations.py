# -*- encoding: utf-8 -*-

from pathlib import Path
from os import PathLike
from typing import (Any,
                    AnyStr,
                    ByteString,
                    Dict,
                    Generator,
                    Iterable,
                    List,
                    NamedTuple,
                    Optional,
                    Sequence,
                    SupportsInt,
                    Text, Tuple, Type, TypeVar,
                    Union,
                    NewType,
                    )

PathInfo = NewType('PathInfo', Union[Path, PathLike, Text, ByteString])
