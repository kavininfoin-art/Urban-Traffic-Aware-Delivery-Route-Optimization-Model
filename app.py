import os
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

from route_optimizer import optimize_route
from report_generator import generate_pdf_report

os.makedirs("outputs", exist_ok=True)

st.set_page_config(
    page_title="Urban Traffic-Aware Route Optimization",
    layout="wide"
)

st.title("Urban Traffic-Aware Delivery Route Optimization Model")

st.write(
    "This software predicts traffic-aware travel time and finds the best delivery route."
)

DATA_PATH = "data/traffic_training_data.csv"

data = pd.read_csv(DATA_PATH)

location_coordinates = {
    "Warehouse": [13.0827, 80.2707],
    "A": [13.0674, 80.2376],
    "B": [13.0358, 80.2445],
    "C": [13.0067, 80.2206],
    "D": [13.0475, 80.2090],
    "E": [13.0900, 80.2200],
    "F": [13.1200, 80.2500],
}

st.sidebar.header("Input Settings")

all_locations = sorted(
    list(set(data["from_location"].unique()) | set(data["to_location"].unique()))
)

start_location = st.sidebar.selectbox(
    "Select Start Location",
    all_locations,
    index=all_locations.index("Warehouse")
)

delivery_locations = st.sidebar.multiselect(
    "Select Delivery Locations",
    [loc for loc in all_locations if loc != start_location],
    default=["A", "B", "C", "D"]
)

st.subheader("Existing Road and Traffic Dataset")
st.dataframe(data)

if st.sidebar.button("Optimize Route"):
    if not delivery_locations:
        st.warning("Please select at least one delivery location.")
    else:
        route, total_time, total_distance = optimize_route(
            data,
            start_location,
            delivery_locations
        )

        st.success("Route Optimized Successfully")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Distance", f"{total_distance} km")
        col2.metric("Estimated Time", f"{total_time} min")
        col3.metric("Total Stops", len(route))

        st.subheader("Optimized Route")
        st.write(" → ".join(route))

        result_df = pd.DataFrame(
            {
                "Route Sequence": list(range(1, len(route) + 1)),
                "Location": route,
            }
        )

        st.dataframe(result_df)

        result_df.to_csv("outputs/optimized_route.csv", index=False)

        st.subheader("Route Map")

        first_location = route[0]
        m = folium.Map(
            location=location_coordinates[first_location],
            zoom_start=12
        )

        route_points = []

        for location in route:
            if location in location_coordinates:
                coords = location_coordinates[location]
                route_points.append(coords)

                folium.Marker(
                    location=coords,
                    popup=location,
                    tooltip=location
                ).add_to(m)

        folium.PolyLine(
            route_points,
            weight=5,
            opacity=0.8
        ).add_to(m)

        m.save("outputs/route_map.html")

        st_folium(m, width=900, height=500)

        report_path = generate_pdf_report(route, total_time, total_distance)

        st.subheader("Download Outputs")

        with open("outputs/optimized_route.csv", "rb") as file:
            st.download_button(
                label="Download Optimized Route CSV",
                data=file,
                file_name="optimized_route.csv",
                mime="text/csv"
            )

        with open(report_path, "rb") as file:
            st.download_button(
                label="Download PDF Report",
                data=file,
                file_name="route_report.pdf",
                mime="application/pdf"
            )