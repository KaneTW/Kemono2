from dataclasses import dataclass
from re import RegexFlag, Pattern, compile as compile_regexp


class Encodings:
    HEX = "hex"
    ASCII = "ascii"


@dataclass
class KeyConstraints:
    min_length: int = 1
    max_length: int = 1024
    encoding: str = Encodings.ASCII
    length: int = None
    case: str = None
    pattern: Pattern = None


service_constraints = dict(
    patreon=KeyConstraints(length=43),
    fanbox=KeyConstraints(),
    fantia=KeyConstraints(
        length=32,
        encoding=Encodings.HEX,
        case="lower"
    ),
    gumroad=KeyConstraints(min_length=200),
    subscribestar=KeyConstraints(),
    dlsite=KeyConstraints(),
    discord=KeyConstraints(
        pattern=compile_regexp(
            pattern=r"/(mfa\.[a-z0-9_-]{20,})|([a-z0-9_-]{23,28}\.[a-z0-9_-]{6,7}\.[a-z0-9_-]{27})/i",
            flags=RegexFlag.IGNORECASE
        )
    ),
)
