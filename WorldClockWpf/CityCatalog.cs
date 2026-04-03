namespace WorldClockWpf;

public static class CityCatalog
{
    public static readonly IReadOnlyDictionary<string, string> Map = new Dictionary<string, string>
    {
        ["北京"] = "China Standard Time",
        ["上海"] = "China Standard Time",
        ["广州"] = "China Standard Time",
        ["深圳"] = "China Standard Time",
        ["香港"] = "China Standard Time",
        ["台北"] = "Taipei Standard Time",
        ["东京"] = "Tokyo Standard Time",
        ["大阪"] = "Tokyo Standard Time",
        ["首尔"] = "Korea Standard Time",
        ["新加坡"] = "Singapore Standard Time",
        ["曼谷"] = "SE Asia Standard Time",
        ["雅加达"] = "SE Asia Standard Time",
        ["新德里"] = "India Standard Time",
        ["迪拜"] = "Arabian Standard Time",
        ["利雅得"] = "Arab Standard Time",
        ["耶路撒冷"] = "Israel Standard Time",
        ["伊斯坦布尔"] = "Turkey Standard Time",
        ["莫斯科"] = "Russian Standard Time",
        ["伦敦"] = "GMT Standard Time",
        ["都柏林"] = "GMT Standard Time",
        ["巴黎"] = "Romance Standard Time",
        ["柏林"] = "W. Europe Standard Time",
        ["阿姆斯特丹"] = "W. Europe Standard Time",
        ["马德里"] = "Romance Standard Time",
        ["罗马"] = "W. Europe Standard Time",
        ["维也纳"] = "W. Europe Standard Time",
        ["华沙"] = "Central European Standard Time",
        ["雅典"] = "GTB Standard Time",
        ["赫尔辛基"] = "FLE Standard Time",
        ["基辅"] = "FLE Standard Time",
        ["纽约"] = "Eastern Standard Time",
        ["华盛顿"] = "Eastern Standard Time",
        ["多伦多"] = "Eastern Standard Time",
        ["迈阿密"] = "Eastern Standard Time",
        ["芝加哥"] = "Central Standard Time",
        ["达拉斯"] = "Central Standard Time",
        ["休斯顿"] = "Central Standard Time",
        ["丹佛"] = "Mountain Standard Time",
        ["凤凰城"] = "US Mountain Standard Time",
        ["洛杉矶"] = "Pacific Standard Time",
        ["旧金山"] = "Pacific Standard Time",
        ["西雅图"] = "Pacific Standard Time",
        ["温哥华"] = "Pacific Standard Time",
        ["墨西哥城"] = "Central Standard Time (Mexico)",
        ["圣保罗"] = "E. South America Standard Time",
        ["布宜诺斯艾利斯"] = "Argentina Standard Time",
        ["圣地亚哥"] = "Pacific SA Standard Time",
        ["悉尼"] = "AUS Eastern Standard Time",
        ["墨尔本"] = "AUS Eastern Standard Time",
        ["布里斯班"] = "E. Australia Standard Time",
        ["珀斯"] = "W. Australia Standard Time",
        ["奥克兰"] = "New Zealand Standard Time",
        ["开罗"] = "Egypt Standard Time",
        ["约翰内斯堡"] = "South Africa Standard Time",
        ["内罗毕"] = "E. Africa Standard Time"
    };

    public static IReadOnlyList<string> Search(string keyword, IEnumerable<string> excluded)
    {
        var excludeSet = excluded.ToHashSet();
        var query = keyword.Trim();
        IEnumerable<string> source = Map.Keys.Where(city => !excludeSet.Contains(city));
        if (!string.IsNullOrWhiteSpace(query))
        {
            source = source.Where(city => city.Contains(query, StringComparison.OrdinalIgnoreCase));
        }

        return source.Take(30).ToList();
    }
}
