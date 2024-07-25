import cv2
import os

def extract_frames(video_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Extract frames
    frame_number = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Save frame as an image
        frame_filename = os.path.join(output_folder, f"frame_{frame_number:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
        frame_number += 1

    # Release the video object
    video.release()
    print(f"Frames extracted: {frame_number}")

# Example usage
video_path = 'no_detection.mp4'  # Replace with your video file path
output_folder = 'no_detection'  # Replace with your desired output folder
extract_frames(video_path, output_folder)
