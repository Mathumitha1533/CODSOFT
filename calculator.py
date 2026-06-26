# calculator.py - Complete Calculator Application
# CODSOFT Python Programming Internship - Task 2

import json
import os
from datetime import datetime
import math

# File to store calculation history
HISTORY_FILE = "history.json"
history = []

# ========== FILE HANDLING ==========

def load_history():
    """Load calculation history from file"""
    global history
    
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as file:
                history = json.load(file)
                print(f"Loaded {len(history)} calculations from history")
        except:
            print("Error loading history. Starting fresh.")
            history = []
    else:
        print(" No saved history found.")
        history = []

def save_history():
    """Save calculation history to file"""
    try:
        with open(HISTORY_FILE, 'w') as file:
            json.dump(history, file, indent=4)
        print(" History saved successfully!")
    except:
        print(" Error saving history!")

# ========== CORE CALCULATION FUNCTIONS ==========

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero is not allowed!")
    return a / b

def power(a, b):
    return a ** b

def modulus(a, b):
    if b == 0:
        raise ValueError("Modulus by zero is not allowed!")
    return a % b

def square_root(a):
    if a < 0:
        raise ValueError("Cannot calculate square root of negative number!")
    return math.sqrt(a)

def percentage(a, b):
    """Calculate what percentage a is of b"""
    if b == 0:
        raise ValueError("Cannot calculate percentage with zero!")
    return (a / b) * 100

# ========== OPERATION HANDLER ==========

def perform_calculation():
    """Main calculation function"""
    print("\n" + "="*50)
    print("CALCULATOR")
    print("="*50)
    
    # Show available operations
    print("\n Available Operations:")
    print("  1.  Addition (+)")
    print("  2.  Subtraction (-)")
    print("  3.   Multiplication (*)")
    print("  4.  Division (/)")
    print("  5.  Power (^)")
    print("  6.  Modulus (%)")
    print("  7.  Square Root")
    print("  8.  Percentage")
    
    try:
        choice = input("\n Choose operation (1-8): ")
        
        if choice == '7':  # Square root - only one number needed
            try:
                num = float(input(" Enter number: "))
                result = square_root(num)
                operation_symbol = "√"
                expression = f"√{num}"
                print(f"\n Result: {expression} = {result:.6f}")
                
                # Save to history
                save_to_history(expression, result)
                return
            except ValueError as e:
                print(f" Error: {e}")
                return
        
        # For operations requiring two numbers
        try:
            num1 = float(input(" Enter first number: "))
            num2 = float(input(" Enter second number: "))
        except ValueError:
            print(" Invalid input! Please enter numbers only.")
            return
        
        result = None
        operation_symbol = ""
        expression = ""
        
        if choice == '1':
            result = add(num1, num2)
            operation_symbol = "+"
            expression = f"{num1} {operation_symbol} {num2}"
        elif choice == '2':
            result = subtract(num1, num2)
            operation_symbol = "-"
            expression = f"{num1} {operation_symbol} {num2}"
        elif choice == '3':
            result = multiply(num1, num2)
            operation_symbol = "*"
            expression = f"{num1} {operation_symbol} {num2}"
        elif choice == '4':
            result = divide(num1, num2)
            operation_symbol = "/"
            expression = f"{num1} {operation_symbol} {num2}"
        elif choice == '5':
            result = power(num1, num2)
            operation_symbol = "^"
            expression = f"{num1} {operation_symbol} {num2}"
        elif choice == '6':
            result = modulus(num1, num2)
            operation_symbol = "%"
            expression = f"{num1} {operation_symbol} {num2}"
        elif choice == '8':
            result = percentage(num1, num2)
            operation_symbol = "% of"
            expression = f"{num1} is what % of {num2}"
        else:
            print(" Invalid choice! Please select 1-8.")
            return
        
        # Display result
        if result is not None:
            print(f"\n Result: {expression} = {result:.6f}")
            # Save to history
            save_to_history(expression, result)
        
    except ValueError as e:
        print(f" Error: {e}")
    except Exception as e:
        print(f" Unexpected error: {e}")

def save_to_history(expression, result):
    """Save calculation to history"""
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "expression": expression,
        "result": round(result, 6) if isinstance(result, float) else result
    }
    history.append(entry)
    save_history()
    print("Calculation saved to history!")

# ========== HISTORY FUNCTIONS ==========

def view_history():
    """View calculation history"""
    if not history:
        print("\n No calculations in history yet!")
        return
    
    print("\n" + "="*60)
    print("CALCULATION HISTORY")
    print("="*60)
    
    for i, entry in enumerate(history, 1):
        print(f"{i:2}. {entry['timestamp']}")
        print(f"   {entry['expression']} = {entry['result']}")
        print("-"*50)

def clear_history():
    """Clear calculation history"""
    global history
    if not history:
        print(" History is already empty!")
        return
    
    confirm = input(" Are you sure you want to clear ALL history? (y/n): ")
    if confirm.lower() == 'y':
        history = []
        save_history()
        print(" History cleared!")
    else:
        print(" Operation cancelled.")

# ========== ADDITIONAL FEATURES ==========

def advanced_calculator():
    """Advanced scientific calculations"""
    print("\n" + "="*50)
    print(" ADVANCED CALCULATOR")
    print("="*50)
    print("  1. Sine (sin)")
    print("  2. Cosine (cos)")
    print("  3. Tangent (tan)")
    print("  4. Logarithm (log)")
    print("  5. Natural Log (ln)")
    print("  6. Factorial")
    
    try:
        choice = input("\n Choose operation (1-6): ")
        
        if choice in ['1', '2', '3', '4', '5']:
            try:
                num = float(input(" Enter number: "))
            except ValueError:
                print(" Invalid input!")
                return
            
            if choice == '1':
                result = math.sin(math.radians(num))
                operation = f"sin({num}°)"
            elif choice == '2':
                result = math.cos(math.radians(num))
                operation = f"cos({num}°)"
            elif choice == '3':
                if num % 180 == 90:
                    print("Tangent is undefined at 90° + 180°n")
                    return
                result = math.tan(math.radians(num))
                operation = f"tan({num}°)"
            elif choice == '4':
                if num <= 0:
                    print(" Logarithm requires positive number!")
                    return
                result = math.log10(num)
                operation = f"log10({num})"
            elif choice == '5':
                if num <= 0:
                    print(" Natural log requires positive number!")
                    return
                result = math.log(num)
                operation = f"ln({num})"
            
            print(f"\n Result: {operation} = {result:.6f}")
            save_to_history(operation, result)
            
        elif choice == '6':
            try:
                num = int(input(" Enter integer (0-20): "))
                if num < 0 or num > 20:
                    print(" Please enter number between 0 and 20")
                    return
                result = math.factorial(num)
                print(f"\n Result: {num}! = {result}")
                save_to_history(f"{num}!", result)
            except ValueError:
                print(" Invalid input! Enter an integer.")
        else:
            print(" Invalid choice!")
            
    except Exception as e:
        print(f" Error: {e}")

def show_statistics():
    """Show calculator statistics"""
    if not history:
        print(" No calculations to analyze!")
        return
    
    total = len(history)
    print("\n" + "="*40)
    print(" CALCULATOR STATISTICS")
    print("="*40)
    print(f" Total calculations: {total}")
    
    # Count operation types
    operation_counts = {}
    for entry in history:
        expr = entry['expression']
        # Extract operation type
        if '+' in expr:
            op = 'Addition'
        elif '-' in expr:
            op = 'Subtraction'
        elif '*' in expr:
            op = 'Multiplication'
        elif '/' in expr:
            op = 'Division'
        elif '^' in expr:
            op = 'Power'
        elif '%' in expr:
            op = 'Modulus/Percentage'
        elif '√' in expr or 'sin' in expr or 'cos' in expr:
            op = 'Advanced'
        else:
            op = 'Other'
        
        operation_counts[op] = operation_counts.get(op, 0) + 1
    
    print("\nOperation breakdown:")
    for op, count in operation_counts.items():
        percentage = (count / total) * 100
        print(f"   {op}: {count} ({percentage:.1f}%)")
    
    print("="*40)

# ========== MAIN MENU ==========

def main():
    """Main program loop"""
    load_history()
    
    while True:
        print("\n" + "="*50)
        print(" CALCULATOR APPLICATION")
        print("="*50)
        print("1.  Basic Calculator")
        print("2.  Advanced Calculator")
        print("3.  View History")
        print("4.  View Statistics")
        print("5.  Clear History")
        print("6.  Exit")
        print("="*50)
        
        choice = input("Choose option (1-6): ")
        
        if choice == '1':
            perform_calculation()
        elif choice == '2':
            advanced_calculator()
        elif choice == '3':
            view_history()
        elif choice == '4':
            show_statistics()
        elif choice == '5':
            clear_history()
        elif choice == '6':
            save_history()
            print("\n Goodbye! Thanks for using Calculator!")
            break
        else:
            print(" Invalid option! Please choose 1-6.")

if __name__ == "__main__":
    main()