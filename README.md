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

#### Installation 

##### requirements
install the general requirements from `requirments.txt`
then install torch with the cuda binary for your cuda version. 

example for cuda 12.8:
`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128`

#### Troubleshooting
if you are getting warnings from transformers about outdated/deprecated models lacking the GenerativeMixin
you will need to downgrade transformers beneath `4.50.0` or patch the model in question.
