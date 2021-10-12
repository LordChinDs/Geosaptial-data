import pandas as pd
import geopandas as gp
import folium as fo
import streamlit as st
from streamlit_folium import folium_static

import numpy as np
import altair as alt
import pydeck as pdk

# Header of page
st.header('Travelling Data')

#Sub-header of page
st.subheader('by Chanin 6130804021')

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

# LOADING DATA
DATE_TIME = "date/time"

Data_20190101 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190101.csv")
Data_20190102 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190102.csv")
Data_20190103 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190103.csv")
Data_20190104 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190104.csv")
Data_20190105 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190105.csv")

if date_select == "1/1/2019" :
  DATA = Data_20190101
  d,m,y = 1,1,2019
elif date_select == "2/1/2019" :
  DATA = Data_20190102
  d,m,y = 2,1,2019
elif date_select == "3/1/2019" :
  DATA = Data_20190103
  d,m,y = 3,1,2019
elif date_select == "4/1/2019" :
  DATA = Data_20190104
  d,m,y = 4,1,2019
elif date_select == "5/1/2019" :
  DATA = Data_20190105
  d,m,y = 5,1,2019

@st.cache(persist=True)
def load_data_start(nrows):
    data_start = pd.read_csv(DATA, nrows=nrows)
    data_start = data_start[['timestart','latstartl','lonstartl']].copy()
    data_start = data_start.rename(columns = {'timestart': 'Date/Time', 'latstartl': 'Lat', 'lonstartl': 'Lon'}, inplace = False)
    lowercase = lambda x: str(x).lower()
    data_start.rename(lowercase, axis="columns", inplace=True)
    data_start[DATE_TIME] = pd.to_datetime( data_start[DATE_TIME],format= '%d/%m/%Y %H:%M', errors='ignore'))
    return  data_start

@st.cache(persist=True)
def load_data_stop(nrows):
    data_stop = pd.read_csv(DATA, nrows=nrows)
    data_stop = data_stop[['timestop','latstop','lonstop']].copy()
    data_stop = data_stop.rename(columns = {'timestart': 'Date/Time', 'latstop': 'Lat', 'lonstop': 'Lon'}, inplace = False)
    lowercase = lambda x: str(x).lower()
    data_stop.rename(lowercase, axis="columns", inplace=True)
    data_stop[DATE_TIME] = pd.to_datetime( data_end[DATE_TIME],format= '%d/%m/%Y %H:%M', errors='ignore'))
    return  data_stop

data_1 = load_data_start(100000)

data_2 = load_data_stop(100000)

# CREATING FUNCTION FOR MAPS

def map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.beta_columns((2,2))

with row1_1:
    Date_selected = st.sidebar.selectbox('Select Date', ("1/1/2019", "2/1/2019","3/1/2019","4/1/2019","5/1/2019"))
    hour_selected = st.slider("Select hour of travelling", 0, 23)

with row1_2:
    st.write(
    """
    ##
    Examining Traveling Data at bangkok
    By sliding the slider and selecting date.
    """)

# FILTERING DATA BY HOUR SELECTED
data_1 = data_1[(data_1[DATE_TIME].dt.hour == hour_selected) & (data_1[DATE_TIME].dt.day == d) & (data_1[DATE_TIME].dt.month == m) & (data_1[DATE_TIME].dt.year == y)]
data_2 = data_2[(data_2[DATE_TIME].dt.hour == hour_selected) & (data_2[DATE_TIME].dt.day == d) & (data_2[DATE_TIME].dt.month == m) & (data_2[DATE_TIME].dt.year == y)]

# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row2_1, row2_2 = st.beta_columns((2,2))

# SETTING THE ZOOM LOCATIONS 
midpoint_1 = (np.average(data_1["Lat"]), np.average(data_1["Lon"]))
midpoint_2 = (np.average(data_2["Lat"]), np.average(data_2["Lon"]))

with row2_1:
    st.write("**All start from %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
    map(data_1, midpoint_1[0], midpoint_1[1], 11)

with row2_2:
    st.info("**All stop from %i:00 - %i:00**" % (hour_selected, (hour_selected + 1) % 24))
    map(data_2, midpoint_2[0], midpoint_2[1], 11)

# FILTERING DATA1 FOR THE HISTOGRAM
filtered_1 = data_1[(data_1[DATE_TIME].dt.hour >= hour_selected) & (data_1[DATE_TIME].dt.hour < (hour_selected + 1))]
hist_1 = np.histogram(filtered_1[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data_1 = pd.DataFrame({"minute": range(60), "start": hist_1})

# LAYING OUT THE HISTOGRAM SECTION
st.write("")
st.write("**Breakdown of all travelling started per minute between  %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
st.altair_chart(alt.Chart(chart_data)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("travelling started:Q"),
        tooltip=['minute', 'start']
    ).configure_mark(
        opacity=0.5,
        color='red'
    ), use_container_width=True)

# FILTERING DATA2 FOR THE HISTOGRAM
filtered_2 = data_2[(data_2[DATE_TIME].dt.hour >= hour_selected) & (data_2[DATE_TIME].dt.hour < (hour_selected + 1))]
hist_2 = np.histogram(filtered_2[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data_2 = pd.DataFrame({"minute": range(60), "stop": hist_2})

# LAYING OUT THE HISTOGRAM SECTION
st.write("")
st.write("**Breakdown of all travelling stopped per minute between  %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
st.altair_chart(alt.Chart(chart_data)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("travelling stop:Q"),
        tooltip=['minute', 'stop']
    ).configure_mark(
        opacity=0.5,
        color='green'
    ), use_container_width=True)