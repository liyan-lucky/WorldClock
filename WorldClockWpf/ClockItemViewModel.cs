using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows.Media;

namespace WorldClockWpf;

public sealed class ClockItemViewModel : INotifyPropertyChanged
{
    private static readonly string[] Weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"];
    private readonly TimeZoneInfo _timeZoneInfo;

    public string City { get; }
    public string TimeZoneId { get; }
    public string RegionText { get; }

    private string _timeText = "--:--";
    private string _dateText = string.Empty;
    private Brush _cardBackground = Brushes.Transparent;
    private Brush _cardBorderBrush = Brushes.Transparent;
    private Brush _primaryForeground = Brushes.White;
    private Brush _secondaryForeground = Brushes.LightGray;
    private Brush _mutedForeground = Brushes.Gray;

    public string TimeText
    {
        get => _timeText;
        private set => SetField(ref _timeText, value);
    }

    public string DateText
    {
        get => _dateText;
        private set => SetField(ref _dateText, value);
    }

    public Brush CardBackground
    {
        get => _cardBackground;
        private set => SetField(ref _cardBackground, value);
    }

    public Brush CardBorderBrush
    {
        get => _cardBorderBrush;
        private set => SetField(ref _cardBorderBrush, value);
    }

    public Brush PrimaryForeground
    {
        get => _primaryForeground;
        private set => SetField(ref _primaryForeground, value);
    }

    public Brush SecondaryForeground
    {
        get => _secondaryForeground;
        private set => SetField(ref _secondaryForeground, value);
    }

    public Brush MutedForeground
    {
        get => _mutedForeground;
        private set => SetField(ref _mutedForeground, value);
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    public ClockItemViewModel(string city, string timeZoneId)
    {
        City = city;
        TimeZoneId = timeZoneId;
        _timeZoneInfo = TimeZoneInfo.FindSystemTimeZoneById(timeZoneId);
        RegionText = timeZoneId.Split('/')[0];
    }

    public void Update(bool showSeconds)
    {
        var now = TimeZoneInfo.ConvertTime(DateTimeOffset.UtcNow, _timeZoneInfo);
        var week = System.Globalization.ISOWeek.GetWeekOfYear(now.Date);
        TimeText = now.ToString(showSeconds ? "HH:mm:ss" : "HH:mm");
        DateText = $"{now:yyyy-MM-dd}  {Weekdays[((int)now.DayOfWeek + 6) % 7]}  {week}周";
    }

    public void ApplyTheme(string themeMode, double opacity)
    {
        CardBackground = ThemeBrushes.CreateCardBrush(themeMode, opacity);
        CardBorderBrush = ThemeBrushes.CreateBorderBrush(themeMode, opacity);
        PrimaryForeground = ThemeBrushes.CreatePrimaryTextBrush(themeMode);
        SecondaryForeground = ThemeBrushes.CreateSecondaryTextBrush(themeMode);
        MutedForeground = ThemeBrushes.CreateMutedTextBrush(themeMode);
    }

    private void SetField<T>(ref T storage, T value, [CallerMemberName] string? propertyName = null)
    {
        if (EqualityComparer<T>.Default.Equals(storage, value))
        {
            return;
        }

        storage = value;
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
