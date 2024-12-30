import tkinter as tk

from mainwindow import initialize_gui, show_congratulations

window: tk.Tk = initialize_gui()

show_congratulations(window, lambda: None)  # lambda: None as a placeholder to a restart function.

# Run the Tkinter event loop
# ==========================
window.mainloop()
window.destroy()  # Close the window after the event loop ends (on window.quit())
