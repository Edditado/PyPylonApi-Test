# PyPylonApi-Test
Prueba del wrapper para Python del Api Pylon de las cámaras Basler, en conjunto con la librería de Visión por Computador OpenCV.

### Repositorio del wrapper
- https://github.com/StudentCV/PyPylon

### Equipos usados en la prueba
- Cámara Basler acA1300-75gc
- Cámara Basler acA1300-60gmNIR
- Switch Cisco Gigabit SG200-08

### Observaciones
- Al conectar 2 o mas cámaras a un computador con una sola tarjeta de red (por medio del switch), se debe tener en cuenta el ancho de banda que ocupará cada cámara. Una solución es seteando los fps adquiridos por cada cámara (Para este caso específico funciona seteando ambas cámaras a 25fps).
- Si se quiere hacer un programa ejecutable con **pyinstaller**, al final del proceso de generación del ejecutable se deben copiar los archivos .dll (.so) del directorio donde se instala el wrapper (../site-packages/pypylon) al directorio del ejecutable, o especificarlos en la variable "datas" del archivo .spec antes de generar el ejecutable.
