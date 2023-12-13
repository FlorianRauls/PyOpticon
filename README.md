The "PyOpticon" project is a work-in-progress Python project with a data pipeline focusing on the collection, storage, and potential analysis of process, hardware, and network data. Here's a structured README for the project:

---

# PyOpticon Project

## Overview
The PyOpticon project is designed to monitor and analyze system performance and network data. It aims to provide insights into system processes, hardware efficiency, and network utilization.
I created this in my spare time to see why my PC is lagging sometimes. So do not take it too seriously (or maybe do 😉).

## Features
Currently, the project includes the following features:
1. **Docker Container Initialization**: Leveraging Docker to create isolated environments for data collection.
2. **Data Collection**: Gathering data related to system processes, hardware performance, and network statistics.
3. **Data Storage**: Utilizing MySQL for efficient data storage and retrieval.

## Technologies Used
- **Python**: The core programming language for the project.
- **Docker**: For creating and managing containerized environments.
- **MySQL**: Database management system for storing collected data.

## Project Structure
The project contains the following main components:
- `compose.yaml`: Docker compose file for setting up the environment.
- `src/`: Source directory containing the core code.
  - `db/`: Contains Dockerfile for the database setup.
  - `tracker/`: Includes the application logic for data collection (`app.py`) and database configuration (`db.yaml`).

## Usage
To use PyOpticon, ensure Docker and Python are installed on your system. Then, you can start the Docker container defined in `compose.yaml` to initiate the data collection process.

## Work in Progress
The following features and improvements are currently under development:
- **Data Cleaning**: Implementing procedures to clean and preprocess the collected data for analysis.
- **Data Visualization and Pattern Discovery**: Developing tools and methods for visualizing the collected data and uncovering meaningful patterns and insights.

## Contribution
Contributions to the project are welcome. Please follow standard practices for code contributions, including feature branching and pull requests.

## License
MIT-License
