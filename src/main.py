from sensor_extendido import*

# ========================
# Ejemplo de uso
# ========================

if __name__ == "__main__":
    
    # Dependencias
    configuracion = Configuracion(parametros={
        "min_alertas": 5,   
        "timeout": 60,      
        "eval_freq": 3           
    })
    fabrica = FabricaSensores()

    # Mostrar configuración inicial
    print("\n--- CONFIGURACIÓN INICIAL ---")
    configuracion.mostrar()

    # Crear sensores vía fábrica
    sensores = [
        fabrica.crear_sensor("temperatura", "T1"),
        fabrica.crear_sensor("vibracion", "V1"),
        fabrica.crear_sensor("presion", "P1"),
    ]

    # Alimentar sensores con datos
    sensores[0].leer(90)
    sensores[1].leer(3)
    sensores[2].leer(120)

    # Crear notificadores
    notificadores = [
        NotificadorEmail("admin@correo.com"),
        NotificadorWebhook("http://localhost/webhook"),
        NotificadorSMS("+521234567890"),
    ]

    # Crear gestor y evaluar
    gestor = GestorAlertas(sensores, notificadores, configuracion, fabrica)
    gestor.evaluar_y_notificar()

    print("\n=== REPORTE DE ALERTAS ===")
    print(gestor.generar_reporte())

    # Modificar configuración
    print("\n--- MODIFICANDO CONFIGURACIÓN ---")
    configuracion.set("eval_freq", 10)
    configuracion.set("timeout", 120)
    configuracion.set("max_temp", 40) # Se agrega en las configuraciones
    configuracion.mostrar()
