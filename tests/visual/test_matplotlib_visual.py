"""Visual regression tests for matplotlib adapter."""

import pytest
import numpy as np
import matplotlib.pyplot as plt
import sane_figs


# ============================================================================
# Article Mode Tests
# ============================================================================

@pytest.mark.visual
@pytest.mark.matplotlib
def test_matplotlib_article_mode_figure(fig_regression, sample_data, matplotlib_version):
    """Test that article mode produces consistent figure output."""
    # Apply article mode
    sane_figs.setup(mode='article')
    
    # Create a simple figure
    fig, ax = plt.subplots()
    ax.plot(sample_data['x'], sample_data['y1'], label='sin(x)')
    ax.plot(sample_data['x'], sample_data['y2'], label='cos(x)')
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title('Test Figure')
    ax.legend()
    
    # Save for regression testing
    fig_regression.check(fig, basename=f"article_mode_mpl_{matplotlib_version}")


@pytest.mark.visual
@pytest.mark.matplotlib
def test_matplotlib_article_mode_font_sizes(fig_regression, sample_data, matplotlib_version):
    """Test that article mode applies correct font sizes."""
    # Apply article mode
    sane_figs.setup(mode='article')
    
    # Create a figure with text elements
    fig, ax = plt.subplots()
    ax.plot(sample_data['x'], sample_data['y1'])
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title('Article Mode Font Sizes')
    
    # Check with text elements
    text_elements = {
        'title': ax.title,
        'xlabel': ax.xaxis.label,
        'ylabel': ax.yaxis.label,
    }
    fig_regression.check_with_text(fig, basename=f"article_mode_fonts_mpl_{matplotlib_version}", text_elements=text_elements)


# ============================================================================
# Presentation Mode Tests
# ============================================================================

@pytest.mark.visual
@pytest.mark.matplotlib
def test_matplotlib_presentation_mode_figure(fig_regression, sample_data, matplotlib_version):
    """Test that presentation mode produces consistent figure output."""
    # Apply presentation mode
    sane_figs.setup(mode='presentation')
    
    # Create a simple figure
    fig, ax = plt.subplots()
    ax.plot(sample_data['x'], sample_data['y1'], label='sin(x)')
    ax.plot(sample_data['x'], sample_data['y2'], label='cos(x)')
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title('Test Figure')
    ax.legend()
    
    # Save for regression testing
    fig_regression.check(fig, basename=f"presentation_mode_mpl_{matplotlib_version}")


@pytest.mark.visual
@pytest.mark.matplotlib
def test_matplotlib_presentation_mode_font_sizes(fig_regression, sample_data, matplotlib_version):
    """Test that presentation mode applies correct font sizes."""
    # Apply presentation mode
    sane_figs.setup(mode='presentation')
    
    # Create a figure with text elements
    fig, ax = plt.subplots()
    ax.plot(sample_data['x'], sample_data['y1'])
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title('Presentation Mode Font Sizes')
    
    # Check with text elements
    text_elements = {
        'title': ax.title,
        'xlabel': ax.xaxis.label,
        'ylabel': ax.yaxis.label,
    }
    fig_regression.check_with_text(fig, basename=f"presentation_mode_fonts_mpl_{matplotlib_version}", text_elements=text_elements)


# ============================================================================
# Colorway Tests
# ============================================================================

@pytest.mark.visual
@pytest.mark.matplotlib
def test_matplotlib_colorway_default(fig_regression, sample_data, matplotlib_version):
    """Test that default colorway produces consistent output."""
    # Apply article mode with default colorway
    sane_figs.setup(mode='article', colorway='default')
    
    # Create a figure with multiple lines
    fig, ax = plt.subplots()
    ax.plot(sample_data['x'], sample_data['y1'], label='sin(x)')
    ax.plot(sample_data['x'], sample_data['y2'], label='cos(x)')
    ax.plot(sample_data['x'], sample_data['y3'], label='sin(x+π/4)')
    ax.plot(sample_data['x'], sample_data['y4'], label='cos(x+π/4)')
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title('Default Colorway')
    ax.legend()
    
    # Save for regression testing
    fig_regression.check(fig, basename=f"colorway_default_mpl_{matplotlib_version}")


@pytest.mark.visual
@pytest.mark.matplotlib
def test_matplotlib_colorway_nature(fig_regression, sample_data, matplotlib_version):
    """Test that nature colorway produces consistent output."""
    # Apply article mode with nature colorway
    sane_figs.setup(mode='article', colorway='nature')
    
    # Create a figure with multiple lines
    fig, ax = plt.subplots()
    ax.plot(sample_data['x'], sample_data['y1'], label='sin(x)')
    ax.plot(sample_data['x'], sample_data['y2'], label='cos(x)')
    ax.plot(sample_data['x'], sample_data['y3'], label='sin(x+π/4)')
    ax.plot(sample_data['x'], sample_data['y4'], label='cos(x+π/4)')
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title('Nature Colorway')
    ax.legend()
    
    # Save for regression testing
    fig_regression.check(fig, basename=f"colorway_nature_mpl_{matplotlib_version}")


@pytest.mark.visual
@pytest.mark.matplotlib
def test_matplotlib_colorway_vibrant(fig_regression, sample_data, matplotlib_version):
    """Test that vibrant colorway produces consistent output."""
    # Apply article mode with vibrant colorway
    sane_figs.setup(mode='article', colorway='vibrant')
    
    # Create a figure with multiple lines
    fig, ax = plt.subplots()
    ax.plot(sample_data['x'], sample_data['y1'], label='sin(x)')
    ax.plot(sample_data['x'], sample_data['y2'], label='cos(x)')
    ax.plot(sample_data['x'], sample_data['y3'], label='sin(x+π/4)')
    ax.plot(sample_data['x'], sample_data['y4'], label='cos(x+π/4)')
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title('Vibrant Colorway')
    ax.legend()
    
    # Save for regression testing
    fig_regression.check(fig, basename=f"colorway_vibrant_mpl_{matplotlib_version}")


@pytest.mark.visual
@pytest.mark.matplotlib
def test_matplotlib_colorway_pastel(fig_regression, sample_data, matplotlib_version):
    """Test that pastel colorway produces consistent output."""
    # Apply article mode with pastel colorway
    sane_figs.setup(mode='article', colorway='pastel')
    
    # Create a figure with multiple lines
    fig, ax = plt.subplots()
    ax.plot(sample_data['x'], sample_data['y1'], label='sin(x)')
    ax.plot(sample_data['x'], sample_data['y2'], label='cos(x)')
    ax.plot(sample_data['x'], sample_data['y3'], label='sin(x+π/4)')
    ax.plot(sample_data['x'], sample_data['y4'], label='cos(x+π/4)')
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title('Pastel Colorway')
    ax.legend()
    
    # Save for regression testing
    fig_regression.check(fig, basename=f"colorway_pastel_mpl_{matplotlib_version}")


@pytest.mark.visual
@pytest.mark.matplotlib
def test_matplotlib_colorway_colorblind_safe(fig_regression, sample_data, matplotlib_version):
    """Test that colorblind-safe colorway produces consistent output."""
    # Apply article mode with colorblind-safe colorway
    sane_figs.setup(mode='article', colorway='colorblind-safe')
    
    # Create a figure with multiple lines
    fig, ax = plt.subplots()
    ax.plot(sample_data['x'], sample_data['y1'], label='sin(x)')
    ax.plot(sample_data['x'], sample_data['y2'], label='cos(x)')
    ax.plot(sample_data['x'], sample_data['y3'], label='sin(x+π/4)')
    ax.plot(sample_data['x'], sample_data['y4'], label='cos(x+π/4)')
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title('Colorblind-Safe Colorway')
    ax.legend()
    
    # Save for regression testing
    fig_regression.check(fig, basename=f"colorway_colorblind_safe_mpl_{matplotlib_version}")


# ============================================================================
# Watermark Tests
# ============================================================================

@pytest.mark.visual
@pytest.mark.matplotlib
def test_matplotlib_text_watermark(fig_regression, sample_data, matplotlib_version):
    """Test that text watermark produces consistent output."""
    # Apply article mode with text watermark
    sane_figs.setup(mode='article', watermark='© 2025 Test Lab')
    
    # Create a figure
    fig, ax = plt.subplots()
    ax.plot(sample_data['x'], sample_data['y1'])
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title('Text Watermark')
    
    # Save for regression testing
    fig_regression.check(fig, basename=f"watermark_text_mpl_{matplotlib_version}")


@pytest.mark.visual
@pytest.mark.matplotlib
def test_matplotlib_watermark_positions(fig_regression, sample_data, matplotlib_version):
    """Test that watermark positions are consistent."""
    from sane_figs import create_text_watermark
    
    # Test different positions
    positions = ['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center']
    
    for i, position in enumerate(positions):
        # Reset and apply with watermark
        sane_figs.setup(mode='article', watermark=create_text_watermark(
            text='© 2025',
            position=position
        ))
        
        # Create a figure
        fig, ax = plt.subplots()
        ax.plot(sample_data['x'], sample_data['y1'])
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_title(f'Watermark {position}')
        
        # Save for regression testing
        fig_regression.check(fig, basename=f"watermark_{position}_mpl_{matplotlib_version}")


# ============================================================================
# Context Manager Tests
# ============================================================================

@pytest.mark.visual
@pytest.mark.matplotlib
def test_matplotlib_context_manager(fig_regression, sample_data, matplotlib_version):
    """Test that context manager produces consistent output."""
    # Use context manager
    with sane_figs.publication_style(mode='article'):
        fig, ax = plt.subplots()
        ax.plot(sample_data['x'], sample_data['y1'], label='sin(x)')
        ax.plot(sample_data['x'], sample_data['y2'], label='cos(x)')
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_title('Context Manager Test')
        ax.legend()
    
    # Save for regression testing
    fig_regression.check(fig, basename=f"context_manager_mpl_{matplotlib_version}")


# ============================================================================
# Style Reset Tests
# ============================================================================

@pytest.mark.visual
@pytest.mark.matplotlib
def test_matplotlib_style_reset(fig_regression, sample_data, matplotlib_version):
    """Test that style reset works correctly."""
    # Apply article mode
    sane_figs.setup(mode='article')
    
    # Create first figure with styling
    fig1, ax1 = plt.subplots()
    ax1.plot(sample_data['x'], sample_data['y1'])
    ax1.set_xlabel('X Axis')
    ax1.set_ylabel('Y Axis')
    ax1.set_title('Styled Figure')
    
    # Reset style
    sane_figs.reset()
    
    # Create second figure without styling
    fig2, ax2 = plt.subplots()
    ax2.plot(sample_data['x'], sample_data['y1'])
    ax2.set_xlabel('X Axis')
    ax2.set_ylabel('Y Axis')
    ax2.set_title('Reset Figure')
    
    # Check both figures
    fig_regression.check(fig1, basename=f"styled_before_reset_mpl_{matplotlib_version}")
    fig_regression.check(fig2, basename=f"styled_after_reset_mpl_{matplotlib_version}")


# ============================================================================
# Grid and Spine Tests
# ============================================================================

@pytest.mark.visual
@pytest.mark.matplotlib
def test_matplotlib_grid_and_spines(fig_regression, sample_data, matplotlib_version):
    """Test that grid and spine settings are consistent."""
    # Apply article mode
    sane_figs.setup(mode='article')
    
    # Create a figure
    fig, ax = plt.subplots()
    ax.plot(sample_data['x'], sample_data['y1'])
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title('Grid and Spines')
    
    # Save for regression testing
    fig_regression.check(fig, basename=f"grid_spines_mpl_{matplotlib_version}")


# ============================================================================
# Legend Tests
# ============================================================================

@pytest.mark.visual
@pytest.mark.matplotlib
def test_matplotlib_legend(fig_regression, sample_data, matplotlib_version):
    """Test that legend styling is consistent."""
    # Apply article mode
    sane_figs.setup(mode='article')
    
    # Create a figure with legend
    fig, ax = plt.subplots()
    ax.plot(sample_data['x'], sample_data['y1'], label='sin(x)')
    ax.plot(sample_data['x'], sample_data['y2'], label='cos(x)')
    ax.plot(sample_data['x'], sample_data['y3'], label='sin(x+π/4)')
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title('Legend Test')
    ax.legend(loc='best')
    
    # Save for regression testing
    fig_regression.check(fig, basename=f"legend_mpl_{matplotlib_version}")
