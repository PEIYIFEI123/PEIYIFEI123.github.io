# Import required libraries
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Solve cross-domain communication issues between front and back ends

# Define core calculation function: input PV capacity and service life, output environmental benefit data
def calculate_env_impact(pv_cap, years):
    # 1. Calculate annual power generation: 1kW PV generates about 1.2 MWh of electricity per year (industry empirical value)
    annual_power = pv_cap * 1.2
    # 2. Calculate annual CO2 reduction: grid emits 0.55 tons of CO2 per MWh; PV lifecycle carbon emissions amortized annually
    co2_reduction = (annual_power * 0.55) - (pv_cap * 0.55 / years)
    # 3. Calculate annual fossil energy replacement: 1kWh ≈ 0.3kg standard coal, converted to tons
    coal_replacement = (annual_power * 1000 * 0.3) / 1000

    # Return calculation results with 2 decimal places
    return {
        "annual_power": round(annual_power, 2),  # Annual power generation (MWh)
        "co2_reduction": round(co2_reduction, 2),  # Annual CO2 reduction (tons)
        "coal_replacement": round(coal_replacement, 2)  # Annual fossil energy replacement (tons of standard coal)
    }

# Define back-end interface: front end calls this address to get calculation results
@app.route('/calculate', methods=['POST'])
def calculate():
    # Get parameters passed from the front end
    data = request.get_json()
    pv_cap = float(data.get('pv_cap'))  # PV capacity (kW)
    years = int(data.get('years'))      # Service life (years)
    # Call the calculation function
    result = calculate_env_impact(pv_cap, years)
    # Return results to the front end
    return jsonify(result)

# Start the back-end service
if __name__ == '__main__':
    app.run(debug=True)  # debug=True: auto-restart after code modification for easy testing