import pprint
import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['institutions', 'positions', 'experiences', 'skills','feedback', 'users']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        """ Creates tables and populates initial data. """

        create_dir = os.path.join(data_path, "create_tables")
        data_dir = os.path.join(data_path, "initial_data")

        cnx = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database,
            charset='utf8mb4'
        )
        cursor = cnx.cursor()

        # Drop all tables if purge=True
        if purge:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            tables = self.query("SHOW TABLES")
            for table in tables:
                table_name = list(table.values())[0]
                cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`;")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            cnx.commit()
            print("Purged existing tables.")

        essential_tables = ["institutions.sql", "positions.sql", "experiences.sql", "skills.sql", "feedback.sql"]
        executed_files = set()

        # Create essential tables first (positions before experiences)
        for table_file in essential_tables:
            sql_path = os.path.join(create_dir, table_file)
            if os.path.exists(sql_path):
                with open(sql_path, "r") as file:
                    sql_script = file.read()
                    cursor.execute(sql_script, multi=True)
                    executed_files.add(table_file)
                    print(f"Executed {table_file}")

        # Execute all other table creation scripts
        for sql_file in sorted(glob.glob(os.path.join(create_dir, "*.sql"))):
            file_name = os.path.basename(sql_file)
            if file_name not in executed_files:
                with open(sql_file, "r") as file:
                    sql_script = file.read()
                    cursor.execute(sql_script, multi=True)
                    print(f"Executed {file_name}")

        # Execute initial data population scripts
        for sql_file in sorted(glob.glob(os.path.join(data_dir, "*.sql"))):
            with open(sql_file, "r") as file:
                sql_script = file.read()
                cursor.execute(sql_script, multi=True)
                print(f"Executed {sql_file}")
        
        cnx.commit()

        # Temporarily disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        # Insert initial data from CSV files (positions before experiences)
        for sql_file in sorted(glob.glob(os.path.join(create_dir, "*.sql"))):
            table_name = os.path.splitext(os.path.basename(sql_file))[0]  # Remove .sql extension
            csv_file = os.path.join(data_dir, f"{table_name}.csv")

            if os.path.exists(csv_file):
                with open(csv_file, 'r') as file:
                    reader = csv.reader(file)
                    columns = next(reader)  # Read the header row
                    values_placeholder = ", ".join(["%s"] * len(columns))
                    insert_query = f"INSERT INTO `{table_name}` ({', '.join(columns)}) VALUES ({values_placeholder})"

                    # Insert all rows from the CSV into the database
                    data_tuples = [tuple(None if val.strip().upper() == "NULL" or val.strip() == "" else val for val in row) for row in reader]
                    cursor.executemany(insert_query, data_tuples)
                    print(f"Inserted {len(data_tuples)} rows into {table_name} from {csv_file}")
            else:
                print(f"CSV file not found for table: {table_name}")

        # Re-enable foreign key checks after the inserts
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Database setup complete.")

    def getResumeData(self):
        resume_data = {}

        # Fetch all institutions
        institutions_query = "SELECT * FROM institutions"
        institutions = self.query(institutions_query)

        # Fetch all positions
        positions_query = "SELECT * FROM positions"
        positions = self.query(positions_query)

        # Fetch all experiences
        experiences_query = "SELECT * FROM experiences"
        experiences = self.query(experiences_query)

        # Fetch all skills
        skills_query = "SELECT * FROM skills"
        skills = self.query(skills_query)

        # Organize data into a nested dictionary
        for institution in institutions:
            inst_id = institution["inst_id"]
            resume_data[inst_id] = {
                "address": institution["address"],
                "city": institution["city"],
                "state": institution["state"],
                "type": institution["type"],
                "zip": institution["zip"],
                "department": institution["department"],
                "name": institution["name"],
                "positions": {}
            }

        for position in positions:
            pos_id = position["position_id"]
            inst_id = position["inst_id"]  # Foreign key reference

            if inst_id in resume_data:
                resume_data[inst_id]["positions"][pos_id] = {
                    "end_date": position["end_date"],
                    "responsibilities": position["responsibilities"],
                    "start_date": position["start_date"],
                    "title": position["title"],
                    "experiences": {}
                }

        for experience in experiences:
            exp_id = experience["experience_id"]
            pos_id = experience["position_id"]  # Foreign key reference

            for inst_id in resume_data:
                if pos_id in resume_data[inst_id]["positions"]:
                    resume_data[inst_id]["positions"][pos_id]["experiences"][exp_id] = {
                        "description": experience["description"],
                        "end_date": experience["end_date"],
                        "hyperlink": experience["hyperlink"],
                        "name": experience["name"],
                        "skills": {}
                    }

        for skill in skills:
            skill_id = skill["skill_id"]
            exp_id = skill["experience_id"]  # Foreign key reference

            for inst_id in resume_data:
                for pos_id in resume_data[inst_id]["positions"]:
                    if exp_id in resume_data[inst_id]["positions"][pos_id]["experiences"]:
                        resume_data[inst_id]["positions"][pos_id]["experiences"][exp_id]["skills"][skill_id] = {
                            "name": skill["name"],
                            "skill_level": skill["skill_level"]
                        }
        print(resume_data)
        return resume_data

    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        if not parameters:
            print("No data to insert.")
            return

        # Construct the INSERT query
        placeholders = ", ".join(["%s"] * len(columns))
        column_names = ", ".join(columns)
        query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"

        cnx = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database,
            charset='utf8mb4'
        )
        cursor = cnx.cursor()

        try:
            cursor.executemany(query, parameters)  # Efficient batch insert
            cnx.commit()
            print(f"Inserted {cursor.rowcount} rows into {table}.")
        except mysql.connector.Error as err:
            print(f"Error inserting rows into {table}: {err}")
        finally:
            cursor.close()
            cnx.close()

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
    def createUser(self, email='me@email.com', password='password', role='user'):
        if role not in ['guest','owner']:
            return {'success': 0, 'error': 'Invalid role. Must be "guest" or "owner".'}
        
        encrypted_password = self.onewayEncrypt(password)
        try:
            # Check if the user already exists
            existing_user = self.query("SELECT * FROM users WHERE email = %s", (email,))
            if existing_user:
                return {'success': 0, 'error': 'User already exists.'}

            # Insert the new user into the database
            self.query("INSERT INTO users (email, password, role) VALUES (%s, %s, %s)",
                    (email, encrypted_password, role))

            return {'success': 1, 'message': 'User created successfully.'}

        except mysql.connector.Error as e:
            return {'success': 0, 'error': f'Database error: {str(e)}'}

    def authenticate(self, email='me@email.com', password='password'):
        try:
            # Encrypt the provided password using the same encryption method
            encrypted_password = self.onewayEncrypt(password)

            # Check if the user exists with the provided email and encrypted password
            user = self.query("SELECT * FROM users WHERE email = %s AND password = %s", (email, encrypted_password))
            if user:
                return {'success': 1, 'message': 'Authentication successful.'}
            else:
                return {'success': 0, 'error': 'Invalid email or password.'}

        except mysql.connector.Error as e:
            return {'success': 0, 'error': f'Database error: {str(e)}'}

    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message


