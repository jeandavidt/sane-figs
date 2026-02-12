"""MkDocs hooks for sane-figs documentation."""

from pathlib import Path
import subprocess
import sys


def on_pre_build(config):
    """Generate figures and export Marimo notebooks before the build process starts."""
    project_root = Path(__file__).parent.parent
    docs_source = project_root / "docs_source"

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

    # Export Marimo notebooks to docs_source
    print("\nExporting Marimo notebooks to HTML WASM...")
    marimo_notebooks = [
        ("examples/interactive_demo.py", "interactive_demo.html"),
        ("examples/size_comparison_demo.py", "size_comparison_demo.html"),
    ]

    for notebook_path, output_name in marimo_notebooks:
        try:
            output_path = docs_source / output_name
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "marimo",
                    "export",
                    "html-wasm",
                    notebook_path,
                    "--mode",
                    "run",
                    "--no-show-code",
                    "-o",
                    str(output_path),
                    "-f",
                ],
                capture_output=True,
                text=True,
                cwd=project_root,
            )

            if result.returncode == 0:
                print(f"Exported {notebook_path} to {output_name}")
            else:
                print(f"Warning: Failed to export {notebook_path}")
                if result.stderr:
                    print(result.stderr)
        except Exception as e:
            print(f"Warning: Error exporting {notebook_path}: {e}")
