# password_generator.py - Complete Password Generator Application
# CODSOFT Python Programming Internship - Task 3

import random
import string
import json
import os
from datetime import datetime

# File to store generated passwords - FIXED FILENAME
PASSWORDS_FILE = "saved_passwords.json"  # Changed from passwords.json
generated_passwords = []

# ========== FILE HANDLING ==========

def load_passwords():
    """Load saved passwords from file"""
    global generated_passwords
    
    if os.path.exists(PASSWORDS_FILE):
        try:
            with open(PASSWORDS_FILE, 'r') as file:
                generated_passwords = json.load(file)
                print(f"Loaded {len(generated_passwords)} saved passwords")
        except:
            print(" Error loading passwords. Starting fresh.")
            generated_passwords = []
    else:
        print(" No saved passwords found. Creating new file...")
        generated_passwords = []
        # Create empty JSON file
        with open(PASSWORDS_FILE, 'w') as file:
            json.dump([], file)
        print(" Created saved_passwords.json file")

def save_passwords():
    """Save passwords to file"""
    try:
        with open(PASSWORDS_FILE, 'w') as file:
            json.dump(generated_passwords, file, indent=4)
        print(" Passwords saved successfully!")
    except:
        print(" Error saving passwords!")

# ========== PASSWORD GENERATION ==========

def generate_password(length, use_uppercase=True, use_lowercase=True, 
                      use_digits=True, use_special=True, exclude_ambiguous=False):
    """Generate a random password based on user preferences"""
    
    # Build character pool
    characters = ""
    
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Remove ambiguous characters if requested
    if exclude_ambiguous:
        ambiguous = "lI1O0"
        characters = ''.join(c for c in characters if c not in ambiguous)
    
    if not characters:
        raise ValueError(" At least one character type must be selected!")
    
    if length < 1:
        raise ValueError(" Password length must be at least 1!")
    
    # Generate password
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_multiple_passwords(count, length, use_uppercase=True, use_lowercase=True,
                                use_digits=True, use_special=True, exclude_ambiguous=False):
    """Generate multiple passwords at once"""
    passwords = []
    for _ in range(count):
        try:
            pwd = generate_password(length, use_uppercase, use_lowercase,
                                    use_digits, use_special, exclude_ambiguous)
            passwords.append(pwd)
        except ValueError as e:
            print(f"Error: {e}")
            return []
    return passwords

def check_password_strength(password):
    """Check password strength and return score"""
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 12:
        score += 2
        feedback.append(" Good length (12+ characters)")
    elif len(password) >= 8:
        score += 1
        feedback.append(" Decent length (8-11 characters)")
    else:
        feedback.append(" Too short (less than 8 characters)")
    
    # Character variety checks
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append(" Missing lowercase letters")
    
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append(" Missing uppercase letters")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append(" Missing numbers")
    
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1
    else:
        feedback.append(" Missing special characters")
    
    # Check for patterns
    common_patterns = ["password", "123456", "qwerty", "admin", "letmein"]
    if any(pattern in password.lower() for pattern in common_patterns):
        score -= 1
        feedback.append(" Contains common password pattern")
    
    # Determine strength
    if score >= 6:
        strength = " STRONG"
    elif score >= 4:
        strength = " MEDIUM"
    else:
        strength = " WEAK"
    
    return strength, score, feedback

# ========== USER INTERFACE ==========

def generate_single_password():
    """Generate a single password with user options"""
    print("\n" + "="*50)
    print("🔑 GENERATE PASSWORD")
    print("="*50)
    
    try:
        length = int(input(" Enter password length (8-50 recommended): "))
        if length < 1:
            print(" Length must be at least 1!")
            return
        
        print("\n Character options:")
        use_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
        use_lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'
        use_digits = input("Include numbers? (y/n): ").lower() == 'y'
        use_special = input("Include special characters? (y/n): ").lower() == 'y'
        exclude_ambiguous = input("Exclude ambiguous characters (l, I, 1, O, 0)? (y/n): ").lower() == 'y'
        
        password = generate_password(length, use_uppercase, use_lowercase,
                                     use_digits, use_special, exclude_ambiguous)
        
        print("\n" + "="*50)
        print("GENERATED PASSWORD")
        print("="*50)
        print(f" Password: {password}")
        
        # Check strength
        strength, score, feedback = check_password_strength(password)
        print(f"\n Strength: {strength} (Score: {score}/6)")
        print("\n Analysis:")
        for item in feedback:
            print(f"  {item}")
        print("="*50)
        
        # Option to save
        save = input("\n Save this password? (y/n): ").lower() == 'y'
        if save:
            save_to_history(password, f"Custom {length} chars")
        
    except ValueError as e:
        print(f" Invalid input: {e}")
    except Exception as e:
        print(f" Error: {e}")

def generate_bulk_passwords():
    """Generate multiple passwords at once"""
    print("\n" + "="*50)
    print(" BULK PASSWORD GENERATOR")
    print("="*50)
    
    try:
        count = int(input(" How many passwords to generate? (1-20): "))
        if count < 1 or count > 20:
            print(" Please enter between 1 and 20!")
            return
        
        length = int(input(" Password length (8-50 recommended): "))
        if length < 1:
            print(" Length must be at least 1!")
            return
        
        print("\n Character options:")
        use_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
        use_lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'
        use_digits = input("Include numbers? (y/n): ").lower() == 'y'
        use_special = input("Include special characters? (y/n): ").lower() == 'y'
        
        passwords = generate_multiple_passwords(count, length, use_uppercase, use_lowercase,
                                                use_digits, use_special)
        
        if passwords:
            print("\n" + "="*50)
            print(" GENERATED PASSWORDS")
            print("="*50)
            for i, pwd in enumerate(passwords, 1):
                strength, score, _ = check_password_strength(pwd)
                print(f"{i:2}. {pwd}  [{strength}]")
            print("="*50)
            
            # Option to save all
            save = input("\n Save all passwords? (y/n): ").lower() == 'y'
            if save:
                for pwd in passwords:
                    save_to_history(pwd, f"Bulk {length} chars")
        
    except ValueError as e:
        print(f" Invalid input: {e}")
    except Exception as e:
        print(f" Error: {e}")

def save_to_history(password, description):
    """Save generated password to history"""
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "password": password,
        "description": description
    }
    generated_passwords.append(entry)
    save_passwords()
    print(" Password saved to history!")

def view_history():
    """View saved passwords history"""
    if not generated_passwords:
        print("\n📭 No passwords saved yet!")
        return
    
    print("\n" + "="*70)
    print(" GENERATED PASSWORDS HISTORY")
    print("="*70)
    
    for i, entry in enumerate(generated_passwords, 1):
        print(f"{i:2}. {entry['timestamp']}")
        print(f"   Password: {entry['password']}")
        print(f"   {entry['description']}")
        print("-"*60)

def clear_history():
    """Clear password history"""
    global generated_passwords
    
    if not generated_passwords:
        print(" History is already empty!")
        return
    
    confirm = input(" Are you sure you want to clear ALL saved passwords? (y/n): ")
    if confirm.lower() == 'y':
        generated_passwords = []
        save_passwords()
        print(" Password history cleared!")
    else:
        print("❌ Operation cancelled.")

def show_statistics():
    """Show password generation statistics"""
    if not generated_passwords:
        print("📭 No passwords generated yet!")
        return
    
    print("\n" + "="*40)
    print(" PASSWORD STATISTICS")
    print("="*40)
    print(f" Total passwords generated: {len(generated_passwords)}")
    
    # Average length
    avg_length = sum(len(entry['password']) for entry in generated_passwords) / len(generated_passwords)
    print(f" Average password length: {avg_length:.1f} characters")
    
    # Most recent password
    latest = generated_passwords[-1]
    print(f" Latest: {latest['timestamp']}")
    print(f"   Password: {latest['password']}")
    print("="*40)

def show_quick_generate():
    """Quickly generate a strong 16-character password"""
    print("\n" + "="*50)
    print(" QUICK GENERATE - Strong Password")
    print("="*50)
    
    try:
        length = 16
        password = generate_password(length, True, True, True, True, False)
        print(f" Generated Password: {password}")
        
        # Check strength
        strength, score, _ = check_password_strength(password)
        print(f" Strength: {strength} (Score: {score}/6)")
        
        save = input("\n Save this password? (y/n): ").lower() == 'y'
        if save:
            save_to_history(password, f"Quick 16 chars")
    except Exception as e:
        print(f" Error: {e}")

# ========== MAIN MENU ==========

def main():
    """Main program loop"""
    load_passwords()
    
    while True:
        print("\n" + "="*50)
        print(" PASSWORD GENERATOR APPLICATION")
        print("="*50)
        print("1.  Quick Generate (Strong Password)")
        print("2.  Custom Password Generator")
        print("3.  Bulk Passwords Generator")
        print("4.  View History")
        print("5.  View Statistics")
        print("6.  Clear History")
        print("7.  Exit")
        print("="*50)
        
        choice = input("Choose option (1-7): ")
        
        if choice == '1':
            show_quick_generate()
        elif choice == '2':
            generate_single_password()
        elif choice == '3':
            generate_bulk_passwords()
        elif choice == '4':
            view_history()
        elif choice == '5':
            show_statistics()
        elif choice == '6':
            clear_history()
        elif choice == '7':
            save_passwords()
            print("\n Goodbye! Thanks for using Password Generator!")
            break
        else:
            print(" Invalid option! Please choose 1-7.")

if __name__ == "__main__":
    main()