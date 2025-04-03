import curses
import os
import textwrap


package_sets = [
    {
        "name": "Essentials",
        "description": "Basic utilities for a smooth Arch Linux experience.",
        "packages": [
            {"name": "vim", "description": "Text editor", "command": "sudo pacman -S vim"},
            {"name": "htop", "description": "Interactive process viewer", "command": "sudo pacman -S htop"},
            {"name": "wget", "description": "Command-line file downloader", "command": "sudo pacman -S wget"},
        ],
    },
    {
        "name": "Browsers",
        "description": "Web browsers for various purposes.",
        "packages": [
            {"name": "firefox", "description": "A popular, open-source browser known for its speed, security, and customizability. Supports a wide range of extensions and has a strong focus on privacy.", "command": "sudo pacman -S firefox"},
            {"name": "chromium", "description": "The open-source foundation for Google Chrome, offering a fast, feature-rich browsing experience without proprietary components.", "command": "sudo pacman -S chromium"},
            {"name": "vivaldi", "description": "A highly customizable Chromium-based browser designed for power users with many advanced features that go beyond the basic web experience.", "command": "yay -S vivaldi"},
            {"name": "brave-bin", "description": "A privacy-focused browser that blocks ads and trackers by default, built on Chromium.", "command": "yay -S brave-bin"},
            {"name": "torbrowser-launcher", "description": "A launcher for Tor Browser, providing secure and anonymous browsing through the Tor network.", "command": "sudo pacman -S torbrowser-launcher"},
    ],
}

]

selected_packages = {}

def draw_menu(stdscr, options, title="Menu", selected_index=0):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    stdscr.addstr(1, width // 2 - len(title) // 2, title, curses.A_BOLD | curses.A_UNDERLINE)
    
    for index, option in enumerate(options):
        if index == selected_index:
            stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(3 + index, 2, option)
        if index == selected_index:
            stdscr.attroff(curses.A_REVERSE)
    
    stdscr.refresh()

def category_menu(stdscr):
    selected_index = 0
    
    while True:
        categories = [category["name"] for category in package_sets] + ["Proceed to Install", "Exit "]
        draw_menu(stdscr, categories, title="Select a Category", selected_index=selected_index)
        
        key = stdscr.getch()
        if key == curses.KEY_UP and selected_index > 0:
            selected_index -= 1
        elif key == curses.KEY_DOWN and selected_index < len(categories) - 1:
            selected_index += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            if selected_index == len(categories) - 1:
                return
            elif selected_index == len(categories) - 2:
                confirm_installation(stdscr)
            else:
                package_menu(stdscr, package_sets[selected_index])

def package_menu(stdscr, category):
    current_idx = 0
    package_list = category["packages"]
    
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        stdscr.addstr(1, w//2 - len(category["name"])//2, category["name"], curses.A_BOLD | curses.A_UNDERLINE)
        
        for idx, pkg in enumerate(package_list):
            prefix = "✔" if selected_packages.get(pkg["name"], False) else "⬜"
            if idx == current_idx:
                stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(3 + idx, 2, f"{prefix} {pkg['name']}")
            if idx == current_idx:
                stdscr.attroff(curses.A_REVERSE)

        desc_start = h - 5
        stdscr.addstr(desc_start, 2, "Description:", curses.A_BOLD | curses.A_UNDERLINE)
        
        wrapped_desc = textwrap.wrap(package_list[current_idx]["description"], w - 4)
        for i, line in enumerate(wrapped_desc[:3]):
            stdscr.addstr(desc_start + 2 + i, 2, line)
        
        stdscr.addstr(h-2, 2, "Press SPACE to select, ENTER to confirm, or 'q' to go back.")
        
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == curses.KEY_UP and current_idx > 0:
            current_idx -= 1
        elif key == curses.KEY_DOWN and current_idx < len(package_list) - 1:
            current_idx += 1
        elif key == ord(" "):
            package_name = package_list[current_idx]["name"]
            selected_packages[package_name] = not selected_packages.get(package_name, False)
        elif key in [curses.KEY_ENTER, 10, 13]:
            return
        elif key == ord("q"):
            return

def confirm_installation(stdscr):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    selected_packages_list = [pkg for pkg, is_selected in selected_packages.items() if is_selected]
    
    stdscr.addstr(1, width // 2 - 8, "Confirm Installation", curses.A_BOLD | curses.A_UNDERLINE)
    
    if not selected_packages_list:
        stdscr.addstr(3, 2, "No packages selected. Press ENTER to go back.")
    else:
        stdscr.addstr(3, 2, "The following packages will be installed:")
        for index, package in enumerate(selected_packages_list):
            stdscr.addstr(5 + index, 4, f"- {package}")
        stdscr.addstr(height - 2, 2, "Press ENTER to install or 'q' to cancel.")
    
    stdscr.refresh()
    
    while True:
        key = stdscr.getch()
        if key in [curses.KEY_ENTER, 10, 13]:
            install_selected_packages(stdscr)
            return
        elif key == ord("q"):
            return 

def install_selected_packages(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(1, w//2 - 6, "Installing...", curses.A_BOLD)
    stdscr.refresh()
    
    curses.endwin()

    for category in package_sets:
        for pkg in category["packages"]:
            if selected_packages.get(pkg["name"], False):
                print(f"Installing {pkg['name']}...")
                os.system(pkg["command"])
                print(f"{pkg['name']} installed!")
    
    input("Installation complete! Press ENTER to return to the menu.")
    return

if __name__ == "__main__":
    curses.wrapper(category_menu)
