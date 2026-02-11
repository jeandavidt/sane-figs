"""Pytest configuration and fixtures for version-specific testing."""

import pytest
from typing import Optional
import sys


# ============================================================================
# Library Version Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def matplotlib_version() -> Optional[str]:
    """Get the installed matplotlib version.
    
    Returns:
        Version string or None if matplotlib is not installed.
    """
    try:
        import matplotlib
        return matplotlib.__version__
    except ImportError:
        return None


@pytest.fixture(scope="session")
def seaborn_version() -> Optional[str]:
    """Get the installed seaborn version.
    
    Returns:
        Version string or None if seaborn is not installed.
    """
    try:
        import seaborn
        return seaborn.__version__
    except ImportError:
        return None


@pytest.fixture(scope="session")
def plotly_version() -> Optional[str]:
    """Get the installed plotly version.
    
    Returns:
        Version string or None if plotly is not installed.
    """
    try:
        import plotly
        return plotly.__version__
    except ImportError:
        return None


@pytest.fixture(scope="session")
def altair_version() -> Optional[str]:
    """Get the installed altair version.
    
    Returns:
        Version string or None if altair is not installed.
    """
    try:
        import altair
        return altair.__version__
    except ImportError:
        return None


@pytest.fixture(scope="session")
def python_version() -> str:
    """Get the current Python version.
    
    Returns:
        Python version string (e.g., "3.11.0").
    """
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


# ============================================================================
# Version Tuple Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def matplotlib_version_tuple(matplotlib_version: Optional[str]) -> Optional[tuple]:
    """Get matplotlib version as a tuple for comparison.
    
    Returns:
        Version tuple (major, minor, patch) or None if not installed.
    """
    if matplotlib_version is None:
        return None
    try:
        import packaging.version
        return tuple(map(int, packaging.version.parse(matplotlib_version).base_version.split('.')))
    except Exception:
        return None


@pytest.fixture(scope="session")
def seaborn_version_tuple(seaborn_version: Optional[str]) -> Optional[tuple]:
    """Get seaborn version as a tuple for comparison.
    
    Returns:
        Version tuple (major, minor, patch) or None if not installed.
    """
    if seaborn_version is None:
        return None
    try:
        import packaging.version
        return tuple(map(int, packaging.version.parse(seaborn_version).base_version.split('.')))
    except Exception:
        return None


@pytest.fixture(scope="session")
def plotly_version_tuple(plotly_version: Optional[str]) -> Optional[tuple]:
    """Get plotly version as a tuple for comparison.
    
    Returns:
        Version tuple (major, minor, patch) or None if not installed.
    """
    if plotly_version is None:
        return None
    try:
        import packaging.version
        return tuple(map(int, packaging.version.parse(plotly_version).base_version.split('.')))
    except Exception:
        return None


@pytest.fixture(scope="session")
def altair_version_tuple(altair_version: Optional[str]) -> Optional[tuple]:
    """Get altair version as a tuple for comparison.
    
    Returns:
        Version tuple (major, minor, patch) or None if not installed.
    """
    if altair_version is None:
        return None
    try:
        import packaging.version
        return tuple(map(int, packaging.version.parse(altair_version).base_version.split('.')))
    except Exception:
        return None


# ============================================================================
# Pytest Configuration
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers for version-specific tests."""
    # Matplotlib markers
    config.addinivalue_line(
        "markers", "matplotlib_min: Tests for matplotlib minimum version (2.0.x)"
    )
    config.addinivalue_line(
        "markers", "matplotlib_3_0: Tests for matplotlib 3.0+"
    )
    config.addinivalue_line(
        "markers", "matplotlib_3_5: Tests for matplotlib 3.5+"
    )
    
    # Seaborn markers
    config.addinivalue_line(
        "markers", "seaborn_0_11: Tests for seaborn 0.11+"
    )
    config.addinivalue_line(
        "markers", "seaborn_0_12: Tests for seaborn 0.12+"
    )
    
    # Plotly markers
    config.addinivalue_line(
        "markers", "plotly_5_0: Tests for plotly 5.0+"
    )
    
    # Altair markers
    config.addinivalue_line(
        "markers", "altair_5_0: Tests for altair 5.0+"
    )
    
    # Library-specific markers
    config.addinivalue_line(
        "markers", "matplotlib: Tests requiring matplotlib"
    )
    config.addinivalue_line(
        "markers", "seaborn: Tests requiring seaborn"
    )
    config.addinivalue_line(
        "markers", "plotly: Tests requiring plotly"
    )
    config.addinivalue_line(
        "markers", "altair: Tests requiring altair"
    )
    
    # Visual regression marker
    config.addinivalue_line(
        "markers", "visual: Visual regression tests"
    )


def pytest_collection_modifyitems(config, items):
    """Skip tests based on installed library versions.
    
    This function automatically skips tests that require specific library
    versions that are not installed or are incompatible.
    """
    try:
        import packaging.version
    except ImportError:
        # If packaging is not available, skip version checking
        return
    
    # Get installed versions
    mpl_ver = None
    sns_ver = None
    plt_ver = None
    alt_ver = None
    
    try:
        import matplotlib
        mpl_ver = packaging.version.parse(matplotlib.__version__)
    except ImportError:
        pass
    
    try:
        import seaborn
        sns_ver = packaging.version.parse(seaborn.__version__)
    except ImportError:
        pass
    
    try:
        import plotly
        plt_ver = packaging.version.parse(plotly.__version__)
    except ImportError:
        pass
    
    try:
        import altair
        alt_ver = packaging.version.parse(altair.__version__)
    except ImportError:
        pass
    
    for item in items:
        # Skip matplotlib version-specific tests
        if mpl_ver:
            if item.get_closest_marker("matplotlib_3_5") and mpl_ver < packaging.version.parse("3.5.0"):
                item.add_marker(pytest.mark.skip(reason=f"Requires matplotlib 3.5+, found {mpl_ver}"))
            elif item.get_closest_marker("matplotlib_3_0") and mpl_ver < packaging.version.parse("3.0.0"):
                item.add_marker(pytest.mark.skip(reason=f"Requires matplotlib 3.0+, found {mpl_ver}"))
        else:
            if any(m in item.keywords for m in ["matplotlib_min", "matplotlib_3_0", "matplotlib_3_5", "matplotlib"]):
                item.add_marker(pytest.mark.skip(reason="Matplotlib not installed"))
        
        # Skip seaborn version-specific tests
        if sns_ver:
            if item.get_closest_marker("seaborn_0_12") and sns_ver < packaging.version.parse("0.12.0"):
                item.add_marker(pytest.mark.skip(reason=f"Requires seaborn 0.12+, found {sns_ver}"))
            elif item.get_closest_marker("seaborn_0_11") and sns_ver < packaging.version.parse("0.11.0"):
                item.add_marker(pytest.mark.skip(reason=f"Requires seaborn 0.11+, found {sns_ver}"))
        else:
            if any(m in item.keywords for m in ["seaborn_0_11", "seaborn_0_12", "seaborn"]):
                item.add_marker(pytest.mark.skip(reason="Seaborn not installed"))
        
        # Skip plotly version-specific tests
        if plt_ver:
            if item.get_closest_marker("plotly_5_0") and plt_ver < packaging.version.parse("5.0.0"):
                item.add_marker(pytest.mark.skip(reason=f"Requires plotly 5.0+, found {plt_ver}"))
        else:
            if any(m in item.keywords for m in ["plotly_5_0", "plotly"]):
                item.add_marker(pytest.mark.skip(reason="Plotly not installed"))
        
        # Skip altair version-specific tests
        if alt_ver:
            if item.get_closest_marker("altair_5_0") and alt_ver < packaging.version.parse("5.0.0"):
                item.add_marker(pytest.mark.skip(reason=f"Requires altair 5.0+, found {alt_ver}"))
        else:
            if any(m in item.keywords for m in ["altair_5_0", "altair"]):
                item.add_marker(pytest.mark.skip(reason="Altair not installed"))


# ============================================================================
# Helper Fixtures
# ============================================================================

@pytest.fixture
def skip_if_no_matplotlib(matplotlib_version: Optional[str]):
    """Skip test if matplotlib is not installed."""
    if matplotlib_version is None:
        pytest.skip("Matplotlib not installed")


@pytest.fixture
def skip_if_no_seaborn(seaborn_version: Optional[str]):
    """Skip test if seaborn is not installed."""
    if seaborn_version is None:
        pytest.skip("Seaborn not installed")


@pytest.fixture
def skip_if_no_plotly(plotly_version: Optional[str]):
    """Skip test if plotly is not installed."""
    if plotly_version is None:
        pytest.skip("Plotly not installed")


@pytest.fixture
def skip_if_no_altair(altair_version: Optional[str]):
    """Skip test if altair is not installed."""
    if altair_version is None:
        pytest.skip("Altair not installed")


@pytest.fixture
def skip_if_matplotlib_lt(matplotlib_version_tuple: Optional[tuple], min_version: tuple):
    """Skip test if matplotlib version is less than min_version.
    
    Args:
        min_version: Minimum version as tuple (major, minor, patch)
    """
    if matplotlib_version_tuple is None:
        pytest.skip("Matplotlib not installed")
    if matplotlib_version_tuple < min_version:
        pytest.skip(f"Requires matplotlib {min_version[0]}.{min_version[1]}.{min_version[2]}+, found {matplotlib_version_tuple}")


@pytest.fixture
def skip_if_seaborn_lt(seaborn_version_tuple: Optional[tuple], min_version: tuple):
    """Skip test if seaborn version is less than min_version.
    
    Args:
        min_version: Minimum version as tuple (major, minor, patch)
    """
    if seaborn_version_tuple is None:
        pytest.skip("Seaborn not installed")
    if seaborn_version_tuple < min_version:
        pytest.skip(f"Requires seaborn {min_version[0]}.{min_version[1]}.{min_version[2]}+, found {seaborn_version_tuple}")


@pytest.fixture
def skip_if_plotly_lt(plotly_version_tuple: Optional[tuple], min_version: tuple):
    """Skip test if plotly version is less than min_version.
    
    Args:
        min_version: Minimum version as tuple (major, minor, patch)
    """
    if plotly_version_tuple is None:
        pytest.skip("Plotly not installed")
    if plotly_version_tuple < min_version:
        pytest.skip(f"Requires plotly {min_version[0]}.{min_version[1]}.{min_version[2]}+, found {plotly_version_tuple}")


@pytest.fixture
def skip_if_altair_lt(altair_version_tuple: Optional[tuple], min_version: tuple):
    """Skip test if altair version is less than min_version.
    
    Args:
        min_version: Minimum version as tuple (major, minor, patch)
    """
    if altair_version_tuple is None:
        pytest.skip("Altair not installed")
    if altair_version_tuple < min_version:
        pytest.skip(f"Requires altair {min_version[0]}.{min_version[1]}.{min_version[2]}+, found {altair_version_tuple}")
