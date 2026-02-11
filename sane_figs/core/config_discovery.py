"""Configuration discovery for sane-figs."""

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sane_figs.core.presets import Preset
    from sane_figs.styling.colorways import Colorway


def get_config_dir() -> Path:
    """
    Get the user configuration directory for sane-figs.

    Returns:
        Path to the configuration directory.
    """
    # Try XDG_CONFIG_HOME first (Linux)
    config_home = Path.home() / ".config" / "sane-figs"
    if config_home.exists() or config_home.parent.exists():
        return config_home

    # Fall back to ~/.sane_figs
    return Path.home() / ".sane_figs"


def ensure_config_dir() -> Path:
    """
    Ensure the configuration directory exists.

    Returns:
        Path to the configuration directory.
    """
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def discover_preset_files() -> list[Path]:
    """
    Discover preset files from standard locations.

    Locations are checked in order of precedence (highest first):
    1. ./sane_figs.yaml (project root)
    2. ./.sane_figs/presets.yaml (project directory)
    3. ~/.config/sane-figs/presets.yaml (user config)
    4. ~/.sane_figs.yaml (user home)

    Returns:
        List of paths to preset files, in order of precedence.
    """
    preset_files = []

    # Get current working directory
    cwd = Path.cwd()

    # 1. ./sane_figs.yaml (project root)
    project_yaml = cwd / "sane_figs.yaml"
    if project_yaml.exists():
        preset_files.append(project_yaml)

    # 2. ./.sane_figs/presets.yaml (project directory)
    project_dir_yaml = cwd / ".sane_figs" / "presets.yaml"
    if project_dir_yaml.exists():
        preset_files.append(project_dir_yaml)

    # 3. ~/.config/sane-figs/presets.yaml (user config)
    config_dir = get_config_dir()
    config_yaml = config_dir / "presets.yaml"
    if config_yaml.exists():
        preset_files.append(config_yaml)

    # 4. ~/.sane_figs.yaml (user home)
    home_yaml = Path.home() / ".sane_figs.yaml"
    if home_yaml.exists():
        preset_files.append(home_yaml)

    return preset_files


def discover_colorway_files() -> list[Path]:
    """
    Discover colorway files from standard locations.

    Locations are checked in order of precedence (highest first):
    1. ./colorways.yaml (project root)
    2. ./.sane_figs/colorways.yaml (project directory)
    3. ~/.config/sane-figs/colorways.yaml (user config)
    4. ~/.colorways.yaml (user home)

    Returns:
        List of paths to colorway files, in order of precedence.
    """
    colorway_files = []

    # Get current working directory
    cwd = Path.cwd()

    # 1. ./colorways.yaml (project root)
    project_yaml = cwd / "colorways.yaml"
    if project_yaml.exists():
        colorway_files.append(project_yaml)

    # 2. ./.sane_figs/colorways.yaml (project directory)
    project_dir_yaml = cwd / ".sane_figs" / "colorways.yaml"
    if project_dir_yaml.exists():
        colorway_files.append(project_dir_yaml)

    # 3. ~/.config/sane-figs/colorways.yaml (user config)
    config_dir = get_config_dir()
    config_yaml = config_dir / "colorways.yaml"
    if config_yaml.exists():
        colorway_files.append(config_yaml)

    # 4. ~/.colorways.yaml (user home)
    home_yaml = Path.home() / ".colorways.yaml"
    if home_yaml.exists():
        colorway_files.append(home_yaml)

    return colorway_files


def load_all_discovered_presets() -> list["Preset"]:
    """
    Load all presets from discovered configuration files.

    Returns:
        List of Preset objects from all discovered files.
    """
    from sane_figs.core.yaml_parser import load_presets_from_yaml

    all_presets = []
    preset_files = discover_preset_files()

    for preset_file in preset_files:
        try:
            presets = load_presets_from_yaml(preset_file)
            all_presets.extend(presets)
        except Exception:
            # Silently skip files that can't be loaded
            continue

    return all_presets


def load_all_discovered_colorways() -> list["Colorway"]:
    """
    Load all colorways from discovered configuration files.

    Returns:
        List of Colorway objects from all discovered files.
    """
    from sane_figs.core.yaml_parser import load_colorways_from_yaml

    all_colorways = []
    colorway_files = discover_colorway_files()

    for colorway_file in colorway_files:
        try:
            colorways = load_colorways_from_yaml(colorway_file)
            all_colorways.extend(colorways)
        except Exception:
            # Silently skip files that can't be loaded
            continue

    return all_colorways
