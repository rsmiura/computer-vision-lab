# Computer Vision Lab

OpenCV experiments and notebooks for learning image processing.

## Setup

Use Python with desktop GUI support. In PowerShell, from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Image basics

Run the desktop display demo from the repository root:

```powershell
python notebooks/01-image-basics/display_image.py
```

Close the Matplotlib plot to continue. The first two OpenCV windows show for
eight seconds each; press any key in the third window and `q` in the last.

To explore the notebook with its bundled image assets:

```powershell
Set-Location notebooks/01-image-basics
jupyter notebook 01_Getting_Started_with_Images.ipynb
```
