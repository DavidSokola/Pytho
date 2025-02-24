# pipeline_code.py

import cv2
import hailo
from gi.repository import Gst
from hailo_apps_infra.hailo_rpi_common import get_caps_from_pad, get_numpy_from_buffer
from hailo_apps_infra.detection_pipeline import GStreamerDetectionApp

# Config
FRAMES_PER_DECODE = 30
DMC_CONF_THRESH   = 0.4

def app_callback(pad, info, user_data):
    """Called for every new GstBuffer in the pipeline."""
    buffer = info.get_buffer()
    if not buffer:
        return Gst.PadProbeReturn.OK

    user_data.increment()
    frame_idx = user_data.get_count()
    do_decode = (frame_idx % FRAMES_PER_DECODE == 0)

    roi = hailo.get_roi_from_buffer(buffer)
    detections = roi.get_objects_typed(hailo.HAILO_DETECTION)

    print(f"[DEBUG] Frame {frame_idx} => {len(detections)} detections (decode={do_decode}).")

    # If we're not decoding this frame, just exit quickly
    if not do_decode:
        return Gst.PadProbeReturn.OK

    # If use_frame is set, extract the video frame
    gst_format, width, height = get_caps_from_pad(pad)
    if not (user_data.use_frame and gst_format and width and height):
        return Gst.PadProbeReturn.OK

    frame_rgb = get_numpy_from_buffer(buffer, gst_format, width, height)
    frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    # For each detection, check if label == "DMC" above threshold
    for det in detections:
        label = det.get_label()
        conf  = det.get_confidence()
        bbox  = det.get_bbox()
        if label == "DMC" and conf >= DMC_CONF_THRESH:
            x0 = int(bbox.xmin() * width)
            y0 = int(bbox.ymin() * height)
            x1 = int(bbox.xmax() * width)
            y1 = int(bbox.ymax() * height)
            roi_img = frame_bgr[y0:y1, x0:x1].copy()

            try:
                user_data.roi_queue.put_nowait((frame_idx, roi_img))
                print(f"[DEBUG] Enqueued ROI from frame {frame_idx} for decode.")
            except:
                print(f"[DEBUG] ROI queue full; skipping decode for frame {frame_idx}.")

    return Gst.PadProbeReturn.OK

class MyDetectionApp(GStreamerDetectionApp):
    """Optional custom detection app to override get_pipeline_string or add debug."""
    def __init__(self, callback, user_data):
        super().__init__(callback, user_data)
        print("[DEBUG] MyDetectionApp initialized.")
