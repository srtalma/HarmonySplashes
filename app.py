import streamlit as st
import pandas as pd
import pickle

# Set the page title
st.set_page_config(page_title='Harmony Splash Project')

def load_model():
    try:
        model_filename = 'model.pkl'  # Adjust the path if the file is in a subfolder
        with open(model_filename, 'rb') as file:
            model = pickle.load(file)
        st.success("Model loaded successfully!")
        return model
    except FileNotFoundError:
        st.error(f"Model file not found at {model_filename}")
    except Exception as e:
        st.error(f"Error loading model: {e}")
    return None

# Main function for the Streamlit app
def main():
    # Load the model
    model = load_model()

    if model:
        # -------------------- User input ----------------------
        activity = st.selectbox('Select the Activity', ['Shower', 'Hand Washing', 'Dishwashing', 'Laundry'], label_visibility="visible")
        time_of_day = st.selectbox('Select the Time of Day', ['Morning', 'Afternoon', 'Evening'], label_visibility="visible")
        season = st.selectbox('Select the Season', ['Spring', 'Summer', 'Autumn', 'Winter'], label_visibility="visible")

        st.subheader("Select a range of External Temperature")
        external_temp = st.slider("External Temperature", min_value=-5, max_value=35, label_visibility="visible") # type slider 

        st.subheader("Select the Room Temperature")
        room_temp = st.slider("Room Temperature", min_value=0, max_value=50, label_visibility="visible") # type slider

        st.subheader("Select the Room Humidities")
        room_humidities = st.slider("Room Humidities", min_value=40, max_value=80, label_visibility="visible") # type slider

        st.subheader("Select the Flow Rate")
        flow_rate = st.slider("Flow Rate", min_value=5, max_value=50, label_visibility="visible") # type slider

        st.subheader("Select the Cold Water Temperature")
        cold_water = st.slider("Cold Water Temperature", min_value=0, max_value=30, label_visibility="visible") # type slider

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
