# lib/dog.py

from config import CONN, CURSOR


class Dog:
    # Constructor
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    # Class method to create the dogs table
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
        

    # Class method to drop the dogs table if it exists
    @classmethod
    def drop_table(cls):
        
        sql = """
            DROP TABLE IF EXISTS dogs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    # Instance method to save a Dog object to the database
    def save(self):
        if self.id:
            self.update()
        else:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.breed))
            CONN.commit()
            self.id = CURSOR.lastrowid

    # Class method to create a Dog instance and save it to the database
    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    # Class method to construct a Dog instance from database row data
    @classmethod
    def new_from_db(cls, row):
        id, name, breed = row
        dog = cls(name, breed)
        dog.id = id
        return dog

    # Class method to retrieve all Dog instances from the database
    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM dogs"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.new_from_db(row) for row in rows]

    # Class method to find a dog by its name
    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM dogs WHERE name = ?"
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    # Class method to find a dog by its id
    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM dogs WHERE id = ?"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    # Instance method to update the dog's record in the database
    def update(self):
        sql = "UPDATE dogs SET name = ?, breed = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()
