from flask import Flask, render_template, request, redirect, url_for, flash
from storage import FoodieDatabase
from models import FoodieItem

app = Flask(__name__)
app.config["SECRET_KEY"] = "foodie-roadmap-dev-key"

database = FoodieDatabase()


@app.route("/")
def home():
    item_type = request.args.get("type", "all")
    cuisine = request.args.get("cuisine", "all")
    search_text = request.args.get("search", "").strip()

    items = database.get_items(item_type=item_type, cuisine=cuisine, search_text=search_text)
    cuisines = database.get_cuisines()
    stats = database.get_stats()

    return render_template(
        "index.html",
        items=items,
        cuisines=cuisines,
        stats=stats,
        selected_type=item_type,
        selected_cuisine=cuisine,
        search_text=search_text,
    )


@app.route("/add", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        item = FoodieItem.from_form(request.form)
        errors = item.validate()

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("form.html", item=item, form_title="Add a Foodie Find")

        database.add_item(item)
        flash("Your foodie find was saved.", "success")
        return redirect(url_for("home"))

    return render_template("form.html", item=None, form_title="Add a Foodie Find")


@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    saved_item = database.get_item(item_id)

    if saved_item is None:
        flash("That item could not be found.", "error")
        return redirect(url_for("home"))

    if request.method == "POST":
        updated_item = FoodieItem.from_form(request.form, item_id=item_id)
        errors = updated_item.validate()

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("form.html", item=updated_item, form_title="Edit Foodie Find")

        database.update_item(updated_item)
        flash("Your foodie find was updated.", "success")
        return redirect(url_for("home"))

    return render_template("form.html", item=saved_item, form_title="Edit Foodie Find")


@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    database.delete_item(item_id)
    flash("The item was removed from your roadmap.", "success")
    return redirect(url_for("home"))


@app.route("/favorite/<int:item_id>", methods=["POST"])
def toggle_favorite(item_id):
    database.toggle_favorite(item_id)
    return redirect(request.referrer or url_for("home"))


@app.route("/seed")
def seed_data():
    database.seed_sample_data()
    flash("Sample recipes and restaurants were added.", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
