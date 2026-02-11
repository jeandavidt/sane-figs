# Testing Guide

This document explains the testing system used in the sane-figs repository, including how to run tests, write new tests, and understand the testing architecture.

## Table of Contents

- [Overview](#overview)
- [Test Framework](#test-framework)
- [Test Organization](#test-organization)
- [Running Tests](#running-tests)
- [Version-Specific Testing](#version-specific-testing)
- [Visual Regression Tests](#visual-regression-tests)
- [Writing Tests](#writing-tests)
- [Test Fixtures](#test-fixtures)
- [Test Markers](#test-markers)
- [Coverage](#coverage)
- [Continuous Integration](#continuous-integration)

## Overview

The sane-figs testing system is designed to ensure compatibility across multiple Python versions (3.8-3.12) and multiple visualization library versions (Matplotlib, Seaborn, Plotly, Altair). The system uses:

- **pytest** as the test runner
- **tox** for multi-environment testing
- **pytest-regressions** for visual regression testing
- **pytest-cov** for code coverage
- **pytest-xdist** for parallel test execution

## Test Framework

### Core Dependencies

The testing framework relies on the following packages (defined in [`pyproject.toml`](pyproject.toml:59-75)):

```toml
[project.optional-dependencies]
test = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-regressions>=2.5.0",
    "pytest-xdist>=3.0.0",
    "packaging>=23.0.0",
]
```

### Pytest Configuration

Pytest is configured in [`pyproject.toml`](pyproject.toml:102-121):

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --cov=sane_figs --cov-report=term-missing --strict-markers"
```

## Test Organization

```
tests/
├── __init__.py
├── conftest.py              # Main pytest configuration and fixtures
├── test_colorways.py        # Colorway module tests
├── test_presets.py          # Preset module tests
├── test_watermarks.py       # Watermark module tests
└── visual/                  # Visual regression tests
    ├── __init__.py
    ├── conftest.py          # Visual test fixtures
    └── test_matplotlib_visual.py
```

### Unit Tests

Unit tests are located in the `tests/` directory and test individual modules:

- [`test_colorways.py`](tests/test_colorways.py) - Tests for colorway functionality
- [`test_presets.py`](tests/test_presets.py) - Tests for preset configurations
- [`test_watermarks.py`](tests/test_watermarks.py) - Tests for watermark functionality

### Visual Regression Tests

Visual regression tests are located in [`tests/visual/`](tests/visual/) and verify that figure output remains consistent across versions. These tests use [`pytest-regressions`](https://pytest-regressions.readthedocs.io/) to compare generated figures against baseline images.

## Running Tests

### Quick Start

Run all tests with the default Python version:

```bash
pytest tests/ -v
```

### Using Tox

Tox is the recommended way to run tests across multiple environments. See [`tox.ini`](tox.ini) for all available environments.

#### Run all test environments:

```bash
tox
```

#### Run specific environments:

```bash
# Run tests with Python 3.11 and all libraries
tox -e py311-all

# Run tests with minimum matplotlib version
tox -e py38-matplotlib-min

# Run visual regression tests
tox -e visual

# Run linting
tox -e lint

# Run full test suite
tox -e full
```

#### Available Tox Environments

| Environment | Description |
|-------------|-------------|
| `py38-matplotlib-min` | Python 3.8 with minimum matplotlib (2.0.x) |
| `py38-seaborn-min` | Python 3.8 with minimum seaborn (0.9.x) |
| `py38-plotly-min` | Python 3.8 with minimum plotly (4.0.x) |
| `py38-altair-min` | Python 3.8 with minimum altair (3.0.x) |
| `py310-matplotlib-latest` | Python 3.10 with latest matplotlib |
| `py310-seaborn-latest` | Python 3.10 with latest seaborn |
| `py310-plotly-latest` | Python 3.10 with latest plotly |
| `py310-altair-latest` | Python 3.10 with latest altair |
| `py312-matplotlib-latest` | Python 3.12 with latest matplotlib |
| `py312-seaborn-latest` | Python 3.12 with latest seaborn |
| `py312-plotly-latest` | Python 3.12 with latest plotly |
| `py312-altair-latest` | Python 3.12 with latest altair |
| `py39-all` | Python 3.9 with all libraries |
| `py311-all` | Python 3.11 with all libraries |
| `lint` | Run linting and type checking |
| `visual` | Run visual regression tests |
| `full` | Run all tests with all library versions |
| `format` | Format code with black and ruff |
| `docs` | Build documentation |
| `clean` | Clean up build artifacts |
| `report` | Generate coverage report |

### Running Tests by Marker

Run tests with specific markers:

```bash
# Run only matplotlib tests
pytest tests/ -v -m matplotlib

# Run only seaborn tests
pytest tests/ -v -m seaborn

# Run only visual regression tests
pytest tests/ -v -m visual

# Run tests for matplotlib 3.5+
pytest tests/ -v -m matplotlib_3_5
```

### Running Tests in Parallel

Use pytest-xdist to run tests in parallel:

```bash
pytest tests/ -v -n auto
```

## Version-Specific Testing

The testing system automatically handles version-specific tests through a combination of fixtures and markers.

### Version Detection Fixtures

The main [`conftest.py`](tests/conftest.py) provides session-scoped fixtures for detecting installed library versions:

```python
@pytest.fixture(scope="session")
def matplotlib_version() -> Optional[str]:
    """Get the installed matplotlib version."""
    try:
        import matplotlib
        return matplotlib.__version__
    except ImportError:
        return None
```

Similar fixtures exist for:
- [`seaborn_version()`](tests/conftest.py:26-37)
- [`plotly_version()`](tests/conftest.py:40-51)
- [`altair_version()`](tests/conftest.py:54-65)
- [`python_version()`](tests/conftest.py:68-75)

### Version Tuple Fixtures

For easy version comparison, tuple fixtures are provided:

```python
@pytest.fixture(scope="session")
def matplotlib_version_tuple(matplotlib_version: Optional[str]) -> Optional[tuple]:
    """Get matplotlib version as a tuple for comparison."""
    if matplotlib_version is None:
        return None
    try:
        import packaging.version
        return tuple(map(int, packaging.version.parse(matplotlib_version).base_version.split('.')))
    except Exception:
        return None
```

### Automatic Test Skipping

The [`pytest_collection_modifyitems()`](tests/conftest.py:201-278) hook automatically skips tests that require specific library versions that are not installed or are incompatible:

```python
def pytest_collection_modifyitems(config, items):
    """Skip tests based on installed library versions."""
    # ... version detection logic ...
    
    for item in items:
        # Skip matplotlib version-specific tests
        if mpl_ver:
            if item.get_closest_marker("matplotlib_3_5") and mpl_ver < packaging.version.parse("3.5.0"):
                item.add_marker(pytest.mark.skip(reason=f"Requires matplotlib 3.5+, found {mpl_ver}"))
        else:
            if any(m in item.keywords for m in ["matplotlib_min", "matplotlib_3_0", "matplotlib_3_5", "matplotlib"]):
                item.add_marker(pytest.mark.skip(reason="Matplotlib not installed"))
```

### Helper Skip Fixtures

Convenience fixtures are provided for manual skipping:

```python
@pytest.fixture
def skip_if_no_matplotlib(matplotlib_version: Optional[str]):
    """Skip test if matplotlib is not installed."""
    if matplotlib_version is None:
        pytest.skip("Matplotlib not installed")

@pytest.fixture
def skip_if_matplotlib_lt(matplotlib_version_tuple: Optional[tuple], min_version: tuple):
    """Skip test if matplotlib version is less than min_version."""
    if matplotlib_version_tuple is None:
        pytest.skip("Matplotlib not installed")
    if matplotlib_version_tuple < min_version:
        pytest.skip(f"Requires matplotlib {min_version[0]}.{min_version[1]}.{min_version[2]}+, found {matplotlib_version_tuple}")
```

## Visual Regression Tests

Visual regression tests ensure that figure output remains consistent across versions. These tests are located in [`tests/visual/`](tests/visual/).

### Visual Test Configuration

The [`tests/visual/conftest.py`](tests/visual/conftest.py) provides:

1. **Matplotlib Setup** - Ensures consistent headless testing:

```python
@pytest.fixture(autouse=True)
def setup_matplotlib():
    """Setup matplotlib for consistent testing."""
    matplotlib.use('Agg', force=True)
    plt.rcParams['figure.figsize'] = (6.4, 4.8)
    plt.rcParams['figure.dpi'] = 100
    
    yield
    
    plt.close('all')
```

2. **Figure Regression Fixture** - Custom fixture for comparing figures:

```python
@pytest.fixture
def fig_regression(num_regression, datadir, request):
    """Custom fixture for figure regression testing."""
    class FigureRegression:
        def check(self, fig, basename: str, tolerance: float = 1.0):
            """Check figure against baseline."""
            # Convert figure to image array
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            
            from PIL import Image
            img = Image.open(buf)
            img_array = np.array(img)
            
            # Compare against baseline
            self.num_regression.check(img_array, basename=basename, default_tolerance=tolerance)
    
    return FigureRegression(num_regression, datadir, request)
```

3. **Sample Data Fixtures** - Provide consistent test data:

```python
@pytest.fixture
def sample_data():
    """Generate sample data for testing."""
    x = np.linspace(0, 10, 100)
    return {
        'x': x,
        'y1': np.sin(x),
        'y2': np.cos(x),
        'y3': np.sin(x + np.pi/4),
        'y4': np.cos(x + np.pi/4),
    }
```

### Writing Visual Tests

Visual tests are marked with `@pytest.mark.visual` and use the `fig_regression` fixture:

```python
@pytest.mark.visual
@pytest.mark.matplotlib
def test_matplotlib_article_mode_figure(fig_regression, sample_data, matplotlib_version):
    """Test that article mode produces consistent figure output."""
    sane_figs.setup(mode='article')
    
    fig, ax = plt.subplots()
    ax.plot(sample_data['x'], sample_data['y1'], label='sin(x)')
    ax.plot(sample_data['x'], sample_data['y2'], label='cos(x)')
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title('Test Figure')
    ax.legend()
    
    fig_regression.check(fig, basename=f"article_mode_mpl_{matplotlib_version}")
```

### Updating Baselines

When visual tests fail due to intentional changes, update baselines:

```bash
# Update all baselines
pytest tests/visual/ --regression -v --force-regen

# Update specific test baseline
pytest tests/visual/test_matplotlib_visual.py::test_name --regression --force-regen
```

## Writing Tests

### Unit Test Structure

Unit tests follow standard pytest conventions:

```python
"""Tests for module_name module."""

import pytest
from sane_figs.module_name import function_name

def test_function_name_basic():
    """Test basic functionality of function_name."""
    result = function_name(input_data)
    assert result == expected_output

def test_function_name_edge_case():
    """Test edge case for function_name."""
    with pytest.raises(ValueError, match="Expected error message"):
        function_name(invalid_input)

@pytest.mark.matplotlib
def test_function_name_with_matplotlib(skip_if_no_matplotlib):
    """Test function_name with matplotlib."""
    # Test code here
    pass
```

### Test Naming Conventions

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`
- Docstrings: Describe what is being tested

### Using Fixtures

Fixtures are automatically discovered and can be used as function arguments:

```python
def test_with_version_fixture(matplotlib_version, matplotlib_version_tuple):
    """Test using version fixtures."""
    if matplotlib_version:
        print(f"Testing with matplotlib {matplotlib_version}")
        assert matplotlib_version_tuple[0] >= 2
```

## Test Fixtures

### Available Fixtures

The following fixtures are available in [`tests/conftest.py`](tests/conftest.py):

| Fixture | Description |
|---------|-------------|
| `matplotlib_version` | Installed matplotlib version string |
| `seaborn_version` | Installed seaborn version string |
| `plotly_version` | Installed plotly version string |
| `altair_version` | Installed altair version string |
| `python_version` | Current Python version string |
| `matplotlib_version_tuple` | Matplotlib version as tuple (major, minor, patch) |
| `seaborn_version_tuple` | Seaborn version as tuple |
| `plotly_version_tuple` | Plotly version as tuple |
| `altair_version_tuple` | Altair version as tuple |
| `skip_if_no_matplotlib` | Skip test if matplotlib not installed |
| `skip_if_no_seaborn` | Skip test if seaborn not installed |
| `skip_if_no_plotly` | Skip test if plotly not installed |
| `skip_if_no_altair` | Skip test if altair not installed |
| `skip_if_matplotlib_lt` | Skip test if matplotlib < min_version |
| `skip_if_seaborn_lt` | Skip test if seaborn < min_version |
| `skip_if_plotly_lt` | Skip test if plotly < min_version |
| `skip_if_altair_lt` | Skip test if altair < min_version |

### Visual Test Fixtures

The following fixtures are available in [`tests/visual/conftest.py`](tests/visual/conftest.py):

| Fixture | Description |
|---------|-------------|
| `setup_matplotlib` | Auto-use fixture for matplotlib setup |
| `fig_regression` | Custom figure regression fixture |
| `sample_data` | Sample numeric data for testing |
| `sample_categorical_data` | Sample categorical data for testing |
| `sample_scatter_data` | Sample scatter plot data for testing |
| `baseline_dir` | Path to baseline directory |
| `diff_dir` | Path to diff directory for failures |
| `versioned_basename` | Function to generate versioned basenames |

## Test Markers

### Available Markers

The following markers are defined in [`pyproject.toml`](pyproject.toml:108-121) and [`tests/conftest.py`](tests/conftest.py:150-198):

| Marker | Description |
|--------|-------------|
| `visual` | Marks tests as visual regression tests |
| `matplotlib_min` | Tests for matplotlib minimum version (2.0.x) |
| `matplotlib_3_0` | Tests for matplotlib 3.0+ |
| `matplotlib_3_5` | Tests for matplotlib 3.5+ |
| `seaborn_0_11` | Tests for seaborn 0.11+ |
| `seaborn_0_12` | Tests for seaborn 0.12+ |
| `plotly_5_0` | Tests for plotly 5.0+ |
| `altair_5_0` | Tests for altair 5.0+ |
| `matplotlib` | Tests requiring matplotlib |
| `seaborn` | Tests requiring seaborn |
| `plotly` | Tests requiring plotly |
| `altair` | Tests requiring altair |

### Using Markers

```python
@pytest.mark.matplotlib
def test_matplotlib_feature():
    """Test matplotlib-specific feature."""
    pass

@pytest.mark.visual
@pytest.mark.matplotlib
def test_visual_regression():
    """Test visual regression."""
    pass

@pytest.mark.matplotlib_3_5
def test_matplotlib_3_5_feature():
    """Test feature requiring matplotlib 3.5+."""
    pass
```

## Coverage

### Generating Coverage Reports

Coverage is automatically generated when running tests with pytest-cov:

```bash
# Terminal coverage report
pytest tests/ -v --cov=sane_figs --cov-report=term-missing

# HTML coverage report
pytest tests/ -v --cov=sane_figs --cov-report=html

# Both terminal and HTML
pytest tests/ -v --cov=sane_figs --cov-report=term-missing --cov-report=html
```

### Coverage with Tox

```bash
# Run tests with coverage
tox -e py311-all

# Generate combined coverage report
tox -e report
```

### Coverage Goals

The project aims for:
- **Line coverage**: > 80%
- **Branch coverage**: > 70%

## Continuous Integration

### GitHub Actions

The repository uses GitHub Actions for CI/CD. The workflow is defined in `.github/workflows/` and typically includes:

1. **Linting** - Run black, ruff, and mypy
2. **Testing** - Run tests across multiple Python versions
3. **Coverage** - Generate and upload coverage reports
4. **Visual Tests** - Run visual regression tests

### Local CI Simulation

To simulate CI locally:

```bash
# Run linting
tox -e lint

# Run all tests
tox

# Run visual tests
tox -e visual
```

## Best Practices

### Writing Tests

1. **Keep tests independent** - Each test should be able to run in isolation
2. **Use descriptive names** - Test names should clearly describe what is being tested
3. **Test edge cases** - Include tests for boundary conditions and error cases
4. **Use fixtures** - Leverage fixtures for common setup/teardown logic
5. **Mark tests appropriately** - Use markers to categorize tests

### Version-Specific Tests

1. **Use markers** - Mark tests with appropriate version markers
2. **Document requirements** - Clearly document version requirements in docstrings
3. **Handle missing libraries** - Tests should gracefully handle missing libraries

### Visual Tests

1. **Use consistent data** - Use provided sample data fixtures
2. **Version baselines** - Include version in baseline filenames
3. **Test text elements** - Use `check_with_text()` for figures with dynamic text
4. **Keep tests focused** - Each visual test should verify one aspect

## Troubleshooting

### Tests Skipped Unexpectedly

If tests are being skipped unexpectedly:

1. Check installed library versions: `pip list`
2. Verify markers are correctly applied
3. Check [`pytest_collection_modifyitems()`](tests/conftest.py:201-278) logic

### Visual Tests Failing

If visual tests fail:

1. Check if the change is intentional
2. Update baselines with `--force-regen`
3. Verify matplotlib backend is set to 'Agg'
4. Check for platform-specific rendering differences

### Coverage Issues

If coverage is lower than expected:

1. Run tests with verbose output: `pytest -v --cov=sane_figs --cov-report=term-missing`
2. Check for missing test cases
3. Verify all code paths are tested

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [tox Documentation](https://tox.wiki/)
- [pytest-regressions Documentation](https://pytest-regressions.readthedocs.io/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
