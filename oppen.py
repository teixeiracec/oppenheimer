import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Constants
G = 6.67430e-8  # Gravitational constant in cm^3 g^-1 s^-2
c = 2.99792458e10  # Speed of light in cm/s
solar_mass = 1.989e33  # Mass of the sun in grams

# Initial conditions and parameters
M_sun = 1  # Mass of the star in solar masses
M = M_sun * solar_mass  # Mass of the star in grams
r_0 = 1e6  # Initial radius in cm
r_b = 1e7  # Boundary radius in cm

# Schwarzschild radius for a solar mass black hole
r_s = 2 * G * M / c**2  # Schwarzschild radius in cm

# Spatial array (normalized by Schwarzschild radius)
r = np.linspace(-1.2, 1.2, 100)  # Normalized radius array from -1.2 to 1.2

# Create a meshgrid for r
X, Y, Z = np.meshgrid(r, r, r)

# Convert to spherical coordinates
def spherical_coordinates(X, Y, Z, r_s):
    return np.sqrt(X**2 + Y**2 + Z**2) * r_s

# Define the functions for e^nu and e^lambda based on the given equations
def enu(r, M):
    return 1 - 2 * G * M / (r * c**2)

def elambda(r, M):
    return (1 - 2 * G * M / (r * c**2))**(-1)

# Function to calculate mass
def mass(r, r_b, rho_0):
    return 4 / 3 * np.pi * rho_0 * (r_b**3 - r**3)

# Function to calculate density
def density(r, r_b, rho_0):
    return np.where(r < r_b, rho_0 * (1 - (r / r_b) ** 2), 0)

# Function to calculate pressure
def pressure(r, r_b, rho_0):
    return (rho_0 * c**2 / 3) * (1 - (r / r_b) ** 2)

# Function to create a Plotly figure for mass
def create_mass_figure(M, r_b):
    R = spherical_coordinates(X, Y, Z, r_s)
    rho_0 = 1e15  # Central density in g/cm^3
    mass_values = mass(R, r_b, rho_0)
    
    fig = go.Figure(data=[go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=mass_values.flatten(),
        isomin=mass_values.min(),
        isomax=mass_values.max(),
        opacity=0.1,
        surface_count=17,
        colorscale='Blues',
        colorbar=dict(title='Mass (g)')
    )])
    fig.update_layout(title='Mass as a Function of Radius',
                      scene=dict(
                          xaxis_title='X (r/r_s)',
                          yaxis_title='Y (r/r_s)',
                          zaxis_title='Z (r/r_s)'
                      ))
    return fig

# Function to create a Plotly figure for density
def create_density_figure(M, r_b):
    R = spherical_coordinates(X, Y, Z, r_s)
    rho_0 = 1e15  # Central density in g/cm^3
    density_values = density(R, r_b, rho_0)
    
    fig = go.Figure(data=[go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=density_values.flatten(),
        isomin=density_values.min(),
        isomax=density_values.max(),
        opacity=0.1,
        surface_count=17,
        colorscale='Greens',
        colorbar=dict(title='Density (g/cm^3)')
    )])
    fig.update_layout(title='Density as a Function of Radius',
                      scene=dict(
                          xaxis_title='X (r/r_s)',
                          yaxis_title='Y (r/r_s)',
                          zaxis_title='Z (r/r_s)'
                      ))
    return fig

# Function to create a Plotly figure for pressure
def create_pressure_figure(M, r_b):
    R = spherical_coordinates(X, Y, Z, r_s)
    rho_0 = 1e15  # Central density in g/cm^3
    pressure_values = pressure(R, r_b, rho_0)
    
    fig = go.Figure(data=[go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=pressure_values.flatten(),
        isomin=pressure_values.min(),
        isomax=pressure_values.max(),
        opacity=0.1,
        surface_count=17,
        colorscale='Reds',
        colorbar=dict(title='Pressure (dyn/cm^2)')
    )])
    fig.update_layout(title='Pressure as a Function of Radius',
                      scene=dict(
                          xaxis_title='X (r/r_s)',
                          yaxis_title='Y (r/r_s)',
                          zaxis_title='Z (r/r_s)'
                      ))
    return fig

# Function to create a Plotly figure for e^nu
def create_enu_figure(M, r_b):
    r_s = 2 * G * M / c**2  # Schwarzschild radius in cm
    R = spherical_coordinates(X, Y, Z, r_s)
    enu_values = enu(R, M)
    
    fig = go.Figure(data=[go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=enu_values.flatten(),
        isomin=enu_values.min(),
        isomax=enu_values.max(),
        opacity=0.1,  # lower opacity to see through
        surface_count=17,  # number of isosurfaces, 2 to 17
        colorscale='Viridis',
        colorbar=dict(title='e^ν')
    )])
    fig.update_layout(title='e^ν as a Function of Radius',
                      scene=dict(
                          xaxis_title='X (r/r_s)',
                          yaxis_title='Y (r/r_s)',
                          zaxis_title='Z (r/r_s)'
                      ))
    return fig

# Function to create a Plotly figure for e^lambda
def create_elambda_figure(M, r_b):
    r_s = 2 * G * M / c**2  # Schwarzschild radius in cm
    R = spherical_coordinates(X, Y, Z, r_s)
    elambda_values = elambda(R, M)
    
    fig = go.Figure(data=[go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=elambda_values.flatten(),
        isomin=elambda_values.min(),
        isomax=elambda_values.max(),
        opacity=0.1,  # lower opacity to see through
        surface_count=17,  # number of isosurfaces, 2 to 17
        colorscale='Plasma',
        colorbar=dict(title='e^λ')
    )])
    fig.update_layout(title='e^λ as a Function of Radius',
                      scene=dict(
                          xaxis_title='X (r/r_s)',
                          yaxis_title='Y (r/r_s)',
                          zaxis_title='Z (r/r_s)'
                      ))
    return fig

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='J. R. Oppenheimer and H. Snyder (1939). On Continued Gravitational Contraction. Phys. Rev. 56, 455-59'),

    html.Div([
        html.Label('Mass of the star (Solar Masses):'),
        dcc.Slider(
            id='mass-slider',
            min=0.5,
            max=10,
            step=0.1,
            value=1,
            marks={i: f'{i}' for i in range(1, 11)}
        ),
        html.Label('Boundary radius (cm):'),
        dcc.Slider(
            id='radius-slider',
            min=5e6,
            max=2e7,
            step=1e6,
            value=1e7,
            marks={int(i): f'{int(i):.0e}' for i in np.linspace(5e6, 2e7, 5)}
        )
    ]),

    dcc.Graph(
        id='enu-graph'
    ),

    dcc.Graph(
        id='elambda-graph'
    ),

    dcc.Graph(
        id='mass-graph'
    ),

    dcc.Graph(
        id='density-graph'
    ),

    dcc.Graph(
        id='pressure-graph'
    )
])

# Define callback to update graphs
@app.callback(
    [Output('enu-graph', 'figure'),
     Output('elambda-graph', 'figure'),
     Output('mass-graph', 'figure'),
     Output('density-graph', 'figure'),
     Output('pressure-graph', 'figure')],
    [Input('mass-slider', 'value'),
     Input('radius-slider', 'value')]
)
def update_graphs(mass, boundary_radius):
    M = mass * solar_mass
    r_b = boundary_radius
    enu_fig = create_enu_figure(M, r_b)
    elambda_fig = create_elambda_figure(M, r_b)
    mass_fig = create_mass_figure(M, r_b)
    density_fig = create_density_figure(M, r_b)
    pressure_fig = create_pressure_figure(M, r_b)
    return [enu_fig, elambda_fig, mass_fig, density_fig, pressure_fig]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
