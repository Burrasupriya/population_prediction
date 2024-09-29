from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd

app = Flask(__name__)


data_copy = joblib.load('data1.joblib')


def predict_population_for_year(country, year):

    country_data = data_copy[data_copy['Country/Territory'] == country]
    
    if country_data.empty:
        return None, None  


    current_population = country_data['2022 Population'].values[0]
    growth_2020_2022 = country_data['Growth_2020_2022'].values[0]

    years_from_2022 = year - 2022
    predicted_population = current_population * (1 + (growth_2020_2022 / 100)) ** years_from_2022
    
    return predicted_population, growth_2020_2022

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    data = request.get_json()
    country = data['country']
    year = int(data['year'])

    predicted_population, predicted_growth = predict_population_for_year(country, year)
    
    if predicted_population is None:
        return jsonify({'error': f"No data available for country: {country}"}), 404

    return jsonify({
        'predicted_population': predicted_population,
        'predicted_growth': predicted_growth
    })

if __name__ == '__main__':
    app.run(debug=True)
