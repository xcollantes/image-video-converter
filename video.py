import argparse
import os
import subprocess

from moviepy.editor import VideoFileClip


def check_gpu_availability():
    """Check if ffmpeg is compiled with GPU support"""
    try:
        # Run ffmpeg -version and capture output
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        output = result.stdout.lower()

        # Check for common GPU support indicators
        gpu_supports = {
            "nvidia": "cuda" in output or "nvenc" in output,
            "amd": "amf" in output or "opencl" in output,
            "intel": "qsv" in output,
        }

        return gpu_supports
    except Exception:
        return None


def convert_to_gif(input_path, output_path=None, fps=10, resize_factor=1.0):
    """
    Convert MP4 video to GIF format

    Args:
        input_path (str): Path to input MP4 file
        output_path (str): Path for output GIF file (optional)
        fps (int): Frames per second for output GIF
        resize_factor (float): Factor to resize the video (1.0 = original size)
    """
    try:
        # If no output path specified, create one based on input filename
        if output_path is None:
            output_path = os.path.splitext(input_path)[0] + ".gif"

        # Load the video file
        video = VideoFileClip(input_path)

        # Resize if needed
        if resize_factor != 1.0:
            video = video.resize(resize_factor)

        # Check if GPU support is available
        gpu_supports = check_gpu_availability()
        if gpu_supports and any(gpu_supports.values()):
            # Convert to GIF with GPU support
            print(f"Converting {input_path} to GIF with GPU support...")
            video.write_gif(
                output_path,
                fps=fps,
                verbose=False,
                logger=None,
                writeLogfile=False,
                ffmpeg_params=[
                    "-hwaccel_device",
                    "0",
                    "-hwaccel_output_format",
                    "cuda",
                ],
            )
        else:
            # Convert to GIF without GPU support
            print(f"Converting {input_path} to GIF...")
            video.write_gif(output_path, fps=fps)

        print(f"Successfully created GIF: {output_path}")

        # Close the video to free up resources
        video.close()

    except Exception as e:
        print(f"Error converting video: {str(e)}")
        if "video" in locals():
            video.close()


def main():
    # Set up command line argument parser
    parser = argparse.ArgumentParser(description="Convert MP4 video to GIF")
    parser.add_argument("input", help="Input MP4 file path")
    parser.add_argument("-o", "--output", help="Output GIF file path")
    parser.add_argument(
        "-f",
        "--fps",
        type=int,
        default=10,
        help="Frames per second for output GIF (default: 10)",
    )
    parser.add_argument(
        "-r",
        "--resize",
        type=float,
        default=1.0,
        help="Resize factor (default: 1.0, no resize)",
    )

    args = parser.parse_args()

    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist")
        return

    # Convert the video
    convert_to_gif(args.input, args.output, args.fps, args.resize)


if __name__ == "__main__":
    main()
