# Handwriting Prediction Using SVM

This project is a simple handwriting recognition system using the Support Vector Machine (SVM) algorithm. The system consists of a machine learning model trained on a handwritten digit dataset and a Kivy-based graphical user interface (GUI) to facilitate prediction testing.

## Features

- **Model Training**: A Jupyter Notebook (`SVM.ipynb`) for loading the dataset, processing images, training the SVM model, and evaluating accuracy.
- **Interactive GUI**: A desktop application (`gui_kivy.py`) that allows users to select images and view the model's prediction results directly.
- **Visualization**: A clean interface with model accuracy statistics.

## Prerequisites

Before running this project, make sure you have the following Python libraries installed:

- Python 3.x
- Numpy
- Scikit-learn
- Pillow (PIL)
- Kivy
- Joblib
- Matplotlib (optional, for visualization in the notebook)

You can install them using pip:

```bash
pip install numpy scikit-learn pillow kivy joblib matplotlib
```

## How to Use

### 1. Model Training (Optional)

If you want to retrain the model or use your own dataset:

1. Open the `SVM.ipynb` file using Jupyter Notebook or a supported editor (such as VS Code).
2. Ensure your dataset is available and the path in the notebook matches the location of your dataset.
3. Run the cells in the notebook sequentially to train the model.
4. The trained model will be saved as `svm_model.pkl`.

### 2. Running the GUI Application

To use the prediction application:

1. Ensure the `svm_model.pkl` file is in the same directory as `gui_kivy.py`. (If it isn't there, run the training notebook first.)
2. Run the application with the command:

```bash
python gui_kivy.py
```

3. In the application interface:
- Click the **Select Image** button to upload a handwritten image (.png, .jpg, .jpeg format).
- The image will appear in the preview.
- Click the **Predict Now** button to view the number recognition results.

## File Structure

- `SVM.ipynb`: Notebook for data preprocessing and SVM model training.
- `gui_kivy.py`: The main script for the GUI application.
- `svm_model.pkl`: The trained SVM model file (generated after running the notebook).
- `UNPATTI logo.png`: Logo asset for the GUI application.

## Note

- This application is designed to accept image input in the form of handwritten numbers (0-9).
- For best results, use an image with a clean background and good contrast, similar to the MNIST dataset or the training data used.
