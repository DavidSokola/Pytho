# user_callback.py

from hailo_apps_infra.hailo_rpi_common import app_callback_class

class user_app_callback_class(app_callback_class):
    """Manages user data/state, like the ROI queue for decoding."""
    def __init__(self, roi_queue):
        super().__init__()
        self.roi_queue = roi_queue
        print("[DEBUG] user_app_callback_class initialized.")
