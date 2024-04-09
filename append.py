import pandas as pd
import os

def merge_excel_files_with_goal(fulfillment_folder, extras_folder, output_folder, total_goal):
    # Leer el archivo de la carpeta fulfillment
    fulfillment_file = [f for f in os.listdir(fulfillment_folder) if f.endswith('.xlsx')][0]
    df_fulfillment = pd.read_excel(os.path.join(fulfillment_folder, fulfillment_file), engine='openpyxl')
    
    # Leer el archivo de la carpeta extras
    extras_file = [f for f in os.listdir(extras_folder) if f.endswith('.xlsx')][0]
    df_extras = pd.read_excel(os.path.join(extras_folder, extras_file), engine='openpyxl')
    
    # Usar esta línea si decides predefinir county y property_type para el ejemplo
    df_extras_filtered = df_extras
    
    # Remover duplicados en df_extras_filtered antes de combinarlo
    df_extras_filtered.drop_duplicates(subset=['OWNER FULL NAME', 'ADDRESS', 'ZIP', 'MAILING ADDRESS', 'MAILING ZIP'], inplace=True)
    
    # Calcular cuántas propiedades se necesitan del archivo extras después de filtrar
    current_properties_count = len(df_fulfillment)
    needed_properties_count = total_goal - current_properties_count
    
    if needed_properties_count > 0:
        # Ordenar df_extras_filtered y tomar las mejores propiedades según el criterio definido
        df_extras_best_properties = df_extras_filtered.sort_values(by=['SCORE', 'LIKELY DEAL SCORE', 'BUYBOX SCORE'], ascending=[False, False, False]).head(needed_properties_count)
        
        # Asegurarse de que df_extras_best_properties solo incluya columnas de df_fulfillment
        df_extras_best_properties = df_extras_best_properties.reindex(columns=df_fulfillment.columns)
        
        # Combinar los archivos manteniendo solo las columnas de df_fulfillment
        df_combined = pd.concat([df_fulfillment, df_extras_best_properties], ignore_index=True)
    else:
        df_combined = df_fulfillment
    
    # Ordenar el DataFrame combinado por SCORE, LIKELY DEAL SCORE y BUYBOX SCORE en orden descendente
    df_combined.sort_values(by=['SCORE', 'LIKELY DEAL SCORE', 'BUYBOX SCORE'], ascending=[False, False, False], inplace=True)
    
    # Guardar el archivo combinado y limpio en la carpeta de salida
    output_file_path = os.path.join(output_folder, 'combined_properties.xlsx')
    df_combined.to_excel(output_file_path, index=False, engine='openpyxl')
    
    return f"Archivo combinado creado en: {output_file_path}"

# Solicitar al usuario el número total de propiedades deseado
goal_total = int(input("Por favor, ingresa el objetivo total de propiedades: "))

# Llamar a la función con los parámetros necesarios
merge_excel_files_with_goal('fulfillment', 'extras', 'output', goal_total)

