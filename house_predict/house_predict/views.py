from django.shortcuts import render
from django.http import JsonResponse
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pandas as pd


def home(request):
    return render(request, 'home.html')

def prediction_page(request):
    return render(request, 'prediction.html')
    
def predict(request):
    if request.method == 'POST':
        # Extract data from POST request
        location_encoded = request.POST.get("location_encoded")  # Corrected field name
        bhk_numeric = request.POST.get("BHK_numeric")  # Corrected field name
        floor_numeric = request.POST.get("Floor_numeric")  # Corrected field name
        furnishing_encoded = request.POST.get("Furnishing_encoded")  # Corrected field name
        car_parking_numeric = request.POST.get("Car Parking_numeric")  # Corrected field name
        super_area_numeric = request.POST.get("Super Area_numeric")  # Corrected field name
        carpet_area_numeric = request.POST.get("Carpet Area_numeric")  # Corrected field name

        # Check if any of the required fields are None
        if None in [location_encoded, bhk_numeric, floor_numeric, furnishing_encoded, car_parking_numeric, super_area_numeric, carpet_area_numeric]:
            return JsonResponse({"error": "Missing required fields"})

        # Convert string values to integers
        try:
            location_encoded = int(location_encoded)
            bhk_numeric = int(bhk_numeric)
            floor_numeric = int(floor_numeric)
            furnishing_encoded = int(furnishing_encoded)
            car_parking_numeric = int(car_parking_numeric)
            super_area_numeric = int(super_area_numeric)
            carpet_area_numeric = int(carpet_area_numeric)
        except ValueError:
            return JsonResponse({"error": "Invalid input format for numeric fields"})

        # Perform prediction using your trained model
        predicted_amount = predict_amount( location_encoded, bhk_numeric, floor_numeric, furnishing_encoded, car_parking_numeric, super_area_numeric, carpet_area_numeric)

        # Return predicted amount as JSON response
        return JsonResponse({"predicted_amount": predicted_amount})

    else:
        return render(request, 'prediction.html')

def predict_amount( location_encoded, bhk_numeric, floor_numeric, furnishing_encoded, car_parking_numeric, super_area_numeric, carpet_area_numeric):
    # Load your dataset
    dataset_path = 'C:/Users/Kevin/Desktop/house predicction/houserate_prediction.csv'
    dataset = pd.read_csv(dataset_path)

    # Assuming 'features' contains the features you want to use for prediction
    # and 'target' contains the target variable (house prices)
    features = dataset[[ 'location_encoded','BHK_numeric', 'Floor_numeric',
                        'Furnishing_encoded', 'Carpet Area_numeric',
                        'Super Area_numeric', 'Car Parking_numeric']]  # Replace with your actual feature names
    target = dataset['Amount(in lakh)']  # Replace with your actual target variable name

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # Initialize the Random Forest Regressor
    random_forest = RandomForestRegressor(n_estimators=100, max_depth=5, min_samples_split=10, random_state=42)

    # Train the model
    random_forest.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = random_forest.predict(X_test)

    # Calculate evaluation metrics
    mse = mean_squared_error(y_test, predictions)
    r_squared = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)

    # Making prediction using the trained model
    new_features = [[location_encoded, bhk_numeric, floor_numeric, furnishing_encoded,  car_parking_numeric, super_area_numeric, carpet_area_numeric]]
    predicted_amount = random_forest.predict(new_features)

    return predicted_amount[0]
