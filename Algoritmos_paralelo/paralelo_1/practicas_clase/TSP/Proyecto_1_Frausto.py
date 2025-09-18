from multiprocessing import Pool,cpu_count

class Corredor:
    def __init__(self,total_distancia):
        self.total_distancia = total_distancia
        pass
    
    def calculate_distance(self, individual):
        """Calcular la distancia total de una ruta"""
        total_distance = 0
        for i in range(len(individual)):
            from_city = individual[i]
            to_city = individual[(i + 1) % len(individual)]
            total_distance += self.distance_matrix[from_city][to_city]
        return total_distance