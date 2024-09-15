import streamlit as st
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Set the page title
st.set_page_config(page_title='Harmony Splash Project')

# Function to train the model
def train_model():
    # Read the Excel file
    df = pd.read_excel(r"data.xlsx")

    # Drop rows with any NaN values
    df = df.dropna()

    # Encode categorical features
    encoder = OneHotEncoder(sparse_output=False)
    encoded_features = encoder.fit_transform(df[['Activity', 'TimeOfDay', 'Season']])
    encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(['Activity', 'TimeOfDay', 'Season']))

    # Concatenate encoded features with the rest of the data
    df_encoded = pd.concat([df.drop(['Activity', 'TimeOfDay', 'Season'], axis=1), encoded_df], axis=1)

    # Define features and target variable
    X = df_encoded.drop(['UserID', 'DesiredTemp'], axis=1)
    y = df_encoded['DesiredTemp']

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the model
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    st.write(f'Mean Squared Error: {mse}')
    st.write(f'R2 Score: {r2}')

    return model

# Main function for the Streamlit app
def main():
    # Train the model
    model = train_model()

    if model:
        # -------------------- User input ----------------------
        activity = st.selectbox('Select the Activity', ['Shower', 'Hand Washing', 'Dishwashing', 'Laundry'])
        time_of_day = st.selectbox('Select the Time of Day', ['Morning', 'Afternoon', 'Evening'])
        season = st.selectbox('Select the Season', ['Spring', 'Summer', 'Autumn', 'Winter'])

        st.subheader("Select a range of External Temperature")
        external_temp = st.slider("", min_value=-5, max_value=35)

        st.subheader("Select the Room Temperature")
        room_temp = st.slider("", min_value=0, max_value=50)

        st.subheader("Select the Room Humidities")
        room_humidities = st.slider("", min_value=40, max_value=80)

        st.subheader("Select the Flow Rate")
        flow_rate = st.slider("", min_value=5, max_value=50)

        st.subheader("Select the Cold Water Temperature")
        cold_water = st.slider("", min_value=0, max_value=30)

        # Create a DataFrame with the user inputs
        input_data = {
            'ExternalTemp': [external_temp],
            'RoomTemp': [room_temp],
            'RoomHumidity': [room_humidities],
            'FlowRate': [flow_rate],
            'ColdWaterTemp': [cold_water],
            'Activity_Dishwashing': [1 if activity == 'Dishwashing' else 0],
            'Activity_Hand Washing': [1 if activity == 'Hand Washing' else 0],
            'Activity_Laundry': [1 if activity == 'Laundry' else 0],
            'Activity_Shower': [1 if activity == 'Shower' else 0],
            'TimeOfDay_Afternoon': [1 if time_of_day == 'Afternoon' else 0],
            'TimeOfDay_Evening': [1 if time_of_day == 'Evening' else 0],
            'TimeOfDay_Morning': [1 if time_of_day == 'Morning' else 0],
            'Season_Autumn': [1 if season == 'Autumn' else 0],
            'Season_Spring': [1 if season == 'Spring' else 0],
            'Season_Summer': [1 if season == 'Summer' else 0],
            'Season_Winter': [1 if season == 'Winter' else 0]
        }

        input_df = pd.DataFrame(input_data)

        # Predict the desired temperature
        try:
            predicted_temp = model.predict(input_df)
            st.markdown(f'<div style="background-color:green;color:white;padding:10px;border-radius:5px;text-align:center;">Predicted Desired Temperature: {predicted_temp[0]}</div>', unsafe_allow_html=True)    
        except Exception as e:
            st.error(f"Error predicting temperature: {e}")

if __name__ == '__main__':
    main()
