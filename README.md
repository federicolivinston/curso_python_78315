# cursoPython78315
repositorio para el cusrso de python de coderhuse
Segunda Entrega
Se deben descar los archivos, si se va a descargar solo dist recordar tambien descargar ademas de main y setup la carpeta data que contiene los archivos de datos.

Al ejecutar la segunda entrega se tendran dos opciones, login y salir
Para loguearse se deben usar los siguientes datos:
usr: admin
pwd: admin123
o se puede buscar o agregar cualquier usuario en el archivo /data/users.json

una vez logueado el admin se pueden registrar usuarios, mostrar la lista de los mismos, registrar un cliente,
mostrar todos los clientes o solo los activos y desloguearse.
Si se desloguea y no se corta la ejecucion es posible loguearse con cualquiera de los usuarios registrados antes.
Si se utiliza la opcion 99 se sale de la aplicacion pero los usuarios y clientes registrados quedn en los archivos 
en /data por lo que al reejecutar es posible loguearse con cualquier usuario dado de alta en la sesion anterior y lo mismo si se muestran los clientes.

Los pasos sugeridos para probar son:
1. loguearse con admin
2. registrar n usuarios
3. mostrar la lista de usuarios actual
4. Registrar n clientes
5. mostrar la lista de clientes completa (verificar que hay un cliente inactivo)
6. mostrar la lista de clientes activos (verificar que el inactivo no viene)
7. hacer logout
8. salir de la ejecucion
9. volver a ejecutar la app
10. hacer login con algun usuario registrado durante la ejecucion
11. volver a mostrar la lista de usuarios y clientes
12. registrar algun usuario o cliente mas
13. hacer logout
14. salir de la aplicacion con la opcion 99
