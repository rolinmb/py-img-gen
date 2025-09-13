import tkinter as tk
from tkinter import messagebox
from PIL import Image
import os
import math

def generate_image():
    filename = entry.get().strip()
    if not filename:
        messagebox.showerror("Error", "Please enter a file name")
        return

    # Ensure it has .png extension
    if not filename.lower().endswith(".png"):
        filename += ".png"

    filepath = os.path.join("img", filename)

    width, height = 256, 256
    img = Image.new("RGBA", (width, height))

    for y in range(height):
        for x in range(width):
            r = int((math.sin(x / 20) + 1) * 127)   # 0-254
            g = int((math.cos(y / 20) + 1) * 127)   # 0-254
            b = int((math.sin((x + y) / 30) + 1) * 127)  # 0-254
            a = 255  # Fully opaque
            img.putpixel((x, y), (r, g, b, a))

    img.save(filepath)
    messagebox.showinfo("Success", f"Image saved to {filepath}")

if __name__ == "__main__":
    os.makedirs("img", exist_ok=True)
    root = tk.Tk()
    root.title("py-img-gen")

    tk.Label(root, text="Output File Name:").pack(pady=5)
    entry = tk.Entry(root, width=30)
    entry.pack(pady=5)

    btn = tk.Button(root, text="generate image", command=generate_image)
    btn.pack(pady=10)

    root.mainloop()
