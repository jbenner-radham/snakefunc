from typing import Literal

type CoercibleSequenceType = Literal["bytearray", "bytes", "list", "str", "tuple"]
type IncoercibleSequenceType = Literal["range"]
type SequenceType = CoercibleSequenceType | IncoercibleSequenceType
