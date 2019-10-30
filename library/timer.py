from pygame import time


class Timer:
    """Helper class that provides images at any given time."""

    def __init__(self, frames, wait=100, frame_index=0, step=1, loop_once=False):
        self.frames = frames
        self.wait = wait
        self.frame_index = frame_index
        self.step = step
        self.loop_once = loop_once
        self.finished = False
        self.last_frame = len(frames) - 1 if step == 1 else 0
        self.last = None

    def _get_frame_index(self):
        now = time.get_ticks()
        if self.last is None:
            self.last = now
            self.frame_index = 0 if self.step == 1 else len(self.frames) - 1
            return 0
        elif not self.finished and now - self.last > self.wait:
            self.frame_index += self.step
            if self.loop_once and self.frame_index == self.last_frame:
                self.finished = True
            else:
                self.frame_index %= len(self.frames)
            self.last = now
        return self.frame_index

    def reset(self):
        self.last = None
        self.finished = False

    def get_image(self):
        return self.frames[self._get_frame_index()]
