# 📦 Ecommerce API

Este documento detalla los endpoints disponibles en la API de Ecommerce.

## 🌐 **Base URL:**
```
http://127.0.0.1:8000/api/
```

---

## 🔐 **Autenticación** (JWT)

### 🟢 **Login**
**Endpoint:**
```
POST /auth/login/
```
**Body:** (JSON)
```json
{
  "email": "admin@example.com",
  "password": "123456"
}
```
**Respuesta Exitosa (200):**
```json
{
  "access": "token_aqui",
  "refresh": "refresh_token_aqui"
}
```

### 🟢 **Registrar Usuario**
**Endpoint:**
```
POST /auth/register/
```
**Body:** (JSON)
```json
{
  "username": "nuevo_user",
  "email": "nuevo@example.com",
  "password": "123456"
}
```

### 🔄 **Refrescar Token**
**Endpoint:**
```
POST /auth/refresh/
```
**Body:** (JSON)
```json
{
  "refresh": "refresh_token_aqui"
}
```

---

## 🛍 **Productos**

### 🔍 **Obtener Todos los Productos**
**Endpoint:**
```
GET /products/
```
**Headers:**
```
Authorization: Bearer token_aqui
```
**Respuesta (200):**
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "price": 1000,
    "category": "laptop",
    "description": "Laptop potente"
  }
]
```

### 🔍 **Obtener Producto por ID**
**Endpoint:**
```
GET /products/{id}/
```

### ➕ **Crear Producto (Admin)**
**Endpoint:**
```
POST /products/
```
**Headers:**
```
Authorization: Bearer token_aqui
```
**Body:** (JSON)
```json
{
  "name": "Celular",
  "price": 500,
  "category": "mobile",
  "description": "Celular de gama alta"
}
```

### 📝 **Actualizar Producto (Admin)**
**Endpoint:**
```
PUT /products/{id}/
```

### 🗑 **Eliminar Producto (Admin)**
**Endpoint:**
```
DELETE /products/{id}/
```

---

## 🛒 **Órdenes**

### 🔍 **Obtener Todas las Órdenes (Admin)**
**Endpoint:**
```
GET /orders/
```

### ➕ **Crear Orden**
**Endpoint:**
```
POST /orders/
```
**Body:** (JSON)
```json
{
  "user": 1,
  "products": [
    { "id": 2, "quantity": 1 },
    { "id": 3, "quantity": 2 }
  ],
  "total_price": 1500
}
```

### 🔍 **Obtener Orden por ID**
**Endpoint:**
```
GET /orders/{id}/
```

### 📝 **Actualizar Estado de Orden (Admin)**
**Endpoint:**
```
PUT /orders/{id}/
```

### 🗑 **Eliminar Orden (Admin)**
**Endpoint:**
```
DELETE /orders/{id}/
```

---

## 👤 **Usuarios**

### 🔍 **Obtener Todos los Usuarios (Admin)**
**Endpoint:**
```
GET /auth/users/
```

### 🔍 **Obtener Usuario por ID**
**Endpoint:**
```
GET /auth/users/{id}/
```

---

## 🔧 **Extras**
- Todas las peticiones **protegidas** requieren autenticación con JWT.
- Para probar los endpoints, puedes usar **Postman** o la interfaz de **Swagger** (`/swagger/`).
- Para obtener un usuario admin, crea uno manualmente en la base de datos o modifica su `role` tras registrarlo.

---

📌 **Hecho con ❤️ para el Ecommerce API** 🚀

## Vamos a instalar pip install python-dotenv

## CREAMOS UN ARCHIVO .ENV Y COLOCAMOS NUESTRAS CREDENCIALES

