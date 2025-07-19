import os
import shutil
import argparse

# Define the video file extensions to look for
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.mpeg','.m4v','.mpg','.m4a','.asf','.webm'}

def is_video_file(filename):
    return os.path.splitext(filename)[1].lower() in VIDEO_EXTENSIONS

def copy_videos_preserve_structure(src_dir, tgt_dir):
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if is_video_file(file):
                src_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(src_file_path, src_dir)
                tgt_file_path = os.path.join(tgt_dir, relative_path)

                if not os.path.exists(tgt_file_path):
                    os.makedirs(os.path.dirname(tgt_file_path), exist_ok=True)
                    shutil.copy2(src_file_path, tgt_file_path)
                    print(f"Copied: {relative_path}")
                # else:
                #     print(f"Skipped (already exists): {relative_path}")

def main():
    parser = argparse.ArgumentParser(description='Copy video files from one directory to another, preserving structure.')
    parser.add_argument('source', help='Source directory path')
    parser.add_argument('target', help='Target directory path')
    parser.add_argument('--log', default='copy_videos.log', help='Log file path (default: copy_videos.log)')

    args = parser.parse_args()

    if not os.path.isdir(args.source):
        print(f"Error: Source directory does not exist: {args.source}")
        return

    os.makedirs(args.target, exist_ok=True)

    copy_videos_preserve_structure(args.source, args.target)

if __name__ == '__main__':
    main()
