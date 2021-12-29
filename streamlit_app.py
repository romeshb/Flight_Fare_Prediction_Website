import streamlit as st
import datetime
import time
import sklearn
import pickle
import pandas as pd

# Load the model
pickled_file = open('flightModel.pkl', 'rb')
model = pickle.load(pickled_file)

def main():
    st.set_page_config(
    page_title="Flight Fare Predication WebApp",
    page_icon="✈",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        'Get help': 'https://github.com/romeshb/Flight_Fare_Prediction_Website',
        'Report a bug': "https://github.com/romeshb/Flight_Fare_Prediction_Website/issues/new",
        'About': "# Flight Fare Price Prediction WebApp, Using *Machine Learning*!"
    }
    )
    
    st.title('Know Your Flight Fare ✈')
    st.subheader('Using Machine Learning, get to know your Flight Fares Better.')

    col1, col2 = st.columns([1,1]) # layout of two columns
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    with col1:
        source = st.selectbox("Flying from",["Delhi","Kolkata","Bengaluru","Mumbai","Chennai"])
        dep_date = st.date_input("Departure Date", today)
        #print(dep_date)
        dep_time= st.slider("Departure Time",value = (datetime.time()),step= datetime.timedelta(minutes = 5))
        #print(dep_time)
        numb_stops = st.selectbox("Stops",['Non-Stop','1 Stop','2 Stops','3 Stops'],help='Select Number of Stops')
        #print(numb_stops)
    with col2:
        destination = st.selectbox("Flying to",['New Delhi',"Delhi","Bengaluru",'Hyderabad',"Kolkata",'Cochin'])
        arr_date = st.date_input("Arrival Date", tomorrow)
        arr_time= st.slider("Arrival Time",value = (datetime.time()),step= datetime.timedelta(minutes = 5))
        airline = st.selectbox("Airline",['Jet Airways' , 'Multiple carriers' , 'Air India' ,'Multiple carriers',
                                          'SpiceJet','GoAir','IndiGo','Vistara' ,'Multiple carriers Premium economy',
                                      'Air Asia','Vistara Premium economy'])
    # warning for certain conditions
    if source == destination:
        st.error('Arrival and Destination Cannot be Same.')
    if dep_date > arr_date:
        st.error('Please Select Correct Arrival Date, It Must be Greater than Departure Date.')

    # prediction on button press
    if st.button('Show Fare ✈️'):
        Total_Stops = pd.DataFrame([numb_stops]).replace({'Non-Stop': 0, '1 Stop': 1, '2 Stops': 2, '3 Stops': 3, '4 Stops': 4})[0][0]
        # print(Total_Stops)
        Journey_Month = pd.to_datetime(dep_date, format="%Y-%m-%d").month
        # print('Journey_month',Journey_month)
        Journey_Day = int(pd.to_datetime(dep_date, format="%Y-%m-%d").day)
        # print("Journey_day", Journey_Day)
        Dep_hour = int(pd.to_datetime(dep_time, format="%H:%M:%S").hour)
        # print(Dep_hour)
        Dep_minutes = int(pd.to_datetime(dep_time, format="%H:%M:%S").minute)
        # print(Dep_minutes)
        Arrival_hour = int(pd.to_datetime(arr_time, format="%H:%M:%S").hour)
        # print(Arrival_hour)
        Arrival_minutes = int(pd.to_datetime(arr_time, format="%H:%M:%S").minute)
        # print(Arrival_minutes)

        # Getting Duration_in_mins using Depature Datetime and Arrival Datetime
        Dep_time = "-".join(([dep_date.isoformat(), dep_time.isoformat()]))
        Dep_time = pd.to_datetime(Dep_time, format="%Y-%m-%d-%H:%M:%S")
        # print(Dep_time, 'Depature time')
        Arr_time = "-".join(([arr_date.isoformat(), arr_time.isoformat()]))
        Arr_time = pd.to_datetime(Arr_time, format="%Y-%m-%d-%H:%M:%S")
        # print(Arr_time,'Arrival time')
        Duration_timedelta = Arr_time - Dep_time
        # print(Duration_timedelta, "Duration")
        Duration_in_mins = int(Duration_timedelta.total_seconds() / 60)
        # print(Duration_in_mins, "Duration in Minutes")

        df = pd.DataFrame([[Total_Stops, Journey_Month, Journey_Day, Dep_hour, Dep_minutes, Arrival_hour,
                            Arrival_minutes, Duration_in_mins]],
                          columns=['Total_Stops', 'Journey_Month', 'Journey_Day', 'Dep_hour', 'Dep_minutes',
                                   'Arrival_hour', 'Arrival_minutes', 'Duration_in_mins'])
        # print(df.iloc[[0]])

        # Airline
        Airline_one_hot = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                       columns=['Airline_Air India',
                                                'Airline_GoAir',
                                                'Airline_IndiGo',
                                                'Airline_Jet Airways',
                                                'Airline_Multiple carriers',
                                                'Airline_Multiple carriers Premium economy',
                                                'Airline_SpiceJet',
                                                'Airline_Vistara',
                                                'Airline_Vistara Premium economy'])
        selected_airline = "_".join(("Airline", airline))
        if airline != 'Air Asia':
            Airline_one_hot[selected_airline][0] = 1
        #Airline_one_hot

        # Soure
        Source_one_hot = pd.DataFrame([[0, 0, 0, 0]],
                                      columns=['Source_Chennai',
                                               'Source_Delhi',
                                               'Source_Kolkata',
                                               'Source_Mumbai'])
        selected_source = "_".join(("Source", source))
        if source != "Bengaluru":
            Source_one_hot[selected_source][0] = 1
        #Source_one_hot

        # Destination
        Destination_one_hot = pd.DataFrame([[0, 0, 0, 0, 0]],
                                           columns=['Destination_Cochin',
                                                    'Destination_Delhi',
                                                    'Destination_Hyderabad',
                                                    'Destination_Kolkata',
                                                    'Destination_New Delhi'])
        selected_destination = "_".join(("Destination", destination))
        if destination != "Bengaluru":
            Destination_one_hot[selected_destination][0] = 1
        #Destination_one_hot

        # weekday
        weekday = pd.to_datetime(dep_date, format="%Y-%m-%d").day_name()
        #weekday
        Weekday_one_hot = pd.DataFrame([[0, 0, 0, 0, 0, 0]],
                                       columns=['Weekday_name_of_Journey_Monday',
                                                'Weekday_name_of_Journey_Saturday',
                                                'Weekday_name_of_Journey_Sunday',
                                                'Weekday_name_of_Journey_Thursday',
                                                'Weekday_name_of_Journey_Tuesday',
                                                'Weekday_name_of_Journey_Wednesday'])
        selected_weekday = "_".join(("Weekday_name_of_Journey", weekday))
        if weekday != "Friday":
            Weekday_one_hot[selected_weekday][0] = 1
        #Weekday_one_hot

        # We create list of X variables as used in model training, same sequence.
        # ['Total_Stops', 'Journey_Month', 'Journey_Day', 'Dep_hour',
        #  'Dep_minutes', 'Arrival_hour', 'Arrival_minutes', 'Duration_in_mins',
        #  'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo',
        #  'Airline_Jet Airways', 'Airline_Multiple carriers',
        #  'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
        #  'Airline_Vistara', 'Airline_Vistara Premium economy', 'Source_Chennai',
        #  'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai', 'Destination_Cochin',
        #  'Destination_Delhi', 'Destination_Hyderabad', 'Destination_Kolkata',
        #  'Destination_New Delhi', 'Weekday_name_of_Journey_Monday',
        #  'Weekday_name_of_Journey_Saturday', 'Weekday_name_of_Journey_Sunday',
        #  'Weekday_name_of_Journey_Thursday', 'Weekday_name_of_Journey_Tuesday',
        #  'Weekday_name_of_Journey_Wednesday']


        X = pd.concat([df, Airline_one_hot, Source_one_hot, Destination_one_hot, Weekday_one_hot], axis=1)
        predicted_fare = model.predict(X)

        # with st.spinner('Wait for it...'):
        #     time.sleep(1)
        # st.success('Done!,Predicted Fare for your Journey is: **Rs.{}**'.format(round(predicted_fare[0],2)))

        st.write('Predicted Fare for your Journey is: **Rs.{}**'.format(int(round(predicted_fare[0],0))))
    else:
        st.write('Click to Predict the Fare for your trip.')

if __name__ == '__main__':
    main()
