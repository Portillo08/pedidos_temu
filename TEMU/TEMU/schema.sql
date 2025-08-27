-- schema.sql
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    email TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    fecha_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado TEXT DEFAULT 'Pendiente',
    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
);

CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER,
    nombre TEXT NOT NULL,
    cantidad INTEGER DEFAULT 1,
    costo_temu REAL NOT NULL,
    precio_venta REAL NOT NULL,
    ganancia REAL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos (id)
);