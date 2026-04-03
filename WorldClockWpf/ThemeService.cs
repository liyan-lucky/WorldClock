using Microsoft.Win32;

namespace WorldClockWpf;

public static class ThemeService
{
    public static string ResolveTheme(string themeMode)
    {
        if (themeMode != "system")
        {
            return themeMode;
        }

        try
        {
            using var key = Registry.CurrentUser.OpenSubKey(@"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize");
            var value = key?.GetValue("AppsUseLightTheme");
            if (value is int intValue && intValue == 0)
            {
                return "dark";
            }
        }
        catch
        {
        }

        return "light";
    }
}
