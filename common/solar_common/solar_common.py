# csv header
from Typing import TypedDict

fieldnames = [
    "timestamp",
    "PV voltage",
    "PV current",
    "PV power L",
    "PV power H",
    "battery voltage",
    "battery current",
    "battery power L",
    "battery power H",
    "load voltage",
    "load current",
    "load power",
    "battery percentage",
]


Sample = TypedDict(
    "Sample",
    {
        "timestamp": float,
        "PV voltage": float,
        "PV current": float,
        "PV power L": float,
        "PV power H": float,
        "battery voltage": float,
        "battery current": float,
        "battery power L": float,
        "battery power H": float,
        "load voltage": float,
        "load current": float,
        "load power": float,
        "battery percentage": float,
    },
)
