# 📘 cursoPython78315

Repositorio para el curso de Python de **Coderhouse** dictado por *Federico Livingston*.

Entrega N°3: **Biblioteca Nacional de la Juventud**  
Aplicación web desarrollada con Django que permite gestionar libros, autores y categorías con filtros, validaciones y una interfaz moderna basada en Bootstrap.

---

## 📁 Estructura del Proyecto

| Componente         | Ruta                                       |
|--------------------|--------------------------------------------|
| Proyecto principal | `book_library/`                            |
| Aplicación         | `book_library/library/`                    |
| Templates App      | `book_library/library/templates/`          |
| Template base      | `book_library/templates/base.html`         |
| Estilos (CSS)      | `book_library/static/css/`                 |
| Imágenes           | `book_library/static/img/`                 |
| Requisitos         | `requirements.txt`                         |

---

## ⚙️ Funcionalidades Disponibles

### 👤 Modelo `Author` (Autores)
- Listado con filtro por nombre
- Crear, modificar y eliminar autores
- Validación: nombres duplicados no permitidos
- Restricción: no se pueden eliminar autores con libros asociados

### 🗂️ Modelo `Category` (Categorías)
- Listado con filtro por nombre y estado (activo/inactivo)
- Crear, modificar y eliminar categorías
- Validación: nombres duplicados no permitidos
- Restricción: no se pueden eliminar categorías con libros asociados

### 📖 Modelo `Book` (Libros)
- Listado con filtros por título, ISBN y código de biblioteca
- Detalle completo del libro
- Crear, modificar y eliminar libros
- Validaciones:
  - ISBN con formato `999-99-99999-99-9`
  - Código de biblioteca con formato `99-999`
  - Códigos duplicados no permitidos
- Imagen opcional para cada libro

---

## 💾 Base de Datos de Prueba

Se incluye una base de datos con contenido precargado:  
📄 `db.sqlite3.default`

### 🔑 Datos de acceso
Usuario: admin
Contraseña: admin123


### 🧰 Para utilizarla:
1. Renombrar `db.sqlite3.default` a `db.sqlite3`
2. Colocarla en la raíz del proyecto, reemplazando la existente si aplica

---

## ✅ Camino de Testing Sugerido

> Recomendado utilizar la base precargada. Si no, primero crear registros de los modelos.

### 🏠 Home
- Ingreso a la web principal
- Ver presentación del sitio
- Acceso al menú (esquina superior izquierda)

---

### 👤 Autores

- ✅ Filtrar por nombre
- ✅ Crear un nuevo autor
- ✅ Modificar un autor existente
- ⚠️ Intentar crear/modificar un autor con nombre ya existente → debe dar error
- ✅ Eliminar un autor sin libros asociados
- ❌ Eliminar un autor con libros asociados → debe dar error

---

### 🗂 Categorías

- ✅ Filtrar por nombre y estado (activo/inactivo)
- ✅ Crear una nueva categoría
- ✅ Modificar una categoría existente
- ⚠️ Intentar crear/modificar una categoría con nombre ya existente → debe dar error
- ✅ Eliminar una categoría sin libros asociados
- ❌ Eliminar una categoría con libros asociados → debe dar error

---

### 📘 Libros

- ✅ Filtrar por título, ISBN o código de biblioteca
- ✅ Ver detalle del libro
- ✅ Crear un nuevo libro
- ✅ Modificar un libro existente
- ⚠️ Crear/modificar un libro con código duplicado → debe dar error
- ⚠️ Ingresar ISBN o código con formato incorrecto → debe dar error
- ✅ Eliminar un libro

📌 **Nota sobre las imágenes:**  
La imagen es opcional. Si se quiere mostrar una imagen personalizada:
- Indicar el nombre del archivo en el formulario (`ej: portada.jpg`)
- Colocar la imagen en la carpeta:
/book_library/static/img/book_images/

> *La funcionalidad de subida directa desde el formulario aún no está implementada*

---

## 🛠 Instalación del Entorno

Requisitos previos:

- Python 3.10+
- pip (administrador de paquetes)

### ▶️ Instalación

```bash
pip install -r requirements.txt
