# Data Management course project #
JSON is a popular textual data format that's used for exchanging data in modern web and mobile applications. JSON is also used for storing unstructured data in log files or NoSQL databases.
# Deliverables #
- Choose a MongoDB that manages JSON documents. Given a large number of JSON documents, I created a document database based on this data.
- JSON to Relationa: I parse the data and create a relational database dbjson corresponding to it. I study the data first and propose a relational schema for it and minimize redundancy: My ER Diagram

![ER_diagram](https://github.com/sai-shi/JSON-document-database-design-and-analysis/blob/main/ER_diagram.png)

- Comparative Studies: Given a number of queries and tasks to complete over the 2 databases, their performances are compared.
- Optimize databases: introduce indices.

# Program #
- In Python, run mongodb_populate.py to parse json file and import all data into mongodb client;
- Open MySQL, run create_empty_tables.sql to create all Tables based on the relational schema;
- In Python, run mysql_populate.py to parse json file and import all data into MySQL; 
- RDBMS queries: run Jupyter notebook mysql_query.ipynb; 
- NoSQL queries: run Jupyter notebook mongodb_query.ipynb.
