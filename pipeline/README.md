# LMNH-Kafka-Pipeline

### Overview
This project implements a data pipeline that connects to a Kafka data stream, reads the incoming data, cleans it and then uploads the cleaned data to a PostgreSQL database. The pipeline is modular, with each stage of the process handled by a separate script: extract.py, transform.py, and load.py (described below).  

### Installation
1. Clone the repository:
```bash
git clone https://github.com/AlexOBarnes/LMNH-Kafka-Pipeline.git
```

2. Install the required Python packages:

```bash
cd pipeline/
pip install -r requirements.txt
```
Requirements.txt file includes all dependencies including: confluent_kafka, psycopg2, and python-dotenv.

### Setup
In order to run the script users must create a .env file containing the following things.
- Confluent_kafka requirements:
    - `BOOTSTRAP_SERVERS`
    - `SECURITY_PROTOCOL`
    - `SASL_MECHANISM`
    - `KAFKA_USERNAME`
    - `KAFKA_PASSWORD`
    - `TOPIC`
    - `GROUPID`  
- Psycopg2 requirements:
    - `DATABASE`
    - `USER`
    - `HOST`
    - `PASSWORD`
    - `PORT`  

The *.py files use environment variables and the names of these can be changed easily to match your .env format.

This script utilises both a [kafka cluster](https://docs.confluent.io/confluent-cli/current/command-reference/kafka/cluster/confluent_kafka_cluster_create.html) and a [PostgreSQL](https://www.moncefbelyamani.com/how-to-install-postgresql-on-a-mac-with-homebrew-and-lunchy/) database. Please ensure that you have downloaded and setup both of these up before moving on with the setup.  

In order to create an appropriately named database on either a cloud database service (e.g. AWS RDS) or locally, use the following command.   
```bash

psql -h $HOST -U $USER $DATABASE -c "CREATE DATABASE museum;"
```
If you choose to run this locally, make sure to update line 16 & 33 of load.py, as psycopg2 would only require host,database and user fields.  

Once the database has been set up run the following commands.
```bash
cd ../database/
psql -h $HOST -U $USER $DATABASE -f schema.sql
```
This will create the tables this script uses and will seed some tables with static data. Within this folder, there is also a corresponding entity relationship diagram is present.

### Usage
To run the pipeline; 
```bash
python pipeline.py
```
You can include `-l` tag to log warnings to file.

To kill the script use control C.

In order to truncate the database;
```bash
bash reset.sh
```
This will remove data from only the `rating_interaction` and `request_interaction` tables, to reset the entire database re-run the `schema.sql` script.

### How It Works

#### pipeline.py
- Parses command line arguments if present and configures the log.
- Then the extract.py function is called.
- If -l flag is used then only warnings and errors are logged. Without the flag log info, warnings and errors are logged to terminal.

#### extract.py
- Loads in the environment variables.
- Creates and configures a consumer (confluent_kafka).
- Calls `check_data()` to test data validity.
- If data is in a valid format according to the database schema it is passed to be `transform()` and then `load_data()`

#### transform.py
- Contains `check_valid_keys()`, `check_valid_date()`, `check_valid_site()`, `check_valid_value()` functions.
- The `check_valid_*()` each check that part of the received data is in the correct format and is a valid value.
- `transform()` converts and then returns the validated data depending on whether it is a request or a review.

#### load.py
- Calls `insert_request()` or `insert_review()` depending on the data received.
- Each `insert_*()` uses psycopg2 to connect to a given PostgreSQL database and execute an insert query.
- Returned data is then logged, a warning is logged if no data is returned.

#### reset.sh
- Truncates the rating_interaction and request_interaction tables using environment variables.
- Update the variable names in the script to be consistent with your naming convention.
- This script can be modified to truncate other tables, but the current two have been chosen as the others are filled with static data.

### Contribution
Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure that your code adheres to the project's coding standards, I use pylint to format my code, and is well-documented. Code must score above an 8 in pylint and the unit tests included in the repository must pass.

### Licence
This project is licensed under the MIT License - Please see the [attached](https://github.com/AlexOBarnes/LMNH-Kafka-Pipeline/blob/main/LICENSE) file 

