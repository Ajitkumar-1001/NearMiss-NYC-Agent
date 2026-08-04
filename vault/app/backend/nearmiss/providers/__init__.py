"""Provider adapters. ADR-003.

Every external boundary in FR-011 gets one protocol and two implementations: a
runtime one and a fixture one. Business logic never imports a vendor SDK.

At P0 the runtime implementations are unconfigured and raise
ProviderUnavailable, so the orchestrator's ladder degrades to fixtures — which
is exactly what PRD §10.1 specifies ("P0 excludes all runtime external API
dependencies"). Wiring a runtime provider is a change to one file here.
"""

from .base import ProviderUnavailable

__all__ = ["ProviderUnavailable"]
