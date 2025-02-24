# main.py

import sys
import signal
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
from queue import Queue

from decode_thread import DMCDecoderThread
from user_callback import user_app_callback_class
from pipeline_code import MyDetectionApp, app_callback

QUEUE_MAXSIZE = 50

decoder_thread = None
app = None

def signal_handler(sig, frame):
    print(f"[MAIN] Caught signal {sig}, shutting down gracefully...")
    if decoder_thread:
        decoder_thread.stop()
    if app:
        app.stop()
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("[DEBUG] Initializing GStreamer...")
    Gst.init(None)

    print("[DEBUG] Creating ROI queue...")
    roi_queue = Queue(maxsize=QUEUE_MAXSIZE)

    global decoder_thread
    decoder_thread = DMCDecoderThread(roi_queue)
    decoder_thread.start()
    print("[DEBUG] Decoder thread started.")

    # Create user_data for pipeline (passing the queue)
    user_data = user_app_callback_class(roi_queue)
    user_data.use_frame = True  # So we can extract frames

    # Create and run GStreamer app
    global app
    app = MyDetectionApp(app_callback, user_data)

    try:
        print("[DEBUG] Running pipeline...")
        app.run()  
        print("[DEBUG] Pipeline finished (end of stream?).")
    finally:
        print("[MAIN] Stopping decode thread.")
        decoder_thread.stop()
        decoder_thread.join()
        print("[MAIN] Decoder thread joined.")
        print("[MAIN] Done.")

if __name__ == "__main__":
    main()
