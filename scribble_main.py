#!/usr/bin/env python3
"""
Scribble Ransomware Simulation
Educational Project for Cybersecurity Course

WARNING: This is for educational purposes only. Using this code for malicious
purposes is illegal and unethical.
"""

import os
import sys
import argparse
from scribble_core import ScribbleRansomware, create_test_files
from scribble_gui import ScribbleGUI
import tkinter as tk

def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description="Scribble Ransomware Simulation (Educational Purposes Only)")
    
    parser.add_argument(
        "--mode",
        choices=["encrypt", "decrypt", "gui", "create-test"],
        default="gui",
        help="Operation mode: encrypt, decrypt, gui, or create-test"
    )
    
    parser.add_argument(
        "--test-dir",
        default=os.path.join(os.getcwd(), "test_files"),
        help="Directory for test files (default: ./test_files)"
    )
    
    parser.add_argument(
        "--num-files",
        type=int,
        default=10,
        help="Number of test files to create (default: 10)"
    )
    
    parser.add_argument(
        "--timeout",
        type=int,
        default=3600,
        help="Countdown timeout in seconds (default: 3600 = 1 hour)"
    )
    
    parser.add_argument(
        "--safe",
        action="store_true",
        default=True,
        help="Safe mode - only operate in test directory (default: True)"
    )
    
    return parser.parse_args()

def main():
    """Main entry point for the program"""
    args = parse_arguments()
    
    # Always run in test mode for safety
    test_mode = args.safe
    
    if args.mode == "create-test":
        # Create test files
        num_created = create_test_files(args.test_dir, args.num_files)
        print(f"Created {num_created} test files in {args.test_dir}")
        return
    
    # Initialize the ransomware
    ransomware = ScribbleRansomware(test_mode=test_mode, target_directory=args.test_dir)
    ransomware.countdown_time = args.timeout
    
    # Check if a previous session exists
    previous_session = ransomware.load_metadata()
    if previous_session:
        print("Found previous session metadata")
    
    if args.mode == "encrypt":
        # Encrypt files
        print(f"Searching for files in {args.test_dir if test_mode else 'user directory'}")
        num_encrypted = ransomware.start_encryption()
        print(f"Encrypted {num_encrypted} files")
        print(f"Deadline: {ransomware.deadline}")
    
    elif args.mode == "decrypt":
        # Decrypt files
        if not previous_session:
            print("No previous session found. Cannot decrypt.")
            return
        
        num_decrypted = ransomware.start_decryption()
        print(f"Decrypted {num_decrypted} files")
    
    elif args.mode == "gui":
        # Start the GUI
        root = tk.Tk()
        app = ScribbleGUI(root, ransomware)
        root.mainloop()

if _name_ == "_main_":
    # Display warning
    print("""
    WARNING: This is a ransomware simulation for educational purposes only.
    Using this code for malicious purposes is illegal and unethical.
    This simulation will only operate in a test directory by default.
    """)
    
    main()