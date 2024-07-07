import pandas as pd


# Crear el DataFrame con datos ficticios
data = {
    'ingreso': [2, 12, 67, 89],  # Ingreso en una escala
    'educacion': [1, 6, 13, 16]  # Años de educación
}

df = pd.DataFrame(data)

# Umbrales de pobreza para cada dimensión
umbrales = {
    'ingreso': 30,
    'educacion': 7
}

# Ponderadores para cada dimensión (suman 1)
ponderadores = {
    'ingreso': 1,
    'educacion': 1
}

# Parámetros
alpha = 1  # Ajustar alfa según sea necesario
theta = 1  # Ajustar theta según sea necesario
dim_t = len(umbrales)

# Calcular las brechas de pobreza y el índice BC 
def calcular_bc(df, umbrales, ponderadores, alpha, theta, dim_t):
    df['suma_brechas'] = 0
    for dim, umbral in umbrales.items():
        brecha = []
        for valor in df[dim]:
            if valor < umbral:
                b = (1 - valor / umbral)
            else:
                b = 0
            brecha.append(b)
        brecha = [(ponderadores[dim] / dim_t) * b ** theta for b in brecha]
        df[f'brecha_{dim}'] = brecha
        df['suma_brechas'] += df[f'brecha_{dim}']

    df['suma_brechas'] = [s ** (alpha / theta) if s != 0 else 0 for s in df['suma_brechas']]
    
    # Calcular el índice BC
    bc_index = df['suma_brechas'].sum() / len(df)
    return bc_index

# Calcular BC
bc_index = calcular_bc(df, umbrales, ponderadores, alpha, theta, dim_t)

print(f'Índice de Bourguignon y Chakravarty BC({alpha}, {theta}): {bc_index:.4f}')