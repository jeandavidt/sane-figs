import matplotlib.pyplot as plt
import sane_figs
import numpy as np
import os

def create_dummy_plot(title):
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    plt.plot(x, y1, label='Sin(x)')
    plt.plot(x, y2, label='Cos(x)')
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()

def main():
    presets = ['ulaval', 'modeleau', 'marimo', 'latex']
    
    output_dir = "verification_output"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Generating figures in {output_dir}...")
    
    for preset in presets:
        try:
            print(f"Testing preset: {preset}")
            sane_figs.setup(mode=preset)
            
            # Create Matplotlib figure
            plt.figure()
            create_dummy_plot(f"{preset.capitalize()} Theme")
            
            # Debug information to confirm successful configuration
            print(f"  - Font Family: {plt.rcParams['font.family']}")
            if preset == 'latex':
                 print(f"  - Math Fontset: {plt.rcParams.get('mathtext.fontset')}")
            
            plt.savefig(f"{output_dir}/{preset}_matplotlib.png")
            plt.close()
            
            print(f"  - Generated {preset}_matplotlib.png")
            
        except Exception as e:
            print(f"  - Failed to generate {preset}: {e}")

if __name__ == "__main__":
    main()
