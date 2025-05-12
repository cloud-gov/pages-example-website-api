![Pages](/assets/images/pages-logo.png)

![Static Badge](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Static Badge](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)


# API Application

## Intro

This python flask application provides a way to interact with a PostgreSQL database by providing a secure connection using Cloud Foundry environment variables and return the result as JSON to a static website hosted on Pages. 

**Functions**

- Connect to the RDS service instance
- Access the database 
- Execute a SQL query
- Fetch data from the database
- Return the result as JSON

## Where to input your own data

There are a few instances in the `app.py` and the `manifest.yml` file where you will need to inject your own data that is specific to your project/work.

In `app.py`

Line 14: `CORS(app, origins=['https://your-pages-url'], headers=['Content-Type'], methods=['GET'])`
<br>
*when launching the application for the first time this line can be ommitted until you are ready for your Pages site to hit the API endpoint*
<br>

Line 11: `port = int(os.getenv('PORT', {whatever port you wish to expose})`

Line 17: `aws_rds = app_env.get_service(name='your-db-name')`

<br>

*Optional if you wish to serve from the root URL or not*

<br>

Line 56: `@app.route('/', methods=['GET'])`

Line 69: `@app.route('/your_sub_route', methods=['GET'])`

Line 66: `query = 'SELECT * FROM {your_table} LIMIT 15'`

In `manifest.yml`

Line 3: `- name: your_app_name`

Line 14: `- {your_db_name}`

## Set Up

### Prequesites
- Pages [sandbox](https://cloud.gov/pages/documentation/sandbox/) or existing account.
- Pages [site](https://github.com/Ephraim-G/Data-table) to display the data.
*the site repository linked is the example site created in conjunction for and with this application, feel free to utilize that one for testing purposes or create your own.*
- [Cloud Foundry CLI](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html)
- [Cloud Foundry CLI Service Connection Plugin](https://github.com/cloud-gov/cf-service-connect)
- cloud.gov [sandbox](https://cloud.gov/docs/pricing/free-limited-sandbox/#sandbox-limitations) or existing account with the following security groups applied `trusted_local_networks_egress` and `public-egress`.
- [PostgrSQL v15 database](https://cloud.gov/docs/services/relational-database/#create-an-instance) within cloud.gov.
- Dataset to `COPY` into the PostgreSQL database
*for this example we used a CSV file from [data.gov](https://catalog.data.gov/dataset/?q=&sort=views_recent+desc&ext_location=&ext_bbox=&ext_prev_extent=&_res_format_limit=0).
- [Python](https://www.python.org/downloads/) or download via [Homebrew](https://docs.brew.sh/Homebrew-and-Python).
- [pip](https://pypi.org/project/pip/) 

## Implementation

1. Login to cloud.gov via the terminal with `cf login -a api.fr.cloud.gov --sso`.
2. Follow the cloud.gov [documentation](https://cloud.gov/docs/services/relational-database/#create-an-instance) to provision a `aws-rds` `micro-psql` database instance.
3. Via the CF service connection plugin connect to your databse and [create](https://www.postgresql.org/docs/current/tutorial-table.html) a table with column(s) containing the proper headers according to your CSV file dataset.
4. [Import](https://www.postgresqltutorial.com/postgresql-tutorial/import-csv-file-into-posgresql-table/) the CSV file into the created table.
5. Fork this repository and clone it directly to your machine.
6. Move into the forked repository with `cd /path/to/forked/repository`.
7. In whatever IDE of your choice input your own specific data where applicable.
7. Run `pip install -r requirements.txt` to install the necessary modules.
8. Deploy the app into your space with `cf push`.
9. Verify that the application is in the space with `cf apps`.

*To bind via the CLI instead of using the manifest.yml file*
1. [Bind](https://docs.cloudfoundry.org/devguide/services/application-binding.html#bind) the application to the RDS service instance previously provisioned with the cf CLI.
2. Redeploy the application with `cf restart app-name`.

# Development

## Run mock API test locally via Docker

### Prerequisites

- **Docker and Docker Compose** (v20.10.0+)
- **Python 3.8+**
- **pip**
- **pytest** (installed via `requirements.txt`)
- **FastAPI**

### Dependencies

All required packages are listed in the `requirements.txt` file.

## Getting Started

### Install Dependencies

Install required Python packages:

`pip install requirements.txt`

`pip install "fastapi[standard]"`

### Setup Test Database

Run the database setup script to create a Docker container with PostgreSQL and seed it with mock data.

`./test-db.sh`

This script will:

- Build and start Docker containers
- Initialize the PostgreSQL database
- Create a users table
- Populate the table with 10 mock users

### Run Tests

Execute the test via pytest:

`pytest test.py -v`

The test will:

- Execute a mock HTTP request to the FastAPI endpoint
- Verify the connection to the PostgreSQL database works correctly
- Validate the returned user data matches the expected format

## Troubleshooting

- **Database Connection Issues**: Ensure Docker containers are running with `docker ps`
- **Port Conflicts**: Check if port 5432 is already in use
- **Permission Denied**: You may need to make the `test-db.sh` script executable with `chmod +x test-db.sh`

## Cleanup

To stop and remove the Docker containers:

`docker compose down`

 









