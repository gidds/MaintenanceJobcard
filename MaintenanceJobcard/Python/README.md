# Maintenance Tracker

Maintenance Tracker is a Python-based desktop application for managing maintenance job cards in industrial or manufacturing settings. It provides an easy-to-use interface for creating, saving, and searching job cards.

## Features

- Create and save maintenance job cards
- Search for existing job cards by requisition number or job card number
- Automatic calculation of time spent on each job
- Date picker for easy date selection
- Time selectors for precise time input
- Configurable job cards data file location
- Simple and intuitive user interface

## Requirements

- Python 3.6 or higher
- tkinter (usually comes pre-installed with Python)
- tkcalendar

## Installation

1. Clone this repository or download the source code.
2. Navigate to the project directory.
3. Install the required packages:


## Usage

1. Run the application:


2. On first run, you'll be prompted to select or create an XML file to store job cards data.
3. Use the "Create Jobcard" tab to input and save new job cards.
4. Use the "Search Jobcard" tab to find and view existing job cards.

## Application Structure

- `maintenance_tracker.py`: Main application file
- `config.ini`: Configuration file storing the path to the job cards XML file
- `README.md`: This file, containing information about the project

## Contributing

Contributions to improve Maintenance Tracker are welcome. Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any problems or have any questions, please open an issue in the GitHub repository.
