# 📘 cursoPython78315

Repositorio para el curso de Python de **Coderhouse** de *Federico Livingston*.

Entrega Final: **Biblioteca Nacional de la Juventud**  
Aplicación web desarrollada con Django que permite gestionar libros, autores y categorías con filtros, validaciones y una interfaz moderna basada en Bootstrap.

---

## 📁 Estructura del Proyecto

| Componente         | Ruta                                       |
|--------------------|--------------------------------------------|
| Proyecto principal | `book_library/`                            |
| Aplicación         | `book_library/library/`                    |
| Templates App      | `book_library/library/templates/`          |
| Aplicación         | `book_library/library_user/`               |
| Templates App      | `book_library/library_user/templates/`     |
| Template base      | `book_library/templates/base.html`         |
| Template 404       | `book_library/templates/404.html`          |
| Estilos (CSS)      | `book_library/static/css/`                 |
| Imágenes           | `book_library/static/img/`                 |
| Media              | `book_library/media/`                      |
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
- Reservar / Devolver libro
- Crear, modificar y eliminar libros
- Validaciones:
  - ISBN con formato `999-99-99999-99-9`
  - Código de biblioteca con formato `99-999`
  - Códigos duplicados no permitidos
- Imagen opcional para cada libro

### 👤 Modelo `User` (Modelo auth user de django)
- Registrar usuario
- LogIn / LogOut a la aplicacion
- Ver perfil completo del usuario
- Editar Perfil
- Cambiar Contraseña

### 🖼️ Modelo `Avatar` (Avatar del usuario)
- Agregar, modificar o eliminar el avatar del usuario

---

## 💾 Datos de Prueba

Se incluye una base de datos con contenido precargado:  
📄 `db.sqlite3.default`

Se incluyen las imagenes de los dos libros de prueba en la carpeta:
📂 `media/` — Archivos subidos por usuarios (imágenes de libros, avatares, etc.)

### 🔑 Datos de acceso
Usuario comun: 
Usuario: user
Contraseña: user123

Usuario administrador
Usuario: admin
Contraseña: admin123

### 🧰 Para utilizarla:
1. Renombrar `db.sqlite3.default` a `db.sqlite3`
2. Colocarla en la raíz del proyecto, reemplazando la existente si aplica

---

# ✅ Camino de Testing Sugerido

> Recomendado utilizar la base precargada. Si no, primero crear registros de los modelos.

## Acceso Anonimo

### 🏠 Home
- ✅ Ingreso a la web principal
- ✅ Ver presentación del sitio
- ✅ Acceso al menú (esquina superior izquierda)
- ✅ Ver la seccion Conocenos
- ✅ Acceder al listado de libros
- ✅ Filtrar por alguno de los filtros
- ✅ Ver el detalle de un libro
- ✅ Acceder al login
- ✅ Registrar un usuario
- ❌ Intentar registrar un usurio diferente con el mismo nombre de usuario → debe dar error

## Acceso con usuario registrado
- ✅ Loguearse con el usuario registrado
- ✅ Acceder al menu → verificar que tengo las opciones de logout y ver perfil en vez de login
- ✅ Acceder al listado de libros
- ✅ Filtrar por alguno de los filtros
- ✅ ver el detalle de un libro → debe aparece la opcion Reservar
- ✅ Reservar el libro → debe cambiar el estado a reservado y aparecer la opcion Devolver
- ✅ Devolver el libro → debe cambiar el estado a Disonible y aparecer la opcion Reservar
- ✅ Volver a reservar el libro y dejarlo reservado para pruebas futuras.
- ✅ Acceder al perfil del usuario → deben aparecer los datos del usuario y un avatar default 
- ✅ Acceder modificar el avatar y subir una imagen → debe modificarse la imagen en el perfil y en el encabezado a la derecha
- ✅ Acceder a modificar perfil y marcar eliminar → debe volver al avatar default.
- ✅ Acceder a modificar datos y modificarlos → verificar que el campo email verifica el formato
- ✅ Acceder a cambiar contraseña y cambiarla → debe mantenerse logueado y volver al perfil

## Acceso con usuario user
- ✅ Loguearse con el usuario user o un usario distinto al usado antes
- ✅ Acceder al listado de libros → verificar que el libro reservado antes tenga el estado correcto
- ✅ Acceder al detalle del libro reservado → verificar que no aparecen las opciones reservar/devolver

## Acceso con usuario admin
Si no se utiliza la base adjunta se debe crear un grupo admin y asignarselo al superusuario
- ✅ Acceder con el usuario admin
- ✅ Verificar que aparecen las opciones de administracion de autores, categorias y libros

Ejecutar las siguientes acciones por modelo:
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

---

## 🛠 Instalación del Entorno

Requisitos previos:

- Python 3.10+
- pip (administrador de paquetes)

### ▶️ Instalación

```bash
pip install -r requirements.txt

**Incluir migraciones en caso de que usen base de datos vacía:**

```bash
python manage.py makemigrations
python manage.py migrate