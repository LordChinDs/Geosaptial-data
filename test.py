import pandas as pd
import geopandas as gp
import folium as fo
import streamlit as st
from streamlit_folium import folium_static
import altair as alt
import pydeck as pdk
import numpy as np

Data1 = pd.read_csv('https://raw.github.com/Maplub/odsample/9cfc6ae4dd6a23e874b60b095d9dfcac11cddbed/20190101.csv')
Data2 = pd.read_csv('https://raw.github.com/Maplub/odsample/9cfc6ae4dd6a23e874b60b095d9dfcac11cddbed/20190102.csv')
Data3 = pd.read_csv('https://raw.github.com/Maplub/odsample/9cfc6ae4dd6a23e874b60b095d9dfcac11cddbed/20190103.csv')
Data4 = pd.read_csv('https://raw.github.com/Maplub/odsample/9cfc6ae4dd6a23e874b60b095d9dfcac11cddbed/20190104.csv')
Data5 = pd.read_csv('https://raw.github.com/Maplub/odsample/9cfc6ae4dd6a23e874b60b095d9dfcac11cddbed/20190105.csv')

DATE_TIME = "timestart"
Data1[DATE_TIME] = pd.to_datetime(Data1[DATE_TIME])
Data2[DATE_TIME] = pd.to_datetime(Data2[DATE_TIME])
Data3[DATE_TIME] = pd.to_datetime(Data3[DATE_TIME])
Data4[DATE_TIME] = pd.to_datetime(Data4[DATE_TIME])
Data5[DATE_TIME] = pd.to_datetime(Data5[DATE_TIME])

Data1.drop(['Unnamed: 0','latstop','lonstop','timestop','Unnamed: 7','Unnamed: 8','Unnamed: 9','Unnamed: 10','Unnamed: 11'],axis=1,inplace=True)
Data2.drop(['Unnamed: 0','latstop','lonstop','timestop','Unnamed: 7','Unnamed: 8','Unnamed: 9','Unnamed: 10','Unnamed: 11','Unnamed: 12','Unnamed: 13'],axis=1,inplace=True)
Data3.drop(['Unnamed: 0','latstop','lonstop','timestop','Unnamed: 7','Unnamed: 8','Unnamed: 9','Unnamed: 10','Unnamed: 11'],axis=1,inplace=True)
Data4.drop(['Unnamed: 0','latstop','lonstop','timestop','Unnamed: 7','Unnamed: 8','Unnamed: 9','Unnamed: 10','Unnamed: 11'],axis=1,inplace=True)
Data5.drop(['Unnamed: 0','latstop','lonstop','timestop','Unnamed: 7','Unnamed: 8','Unnamed: 9','Unnamed: 10','Unnamed: 11'],axis=1,inplace=True)

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
                get_position=["lonstartl", "latstartl"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))

	# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns((2,3))

with row1_1:
    st.title("BKK  Ridesharing Data")
    hour_selected = st.slider("Select hour of pickup", 0, 23)

with row1_2:
    st.write(
    """
    ##
    Examining how  pickups vary over time in Bangkok City's.
    By sliding the slider on the left you can view different slices of time and explore different transportation trends.
    """)
st.write('Made by Sanhanat Chalanant ')

# FILTERING DATA BY HOUR SELECTED
Data1 = Data1[Data1[DATE_TIME].dt.hour == hour_selected]
Data2 = Data2[Data2[DATE_TIME].dt.hour == hour_selected]
Data3 = Data3[Data3[DATE_TIME].dt.hour == hour_selected]
Data4 = Data4[Data4[DATE_TIME].dt.hour == hour_selected]
Data5 = Data5[Data5[DATE_TIME].dt.hour == hour_selected]




# SETTING THE ZOOM LOCATIONS 
zoom_level = 12
bkk = [13.736717,	100.523186]

st.write('''**All BKK City from %i:00 and %i:00**''' % (hour_selected, (hour_selected + 1) % 24))


#with row3_1:
st.write("** 01/01/2019 **" )
map(Data1, bkk[0], bkk[1], 11)


st.write("** 02/01/2019 **" )
map(Data2, bkk[0], bkk[1], 11)

st.write("** 03/01/2019 **" )
map(Data3, bkk[0], bkk[1], 11)

st.write("** 04/01/2019 **" )
map(Data4, bkk[0], bkk[1], 11)

st.write("** 04/01/2019 **" )
map(Data5, bkk[0], bkk[1], 11)

 
# FILTERING DATA FOR THE HISTOGRAM
filtered1 = Data1[
    (Data1[DATE_TIME].dt.hour >= hour_selected) & (Data1[DATE_TIME].dt.hour < (hour_selected + 1))
    ]

hist1 = np.histogram(filtered1[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

chart_data1 = pd.DataFrame({"minute": range(60), "pickups": hist1})

# LAYING OUT THE HISTOGRAM SECTION

st.write("")

st.write("**Breakdown of rides  in 01/01/2019 per minute between %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))

st.altair_chart(alt.Chart(chart_data1)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=['minute', 'pickups']
    ).configure_mark(
        opacity=0.5,
        color='orange'
    ), use_container_width=True)
#day2

filtered2 = Data2[
    (Data2[DATE_TIME].dt.hour >= hour_selected) & (Data2[DATE_TIME].dt.hour < (hour_selected + 1))
    ]

hist2 = np.histogram(filtered2[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

chart_data2 = pd.DataFrame({"minute": range(60), "pickups": hist2})

# LAYING OUT THE HISTOGRAM SECTION

st.write("")

st.write("**Breakdown of rides in 02/01/2019 per minute between %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))

st.altair_chart(alt.Chart(chart_data2)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=['minute', 'pickups']
    ).configure_mark(
        opacity=0.5,
        color='orange'
    ), use_container_width=True)

#day2

filtered3 = Data3[
    (Data3[DATE_TIME].dt.hour >= hour_selected) & (Data3[DATE_TIME].dt.hour < (hour_selected + 1))
    ]

hist3 = np.histogram(filtered3[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

chart_data3 = pd.DataFrame({"minute": range(60), "pickups": hist3})

# LAYING OUT THE HISTOGRAM SECTION

st.write("")

st.write("**Breakdown of rides in 03/01/2019 per minute between %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))

st.altair_chart(alt.Chart(chart_data3)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=['minute', 'pickups']
    ).configure_mark(
        opacity=0.5,
        color='orange'
    ), use_container_width=True)

#day4

filtered4 = Data4[
    (Data4[DATE_TIME].dt.hour >= hour_selected) & (Data4[DATE_TIME].dt.hour < (hour_selected + 1))
    ]

hist4 = np.histogram(filtered4[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

chart_data4 = pd.DataFrame({"minute": range(60), "pickups": hist4})

# LAYING OUT THE HISTOGRAM SECTION

st.write("")

st.write("**Breakdown of rides in 04/01/2019 per minute between %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))

st.altair_chart(alt.Chart(chart_data4)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=['minute', 'pickups']
    ).configure_mark(
        opacity=0.5,
        color='orange'
    ), use_container_width=True)

#day5

filtered5 = Data5[
    (Data5[DATE_TIME].dt.hour >= hour_selected) & (Data5[DATE_TIME].dt.hour < (hour_selected + 1))
    ]

hist5 = np.histogram(filtered5[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

chart_data5 = pd.DataFrame({"minute": range(60), "pickups": hist5})

# LAYING OUT THE HISTOGRAM SECTION

st.write("")

st.write("**Breakdown of rides in 05/01/2019 per minute between %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))

st.altair_chart(alt.Chart(chart_data5)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=['minute', 'pickups']
    ).configure_mark(
        opacity=0.5,
        color='orange'
    ), use_container_width=True)