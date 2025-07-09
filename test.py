import pandas as pd
import numpy as np


def transformar_recetas():
    # Leer el archivo de recetas
    df_recetas = pd.read_excel('Recetas.xlsx', header=None)

    # Lista para almacenar todas las filas transformadas
    filas_transformadas = []

    # Variables para rastrear el estado actual
    receta_actual = None
    codigo_actual = None

    # Iterar por cada fila del archivo de recetas
    for idx, row in df_recetas.iterrows():
        # Convertir la fila a lista para facilitar el acceso
        valores = row.values

        # Verificar si es una nueva receta
        if pd.notna(valores[0]) and 'Nº de receta:' in str(valores[0]):
            codigo_actual = str(valores[1]).strip() if pd.notna(valores[1]) else None

        # Verificar si es el nombre de la receta
        elif pd.notna(valores[0]) and 'Nombre:' in str(valores[0]):
            receta_actual = str(valores[1]).strip() if pd.notna(valores[1]) else None

        # Verificar si es una fila de ingrediente (tiene datos en las columnas relevantes)
        elif (pd.notna(valores[0]) and pd.notna(valores[1]) and
              pd.notna(valores[3]) and pd.notna(valores[4]) and
              'Código' not in str(valores[0]) and  # Excluir filas de encabezado
              'Maiz y Olivo' not in str(valores[0]) and  # Excluir filas de marca
              receta_actual and codigo_actual):

            # Extraer la información del ingrediente
            codigo_ingrediente = str(valores[0]).strip()
            ingrediente = str(valores[1]).strip() if pd.notna(valores[1]) else ''
            cantidad = str(valores[3]).strip() if pd.notna(valores[3]) else '0'
            unidad = str(valores[4]).strip() if pd.notna(valores[4]) else ''

            # Filtrar ingredientes válidos (excluir filas de costos, factores, etc.)
            if (ingrediente and
                    ingrediente not in ['% de Costo', 'Factor', 'I.V.A.', 'PRECIO ADAPTADO A NUESTRA CARTA'] and
                    'Costo' not in ingrediente and
                    not ingrediente.startswith('$')):
                # Crear la fila transformada
                fila = {
                    'Familia': 'Recetas',  # Valor por defecto
                    'Clave Softrestaurant': '',  # Vacío como en el ejemplo
                    'Producto/Subreceta': receta_actual,
                    'Clave del': codigo_ingrediente,
                    'Insumo O subreceta': ingrediente,
                    'UmED': unidad,
                    'Cant': cantidad,
                    'Cant de rendimie de subrecrta': '1.0',  # Valor por defecto
                    'Unnamed: 8': ''  # Columna vacía adicional
                }

                filas_transformadas.append(fila)

    # Crear el DataFrame con las filas transformadas
    df_nuevas_recetas = pd.DataFrame(filas_transformadas)

    # Eliminar duplicados si los hay
    df_nuevas_recetas = df_nuevas_recetas.drop_duplicates()

    # Leer el archivo de formato existente para preservar su contenido
    try:
        df_existente = pd.read_excel('Formato_insumos.xlsx')

        # Concatenar los datos existentes con las nuevas recetas
        df_combinado = pd.concat([df_existente, df_nuevas_recetas], ignore_index=True)

    except FileNotFoundError:
        # Si el archivo no existe, usar solo las nuevas recetas
        df_combinado = df_nuevas_recetas
        print("Archivo Formato_insumos.xlsx no encontrado, se creará uno nuevo.")

    # Guardar el resultado en la primera hoja del archivo
    df_combinado.to_excel('Formato_insumos.xlsx', index=False)

    print(
        f"Transformación completada. Se procesaron {len(filas_transformadas)} ingredientes de {len(df_nuevas_recetas['Producto/Subreceta'].unique())} recetas diferentes.")

    # Mostrar resumen de ingredientes por receta
    print("\nResumen de ingredientes por receta:")
    for receta in df_nuevas_recetas['Producto/Subreceta'].unique():
        cantidad = len(df_nuevas_recetas[df_nuevas_recetas['Producto/Subreceta'] == receta])
        print(f"- {receta}: {cantidad} ingredientes")

    return df_nuevas_recetas


# Ejecutar la función
if __name__ == "__main__":
    df_resultado = transformar_recetas()