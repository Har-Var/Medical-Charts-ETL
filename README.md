
# NCERT Books Downloader

## Description  
NCERT Books Downloader is a project designed to simplify and improve the process of downloading NCERT books by offering a user-friendly Graphical User Interface (GUI). While the official NCERT [Download Page](https://ncert.nic.in/textbook.php) allows users to select and download books, it provides them in a Zip format with separate files for each chapter, index, and cover page. This application consolidates all these files into a single, easily accessible PDF format, streamlining the download experience.


## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Har-Var/NCERT-Books-Downloader.git
   cd NCERT-Books-Downloader
   ```
2. Ensure you have Python 3.x installed.
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. If there are residual files in the `data/` folder. Run the following cleanup script.
   ```bash
   python run_cleanup.py
   ```
5. Run the scraper script to generate resource file
   ```bash
   python run_scraper.py
   ```

## Usage
Run the CLI App with:
```bash
python run_cli_app.py
```

Run the GUI App with:
```bash
python run_gui_app.py
```

## Features
- Provides an improved User Interface to download NCERT Books.
- Contains both - a Graphical User Interface App and a Command Line App.
- Improves upon the official download page by further processing downloaded Zips and transforming them into consolidated PDF Books.

## Project Structure
The project is organized into the following folders:

* `src`: Contains the source code for the project.
	+ `downloader`: Contains the code for the book downloader.
		- `downloader_funcs.py`: Contains utility functions for downloading books.
		- `gui_downloader.py`: Contains the code for the graphical user interface (GUI) version of the downloader.
		- `cli_downloader.py`: Contains the code for the command-line interface (CLI) version of the downloader.
	+ `scraper`: Contains the code for scraping book data from the NCERT website.
		- `scraper.py`: Contains the main scraping logic.
	+ `utils`: Contains utility functions for the project.
		- `folders_cleanup.py`: Contains functions for cleaning up folders.
   + `run_cleanup.py`: Script for cleaning up data folders.
   + `run_scraper.py`: Script to generate resource file containing books download links.
   + `run_cli_app.py`: Script to run CLI based downloader App.
   + `run_gui_app.py`: Script to run GUI based downloader App.
* `config`: Contains configuration files for the project.
* `requirements.txt`: Contains the dependencies required by the project.
* `data`: Contains the data files generated by the scraper and downloader.
   + `resources`: Contains the output of run_scraper.py script - `ncert_books_links.json`. The file contains download links for books.
   + `downloading`: Holds temporary downloaded book files which are being processed currently.
   + `books`: Processed books are moved to this folder


## Contributing
Contributions are welcome! Please submit a pull request with any improvements.

## License
This project is licensed under the MIT License.

## Authors
- [Har-Var](https://github.com/Har-Var)

## Acknowledgments
Thanks to the National Council of Educational Research & Training (NCERT) and to everyone who helped test and improve the downloader.