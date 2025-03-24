from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    Float,
    insert,
    text,
)

# Use a persistent SQLite database file
engine = create_engine("sqlite:///database.db")
metadata_obj = MetaData()

# Define 'receipts' table
receipts = Table(
    "receipts",
    metadata_obj,
    Column("receipt_id", Integer, primary_key=True),
    Column("customer_name", String(16)),
    Column("price", Float),
    Column("tip", Float),
)

# Create the table if it doesn't exist
metadata_obj.create_all(engine)

# Function to insert rows into the table
def insert_rows_into_table(rows, table):
    with engine.begin() as connection:
        connection.execute(insert(table), rows)

# Insert sample data if table is empty
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM receipts"))
    count = result.scalar()
    if count == 0:
        rows = [
            {"receipt_id": 1, "customer_name": "Ezekiel Frost", "price": 10.50, "tip": 2.00},
            {"receipt_id": 2, "customer_name": "Marla Dune", "price": 23.75, "tip": 4.50},
            {"receipt_id": 3, "customer_name": "Thorne Blackwood", "price": 55.20, "tip": 6.25},
            {"receipt_id": 4, "customer_name": "Selene Ashford", "price": 32.10, "tip": 3.50},
            {"receipt_id": 5, "customer_name": "Vesper Hawthorne", "price": 19.80, "tip": 2.75},
            {"receipt_id": 6, "customer_name": "Jaxon Raines", "price": 48.60, "tip": 5.00},
            {"receipt_id": 7, "customer_name": "Liora Vale", "price": 27.45, "tip": 3.00},
            {"receipt_id": 8, "customer_name": "Orion Finch", "price": 60.25, "tip": 7.50},
            {"receipt_id": 9, "customer_name": "Calista Morrigan", "price": 38.90, "tip": 4.25},
            {"receipt_id": 10, "customer_name": "Dorian Storm", "price": 50.75, "tip": 6.75},
            {"receipt_id": 11, "customer_name": "Lucian Crowe", "price": 11.90, "tip": 1.50},
            {"receipt_id": 12, "customer_name": "Eris Delacroix", "price": 29.95, "tip": 3.75},
            {"receipt_id": 13, "customer_name": "Zane Evermore", "price": 45.80, "tip": 5.50},
            {"receipt_id": 14, "customer_name": "Isolde Winter", "price": 31.20, "tip": 2.25},
            {"receipt_id": 15, "customer_name": "Galen Hallow", "price": 18.60, "tip": 2.00},
            {"receipt_id": 16, "customer_name": "Sable Whitmore", "price": 54.35, "tip": 6.00},
            {"receipt_id": 17, "customer_name": "Cassian Vex", "price": 28.10, "tip": 3.25},
            {"receipt_id": 18, "customer_name": "Selwyn Fox", "price": 61.45, "tip": 7.75},
            {"receipt_id": 19, "customer_name": "Thalia Rune", "price": 37.20, "tip": 4.00},
            {"receipt_id": 20, "customer_name": "Draven Nocturne", "price": 49.95, "tip": 6.25},
            {"receipt_id": 21, "customer_name": "Kieran Wolfe", "price": 12.75, "tip": 1.75},
            {"receipt_id": 22, "customer_name": "Ember Sterling", "price": 30.60, "tip": 3.50},
            {"receipt_id": 23, "customer_name": "Valko Nightshade", "price": 47.90, "tip": 5.75},
            {"receipt_id": 24, "customer_name": "Ronan Greaves", "price": 33.40, "tip": 3.00},
            {"receipt_id": 25, "customer_name": "Lyra Voss", "price": 20.50, "tip": 2.25},
            {"receipt_id": 26, "customer_name": "Caius Everdark", "price": 53.25, "tip": 6.50},
            {"receipt_id": 27, "customer_name": "Eowyn Vale", "price": 26.80, "tip": 2.75},
            {"receipt_id": 28, "customer_name": "Phoenix Ashen", "price": 59.30, "tip": 7.00},
            {"receipt_id": 29, "customer_name": "Leif Hawthorne", "price": 36.15, "tip": 3.75},
            {"receipt_id": 30, "customer_name": "Zephyr Sterling", "price": 48.75, "tip": 6.00},
            {"receipt_id": 31, "customer_name": "Solene Ardent", "price": 13.90, "tip": 1.25},
            {"receipt_id": 32, "customer_name": "Orpheus Dawn", "price": 31.95, "tip": 2.50},
            {"receipt_id": 33, "customer_name": "Nyx Holloway", "price": 46.85, "tip": 5.25},
            {"receipt_id": 34, "customer_name": "Rowan Nightshade", "price": 32.75, "tip": 3.00},
            {"receipt_id": 35, "customer_name": "Dante Crowley", "price": 22.50, "tip": 2.00},
            {"receipt_id": 36, "customer_name": "Sylas Vex", "price": 55.90, "tip": 6.75},
            {"receipt_id": 37, "customer_name": "Isabeau Winters", "price": 27.85, "tip": 3.25},
            {"receipt_id": 38, "customer_name": "Astra Everhart", "price": 62.10, "tip": 8.00},
            {"receipt_id": 39, "customer_name": "Tiberius Dusk", "price": 39.60, "tip": 4.50},
            {"receipt_id": 40, "customer_name": "Eldric Thorn", "price": 50.95, "tip": 6.25},
        ]
        insert_rows_into_table(rows, receipts)