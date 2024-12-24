import tkinter as tk
from tkinter import messagebox
from threading import Thread, Event
from time import sleep
import pygetwindow as gw
import pystray
from PIL import Image, ImageDraw


class ReminderApp:
    """
    A class to represent the Eye Reminder application.
        made by Vikas GAC APAC FI
    Attributes
    ----------
    root : tk.Tk
        The root window of the Tkinter application.
    stop_event : threading.Event
        An event to signal stopping the reminder.
    reminder_running : bool
        A flag to indicate if the reminder is running.
    timer_label : tk.Label
        A label to display the timer status.
    long_break_label : tk.Label
        A label for the long break input.
    long_break_entry : tk.Entry
        An entry widget for the long break duration.
    short_break_label : tk.Label
        A label for the short break input.
    short_break_entry : tk.Entry
        An entry widget for the short break duration.
    start_button : tk.Button
        A button to start the reminder.
    stop_button : tk.Button
        A button to stop the reminder.
    minimize_button : tk.Button
        A button to minimize the application to the system tray.
    exit_button : tk.Button
        A button to close the application.
    tray_icon : pystray.Icon
        The system tray icon for the application.

    Methods
    -------
    start_reminder():
        Starts the reminder timer.
    stop_reminder():
        Stops the reminder timer.
    remind():
        Runs the reminder loop.
    run_timer(seconds, message):
        Runs a countdown timer.
    check_if_teams_running():
        Checks if Microsoft Teams is running.
    minimize_window():
        Minimizes the application to the system tray.
    restore_window():
        Restores the application window from the system tray.
    create_tray_icon():
        Creates a system tray icon.
    """

    def __init__(self, root):
        """
        Constructs all the necessary attributes for the ReminderApp object.

        Parameters
        ----------
        root : tk.Tk
            The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Eye Reminder")
        self.root.geometry("420x280")
        self.root.configure(bg="#f0f8ff")

        self.timer_label = tk.Label(root, text="Please start timer", font=("Helvetica", 14), bg="#f0f8ff", fg="#333")
        self.timer_label.pack(pady=10)

        self.stop_event = Event()
        self.reminder_running = False

        self.long_break_label = tk.Label(root, text="Long break (Min.):", font=("Helvetica", 12), bg="#f0f8ff",
                                         fg="#333")
        self.long_break_label.pack()
        self.long_break_entry = tk.Entry(root, font=("Helvetica", 12), bg="#e6f7ff", fg="#333")
        self.long_break_entry.insert(0, "20")
        self.long_break_entry.pack()

        self.short_break_label = tk.Label(root, text="Short break (Sec.):", font=("Helvetica", 12), bg="#f0f8ff",
                                          fg="#333")
        self.short_break_label.pack()
        self.short_break_entry = tk.Entry(root, font=("Helvetica", 12), bg="#e6f7ff", fg="#333")
        self.short_break_entry.insert(0, "20")
        self.short_break_entry.pack(pady=10)

        button_frame1 = tk.Frame(root, bg="#f0f8ff")
        button_frame1.pack(pady=10)

        self.start_button = tk.Button(button_frame1, text="Start", command=self.start_reminder, bg="#32cd32",
                                      fg="#fff",
                                      font=("Helvetica", 14), width=16, height=1)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(button_frame1, text="Stop", command=self.stop_reminder, bg="#87cefa",
                                     fg="#000",
                                     font=("Helvetica", 14), width=16, height=1)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        button_frame2 = tk.Frame(root, bg="#f0f8ff")
        button_frame2.pack(pady=10)

        self.minimize_button = tk.Button(button_frame2, text="Minimize", command=self.minimize_window,
                                         bg="#ffd700", fg="#000",
                                         font=("Helvetica", 14), width=16, height=1)
        self.minimize_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = tk.Button(button_frame2, text="Close", command=self.root.quit, bg="#ff4500",
                                     fg="#fff",
                                     font=("Helvetica", 14), width=16, height=1)
        self.exit_button.pack(side=tk.LEFT, padx=5)

    def start_reminder(self):
        """
        Starts the reminder timer by reading the long and short break durations.
        """
        long_break = self.long_break_entry.get()
        short_break = self.short_break_entry.get()

        if not long_break or not short_break:
            messagebox.showerror("Input Error", "Both long break and short break values must be entered.")
            return

        try:
            long_break = int(long_break)
            short_break = int(short_break)
        except ValueError:
            messagebox.showerror("Input Error", "Both long break and short break values must be numerical.")
            return

        if not self.reminder_running:
            self.reminder_running = True
            self.stop_event.clear()
            Thread(target=self.remind, daemon=True).start()
        else:
            messagebox.showwarning("Warning", "A reminder is already running!")

    def stop_reminder(self):
        """
        Stops the reminder timer.
        """
        if self.reminder_running:
            self.stop_event.set()
            self.reminder_running = False
        else:
            messagebox.showwarning("Warning", "No active reminder to stop!")

    def remind(self):
        """
        Runs the reminder loop, alternating between long and short breaks.
        """
        while not self.stop_event.is_set():
            long_break = int(self.long_break_entry.get()) * 60
            self.run_timer(long_break, "Time to break: {} min {} sec")
            if self.stop_event.is_set():
                break
            if not self.check_if_teams_running():
                messagebox.showinfo("Reminder", "Take a break!")
            short_break = int(self.short_break_entry.get())
            self.run_timer(short_break, "Break time left: {} sec")
            if self.stop_event.is_set():
                break
            if not self.check_if_teams_running():
                messagebox.showinfo("Reminder", "Break over! Back to work!")

    def run_timer(self, seconds, message):
        """
        Runs a countdown timer and updates the timer label.

        Parameters
        ----------
        seconds : int
            The duration of the timer in seconds.
        message : str
            The message format to display on the timer label.
        """
        for remaining in range(seconds, 0, -1):
            if self.stop_event.is_set():
                self.timer_label.config(text="Reminder stopped.")
                break
            if "Break" in message:
                self.timer_label.config(text=message.format(remaining))
            else:
                minutes, secs = divmod(remaining, 60)
                self.timer_label.config(text=message.format(minutes, secs))
            sleep(1)
        else:
            self.timer_label.config(text=message.format(0, 0))

    def check_if_teams_running(self):
        """
        Checks if Microsoft Teams is running.

        Returns
        -------
        bool
            True if Microsoft Teams is running, False otherwise.
        """
        for window in gw.getAllWindows():
            if window.title.count("|") == 1 and window.title.endswith("| Microsoft Teams") and window.title not in [
                "Calendar | Microsoft Teams", "People | Microsoft Teams"]:
                return True
        return False

    def minimize_window(self):
        """
        Minimizes the application to the system tray.
        """
        self.root.withdraw()  # Hide the main window
        self.create_tray_icon()  # Create system tray icon

    def restore_window(self):
        """
        Restores the application window from the system tray.
        """
        self.root.deiconify()  # Restore the window
        self.root.lift()  # Bring the window to the front
        if self.tray_icon:
            self.tray_icon.stop()  # Stop and remove the tray icon when window is restored

    def create_tray_icon(self):
        """
        Creates a system tray icon for the application.
        """

        def on_restore(icon, item):
            icon.stop()
            self.restore_window()  # Restore window when clicking the tray icon

        # Create an icon image
        image = Image.new("RGB", (64, 64), "grey")
        draw = ImageDraw.Draw(image)
        # Draw a clock shape
        draw.ellipse([8, 8, 56, 56], outline="black", fill="white")  # Clock face
        draw.line([32, 32, 32, 16], fill="black", width=2)  # Hour hand
        draw.line([32, 32, 48, 32], fill="black", width=2)  # Minute hand

        # Create a system tray icon
        self.tray_icon = pystray.Icon("Reminder App", image, "Reminder App", menu=pystray.Menu(
            pystray.MenuItem("Restore", on_restore)
        ))
        Thread(target=self.tray_icon.run, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()
