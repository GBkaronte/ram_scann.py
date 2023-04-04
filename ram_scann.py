import psutil

# Obtener todos los procesos en ejecución
procesos = list(psutil.process_iter())

# Separar los procesos en dos categorías según su uso de internet
procesos_sin_internet = []
procesos_con_internet = []

for proceso in procesos:
    # Obtener las conexiones del proceso
    try:
        conexiones = proceso.connections()
    except (psutil.AccessDenied, psutil.ZombieProcess):
        # Si no se pueden obtener las conexiones, continuar con el siguiente proceso
        continue

    if conexiones:
        # Si hay conexiones, el proceso usa internet
        procesos_con_internet.append(proceso)
    else:
        # Si no hay conexiones, el proceso no usa internet
        procesos_sin_internet.append(proceso)

# Mostrar los procesos sin internet y su PID
print("******** Procesos sin internet ********")
for proceso in procesos_sin_internet:
    nombre_proceso = proceso.name()
    pid_proceso = proceso.pid
    print(f"{nombre_proceso} (PID {pid_proceso})")

# Mostrar los procesos con internet, su PID, la dirección IP y el puerto utilizado
print("\n******** Procesos con internet ********")
for proceso in procesos_con_internet:
    nombre_proceso = proceso.name()
    pid_proceso = proceso.pid
    conexiones_proceso = proceso.connections()
    for conexion in conexiones_proceso:
        if conexion.status == "LISTEN":
            direccion_ip = conexion.laddr.ip
            puerto = conexion.laddr.port
            print(f"{nombre_proceso} (PID {pid_proceso}) - IP: {direccion_ip} - Puerto: {puerto}")
        else:
            direccion_ip = conexion.raddr.ip
            puerto = conexion.raddr.port
            print(f"{nombre_proceso} (PID {pid_proceso}) - IP: {direccion_ip} - Puerto: {puerto}")
