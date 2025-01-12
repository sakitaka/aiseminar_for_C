# Garbage Sorting Device

This repository contains the source code for a garbage sorting device designed to separate cans and PET bottles automatically. The device utilizes a Jetson module and Keigan motor for its operation, with a camera connected to the Jetson to identify the type of garbage and sort it accordingly.

## Features
- Real-time object recognition to classify cans and PET bottles.
- Automatic sorting mechanism using a Keigan motor.
- Easy model training and testing with provided scripts.

## System Requirements
- **Jetson Module**: Tested on Jetson nano.
- **Camera**: Any compatible USB or CSI camera.
- **Motor**: Keigan motor for sorting mechanism.
- **Python Version**: 3.8 or later.
[](
## Installation\
1. Clone this repository:\
   ```bash\
   git clone https://github.com/sakitaka/aiseminar_for_C.git\
   cd garbage-sorting-device\
   ```\
\
2. Install dependencies:\
   ```bash\
   pip install -r requirements.txt\
   ```\
\
3. Set up your Jetson environment according to [NVIDIA's official guide](https://developer.nvidia.com/embedded).\
)
## Workflow

### 1. Model Training (`learn.py`)
Use `learn.py` to train a model for classifying cans and PET bottles:
1. Prepare your dataset with the following structure:
   ```
   data/
   ├── train/
   │   ├── can/
   │   └── pet/
   └── val/
       ├── can/
       └── pet/
   ```
2. Run the training script:
   ```bash
   python learn.py
   ```
3. The trained model weights will be saved as `model_weight_res.pth`.

### 2. Device Operation (`demo2.py`)
Use `demo2.py` to run the sorting device:
1. Ensure the trained model (`model_weight.pth`) is available in the working directory.
2. Connect the camera and Keigan motors to the Jetson.
3. Start the program:
   ```bash
   python demo2.py
   ```
4. Follow the on-screen instructions to classify and sort garbage.

## Directory Structure
```
.
├── learn.py           # Script for training the model
├── demo2.py           # Main script to run the device
├── models/            # Pre-trained models for object recognition
├── utils/             # Helper functions and utilities
├── data/              # Directory for training and validation data
└── README.md          # Project documentation
```

## Notes
- Ensure the Keigan motor is calibrated before use.
- Use `learn.py` to retrain the model if necessary.



---

For any issues or feature requests, please open an issue on this repository.

