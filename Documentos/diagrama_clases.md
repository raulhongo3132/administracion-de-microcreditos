-- Diagrama de clases --

Login
+------------------------------------+
| Usuario                            |
+------------------------------------+
|   Usuario   varchar(25)            |
|   Contraseña  varchar(100)         |
|   Intentos  int                    |
+------------------------------------+
|   validarCredenciales()            |
|   cambiarContraseña()              |
|   login()                          |
|   autenticarSesion()               |
+------------------------------------+

+------------------------------------+
| Sesión                             |
+------------------------------------+
|   Id sesión int                    |
|   Estado bool                      |
+------------------------------------+
|   esValida()                       |
|   logout()                         |
+------------------------------------+
