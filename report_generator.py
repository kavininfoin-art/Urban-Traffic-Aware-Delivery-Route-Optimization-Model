import os
from fpdf import FPDF

os.makedirs("outputs", exist_ok=True)


def generate_pdf_report(route, total_time, total_distance):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Urban Traffic-Aware Delivery Route Optimization Report", ln=True)

    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Optimized Delivery Route:", ln=True)

    route_text = " -> ".join(route)
    pdf.multi_cell(0, 10, route_text)

    pdf.ln(5)

    pdf.cell(0, 10, f"Total Distance: {total_distance} km", ln=True)
    pdf.cell(0, 10, f"Estimated Travel Time: {total_time} minutes", ln=True)

    pdf.ln(10)

    pdf.multi_cell(
        0,
        10,
        "This report was generated using an AI-based traffic-aware delivery route "
        "optimization model. The system predicts road travel time using machine "
        "learning and selects the route with minimum estimated delivery time.",
    )

    output_path = "outputs/route_report.pdf"
    pdf.output(output_path)

    return output_path