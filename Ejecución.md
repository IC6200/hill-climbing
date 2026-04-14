# Instrucciones de ejecución Hill Climbing.

## Instalar el entorno
Para tener una correcta ejecución del simulador debemos primero 
ejecutar el siguiente comando en la consola:

     python3 -m venv venv
    
luego:

    source venv/bin/activate

Una vez ejecutado esto debemos instalar algunos paquetes que 
nos ayudarán con los siguientes comandos:

    pip install tabulate
    pip install pygame

finalmente podemos ejecutar:

    python3 GUI.py
    
Una vez hecho esto, debemos:
__1- Indicar el tamaño de nuestro mapa__
    Para esto debemos agregar en la interfaz en los campos de texto
    la cantidad de filas y columnas de la matriz

__2- Colocar los elementos en el mapa__
    Presionamos un boton, casa u hospital, si presionamos cualquier campo
    sobre la matriz se verá reflejado, para quitar un elemento presionamos
    el botón de quitar y presionamos en la matriz el elemento a quitar
__3- Iniciar la simulación__
    Para ver la posición óptima de los Hospitales presionamos el botón simular
    y luego se verá en la interfaz el nuevo mapa.