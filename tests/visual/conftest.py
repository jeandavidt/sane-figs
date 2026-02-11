"""Configuration for visual regression tests."""

import pytest
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Any
import io


# ============================================================================
# Matplotlib Setup
# ============================================================================

@pytest.fixture(autouse=True)
def setup_matplotlib():
    """Setup matplotlib for consistent testing.
    
    This fixture ensures that:
    1. The Agg backend is used for headless testing
    2. Figures are cleaned up after each test
    3. Consistent figure settings are applied
    """
    # Use Agg backend for headless testing
    matplotlib.use('Agg', force=True)
    
    # Set consistent figure size for testing
    plt.rcParams['figure.figsize'] = (6.4, 4.8)
    plt.rcParams['figure.dpi'] = 100
    
    yield
    
    # Clean up all figures
    plt.close('all')


# ============================================================================
# Figure Regression Fixture
# ============================================================================

@pytest.fixture
def fig_regression(image_regression, datadir, request):
    """Custom fixture for figure regression testing.

    This fixture provides a simple interface for comparing matplotlib
    figures against baseline images. It handles:
    1. Converting figures to image arrays
    2. Comparing against stored baselines
    3. Generating diffs on failure

    Args:
        image_regression: pytest-regressions image regression fixture
        datadir: pytest-datadir fixture for test data directory
        request: pytest request object

    Returns:
        FigureRegression object with check() method
    """
    class FigureRegression:
        def __init__(self, image_regression, datadir, request):
            self.image_regression = image_regression
            self.datadir = datadir
            self.request = request

        def check(self, fig, basename: str, tolerance: float = 1.0):
            """Check figure against baseline.

            Args:
                fig: Matplotlib figure object
                basename: Base name for the baseline file
                tolerance: Tolerance for pixel differences (default: 1.0)
            """
            # Save figure to bytes
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)

            # Get image data as bytes
            image_data = buf.getvalue()

            # Use image_regression for comparison
            self.image_regression.check(
                image_data,
                basename=basename,
                diff_threshold=tolerance
            )

        def check_with_text(self, fig, basename: str, text_elements: dict):
            """Check figure with text elements against baseline.

            This is useful for testing figures with dynamic text content
            that should be consistent across versions.

            Args:
                fig: Matplotlib figure object
                basename: Base name for the baseline file
                text_elements: Dictionary of text element names to check
            """
            # Check the figure image
            self.check(fig, basename)

            # Check text elements
            text_data = {}
            for name, element in text_elements.items():
                if hasattr(element, 'get_text'):
                    text_data[name] = element.get_text()
                elif isinstance(element, str):
                    text_data[name] = element

            if text_data:
                # Use num_regression for text data
                from pytest_regressions.num_regression import NumericRegressionFixture
                num_regression = NumericRegressionFixture(
                    datadir=self.datadir,
                    original_datadir=self.datadir,
                    request=self.request,
                )
                num_regression.check(
                    text_data,
                    basename=f"{basename}_text"
                )

    return FigureRegression(image_regression, datadir, request)


# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def sample_data():
    """Generate sample data for testing.
    
    Returns:
        Dictionary with x, y1, y2 arrays
    """
    x = np.linspace(0, 10, 100)
    return {
        'x': x,
        'y1': np.sin(x),
        'y2': np.cos(x),
        'y3': np.sin(x + np.pi/4),
        'y4': np.cos(x + np.pi/4),
    }


@pytest.fixture
def sample_categorical_data():
    """Generate sample categorical data for testing.
    
    Returns:
        Dictionary with categories and values
    """
    np.random.seed(42)
    categories = ['A', 'B', 'C', 'D', 'E']
    return {
        'categories': categories,
        'values': np.random.randn(len(categories)),
        'values2': np.random.randn(len(categories)),
    }


@pytest.fixture
def sample_scatter_data():
    """Generate sample scatter plot data for testing.
    
    Returns:
        Dictionary with x, y, color arrays
    """
    np.random.seed(42)
    n = 50
    return {
        'x': np.random.randn(n),
        'y': np.random.randn(n),
        'colors': np.random.choice(['red', 'blue', 'green'], n),
        'sizes': np.random.uniform(20, 200, n),
    }


# ============================================================================
# Baseline Directory Fixture
# ============================================================================

@pytest.fixture
def baseline_dir(datadir):
    """Get the baseline directory for visual tests.
    
    Args:
        datadir: pytest-datadir fixture
    
    Returns:
        Path to baseline directory
    """
    baseline_path = Path(datadir) / "__baseline__"
    baseline_path.mkdir(parents=True, exist_ok=True)
    return baseline_path


# ============================================================================
# Diff Directory Fixture
# ============================================================================

@pytest.fixture
def diff_dir(tmp_path):
    """Get the diff directory for visual test failures.
    
    Args:
        tmp_path: pytest tmp_path fixture
    
    Returns:
        Path to diff directory
    """
    diff_path = tmp_path / "__diffs__"
    diff_path.mkdir(parents=True, exist_ok=True)
    return diff_path


# ============================================================================
# Version-Specific Basename Fixture
# ============================================================================

@pytest.fixture
def versioned_basename(matplotlib_version, request):
    """Generate a versioned basename for visual tests.
    
    This ensures that different library versions have separate
    baseline images, allowing for version-specific differences.
    
    Args:
        matplotlib_version: Matplotlib version fixture
        request: pytest request object
    
    Returns:
        Function that generates versioned basenames
    """
    def _basename(name: str) -> str:
        """Generate a versioned basename.
        
        Args:
            name: Base name for the test
        
        Returns:
            Versioned basename string
        """
        test_name = request.node.name
        version_suffix = matplotlib_version.replace('.', '_') if matplotlib_version else 'unknown'
        return f"{test_name}_{name}_mpl_{version_suffix}"
    
    return _basename
