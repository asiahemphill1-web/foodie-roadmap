import os
import sqlite3
from models import FoodieItem


class FoodieDatabase:
    def __init__(self, database_path="data/foodie_roadmap.db"):
        self.database_path = database_path
        self.create_database_folder()
        self.create_tables()
        self.update_existing_database()

    def create_database_folder(self):
        folder_name = os.path.dirname(self.database_path)
        if folder_name and not os.path.exists(folder_name):
            os.makedirs(folder_name)

    def connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def create_tables(self):
        with self.connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS foodie_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    item_type TEXT NOT NULL,
                    cuisine TEXT NOT NULL,
                    ingredients TEXT,
                    location TEXT,
                    link TEXT,
                    notes TEXT,
                    rating INTEGER DEFAULT 0,
                    has_tried INTEGER DEFAULT 0,
                    is_favorite INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def update_existing_database(self):
        needed_columns = {
            "ingredients": "TEXT",
            "location": "TEXT",
            "link": "TEXT",
            "has_tried": "INTEGER DEFAULT 0",
        }

        with self.connect() as connection:
            rows = connection.execute("PRAGMA table_info(foodie_items)").fetchall()
            existing_columns = [row["name"] for row in rows]

            for column_name, column_type in needed_columns.items():
                if column_name not in existing_columns:
                    connection.execute(f"ALTER TABLE foodie_items ADD COLUMN {column_name} {column_type}")

            if "location_or_link" in existing_columns:
                connection.execute(
                    """
                    UPDATE foodie_items
                    SET location = COALESCE(location, location_or_link, '')
                    WHERE location IS NULL OR location = ''
                    """
                )

    def add_item(self, item):
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO foodie_items
                (title, item_type, cuisine, ingredients, location, link, notes, rating, has_tried, is_favorite)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item.title,
                    item.item_type,
                    item.cuisine,
                    item.ingredients,
                    item.location,
                    item.link,
                    item.notes,
                    item.rating,
                    int(item.has_tried),
                    int(item.is_favorite),
                ),
            )

    def get_items(self, item_type="all", cuisine="all", search_text=""):
        query = "SELECT * FROM foodie_items WHERE 1 = 1"
        values = []

        if item_type != "all":
            query += " AND item_type = ?"
            values.append(item_type)

        if cuisine != "all":
            query += " AND cuisine = ?"
            values.append(cuisine)

        if search_text:
            query += """
                AND (
                    title LIKE ? OR cuisine LIKE ? OR ingredients LIKE ? OR
                    notes LIKE ? OR location LIKE ? OR link LIKE ?
                )
            """
            search_pattern = f"%{search_text}%"
            values.extend([search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern])

        query += " ORDER BY is_favorite DESC, created_at DESC"

        with self.connect() as connection:
            rows = connection.execute(query, values).fetchall()
            return [FoodieItem.from_row(row) for row in rows]

    def get_item(self, item_id):
        with self.connect() as connection:
            row = connection.execute("SELECT * FROM foodie_items WHERE id = ?", (item_id,)).fetchone()
            if row is None:
                return None
            return FoodieItem.from_row(row)

    def update_item(self, item):
        with self.connect() as connection:
            connection.execute(
                """
                UPDATE foodie_items
                SET title = ?, item_type = ?, cuisine = ?, ingredients = ?, location = ?, link = ?,
                    notes = ?, rating = ?, has_tried = ?, is_favorite = ?
                WHERE id = ?
                """,
                (
                    item.title,
                    item.item_type,
                    item.cuisine,
                    item.ingredients,
                    item.location,
                    item.link,
                    item.notes,
                    item.rating,
                    int(item.has_tried),
                    int(item.is_favorite),
                    item.item_id,
                ),
            )

    def delete_item(self, item_id):
        with self.connect() as connection:
            connection.execute("DELETE FROM foodie_items WHERE id = ?", (item_id,))

    def toggle_favorite(self, item_id):
        item = self.get_item(item_id)
        if item is None:
            return

        new_value = 0 if item.is_favorite else 1
        with self.connect() as connection:
            connection.execute("UPDATE foodie_items SET is_favorite = ? WHERE id = ?", (new_value, item_id))

    def get_cuisines(self):
        with self.connect() as connection:
            rows = connection.execute("SELECT DISTINCT cuisine FROM foodie_items ORDER BY cuisine").fetchall()
            return [row["cuisine"] for row in rows]

    def get_stats(self):
        with self.connect() as connection:
            total = connection.execute("SELECT COUNT(*) AS count FROM foodie_items").fetchone()["count"]
            recipes = connection.execute("SELECT COUNT(*) AS count FROM foodie_items WHERE item_type = 'recipe'").fetchone()["count"]
            restaurants = connection.execute("SELECT COUNT(*) AS count FROM foodie_items WHERE item_type = 'restaurant'").fetchone()["count"]
            favorites = connection.execute("SELECT COUNT(*) AS count FROM foodie_items WHERE is_favorite = 1").fetchone()["count"]

        return {
            "total": total,
            "recipes": recipes,
            "restaurants": restaurants,
            "favorites": favorites,
        }

    def seed_sample_data(self):
        if self.get_stats()["total"] > 0:
            return

        samples = [
            FoodieItem("Shrimp and Grits", "recipe", "Southern Comfort Food", "shrimp, grits, garlic, butter, cheddar, green onion", "Home recipe", "https://example.com/shrimp-grits", "Try this on a Sunday dinner night.", 5, True, True),
            FoodieItem("Tacos al Pastor", "recipe", "Mexican", "pork, pineapple, corn tortillas, onion, cilantro", "Family recipe notebook", "", "Add extra pineapple and charred onions.", 0, False, False),
            FoodieItem("Little Italy Pasta Spot", "restaurant", "Italian", "", "Atlanta, GA", "https://example.com/pasta", "Good date night idea.", 5, True, True),
            FoodieItem("Jerk Chicken Plate", "restaurant", "Jamaican", "", "Decatur, GA", "", "Order extra plantains when I visit.", 0, False, False),
            FoodieItem("Ropa Vieja", "recipe", "Cuban", "beef, bell peppers, tomato sauce, onion, garlic", "Online recipe", "https://example.com/ropa-vieja", "Save for meal prep.", 4, True, False),
            FoodieItem("Jollof Rice Night", "recipe", "African Dishes", "rice, tomato stew, peppers, onions, stock", "Shared by a friend", "", "Compare Ghanaian and Nigerian styles.", 5, True, True),
        ]

        for item in samples:
            self.add_item(item)
