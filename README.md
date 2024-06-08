<figure role="img" aria-labelledby="REAT_ascii_logo" style="line-height: 1.2; letter-spacing: -1px;font-family: 'Courier New';"><pre align="center">
 /^--^\     /^--^\     /^--^\
 \____/     \____/     \____/
 /      \   /      \   /      \
 |        | |        | |        |
 \__  __/   \__  __/   \__  __/
|^|^|^|^|^|^|^|^|^|^|^|^|^|^\ \^|^|^|^/ /^|^|^|^|^\ \^|^|^|^|^|^|^|^|^|^|^|^|^|
|_|_|_|_|_|_|_|_|_|_|_|_|_|_|\ \|_|_|/ /|_|_|_|_|_|\ \|_|_|_|_|_|_|_|_|_|_|_|_|
|  ___          _   ___    _ /_/    _\ \        _ /_/         _               |
| | _ \___ __ _| | | __|__| |_ __ _| |_/___    /_\  _ _  __ _| |_  _____ _ _  |
| |   / -_) _` | | | _|(_-<  _/ _` |  _/ -_)  / _ \| ' \/ _` | | |/ / -_) '_| |
| |_|_\___\__,_|_| |___/__/\__\__,_|\__\___| /_/ \_\_||_\__,_|_|   /\___|_|   |
|______________________________________________________________/__/___________|
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
</pre></figure>

<h1 align="center"><br>
  Real Estate Analyzer Tool
  <br>
</h1>

<h4 align="center">A Python web scraping tool for real estate websites, capable of extracting data into tables, charts, and creating PDFs.</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#installation">Installation</a> •
  <a href="#installation">Files after fresh installation</a>
</p>

<div style="text-align:center">
<video width="640" height="480" controls autoplay>
  <source src="REAT_small_intro.mp4" type="video/mp4">
</video>
<p>Full video link: <a href="https://youtu.be/UDdDWQrBvBQ?si=ImNulx6Ndnprui7R">https://youtu.be/UDdDWQrBvBQ?si=ImNulx6Ndnprui7R</a></p>
</div>

## Key Features

1. Data Scraping: Real Estate Analyzer Tool seamlessly scrapes data from supported websites, ensuring you have the most up-to-date information at your fingertips.

2. Data Organization: Say goodbye to spreadsheet chaos. Our application efficiently organizes the collected data, making it easy to access and work with.

3. Dynamic Charts: Transform raw data into stunning, interactive charts, enabling you to visualize trends and insights at a glance.

4. Informative Tables: Create customizable tables that are both informative and aesthetically pleasing, ensuring your data is presented with clarity.

5. PDF Reports: Generate professional PDF reports with just a few clicks, incorporating your charts, tables, and additional insights into a polished document.

## How To Use

### Data creator tab

1. Site Selector
* Choose your desired website source from a list of supported options.
* Stay flexible as new websites become available, ensuring your data collection remains up-to-date.
2. Web Search Section
* Simply copy the complete link from your browser after navigating to the specific webpage you wish to scrape.
* Connect with the exact data you need, no matter how deep or complex the webpage structure.
3. Search Parameters
* Customize your web scraping process by filling in the required search parameters, such as keywords, date ranges, or specific categories.
* Start the search using your app, tailoring the data collection to your precise needs.
4. Terminal Section
* Monitor the progress of the scraping process in real-time as the app works its magic.
* Be prepared to respond to any questions that may arise during the search, allowing you to guide the process to meet your goals effectively.

### Data tab

* Key Data Details:\
This table provides a snapshot of the key details of your collected data, giving you an overview of the dataset's structure and content.
* Maximum Values:\
Discover the maximum values within each column, gaining insight into the upper bounds of your data's numeric attributes.
* Minimum Values:\
Uncover the minimum values within each column, highlighting the lower limits of your data's numeric attributes.
* Top 20 Descriptive Rows:\
Access the top 20 rows of your data, sorted in descending order based on the "Price" column and two other dynamic columns (which adapt to your collected data). This table allows you to quickly identify the most valuable entries.
* Bottom 20 Descriptive Rows:\
Similar to the previous table, but sorted in ascending order, allowing you to explore the least expensive or relevant entries in your dataset.
* Median and Neighboring Rows:\
Dive deeper into the data by exploring it based on the middle value (if it exists) or the values closest to the mean of the "Area" column. This table displays these values and a maximum of 9 rows in both descending and ascending orders, enabling you to analyze data distribution effectively.

### Charts tab

* Property Distribution by Area:\
Chart the number of properties based on their areas, offering a clear overview of area-related trends in your dataset.
* Property Distribution by Price:\
Visualize the distribution of properties based on their prices, allowing you to identify price-related patterns.
* Price vs. Rooms Histogram:\
Similar to the previous chart, but color-coded to represent the number of rooms (including half-rooms), providing insights into room configurations across different price ranges.
* Unit Price or Monthly Rental Price:\
The chart displays either unit prices or monthly rental prices, depending on the collected data, to visualize the distribution of properties, facilitating pricing analysis.
* Heat Map with Area-Based Histograms:\
Utilize a heat map combined with area-based histograms to reveal the relationship between unit price or monthly rental price and property area, highlighting area-specific property concentration.
* Scatter Plot Analysis:\
Delve into the unit price or monthly rental price of properties as they relate to their areas. The size and color of data points represent additional aspects of the data, offering multidimensional insights.
* Location Choropleth:\
This interactive map displays the geographical distribution of properties found in the dataframe. The size of markers indicates the number of properties at each location. To enable this chart, ensure you've provided your Mapbox API key in the app settings.

### Pdf maker tab

* Choose Your Content:\
Select the tables and charts you wish to include in your PDF report based on your specific needs and preferences. Whether it's tables, charts, or both, you have complete control over your content selection.
* Customize Titles and Descriptions:\
While the application provides default titles, subtitles, and descriptions for your charts, you can modify these to better convey your insights and findings. Tailor the narrative to suit your unique story.
* Add a Unique Introduction:\
Infuse your report with a personalized touch by adding a unique introduction. Share context, objectives, or any other information that sets the stage for your data analysis.
* View and Download PDFs:\
The app opens a built-in PDF viewer within the application, enabling you to instantly view and download your report with a simple click. This feature makes your reports readily accessible for sharing or further analysis, all without leaving the app.

### Settings tab

* Choose Your Web Browser:\
Select your preferred web browser for running the app. Your choice of browser allows you to integrate seamlessly with the app, ensuring a familiar and convenient experience.
* Mapbox API Key:\
If you intend to use the location-related features, including the dynamic map generation, simply provide your Mapbox API key. This key allows the app to collect GPS coordinates and display geographical data accurately.
* User Credentials for Ingatlan.com:\
To enable specific scraping functions for the Ingatlan.com website, input your username and email credentials. This information is crucial for accessing the desired data from the site, ensuring a streamlined data collection process.

## How it works

### General details

**Programming languages:**
- Python
- Javascript
- Html
- CSS
- Bootstrap 5 (CSS framework)

**Supported browsers:**
- Chrome
- Edge

**Used python packages:**
- flask
- flask Socketio
- collection
- pandas
- plotly
- html2image
- PIL
- os
- datetime
- pickle
- urllib.parse
- numpy
- requests
- re
- selenium 4.12.0 (the last version which is compatible with the undetected chrome driver)
- undetected_chromedriver
- fpdf2
- matplotlib
- kaleido
- setuptools

### Main app concept (skeleton)

The app uses Flask as main framework to provide GUI and control the app general function and working methods.\
Each tab represents a separate HTML page extended from the base HTML page containing the navigation bar.\
The core of the app resides in the `scrapping.html` and function.\
Upon the initial app load, all tabs display their information in an accordion panel, except for the `Data collector tab (scrapping.html)`.\
To begin the scraping process, the user selects a webpage to scrape and proceeds to fill the web search field or input manual search parameters, followed by clicking the 'Search' button. This initializes the variables, clears the necessary folders, and commences the web scraping process.\
\
During scraping, the `my_event` function triggers, moving through the criteria defined by the user. The `real_estate_webscrpmod.py` functions yield the scraping process's status to the `my_event` function, which transmits this information to the terminal using the socket.io protocol.\
Should an issue arise during the process that requires user interaction, the scraping function halts, displaying a message on the terminal, awaiting user action.\
Should an issue arise during the process that requires user interaction, the scraping function halts, displaying a message on the terminal, awaiting user action. If the process runs smoothly, the scraped data is passed in a "ready for dataframe" format to the `dataframe_creator` function. This function generates an unfiltered dataframe, saves it in CSV and pickle formats, and then filters the dataframe to address inconsistencies, saving it with the '_filtered' keyword appended to the filename. This filtered file is utilized in further app processes.\
The unfiltered dataframe can be cleaned and furter processed by the user.\
\
Moving to the `Data tab`, the `data` function leverages the `real_estate_df.py` function pack to create various tables. The raw dataframes are formatted using HTML and CSS code for display in the web browser.\
\
In the `Charts tab`, the `charts` function utilizes the `real_estate_visual.py` function pack to produce JSON data for the plots. The web browser then generates interactive diagrams using HTML and Plotly JS extensions. These plots can be saved to PDF directly from the Charts tab.\
Special mention is made for the choropleth generator, which utilizes the Mapbox API to obtain Longitude and Latitude data and calculates an ideal zoom size, although the function's data grabber may require properly cleaned and altered data. The function saves the coordinates for further use, reducing reliance on the Mapbox API and speeding up the chart generation process. Proper full data cleaning and alteration is not in the scope of this project. The choropleth function is in experimental state.\
The function saves the coordinate data into a file for future use, aiming to reduce reliance on the Mapbox API and expedite the chart generation process.
\
The generator functions in the Data and Charts sections dynamically adjust based on the scraped data, such as property types, currency, and more.\
\
The `PDF Maker tab` allows users to define the contents of a PDF report. Robust JS code manages on-the-fly updates for switches based on modifications or selections of item titles, subtitles, or descriptions. The text field incorporates a simple character and row limiter function to ensure consistent data for the PDF creator functions. Additionally, there are some basic page numbering options available. Users may need to revise descriptions or elements for a well-organized final PDF report.\
The 'Create PDF' button submits data to the Flask server using the fetch API, including a JSON aggregation of the form of the status of the switches, and the JSON of titles, subtitles, descriptions, and item status indicated by their color-coded names. The PDF creation involves generating PNGs by screenshotting the web browser (in headless mode) for tables and using the Plotly `write_image` function for charts.\
All these are saved to the 'files/png' folder along with the 'titles_txt.json', which contains descriptive data and status codes for the items.\
The PDF creation process, managed by the `real_estate_pdf_maker.py` function pack, involves positioning elements, calculating image sizes, and their placement, following specific rules and logic for coordinated positioning.\
The PDF opens in the web browser's built-in PDF viewer, enabling saving and printing. The PDF files are saved to the 'static' folder as Flask accesses files from this location.\
\
The `Settings tab` allows users to provide certain settings that are saved in the `settings.json` file.\
\
Upon running the app after generating and navigating through the tabs successfully, the last saved data is visible under the respective tabs. Clicking the 'Search' button in the Data collector tab clears all data and initializes a new search.

## Installation

1. Install the latest version of [python](https://www.python.org/downloads/) (the app was tested on ver3.12)
2. Install an IDE (e.g VSC)
3. Create a venv for the app (preferably using your IDE)\
In case of VSC do the following:
    - Create a folder for the app
    - Open this folder in VSC **File > Open Folder**
    - In the Command Palette (**View > Command Palette)** select **Python: Create Environment**
    - Select the python version (the latest advised)
    - Create new terminal **Terminal > Create New Terminal**\
If you encounter an error stating that running scripts is denied in PowerShell, you will likely need to allow running scripts.\
Open a powershell as administrator and type in the following:
      ```bash
      Set-ExecutionPolicy -ExecutionPolicy AllSigned
      ```
      Whenever you open the terminal in VSC and it prompts whether you want to allow running scripts, choose the option [A] to 'Always run'.
4. At this point, you should have a folder and a virtual environment (venv) for the app. Copy all the files and folders from the downloaded app, maintaining the original file structure, into your app folder
5. Download and copy the [chromedriver](https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json) or [edgedriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) into the app main folder too.\
It's important to note that the driver version number should match the web browser version number. It's generally advisable to use the latest version for both.
6. Install all dependencies:
    ```bash
   pip install -r requirements.txt
    ```
4. You are ready. Run the app:
    ```bash
   python3 real_estate_analyzer.py
    ```
    or in VSC click the run python file button at the top right corner.\

## Files after fresh installation
* main app folder
    - static folder
        - css folder
            - df_style.css (Data section styling)
            - index.css (Homepage styling)
            - navbar.css (Navbar styling)
            - terminal.css (Terminal styling)
        - pics folder
            - footer.png (Footer picture for the pdf)
            - header.png (Header png for the pdf)
            - logo.png (Logo to the header for the pdf)
        - script
            - scrap.js (JS module for the scrapping.html)
            - settings.js (JS module for the settings.html)
            - terminal.js (JS module for the terminal)
    - templates folder
        - base.html (The base html)
        - charts.html (Charts tab)
        - data.html (Data tab)
        - index.html (Home tab)
        - navbar.html (Navbar inserted to the base.html)
        - pdf_maker.html (Pdf maker tab)
        - pdf_read.html (read the created pdf)
        - scrapping.html (Data collector tab)
        - settings.html (Settings tab)
        - socketio_scramble_effect.html (Terminal)
        - to_print.html (Helper html to create the df pngs)
    - README.md (This file)
    - real_estate_df.py (Functions to create the tables)
    - real_estate_general_funcs.py (All the general functions to the app e.g. file operations, df creator etc.)
    - real_estate_pdf_maker.py (Pdf generator functions)
    - real_estate_visual.py (Chart generator functions)
    - real_estate_webscrpmod.py (Web scraping classes with functions)
    - REAT_small_intro.mp4 (Small video embeded in this file)
    - requirements.txt (requirements for easy installation of dependencies)

