import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash

# get the data from csv file (already preprocessed)
crashData2 = pd.read_csv("crash_new3.csv")
crashData = crashData2.fillna('?')

external_stylesheets = ['styles.css']

# Initialize the app
app = Dash(__name__, assets_folder='assets')


maxVic = crashData["casualties"].max()


newnames = {'🛧': '🛧 plane', '🚁': '🚁 helicopter', '🛦': '🛦 military'}

# get line size based on the amount of casualties
def getLineSize(casualties):
    vicRange = 4.5 - 1
    relVic = (casualties / maxVic) * vicRange
    return 1 + relVic


fig = px.scatter_geo(crashData,
                     locationmode="ISO-3",
                     lon=crashData['lon_loc'],
                     lat=crashData['lat_loc'],
                     text=crashData['icon'],
                     projection="orthographic",
                     custom_data=[crashData['Year'], crashData['Date'], crashData['Time'], crashData['Location']],
                     symbol=crashData['icon'],
                    )

# Set mode to 'text' to display only text without markers when hovering
fig.update_traces(mode='text', textfont=dict(size=18))
fig.update_traces(hovertemplate="<br><b>Date:</b> %{customdata[1]} %{customdata[0]} <br> <br><b>Time:</b> %{customdata[2]}<br> <br><b>Location:</b> %{customdata[3]}<br>")

fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name]
                                     )
                  )

for i in range(len(crashData)):
    crashPath = crashData["Route"][i]
    crashLoc = crashData["Location"][i]
    numVics = crashData["casualties"][i]

    fig.add_trace(go.Scattergeo(
        locationmode="ISO-3",
        lon=[crashData['lon_start'][i], crashData['lon_loc'][i], crashData['lon_end'][i]],
        lat=[crashData['lat_start'][i], crashData['lat_loc'][i], crashData['lat_end'][i]],
        mode= 'lines+markers',
        line=dict(width=getLineSize(numVics), color='lightgray'),
        marker=dict(size=4),
        name='',
        hovertemplate=
        f'<br><b>Flight path:</b> {crashPath}<br>' + f'<br><b>Crash location:</b> {crashLoc}<br>',
        showlegend=False
    ))
fig.data = fig.data[::-1]

# fig.update_layout(showlegend=False)
fig.update_layout(legend_title_text='Type of aircraft')
fig.update_layout(margin=dict(t=5, b=5, l=0, r=0))

crashData = pd.read_csv("crash_new3.csv")
totalPass = crashData["Casualty Passenger"].sum()
totalCrew = crashData["Casuality Crew"].sum()
totalGround = crashData["Ground"].sum()

pieAboardDF = pd.DataFrame()
totalPassA = crashData["Aboard passengers"].sum()
totalCrewA = crashData["Aboard Crew"].sum()

labels = ['Passengers, survived', 'Crew, survived', 'Passengers, passed away', 'Crew, passed away']
values = [totalPassA - totalPass, totalCrewA - totalCrew, totalPass, totalCrew]
colors = ['lightgreen', 'lightgreen', 'lightgrey', 'lightgrey']

labels2 = ['Passengers', 'Crew', 'Ground']
values2 = [totalPassA, totalCrewA, totalGround]
colors2 = ['lightgrey', 'lightgrey', 'lightgrey']

fig2 = go.Figure(
    data=[
        go.Pie(
            labels=labels,
            values=values,
            textfont_size=20,
            marker=dict(colors=colors, pattern=dict(shape=["", "+", "", "+"])),
            hole=.4,
            direction='clockwise',
            sort=False,
            textinfo='value',
            title=dict(text='People on board', font=dict(size=20)),
            titleposition='top center'
        )
    ]
)
fig2.update_layout(margin=dict(t=0, b=0, l=0, r=0))

bar_data = crashData['Year'].value_counts().reset_index()
bar_data.columns = ['Year', 'Num']

# Create a bar chart using Plotly Express
fig4 = px.bar(bar_data, x='Year', y='Num', title='Crash Count by Year', labels={'Count': 'Crash Count'})
hover_template = '<b>Year:</b> %{x} <br>' + '<b>Crash Count:</b> %{y}'
fig4.update_layout(margin=dict(t=50, b=20, l=100, r=50), title_x=0.4, yaxis_title="#crashes")
fig4.update_traces(marker_color='lightgrey', hovertemplate=hover_template)
# Increase the size of the title
fig4.update_layout(title=dict(text='Crash Count by Year', font_size=20))

# Plane crashes over the past 10 years
app.layout = html.Div([
    html.H1("Plane crashes over the past 10 years", style={'textAlign': 'center', 'fontSize': 40}),
    html.Div(className='container', children=[
        dcc.Graph(className='globe', figure=fig, id='globe'),
        dcc.Graph(className='pie1', figure=fig2, id='pie1'),
        dcc.Graph(className='bar2', figure=fig4, id = 'bar2'),
    ])
])

@app.callback(
    [Output("globe", "figure", allow_duplicate=True), Output("pie1", "figure", allow_duplicate=True)],
    Input("bar2", "clickData"),
    prevent_initial_call=True
)
def fig_click(clickData):
    if clickData is None:
        return fig, fig2

    selected_year = clickData['points'][0]['x']
    filtered_data = crashData[crashData['Year'] == selected_year]

    updated_fig = px.scatter_geo(filtered_data,
                     locationmode="ISO-3",
                     lon=filtered_data['lon_loc'],
                     lat=filtered_data['lat_loc'],
                     text=filtered_data['icon'],
                     projection="orthographic",
                     custom_data=[filtered_data['Year'], filtered_data['Date'], filtered_data['Time'], filtered_data['Location']],
                     symbol=filtered_data['icon'],
                    )

    # Set mode to 'text' to display only text without markers when hovering
    updated_fig.update_traces(mode='text', textfont=dict(size=18))
    updated_fig.update_traces(
        hovertemplate="<br><b>Date:</b> %{customdata[1]} %{customdata[0]} <br> <br><b>Time:</b> %{customdata[2]}<br> <br><b>Location:</b> %{customdata[3]}<br>")

    updated_fig.for_each_trace(lambda t: t.update(name=newnames[t.name],
                                                  legendgroup=newnames[t.name]
                                                  )
                               )

    for i in range(len(filtered_data)):
        crashPath = filtered_data["Route"].iloc[i]
        crashLoc = filtered_data["Location"].iloc[i]
        numVics = filtered_data["casualties"].iloc[i]

        updated_fig.add_trace(go.Scattergeo(
            locationmode="ISO-3",
            lon=[filtered_data['lon_start'].iloc[i], filtered_data['lon_loc'].iloc[i],
                 filtered_data['lon_end'].iloc[i]],
            lat=[filtered_data['lat_start'].iloc[i], filtered_data['lat_loc'].iloc[i],
                 filtered_data['lat_end'].iloc[i]],
            mode='lines+markers',
            line=dict(width=getLineSize(numVics), color='lightgray'),
            marker=dict(size=4),
            name='',
            hovertemplate=
            f'<br><b>Flight path:</b> {crashPath}<br>' + f'<br><b>Crash location:</b> {crashLoc}<br>',
            showlegend=False
        ))

    updated_fig.data = updated_fig.data[::-1]

    # Update layout as needed
    updated_fig.update_layout(legend_title_text='Type of aircraft')
    updated_fig.update_layout(margin=dict(t=5, b=5, l=0, r=0))

    # Update pie chart
    totalPassA = filtered_data["Aboard passengers"].sum()
    totalCrewA = filtered_data["Aboard Crew"].sum()

    totalPass = filtered_data["Casualty Passenger"].sum()
    totalCrew = filtered_data["Casuality Crew"].sum()
    totalGround = filtered_data["Ground"].sum()

    labels = ['Passengers, survived', 'Crew, survived', 'Passengers, passed away', 'Crew, passed away']
    values = [totalPassA - totalPass, totalCrewA - totalCrew, totalPass, totalCrew]
    colors = ['lightgreen', 'lightgreen', 'lightgrey', 'lightgrey']

    fig2_updated = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                textfont_size=20,
                marker=dict(colors=colors, pattern=dict(shape=["", "+", "", "+"])),
                hole=.4,
                direction='clockwise',
                sort=False,
                textinfo='value',
                title=dict(text=f'People on board ({selected_year})', font=dict(size=20)),
                titleposition='top center'
            )
        ]
    )
    fig2_updated.update_layout(margin=dict(t=0, b=0, l=0, r=0))

    # Return both updated figures
    return updated_fig, fig2_updated

@app.callback(
    Output('pie1', 'figure'),
    Input('globe', 'clickData')
)

def update_pie_on_globe(clickData):
    if clickData is None:
        return fig2

    selected_marker_data = clickData['points'][0]['customdata']
    print(selected_marker_data)
    selected_place = selected_marker_data[3]

    # Filter the crashData for the selected year
    filtered_data = crashData[crashData['Location'] == selected_place]

    # Update pie chart
    totalPassA = filtered_data["Aboard passengers"].sum()
    totalCrewA = filtered_data["Aboard Crew"].sum()

    totalPass = filtered_data["Casualty Passenger"].sum()
    totalCrew = filtered_data["Casuality Crew"].sum()
    totalGround = filtered_data["Ground"].sum()

    labels = ['Passengers, survived', 'Crew, survived', 'Passengers, passed away', 'Crew, passed away']
    values = [totalPassA - totalPass, totalCrewA - totalCrew, totalPass, totalCrew]
    colors = ['lightgreen', 'lightgreen', 'lightgrey', 'lightgrey']

    updated_pie_chart = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                textfont_size=20,
                marker=dict(colors=colors, pattern=dict(shape=["", "+", "", "+"])),
                hole=.4,
                direction='clockwise',
                sort=False,
                textinfo='value',
                title=dict(text=f'People on board in {selected_place}', font=dict(size=20)),
                titleposition='top center'
            )
        ]
    )
    updated_pie_chart.update_layout(margin=dict(t=0, b=0, l=0, r=0))

    return updated_pie_chart

if __name__ == '__main__':
    app.run_server(debug=True)