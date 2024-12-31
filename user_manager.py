import sqlite3

class User_manager:
    def __init__(self, database_path):
        """
        Initialize the User_manager with the path to the SQLite database.
        Create a table for users if it doesn't already exist.
        """
        self.conn = sqlite3.connect(database_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Create the users table if it doesn't already exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                username TEXT
            )
        ''')
        self.conn.commit()

    def add_user(self, telegram_id, username):
        """
        Add a new user to the database.
        
        Args:
        - telegram_id: The Telegram ID of the user.
        - username: The username of the user.
        """
        try:
            self.cursor.execute(
                "INSERT INTO users (telegram_id, username) VALUES (?, ?)",
                (telegram_id, username)
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            # User already exists in the database
            pass

    def get_users_telegram_id(self):
        """
        Get a list of all Telegram IDs of users in the database.
        
        Returns:
        - A list of tuples containing Telegram IDs.
        """
        self.cursor.execute("SELECT telegram_id FROM users")
        return self.cursor.fetchall()

    def get_user_by_telegram_id(self, telegram_id):
        """
        Retrieve user details by their Telegram ID.
        
        Args:
        - telegram_id: The Telegram ID of the user to fetch.
        
        Returns:
        - A dictionary with user details, or None if the user doesn't exist.
        """
        self.cursor.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (telegram_id,)
        )
        row = self.cursor.fetchone()
        if row:
            return {'id': row[0], 'telegram_id': row[1], 'username': row[2]}
        return None

    def delete_user(self, telegram_id):
        """
        Delete a user from the database by their Telegram ID.
        
        Args:
        - telegram_id: The Telegram ID of the user to delete.
        """
        self.cursor.execute(
            "DELETE FROM users WHERE telegram_id = ?",
            (telegram_id,)
        )
        self.conn.commit()

    def close(self):
        """Close the connection to the database."""
        self.conn.close()