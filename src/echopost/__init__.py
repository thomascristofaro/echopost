"""
EchoPost - Un tool per leggere feed RSS, estrarre articoli rilevanti con AI,
e pubblicarli automaticamente su LinkedIn.
"""

from .main import main
from .config import load_settings

__all__ = [
    "main",
    "load_settings"
]