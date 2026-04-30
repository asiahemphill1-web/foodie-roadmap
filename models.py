class FoodieItem:
    def __init__(
        self,
        title,
        item_type,
        cuisine,
        ingredients="",
        location="",
        link="",
        notes="",
        rating=0,
        has_tried=False,
        is_favorite=False,
        item_id=None,
    ):
        self.item_id = item_id
        self.title = title.strip()
        self.item_type = item_type.strip().lower()
        self.cuisine = cuisine.strip().title()
        self.ingredients = ingredients.strip()
        self.location = location.strip()
        self.link = link.strip()
        self.notes = notes.strip()
        self.rating = int(rating) if str(rating).strip() else 0
        self.has_tried = bool(has_tried)
        self.is_favorite = bool(is_favorite)

    @classmethod
    def from_form(cls, form_data, item_id=None):
        favorite_value = form_data.get("is_favorite") == "on"
        tried_value = form_data.get("has_tried") == "on"

        return cls(
            item_id=item_id,
            title=form_data.get("title", ""),
            item_type=form_data.get("item_type", ""),
            cuisine=form_data.get("cuisine", ""),
            ingredients=form_data.get("ingredients", ""),
            location=form_data.get("location", ""),
            link=form_data.get("link", ""),
            notes=form_data.get("notes", ""),
            rating=form_data.get("rating", 0),
            has_tried=tried_value,
            is_favorite=favorite_value,
        )

    @classmethod
    def from_row(cls, row):
        return cls(
            item_id=row["id"],
            title=row["title"],
            item_type=row["item_type"],
            cuisine=row["cuisine"],
            ingredients=row["ingredients"],
            location=row["location"],
            link=row["link"],
            notes=row["notes"],
            rating=row["rating"],
            has_tried=bool(row["has_tried"]),
            is_favorite=bool(row["is_favorite"]),
        )

    def validate(self):
        errors = []
        allowed_types = ["recipe", "restaurant"]

        if not self.title:
            errors.append("Please enter a title.")

        if self.item_type not in allowed_types:
            errors.append("Please choose recipe or restaurant.")

        if not self.cuisine:
            errors.append("Please enter a cuisine category.")

        if self.rating < 0 or self.rating > 5:
            errors.append("Rating must be between 0 and 5.")

        if not self.has_tried and self.rating != 0:
            errors.append("Only rate items after you have tried the recipe or visited the restaurant.")

        return errors

    def stars(self):
        if not self.has_tried:
            return "Not tried yet"

        if self.rating == 0:
            return "Tried, not rated yet"

        return "★" * self.rating + "☆" * (5 - self.rating)

    def experience_label(self):
        if self.item_type == "recipe":
            return "Tried" if self.has_tried else "Want to cook"
        return "Visited" if self.has_tried else "Want to visit"
