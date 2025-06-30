# FrameExtractor

Video analyzer and frame selection tools. 
built to aid GenAI LoRA dataset selection and annotation process, but could be used for any purpose.

### Usage

#### CLI
the cli tool `cli.py` can be used to execute the analyzer and collator modules.

* `-i` - sets up the analyzer interactively (prompts the user for the job id `-j` and threshold `-t`)
* `-c` - runs the collator GUI which then prompt the user to open a video_frame_analysis.xlsx workbook
* `-o` - custom output directory path
* `-v` - list of video paths to skip the interactive selector, or if they are in various folders.


### Details

#### Analyzer
The analyzer processes each video sequentially in three stages.
1. Passes the video through `scenedetect` to get scene boundaries.
2. Saves first-middle-last frames from each scene to the job output folder
3. Runs CausalLM inference with `MiaoshouAI/Florence-2-large-PromptGen-v2.0` on the scenes mid-frame to generate a scene description.

*NOTE:*

The Analyzer process can save well over 1000 high-quality (95) jpg images per standard (25m) length episode. It's up to the user to clear out the job folder when you're done with the raw Analyzer outputs.

The Collator save the selected Frame Data within a new workbook so all other job data can safely be deleted.

Tested on a laptop i9 and under-volted RTX 3080, The Analyzer takes roughly 15 minutes for each 25-minute video - 60% of which is the scene description stage. 
The Image-To-Text inference uses ~ 8GB of VRAM with the florence2-large finetune model. A smaller prompt-gen model could be used on more constrained GPU's
#### Collator
The Collator GUI processes the raw `video_frame_analysis.xlsx` workbooks created by the analyzer allowing the user to cherry-pick scenes, the best frame in scene and adjust the description.
The selected frames and descriptions are then saved in a new workbook which can then been used for lora training or whatever else.

The Collator has a number of keyboard shortcuts to expedite the selection and editing process:

* ``` ` ```, `~`, and `shift+enter` for skip, undo, and keep frame actions
* `Tab` for toggling focus on the description field
* 1-9 for selecting the desired scene image (when not focused on the description)

When finished with the current workbook, the collator will wait for you to select a final action from the topbar.

* `Load` - continue processing by selecting another workbook
* `Finish` - complete the job, saving the selected frames workbook
* `Exit` - close without saving 

#### CLI Output Example With Timings
```commandline
2025_06_30_16:47:50: Starting job_000
2025_06_30_16:47:50: Starting Video 1
Detected: 356 | Progress: 100%|█████████▉| 34286/34293 [03:49<00:00, 149.46frames/s]
100%|██████████| 1071/1071 [02:07<00:00,  8.42images/s]
Describing Scenes: 100%|██████████| 357/357 [10:06<00:00,  1.70s/scene]
2025_06_30_17:04:02: Done
```

#### Installation 

##### requirements
install the general requirements from `requirments.txt`
then install torch with the cuda binary for your cuda version. 

example for cuda 12.8:
`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128`

#### Troubleshooting
if you are getting warnings from transformers about outdated/deprecated models lacking the GenerativeMixin
you will need to downgrade transformers beneath `4.50.0` or patch the model in question.
