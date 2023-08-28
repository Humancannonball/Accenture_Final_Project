This project is a COVID-19 dashboard that displays epidemiological data and GDP information for various countries. The dashboard is built using Dash, MongoDB, Snowflake.

To run the project: 
0. Create a virtual enviroment. Install necessary dependencies: pymongo snowflake.connector dash pandas dotenv.
1. Fill in the .env file with your Snowflake credentials and MongoDB connection string.
2. Run mongodb.py to create a MongoDB table out of the csv file. 
3. Run main.py, connect to the localhost:8050.


Task 1.
Created account (AWS, Ohio region). Got a COVID-19 Epidemiological Data by Starschema. Created a resource monitor.

Task 2-3.
Analyzed dataset using example queries provided by Starschema, viewed main tables, viewed main connections between data. Downloaded World GDP (current US$) dataset from worldbank.org. Created a MongoDB table out of the gdp.csv. The table contains id, Country name, and years 2015-2022.

Task 4-5. 
Created both API and visualization dashboard using Dash. The dashboard contains 2 graphs, from MongoDB data, and from Snowflake data. Both graphs are interactive, and can be filtered by country. 
The API eases the process of interacting, getting data from Snowflake and MongoDB, and makes the code reusable and clean.

Bonus: Added a button to the dashboard, which allows users to add annotations or comments, which are then stored in the MongoDB.

Task 7-8.

Implemented simple, yet efficient caching for requested data. The code is optimized in a way that it doesn't make unnecessary requests to the database, and doesn't make unnecessary calculations. The SQL queries get the data which is needed, not more.
