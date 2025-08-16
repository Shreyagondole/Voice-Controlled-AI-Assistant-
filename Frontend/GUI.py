import os
import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

assistant_status = "Available…"
microphone_status = "True"

# Show hello message as soon as GUI starts
HELLO_USERNAME = os.environ.get("Username", "shreya")
HELLO_MESSAGE = f"Hello {HELLO_USERNAME}, How are you?"

# Helper for temp directory path
def TempDirectoryPath(filename):
    temp_dir = os.path.join(os.getcwd(), "Frontend", "Files")
    os.makedirs(temp_dir, exist_ok=True)
    return os.path.join(temp_dir, filename)

def AnswerModifier(text):
    return text

def QueryModifier(text):
    return text

def SetAssistantStatus(status):
    global assistant_status
    assistant_status = status
    if WhatsAppGUI.gui_instance:
        WhatsAppGUI.gui_instance.status_label.configure(text=f"Status: {status}")

def SetMicrophoneStatus(status):
    global microphone_status
    microphone_status = status
    if WhatsAppGUI.gui_instance:
        WhatsAppGUI.gui_instance.mic_label.configure(text=f"Mic: {status}")

def GetMicrophoneStatus():
    return microphone_status

def GetAssistantStatus():
    return assistant_status

def ShowTextToScreen(text, sender="assistant"):
    pass  # No chat bubbles

class WhatsAppGUI(ctk.CTk):
    gui_instance = None
    def __init__(self):
        super().__init__()
        WhatsAppGUI.gui_instance = self
        self.title("Jarvis Assistant")
        self.geometry("500x700")
        self.resizable(False, False)
        self.configure(bg="#111b21")
        # Header
        self.header = ctk.CTkFrame(self, fg_color="#202c33", height=60)
        self.header.pack(fill="x", side="top")
        self.title_label = ctk.CTkLabel(self.header, text="Jarvis Assistant", font=("Segoe UI", 20, "bold"), fg_color="#202c33")
        self.title_label.pack(side="left", padx=10)
        self.status_label = ctk.CTkLabel(self.header, text=f"Status: {assistant_status}", font=("Segoe UI", 12), fg_color="#202c33")
        self.status_label.pack(side="right", padx=10)
        self.mic_label = ctk.CTkLabel(self.header, text=f"Mic: {microphone_status}", font=("Segoe UI", 12), fg_color="#202c33")
        self.mic_label.pack(side="right", padx=5)
        # Animated avatar area
        avatar_gif_path = TempDirectoryPath("avatar.gif")
        self.avatar_panel = ctk.CTkLabel(self, text="")
        self.avatar_panel.pack(pady=(60, 50))
        if os.path.exists(avatar_gif_path):
            self.avatar_frames = [ImageTk.PhotoImage(frame.copy().resize((450, 450)))  # Increased size here
                                  for frame in ImageSequence.Iterator(Image.open(avatar_gif_path))]
            self.avatar_frame_index = 0
            self.animate_avatar()
        else:
            self.avatar_panel.configure(text="🤖", font=("Segoe UI", 200))  # Increased emoji size

        # Frame for buttons (optional, for layout)
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(side="bottom", pady=40)  # Increased bottom padding

        # Start Recognition Button
        self.start_button = ctk.CTkButton(
            self.button_frame,
            text="Start Recognition",
            command=self.start_recognition,
            width=220,    # Increase width
            height=48,    # Increase height
            font=("Segoe UI", 16, "bold")  # Optional: larger font
        )
        self.start_button.pack(side="top", fill="x", pady=(0, 10))  # Top button, 10px gap below

        # Stop Recognition Button
        self.stop_button = ctk.CTkButton(
            self.button_frame,
            text="Stop Recognition",
            command=self.stop_recognition,
            width=220,
            height=48,
            font=("Segoe UI", 16, "bold")
        )
        self.stop_button.pack(side="top", fill="x")  # Stacked below the start button

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        # Set window icon
        self.icon_path = os.path.join(os.path.dirname(__file__), '..', 'jarvis.ico')
        try:
            self.iconbitmap(self.icon_path)
        except Exception:
            pass

    def animate_avatar(self):
        if hasattr(self, 'avatar_frames') and self.avatar_frames:
            frame = self.avatar_frames[self.avatar_frame_index]
            self.avatar_panel.configure(image=frame)
            self.avatar_frame_index = (self.avatar_frame_index + 1) % len(self.avatar_frames)
            self.after(80, self.animate_avatar)

    def on_close(self):
        self.destroy()
        os._exit(0)

    def start_recognition(self):
        self.status_label.configure(text="Status: Recognition started")
        print("Recognition started")

    def stop_recognition(self):
        self.status_label.configure(text="Status: Recognition stopped")
        print("Recognition stopped")

def GraphicalUserInterface():
    app = WhatsAppGUI()
    app.mainloop()
