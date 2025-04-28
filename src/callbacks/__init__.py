from .dropdowns import register_dropdown_callbacks
from .status_pie import register_status_callbacks
from .latency import register_latency_callbacks
from .load import register_load_callbacks
from .download import register_download_callbacks
from .comments import register_comments_callbacks

def register_callbacks(app):
    register_dropdown_callbacks(app)
    register_status_callbacks(app)
    register_latency_callbacks(app)
    register_load_callbacks(app)
    register_download_callbacks(app)
    register_comments_callbacks(app)