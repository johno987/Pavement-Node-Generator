# Pavement Node Generator

This Python script provides a simple GUI for generating node coordinates in a pavement cross-section, saving them to a text file (compatible with ANSYS `/PREP7` format), and plotting the resulting grid in a 2D diagram. You can configure different pavement structures (Flexible, Rigid, or Semi-Rigid) by specifying individual layer thicknesses.

---

## Features

- **Interactive GUI**: Uses `tkinter` for a user-friendly interface.  
- **Pavement Type Selection**: Supports Flexible, Rigid, and Semi-Rigid pavement designs.  
- **Layer Thickness Input**: Dynamically adapts input fields based on pavement type.  
- **File Export**: Writes node coordinates to a text file, prefixed with `/PREP7` commands.  
- **Visualisation**: Plots the generated pavement layers and node grid using `matplotlib`.  

---

## Requirements

- **Python** 3.7+ (should work with most 3.x versions)  
- **tkinter** (commonly included in standard Python installations on Windows/macOS; for Linux, install via system packages)  
- **matplotlib** (install with `pip install matplotlib` if not already installed)

---

## Installation

1. Clone or download this repository.
2. Ensure you have Python 3.7+ installed.
3. Install any missing dependencies:
   ```bash
   pip install matplotlib

## Usage

1. Open a terminal or command prompt
2. Navigate to the folder containing this script
3. Run
   ```bash
   python Pavement_GeneratorLabel.py
4. Select the Pavement Type from the dropdown (Flexible, Rigid, or Semi-Rigid).
5. Adjust the displayed layer thicknesses as needed.
6. Click Generate Pavement Nodes.
   - You’ll be prompted to choose a save location for the output file.
   - After saving, the script automatically plots the cross-section with node labels.

## How It Works

1. User Input: The GUI collects layer thicknesses for the chosen pavement type.
2. Node Generation:
   - X-coordinates are predefined for a half-lane (including tyre regions).
   - Y-coordinates are calculated by subtracting layer thicknesses from a starting reference (y=0).
   - An additional 1.5m is automatically added for the subgrade.
3. File Writing:
   - Exports each node in the format N,nodeID,x,y,0.0, prefixed by /PREP7.
4. Plotting:
   - Displays a 2D grid of the generated nodes using matplotlib, labelling each node with its (x, y) coordinate.
