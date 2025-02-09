import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt

# X-coordinates for half-lane (including tire regions).
X_COORDS = [0.0, 0.475, 0.725, 2.275, 2.525, 3.0]

def generate_pavement_nodes(pavement_type, layers):
    """
    Generate nodes for the chosen pavement type and layer thicknesses.
    We automatically add 1.5 m for the subgrade below the final layer.
    
    Returns a tuple:
      (nodes, col_lines, row_lines)
      where 'nodes' is a set of (x, y, 0),
            col_lines/row_lines are for plotting.
    """
    # Build Y-coordinates from y=0 downward
    y_coords = [0.0]

    if pavement_type == "Flexible":
        thicknesses = [
            layers["surface"],
            layers["binder"],
            layers["base"],
            layers["subbase"]
        ]
    elif pavement_type == "Rigid":
        thicknesses = [
            layers["rigid_slab"],
            layers["rigid_subbase"]
        ]
    else:  # "Semi-Rigid"
        thicknesses = [
            layers["asphalt"],
            layers["ctb"],
            layers["semirigid_subbase"]
        ]

    current_y = 0.0
    for t in thicknesses:
        current_y -= t
        y_coords.append(current_y)

    # Add 1.5 m for the subgrade
    current_y -= 1.5
    y_coords.append(current_y)

    # Create set of nodes
    nodes = set()
    for y in y_coords:
        for x in X_COORDS:
            nodes.add((x, y, 0.0))

    # Build lines for plotting
    col_lines = []
    for x in X_COORDS:
        col_line = [(x, y, 0.0) for y in y_coords]
        col_lines.append(col_line)

    row_lines = []
    for y in y_coords:
        row_line = [(x, y, 0.0) for x in X_COORDS]
        row_lines.append(row_line)

    return nodes, col_lines, row_lines

def write_to_text(file_path, nodes_list):
    """
    Writes the file with the first line '/PREP7',
    then lines of the form 'N,nodeID,x,y,0'.
    """
    with open(file_path, "w") as f:
        f.write("/PREP7\n")
        for nid, x, y, z in nodes_list:
            f.write(f"N,{nid},{x},{y},{z}\n")

def plot_pavement(nodes, col_lines, row_lines):
    """
    Simple 2D plot of the pavement 'grid' using matplotlib,
    with each node labeled by (x,y).
    """
    plt.figure()
    # Plot vertical lines
    for col in col_lines:
        xs = [p[0] for p in col]
        ys = [p[1] for p in col]
        plt.plot(xs, ys, marker='o')
    
    # Plot horizontal lines
    for row in row_lines:
        xs = [p[0] for p in row]
        ys = [p[1] for p in row]
        plt.plot(xs, ys, marker='o')

    # Annotate each node with its (x,y) coordinate
    for (x, y, _) in nodes:
        # Format with 2 decimal places, small offset for readability
        plt.annotate(
            f"({x:.2f}, {y:.2f})",
            (x, y),
            xytext=(3, 3),
            textcoords="offset points",
            fontsize=8
        )

    plt.title("Pavement Cross-Section Nodes")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m, negative down)")
    plt.gca().invert_yaxis()  # top layer at y=0
    plt.axis("equal")
    plt.grid(True)
    plt.show()

def on_pavement_change(*args):
    """
    Called whenever the pavement type dropdown changes.
    Show/hide the relevant entry fields for the chosen type.
    """
    ptype = pavement_type_var.get()

    # Hide all first
    for w in flexible_widgets + rigid_widgets + semirigid_widgets:
        w.grid_remove()

    # Show relevant fields
    if ptype == "Flexible":
        for w in flexible_widgets:
            w.grid()
    elif ptype == "Rigid":
        for w in rigid_widgets:
            w.grid()
    elif ptype == "Semi-Rigid":
        for w in semirigid_widgets:
            w.grid()

def on_generate():
    # 1) Check which pavement type
    ptype = pavement_type_var.get()
    if ptype not in ("Flexible", "Rigid", "Semi-Rigid"):
        messagebox.showerror("Error", "Please select a pavement type.")
        return

    # 2) Gather thickness inputs
    try:
        if ptype == "Flexible":
            layers = {
                "surface": float(surface_var.get()),
                "binder": float(binder_var.get()),
                "base": float(base_var.get()),
                "subbase": float(subbase_var.get())
            }
        elif ptype == "Rigid":
            layers = {
                "rigid_slab": float(rigid_slab_var.get()),
                "rigid_subbase": float(rigid_subbase_var.get())
            }
        else:  # "Semi-Rigid"
            layers = {
                "asphalt": float(asphalt_var.get()),
                "ctb": float(ctb_var.get()),
                "semirigid_subbase": float(semirigid_subbase_var.get())
            }
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric thicknesses.")
        return

    # 3) Generate nodes
    nodes, col_lines, row_lines = generate_pavement_nodes(ptype, layers)

    # 4) Sort so top row (y=0) is first, left to right,
    #    then proceed downward:
    sorted_nodes = sorted(nodes, key=lambda p: (-p[1], p[0]))
    node_list = [(i+1, x, y, z) for i, (x, y, z) in enumerate(sorted_nodes)]

    # 5) Ask user where to save
    file_path = filedialog.asksaveasfilename(
        title="Save Pavement Node Coordinates As...",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not file_path:
        messagebox.showinfo("Canceled", "File save canceled.")
        return

    # 6) Write output
    write_to_text(file_path, node_list)
    messagebox.showinfo("Success", f"Pavement nodes saved to:\n{file_path}")

    # 7) Plot (now passing 'nodes' in addition to lines)
    plot_pavement(nodes, col_lines, row_lines)

# ---------------- Build the GUI with explicit row placements ----------------
root = tk.Tk()
root.title("ANSYS Pavement Node Generator")

# Pavement type
pavement_type_var = tk.StringVar(value="Flexible")
pavement_type_var.trace_add("write", on_pavement_change)

# Label (example credit label)
tk.Label(root, text='Software created by W.Johnson').grid(row=7, column=0, padx=5, pady=30, sticky='e')

tk.Label(root, text="Select Pavement Type:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
ptype_menu = tk.OptionMenu(root, pavement_type_var, "Flexible", "Rigid", "Semi-Rigid")
ptype_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

#
# Flexible
#
surface_label = tk.Label(root, text="Surface thickness (m):")
surface_var = tk.StringVar(value="0.06")
surface_entry = tk.Entry(root, textvariable=surface_var, width=8)

binder_label = tk.Label(root, text="Binder thickness (m):")
binder_var = tk.StringVar(value="0.08")
binder_entry = tk.Entry(root, textvariable=binder_var, width=8)

base_label = tk.Label(root, text="Base thickness (m):")
base_var = tk.StringVar(value="0.20")
base_entry = tk.Entry(root, textvariable=base_var, width=8)

subbase_label = tk.Label(root, text="Subbase thickness (m):")
subbase_var = tk.StringVar(value="0.20")
subbase_entry = tk.Entry(root, textvariable=subbase_var, width=8)

surface_label.grid(row=1, column=0, padx=5, pady=2, sticky="e")
surface_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")

binder_label.grid(row=2, column=0, padx=5, pady=2, sticky="e")
binder_entry.grid(row=2, column=1, padx=5, pady=2, sticky="w")

base_label.grid(row=3, column=0, padx=5, pady=2, sticky="e")
base_entry.grid(row=3, column=1, padx=5, pady=2, sticky="w")

subbase_label.grid(row=4, column=0, padx=5, pady=2, sticky="e")
subbase_entry.grid(row=4, column=1, padx=5, pady=2, sticky="w")

flexible_widgets = [
    surface_label, surface_entry,
    binder_label, binder_entry,
    base_label, base_entry,
    subbase_label, subbase_entry
]

#
# Rigid
#
rigid_slab_label = tk.Label(root, text="Concrete slab thickness (m):")
rigid_slab_var = tk.StringVar(value="0.20")
rigid_slab_entry = tk.Entry(root, textvariable=rigid_slab_var, width=8)

rigid_subbase_label = tk.Label(root, text="Subbase thickness (m):")
rigid_subbase_var = tk.StringVar(value="0.20")
rigid_subbase_entry = tk.Entry(root, textvariable=rigid_subbase_var, width=8)

rigid_slab_label.grid(row=1, column=2, padx=5, pady=2, sticky="e")
rigid_slab_entry.grid(row=1, column=3, padx=5, pady=2, sticky="w")

rigid_subbase_label.grid(row=2, column=2, padx=5, pady=2, sticky="e")
rigid_subbase_entry.grid(row=2, column=3, padx=5, pady=2, sticky="w")

rigid_widgets = [
    rigid_slab_label, rigid_slab_entry,
    rigid_subbase_label, rigid_subbase_entry
]

#
# Semi-Rigid
#
asphalt_label = tk.Label(root, text="Asphalt layer thickness (m):")
asphalt_var = tk.StringVar(value="0.08")
asphalt_entry = tk.Entry(root, textvariable=asphalt_var, width=8)

ctb_label = tk.Label(root, text="Cement treated base (m):")
ctb_var = tk.StringVar(value="0.20")
ctb_entry = tk.Entry(root, textvariable=ctb_var, width=8)

semirigid_subbase_label = tk.Label(root, text="Subbase thickness (m):")
semirigid_subbase_var = tk.StringVar(value="0.20")
semirigid_subbase_entry = tk.Entry(root, textvariable=semirigid_subbase_var, width=8)

asphalt_label.grid(row=3, column=2, padx=5, pady=2, sticky="e")
asphalt_entry.grid(row=3, column=3, padx=5, pady=2, sticky="w")

ctb_label.grid(row=4, column=2, padx=5, pady=2, sticky="e")
ctb_entry.grid(row=4, column=3, padx=5, pady=2, sticky="w")

semirigid_subbase_label.grid(row=5, column=2, padx=5, pady=2, sticky="e")
semirigid_subbase_entry.grid(row=5, column=3, padx=5, pady=2, sticky="w")

semirigid_widgets = [
    asphalt_label, asphalt_entry,
    ctb_label, ctb_entry,
    semirigid_subbase_label, semirigid_subbase_entry
]

# Initially hide all
for w in flexible_widgets + rigid_widgets + semirigid_widgets:
    w.grid_remove()

# Generate button at the bottom
generate_button = tk.Button(root, text="Generate Pavement Nodes", command=on_generate)
generate_button.grid(row=10, column=0, columnspan=4, pady=10)

# Initialize widget visibility based on the default pavement type
on_pavement_change()

root.mainloop()
