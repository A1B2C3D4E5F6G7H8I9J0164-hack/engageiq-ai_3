"""Unit tests for the FramePreprocessor class."""

import numpy as np

from src.pipeline.capture import TimestampedFrame
from src.pipeline.preprocessor import FramePreprocessor


def test_preprocessor_shape_and_range():
    """Test default resizing shape, data type, and normalization range."""
    # Simulate a BGR 1080p frame (height=1080, width=1920, channels=3)
    frame = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)

    # Target size: (width=640, height=480)
    prep = FramePreprocessor(target_size=(640, 480))
    result = prep.process(frame)

    # Output shape should be (height, width, channels) -> (480, 640, 3)
    assert result.shape == (480, 640, 3)
    assert result.dtype == np.float32

    # Value range should be scaled to [0.0, 1.0]
    assert result.min() >= 0.0
    assert result.max() <= 1.0


def test_preprocessor_rgb_conversion():
    """Test that BGR color channel ordering is correctly converted to RGB."""
    # Create a small image filled with a single color: Pure Blue in BGR: B=255, G=0, R=0
    frame = np.zeros((10, 10, 3), dtype=np.uint8)
    frame[:, :] = [255, 0, 0]

    # Process (resizing to 5x5)
    prep = FramePreprocessor(target_size=(5, 5))
    result = prep.process(frame)

    # Pure Blue in BGR becomes Pure Blue in RGB (R=0, G=0, B=255)
    # Normalized value should be (0.0, 0.0, 1.0)
    assert np.allclose(result[0, 0, 0], 0.0)  # Red channel
    assert np.allclose(result[0, 0, 1], 0.0)  # Green channel
    assert np.allclose(result[0, 0, 2], 1.0)  # Blue channel


def test_preprocessor_timestamp_preservation():
    """Test that the input frame's timestamp is preserved in the preprocessed output."""
    raw_frame = np.zeros((100, 100, 3), dtype=np.uint8)
    test_ts = 987654321.123
    ts_frame = TimestampedFrame(raw_frame, timestamp=test_ts)

    prep = FramePreprocessor(target_size=(50, 50))
    result = prep.process(ts_frame)

    assert isinstance(result, TimestampedFrame)
    assert result.timestamp == test_ts
