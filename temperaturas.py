import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Diccionario de meses
MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

def cargar_datos():
    # Cargar el CSV y pasar el campo "Fecha" a datetime
    try:
        df = pd.read_csv("./csv/Datos_Meteorologicos_Arg_2023.csv")
        df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d/%m/%Y")
        return df
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'Datos_Meteorologicos_Arg_2023.csv'")
        exit()
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        exit()

def obtener_ciudades(df):
    # Devolver una lista de ciudades únicas
    return sorted(df["Ciudad"].unique())

def main():
    print("🌤️ CONSULTOR DE TEMPERATURAS - ARGENTINA 2023 🌤️")
    print("Cargando datos...\n")
    
    df = cargar_datos()
    ciudades = obtener_ciudades(df)
    
    while True:
        # Mostrar ciudades disponibles
        print("Ciudades disponibles:")
        for i, ciudad in enumerate(ciudades, 1):
            print(f"  {i}. {ciudad}")
        
        # Seleccionar ciudad
        try:
            opcion = int(input("\nSeleccione el número de la ciudad: ")) - 1
            if opcion < 0 or opcion >= len(ciudades):
                print("El número no es válido. Inténtelo de nuevo.\n")
                continue
            ciudad = ciudades[opcion]
        except ValueError:
            print("Por favor, ingrese un número válido.\n")
            continue
        
        # Seleccionar mes
        try:
            mes = int(input("\nSeleccione el mes (1-12): "))
            if mes not in range(1, 13):
                print("El mes no es válido. Debe estar entre 1 y 12.\n")
                continue
            nombre_mes = MESES[mes]
        except ValueError:
            print("Por favor, ingrese un número válido.\n")
            continue
        
        # Filtrar los datos
        datos_mes = df[(df["Ciudad"] == ciudad) & (df["Fecha"].dt.month == mes)]
        
        if datos_mes.empty:
            print("No hay datos para esa ciudad en ese mes.\n")
            continue
        
        # Estadísticas simples
        temp_media = (datos_mes["Temperatura Maxima"] + datos_mes["Temperatura Minima"]) / 2
        media_mes = temp_media.mean()
        dia_max = datos_mes.loc[datos_mes["Temperatura Maxima"].idxmax()]
        dia_min = datos_mes.loc[datos_mes["Temperatura Minima"].idxmin()]
        
        # Crear el gráfico
        plt.figure(figsize=(12, 6))
        plt.plot(datos_mes["Fecha"], datos_mes["Temperatura Maxima"], 
                 label="Temperatura Máxima", color="red", marker="o", linewidth=2)
        plt.plot(datos_mes["Fecha"], datos_mes["Temperatura Minima"], 
                 label="Temperatura Mínima", color="blue", marker="o", linewidth=2)
        
        # Rellenar el área entre las curvas
        plt.fill_between(datos_mes["Fecha"], 
                         datos_mes["Temperatura Minima"], 
                         datos_mes["Temperatura Maxima"], 
                         color="lightblue", alpha=0.4)
        
        # Títulos y etiquetas
        plt.title(f"Temperaturas en {ciudad} - {nombre_mes} 2023\n"
                  f"Temperatura media del mes: {media_mes:.1f}°C", 
                  fontsize=16, fontweight="bold")
        plt.xlabel("Fecha")
        plt.ylabel("Temperatura (°C)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        plt.tight_layout() # Ajustar automáticamente el espaciado del gráfico para que nada se corte ni se superponga
        plt.show()
        
        # Mostrar estadísticas
        print(f"\n📊 Estadísticas de {nombre_mes} en {ciudad}:")
        print(f"   • Temperatura media: {media_mes:.1f}°C")
        print(f"   • Día más cálido: {dia_max['Fecha'].strftime('%d/%m')} → {dia_max['Temperatura Maxima']}°C")
        print(f"   • Día más frío:   {dia_min['Fecha'].strftime('%d/%m')} → {dia_min['Temperatura Minima']}°C")
        print(f"   • Días registrados: {len(datos_mes)}\n")
        
        # Preguntar si se desea continuar
        while True:
            seguir = input("¿Desea hacer otra consulta? (s/n): ").strip().lower()
            if seguir in ["s", "si", "y"]:
                print("")
                break
            elif seguir in ["n", "no"]:
                print("\n¡Gracias por usar el consultor!\n")
                return
            else:
                print("Responda con 's' (sí) o 'n' (no).")

# Ejecutar el programa sólo cuando se corre el script directamente
if __name__ == "__main__": 
    main()