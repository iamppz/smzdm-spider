import struct
import ctypes
import os

def is_64_windows():
    """Find out how many bits is OS. """
    return 'PROGRAMFILES(X86)' in os.environ

def get_sys_parameters_info():
    """Based on if this is 32bit or 64bit returns correct version of SystemParametersInfo function. """
    return ctypes.windll.user32.SystemParametersInfoW if is_64_windows() \
        else ctypes.windll.user32.SystemParametersInfoA

def change_wallpaper():
    sys_parameters_info = get_sys_parameters_info()
    r = sys_parameters_info(SPI_SETDESKWALLPAPER, 0, WALLPAPER_PATH, 3)
    if not r:           # When the SPI_SETDESKWALLPAPER flag is used, SystemParametersInfo returns TRUE unless there is an error (like when the specified file doesn't exist).
        print(ctypes.WinError())

SPI_SETDESKWALLPAPER = 20
WALLPAPER_PATH = 'C:\\your_file_name.jpg'
change_wallpaper()