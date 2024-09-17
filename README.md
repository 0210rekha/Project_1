### YouTube Data Harvesting and Data Warehousing ###

***** Overview ******

This project facilitates the extraction of data from a specific YouTube channel using its Channel ID and stores the collected information in a SQL database. It is designed to streamline data analysis and reporting by organizing and storing YouTube channel data in a systematic way. The project gathers information such as video details, performance statistics, and relevant metadata, providing insights into the channel's performance and content trends.

****** Features ******

  **Channel Data Extraction**: Fetches comprehensive information about a YouTube channel’s videos by using its Channel ID
  **Data Warehousing**: Efficiently stores all extracted data in a SQL database, allowing for easy querying and advanced analytics.
  **Automated Data Pipeline**: Automates the process of regularly fetching and updating the database with the latest data from the channel.
  **Data Analysis Ready**: The extracted data is structured and stored in a format ready for analysis, enabling further insights into viewership trends, video performance,   and more.

****** Technologies Used ******

  **Python**: Core language for data extraction, transformation, and processing.
  **YouTube Data API v3**: Provides access to data from the YouTube platform. The API is utilized via the google-api-python-client package.

    To install this package: pip install google-api-python-client

  **MySQL Database**: Relational Database Management System (RDBMS) used for data warehousing. Structured Query Language (SQL) handles data manipulation and management.

  **Pandas**: A powerful data manipulation library that provides essential tools for data transformation and analysis.

    To install this package: pip install Pandas

  **mysql-connetor**: Official MySQL connector for Python that allows for smooth interaction between the Python application and the MySQL database.

    To install this package: pip install mysql-connector-python

  **Streamlit** - A fast, lightweight web application framework that allows developers to quickly create interactive, data-driven web apps with minimal code. It is utilized here to visualize data and provide a downloadable CSV format.

    To install this package: pip install streamlit

You can install the dependencies one by one, or alternatively, use the provided requirements.txt file to install all packages at once:

****** Installation ******

Install the pytohn package that you needed for this project are provide in the *requirement.txt* file. Execute the requiremnt text in the cmd prompt or in terminal if you are using mac. By using the below command.

    To install this package: pip install -r requirements.txt

****** Installation Guide ******

To set up the project, follow these steps:

- Python Environment: Ensure you have Python 3.x installed on your machine.
- Google Cloud Setup:
            Set up a Google Cloud Project.
            Enable the YouTube Data API v3 for your project.
            Generate an API key, which you'll need to add to the Harvest.py file.
- MySQL Setup:
            Install MySQL on your local machine or server.
            Configure the hostname, username, and password in the Warehouse.py file to enable database connection.
- Streamlit Setup: Sign in or sign up for Streamlit to deploy the app.

****** Usage ******

Once you’ve completed the installation, you can proceed with the following:

 Clone the Repository: git clone https://github.com/0210rekha/Project_1.git

 Run the Streamlit Web Application: Start the Streamlit app using the following command: streamlit run youtube_app.py

 Viewing and Analyzing Data: After launching the Streamlit app, you can view, analyze, and download the harvested YouTube channel data in CSV format directly from the web interface.

****** Project Structure ******

Harvest.py: Contains the core functionality to extract data from YouTube using the API.
Warehouse.py: Includes the logic for interacting with the MySQL database to store and retrieve data.
YouTube_app.py: Defines the Streamlit app configuration and displays the user interface.
requirements.txt: Lists all Python dependencies required to run the project.

****** Contributions ******

We welcome contributions! If you'd like to improve the project or have any suggestions, feel free to open a pull request or submit an issue on GitHub.

****** Demo ******

Watch a detailed walkthrough and demo on linkedin: https://www.linkedin.com/posts/rekha-b-94366a329_youtubedata-datawarehousing-automation-activity-7241674382878638080-ZfS8?utm_source=share&utm_medium=member_desktop

