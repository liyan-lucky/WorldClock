namespace WorldClockWpf;

public sealed class AppConfig
{
    public static readonly IReadOnlyList<string> DefaultCities = ["北京", "伦敦", "纽约", "东京"];

    public double WindowWidth { get; set; } = 320;
    public double WindowHeight { get; set; } = 240;
    public double WindowLeft { get; set; } = 120;
    public double WindowTop { get; set; } = 120;
    public bool AlwaysOnTop { get; set; }
    public bool ShowSeconds { get; set; } = true;
    public double Opacity { get; set; } = 1.0;
    public string ThemeMode { get; set; } = "system";
    public List<string> Cities { get; set; } = [.. DefaultCities];

    public static AppConfig CreateDefault() => new();

    public AppConfig Normalize()
    {
        Opacity = Math.Clamp(Opacity, 0.0, 1.0);
        if (ThemeMode is not ("system" or "light" or "dark"))
        {
            ThemeMode = "system";
        }

        Cities = Cities.Where(CityCatalog.Map.ContainsKey).Distinct().ToList();
        if (Cities.Count == 0)
        {
            Cities = [.. DefaultCities];
        }

        WindowWidth = Math.Max(220, WindowWidth);
        WindowHeight = Math.Max(150, WindowHeight);
        return this;
    }
}
