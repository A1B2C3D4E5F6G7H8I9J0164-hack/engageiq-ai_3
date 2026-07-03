"""Unit tests for the WebcamCapture class."""

import time
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from src.pipeline.capture import TimestampedFrame, WebcamCapture


def test_capture_init_success():
    """Test successful initialization of WebcamCapture."""
    with patch("cv2.VideoCapture") as mock_video_capture:
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda prop: 640 if prop == 3 else 480
        mock_video_capture.return_value = mock_cap

        cap = WebcamCapture(source=0, fps=15, resolution=(640, 480))
        assert cap.source == 0
        assert cap.fps == 15
        assert cap.resolution == (640, 480)
        assert cap.cap is mock_cap

        # Verify context manager release
        with cap as c:
            assert c is cap
        mock_cap.release.assert_called_once()


def test_capture_init_failure():
    """Test exception raising when webcam source cannot be opened."""
    with patch("cv2.VideoCapture") as mock_video_capture:
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = False
        mock_video_capture.return_value = mock_cap

        with pytest.raises(RuntimeError, match="Failed to open video source"):
            WebcamCapture(source=99)


def test_capture_fps_stability():
    """Test that WebcamCapture regulates frames to match the target FPS."""
    with patch("cv2.VideoCapture") as mock_video_capture:
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        fake_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_cap.read.return_value = (True, fake_frame)
        mock_video_capture.return_value = mock_cap

        # Target FPS = 10 -> 1 frame every 0.1 seconds
        cap = WebcamCapture(source=0, fps=10)

        # Capture for 0.5 seconds
        start_time = time.time()
        frames = cap.capture(duration=0.5)
        elapsed = time.time() - start_time

        # At 10 FPS, 0.5 seconds should yield 5 frames
        # We allow a +/- 1 frame tolerance due to OS scheduler resolution
        assert len(frames) >= 4
        assert len(frames) <= 6
        assert elapsed >= 0.35  # At least ~0.4s must pass if timing works

        for frame in frames:
            assert isinstance(frame, TimestampedFrame)
            assert hasattr(frame, "timestamp")
            assert isinstance(frame.timestamp, float)

        cap.release()


def test_capture_one_and_stream():
    """Test capture_one and stream generator methods."""
    with patch("cv2.VideoCapture") as mock_video_capture:
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        fake_frame = np.ones((480, 640, 3), dtype=np.uint8) * 128
        mock_cap.read.return_value = (True, fake_frame)
        mock_video_capture.return_value = mock_cap

        cap = WebcamCapture(source=0, fps=30)

        # Test capture_one
        frame = cap.capture_one()
        assert frame is not None
        assert frame.shape == (480, 640, 3)
        assert isinstance(frame, TimestampedFrame)

        # Test stream with duration limit
        stream_frames = list(cap.stream(duration=0.1))
        assert len(stream_frames) > 0
        for f in stream_frames:
            assert f.shape == (480, 640, 3)

        cap.release()
