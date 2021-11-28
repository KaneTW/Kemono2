from dataclasses import dataclass


@dataclass
class KeyConstraints:
    min_length: int = 1
    max_length: int = 1024


service_constraints = dict(
    patreon=KeyConstraints(),
    fanbox=KeyConstraints(),
    gumroad=KeyConstraints(),
    subscribestar=KeyConstraints(),
    dlsite=KeyConstraints(),
    discord=KeyConstraints(),
    fantia=KeyConstraints(),
)
