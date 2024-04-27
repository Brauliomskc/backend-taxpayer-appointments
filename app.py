from math import radians, sin, cos, sqrt, atan2
import json
import random

# Función para calcular la distancia entre dos puntos geográficos
def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371.0  # Radio de la Tierra en km

    # Convierte las coordenadas de grados a radianes.
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Calcula la diferencia que hay entre latitudes y longitudes.
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    # Formula de Haversine
    """
    a
    calcula el cuadrado de la mitad del ángulo entre los dos puntos en la latitud y longitud convertidos a radianes. 
    Esto representa la diferencia angular entre los puntos y se usa para calcular la distancia entre ellos.
    """
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    """
    c
     - Calcula la distancia angular (en radianes) entre los dos puntos utilizando la fórmula de Haversine. sqrt(a) y sqrt(1 - a) 
     corresponden a la raíz cuadrada de las partes internas de la fórmula.
     - atan2 se utiliza para calcular el arco tangente del cociente de estas raíces cuadradas, y se multiplica por 2 para 
     obtener la distancia angular entre los puntos.
    """
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    """
    distance
    multiplica la distancia angular por el radio de la Tierra R para obtener la distancia real entre los dos puntos 
    en la superficie de la Tierra, medida en la misma unidad que el radio (en este caso, kilómetros).
    """
    distance = R * c

    return distance

# Función para calcular el score de los clientes
def calculate_score(client, office_lat, office_lon):
    # Ponderaciones a considerar
    age_weight = 0.1 # 10%
    distance_weight = 0.1 # 10%
    accepted_offers_weight = 0.3 # 30%
    canceled_offers_weight = 0.3 # 30%
    reply_time_weight = 0.2 # 20%

    # Calcular distancia a la oficina
    distance = calculate_distance(client["location"]["latitude"], client["location"]["longitude"], office_lat, office_lon)

    """
     Calcular score
     1. Se multiplica la edad por la ponderación y se divide entre 100
     2. Se divide la distancia entre 100, el resultado se divide entre 1 
        para segurar que cuanto más cerca esté el cliente de la oficina 
        principal, mayor será su puntaje.
     3. Se multiplica el número de ofertas aceptadas por la ponderación de las ofertas aceptadas
        y se divide por 100.
     4. Resta el numero de ofertas canceladas, posterior lo multiplica por la ponderación asignada y 
        lo divide entre 1000.
     5. Se multiplica el tiempo promedio de respuesta por la ponderación asignada y se divide entre 100
     6. Por ultimo, todos los componentes se suman para obtener el puntaje total, se multiplica por 10 para 
        que el score este dentro del rango de 1 a 10 
    """ 
    score = (
        (client["age"] * age_weight / 100) + 
        (distance_weight * (1 - (distance / 100))) +
        (client["accepted_offers"] * accepted_offers_weight / 100) +
        ((100 - client["canceled_offers"]) * canceled_offers_weight / 100) +
        (client["average_reply_time"] * reply_time_weight / 1000)
    ) * 10

    # Define el score entre 1 y 10 y lo redondea para que sea entero
    normalized_score = min(max(round(score), 1), 10)

    return normalized_score

# Cargar datos de clientes desde el archivo taxpayers.json
with open('sample-data/taxpayers.json') as f:
    data = json.load(f)

# Coordenadas de la oficina principal
office_lat = 19.3797208
office_lon = -99.1940332

# Agrega datos aleatorios a los clientes que cuenten con poca información
for _ in range(10):
    random_client = {
        "id": "random-" + str(random.randint(1000, 9999)),
        "name": "Random Name",
        "location": {
            "latitude": random.uniform(15, 25),
            "longitude": random.uniform(-105, -90)
        },
        "age": random.randint(18, 100),
        "accepted_offers": random.randint(0, 100),
        "canceled_offers": random.randint(0, 100),
        "average_reply_time": random.randint(200, 4000)
    }
    data.append(random_client)

# Calcula el puntaje para cada cliente
for client in data:
    client["score"] = calculate_score(client, office_lat, office_lon)

# Se agrupan a los clientes por puntaje
score_groups = {}
for client in data:
    score = client["score"]
    if score not in score_groups:
        score_groups[score] = []
    score_groups[score].append(client)

# Seleccionar al menos un cliente de cada puntaje del 1 al 10
selected_clients = []
for score in range(1, 11):
    if score in score_groups:
        random_client = random.choice(score_groups[score])
        selected_clients.append(random_client)

# Si aún no se tienen 10 clientes, se completa seleccionando aleatoriamente de los grupos existentes
while len(selected_clients) < 10:
    all_clients = [client for clients in score_groups.values() for client in clients]
    random_client = random.choice(all_clients)
    selected_clients.append(random_client)

# Ordenar la lista de clientes seleccionados por puntaje descendente
sorted_selected_clients = sorted(selected_clients, key=lambda x: x["score"], reverse=True)

# Mostrar la lista de clientes seleccionados con sus puntajes
print(json.dumps(sorted_selected_clients, indent=4))