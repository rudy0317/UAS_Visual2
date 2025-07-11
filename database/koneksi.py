import pymysql

def create_connection():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="sia_rudy_2310010148",
            port=1111
        )
        print("✅ Koneksi berhasil!")
        return conn
    except Exception as e:
        print("❌ Gagal koneksi:", e)
        return None
