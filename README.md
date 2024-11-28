
# Medical Charts ETL

## Description  
Medical Charts ETL is a project that tracks the movement of Medical Charts across various locations like SQL tables, Windows Locations and CSV Files. The end output of the project is that it loads and updates two tables maintained in SQL Server. This project also demonstrates and end-to-end automation, where the entire process can be run using a trigger drop.  


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
   git clone https://github.com/Har-Var/Medical-Charts-ETL.git
   cd Medical-Charts-ETL
   ```
2. Ensure you have Python 3.x installed.
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Configure the config_sample.py file at `src\config\config_sample.py` as per your environment. Rename the file to `config.py`
5. Ensure you have Microsoft Excel installed (version supporting macros)
6. Enable macros in Excel:
   - Go to `File > Options > Trust Center > Trust Center Settings`.
   - Enable "Trust access to VBA project object model."
7. Install SQL Server Management Studio (SSMS)
   - Download and install SSMS from the official Microsoft website:  
      [Download SSMS](https://aka.ms/ssmsfullsetup)
   - Launch SSMS and connect to your SQL Server instance using your credentials.
8. Create a database named `MedicalChartsETL` in SQL Server by executing `sql_scripts\create_EntireDatabase_MedicalChartsETL.sql` in SSMS

## Usage
Run the demo notebook `end_to_end_demo.ipynb` in the `notebooks` folder.

## Features
- Provides an improved User Interface to download NCERT Books.
- Contains both - a Graphical User Interface App and a Command Line App.
- Improves upon the official download page by further processing downloaded Zips and transforming them into consolidated PDF Books.

## Project Structure
The project is organized into the following folders:

* `src`: Contains the source code for the project.
	+ `automation`: Contains the code for the book downloader.
		- `downloader_funcs.py`: Contains utility functions for downloading books.
		- `gui_downloader.py`: Contains the code for the graphical user interface (GUI) version of the downloader.
		- `cli_downloader.py`: Contains the code for the command-line interface (CLI) version of the downloader.
	+ `dataprep`: Contains the code for scraping book data from the NCERT website.
		- `scraper.py`: Contains the main scraping logic.
	+ `utils`: Contains utility functions for the project.
		- `folders_cleanup.py`: Contains functions for cleaning up folders.
   + `config`: Contains configuration files for the project.
   + `run_scraper.py`: Script to generate resource file containing books download links.
   + `run_cli_app.py`: Script to run CLI based downloader App.
   + `run_gui_app.py`: Script to run GUI based downloader App.
* `requirements.txt`: Contains the dependencies required by the project.
* `data`: Contains the all data files generated by the process.
   + `reports`: Stores all the daily reports.
   + `charts`: Stores all charts whether as .json in `charts_drop_off` location or as .csv in `payment_reconciliation`. Also stores stats for increment push in `resources`. 
* `notebooks`: Contains Jupyter Notebook - `end_to_end_demo.ipynb` for end-to-end demo.
* `sql_scripts`: Contains SQL scripts for creating database and loading data into it.
   + `create_EntireDatabase_MedicalChartsETL.sql`: Creates the entire database along with all the required database objects.
   + `queries`: Some adhoc SQL scripts for querying the database.
   + `<rest folders in the directory>`: the above script is further divided into seperate objects which are organized into seperate folders. 
* `automation`: Contains the locations that manage the automation flow.
   + `<process_name>`: Either `recon_report_load` or `recon_report_update`
      + `staging`: Serves as the staging area. Primarily used for storing reports for `recon_report_load` process.
      + `input`: This is the monitoring area. Copy files here to trigger the automation.
      + `input_archive`: The files that triggered the process moves to here after the automation kicks-off.
      + `log`: Stores all the log files.
      + `trigger`: Holds the trigger file for the process. Exists only for `recon_report_update` process. Copy and paste this file to the monitoring folder to start the process.
* `excel_setup`: Contains the Excel setup file `financial_reconciliation_reports.xlsm` for generating payment reconciliation csv reports.


## Contributing
Contributions are welcome! Please submit a pull request with any improvements.

## License
This project is licensed under the MIT License.

## Authors
- [Har-Var](https://github.com/Har-Var)

## Acknowledgments
Thanks to everyone who helped me test and improve upon this project.
