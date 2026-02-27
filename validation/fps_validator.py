import cv2
from config import MIN_FPS, MIN_DURATION, TOTAL_FRAMES

FPS_TOLERANCE = 0.5  # allow slight hardware variation


def validate_fps_and_duration(cap, is_live=False):
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    duration = 0
    if fps > 0 and frame_count > 0:
        duration = frame_count / fps

    result = {
        "fps": float(fps),
        "duration_sec": float(duration),
        "min_fps_required": MIN_FPS,
        "min_duration_required": MIN_DURATION,
        "valid": True
    }

    # Allow small tolerance for real webcams
    if fps + FPS_TOLERANCE < MIN_FPS:
        result["valid"] = False

    # Duration and frame-count checks only apply to pre-recorded files.
    # For live webcam streams these metadata values are unknown (-1 / 0).
    if not is_live:
        if duration < MIN_DURATION:
            result["valid"] = False

        if frame_count < TOTAL_FRAMES:
            result["valid"] = False

    return result