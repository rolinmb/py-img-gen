import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import math

# Allowed math functions and constants
safe_dict = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
safe_dict.update({"abs": abs, "min": min, "max": max})

preview_img = None  # Global reference to avoid garbage collection

def generate_image():
    global preview_img
    filename = entry_filename.get().strip()
    if not filename:
        messagebox.showerror("Error", "Please enter a file name")
        return

    if not filename.lower().endswith(".png"):
        filename += ".png"

    filepath = os.path.join("img", filename)
    width, height = 256, 256
    img = Image.new("RGBA", (width, height))

    formulas = {
        "r": entry_r.get().strip(),
        "g": entry_g.get().strip(),
        "b": entry_b.get().strip(),
        "a": entry_a.get().strip() or "255"
    }

    for y in range(height):
        for x in range(width):
            local_dict = {"x": x, "y": y}
            try:
                r = int(eval(formulas["r"], {"__builtins__": None}, {**safe_dict, **local_dict})) % 256
                g = int(eval(formulas["g"], {"__builtins__": None}, {**safe_dict, **local_dict})) % 256
                b = int(eval(formulas["b"], {"__builtins__": None}, {**safe_dict, **local_dict})) % 256
                a = int(eval(formulas["a"], {"__builtins__": None}, {**safe_dict, **local_dict})) % 256
            except Exception as e:
                messagebox.showerror("Error", f"Error evaluating formulas: {e}")
                return

            img.putpixel((x, y), (r, g, b, a))

    img.save(filepath)
    messagebox.showinfo("Success", f"Image saved to {filepath}")

    # Update preview
    preview_img = ImageTk.PhotoImage(img.resize((256, 256)))
    label_preview.config(image=preview_img, text="")  # Remove placeholder text

if __name__ == "__main__":
    os.makedirs("img", exist_ok=True)
    root = tk.Tk()
    root.title("")

    # Output filename
    tk.Label(root, text="Output File Name:").pack(pady=2)
    entry_filename = tk.Entry(root, width=30)
    entry_filename.pack(pady=2)

    # R formula
    tk.Label(root, text="Red (R) formula:").pack(pady=2)
    entry_r = tk.Entry(root, width=30)
    entry_r.pack(pady=2)
    entry_r.insert(0, "(sin(x/20)+1)*127")  # default example

    # G formula
    tk.Label(root, text="Green (G) formula:").pack(pady=2)
    entry_g = tk.Entry(root, width=30)
    entry_g.pack(pady=2)
    entry_g.insert(0, "(cos(y/20)+1)*127")

    # B formula
    tk.Label(root, text="Blue (B) formula:").pack(pady=2)
    entry_b = tk.Entry(root, width=30)
    entry_b.pack(pady=2)
    entry_b.insert(0, "(sin((x+y)/30)+1)*127")

    # A formula
    tk.Label(root, text="Alpha (A) formula (optional, default 255):").pack(pady=2)
    entry_a = tk.Entry(root, width=30)
    entry_a.pack(pady=2)

    btn = tk.Button(root, text="generate image", command=generate_image)
    btn.pack(pady=10)

    # Preview area
    label_preview = tk.Label(root, text="No image generated yet", width=32, height=16, relief="solid")
    label_preview.pack(pady=10)

    root.mainloop()
