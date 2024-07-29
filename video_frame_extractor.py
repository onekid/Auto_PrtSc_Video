import cv2
import os
from tqdm import tqdm
import argparse


def capture_screenshots_from_videos(source_folder, target_folder, frame_frequency=80):
    global_counter = 1  # 初始化全局计数器
    # 遍历文件夹及其子文件夹中的所有视频文件
    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                video_file_path = os.path.join(root, file)
                global_counter = process_video_file(video_file_path, target_folder, frame_frequency, global_counter)


def process_video_file(video_file_path, target_folder, frame_frequency, counter):
    cap = cv2.VideoCapture(video_file_path)
    isOpened = cap.isOpened()  # 判断是否打开
    if not isOpened:
        print(f"Failed to open video file: {video_file_path}")
        return counter

    # 获取视频信息
    n_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)  # 帧率
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 宽
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 高

    print(f'Processing {video_file_path}: 帧数={n_frame}, 宽={width}, 高={height}, 帧率={fps}')

    # 创建输出文件夹
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    i = 0  # 记录读取多少帧

    # 创建进度条
    with tqdm(total=n_frame, desc=f"Processing {os.path.basename(video_file_path)}", unit="frame") as pbar:
        while isOpened:
            # 结束标志是否读取到最后一帧
            if i == n_frame:
                break
            else:
                i += 1

            flag, frame = cap.read()  # 读取每一帧

            if flag:
                if i % frame_frequency == 0:
                    file_name = f'{counter:06d}.jpg'  # 名字累加
                    cv2.imwrite(os.path.join(target_folder, file_name), frame,
                                [cv2.IMWRITE_JPEG_QUALITY, 100])  # 质量控制 100最高
                    counter += 1

            # 更新进度条
            pbar.update(1)

    print(f'Finished processing {video_file_path}')
    cap.release()
    return counter


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from videos in a folder")
    parser.add_argument('source_folder', type=str, help='Path to the source folder containing videos')
    parser.add_argument('target_folder', type=str, help='Path to the target folder to save extracted frames')
    parser.add_argument('--frame_frequency', type=int, default=80, help='Frequency of frames to extract')

    args = parser.parse_args()

    source_folder = args.source_folder
    target_folder = args.target_folder
    frame_frequency = args.frame_frequency

    capture_screenshots_from_videos(source_folder, target_folder, frame_frequency)
