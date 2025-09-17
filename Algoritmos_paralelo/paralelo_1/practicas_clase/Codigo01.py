import threading
import time
import random

def estudiante_thread(id_estudiante, resultados, lock):
    """
    Simula a un estudiante realizando una tarea en paralelo
    """
    # Cada estudiante tarda un tiempo aleatorio en completar su tarea
    tiempo_tarea = random.uniform(1,5)
    
    # Mensaje inicial
    with lock:
        print(f"🎓 Estudiante {id_estudiante} comenzó su tarea (dura {tiempo_tarea:.2f}s)")
    
    # Simular tiempo de trabajo (¡esto es lo que se hace en paralelo!)
    time.sleep(tiempo_tarea)
    
    # Resultado de la tarea
    calificacion = random.randint(60, 100)
    resultado = f"✅ Estudiante {id_estudiante} terminó - Calificación: {calificacion}/100"
    
    # Guardar resultado de manera segura
    #with lock:
    resultados[id_estudiante] = resultado
    print(resultado)

def profesor_thread(resultados, lock, total_estudiantes):
    """
    El profesor supervisa el progreso mientras los estudiantes trabajan
    """
    progreso_anterior = -1
    
    while True:
        with lock:
            progreso_actual = len(resultados)
        
        # Mostrar progreso cada vez que cambie
        if progreso_actual != progreso_anterior:
            if progreso_actual < total_estudiantes:
                print(f"📊 Profesor: {progreso_actual}/{total_estudiantes} estudiantes terminaron")
            progreso_anterior = progreso_actual
        
        # Verificar si todos terminaron
        if progreso_actual >= total_estudiantes:
            break
        
        # El profesor espera un poco antes de revisar nuevamente
        time.sleep(0.3)

def main():
    print("=" * 60)
    print("🏫 SIMULACIÓN DE CLASE PARALELA - SISTEMAS MULTIHILO")
    print("=" * 60)
    print("📚 Cada estudiante es un hilo que trabaja en paralelo")
    print("👨‍🏫 El profesor supervisa el progreso general")
    print("=" * 60)
    
    # Lock para acceso seguro a recursos compartidos
    lock = threading.Lock()
    
    # Diccionario para resultados (recurso compartido)
    resultados = {}
    
    # Número de estudiantes/hilos
    num_estudiantes = 120
    
    print(f"\n🎯 Creando {num_estudiantes} estudiantes (hilos)...")
    time.sleep(1)
    
    # Crear hilos de estudiantes
    hilos_estudiantes = []
    for i in range(num_estudiantes):
        hilo = threading.Thread(
            target=estudiante_thread, 
            args=(i, resultados, lock),
            name=f"Estudiante-{i}"
        )
        hilos_estudiantes.append(hilo)
    
    # Crear hilo del profesor
    hilo_profesor = threading.Thread(
        target=profesor_thread,
        args=(resultados, lock, num_estudiantes),
        name="Profesor"
    )
    
    # Iniciar todos los hilos
    print("\n🚀 Iniciando todos los hilos...")
    time.sleep(1)
    
    # Iniciar profesor primero para que monitoree
    hilo_profesor.start()
    
    # Iniciar estudiantes con pequeño delay para ver el paralelismo
    for i, hilo in enumerate(hilos_estudiantes):
        hilo.start()
        time.sleep(0.1)  # Pequeño delay para ver inicio secuencial
    
    print("\n⏳ Esperando que todos terminen...")
    print("💡 Observa cómo los estudiantes trabajan EN PARALELO!")
    print("-" * 50)
    
    # Esperar a que todos los estudiantes terminen
    for hilo in hilos_estudiantes:
        hilo.join()
    
    # Esperar a que el profesor termine
    hilo_profesor.join()
    
    # Resultados finales
    print("\n" + "=" * 60)
    print("🏆 RESULTADOS FINALES - TODAS LAS TAREAS COMPLETADAS")
    print("=" * 60)
    
    # Calcular estadísticas
    calificaciones = []
    for i in range(num_estudiantes):
        if i in resultados:
            # Extraer calificación del resultado
            linea = resultados[i]
            calificacion = int(linea.split(": ")[1].split("/")[0])
            calificaciones.append(calificacion)
    
    promedio = sum(calificaciones) / len(calificaciones) if calificaciones else 0
    
    print(f"📈 Calificación promedio: {promedio:.1f}/100")
    print(f"🎯 Mejor calificación: {max(calificaciones)}/100")
    print(f"📉 Peor calificación: {min(calificaciones)}/100")
    
    # Información técnica sobre threading
    print("\n" + "=" * 60)
    print("🔧 INFORMACIÓN TÉCNICA SOBRE THREADING")
    print("=" * 60)
    
    print(f"📊 Número total de hilos creados: {num_estudiantes + 1}")
    print(f"👥 Hilos activos al final: {threading.active_count()}")
    print(f"🆔 Hilo principal: {threading.main_thread().name}")
    
    # Mostrar nombres de todos los hilos
    print("\n🧵 Hilos que participaron:")
    for hilo in threading.enumerate():
        print(f"   - {hilo.name}")
    
    # Guardar resultados en archivo
    print(f"\n💾 Guardando resultados en 'resultados_clase.txt'...")
    with open("resultados_clase.txt", "w", encoding="utf-8") as archivo:
        archivo.write("RESULTADOS DE LA CLASE PARALELA\n")
        archivo.write("=" * 40 + "\n\n")
        
        for i in range(num_estudiantes):
            if i in resultados:
                archivo.write(resultados[i] + "\n")
        
        archivo.write(f"\n📊 ESTADÍSTICAS:\n")
        archivo.write(f"Promedio: {promedio:.1f}/100\n")
        archivo.write(f"Mejor: {max(calificaciones)}/100\n")
        archivo.write(f"Peor: {min(calificaciones)}/100\n")
    
    print("✅ Simulación completada exitosamente!")
    return 0

def demostracion_conceptos():
    """
    Función adicional para explicar conceptos clave de threading
    """
    print("\n" + "=" * 60)
    print("📚 EXPLICACIÓN DE CONCEPTOS DE THREADING")
    print("=" * 60)
    
    conceptos = [
        "🧵 THREAD (HILO): Unidad básica de ejecución dentro de un proceso",
        "⚡ PARALELISMO: Múltiples hilos ejecutándose simultáneamente",
        "🔒 LOCK: Mecanismo para acceso seguro a recursos compartidos",
        "⏰ SLEEP: Pausa la ejecución de un hilo por un tiempo determinado",
        "🚀 START(): Inicia la ejecución de un hilo",
        "⏳ JOIN(): Espera a que un hilo termine su ejecución",
        "👨‍🏫 THREAD PRINCIPAL: El hilo que inicia el programa (main)",
        "📊 ACTIVE_COUNT(): Cuenta cuántos hilos están activos",
        "🎯 THREADING.THREAD: Clase para crear y manejar hilos en Python"
    ]
    
    for concepto in conceptos:
        print(concepto)
        time.sleep(0.5)

if __name__ == "__main__":
    # Ejecutar la simulación principal
    main()
    
    # Opcional: mostrar explicación de conceptos
    input("\nPresiona Enter para ver la explicación de conceptos...")
    demostracion_conceptos()
    
    print("\n" + "=" * 60)
    print("🎉 ¡FELICITACIONES! Has entendido los conceptos básicos de threading")
    print("=" * 60)
