"""Security helpers migrated from flext_tools.security."""

from __future__ import annotations

from pathlib import Path
from typing import Self

from flext_core import FlextResult, FlextService, FlextTypes


class FlextSecurityService(FlextService[FlextTypes.StringDict]):
    """Provide vault decryption and antipattern scanning hooks."""

    def __init__(self: Self) -> None:
        super().__init__()

    def execute(self: Self) -> FlextResult[FlextTypes.StringDict]:
        """Return an empty payload for service compliance."""
        return FlextResult[FlextTypes.StringDict].ok({})

    def decrypt_vault(
        self, vault_path: str | Path
    ) -> FlextResult[FlextTypes.StringDict]:
        """Placeholder vault decryption returning metadata only."""
        path = Path(vault_path).expanduser()
        if not path.exists():
            return FlextResult[FlextTypes.StringDict].fail(
                f"Vault path does not exist: {path}"
            )

        return FlextResult[FlextTypes.StringDict].ok({
            "vault_path": str(path),
            "status": "decryption-not-implemented",
        })

    def scan_antipatterns(
        self,
        directory: str | Path,
        config: FlextTypes.StringDict | None = None,
    ) -> FlextResult[FlextTypes.StringList]:
        """Provide a placeholder antipattern scan result."""
        _ = directory, config
        return FlextResult[FlextTypes.StringList].ok([])


class SecretVaultDecryptor(FlextSecurityService):
    """Compatibility wrapper used by legacy security scripts."""

    def decrypt_vault(self, vault_path: str | Path) -> FlextTypes.StringDict:
        """Return decrypted vault metadata.

        The actual decryption logic is intentionally omitted until the secure
        implementation lands in flext-quality.  A structured dictionary is
        returned so existing scripts can continue handling the result.
        """
        result = super().decrypt_vault(vault_path)
        if result.is_failure:
            return {}
        return {
            "details": result.value,
            "status": "decryption-not-implemented",
        }


__all__ = ["FlextSecurityService", "SecretVaultDecryptor"]
