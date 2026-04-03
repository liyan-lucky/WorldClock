using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.Runtime.CompilerServices;
using System.Text.Json;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Threading;
using Microsoft.Win32;

namespace WorldClockWpf;

public partial class MainWindow : Window, INotifyPropertyChanged
{
    private readonly DispatcherTimer _timer;
    private readonly string _configPath = Path.Combine(AppContext.BaseDirectory, "world_clock_config.json");
    private AppConfig _config = AppConfig.CreateDefault();
    private string _resolvedTheme = "light";

    public ObservableCollection<ClockItemViewModel> ClockItems { get; } = [];

    public event PropertyChangedEventHandler? PropertyChanged;

    public MainWindow()
    {
        InitializeComponent();
        DataContext = this;

        LoadConfig();
        BuildClockItems();
        ApplyTheme();
        ApplyWindowOptions();
        RefreshClocks();

        _timer = new DispatcherTimer
        {
            Interval = TimeSpan.FromSeconds(1)
        };
        _timer.Tick += (_, _) =>
        {
            RefreshClocks();
            if (_config.ThemeMode == "system")
            {
                var nextTheme = ThemeService.ResolveTheme(_config.ThemeMode);
                if (nextTheme != _resolvedTheme)
                {
                    ApplyTheme();
                }
            }
        };
        _timer.Start();

        MouseLeftButtonDown += (_, _) =>
        {
            try
            {
                DragMove();
            }
            catch
            {
            }
        };

        var settingsMenu = new ContextMenu();
        settingsMenu.Items.Add(new MenuItem { Header = "设置" });
        ((MenuItem)settingsMenu.Items[0]).Click += (_, _) => OpenSettings();
        settingsMenu.Items.Add(new Separator());
        settingsMenu.Items.Add(new MenuItem { Header = "退出" });
        ((MenuItem)settingsMenu.Items[2]).Click += (_, _) => Close();
        ContextMenu = settingsMenu;
    }

    private void LoadConfig()
    {
        if (File.Exists(_configPath))
        {
            try
            {
                var loaded = JsonSerializer.Deserialize<AppConfig>(File.ReadAllText(_configPath));
                if (loaded is not null)
                {
                    _config = loaded.Normalize();
                }
            }
            catch
            {
                _config = AppConfig.CreateDefault();
            }
        }

        Width = Math.Max(MinWidth, _config.WindowWidth);
        Height = Math.Max(MinHeight, _config.WindowHeight);
        Left = _config.WindowLeft;
        Top = _config.WindowTop;
    }

    private void SaveConfig()
    {
        _config.WindowWidth = Width;
        _config.WindowHeight = Height;
        _config.WindowLeft = Left;
        _config.WindowTop = Top;

        var json = JsonSerializer.Serialize(_config, new JsonSerializerOptions { WriteIndented = true });
        File.WriteAllText(_configPath, json);
    }

    private void BuildClockItems()
    {
        ClockItems.Clear();
        foreach (var city in _config.Cities.Where(CityCatalog.Map.ContainsKey))
        {
            ClockItems.Add(new ClockItemViewModel(city, CityCatalog.Map[city]));
        }

        if (ClockItems.Count == 0)
        {
            foreach (var city in AppConfig.DefaultCities)
            {
                ClockItems.Add(new ClockItemViewModel(city, CityCatalog.Map[city]));
            }
            _config.Cities = ClockItems.Select(item => item.City).ToList();
        }
    }

    private void RefreshClocks()
    {
        foreach (var item in ClockItems)
        {
            item.Update(_config.ShowSeconds);
        }
    }

    private void ApplyWindowOptions()
    {
        Topmost = _config.AlwaysOnTop;
        var visualOpacity = 0.18 + (_config.Opacity * 0.82);
        RootBorder.Background = ThemeBrushes.CreatePanelBrush(_resolvedTheme, visualOpacity);
    }

    private void ApplyTheme()
    {
        _resolvedTheme = ThemeService.ResolveTheme(_config.ThemeMode);
        RootBorder.Background = ThemeBrushes.CreatePanelBrush(_resolvedTheme, 0.18 + (_config.Opacity * 0.82));
        foreach (var item in ClockItems)
        {
            item.ApplyTheme(_resolvedTheme, _config.Opacity);
        }
    }

    private void OpenSettings()
    {
        var window = new SettingsWindow(_config, ClockItems.Select(item => item.City).ToList());
        window.Owner = this;
        if (window.ShowDialog() != true)
        {
            return;
        }

        _config = window.BuildConfig(_config);
        BuildClockItems();
        ApplyTheme();
        ApplyWindowOptions();
        RefreshClocks();
        SaveConfig();
    }

    private void DeleteClockMenuItem_Click(object sender, RoutedEventArgs e)
    {
        if (sender is not MenuItem menuItem || menuItem.Tag is not string city)
        {
            return;
        }

        var target = ClockItems.FirstOrDefault(item => item.City == city);
        if (target is null)
        {
            return;
        }

        ClockItems.Remove(target);
        _config.Cities = ClockItems.Select(item => item.City).ToList();
        SaveConfig();
    }

    protected override void OnClosing(CancelEventArgs e)
    {
        SaveConfig();
        base.OnClosing(e);
    }

    protected override void OnLocationChanged(EventArgs e)
    {
        base.OnLocationChanged(e);
        SaveConfig();
    }

    protected override void OnRenderSizeChanged(SizeChangedInfo sizeInfo)
    {
        base.OnRenderSizeChanged(sizeInfo);
        SaveConfig();
    }

    private void Notify([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
