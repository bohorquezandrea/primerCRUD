from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'productos.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS producto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL
            )
            """
        )

init_db()

# 1. Crear un producto 
@app.route("/api/productos", methods=["POST"])
def crear_producto():
    data = request.get_json()
    if not data or 'nombre' not in data or 'precio' not in data:
        return jsonify({"error": "Faltan campos"}), 400

    with sqlite3.connect(DATABASE) as conn: 
        cursor = conn.execute(
            "INSERT INTO producto (nombre, precio) VALUES (?, ?)",
            (data["nombre"], data["precio"])
        )
        conn.commit()

    return jsonify({"id": cursor.lastrowid}), 201 

# 2. Para enlistar los productos ya dentro de la base de datos 
@app.route("/api/productos", methods=["GET"])
def listar_productos():
    with sqlite3.connect(DATABASE) as conn: 
        cursor = conn.execute("SELECT * FROM producto")

        productos = [
            {"id": row[0], "nombre": row[1], "precio": row[2]}
            for row in cursor.fetchall()
        ]
    return jsonify(productos)

# 3. Actualizar un producto existente
@app.route("/api/productos/<int:id>", methods=["PUT"])
def actualizar_producto(id):
    data = request.json
    with sqlite3.connect(DATABASE) as conn: 
        conn.execute("UPDATE producto SET nombre=?, precio=? WHERE id=?",
            (data["nombre"], data["precio"], id))
        conn.commit()

    return jsonify({"message": "Producto actualizado"})

# 4. Eliminar un producto existente 
@app.route("/api/productos/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(f"DELETE FROM producto WHERE id={id}")
        conn.commit()
    return jsonify({"message": "Producto eliminado"})

# Para inicializar el servidor 
if __name__ == "__main__":
    app.run(debug=True)
