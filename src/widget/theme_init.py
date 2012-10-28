from dtk.ui.skin_config import skin_config
from dtk.ui.theme import Theme, ui_theme
import os
from dtk.ui.utils import get_parent_dir

# Init skin config.
skin_config.init_skin(
    "blue",
    os.path.join(get_parent_dir(__file__, 3), "skin"),
    os.path.expanduser("~/.config/worklist/skin"),
    os.path.expanduser("~/.config/worklist/skin_config.ini"),
    "worklist",
    "1.0"
    )

# Create application theme.
app_theme = Theme(
    os.path.join(get_parent_dir(__file__, 3), "theme"),
    os.path.expanduser("~/.config/worklist/theme")
    )


# Set theme.
skin_config.load_themes(ui_theme, app_theme)
skin_config.set_application_window_size(300, 500)
