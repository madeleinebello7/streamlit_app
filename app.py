import streamlit as st
from vega_datasets import data
source = data.cars()
import matplotlib.pyplot as plt
import altair as alt
from bokeh.models import HoverTool
from bokeh.plotting import figure, show, output_notebook
from bokeh.sampledata.penguins import data
from bokeh.transform import factor_cmap, factor_mark



st.title("Data Visualization web application")

st.header("Part 1: Data Exploration")
st.write("In this section, we will explore the Altair cars dataset.")
st.markdown("*Further resources [here](https://altair-viz.github.io/gallery/selection_histogram.html)*")

slider = st.slider("Slider title", 0, 100, 30)

if slider > 50:
    st.write('Super')


check = st.checkbox("Checkbox title", ["Add a constant", "Add beta 1", "Add beta 2"])
radio = st.radio("Radio title", ["Yes", "No"])
txt = st.text_input("Type here")

if txt:
    st.write(f'tu as écris {txt}')
txt_area = st.text_area("Type here")
button = st.button("Button name")

# Visualization
st.header("Visualization")
choice = st.sidebar.radio("Choisi", ["Matplotlib", "Altair", "Bokeh"])

if choice == 'Matplotlib':

    st.subheader("Matplotlib")

    plt.figure(figsize=(12,8))
    plt.scatter(source['Horsepower'], source['Miles_per_Gallon'])
    st.pyplot(plt)

##ALTAIR
elif choice == 'Altair':
    st.subheader("Altair")
    brush = alt.selection(type='interval')

    points = alt.Chart(source).mark_point().encode(
        x='Horsepower:Q',
        y='Miles_per_Gallon:Q',
        color=alt.condition(brush, 'Origin:N', alt.value('lightgray'))
    ).add_selection(
        brush
    )

    bars = alt.Chart(source).mark_bar().encode(
        y='Origin:N',
        color='Origin:N',
        x='count(Origin):Q'
    ).transform_filter(
        brush
    )

    st.altair_chart(points & bars)

else:

#BOKEH
    st.subheader("Bokeh")

    hover = HoverTool(
        tooltips = [('Label', '@species')], mode='mouse'
    )



    SPECIES = sorted(data.species.unique())
    MARKERS = ['hex', 'circle_x', 'triangle']

    p = figure(title = "Penguin size", 
               background_fill_color="#fafafa",
              tools=[hover, "pan", "crosshair","wheel_zoom", "box_zoom", "reset", "box_select"])

    p.xaxis.axis_label = 'Flipper Length (mm)'
    p.yaxis.axis_label = 'Body Mass (g)'

    p.scatter("flipper_length_mm", 
              "body_mass_g", 
              source=data,
              legend_group="species", 
              fill_alpha=0.4, 
              size=12,
              marker=factor_mark('species', MARKERS, SPECIES),
              color=factor_cmap('species', 'Category10_3', SPECIES))


    p.legend.location = "top_left"
    p.legend.title = "Species"

    st.bokeh_chart(p)