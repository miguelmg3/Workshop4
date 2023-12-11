import numpy as np
import pandas as pd
import statsmodels.api as sm
 
# Función para simular el sistema y calcular la longitud promedio de la cola
def simulate_system(interarrival_dist, preparation_dist, recovery_dist, prep_units, rec_units, operation_time, num_simulations=10, num_samples=10):
    queue_lengths = []
 
    for _ in range(num_simulations):
        queue = []
        for _ in range(num_samples):
            interarrival_times = np.random.exponential(scale=interarrival_dist, size=1)
            preparation_times = np.random.exponential(scale=preparation_dist, size=prep_units)
            recovery_times = np.random.exponential(scale=recovery_dist, size=rec_units)
 
            # Simulación del sistema
            for i in range(prep_units):
                queue.append(preparation_times[i])
            for _ in range(rec_units):
                queue.append(recovery_times[_])
            queue.append(operation_time)
 
        queue_lengths.append(len(queue))
 
    return np.mean(queue_lengths)
 
# Configuración de experimentos
interarrival_rates = [25, 22.5]
preparation_dists = [40, (30, 50)]
recovery_dists = [40, (30, 50)]
prep_units = [4, 5]
rec_units = [4, 5]
operation_time = 20
 
# Configuración para serial correlation analysis
serial_corr_config = {
    'interarrival_dist': 25,
    'preparation_dist': 40,
    'recovery_dist': 40,
    'prep_units': 4,
    'rec_units': 4,
    'operation_time': 20,
    'num_simulations': 10,
    'num_samples': 10
}
 
# Ejecutar simulación para la configuración de serial correlation analysis
serial_corr_result = simulate_system(**serial_corr_config)
print(f"Serial Correlation Analysis Result: {serial_corr_result}")
 
# Construir diseño de experimentos para 8 configuraciones
experiments = []
for interarrival_rate in interarrival_rates:
    for preparation_dist in preparation_dists:
        for recovery_dist in recovery_dists:
            for prep_unit in prep_units:
                for rec_unit in rec_units:
                    config = {
                        'interarrival_dist': interarrival_rate,
                        'preparation_dist': preparation_dist,
                        'recovery_dist': recovery_dist,
                        'prep_units': prep_unit,
                        'rec_units': rec_unit,
                        'operation_time': operation_time,
                        'num_simulations': 10,
                        'num_samples': 10
                    }
                    avg_queue_length = simulate_system(**config)
                    experiments.append({'Configuration': config, 'Avg Queue Length': avg_queue_length})
 
# Mostrar resultados de experimentos
experiment_df = pd.DataFrame(experiments)
print("Experimental Design Results:")
print(experiment_df)
 
# Construir modelo de regresión
X = experiment_df[['interarrival_dist', 'preparation_dist', 'recovery_dist', 'prep_units', 'rec_units', 'operation_time']]
X = sm.add_constant(X)
y = experiment_df['Avg Queue Length']
 
model = sm.OLS(y, X).fit()
 
# Mostrar coeficientes del modelo
print("\nRegression Model Coefficients:")
print(model.params)
 
# Interpretar y concluir
print("\nInterpretation and Conclusions:")
print("The coefficients represent the impact of each factor on the average queue length.")
print("Positive coefficients indicate a positive relationship, while negative coefficients suggest a negative relationship.")
print("The magnitude of the coefficient reflects the strength of the influence.")