# Searchch - Template Matching Application

Searchch is an advanced image processing application that uses template matching for object detection in real-time video streams. This project demonstrates the power of computer vision techniques in practical applications.

## Features

- Real-time object detection using template matching
- User-friendly GUI built with PyQt5
- Template capture functionality
- Adjustable match threshold
- Multi-scale detection support
- Multiple object detection capability

## Requirements

- Python 3.7+
- OpenCV
- PyQt5
- NumPy

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/searchch.git
   cd searchch
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the main application:
   ```
   python main.py
   ```

2. The main window will appear. Follow these steps to use the application:

   a. Click "Capture Template" to select an object of interest from the camera feed.
   b. In the template capture window, click and drag to draw a rectangle around the object.
   c. Click "Start Detection" to begin real-time object detection.
   d. Adjust the match threshold slider if needed.
   e. Click "Stop" to end the detection process.

3. Use the "Help" button for additional guidance on using the application.

## Project Structure

- `main.py`: Entry point of the application
- `config.py`: Configuration settings
- `camera_feed.py`: Handles camera input
- `object_detection.py`: Contains object detection algorithms
- `visualization.py`: Handles result visualization
- `utils.py`: Utility functions
- `gui/`: Contains GUI-related files
  - `main_window.py`: Main application window
  - `result_display_widget.py`: Widget for displaying detection results
  - `template_capture_dialog.py`: Dialog for template capture

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
