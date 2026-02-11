"""MkDocs hooks for sane-figs documentation."""

from pathlib import Path
import subprocess
import sys


def on_pre_build(config):
    """Generate figures before the build process starts."""
    project_root = Path(__file__).parent.parent

    print("Generating documentation figures...")
    try:
        # Run the figure generation script as a module
        result = subprocess.run(
            [sys.executable, "-m", "docs_scripts.generate_figures"],
            capture_output=True,
            text=True,
            cwd=project_root
        )

        if result.returncode == 0:
            print("Figures generated successfully!")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"Warning: Figure generation failed with return code {result.returncode}")
            if result.stderr:
                print(result.stderr)
    except Exception as e:
        print(f"Warning: Error running figure generation: {e}")
