# AI-Powered Vehicle Classification and Counting for Automated Toll Collection

This project is an AI-powered automated toll tax system that leverages cameras to detect, count, and classify vehicles in real-time. It automatically calculates toll taxes based on vehicle type and generates digital reports, aiming to replace manual, error-prone toll collection methods with an efficient, transparent, and automated solution.

## Features

- **Real-time Vehicle Detection and Classification:** Utilizes a YOLOv5 model to detect and classify vehicles from video streams into categories such as Car, Truck, Bus, etc.
- **Automated Toll Calculation:** Calculates toll tax automatically based on the classified vehicle type and predefined toll rates.
- **Admin Dashboard:** A web-based dashboard for administrators to view daily vehicle counts, total toll collections, and system status.
- **Dynamic Toll Rate Management:** Allows administrators to update toll rates for different vehicle categories.
- **Reporting:** Generates digital reports, eliminating the need for manual record-keeping.

## Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript, Tailwind CSS
- **AI/Computer Vision:** PyTorch, OpenCV, YOLOv5
- **Database:** SQLite (default, can be configured for others like PostgreSQL)

## System Architecture

The system follows a modular architecture:

1.  **Live Video Stream Handler:** Captures video footage from cameras.
2.  **AI Detection & Classification Engine:** Processes the video stream, detects and classifies vehicles using the YOLOv5 model.
3.  **Toll Calculation Module:** Calculates the toll based on the vehicle type.
4.  **Database Module:** Stores vehicle logs, toll data, and reports.
5.  **Web Dashboard:** A Django-based web interface for administrators.

## Setup and Installation

For detailed setup and installation instructions, please refer to the [Project Setup and Guide](setupGuide.md). The guide provides a comprehensive walkthrough for setting up the development environment, database, and all necessary dependencies.

## Usage

1.  **Admin Login:** Access the admin dashboard by navigating to the login page. Use the credentials for the admin user.
2.  **Toll Rates:** Navigate to the "Toll Rates" section to view and update the toll charges for each vehicle category.
3.  **Video Detection:** Go to the "Video Detection" page and upload a video file to see the vehicle detection and counting in action.
4.  **Reports:** View the generated reports for vehicle counts and toll collections.

## AI Model

The project uses a pre-trained YOLOv5 model (`Model.pt`) for object detection. This model is capable of identifying various vehicle types. The detection script is located in `apps/detections/services/ai.py`.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request
