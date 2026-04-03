using System.Windows.Media;

namespace WorldClockWpf;

public static class ThemeBrushes
{
    public static Brush CreatePanelBrush(string theme, double opacity)
    {
        return new SolidColorBrush(theme == "dark"
            ? Color.FromArgb(ToAlpha(0.18 + opacity * 0.82), 0x12, 0x1B, 0x27)
            : Color.FromArgb(ToAlpha(0.18 + opacity * 0.82), 0xF8, 0xFB, 0xFF));
    }

    public static Brush CreateCardBrush(string theme, double opacity)
    {
        return new SolidColorBrush(theme == "dark"
            ? Color.FromArgb(ToAlpha(0.12 + opacity * 0.88), 0x1A, 0x24, 0x32)
            : Color.FromArgb(ToAlpha(0.12 + opacity * 0.88), 0xFF, 0xFF, 0xFF));
    }

    public static Brush CreateBorderBrush(string theme, double opacity)
    {
        return new SolidColorBrush(theme == "dark"
            ? Color.FromArgb(ToAlpha(0.16 + opacity * 0.84), 0x22, 0x30, 0x44)
            : Color.FromArgb(ToAlpha(0.16 + opacity * 0.84), 0xDF, 0xE7, 0xF1));
    }

    public static Brush CreatePrimaryTextBrush(string theme) =>
        new SolidColorBrush((Color)ColorConverter.ConvertFromString(theme == "dark" ? "#EEF4FF" : "#1A2433"));

    public static Brush CreateSecondaryTextBrush(string theme) =>
        new SolidColorBrush((Color)ColorConverter.ConvertFromString(theme == "dark" ? "#9CADBF" : "#556476"));

    public static Brush CreateMutedTextBrush(string theme) =>
        new SolidColorBrush((Color)ColorConverter.ConvertFromString(theme == "dark" ? "#7F92A8" : "#7A8696"));

    private static byte ToAlpha(double value) => (byte)Math.Clamp((int)Math.Round(value * 255), 0, 255);
}
