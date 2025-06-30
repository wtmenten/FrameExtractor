# FrameExtractor
Video Analyzer and Frame Extraction tool For AI Lora Generation

`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128`


ffmpeg command
`ffmpeg -i "E:\Videos\anime\spice and wolf\[Erai-raws] Ookami to Koushinryou - Merchant Meets the Wise Wolf - 08 [1080p][HEVC][Multiple Subtitle][FC033020].mkv" -vf "select='gt(scene,0.4)',showinfo" -vsync vfr -an -f null -`