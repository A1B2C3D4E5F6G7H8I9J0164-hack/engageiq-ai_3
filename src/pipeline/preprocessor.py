"""Frame preprocessing module (BGR conversion, resizing, normalization)."""

import time
from typing import Tuple

import cv2
import numpy as np

from src.pipeline.capture import TimestampedFrame


class FramePreprocessor:
    """
    FramePreprocessor converts BGR frames to RGB, resizes them to a target size,
    and normalizes their pixel values to [0.0, 1.0].
    """

    def __init__(self, target_size: Tuple[int, int] = (640, 480)):
        """
        Initialize FramePreprocessor.

        Args:
            target_size: Target resolution as (width, height). Default is (640, 480).
        """
        self.target_size = target_size

    def process(self, frame: np.ndarray) -> TimestampedFrame:
        """
        Preprocess the input frame.

        Args:
            frame: Input BGR, uint8 frame (typically numpy array).

        Returns:
            TimestampedFrame: Resized, RGB converted, and [0.0, 1.0] normalized frame.
        """
        if frame is None:
            raise ValueError("Input frame cannot be None")

        # Convert BGR to RGB (assume BGR by default for 3-channel images)
        if len(frame.shape) == 3 and frame.shape[2] == 3:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            rgb_frame = frame

        # Resize to target size (width, height)
        # Note: cv2.resize expects dsize to be (width, height)
        resized_frame = cv2.resize(rgb_frame, self.target_size)

        # Normalize pixel values to [0.0, 1.0] in float32
        normalized_frame = resized_frame.astype(np.float32) / 255.0

        # Retrieve timestamp from the original frame if it exists, otherwise generate one
        timestamp = getattr(frame, "timestamp", time.time())

        return TimestampedFrame(normalized_frame, timestamp=timestamp)
