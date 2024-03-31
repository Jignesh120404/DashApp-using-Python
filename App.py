import dash
from dash import html, dcc, Input, Output
from dash import callback_context
from bs4 import BeautifulSoup
from dash import html, dcc, dash_table
import requests
import plotly.graph_objects as go
import statistics
import numpy as np
# Create Dash app
app = dash.Dash(__name__,)
global output_message1
# Header style
header_style = {
    'color': '#FFF',  # Header text color (white)
    'background-color': 'rgb(52, 58, 64)',  # Header background color
    'padding': '35px',  # Padding around the header
    'padding-top': '40px',  # Add additional padding at the top to push text down vertically
    'text-align': 'left',  # Align the header text to the left
    'font-size': '20px',  # Font size
    'font-family': 'Arial, sans-serif',  # Font family
}


# Body style
body_style = {
    'overflow-y': 'hidden',  # Add vertical scrollbar
    'height': '250vh',
    'max-width': '100%',
    'margin': '0',  # Remove margin
    'margin-left': '-8px',
    'margin-right': '-100px',
    'margin-top': '-22px',
}

# Additional styles
dashboard_style = {
    'color': 'black',
    'margin-top': '10px',  # Add margin from the top to move it down
    'margin-left': '0px',  # Set left margin to auto to center horizontally
    'margin-right': '5px',  # Set right margin to auto to center horizontally
    'max-width': 'auto',
    'text-align': 'left',
    'font-size': '35px',  # Font size
}
top_style = {
    'margin-top': '-20px',
    'color': '#55595c',
}
top_style2 = {
    'color': '#55595c',
}

data = [
    {'': "Sales Growth", '10 YRS': 2, '5 YRS': 3, '3 YRS': 4, 'TTM': 5},
    {'': "Profit Growth", 'B': 7, 'C': 8, 'D': 9, 'E': 10},
   
]


# Define table columns
columns = [{'name': col, 'id': col} for col in data[0].keys()]


# Define layout
app.layout = html.Div(style=body_style, children=[
    html.H1('REVERSE DCF', style=header_style),
    html.H2("VALUING CONSISTENT COMPOUNDERS", style=dashboard_style),
    html.H3("Select any of the valid stock Symbol to get stats!", style=top_style),
    html.H3("This page will help you calculate intrinsic PE of consistent compounders through growth-RoCE DCF model.",
            style=top_style2),
    html.H3(
        "We then compare this with current PE of the stock to calculate degree of overvaluation.", style=top_style2),
    html.H3("NSE/BSE symbol", style=top_style2),
    dcc.Input(id='nse-bse-input', type='text', placeholder='', style={'margin-top': '-100px', 'width': '195px',
                                                                       'height': '29px', 'margin-right': '10px'}),
    html.Button('Get Stats', id='button', n_clicks=0),
    html.H3("Cost of Capital (CoC): %", style={'margin-top': '5px','color': '#55595c',}),
    
     dcc.Slider(
        id='my-slider',
        min=8,  # Set minimum value
        max=16, 
        value=12, # Set maximum value
        step=0.5,  # Set step size
        marks={i: str(i) for i in range(8, 17)},
        className='horizontal-slider'
           ),
     html.H3("Return on Capital Employed (RoCE): %",style={'margin-top': '-10px','color': '#55595c',}),
     dcc.Slider(
        id='my-slider',
        min=10, 
        value=20,# Set minimum value
        max=100,  # Set maximum value
        step=5,  # Set step size
        marks={i: str(i) for i in range(10, 101, 10)},
        
           ),
     html.H3("Growth during high growth period: $",style={'margin-top': '-10px','color': '#55595c',}),
     dcc.Slider(
        id='my-slider',
        min=8, 
        value=12,# Set minimum value
        max=20,  # Set maximum value
        step=1,  # Set step size
        marks={i: str(i) for i in range(8, 21, 2)},
        
           ),
     html.H3("High growth period(years)",style={'margin-top': '-10px','color': '#55595c',}),
     dcc.Slider(
        id='my-slider',
        min=10,
        value=15,# Set minimum value
        max=25,  # Set maximum value
        step=1,  # Set step size
        marks={i: str(i) for i in range(10, 26, 2)},
        
           ),
     html.H3("Fade period(years):",style={'margin-top': '-10px','color': '#55595c',}),
     dcc.Slider(
        id='my-slider',
        min=5,  # Set minimum value
        max=20,
        value=15,# Set maximum value
        step=2.5,  # Set step size
        marks={i: str(i) for i in range(5, 21, 5)},
        
           ),
     html.H3("Terminal growth rate: %",style={'margin-top': '-10px','color': '#55595c',}),
     dcc.Slider(
        id='my-slider',
        min=0,  # Set minimum value
        max=7.5,
        value=2,# Set maximum value
        step=0.5,  # Set step size
        marks={i: str(i) for i in range(1, 8, 1)},
        
           ),
     html.Div(id='output-container-button', style={'margin-left': '10px','margin-top':'-10px'}),
     
])

output_message = ""

@app.callback(
    Output('output-container-button', 'children'),
    [Input('button', 'n_clicks')],
    [Input('nse-bse-input', 'value')]
)

def update_output(n_clicks, value):
    global output_message  # Declare output_message as global within the function

    if n_clicks:
        triggered_id = callback_context.triggered[0]['prop_id'].split('.')[0]
        if triggered_id == 'button':
            if value:
                output_message = ' '.join(value.strip().split())
                pe_ratio, Fy, cap, med, sales_growth_cleaned, profit_growth_cleaned = scrap1(output_message)
                final = round(int(cap) / int(Fy), 2)
                y =["10 YRS", "5 YRS", "3 YRS","TTM"]
                fig1,mean1 =create_horizontal_bar_graph(sales_growth_cleaned,y,"") 
                fig2,mean2 =create_horizontal_bar_graph(profit_growth_cleaned,y,"")
                sales_growth_cleaned = [mean1 if val == '' else val for val in sales_growth_cleaned]
                profit_growth_cleaned = [mean2 if val == '' else val for val in profit_growth_cleaned]
                
                updated_data = [
                    {'': "Sales Growth", '10 YRS': sales_growth_cleaned[0], '5 YRS': sales_growth_cleaned[1], '3 YRS': sales_growth_cleaned[2], 'TTM': sales_growth_cleaned[3]},
                    {'': "Profit Growth", '10 YRS': profit_growth_cleaned[0], '5 YRS': profit_growth_cleaned[1], '3 YRS': profit_growth_cleaned[2], 'TTM': profit_growth_cleaned[3]},
                ]
                
                
                return [
                    html.H3(f"Stock Symbol: {output_message}"), 
                    html.H3(f"PE Ratio: {pe_ratio}"), 
                    html.H3(f"FY23PE: {final}"), 
                    html.H3(f"5-yr median pre-tax RoCE: {med}%"), 
                    generate_table(updated_data),
                    html.Div([
                        dcc.Graph(figure=fig1),
                        dcc.Graph(figure=fig2)
                    ], style={'display': 'flex', 'flex-direction': 'row'})
                ]
            else:
                output_message = 'NESTLEIND'
                pe_ratio, Fy, cap, med, sales_growth_cleaned, profit_growth_cleaned = scrap1(output_message)
                final = round(int(cap) / int(Fy), 2)
                y =["10 YRS", "5 YRS", "3 YRS","TTM"]
                fig1,mean1 =create_horizontal_bar_graph(sales_growth_cleaned,y,"") 
                fig2,mean2 =create_horizontal_bar_graph(profit_growth_cleaned,y,"")
                sales_growth_cleaned = [mean1 if val == '' else val for val in sales_growth_cleaned]
                profit_growth_cleaned = [mean2 if val == '' else val for val in profit_growth_cleaned]
                
                updated_data = [
                    {'': "Sales Growth", '10 YRS': sales_growth_cleaned[0], '5 YRS': sales_growth_cleaned[1], '3 YRS': sales_growth_cleaned[2], 'TTM': sales_growth_cleaned[3]},
                    {'': "Profit Growth", '10 YRS': profit_growth_cleaned[0], '5 YRS': profit_growth_cleaned[1], '3 YRS': profit_growth_cleaned[2], 'TTM': profit_growth_cleaned[3]},
                ]
                
                
                return [
                    html.H3(f"Stock Symbol: {output_message}"), 
                    html.H3(f"PE Ratio: {pe_ratio}"), 
                    html.H3(f"FY23PE: {final}"), 
                    html.H3(f"5-yr median pre-tax RoCE: {med}%"), 
                    generate_table(updated_data),
                    html.Div([
                        dcc.Graph(figure=fig1),
                        dcc.Graph(figure=fig2)
                    ], style={'display': 'flex', 'flex-direction': 'row'})
                ]

    return ''

def scrap1(val):
    url = f'https://www.screener.in/company/{val}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    number_elements = soup.find_all('span', class_='number')
    extracted_data = number_elements[4].text.strip()
    table = soup.find_all('table', class_='data-table responsive-text-nowrap')
    rows = table[1].find_all('tr')
    fype = rows[10].find_all('td')
    cell_text = fype[len(fype)-2].text.strip().replace(',', '')
    cap = soup.find('span', class_='number').text.strip().replace(',','')
    section = soup.find(id='ratios')
    table = section.find('table',class_='data-table responsive-text-nowrap')
    tds = table.find_all('td')
    vector = []
    for i in range(3, 8):
        value = tds[len(tds) - i].text.strip().replace('%', '')
        vector.append(int(value))

    median = statistics.median(vector)
    begin = soup.find_all('table',class_="ranges-table")
    salesg = begin[0].find_all('td')
    profitg = begin[1].find_all('td')
    sales_growth_cleaned = []
    profit_growth_cleaned = []
    for i in range(len(salesg)):
     if i % 2 != 0:  # Check if index is odd
        sales_growth_cleaned.append((salesg[i].text.strip().replace('%', '')))

# Extract and clean data from profitg table
    for i in range(len(profitg)):
     if i % 2 != 0:  # Check if index is odd
        profit_growth_cleaned.append(profitg[i].text.strip().replace('%', ''))
    return extracted_data,cell_text,cap,median,sales_growth_cleaned,profit_growth_cleaned
def generate_table(data):
    columns = [{'name': col, 'id': col} for col in data[0].keys()]
    return dash_table.DataTable(
        columns=columns,
        data=data
    )
def create_horizontal_bar_graph(x_values, y_labels, graph_title):
    # Convert x_values to integers, replacing empty strings with np.nan
    x_values = [int(val) if val else np.nan for val in x_values]
    
    # Calculate the mean of non-empty x_values
    x_mean = np.nanmean(x_values)
    
    # Replace np.nan with the calculated mean
    x_values = [x_mean if np.isnan(val) else val for val in x_values]
    
    fig = go.Figure(go.Bar(
        x=x_values,
        y=y_labels,
        orientation='h',
        name=graph_title
    ))
    fig.update_layout(
        title=graph_title,
        yaxis=dict(title='Y-axis Label'),
        xaxis=dict(title='X-axis Label')
    )
    return fig,x_mean


    
if __name__ == '__main__':
    app.run_server(debug=True)
