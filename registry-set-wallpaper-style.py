import winreg

reg_path = r'Control Panel\Desktop\\'

WallpaperStyle = 'WallpaperStyle'
TileWallpaper = 'TileWallpaper'

WallpaperStyle_key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE)
winreg.SetValueEx(WallpaperStyle_key, WallpaperStyle, 0, winreg.REG_SZ, str(10))
TileWallpaper_key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE)
winreg.SetValueEx(TileWallpaper_key, TileWallpaper, 0, winreg.REG_SZ, str(0))