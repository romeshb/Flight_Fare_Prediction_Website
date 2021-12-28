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

    if st.button('Show Fare ✈️'):
        # with st.spinner('Wait for it...'):
        #     time.sleep(2)
        # st.success('Done!, Predicted Fare for your Journey is: **Rs.**')
        # pred_fare = model.predict()
        st.write('Predicted Fare for your Journey is: **Rs.**')
    else:
        st.write('Click to Predict the Fare for your trip.')

if __name__ == '__main__':
    main()