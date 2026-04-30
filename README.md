# Foodie Roadmap

Foodie Roadmap is a small Flask application for organizing recipes and restaurants by cuisine category with a pretty pink theme. It is designed for foodies who want one simple place to search, filter, rate, and favorite their foodie finds.

## What the app does

- Add recipes or restaurants
- Organize items by cuisine category
- Save ingredients, location, link, and notes in separate fields
- Search by title, cuisine, ingredients, notes, location, or link
- Filter by recipe, restaurant, and cuisine
- Rate recipes and restaurants from 0 to 5 only after marking them as tried or visited
- Heart favorite items
- Edit and delete saved items
- Store data in a local SQLite database
- Creates a delicious foodie roadmap for foodie lovers and friends!

## Project structure

```text
foodie-roadmap/
├── app.py
├── models.py
├── storage.py
├── requirements.txt
├── README.md
├── data/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── templates/
    ├── base.html
    ├── form.html
    └── index.html
```

## How to install the required packages

Create and activate a virtual environment first.

```bash
python -m venv venv
```

On Mac or Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

Then install the required package.

```bash
pip install -r requirements.txt
```

## How to run the application

From inside the `foodie-roadmap` folder, run:

```bash
python app.py
```

Then open the local Flask link shown in the terminal. It is usually:

```text
http://127.0.0.1:5000
```
