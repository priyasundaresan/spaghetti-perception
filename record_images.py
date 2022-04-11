import pyrealsense2 as rs
import numpy as np
import cv2
import math
import matplotlib.pyplot as plt
import os

try:
    import cPickle as pickle
except ImportError:
    import pickle

class ImgRecorder():
    def __init__(self, out_dir):
        self.out_dir = out_dir
        if not os.path.exists(self.out_dir):
            os.mkdir(self.out_dir)

        self.img_idx = 0

        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

        self.align_to_color = rs.align(rs.stream.color)

        # Start streaming
        self.pipe_profile = self.pipeline.start(self.config)

        # Intrinsics & Extrinsics
        frames = self.pipeline.wait_for_frames()
        frames = self.align_to_color.process(frames)
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        self.depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
        self.color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
        self.depth_to_color_extrin = depth_frame.profile.get_extrinsics_to(color_frame.profile)
        self.colorizer = rs.colorizer()

    def take_image(self):
        color_frame = None
        while color_frame is None:
            frames = self.pipeline.wait_for_frames()
            frames = self.align_to_color.process(frames)
            color_frame = frames.get_color_frame()
        color_frame = np.asanyarray(color_frame.get_data())
        color_frame_preview = cv2.resize(color_frame, (640,360))
        cv2.imshow('img', color_frame_preview)
        cv2.waitKey(100)
        cv2.imwrite(os.path.join(self.out_dir, '%05d.jpg'%self.img_idx), color_frame)
        self.img_idx += 1

    def record_seq(self, max_num_images):
        while self.img_idx < max_num_images:
            ans = input('Take image %d?:'%(self.img_idx))
            if ans == 'n':
                break
            else:
                self.take_image()

if __name__ == '__main__':
    recorder = ImgRecorder('output')
    #recorder.take_image()
    recorder.record_seq(50)
