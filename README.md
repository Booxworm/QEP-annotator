# QEP-annotator

## Clone the repo
```
git clone https://github.com/Booxworm/QEP-annotator.git
cd QEP-annotator
```

## Download data files
Download the zipped data files from https://drive.google.com/file/d/1xMtR-z9hVEKFsR8xd9jHbzLQM5b-4t0p/view?usp=sharing

Unzip the data, and change the file path in scripts/copy_data.txt so that it matches the file path that the data is saved to.

## PostgreSQL
### Installation
Install PostgreSQL from https://www.postgresql.org/download/

### Create db
After setting up PostgreSQL, create a database "TPC-H" under the user "postgres". The password is the same password entered during setup.
```
createdb -U postgres TPC-H
```

Connect to the TPC-H database
```
psql -U postgres -d TPC-H
```

### Create tables
Create the tables by copying the script from scripts/create_tables.txt.
To check that the tables are created, type "\d" in the command line.
To get more info on an individual table, use "\d [TABLE_NAME]"

### Populate db
Populate each table by copying the script from scripts/copy_data.txt, making sure that the file path has been changed.
To check that the db has been populated, run an SQL query to test, such as
```
SELECT r_name, n_name 
FROM region, nation 
WHERE r_regionkey = n_regionkey 
LIMIT 5; 
```
