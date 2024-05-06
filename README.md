# Anti-DoS-attack
Ya se pondrá una descripción xd

## Inicializar la página web

Primero creamos la imagen de docker:

```docker build -t apache .```

Y la lanzamos en el puerto 8080:

```docker run -d -p 8080:80 apache```