import platform
import subprocess
from logger import Logger

def is_dark_mode_enabled_windows():
    try:
        command = [
            "powershell",
            "-Command",
            "(Get-ItemProperty -Path HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize).AppsUseLightTheme"
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
        value = result.stdout.strip()
        return value == "0"
    except FileNotFoundError:
        return False
    
def is_dark_mode_enabled_linux():
    try:
        result = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"],
            stdout=subprocess.PIPE,
            text=True
        )
        theme = result.stdout.strip().lower()
        return "dark" in theme
    except FileNotFoundError:
        return False  

def is_dark_mode_enabled_macos():
    try:
        result = subprocess.run(
            ["defaults", "read", "-g", "AppleInterfaceStyle"],
            stdout=subprocess.PIPE,
            text=True
        )
        return "Dark" in result.stdout
    except subprocess.CalledProcessError:
        return False

def get_default_cfg() -> str:
    os_name = platform.system()
    src = None
    match (os_name) :
        case 'Windows':
           src = 'windows' + '_' + ('dark' if is_dark_mode_enabled_windows() else 'light') + '.json'
        case 'Linux':
            src = 'linux' + '_' + ('dark' if is_dark_mode_enabled_linux() else 'light') + '.json'
        case 'Darwin':
            src = 'macos' + '_' + ('dark' if is_dark_mode_enabled_macos() else 'light') + '.json'
        case _:
            raise TypeError('Unsupported Operating System')
    
    Logger()._instance.get_logger().info('Detected operating system is %s' % os_name)
    Logger()._instance.get_logger().info('Dark mode is %s' % ('enabled' if 'dark' in src else 'disabled'))
    return src