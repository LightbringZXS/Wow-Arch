import subprocess
import sys
import time
import os


def press_enter(message: str) -> None:
    input(message)


def explain_step(message: str) -> None:
    print(f"\n🔍 {message}")
    time.sleep(1.5)  # Pause for readability


def run_command(command: str, description: str) -> bool:
    explain_step(description)
    while True:
        try:
            subprocess.run(command, shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Failed to run: {command}")
            retry = input("Would you like to try again? (y/n): ").lower()
            if retry != "y":
                return False


class HomeSreen:
    @staticmethod
    def print_options() -> None:
        print("1. Update System")
        print("2. About")
        print("3. Clear Terminal")
        print("4. install packages")
        print("5. Exit")

    @staticmethod
    def get_user_choice() -> None:
        while True:
            try:
                choice = int(input("Enter your choice: "))
            except (KeyboardInterrupt, EOFError):
                choice = 5  # exit program
            except ValueError:
                continue
            match choice:
                case 0:
                    HomeSreen.print_options()
                case 1:
                    update_system()
                case 2:
                    about_section()
                case 3:
                    clear_terminal()
                case 4:
                    install_packages()
                case 5:
                    print("\nGoodbye!")
                    sys.exit(0)


def main() -> None:
    print("Welcome to Wow-Arch! 🎉\n")
    print("⚠️ This script requires root privileges for some commands.")
    print("🛑 Do NOT run this script as root for your safety.")
    print("🔑 You will be prompted for your password when necessary.")
    print("✅ The script does NOT store or see your password.")
    print("❌ If you don't have root access, some commands may fail.")
    print("\nℹ️ Note: This program uses emojis for better readability.")
    print("If your system doesn't support emojis, you may see odd symbols.\n")

    HomeSreen.print_options()
    HomeSreen.get_user_choice()

def install_packages() -> None:
    try:
        subprocess.run(
            ["yay", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        subprocess.run(["python", "-m", "wowarch.installhelper"], check=True)
    except FileNotFoundError:
        print("Yay is not installed. Some packages may not be available.")
        print("Would you like to install Yay? (y/n): ")
        response = input().lower()
        if response == "y":
            print("Installing Yay...")
            time.sleep(1.5)
            run_command(
                "sudo pacman -S --needed git base-devel",
                "Installing dependencies for Yay... (pacman -S --needed git base-devel)",
            )
            run_command(
                "cd ~ && git clone https://aur.archlinux.org/yay.git",
                "Cloning Yay from the AUR... (git clone https://aur.archlinux.org/yay.git)",
            )
            print("Navigating to the Yay directory... (cd yay)")
            run_command(
                "cd ~/yay && makepkg -si",
                "Building and installing Yay... (makepkg -si)",
            )
            print("Yay installed successfully! 🎉")
            print("The clone of thye Yay repository is no longer needed.")
            print("Would you like to remove the Yay directory? (y/n): ")
            response = input().lower()
            if response == "y":
                os.system("rm -rf ~/yay")
                print("Yay directory removed successfully! 🎉")
            elif response == "n":
                print("Yay directory will not be removed.")
            else:
                print("Invalid input! Please try again.")
                return
        elif response == "n":
            print("Yay will not be installed.")
            return
        else:
            print("Invalid input! Please try again.")
            return

def update_system() -> None:
    explain_step(
        "Welcome to the system update tool! This will walk you through updating your system."
    )
    press_enter("Press enter to start")

    run_command(
        "sudo pacman -Sy",
        "Step 1: Syncing package databases with the official repositories (pacman -Sy)",
    )
    press_enter("Done! Press enter to continue")

    run_command(
        "sudo pacman -Su",
        "Step 2: Upgrading all installed packages to their latest versions (pacman -Su)",
    )
    press_enter("Done! Press enter to continue")

    explain_step("✅ System update complete!")


def about_section() -> None:
    try:
        with open("help.txt", "r") as help_file:
            print(help_file.read())
    except FileNotFoundError:
        print("❌ help.txt file not found! Please ensure it's in the script directory.")
    press_enter("Press enter to continue")


def clear_terminal() -> None:
    explain_step("To do this yourself type 'clear' outside of Wow-Arch")
    press_enter("Press enter to continue")
    run_command("clear", "Clearing the terminal... 🫰")


if __name__ == "__main__":
    main()
