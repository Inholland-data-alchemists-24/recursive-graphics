"""
Main module integrating the application's components and running the main event loop.
"""
import tkinter as tk

from mainwindow import initialize_gui, show_welcome, show_congratulations

window: tk.Tk = initialize_gui()

show_welcome(window)

# Bind the event handler for the congratulatory message
window.bind("<<congratulations>>", lambda event: show_congratulations(window, lambda: None))
# Trigger the custom event after the trees match condition is met
# window.event_generate("<<congratulations>>")


# Ensure resources are cleaned up when the window is closed
# =========================================================
def on_closing():
    window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)

# Run the Tkinter event loop
# ==========================
window.mainloop()
