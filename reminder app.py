import tkinter as tk
from tkinter import messagebox
from threading import Thread, Event
from time import sleep
import pystray
from PIL import Image, ImageDraw

# Flag and event to track and control reminders
reminder_running = False
stop_event = Event()

def format_time(seconds):
    """Format seconds into 'X hr Y min Z sec'."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours} hr {minutes} min {secs} sec"

def remind(seconds):
    global reminder_running
    reminder_running = True
    stop_event.clear()
    try:
        for remaining in range(seconds, 0, -1):
            if stop_event.is_set():
                timer_label.config(text="Reminder stopped.")
                break
            formatted_time = format_time(remaining)
            timer_label.config(text=f"Time left: {formatted_time}")
            sleep(1)
        else:  # This runs only if the loop wasn't interrupted
            timer_label.config(text="Time left: 0 hr 0 min 0 sec")
            messagebox.showinfo("Reminder", f"Reminder after {format_time(seconds)}!")
    finally:
        reminder_running = False

def set_reminder(seconds):
    global reminder_running
    if reminder_running:
        messagebox.showwarning("Warning", "A reminder is already running!")
    else:
        Thread(target=remind, args=(seconds,), daemon=True).start()

def stop_reminder():
    global reminder_running
    if reminder_running:
        stop_event.set()
        reminder_running = False
    else:
        messagebox.showwarning("Warning", "No active reminder to stop!")

def minimize_window():
    root.withdraw()
    create_tray_icon()

def set_and_minimize():
    """Set a 20-minute reminder and minimize the window."""
    set_reminder(20 * 60)
    minimize_window()

def create_tray_icon():
    def on_restore(icon, item):
        icon.stop()
        root.deiconify()

    # Create an icon image
    image = Image.new("RGB", (64, 64), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle([16, 16, 48, 48], fill="blue")

    # Create a system tray icon
    tray_icon = pystray.Icon("Reminder App", image, "Reminder App", menu=pystray.Menu(
        pystray.MenuItem("Restore", on_restore)
    ))
    Thread(target=tray_icon.run, daemon=True).start()

def exit_app():
    root.quit()

# Root window setup
root = tk.Tk()
root.title("Reminder App")
root.geometry("400x400")
root.configure(bg="#f0f8ff")  # Light blue background

# Timer Label
timer_label = tk.Label(root, text="Time left: 0 hr 0 min 0 sec", font=("Helvetica", 14), bg="#f0f8ff", fg="#333")
timer_label.pack(pady=10)

# Buttons Layout
frame0 = tk.Frame(root, bg="#f0f8ff")
frame0.pack(pady=10)

btn_20min_continue = tk.Button(frame0, text="Continue - 20 Min", command=set_and_minimize, bg="#ffdab9", fg="#000")
btn_20min_continue.pack()

frame1 = tk.Frame(root, bg="#f0f8ff")
frame1.pack(pady=10)

btn_20min = tk.Button(frame1, text="Remind after 20 min", command=lambda: set_reminder(20 * 60), bg="#add8e6", fg="#000")
btn_20min.pack(pady=5)

frame2 = tk.Frame(root, bg="#f0f8ff")
frame2.pack(pady=10)

btn_1hr = tk.Button(frame2, text="Remind after ~ 1 hr", command=lambda: set_reminder(60 * 72), bg="#90ee90", fg="#000")
btn_1hr.pack(side=tk.LEFT, padx=5)

btn_3hr = tk.Button(frame2, text="Remind after ~ 3 hr", command=lambda: set_reminder(60 * 190), bg="#ffcccb", fg="#000")
btn_3hr.pack(side=tk.LEFT, padx=5)

frame3 = tk.Frame(root, bg="#f0f8ff")
frame3.pack(pady=10)

btn_stop = tk.Button(frame3, text="Stop Reminder", command=stop_reminder, bg="#ffa07a", fg="#000")
btn_stop.pack()

frame4 = tk.Frame(root, bg="#f0f8ff")
frame4.pack(pady=10)

btn_minimize = tk.Button(frame4, text="Minimize", command=minimize_window, bg="#ffd700", fg="#000")
btn_minimize.pack(side=tk.LEFT, padx=5)

btn_exit = tk.Button(frame4, text="Exit", command=exit_app, bg="#87cefa", fg="#000")
btn_exit.pack(side=tk.LEFT, padx=5)

root.mainloop()
#"C:\Users\Vikas\AppData\Local\Programs\Python\Python313\pythonw.exe" "C:\Users\Vikas\PycharmProjects\test1\reminder app.py"


#vbs
#Set WshShell = CreateObject("WScript.Shell")
#WshShell.Run """C:\Users\Vikas\AppData\Local\Programs\Python\Python313\pythonw.exe"" ""C:\Users\Vikas\PycharmProjects\test1\reminder app.py""", 0
#Set WshShell = Nothing
