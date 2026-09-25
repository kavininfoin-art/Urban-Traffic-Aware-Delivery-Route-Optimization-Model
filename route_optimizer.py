import pandas as pd
import networkx as nx
import joblib

MODEL_PATH = "models/traffic_prediction_model.pkl"


def load_model():
    return joblib.load(MODEL_PATH)


def predict_travel_time(model, row):
    input_data = pd.DataFrame(
        [
            {
                "distance_km": row["distance_km"],
                "traffic_level": row["traffic_level"],
                "time_of_day": row["time_of_day"],
                "day_type": row["day_type"],
                "weather": row["weather"],
                "road_type": row["road_type"],
            }
        ]
    )

    return float(model.predict(input_data)[0])


def build_graph(data):
    model = load_model()
    graph = nx.Graph()

    for _, row in data.iterrows():
        predicted_time = predict_travel_time(model, row)

        graph.add_edge(
            row["from_location"],
            row["to_location"],
            weight=predicted_time,
            distance=row["distance_km"],
            traffic=row["traffic_level"],
            road_type=row["road_type"],
        )

    return graph


def optimize_route(data, start_location, delivery_locations):
    graph = build_graph(data)

    current_location = start_location
    remaining_locations = delivery_locations.copy()

    final_route = [start_location]
    total_time = 0
    total_distance = 0

    while remaining_locations:
        best_location = None
        best_path = None
        best_time = float("inf")

        for location in remaining_locations:
            try:
                path = nx.shortest_path(
                    graph,
                    source=current_location,
                    target=location,
                    weight="weight",
                )

                time = nx.shortest_path_length(
                    graph,
                    source=current_location,
                    target=location,
                    weight="weight",
                )

                if time < best_time:
                    best_time = time
                    best_location = location
                    best_path = path

            except nx.NetworkXNoPath:
                continue

        if best_location is None:
            break

        for node in best_path[1:]:
            final_route.append(node)

        total_time += best_time

        for i in range(len(best_path) - 1):
            edge = graph[best_path[i]][best_path[i + 1]]
            total_distance += edge["distance"]

        current_location = best_location
        remaining_locations.remove(best_location)

    return final_route, round(total_time, 2), round(total_distance, 2)