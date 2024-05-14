import psycopg
from passlib.context import CryptContext

class UserConnection():
    conn = None
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self):
        try:
            self.conn = psycopg.connect("dbname=libreria user=postgres password=1234 host=localhost port=5432")
        except psycopg.OperationalError as err:
            print(err)
            self.conn.close()
            
            
    def read_all(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM usuarios")
            return cur.fetchall()

    def read_one(self, id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
            return cur.fetchone()

    def write(self, data):
        with self.conn.cursor() as cur:
            # Encriptar la contraseña antes de almacenarla
            hashed_password = self.hash_password(data["contrasena"])
            data["contrasena"] = hashed_password
            cur.execute("""
                         INSERT INTO usuarios(nombre, mail, contrasena) VALUES
                         (%(nombre)s, %(mail)s, %(contrasena)s)
                         """, data)
            self.conn.commit()

    def update(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
                        UPDATE usuarios SET nombre = %(nombre)s, mail = %(mail)s, contrasena = %(contrasena)s WHERE id = %(id)s
                        """, data)
            self.conn.commit()

    def delete(self, id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
            self.conn.commit()

    def read_all_books(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM libros")
            return cur.fetchall()

    def read_one_book(self, id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM libros WHERE id = %s", (id,))
            return cur.fetchone()

    def write_book(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO libros(nombre, descripcion, propietario) VALUES
                        (%(nombre)s, %(descripcion)s, %(propietario)s)
                        """, data)
            self.conn.commit()

    def update_book(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
                        UPDATE libros SET nombre = %(nombre)s, descripcion = %(descripcion)s, propietario = %(propietario)s
                        WHERE id = %(id)s
                        """, data)
            self.conn.commit()

    def delete_book(self, id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM libros WHERE id = %s", (id,))
            self.conn.commit()



    def __del__(self):
        self.conn.close()