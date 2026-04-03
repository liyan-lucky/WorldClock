import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from PyQt5.QtCore import QEvent, QPoint, QRect, QSize, Qt, QTimer, QStringListModel
from PyQt5.QtGui import QColor, QCursor, QFont, QFontMetrics
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

try:
    import winreg
except ImportError:
    winreg = None


CITY_TIMEZONES = {
    "北京": "Asia/Shanghai",
    "香港": "Asia/Hong_Kong",
    "台北": "Asia/Taipei",
    "上海": "Asia/Shanghai",
    "广州": "Asia/Shanghai",
    "深圳": "Asia/Shanghai",
    "东京": "Asia/Tokyo",
    "大阪": "Asia/Tokyo",
    "冲绳": "Asia/Tokyo",
    "首尔": "Asia/Seoul",
    "釜山": "Asia/Seoul",
    "新加坡": "Asia/Singapore",
    "吉隆坡": "Asia/Kuala_Lumpur",
    "槟城": "Asia/Phnom_Penh",
    "万象": "Asia/Vientiane",
    "仰光": "Asia/Yangon",
    "文莱": "Asia/Brunei",
    "雅加达": "Asia/Jakarta",
    "巴厘岛": "Asia/Makassar",
    "马尼拉": "Asia/Manila",
    "胡志明市": "Asia/Ho_Chi_Minh",
    "河内": "Asia/Bangkok",
    "曼谷": "Asia/Bangkok",
    "新德里": "Asia/Kolkata",
    "孟买": "Asia/Kolkata",
    "加尔各答": "Asia/Kolkata",
    "卡拉奇": "Asia/Karachi",
    "达卡": "Asia/Dhaka",
    "加德满都": "Asia/Kathmandu",
    "科伦坡": "Asia/Colombo",
    "塔什干": "Asia/Tashkent",
    "阿拉木图": "Asia/Almaty",
    "阿斯塔纳": "Asia/Almaty",
    "比什凯克": "Asia/Bishkek",
    "乌兰巴托": "Asia/Ulaanbaatar",
    "维库茨克": "Asia/Vladivostok",
    "哈巴罗夫斯克": "Asia/Vladivostok",
    "迪拜": "Asia/Dubai",
    "阿布扎比": "Asia/Dubai",
    "利雅得": "Asia/Riyadh",
    "多哈": "Asia/Qatar",
    "科威特城": "Asia/Kuwait",
    "德黑兰": "Asia/Tehran",
    "耶路撒冷": "Asia/Jerusalem",
    "特拉维夫": "Asia/Jerusalem",
    "安曼": "Asia/Amman",
    "贝鲁特": "Asia/Beirut",
    "大马士革": "Asia/Damascus",
    "巴格达": "Asia/Baghdad",
    "阿富汗": "Asia/Kabul",
    "马斯喀特": "Asia/Muscat",
    "也加达": "Asia/Aden",
    "安卡拉": "Europe/Istanbul",
    "伊斯坦布尔": "Europe/Istanbul",
    "莫斯科": "Europe/Moscow",
    "圣彼得堡": "Europe/Moscow",
    "巴黎": "Europe/Paris",
    "马赛": "Europe/Paris",
    "伦敦": "Europe/London",
    "曼彻斯特": "Europe/London",
    "都柏林": "Europe/Dublin",
    "里斯本": "Europe/Lisbon",
    "马德里": "Europe/Madrid",
    "巴塞罗那": "Europe/Madrid",
    "阿姆斯特丹": "Europe/Amsterdam",
    "布鲁塞尔": "Europe/Brussels",
    "柏林": "Europe/Berlin",
    "法兰克福": "Europe/Berlin",
    "罗马": "Europe/Rome",
    "米兰": "Europe/Rome",
    "维也纳": "Europe/Vienna",
    "布拉格": "Europe/Prague",
    "华沙": "Europe/Warsaw",
    "布达佩斯": "Europe/Budapest",
    "哥本哈根": "Europe/Copenhagen",
    "斯德哥尔摩": "Europe/Stockholm",
    "奥斯陆": "Europe/Oslo",
    "赫尔辛基": "Europe/Helsinki",
    "雅典": "Europe/Athens",
    "基辅": "Europe/Kyiv",
    "布加勒斯特": "Europe/Bucharest",
    "日内瓦": "Europe/Zurich",
    "苏黎世": "Europe/Zurich",
    "伯尔尼": "Europe/Tallinn",
    "里加": "Europe/Riga",
    "维尔纽斯": "Europe/Vilnius",
    "明斯克": "Europe/Minsk",
    "萨拉热窝": "Europe/Sarajevo",
    "贝尔格莱德": "Europe/Belgrade",
    "斯科普里": "Europe/Skopje",
    "索非亚": "Europe/Sofia",
    "萨格勒布": "Europe/Zagreb",
    "卢森堡": "Europe/Luxembourg",
    "马耳他": "Europe/Malta",
    "冰岛": "Atlantic/Reykjavik",
    "纽约": "America/New_York",
    "华盛顿": "America/New_York",
    "波士顿": "America/New_York",
    "费城": "America/New_York",
    "多伦多": "America/Toronto",
    "温哥华岛": "America/Halifax",
    "蒙特利尔": "America/Toronto",
    "魁北克": "America/Toronto",
    "温尼伯": "America/Winnipeg",
    "芝加哥": "America/Chicago",
    "达拉斯": "America/Chicago",
    "休斯顿": "America/Chicago",
    "明尼阿波利斯": "America/Chicago",
    "新奥尔良": "America/Chicago",
    "墨西哥城": "America/Mexico_City",
    "瓜达拉哈拉": "America/Mexico_City",
    "坎昆": "America/Cancun",
    "丹佛": "America/Denver",
    "凤凰城": "America/Phoenix",
    "卡尔加里": "America/Edmonton",
    "洛杉矶": "America/Los_Angeles",
    "旧金山": "America/Los_Angeles",
    "西雅图": "America/Los_Angeles",
    "拉斯维加斯": "America/Los_Angeles",
    "圣迭戈": "America/Los_Angeles",
    "波特兰": "America/Los_Angeles",
    "温哥华": "America/Vancouver",
    "安克雷奇": "America/Anchorage",
    "檀香山": "Pacific/Honolulu",
    "圣保罗": "America/Sao_Paulo",
    "里约热内卢": "America/Sao_Paulo",
    "布宜诺斯艾利斯": "America/Argentina/Buenos_Aires",
    "圣地亚哥": "America/Santiago",
    "利马": "America/Lima",
    "波哥大": "America/Bogota",
    "基多": "America/Guayaquil",
    "拉巴斯": "America/La_Paz",
    "阿斯汪森": "America/Asuncion",
    "蒙特维亚": "America/Montevideo",
    "加拿大神": "America/Panama",
    "圣约瑟": "America/Costa_Rica",
    "哈瓦那": "America/Havana",
    "圣多明各": "America/Santo_Domingo",
    "波多黎各": "America/Puerto_Rico",
    "悉尼": "Australia/Sydney",
    "墨尔本": "Australia/Melbourne",
    "布里斯班": "Australia/Brisbane",
    "珀斯": "Australia/Perth",
    "阿德莱德": "Australia/Adelaide",
    "达尔文": "Australia/Darwin",
    "霍尔": "Australia/Hobart",
    "奥克兰": "Pacific/Auckland",
    "斐济": "Pacific/Fiji",
    "关岛": "Pacific/Guam",
    "塔西提": "Pacific/Tahiti",
    "努库阿洛法": "Pacific/Tongatapu",
    "开罗": "Africa/Cairo",
    "内罗毕": "Africa/Nairobi",
    "拉各斯": "Africa/Lagos",
    "约翰内斯堡": "Africa/Johannesburg",
    "卡萨布兰卡": "Africa/Casablanca",
    "阿尔及尔": "Africa/Algiers",
    "突尼斯": "Africa/Tunis",
    "的黎波里": "Africa/Tripoli",
    "亚的斯亚贝巴": "Africa/Addis_Ababa",
    "达累斯萨拉姆": "Africa/Dar_es_Salaam",
    "坎帕拉": "Africa/Kampala",
    "基加利": "Africa/Kigali",
    "阿克拉": "Africa/Accra",
    "达喀尔": "Africa/Dakar",
    "阿比让": "Africa/Abidjan",
}

WEEKDAY_NAMES = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
DEFAULT_CITIES = ["北京", "伦敦", "纽约", "东京"]
CONFIG_FILE = (
    Path(sys.executable).resolve().with_name("world_clock_config.json")
    if getattr(sys, "frozen", False)
    else Path(__file__).resolve().with_name("world_clock_config.json")
)


def detect_system_theme() -> str:
    if winreg is None:
        return "light"
    try:
        registry = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        )
        value, _ = winreg.QueryValueEx(registry, "AppsUseLightTheme")
        return "light" if value else "dark"
    except OSError:
        return "light"


def with_alpha(hex_color: str, alpha: float) -> str:
    alpha = max(0.0, min(1.0, alpha))
    hex_color = hex_color.lstrip("#")
    red = int(hex_color[0:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:6], 16)
    return f"rgba({red}, {green}, {blue}, {alpha:.3f})"


def get_palette(theme_name: str, surface_alpha: float = 1.0) -> dict:
    surface_alpha = max(0.0, min(1.0, surface_alpha))
    visual_alpha = 0.18 + 0.82 * surface_alpha
    panel_alpha = visual_alpha
    card_alpha = visual_alpha
    input_alpha = visual_alpha
    button_alpha = visual_alpha
    line_alpha = visual_alpha
    border_alpha = visual_alpha
    shadow_alpha = int(110 * visual_alpha)
    if theme_name == "dark":
        return {
            "window_bg": "#0f1722",
            "panel_bg": with_alpha("#121b27", panel_alpha),
            "card_bg": with_alpha("#1a2432", card_alpha),
            "card_border": with_alpha("#223044", border_alpha),
            "text": "#eef4ff",
            "subtle": "#9cadbf",
            "muted": "#7f92a8",
            "line": with_alpha("#2a3442", line_alpha),
            "button": with_alpha("#1a2432", button_alpha),
            "button_hover": with_alpha("#223044", button_alpha),
            "input_bg": with_alpha("#0f1722", input_alpha),
            "list_bg": with_alpha("#0f1722", input_alpha),
            "selection": with_alpha("#2b3b53", input_alpha),
            "shadow": QColor(0, 0, 0, shadow_alpha),
        }
    return {
        "window_bg": "#eef3fb",
        "panel_bg": with_alpha("#f8fbff", panel_alpha),
        "card_bg": with_alpha("#ffffff", card_alpha),
        "card_border": with_alpha("#dfe7f1", border_alpha),
        "text": "#1a2433",
        "subtle": "#556476",
        "muted": "#7a8696",
        "line": with_alpha("#dde5f0", line_alpha),
        "button": with_alpha("#ffffff", button_alpha),
        "button_hover": with_alpha("#edf3fb", button_alpha),
        "input_bg": with_alpha("#ffffff", input_alpha),
        "list_bg": with_alpha("#ffffff", input_alpha),
        "selection": with_alpha("#dfeafb", input_alpha),
        "shadow": QColor(16, 24, 40, int(40 * surface_alpha)),
    }


class ClockCard(QFrame):
    def __init__(self, city_name: str, timezone_name: str, palette: dict, parent=None):
        super().__init__(parent)
        self.city_name = city_name
        self.timezone_name = timezone_name
        self.zone = ZoneInfo(timezone_name)

        self.setObjectName("clockCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 4, 10)
        layout.setSpacing(4)

        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.setSpacing(0)
        bottom_row = QHBoxLayout()
        bottom_row.setContentsMargins(0, 0, 0, 0)
        bottom_row.setSpacing(0)

        self.city_label = QLabel(city_name)
        self.city_label.setFont(QFont("Microsoft YaHei UI", 12, QFont.Bold))
        self.city_label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        city_metrics = QFontMetrics(self.city_label.font())
        self.city_label.setMinimumWidth(city_metrics.horizontalAdvance("测测测测测") + 2)

        self.date_label = QLabel()
        self.date_label.setFont(QFont("Microsoft YaHei UI", 9))
        self.date_label.setMinimumWidth(0)
        self.date_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.time_label = QLabel("--:--:--")
        self.time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.time_label.setFont(QFont("Consolas", 20, QFont.Bold))
        self.time_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        self.zone_label = QLabel(timezone_name.split("/")[0])
        self.zone_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.zone_label.setFont(QFont("Consolas", 9))
        self.zone_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        zone_metrics = QFontMetrics(self.zone_label.font())
        self.zone_label.setFixedWidth(zone_metrics.horizontalAdvance("WWW") + 6)

        top_row.addWidget(self.city_label, 1)
        top_row.addWidget(self.time_label, 0)

        bottom_row.addWidget(self.date_label)
        bottom_row.addStretch(1)
        bottom_row.addWidget(self.zone_label)

        layout.addLayout(top_row)
        layout.addLayout(bottom_row)

        self.apply_palette(palette)
        self.sync_right_column_width()

    def apply_palette(self, palette: dict):
        self.setStyleSheet(
            f"""
            QFrame#clockCard {{
                background: {palette['card_bg']};
                border: 1px solid {palette['card_border']};
                border-radius: 12px;
            }}
            QLabel {{
                background: transparent;
            }}
            """
        )
        self.city_label.setStyleSheet(f"color: {palette['text']};")
        self.time_label.setStyleSheet(f"color: {palette['text']};")
        self.date_label.setStyleSheet(f"color: {palette['subtle']};")
        self.zone_label.setStyleSheet(f"color: {palette['muted']};")

    def sync_right_column_width(self):
        metrics = QFontMetrics(self.time_label.font())
        text_width = metrics.horizontalAdvance(self.time_label.text())
        self.time_label.setFixedWidth(text_width + 8)

    def update_time(self, show_seconds: bool):
        current = datetime.now(self.zone)
        week_number = current.isocalendar().week
        weekday = WEEKDAY_NAMES[current.weekday()]
        self.time_label.setText(current.strftime("%H:%M:%S" if show_seconds else "%H:%M"))
        self.date_label.setText(current.strftime(f"%Y-%m-%d  {weekday}  {week_number}周"))
        self.sync_right_column_width()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            top_level = self.window()
            if hasattr(top_level, "show_delete_popup"):
                top_level.show_delete_popup(self.city_name, event.globalPos())
            event.accept()
            return
        super().mousePressEvent(event)


class MenuPopup(QWidget):
    def __init__(self, window, palette: dict):
        super().__init__(None, Qt.Popup | Qt.FramelessWindowHint)
        self.window = window
        self.palette = palette
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.NoDropShadowWindowHint, True)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self.card = QFrame()
        self.card.setObjectName("menuCard")
        outer.addWidget(self.card)

        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(20)
        effect.setXOffset(0)
        effect.setYOffset(0)
        effect.setColor(palette["shadow"])
        self.card.setGraphicsEffect(effect)

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        removable_cities = [card.city_name for card in self.window.clock_cards]
        addable_cities = [city for city in CITY_TIMEZONES if city not in removable_cities]

        self.add_input = QLineEdit()
        self.add_input.setPlaceholderText("输入地点快速匹配")
        self.add_list = QListWidget()
        self.add_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.add_list.addItems(addable_cities[:12])
        self.add_candidates = addable_cities
        self._set_add_list_height(2)

        self.pin_check = QCheckBox("窗口置顶")
        self.pin_check.setChecked(self.window.always_on_top)

        self.seconds_check = QCheckBox("显示秒数")
        self.seconds_check.setChecked(self.window.show_seconds)

        self.opacity_combo = QComboBox()
        self.opacity_map = {
            "0%": 0.0,
            "15%": 0.15,
            "30%": 0.30,
            "45%": 0.45,
            "100%": 1.0,
            "92%": 0.92,
            "85%": 0.85,
            "78%": 0.78,
            "70%": 0.70,
            "60%": 0.60,
        }
        for label in self.opacity_map:
            self.opacity_combo.addItem(label)
        current_opacity_label = next(
            (label for label, value in self.opacity_map.items() if abs(value - self.window.opacity) < 0.01),
            "92%",
        )
        self.opacity_combo.setCurrentText(current_opacity_label)

        self.theme_combo = QComboBox()
        self.theme_label_map = {
            "跟随系统": "system",
            "浅色": "light",
            "深色": "dark",
        }
        self.theme_combo.addItems(list(self.theme_label_map.keys()))
        reverse_theme = {value: key for key, value in self.theme_label_map.items()}
        self.theme_combo.setCurrentText(reverse_theme.get(self.window.theme_mode, "跟随系统"))

        layout.addWidget(self._make_label("添加地点"))
        layout.addWidget(self.add_input)
        layout.addWidget(self.add_list)
        layout.addWidget(self._make_label("删除地点"))
        layout.addWidget(self.pin_check)
        layout.addWidget(self.seconds_check)
        layout.addWidget(self._make_label("透明度"))
        layout.addWidget(self.opacity_combo)
        layout.addWidget(self._make_label("明暗主题"))
        layout.addWidget(self.theme_combo)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"background:{palette['line']}; max-height: 1px; border:none;")
        layout.addWidget(line)

        button_row = QHBoxLayout()
        button_row.addStretch(1)
        self.apply_button = QPushButton("应用")
        self.exit_button = QPushButton("退出")
        self.cancel_button = QPushButton("取消")
        button_row.addWidget(self.apply_button)
        button_row.addWidget(self.exit_button)
        button_row.addWidget(self.cancel_button)
        layout.addLayout(button_row)

        self.add_input.textChanged.connect(self.filter_cities)
        self.add_list.itemClicked.connect(self.pick_city)
        self.add_list.itemDoubleClicked.connect(self.pick_city)
        self.apply_button.clicked.connect(self.apply_changes)
        self.cancel_button.clicked.connect(self.close)
        self.exit_button.clicked.connect(self.exit_app)

        self.apply_palette(palette)

    def _make_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setStyleSheet(f"color:{self.palette['text']}; background: transparent;")
        return label

    def apply_palette(self, palette: dict):
        self.palette = palette
        self.card.setStyleSheet(
            f"""
            QFrame#menuCard {{
                background: {palette['panel_bg']};
                border: 1px solid {palette['card_border']};
                border-radius: 14px;
            }}
            QLineEdit, QComboBox, QListWidget {{
                background: {palette['input_bg']};
                color: {palette['text']};
                border: 1px solid {palette['card_border']};
                border-radius: 10px;
                padding: 6px 8px;
            }}
            QListWidget::item:selected {{
                background: {palette['selection']};
                color: {palette['text']};
                border-radius: 6px;
            }}
            QCheckBox {{
                color: {palette['text']};
                spacing: 6px;
            }}
            QPushButton {{
                background: {palette['button']};
                color: {palette['text']};
                border: 1px solid {palette['card_border']};
                border-radius: 10px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{
                background: {palette['button_hover']};
            }}
            """
        )
        effect = self.card.graphicsEffect()
        if isinstance(effect, QGraphicsDropShadowEffect):
            effect.setColor(palette["shadow"])

    def filter_cities(self, text: str):
        keyword = text.strip().lower()
        self.add_list.clear()
        filtered = [
            city for city in self.add_candidates if keyword in city.lower()
        ] if keyword else self.add_candidates
        self.add_list.addItems(filtered[:12])
        if self.add_list.count():
            self.add_list.setCurrentRow(0)

    def pick_city(self, item: QListWidgetItem):
        self.add_input.setText(item.text())

    def apply_changes(self):
        city_to_add = self.add_input.text().strip()
        city_to_remove = self.remove_combo.currentText().strip()

        self.window.always_on_top = self.pin_check.isChecked()
        self.window.show_seconds = self.seconds_check.isChecked()
        self.window.opacity = self.opacity_map[self.opacity_combo.currentText()]
        self.window.theme_mode = self.theme_label_map[self.theme_combo.currentText()]

        self.window.apply_window_options()

        if city_to_add and city_to_add in CITY_TIMEZONES:
            self.window.add_clock(city_to_add, CITY_TIMEZONES[city_to_add])
        if city_to_remove:
            self.window.remove_clock_by_city(city_to_remove)

        self.window.save_config()
        self.window.refresh_once()
        self.close()

    def exit_app(self):
        self.window.handle_close()


class DeletePopup(QWidget):
    def __init__(self, window, city_name: str, palette: dict):
        super().__init__(None, Qt.Popup | Qt.FramelessWindowHint)
        self.window = window
        self.city_name = city_name
        self.palette = palette
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.NoDropShadowWindowHint, True)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self.card = QFrame()
        self.card.setObjectName("deleteCard")
        outer.addWidget(self.card)

        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(18)
        effect.setXOffset(0)
        effect.setYOffset(0)
        effect.setColor(palette["shadow"])
        self.card.setGraphicsEffect(effect)

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(0)

        self.delete_button = QPushButton("删除")
        self.delete_button.clicked.connect(self.delete_city)
        layout.addWidget(self.delete_button)

        self.apply_palette(palette)

    def apply_palette(self, palette: dict):
        self.palette = palette
        self.card.setStyleSheet(
            f"""
            QFrame#deleteCard {{
                background: {palette['panel_bg']};
                border: 1px solid {palette['card_border']};
                border-radius: 12px;
            }}
            QPushButton {{
                background: {palette['button']};
                color: {palette['text']};
                border: 1px solid {palette['card_border']};
                border-radius: 10px;
                padding: 6px 18px;
            }}
            QPushButton:hover {{
                background: {palette['button_hover']};
            }}
            """
        )
        effect = self.card.graphicsEffect()
        if isinstance(effect, QGraphicsDropShadowEffect):
            effect.setColor(palette["shadow"])

    def delete_city(self):
        self.window.remove_clock_by_city(self.city_name)
        self.window.save_config()
        self.close()


class CompactMenuPopup(QWidget):
    def __init__(self, window, palette: dict):
        super().__init__(None, Qt.Popup | Qt.FramelessWindowHint)
        self.window = window
        self.palette = palette
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.NoDropShadowWindowHint, True)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self.card = QFrame()
        self.card.setObjectName("compactMenuCard")
        outer.addWidget(self.card)

        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(18)
        effect.setXOffset(0)
        effect.setYOffset(0)
        effect.setColor(palette["shadow"])
        self.card.setGraphicsEffect(effect)

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        used_cities = [card.city_name for card in self.window.clock_cards]
        self.add_candidates = [city for city in CITY_TIMEZONES if city not in used_cities]

        self.add_title = QLabel("添加地点")
        self.add_input = QLineEdit()
        self.add_input.setPlaceholderText("输入地点快速匹配")
        self.add_list = QListWidget()
        self.add_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.add_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.add_list.addItems(self.add_candidates[:12])

        self.pin_check = QCheckBox("窗口置顶")
        self.pin_check.setChecked(self.window.always_on_top)
        self.seconds_check = QCheckBox("显示秒数")
        self.seconds_check.setChecked(self.window.show_seconds)

        self.opacity_title = QLabel("透明度")
        self.opacity_combo = QComboBox()
        self.opacity_map = {
            "100%": 1.0,
            "92%": 0.92,
            "85%": 0.85,
            "78%": 0.78,
            "60%": 0.60,
            "45%": 0.45,
            "30%": 0.30,
            "15%": 0.15,
            "0%": 0.0,
        }
        for label in self.opacity_map:
            self.opacity_combo.addItem(label)
        current_opacity_label = next(
            (label for label, value in self.opacity_map.items() if abs(value - self.window.opacity) < 0.01),
            "92%",
        )
        self.opacity_combo.setCurrentText(current_opacity_label)

        self.theme_title = QLabel("明暗主题")
        self.theme_combo = QComboBox()
        self.theme_label_map = {
            "跟随系统": "system",
            "浅色": "light",
            "深色": "dark",
        }
        self.theme_combo.addItems(list(self.theme_label_map.keys()))
        reverse_theme = {value: key for key, value in self.theme_label_map.items()}
        self.theme_combo.setCurrentText(reverse_theme.get(self.window.theme_mode, "跟随系统"))

        layout.addWidget(self.add_title)
        layout.addWidget(self.add_input)
        layout.addWidget(self.add_list)
        layout.addWidget(self.pin_check)
        layout.addWidget(self.seconds_check)
        layout.addWidget(self.opacity_title)
        layout.addWidget(self.opacity_combo)
        layout.addWidget(self.theme_title)
        layout.addWidget(self.theme_combo)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"background:{palette['line']}; max-height: 1px; border:none;")
        layout.addWidget(line)

        button_row = QHBoxLayout()
        button_row.setContentsMargins(0, 0, 0, 0)
        button_row.setSpacing(6)
        self.apply_button = QPushButton("应用")
        self.exit_button = QPushButton("退出")
        self.cancel_button = QPushButton("取消")
        for button in (self.apply_button, self.exit_button, self.cancel_button):
            button.setMinimumWidth(50)
            button_row.addWidget(button)
        layout.addLayout(button_row)

        self.add_input.textChanged.connect(self.filter_cities)
        self.add_list.itemClicked.connect(self.pick_city)
        self.add_list.itemDoubleClicked.connect(self.pick_city)
        self.apply_button.clicked.connect(self.apply_changes)
        self.cancel_button.clicked.connect(self.close)
        self.exit_button.clicked.connect(self.exit_app)

        self.apply_palette(palette)
        self._set_add_list_height(2)
        self.setFixedWidth(196)

    def _set_add_list_height(self, rows: int):
        row_height = self.add_list.sizeHintForRow(0) if self.add_list.count() else 26
        row_height = max(26, row_height)
        frame = self.add_list.frameWidth() * 2
        self.add_list.setFixedHeight(row_height * rows + frame + 4)

    def apply_palette(self, palette: dict):
        self.palette = palette
        text_style = f"color:{palette['text']}; background: transparent;"
        for label in (self.add_title, self.opacity_title, self.theme_title):
            label.setStyleSheet(text_style)
        self.card.setStyleSheet(
            f"""
            QFrame#compactMenuCard {{
                background: {palette['panel_bg']};
                border: 1px solid {palette['card_border']};
                border-radius: 14px;
            }}
            QLineEdit, QComboBox, QListWidget {{
                background: {palette['input_bg']};
                color: {palette['text']};
                border: 1px solid {palette['card_border']};
                border-radius: 10px;
                padding: 5px 8px;
            }}
            QListWidget {{
                padding: 2px 4px;
            }}
            QListWidget::item:selected {{
                background: {palette['selection']};
                color: {palette['text']};
                border-radius: 6px;
            }}
            QCheckBox {{
                color: {palette['text']};
                spacing: 6px;
            }}
            QPushButton {{
                background: {palette['button']};
                color: {palette['text']};
                border: 1px solid {palette['card_border']};
                border-radius: 10px;
                padding: 6px 8px;
            }}
            QPushButton:hover {{
                background: {palette['button_hover']};
            }}
            """
        )
        effect = self.card.graphicsEffect()
        if isinstance(effect, QGraphicsDropShadowEffect):
            effect.setColor(palette["shadow"])

    def filter_cities(self, text: str):
        keyword = text.strip().lower()
        self.add_list.clear()
        filtered = [city for city in self.add_candidates if keyword in city.lower()] if keyword else self.add_candidates
        self.add_list.addItems(filtered[:12])
        if self.add_list.count():
            self.add_list.setCurrentRow(0)
        self._set_add_list_height(2)

    def pick_city(self, item: QListWidgetItem):
        self.add_input.setText(item.text())

    def apply_changes(self):
        city_to_add = self.add_input.text().strip()
        self.window.always_on_top = self.pin_check.isChecked()
        self.window.show_seconds = self.seconds_check.isChecked()
        self.window.opacity = self.opacity_map[self.opacity_combo.currentText()]
        self.window.theme_mode = self.theme_label_map[self.theme_combo.currentText()]
        self.window.apply_window_options()
        if city_to_add and city_to_add in CITY_TIMEZONES:
            self.window.add_clock(city_to_add, CITY_TIMEZONES[city_to_add])
        self.window.save_config()
        self.window.refresh_once()
        self.close()

    def exit_app(self):
        self.window.handle_close()


class WorldClockWindow(QWidget):
    def __init__(self):
        super().__init__(None, Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setWindowTitle("WorldClock")
        self.resize(360, 250)
        self.move(120, 120)

        self.min_width = 318
        self.min_height = 160
        self.resize_margin = 8

        self.always_on_top = False
        self.show_seconds = True
        self.opacity = 0.92
        self.theme_mode = "system"
        self.current_theme = "light"

        self.drag_pos = None
        self.resize_edge = None
        self.resizing = False
        self.popup = None
        self.delete_popup = None

        self.clock_cards = []

        self._build_ui()
        self.restore_state()
        self.apply_window_options()
        self.refresh_once()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_once)
        self.timer.start(1000)

        self.theme_timer = QTimer(self)
        self.theme_timer.timeout.connect(self.refresh_system_theme)
        self.theme_timer.start(2000)

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(14, 14, 14, 14)

        self.panel = QFrame()
        self.panel.setObjectName("panel")
        root.addWidget(self.panel)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.panel.setGraphicsEffect(shadow)

        panel_layout = QVBoxLayout(self.panel)
        panel_layout.setContentsMargins(14, 12, 14, 14)
        panel_layout.setSpacing(10)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(8)
        self.content_layout.addStretch(1)
        self.scroll.setWidget(self.content)

        panel_layout.addWidget(self.scroll)

        self.apply_theme()

    def resolve_theme(self) -> str:
        return detect_system_theme() if self.theme_mode == "system" else self.theme_mode

    def apply_theme(self):
        self.current_theme = self.resolve_theme()
        palette = get_palette(self.current_theme, self.opacity)

        self.panel.setStyleSheet(
            f"""
            QFrame#panel {{
                background: {palette['panel_bg']};
                border-radius: 12px;
            }}
            QScrollArea, QWidget {{
                background: transparent;
            }}
            """
        )

        effect = self.panel.graphicsEffect()
        if isinstance(effect, QGraphicsDropShadowEffect):
            effect.setColor(palette["shadow"])

        for card in self.clock_cards:
            card.apply_palette(palette)

        if self.popup is not None and self.popup.isVisible():
            self.popup.apply_palette(palette)
        if self.delete_popup is not None and self.delete_popup.isVisible():
            self.delete_popup.apply_palette(palette)

    def apply_window_options(self):
        self.setWindowOpacity(1.0)
        self.setWindowFlag(Qt.Tool, True)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, self.always_on_top)
        self.show()
        self.apply_theme()

    def refresh_system_theme(self):
        if self.theme_mode == "system":
            next_theme = detect_system_theme()
            if next_theme != self.current_theme:
                self.apply_theme()

    def refresh_once(self):
        for card in self.clock_cards:
            card.update_time(self.show_seconds)

    def add_clock(self, city_name: str, timezone_name: str):
        if any(card.city_name == city_name for card in self.clock_cards):
            return
        try:
            card = ClockCard(city_name, timezone_name, get_palette(self.current_theme, self.opacity))
        except ZoneInfoNotFoundError:
            return
        self.clock_cards.append(card)
        self.content_layout.insertWidget(len(self.clock_cards) - 1, card)
        self.update_minimums()

    def remove_clock_by_city(self, city_name: str):
        target = next((card for card in self.clock_cards if card.city_name == city_name), None)
        if target is None:
            return
        self.clock_cards.remove(target)
        target.deleteLater()
        self.update_minimums()

    def update_minimums(self):
        card_min_width = max((card.minimumSizeHint().width() for card in self.clock_cards), default=0)
        window_padding = 44
        fallback_width = 220 if self.show_seconds else 196
        self.min_width = max(fallback_width, card_min_width + window_padding)
        self.setMinimumSize(self.min_width, self.min_height)
        if self.width() < self.min_width:
            self.resize(self.min_width, self.height())

    def save_config(self):
        if self.width() < self.min_width or self.height() < self.min_height:
            return
        data = {
            "window": {
                "width": self.width(),
                "height": self.height(),
                "x": self.x(),
                "y": self.y(),
            },
            "always_on_top": self.always_on_top,
            "alpha": self.opacity,
            "theme_mode": self.theme_mode,
            "show_seconds": self.show_seconds,
            "cities": [card.city_name for card in self.clock_cards],
        }
        try:
            CONFIG_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError:
            pass

    def load_config(self):
        if not CONFIG_FILE.exists():
            return {}
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}

    def restore_state(self):
        data = self.load_config()
        self.always_on_top = bool(data.get("always_on_top", False))
        self.show_seconds = bool(data.get("show_seconds", True))
        self.theme_mode = data.get("theme_mode", "system")
        if self.theme_mode not in {"system", "light", "dark"}:
            self.theme_mode = "system"
        try:
            self.opacity = float(data.get("alpha", 0.92))
        except (TypeError, ValueError):
            self.opacity = 0.92
        self.opacity = max(0.0, min(1.0, self.opacity))

        self.update_minimums()

        window = data.get("window", {})
        if isinstance(window, dict):
            try:
                width = max(self.min_width, int(window.get("width", 360)))
                height = max(self.min_height, int(window.get("height", 250)))
                x = int(window.get("x", 120))
                y = int(window.get("y", 120))
                self.setGeometry(x, y, width, height)
            except (TypeError, ValueError):
                self.resize(max(360, self.min_width), 250)
        cities = data.get("cities")
        if isinstance(cities, list):
            for city in cities:
                if city in CITY_TIMEZONES:
                    self.add_clock(city, CITY_TIMEZONES[city])
        if not self.clock_cards:
            for city in DEFAULT_CITIES:
                self.add_clock(city, CITY_TIMEZONES[city])

    def show_popup(self, global_pos: QPoint):
        if self.delete_popup is not None:
            self.delete_popup.close()
        if self.popup is not None:
            self.popup.close()
        self.popup = CompactMenuPopup(self, get_palette(self.current_theme, self.opacity))
        self.popup.adjustSize()

        popup_size = self.popup.sizeHint()
        screen = QApplication.screenAt(global_pos) or QApplication.primaryScreen()
        available = screen.availableGeometry() if screen is not None else QRect(0, 0, 1920, 1080)
        x = global_pos.x() - 6
        y = global_pos.y() - 6
        if x + popup_size.width() > available.right():
            x = available.right() - popup_size.width()
        if y + popup_size.height() > available.bottom():
            y = global_pos.y() - popup_size.height() + 6
        x = max(available.left() + 6, x)
        y = max(available.top() + 6, y)

        self.popup.move(x, y)
        self.popup.show()
        self.popup.raise_()
        self.popup.activateWindow()

    def show_delete_popup(self, city_name: str, global_pos: QPoint):
        if self.popup is not None:
            self.popup.close()
        if self.delete_popup is not None:
            self.delete_popup.close()
        self.delete_popup = DeletePopup(self, city_name, get_palette(self.current_theme, self.opacity))
        self.delete_popup.adjustSize()

        popup_size = self.delete_popup.sizeHint()
        x = max(8, global_pos.x() - popup_size.width() // 2)
        y = max(8, global_pos.y() - popup_size.height() - 6)

        self.delete_popup.move(x, y)
        self.delete_popup.show()
        self.delete_popup.raise_()
        self.delete_popup.activateWindow()

    def find_clock_card(self, widget):
        current = widget
        while current is not None:
            if isinstance(current, ClockCard):
                return current
            current = current.parentWidget()
        return None

    def contextMenuEvent(self, event):
        widget = self.childAt(event.pos())
        if self.find_clock_card(widget) is None:
            self.show_popup(event.globalPos())
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            widget = self.childAt(event.pos())
            if self.find_clock_card(widget) is None:
                self.show_popup(event.globalPos())
            else:
                event.ignore()
            return
        if event.button() != Qt.LeftButton:
            return

        edge = self.hit_test(event.pos())
        if edge:
            self.resize_edge = edge
            self.resizing = True
            self.drag_pos = event.globalPos()
            self.start_geometry = self.geometry()
            return

        if self.panel.geometry().contains(event.pos()):
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.resizing and self.resize_edge:
            self.perform_resize(event.globalPos())
            return

        if self.drag_pos and event.buttons() & Qt.LeftButton and not self.resize_edge:
            self.move(event.globalPos() - self.drag_pos)
            return

        edge = self.hit_test(event.pos())
        cursor_map = {
            "left": Qt.SizeHorCursor,
            "right": Qt.SizeHorCursor,
            "top": Qt.SizeVerCursor,
            "bottom": Qt.SizeVerCursor,
            "top_left": Qt.SizeFDiagCursor,
            "bottom_right": Qt.SizeFDiagCursor,
            "top_right": Qt.SizeBDiagCursor,
            "bottom_left": Qt.SizeBDiagCursor,
        }
        self.setCursor(QCursor(cursor_map.get(edge, Qt.ArrowCursor)))

    def mouseReleaseEvent(self, _event):
        self.drag_pos = None
        self.resize_edge = None
        self.resizing = False
        self.save_config()

    def hit_test(self, pos: QPoint):
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()
        m = self.resize_margin
        left = x <= m
        right = x >= w - m
        top = y <= m
        bottom = y >= h - m

        if left and top:
            return "top_left"
        if right and top:
            return "top_right"
        if left and bottom:
            return "bottom_left"
        if right and bottom:
            return "bottom_right"
        if left:
            return "left"
        if right:
            return "right"
        if top:
            return "top"
        if bottom:
            return "bottom"
        return None

    def perform_resize(self, global_pos: QPoint):
        rect = QRect(self.start_geometry)
        diff = global_pos - self.drag_pos

        if "left" in self.resize_edge:
            new_left = rect.left() + diff.x()
            max_left = rect.right() - self.min_width
            rect.setLeft(min(new_left, max_left))
        if "right" in self.resize_edge:
            rect.setWidth(max(self.min_width, rect.width() + diff.x()))
        if "top" in self.resize_edge:
            new_top = rect.top() + diff.y()
            max_top = rect.bottom() - self.min_height
            rect.setTop(min(new_top, max_top))
        if "bottom" in self.resize_edge:
            rect.setHeight(max(self.min_height, rect.height() + diff.y()))

        self.setGeometry(rect)

    def handle_close(self):
        self.save_config()
        self.close()


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    window = WorldClockWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
