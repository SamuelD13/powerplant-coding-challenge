from flask import Flask, request, jsonify
import logging
from solver import Solver
import json
import requests

app = Flask(__name__)

logging.basicConfig(filename='production_plan.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

@app.route('/productionplan', methods=['POST'])
def production_plan():
    try:
        data = request.get_json()
        if data is None:
            raise ValueError("Invalid or empty JSON data in request.")

        solver = Solver(data)
        result = solver.solve()

        return jsonify(result), 200

    except ValueError as e:
        logging.error(f"ValueError: {e}")
        return jsonify({"error": "Invalid JSON data", "details": str(e)}), 400

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8888)