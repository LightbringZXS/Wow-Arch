import subprocess
import time

print("Welcome to Wow-Arch! 🎉\n")
print("⚠️ This script requires root privileges for some commands.")
print("🛑 Do NOT run this script as root for your safety.")
print("🔑 You will be prompted for your password when necessary.")
print("✅ The script does NOT store or see your password.")
print("❌ If you don't have root access, some commands may fail.")
print("\nℹ️ Note: This program uses emojis for better readability.")
print("If your system doesn't support emojis, you may see odd symbols.\n")

def explain_step(message):
    print(f"\n🔍 {message}")
    time.sleep(1.5)  # Pause for readability

def run_command(command, description):
    explain_step(description)
    while True:
        try:
            subprocess.run(command, shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Failed to run: {command}")
            retry = input("Would you like to try again? (y/n): ").lower()
            if retry != 'y':
                return False

def update_system():
    explain_step("Welcome to the system update tool! This will walk you through updating your system.")
    print ("Press enter to start")
    input()

    run_command("sudo pacman -Sy", "Step 1: Syncing package databases with the official repositories (pacman -Sy)")
    print ("Done! Press enter to continue")
    input()

    run_command("sudo pacman -Su", "Step 2: Upgrading all installed packages to their latest versions (pacman -Su)")
    print ("Done! Press enter to continue")
    input()

    explain_step("✅ System update complete!")
    main()

def about_section():
    try:
        with open('help.txt', 'r') as help_file:
            print(help_file.read())
    except FileNotFoundError:
        print("❌ help.txt file not found! Please ensure it's in the script directory.")
    input("Press enter to continue")
    main()

def clear_terminal():
    explain_step("To do this yourself type 'clear' outside of Wow-Arch")
    input("Press enter to continue")
    run_command("clear", "Clearing the terminal... 🫰")
    main()

def main():
    print ("1. Update System")
    print ("2. About")
    print ("3. Clear Terminal")
    print ("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        update_system()
    elif choice == "2":
        about_section()
    elif choice == "3":
        clear_terminal()
    elif choice == "4":
        print("Goodbye!")
        exit()
    else:
        print("Invalid choice. Please try again.")

main()