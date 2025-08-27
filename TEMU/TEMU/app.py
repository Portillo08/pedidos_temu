# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import database

app = Flask(__name__)

# Asegurarnos de que la base de datos y tablas existan
database.init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    clientes = conn.execute('''
        SELECT c.*, 
               COUNT(p.id) as total_pedidos,
               SUM(pr.precio_venta * pr.cantidad) as total_cobrado,
               SUM(pr.costo_temu * pr.cantidad) as costo_total,
               SUM((pr.precio_venta - pr.costo_temu) * pr.cantidad) as ganancia_total
        FROM clientes c
        LEFT JOIN pedidos p ON c.id = p.cliente_id
        LEFT JOIN productos pr ON p.id = pr.pedido_id
        GROUP BY c.id
    ''').fetchall()
    conn.close()
    return render_template('index.html', clientes=clientes)

@app.route('/cliente/<int:cliente_id>')
def ver_cliente(cliente_id):
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row

    cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,)).fetchone()
    pedidos = conn.execute('SELECT * FROM pedidos WHERE cliente_id = ?', (cliente_id,)).fetchall()

    productos_data = []
    for pedido in pedidos:
        productos = conn.execute('SELECT * FROM productos WHERE pedido_id = ?', (pedido['id'],)).fetchall()
        productos_data.append({'pedido': pedido, 'productos': productos})

    conn.close()
    return render_template('cliente.html', cliente=cliente, productos_data=productos_data)

@app.route('/nuevo_cliente', methods=['GET', 'POST'])
def nuevo_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        conn = sqlite3.connect('data.db')
        conn.execute('INSERT INTO clientes (nombre, telefono, email) VALUES (?, ?, ?)',
                     (nombre, telefono, email))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('nuevo_cliente.html')

@app.route('/nuevo_pedido/<int:cliente_id>', methods=['GET', 'POST'])
def nuevo_pedido(cliente_id):
    if request.method == 'POST':
        # Crear pedido
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO pedidos (cliente_id) VALUES (?)', (cliente_id,))
        pedido_id = cursor.lastrowid

        # Agregar productos
        nombres = request.form.getlist('nombre_producto')
        cantidades = request.form.getlist('cantidad')
        costos = request.form.getlist('costo_temu')
        precios = request.form.getlist('precio_venta')

        for i in range(len(nombres)):
            if nombres[i]:
                cantidad = int(cantidades[i] or 1)
                costo = float(costos[i])
                precio = float(precios[i])
                ganancia = (precio - costo) * cantidad
                cursor.execute('''
                    INSERT INTO productos (pedido_id, nombre, cantidad, costo_temu, precio_venta, ganancia)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (pedido_id, nombres[i], cantidad, costo, precio, ganancia))

        conn.commit()
        conn.close()
        return redirect(url_for('ver_cliente', cliente_id=cliente_id))

    return render_template('nuevo_pedido.html', cliente_id=cliente_id)

if __name__ == '__main__':
    app.run(debug=True)