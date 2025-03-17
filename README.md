# <span style="font-size:30px;">STEVE-R1: Towards Long Reasoning Computer-use Agents</span>

<a href='#'><img src='https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Paper-orange'></a>
<a href='https://huggingface.co/Fanbin/STEVE-R1-7B-SFT'><img src='https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Models-blue'></a>
<a href='https://huggingface.co/datasets/Fanbin/waa_steve_trajectories'><img src='https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Data-green'></a>
<!-- <a href='https://huggingface.co/collections/zszhong/lyra-evaluation-'><img src='https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Evaluation-yellow'></a><br> -->


We evaluate the performance of the STEVE-R1 agent on both in-domain (Windows 11 OS) and out-of-domain (Ubuntu OS) scenarios. The evaluation involved 16 attempts per task, with task completion rates recorded as the primary metric. In the in-domain Windows 11 setting, the STEVE-R1 agent demonstrated a 14% higher task completion rate compared to the previous open-source state-of-the-art model, UI-TARS-7B-DPO. Furthermore, in the out-of-domain Ubuntu OS environment, where STEVE-R1 was not explicitly trained, it still achieved a 7% higher task completion rate than UI-TARS-7B-DPO.

<div align=center>
<img width="98%" src="assets/performance.svg"/>
</div>

## Release
- Currently only the step-verified 
- 🔥 An improved version <b>STEVE-R1<b> is released with long reasoning ability and long image context. We extend the model context length to <b>128K</b> with at most <b>32 screenshot</b> inputs for a single task. The model response length is greatly improved with deepseek-R1 distillation, see the [examples](https://github.com/FanbinLu/STEVE-R1/tree/main/examples). We release the [training data](), [models](https://huggingface.co/Fanbin/STEVE-R1-7B-SFT), and [evaluation trajectories](https://huggingface.co/datasets/Fanbin/waa_steve_trajectories).
- We release the paper of STEVE: Step Verification Pipeline for Computer-use Agent Training. We propose a single-frame computer-use 7B agent trained with SFT & step-verified KTO. 


## Trajectory Data
We provide some example trajectories of STEVE-R1 on OSWorld in examples/. Please check the [full trajectories](https://huggingface.co/datasets/Fanbin/waa_steve_trajectories) for more results.

A quick preview of the reasoning agent's response:
User task: I've stored my .xcf file on the Desktop. Can you assist me in copying the image and pasting it into a LibreOffice Writer document? Save the document as 'image.docx' on the Desktop, please. (OSWorld/multi_apps/227d2f97-562b-4ccb-ae47-a5ec9e142fbb)
````model outputs
<|begin_of_thought|>
Since it is the first step of the task, I will first think thoroughly about the task.

Okay, let me try to figure out how to help the user copy their .xcf file from the Desktop into a LibreOffice Writer document and save it as 'image.docx' on the Desktop.

First, the user wants to work with an .xcf file, which is an image file format that's often used in software like GIMP. But since they need to paste it into a LibreOffice Writer document, they'll need to convert it to a format that Writer can open, like JPEG or PNG. Because .xcf files aren't natively supported by LibreOffice. So step one might involve opening GIMP or another image editor to convert the .xcf file to a more common format.

Once converted, they need to open LibreOffice Writer. The current desktop has LibreOffice Writer listed in the taskbar, so that's easy. Then, they can create a new document. Pasting the converted image into the document is straightforward by using Ctrl+V or right-clicking and selecting paste. But when pasting into a text document like Writer, pasting as image would be necessary instead of just text. Alternatively, they might need to insert an image using the Insert menu if that's available.

After pasting, saving the document as 'image.docx' on the Desktop requires navigating to the correct save location. They might have to ensure that when saving, they select the Desktop and name it correctly. Since there's already a Home shortcut on the desktop, maybe they can use that to quickly access the Desktop directory when saving.

Potential issues: If the .xcf file isn't accessible from GIMP or another program, converting it first is crucial. Also, making sure that after pasting into Writer, they save properly without overwriting any existing files. I should check if there are alternative methods, like using some third-party software for conversion, but since it's not specified, sticking with standard tools like GIMP and LibreOffice seems best.

Here is the final step-by-step solution.

**TODO Steps:**

1. **Convert the .xcf file to a compatible format (e.g., JPEG/PNG) using GIMP:**
   - Open **GIMP** (double-click its icon on the desktop).
   - In GIMP:  
     - Open your `.xcf` file (`File → Open → Browse → Select your .xcf file`).
     - Go to **File → Export As**, choose `JPEG/PNG` format.
     - Save as `image.jpg` (or similar) on your desktop.

2. **Open LibreOffice Writer:**
   - Click on **LibreOffice Writer** in the taskbar (icon looks like an "A").

3. **Create a new document:**
   - Press `Ctrl + N` or go to `File → New → Text Document`.

4. **Paste the converted image into LibreOffice Writer:**
   - Press `Ctrl + V` (or right-click → Paste) to paste `image.jpg` into your new document.

5. **Save as 'image.docx' on your desktop:**
   - Go to `File → Save As...`.  
   - In the save dialog:  
     1️⃣ Navigate to your desktop (use "Home" shortcut if needed).  
     2️⃣ Name the file `image.docx`.  
     3️⃣ Ensure "Save as type" is set to `Microsoft Word Document (*.docx)`.

**Why this works:**  
- Converting `.xcf` files via GIMP is necessary because LibreOffice doesn’t support native .xcf files.  
- Using `Save As` directly ensures no accidental overwrite of existing files.<|end_of_thought|>
<|begin_of_solution|>
```thoughts
The task involves copying a .xcf file from the desktop into a LibreOffice Writer document and saving it as 'image.docx'. Since .xcf files aren't natively supported by LibreOffice Writer, we need to convert them first using GIMP. The initial step is accessing GIMP from its icon on the desktop.
```

```rationale
We need to open GIMP in order to convert any .xcf files that may be present from the desktop before proceeding with pasting them into a document.
```

```decision
COMMAND
```
```python
computer.mouse.move("<|object_ref_start|>GIMP icon on the desktop<|object_ref_end|><|point_start|>(19,475)<|point_end|>") # Move mouse pointer towards GIMP icon
computer.mouse.double_click() # Open GIMP
```
<|end_of_solution|>
````


## Execution Length
We compare models' performance across different execution lengths. A RESET action is triggered to reset the environment if the model fails to complete the task within 20 steps. The accuracy of the task is only measure when the agent outputs DONE/FAIL/CALL_USER or the maximum execution length is reached. We show that a 5% accuracy improvement in STEVE-R1 by increasing the execution length per attempt.

| Method |  WinAgentArena | OSWorld |
|--------|-------------------|------------------|
| UI-TARS-7B-DPO (20 steps) | 15.4 ± 1.6 | 14.6 ± 1.0 |
| UI-TARS-7B-DPO (40 steps) | 17.8 ± 1.3 | 15.7 ± 0.8 |
| UI-TARS-7B-DPO (60 steps) | 19.3 ± 1.6 | 16.2 ± 1.0 |
| **Our Model**  | | |
| STEVE-R1-SFT (20 steps) | 17.5 ± 2.0 | 9.6 ± 1.1（OOD）|
| STEVE-R1-SFT (40 steps) | 20.1 ± 2.2 | 11.5 ± 1.2 (OOD) |
| STEVE-R1-SFT (60 steps) | 22.3 ± 2.1 | 12.8 ± 1.2 (OOD) |

## RUN
Please follow the installation guide of OSWorld and WindowsAgentArena.
```bash
nohup bash ./start_server.sh &
cd OSWorld;
python run_multienv_cot_qwen2vl.py --headless --observation_type screenshot --max_steps 20 --max_trajectory_length 20 --temperature 0.6 --model cot_qwen2vl --action_space pyautogui --num_envs 7 --result_dir ./results/ --trial-id 15 
```
For WindowsAgentArena,
```bash
nohup bash ./start_server.sh &
cd WindowsAgentArena/scripts;
bash start_multienv_steve_evaluation.sh;
```
