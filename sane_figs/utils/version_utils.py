"""Version utility functions for sane-figs."""

from typing import Tuple


def parse_version(version_string: str) -> Tuple[int, int, int]:
    """
    Parse a version string into a tuple of integers.

    Args:
        version_string: Version string (e.g., "3.5.0", "2.1.3").

    Returns:
        Tuple of (major, minor, patch) version numbers.

    Examples:
        >>> parse_version("3.5.0")
        (3, 5, 0)
        >>> parse_version("2.1.3")
        (2, 1, 3)
    """
    # Remove any non-numeric suffixes (e.g., "3.5.0rc1" -> "3.5.0")
    version = version_string.strip()
    for i, char in enumerate(version):
        if not char.isdigit() and char != ".":
            version = version[:i]
            break

    parts = version.split(".")
    major = int(parts[0]) if len(parts) > 0 else 0
    minor = int(parts[1]) if len(parts) > 1 else 0
    patch = int(parts[2]) if len(parts) > 2 else 0

    return (major, minor, patch)


def version_tuple(version_string: str) -> Tuple[int, int, int]:
    """
    Alias for parse_version for backward compatibility.

    Args:
        version_string: Version string (e.g., "3.5.0", "2.1.3").

    Returns:
        Tuple of (major, minor, patch) version numbers.
    """
    return parse_version(version_string)
