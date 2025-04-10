import os
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

df_q1 = pd.read_csv(os.path.join(os.getcwd(), 'q1.csv'), encoding='utf-8-sig')
# Filtering data for q1
df_q1 = df_q1[['GEO', 'Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)', 'Gender (3)', 'VALUE']]
df_q1 = df_q1[df_q1['Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)'].str.contains('|'.join(['nurse', 'police', 'firefighter']), case=False)]
df_q1 = df_q1[df_q1['Gender (3)'].isin(['Men+', 'Women+'])]
df_q1 = df_q1[df_q1['Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)'] != 'Total - Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)']

df_q2 = pd.read_csv(os.path.join(os.getcwd(), 'q2.csv'), encoding='utf-8-sig')
# Filtering for q2
df_q2 = df_q2[df_q2['Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)'].str.match(r'^[0-3]', na=False)]
df_q2 = df_q2[df_q2['Gender (3)'].isin(['Men+', 'Women+'])]
df_q2 = df_q2.groupby(['GEO', 'Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)', 'Gender (3)'])['VALUE'].sum().reset_index()

df_q3 = pd.read_csv(os.path.join(os.getcwd(), 'q3.csv'), encoding='utf-8-sig')
# Filtering for q3
df_q3 = df_q3[df_q3['Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)'].str.contains('|'.join(['computer', 'mechanical', 'electrical']), case=False, na=False)]
df_q3 = df_q3.groupby(['GEO', 'Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)', 'Gender (3)'])['VALUE'].sum().reset_index()

app = dash.Dash(__name__)
server = app.server

# q1 figure
fig_q1 = px.bar(df_q1,
                x='Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)',
                y='VALUE',
                color='Gender (3)',
                title="Distribution of Essential Services (Nurses, Police, Firefighters)",
                labels={
                    "Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)": "Job Category",
                    "VALUE": "Number of People", "Gender (3)": "Gender"},
                barmode='group')

# q2 figure
fig_q2 = px.bar(df_q2,
                x='Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)',
                y='VALUE',
                color='Gender (3)',
                title="Employment Statistics by Gender for Highest Level NOC Codes (0-4)",
                labels={
                    "Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)": "Occupation",
                    "VALUE": "Number of People", "Gender (3)": "Gender"},
                barmode='group',
                opacity=0.8,
                width=500)

# q3 figure
fig_q3 = px.bar(df_q3,
                x='Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)',
                y='VALUE',
                color='Gender (3)',
                title="Manpower Availability for Engineers in Electronic Vehicle Factory",
                labels={
                    "Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)": "Occupation",
                    "VALUE": "Number of Engineers", "Gender (3)": "Gender"},
                barmode='group')

app.layout = html.Div([
    html.H1("Dashboard: Employment and Human Resource Distribution", style={'text-align': 'center'}),
    
    html.Div([
        dcc.Graph(id='essential-services-bar', figure=fig_q1),
        html.Label("Select Job Category for Essential Services:"),
        dcc.Dropdown(
            id='job-category-dropdown',
            options=[{'label': job, 'value': job} for job in df_q1['Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)'].unique()],
            value='32101 Licensed practical nurses',
            style={'width': '50%'}
        ),
        html.Label("Select Province for Essential Services:"),
        dcc.Dropdown(
            id='province-dropdown-q1',
            options=[{'label': province, 'value': province} for province in df_q1['GEO'].unique()],
            value='Ontario',
            style={'width': '50%'}
        ),
    ], style={'padding': '20px'}),

    html.Div([
        dcc.Graph(id='gender-employment-bar', figure=fig_q2),
    ], style={'padding': '20px'}),

    html.Div([
        html.Label("Select province for Question 2:"),
        dcc.Dropdown(
            id='geo-dropdown',
            options=[{'label': geo, 'value': geo} for geo in df_q2['GEO'].unique()],
            value='Ontario',
            style={'width': '50%'}
        ),
    ], style={'padding': '20px'}),

    html.Div([
        dcc.Graph(id='engineers-manpower-bar', figure=fig_q3),
        html.Label("Select Province for Question 3:"),
        dcc.Dropdown(
            id='geo-dropdown-q3',
            options=[{'label': geo, 'value': geo} for geo in df_q3['GEO'].unique()],
            value='Ontario',
            style={'width': '50%'}
        ),
    ], style={'padding': '20px'})
])

@app.callback(
    Output('essential-services-bar', 'figure'),
    [Input('job-category-dropdown', 'value'), Input('province-dropdown-q1', 'value')]
)
def update_q1_figure(selected_job, selected_province):
    filtered_df_q1 = df_q1[df_q1['Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)'] == selected_job]
    filtered_df_q1 = filtered_df_q1[filtered_df_q1['GEO'] == selected_province]
    fig_q1_updated = px.bar(filtered_df_q1,
                            x='Gender (3)',
                            y='VALUE',
                            color='Gender (3)',
                            title=f"Distribution of Essential Services: {selected_job} in {selected_province}",
                            labels={"Gender (3)": "Gender", "VALUE": "Number of People"},
                            barmode='group')
    return fig_q1_updated

@app.callback(
    Output('gender-employment-bar', 'figure'),
    [Input('geo-dropdown', 'value')]
)
def update_q2_figure(selected_geo):
    filtered_df_q2 = df_q2[df_q2['GEO'] == selected_geo]
    fig_q2_updated = px.bar(filtered_df_q2,
                            x='Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)',
                            y='VALUE',
                            color='Gender (3)',
                            title=f"Employment Statistics by Gender in {selected_geo}",
                            labels={
                                "Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)": "Occupation",
                                "VALUE": "Number of People", "Gender (3)": "Gender"},
                            barmode='group')
    return fig_q2_updated

@app.callback(
    Output('engineers-manpower-bar', 'figure'),
    [Input('geo-dropdown-q3', 'value')]
)
def update_q3_figure(selected_geo):
    filtered_df_q3 = df_q3[df_q3['GEO'] == selected_geo]
    fig_q3_updated = px.bar(filtered_df_q3,
                            x='Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)',
                            y='VALUE',
                            color='Gender (3)',
                            title=f"Manpower Availability for Engineers in {selected_geo}",
                            labels={
                                "Occupation - Unit group - National Occupational Classification (NOC) 2021 (821A)": "Occupation",
                                "VALUE": "Number of Engineers", "Gender (3)": "Gender"},
                            barmode='group')
    return fig_q3_updated

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
