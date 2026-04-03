using System.Windows;

namespace WorldClockWpf;

public partial class SettingsWindow : Window
{
    private readonly List<string> _existingCities;

    public SettingsWindow(AppConfig config, List<string> existingCities)
    {
        InitializeComponent();
        _existingCities = existingCities;

        TopMostCheckBox.IsChecked = config.AlwaysOnTop;
        ShowSecondsCheckBox.IsChecked = config.ShowSeconds;

        ThemeComboBox.ItemsSource = new[]
        {
            new KeyValuePair<string, string>("跟随系统", "system"),
            new KeyValuePair<string, string>("浅色", "light"),
            new KeyValuePair<string, string>("深色", "dark")
        };
        ThemeComboBox.DisplayMemberPath = "Key";
        ThemeComboBox.SelectedValuePath = "Value";
        ThemeComboBox.SelectedValue = config.ThemeMode;

        OpacityComboBox.ItemsSource = new[]
        {
            new KeyValuePair<string, double>("100%", 1.00),
            new KeyValuePair<string, double>("92%", 0.92),
            new KeyValuePair<string, double>("85%", 0.85),
            new KeyValuePair<string, double>("78%", 0.78),
            new KeyValuePair<string, double>("60%", 0.60),
            new KeyValuePair<string, double>("45%", 0.45),
            new KeyValuePair<string, double>("30%", 0.30),
            new KeyValuePair<string, double>("15%", 0.15),
            new KeyValuePair<string, double>("0%", 0.00)
        };
        OpacityComboBox.DisplayMemberPath = "Key";
        OpacityComboBox.SelectedValuePath = "Value";
        OpacityComboBox.SelectedValue = config.Opacity;

        RefreshCandidates();
    }

    public AppConfig BuildConfig(AppConfig previous)
    {
        var next = previous.Normalize();
        next.AlwaysOnTop = TopMostCheckBox.IsChecked == true;
        next.ShowSeconds = ShowSecondsCheckBox.IsChecked == true;
        next.ThemeMode = ThemeComboBox.SelectedValue as string ?? "system";
        next.Opacity = OpacityComboBox.SelectedValue is double opacity ? opacity : 1.0;

        var selectedCity = CandidateList.SelectedItem as string;
        if (!string.IsNullOrWhiteSpace(selectedCity) && !next.Cities.Contains(selectedCity))
        {
            next.Cities.Add(selectedCity);
        }

        return next;
    }

    private void RefreshCandidates()
    {
        CandidateList.ItemsSource = CityCatalog.Search(SearchBox.Text, _existingCities);
        if (CandidateList.Items.Count > 0)
        {
            CandidateList.SelectedIndex = 0;
        }
    }

    private void SearchBox_TextChanged(object sender, System.Windows.Controls.TextChangedEventArgs e)
    {
        RefreshCandidates();
    }

    private void CancelButton_Click(object sender, RoutedEventArgs e)
    {
        DialogResult = false;
    }

    private void ApplyButton_Click(object sender, RoutedEventArgs e)
    {
        DialogResult = true;
    }
}
