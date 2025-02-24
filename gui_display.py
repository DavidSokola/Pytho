# gui_display.py
import tkinter as tk
import threading
import time

# Import the global last_decoded from decode_thread
from decode_thread import last_decoded

REFRESH_MS = 500  # Update GUI every 0.5 seconds

class DecodedGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DMC Decoder")
        self.root.geometry("400x200+100+100")  # width x height + x_offset + y_offset

        # Big label for the last decoded text
        self.label = tk.Label(self.root, text="Waiting for codes...", font=("Arial", 16))
        self.label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Kick off the label refresh
        self.update_label()

    def update_label(self):
        """
        Periodically refreshes the label text with the global last_decoded value.
        """
        # last_decoded is from decode_thread.py (global variable)
        self.label.config(text=f"Last Decoded:\n{last_decoded}")
        # Schedule next update in REFRESH_MS milliseconds
        self.root.after(REFRESH_MS, self.update_label)

    def run(self):
        self.root.mainloop()

def main():
    gui = DecodedGUI()
    gui.run()

if __name__ == "__main__":
    main()
