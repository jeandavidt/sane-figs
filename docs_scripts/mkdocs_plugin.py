"""
MkDocs plugin to automatically generate documentation figures.
"""

from mkdocs.plugins import BasePlugin
from mkdocs.config import Config
from pathlib import Path
import subprocess
import sys


class GenerateFiguresPlugin(BasePlugin):
    """MkDocs plugin that generates figures before building documentation."""

    def on_pre_build(self, config: Config) -> None:
        """Generate figures before the build process starts."""
        # Get the path to the generate_figures.py script
        plugin_dir = Path(__file__).parent
        generate_script = plugin_dir / "generate_figures.py"

        if not generate_script.exists():
            print(f"Warning: Figure generation script not found at {generate_script}")
            return

        print("Generating documentation figures...")
        try:
            # Run the figure generation script without capturing output
            # This allows progress print statements to be shown in real-time
            result = subprocess.run(
                [sys.executable, str(generate_script)],
                cwd=Path(__file__).parent.parent
            )

            if result.returncode == 0:
                print("Figures generated successfully!")
            else:
                print(f"Warning: Figure generation failed with return code {result.returncode}")
        except Exception as e:
            print(f"Warning: Error running figure generation: {e}")
