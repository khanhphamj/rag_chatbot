import pandas as pd
import psycopg2
from psycopg2 import sql

# 📝 Cấu hình kết nối và file
DEFAULT_DB = "postgres"
TARGET_DB = "laptop_db"
USER = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = "5432"
EXCEL_FILE_PATH = "laptop_all.xlsx"
CSV_FILE_PATH = "laptop_all_clean.csv"

# ✅ Step 1: Làm sạch dữ liệu từ Excel và lưu thành CSV
try:
    df = pd.read_excel(EXCEL_FILE_PATH)

    # Chọn và đổi tên cột phù hợp với schema PostgreSQL
    df = df[['name', 'price', 'ram', 'ram_unit', 'rom_type', 'rom', 'rom_unit',
             'screen_size', 'screen_detail', 'cpu', 'gpu', 'battery', 'weight',
             'rating', 'links-href', 'brand', 'series']]

    df.rename(columns={
        'links-href': 'link_href'
    }, inplace=True)

    # Loại bỏ giá trị NaN và làm sạch dữ liệu
    df = df.fillna('')

    # Xuất ra CSV
    df.to_csv(CSV_FILE_PATH, index=False)
    print("✅ Excel file successfully cleaned and saved as CSV.")
except Exception as e:
    print(f"❌ Error cleaning Excel file: {e}")
    exit()

# ✅ Step 2: Kết nối với PostgreSQL và tạo database nếu chưa tồn tại
try:
    conn = psycopg2.connect(
        dbname=DEFAULT_DB,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (TARGET_DB,))
    exists = cur.fetchone()

    if not exists:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(TARGET_DB)))
        print(f"✅ Database '{TARGET_DB}' created successfully.")
    else:
        print(f"✅ Database '{TARGET_DB}' already exists.")

    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Error handling database: {e}")
    exit()

# ✅ Step 3: Kết nối tới database đích và tạo bảng nếu chưa tồn tại
try:
    conn = psycopg2.connect(
        dbname=TARGET_DB,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS laptops (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            price TEXT,
            ram INTEGER,
            ram_unit TEXT,
            rom_type TEXT,
            rom INTEGER,
            rom_unit TEXT,
            screen_size FLOAT,
            screen_detail TEXT,
            cpu TEXT,
            gpu TEXT,
            battery TEXT,
            weight FLOAT,
            rating FLOAT,
            link_href TEXT,
            brand TEXT,
            series TEXT
        );
    """)
    print("✅ Table 'laptops' is ready.")
except Exception as e:
    print(f"❌ Error creating table: {e}")
    exit()

# ✅ Step 4: Import dữ liệu từ CSV vào bảng PostgreSQL
try:
    with open(CSV_FILE_PATH, 'r') as f:
        cur.copy_expert(
            "COPY laptops(name, price, ram, ram_unit, rom_type, rom, rom_unit, screen_size, "
            "screen_detail, cpu, gpu, battery, weight, rating, link_href, brand, series) "
            "FROM STDIN WITH CSV HEADER DELIMITER ','",
            f
        )
    print("✅ Data successfully imported into the database.")
except Exception as e:
    print(f"❌ Error importing data into PostgreSQL: {e}")

# ✅ Step 5: Kiểm tra dữ liệu sau khi import
try:
    cur.execute("SELECT COUNT(*) FROM laptops;")
    count = cur.fetchone()[0]
    print(f"✅ Total records in 'laptops': {count}")
except Exception as e:
    print(f"❌ Error verifying data: {e}")

# ✅ Step 6: Đóng kết nối
cur.close()
conn.close()
print("🔒 Connection closed successfully.")
