# Handwritten_Japanese_Recognition_System

This repository contains a Flask-based web application for recognizing handwritten Japanese characters from the KMNIST dataset. The project is currently in the **mock model phase**, which uses randomly generated predictions for demonstration purposes. The ultimate goal is to integrate a trained deep learning model for accurate recognition.

---

## Project Structure

```
Handwritten_Japanese_Recognition_System/
├── app.py                # Flask main application
├── static/               # Static files
│   ├── css/
│   │   ├── main.css      # Main page styles
│   │   └── result.css    # Result page styles
│   └── js/
│       ├── main.js       # Main page scripts
│       └── result.js     # Result page scripts
├── templates/            # HTML templates
│   ├── index.html        # Upload page
│   └── result.html       # Result display page
├── uploads/              # Directory for uploaded images
├── model_batch_16.pth    # Trained PyTorch model
├── README.md             # Model documentation
├── __init__.py
├── .gitignore          # Git ignore file
├── README.md           # Project documentation
└── requirements.txt    # Project dependencies

```

---

## Features

1. **Upload Handwritten Images**: Users can upload images of handwritten Japanese characters.
2. **Mock Model Predictions**: The app currently uses a mock model to simulate predictions.
3. **Dynamic Result Display**: After uploading an image, the app displays:
   - The predicted class (randomly chosen).
   - A confidence score (randomly generated between 80% and 100%).

---

## Setup Instructions

### 1. Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/KIWI0912/Handwritten_Japanese_Recognition_System.git
cd Handwritten_Japanese_Recognition_System
```

### 2. Set Up a Virtual Environment
Create and activate a virtual environment:
```bash
python3.11 -m venv myenv
source myenv/bin/activate
```

### 3. Install Dependencies
Install the required Python libraries:
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Ensure the `uploads/` directory exists (it will store uploaded images). Start the Flask development server:
```bash
python app.py
```

The app will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## How It Works (Mock Phase)

1. **Upload an Image**: Users upload an image file (`.png`, `.jpg`, or `.jpeg`).
2. **Preprocessing**:
   - The image is converted to grayscale.
   - Resized to 28x28 pixels (the KMNIST dataset format).
   - Normalized to have pixel values between 0 and 1.
3. **Mock Prediction**:
   - The app randomly selects one of the 10 KMNIST classes: `['お', 'き', 'す', 'つ', 'な', 'は', 'ま', 'や', 'れ', 'を']`.
   - Generates a random confidence score between 80% and 100%.
4. **Display Result**:
   - The uploaded image, predicted class, and confidence score are displayed on the result page.

---

## Future Work

1. **Integrate Trained Model**:
   - Replace the mock model with a trained KMNIST classification model.
   - Use TensorFlow/Keras for predictions.
2. **Enhance UI/UX**:
   - Improve the design of `index.html` and `result.html`.
   - Add real-time feedback for invalid file uploads.
3. **Add Unit Tests**:
   - Ensure the app works correctly with both mock and real models.
4. **Deploy the Application**:
   - Host the app on a cloud platform (e.g., Heroku, AWS, or Google Cloud).

---

## Dependencies

The required Python libraries are listed in `requirements.txt`:
- `Flask`: For building the web application.
- `Werkzeug`: For secure file uploads.
- `Pillow`: For image processing.
- `numpy`: For handling image arrays.

Install them using:
```bash
pip install -r requirements.txt
```

---


## Acknowledgments

- **KMNIST Dataset**: The dataset used for training the model.
- **Flask Framework**: For making web development simple and efficient.
- **Pillow Library**: For easy image processing.
