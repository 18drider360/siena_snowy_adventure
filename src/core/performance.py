"""
Performance Profiler
Tools for measuring and optimizing game performance
"""

import time
import pygame
from collections import deque


class PerformanceMonitor:
    """Monitors game performance metrics"""

    def __init__(self, sample_size=60):
        """
        Initialize performance monitor

        Args:
            sample_size: Number of frames to average over
        """
        self.sample_size = sample_size
        self.frame_times = deque(maxlen=sample_size)
        self.update_times = deque(maxlen=sample_size)
        self.render_times = deque(maxlen=sample_size)

        self.frame_start = 0
        self.update_start = 0
        self.render_start = 0

        self.enabled = False

    def start_frame(self):
        """Mark the start of a frame"""
        if self.enabled:
            self.frame_start = time.perf_counter()

    def start_update(self):
        """Mark the start of update phase"""
        if self.enabled:
            self.update_start = time.perf_counter()

    def end_update(self):
        """Mark the end of update phase"""
        if self.enabled:
            update_time = (time.perf_counter() - self.update_start) * 1000  # Convert to ms
            self.update_times.append(update_time)

    def start_render(self):
        """Mark the start of render phase"""
        if self.enabled:
            self.render_start = time.perf_counter()

    def end_render(self):
        """Mark the end of render phase"""
        if self.enabled:
            render_time = (time.perf_counter() - self.render_start) * 1000
            self.render_times.append(render_time)

    def end_frame(self):
        """Mark the end of a frame"""
        if self.enabled:
            frame_time = (time.perf_counter() - self.frame_start) * 1000
            self.frame_times.append(frame_time)

    def get_avg_fps(self):
        """Get average FPS over sample period"""
        if not self.frame_times:
            return 0
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        return 1000 / avg_frame_time if avg_frame_time > 0 else 0

    def get_avg_frame_time(self):
        """Get average frame time in milliseconds"""
        if not self.frame_times:
            return 0
        return sum(self.frame_times) / len(self.frame_times)

    def get_avg_update_time(self):
        """Get average update time in milliseconds"""
        if not self.update_times:
            return 0
        return sum(self.update_times) / len(self.update_times)

    def get_avg_render_time(self):
        """Get average render time in milliseconds"""
        if not self.render_times:
            return 0
        return sum(self.render_times) / len(self.render_times)

    def get_min_fps(self):
        """Get minimum FPS (worst frame)"""
        if not self.frame_times:
            return 0
        max_frame_time = max(self.frame_times)
        return 1000 / max_frame_time if max_frame_time > 0 else 0

    def get_performance_report(self):
        """Get a formatted performance report"""
        if not self.enabled:
            return "Performance monitoring is disabled"

        report = f"""
=== PERFORMANCE REPORT ===
Average FPS:        {self.get_avg_fps():.1f}
Minimum FPS:        {self.get_min_fps():.1f}
Avg Frame Time:     {self.get_avg_frame_time():.2f}ms
Avg Update Time:    {self.get_avg_update_time():.2f}ms
Avg Render Time:    {self.get_avg_render_time():.2f}ms
Sample Size:        {len(self.frame_times)} frames
==========================
"""
        return report

    def draw_overlay(self, screen, x=10, y=10):
        """
        Draw performance overlay on screen

        Args:
            screen: Pygame surface to draw on
            x, y: Position for overlay
        """
        if not self.enabled:
            return

        try:
            font = pygame.font.Font(None, 24)
        except:
            return

        # Performance text
        fps_text = f"FPS: {self.get_avg_fps():.1f}"
        frame_text = f"Frame: {self.get_avg_frame_time():.1f}ms"
        update_text = f"Update: {self.get_avg_update_time():.1f}ms"
        render_text = f"Render: {self.get_avg_render_time():.1f}ms"

        # Background box
        box_height = 100
        box_width = 200
        background = pygame.Surface((box_width, box_height))
        background.set_alpha(128)
        background.fill((0, 0, 0))
        screen.blit(background, (x, y))

        # Draw text
        y_offset = y + 10
        for text in [fps_text, frame_text, update_text, render_text]:
            # Determine color based on performance
            if "FPS" in text:
                fps_value = self.get_avg_fps()
                color = (0, 255, 0) if fps_value >= 55 else (255, 255, 0) if fps_value >= 30 else (255, 0, 0)
            else:
                color = (255, 255, 255)

            surface = font.render(text, True, color)
            screen.blit(surface, (x + 10, y_offset))
            y_offset += 22


class Timer:
    """Simple timer for profiling code sections"""

    def __init__(self, name="Timer"):
        """Initialize timer with a name"""
        self.name = name
        self.start_time = None
        self.elapsed = 0

    def __enter__(self):
        """Start timing when entering context"""
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, *args):
        """Stop timing when exiting context"""
        self.elapsed = (time.perf_counter() - self.start_time) * 1000
        print(f"{self.name}: {self.elapsed:.2f}ms")

    def start(self):
        """Manually start timer"""
        self.start_time = time.perf_counter()

    def stop(self):
        """Manually stop timer and print result"""
        if self.start_time:
            self.elapsed = (time.perf_counter() - self.start_time) * 1000
            print(f"{self.name}: {self.elapsed:.2f}ms")
            return self.elapsed
        return 0


def profile_function(func):
    """
    Decorator to profile a function

    Usage:
        @profile_function
        def my_function():
            # code here
    """
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{func.__name__}() took {elapsed:.2f}ms")
        return result
    return wrapper


# Example usage
if __name__ == '__main__':
    print("Performance Monitor Demo\n")

    # Create monitor
    monitor = PerformanceMonitor(sample_size=10)
    monitor.enabled = True

    # Simulate 10 frames
    for i in range(10):
        monitor.start_frame()

        # Simulate update
        monitor.start_update()
        time.sleep(0.005)  # 5ms
        monitor.end_update()

        # Simulate render
        monitor.start_render()
        time.sleep(0.010)  # 10ms
        monitor.end_render()

        monitor.end_frame()

        # Add some variation
        time.sleep(0.001 * i)

    # Print report
    print(monitor.get_performance_report())

    # Test timer
    print("\nTesting Timer:")
    with Timer("Test Operation"):
        time.sleep(0.05)

    # Test function profiling
    @profile_function
    def slow_function():
        time.sleep(0.02)
        return "done"

    print("\nTesting Function Profiler:")
    slow_function()
