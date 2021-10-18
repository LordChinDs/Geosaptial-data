import pandas as pd
import geopandas as gp
import folium as fo
import streamlit as st
from streamlit_folium import folium_static

import numpy as np
import altair as alt
import pydeck as pdk

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

# Header of page
st.header('Travelling Data')

DATE_TIME = "date/time"

Data_20190101 = pd.read_csv('https://raw.github.com/Maplub/odsample/9cfc6ae4dd6a23e874b60b095d9dfcac11cddbed/20190101.csv')
Data_20190102 = pd.read_csv('https://raw.github.com/Maplub/odsample/9cfc6ae4dd6a23e874b60b095d9dfcac11cddbed/20190102.csv')
Data_20190103 = pd.read_csv('https://raw.github.com/Maplub/odsample/9cfc6ae4dd6a23e874b60b095d9dfcac11cddbed/20190103.csv')
Data_20190104 = pd.read_csv('https://raw.github.com/Maplub/odsample/9cfc6ae4dd6a23e874b60b095d9dfcac11cddbed/20190104.csv')
Data_20190105 = pd.read_csv('https://raw.github.com/Maplub/odsample/9cfc6ae4dd6a23e874b60b095d9dfcac11cddbed/20190105.csv')

@st.cache(persist=True)
def load_data_start(data,nrows):
    data_start = data
    nrows = nrows
    data_start = data_start[['timestart','latstartl','lonstartl']].copy()
    data_start = data_start.rename(columns = {'timestart': 'Date/Time', 'latstartl': 'Lat', 'lonstartl': 'Lon'}, inplace = False)
    lowercase = lambda x: str(x).lower()
    data_start.rename(lowercase, axis="columns", inplace=True)
    data_start[DATE_TIME] = pd.to_datetime( data_start[DATE_TIME])
    return  data_start

@st.cache(persist=True)
def load_data_stop(data,nrows):
    data_stop = data
    nrows = nrows
    data_stop = data_stop[['timestop','latstop','lonstop']].copy()
    data_stop = data_stop.rename(columns = {'timestop': 'Date/Time', 'latstop': 'Lat', 'lonstop': 'Lon'}, inplace = False)
    lowercase = lambda x: str(x).lower()
    data_stop.rename(lowercase, axis="columns", inplace=True)
    data_stop[DATE_TIME] = pd.to_datetime( data_stop[DATE_TIME])
    return  data_stop

#data_start
data_start_20190101 = load_data_start(Data_20190101,100000)
data_start_20190102 = load_data_start(Data_20190102,100000)
data_start_20190103 = load_data_start(Data_20190103,100000)
data_start_20190104 = load_data_start(Data_20190104,100000)
data_start_20190105 = load_data_start(Data_20190105,100000)

#data_stop
data_stop_20190101 = load_data_stop(Data_20190101,100000)
data_stop_20190102 = load_data_stop(Data_20190102,100000)
data_stop_20190103 = load_data_stop(Data_20190103,100000)
data_stop_20190104 = load_data_stop(Data_20190104,100000)
data_stop_20190105 = load_data_stop(Data_20190105,100000)

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
row1_1, row1_2 = st.columns((2,2))

with row1_1:
    hour_selected = st.slider("Select hour of travelling", 0, 23)
    st.write('By Chanin Rakkrai ุ6130804021')

with row1_2:
    st.write(
    """
    ##
    Examining Traveling Data at bangkok
    By sliding the slider hour on the left you can view different slices of time and explore different transportation between 1-5 Jan 2019.
    """)

# FILTERING DATA BY HOUR SELECTED
data_start_20190101 = data_start_20190101[(data_start_20190101[DATE_TIME].dt.hour == hour_selected)]
data_start_20190102 = data_start_20190102[(data_start_20190102[DATE_TIME].dt.hour == hour_selected)]
data_start_20190103 = data_start_20190103[(data_start_20190103[DATE_TIME].dt.hour == hour_selected)]
data_start_20190104 = data_start_20190104[(data_start_20190104[DATE_TIME].dt.hour == hour_selected)]
data_start_20190105 = data_start_20190105[(data_start_20190105[DATE_TIME].dt.hour == hour_selected)]

data_stop_20190101 = data_stop_20190101[(data_stop_20190101[DATE_TIME].dt.hour == hour_selected)]
data_stop_20190102 = data_stop_20190102[(data_stop_20190102[DATE_TIME].dt.hour == hour_selected)]
data_stop_20190103 = data_stop_20190103[(data_stop_20190103[DATE_TIME].dt.hour == hour_selected)]
data_stop_20190104 = data_stop_20190104[(data_stop_20190104[DATE_TIME].dt.hour == hour_selected)]
data_stop_20190105 = data_stop_20190105[(data_stop_20190105[DATE_TIME].dt.hour == hour_selected)]

st.write('''**All Travelling data from %i:00 and %i:00**''' % (hour_selected, (hour_selected + 1) % 24))
#01/01/2019
# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row2_1, row2_2 = st.columns((2,2))

# SETTING THE ZOOM LOCATIONS 
zoom_level = 11
midpoint = [13.7456058, 100.5341187]

with row2_1:
    st.write("** 01 JAN 2019 (Start)**" )
    map(data_start_20190101, midpoint[0], midpoint[1], 11)

with row2_2:
    st.write("** 01 JAN 2019 (Stop)**")
    map(data_stop_20190101, midpoint[0], midpoint[1], 11)

#02/01/2019
# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row3_1, row3_2 = st.columns((2,2))

# SETTING THE ZOOM LOCATIONS 
zoom_level = 11
midpoint = [13.7456058, 100.5341187]

with row3_1:
    st.write("** 02 JAN 2019 (Start)**" )
    map(data_start_20190102, midpoint[0], midpoint[1], 11)

with row3_2:
    st.write("** 02 JAN 2019 (Stop)**")
    map(data_stop_20190102, midpoint[0], midpoint[1], 11)

#03/01/2019
# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row4_1, row4_2 = st.columns((2,2))

# SETTING THE ZOOM LOCATIONS 
zoom_level = 11
midpoint = [13.7456058, 100.5341187]

with row4_1:
    st.write("** 03 JAN 2019 (Start)**" )
    map(data_start_20190103, midpoint[0], midpoint[1], 11)

with row4_2:
    st.write("** 03 JAN 2019 (Stop)**")
    map(data_stop_20190103, midpoint[0], midpoint[1], 11)

#04/01/2019
# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row5_1, row5_2 = st.columns((2,2))

# SETTING THE ZOOM LOCATIONS 
zoom_level = 11
midpoint = [13.7456058, 100.5341187]

with row5_1:
    st.write("** 04 JAN 2019 (Start)**" )
    map(data_start_20190104, midpoint[0], midpoint[1], 11)

with row5_2:
    st.write("** 04 JAN 2019 (Stop)**")
    map(data_stop_20190104, midpoint[0], midpoint[1], 11)

#05/01/2019
# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row6_1, row6_2 = st.columns((2,2))

# SETTING THE ZOOM LOCATIONS 
zoom_level = 11
midpoint = [13.7456058, 100.5341187]

with row6_1:
    st.write("** 05 JAN 2019 (Start)**" )
    map(data_start_20190105, midpoint[0], midpoint[1], 11)

with row6_2:
    st.write("** 05 JAN 2019 (Stop)**")
    map(data_stop_20190105, midpoint[0], midpoint[1], 11)

#1
# FILTERING DATA_start FOR THE HISTOGRAM
filtered_1 = data_start_20190101[(data_start_20190101[DATE_TIME].dt.hour >= hour_selected) & (data_start_20190101[DATE_TIME].dt.hour < (hour_selected + 1))]
hist_1 = np.histogram(filtered_1[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data_1 = pd.DataFrame({"minute": range(60), "start": hist_1})

# LAYING OUT THE HISTOGRAM SECTION
st.write("")
st.write("**Breakdown of 1 JAN 2019 travelling started per minute between  %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
st.altair_chart(alt.Chart(chart_data_1)
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

# FILTERING DATA_stop FOR THE HISTOGRAM
filtered_2 = data_stop_20190101[(data_stop_20190101[DATE_TIME].dt.hour >= hour_selected) & (data_stop_20190101[DATE_TIME].dt.hour < (hour_selected + 1))]
hist_2 = np.histogram(filtered_2[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data_2 = pd.DataFrame({"minute": range(60), "stop": hist_2})

# LAYING OUT THE HISTOGRAM SECTION
st.write("")
st.write("**Breakdown of 1 JAN 2019 travelling stopped per minute between  %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
st.altair_chart(alt.Chart(chart_data_2)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("travelling stop:Q"),
        tooltip=['minute', 'stop']
    ).configure_mark(
        opacity=0.5,
        color='blue'
    ), use_container_width=True)

#2
# FILTERING DATA_start FOR THE HISTOGRAM
filtered_3 = data_start_20190102[(data_start_20190102[DATE_TIME].dt.hour >= hour_selected) & (data_start_20190102[DATE_TIME].dt.hour < (hour_selected + 1))]
hist_3 = np.histogram(filtered_3[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data_3 = pd.DataFrame({"minute": range(60), "start": hist_3})

# LAYING OUT THE HISTOGRAM SECTION
st.write("")
st.write("**Breakdown of 2 JAN 2019 travelling started per minute between  %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
st.altair_chart(alt.Chart(chart_data_3)
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

# FILTERING DATA_stop FOR THE HISTOGRAM
filtered_4 = data_stop_20190102[(data_stop_20190102[DATE_TIME].dt.hour >= hour_selected) & (data_stop_20190102[DATE_TIME].dt.hour < (hour_selected + 1))]
hist_4 = np.histogram(filtered_4[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data_4 = pd.DataFrame({"minute": range(60), "stop": hist_4})

# LAYING OUT THE HISTOGRAM SECTION
st.write("")
st.write("**Breakdown of 2 JAN 2019 travelling stopped per minute between  %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
st.altair_chart(alt.Chart(chart_data_4)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("travelling stop:Q"),
        tooltip=['minute', 'stop']
    ).configure_mark(
        opacity=0.5,
        color='blue'
    ), use_container_width=True)

#3
# FILTERING DATA_start FOR THE HISTOGRAM
filtered_5 = data_start_20190103[(data_start_20190103[DATE_TIME].dt.hour >= hour_selected) & (data_start_20190103[DATE_TIME].dt.hour < (hour_selected + 1))]
hist_5 = np.histogram(filtered_5[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data_5 = pd.DataFrame({"minute": range(60), "start": hist_5})

# LAYING OUT THE HISTOGRAM SECTION
st.write("")
st.write("**Breakdown of 3 JAN 2019 travelling started per minute between  %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
st.altair_chart(alt.Chart(chart_data_5)
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

# FILTERING DATA_stop FOR THE HISTOGRAM
filtered_6 = data_stop_20190103[(data_stop_20190103[DATE_TIME].dt.hour >= hour_selected) & (data_stop_20190103[DATE_TIME].dt.hour < (hour_selected + 1))]
hist_6 = np.histogram(filtered_6[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data_6 = pd.DataFrame({"minute": range(60), "stop": hist_2})

# LAYING OUT THE HISTOGRAM SECTION
st.write("")
st.write("**Breakdown of 3 JAN 2019 travelling stopped per minute between  %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
st.altair_chart(alt.Chart(chart_data_6)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("travelling stop:Q"),
        tooltip=['minute', 'stop']
    ).configure_mark(
        opacity=0.5,
        color='blue'
    ), use_container_width=True)

#4
# FILTERING DATA_start FOR THE HISTOGRAM
filtered_7 = data_start_20190104[(data_start_20190104[DATE_TIME].dt.hour >= hour_selected) & (data_start_20190104[DATE_TIME].dt.hour < (hour_selected + 1))]
hist_7 = np.histogram(filtered_7[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data_7 = pd.DataFrame({"minute": range(60), "start": hist_7})

# LAYING OUT THE HISTOGRAM SECTION
st.write("")
st.write("**Breakdown of 4 JAN 2019 travelling started per minute between  %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
st.altair_chart(alt.Chart(chart_data_7)
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

# FILTERING DATA_stop FOR THE HISTOGRAM
filtered_8 = data_stop_20190104[(data_stop_20190104[DATE_TIME].dt.hour >= hour_selected) & (data_stop_20190104[DATE_TIME].dt.hour < (hour_selected + 1))]
hist_8 = np.histogram(filtered_8[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data_8 = pd.DataFrame({"minute": range(60), "stop": hist_8})

# LAYING OUT THE HISTOGRAM SECTION
st.write("")
st.write("**Breakdown of 4 JAN 2019 travelling stopped per minute between  %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
st.altair_chart(alt.Chart(chart_data_8)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("travelling stop:Q"),
        tooltip=['minute', 'stop']
    ).configure_mark(
        opacity=0.5,
        color='blue'
    ), use_container_width=True)

#5
# FILTERING DATA_start FOR THE HISTOGRAM
filtered_9 = data_start_20190105[(data_start_20190105[DATE_TIME].dt.hour >= hour_selected) & (data_start_20190105[DATE_TIME].dt.hour < (hour_selected + 1))]
hist_9 = np.histogram(filtered_9[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data_9 = pd.DataFrame({"minute": range(60), "start": hist_9})

# LAYING OUT THE HISTOGRAM SECTION
st.write("")
st.write("**Breakdown of 5 JAN 2019 travelling started per minute between  %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
st.altair_chart(alt.Chart(chart_data_9)
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

# FILTERING DATA_stop FOR THE HISTOGRAM
filtered_10 = data_stop_20190105[(data_stop_20190105[DATE_TIME].dt.hour >= hour_selected) & (data_stop_20190105[DATE_TIME].dt.hour < (hour_selected + 1))]
hist_10 = np.histogram(filtered_10[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data_10 = pd.DataFrame({"minute": range(60), "stop": hist_10})

# LAYING OUT THE HISTOGRAM SECTION
st.write("")
st.write("**Breakdown of 5 JAN 2019 travelling stopped per minute between  %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
st.altair_chart(alt.Chart(chart_data_10)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("travelling stop:Q"),
        tooltip=['minute', 'stop']
    ).configure_mark(
        opacity=0.5,
        color='blue'
    ), use_container_width=True)
