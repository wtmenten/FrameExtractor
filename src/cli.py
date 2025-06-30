import argparse
import datetime
from pathlib import Path
import os
import sys

ROOT_DIR = Path(os.path.abspath(__file__)).parent.parent.absolute()
sys.path.append(ROOT_DIR)

from analyzer import FrameAnalyzer

import utils
import collator

DEFAULT_OUTPUT_DIR = os.path.join(ROOT_DIR, "output")



def main():
    parser = argparse.ArgumentParser(
        description="Run a video processing job with a threshold and video inputs."
    )

    parser.add_argument("-v", "--video_paths", nargs='+', type=str, help="List of video file paths")
    parser.add_argument("-j", "--job_id", type=str, help="Unique job ID string")
    parser.add_argument("-t", "--threshold", type=float, help="Threshold for processing")
    parser.add_argument("-i", "--interactive", help="Interactive CLI", action='store_true', default=False)
    parser.add_argument("-o", "--output_dir", type=str, help="Absolute path to root outputs directory", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("-c", "--collate", help="Run the collation utility GUI after frame extraction", action='store_true', default=False)

    args = parser.parse_args()
    analyzer = FrameAnalyzer()
    if args.interactive:
        if args.job_id is None or args.job_id == "":
            args.job_id = input("Job ID: ")
        if args.job_id == "":
            args.job_id = None
        THRESHOLD_DEFAULT = analyzer.threshold
        if args.threshold is None:
            args.threshold = input(f"Threshold({THRESHOLD_DEFAULT}): ")
            if args.threshold.strip() == "":
                args.threshold = THRESHOLD_DEFAULT
            else:
                args.threshold = float(args.threshold)
        if args.video_paths is None or len(args.video_paths) == 0:
            args.video_paths = utils.select_file()
    
    if len(args.video_paths) == 0: 
        print("No videos selected. Exiting...")
        exit(0)
        
    job_dir = utils.get_job_dir(args.output_dir, desc=args.job_id)
    print("{d}: Starting {j}".format(d=datetime.datetime.now().strftime("%Y_%m_%d_%H:%M:%S"), j=os.path.basename(job_dir)))
    analyzer = FrameAnalyzer(threshold=args.threshold, output_dir=job_dir)
    analyzer.analyze(args.video_paths)

    if args.collate:
        collator.main(output_dir=job_dir)

if __name__ == "__main__":
    main()
