import streamlit as st
import numpy as np
import sympy as sp
import plotly.graph_objects as go

# ===============================
# Page config
# ===============================
st.set_page_config(
    page_title="Vector Lab | Steepest Horizontal Gradient",
    layout="wide"
)

# ===============================
# Sidebar — Definitions & Telemetry
# ===============================
with st.sidebar:
    st.title("📘 Definitions")

    tab = st.radio(
        "Learning Pages",
        ["Multivariable Surfaces", "Component Slopes", "Steepest Gradient"]
    )

    if tab == "Multivariable Surfaces":
        st.markdown("""
        ### The Landscape
        Imagine hiking a 3D terrain defined by $f(x, y)$: hills, valleys, and plateaus.
        Height $z$ tells you how high you are.
        Click on the surface to explore slopes!
        """)

    elif tab == "Component Slopes":
        st.markdown("""
        ### Partial Derivatives
        - **Red**: slope along X → $f_x$
        - **Green**: slope along Y → $f_y$

        Imagine moving only in one direction at a time — these slopes tell you how steep the terrain is horizontally.
        """)

    else:
        st.markdown("""
        ### Steepest Horizontal Gradient
        The gradient acts like a "horizontal compass": it points along the xy-plane direction of fastest increase.

        $$
        \vec{v}_{steepest} = (f_x, f_y)
        $$
        """)

    st.divider()
    st.markdown("### 📊 Analysis Output")
    z_val = st.empty()
    fx_val = st.empty()
    fy_val = st.empty()

# ===============================
# Main UI
# ===============================
st.title("🧭 Vector Lab: Steepest Horizontal Gradient")
expr_input = st.text_input("Enter function f(x, y):", "x**2 + y**2")

# ===============================
# Symbolic math setup
# ===============================
x, y = sp.symbols("x y")
try:
    f_expr = sp.sympify(expr_input)
except:
    st.error("Invalid function expression")
    st.stop()

fx_expr = sp.diff(f_expr, x)
fy_expr = sp.diff(f_expr, y)

f = sp.lambdify((x, y), f_expr, "numpy")
fx = sp.lambdify((x, y), fx_expr, "numpy")
fy = sp.lambdify((x, y), fy_expr, "numpy")

# ===============================
# Surface mesh
# ===============================
R = 4
N = 60
xs = np.linspace(-R, R, N)
ys = np.linspace(-R, R, N)
X, Y = np.meshgrid(xs, ys)
Z = f(X, Y)

# ===============================
# Session state for clicked point
# ===============================
if "point" not in st.session_state:
    st.session_state.point = None

# ===============================
# Plot the surface
# ===============================
fig = go.Figure()
fig.add_surface(
    x=X, y=Y, z=Z,
    opacity=0.75,
    colorscale="Blues",
    showscale=False
)

# ===============================
# Add analysis visuals if point is clicked
# ===============================
if st.session_state.point is not None:
    a, b = st.session_state.point
    z0 = f(a, b)
    fx0 = fx(a, b)
    fy0 = fy(a, b)

    # Sidebar values
    z_val.markdown(f"**z = {z0:.4f}**")
    fx_val.markdown(f"**fₓ = {fx0:.4f}**")
    fy_val.markdown(f"**fᵧ = {fy0:.4f}**")

    s = 0.8
    # Partial derivative lines
    fig.add_trace(go.Scatter3d(
        x=[a - s, a + s],
        y=[b, b],
        z=[z0 - fx0 * s, z0 + fx0 * s],
        mode="lines",
        line=dict(color="red", width=6),
        name="∂f/∂x"
    ))

    fig.add_trace(go.Scatter3d(
        x=[a, a],
        y=[b - s, b + s],
        z=[z0 - fy0 * s, z0 + fy0 * s],
        mode="lines",
        line=dict(color="green", width=6),
        name="∂f/∂y"
    ))

    # Gradient arrow (steepest ascent)
    mag = np.hypot(fx0, fy0) or 1
    dx = fx0 / mag
    dy = fy0 / mag

    fig.add_trace(go.Scatter3d(
        x=[a, a + dx],
        y=[b, b + dy],
        z=[z0, z0],
        mode="lines+markers",
        line=dict(color="black", width=8),
        marker=dict(size=4),
        name="Gradient"
    ))

    # Tangent plane
    P = 1.2
    u = np.linspace(-P, P, 15)
    v = np.linspace(-P, P, 15)
    U, V = np.meshgrid(u, v)
    Zp = z0 + fx0 * U + fy0 * V

    fig.add_surface(
        x=a + U,
        y=b + V,
        z=Zp,
        opacity=0.5,
        colorscale=[[0, "#1e3a8a"], [1, "#1e3a8a"]],
        showscale=False,
        name="Tangent Plane"
    )

# ===============================
# Layout
# ===============================
fig.update_layout(
    height=720,
    margin=dict(l=0, r=0, t=0, b=0),
    scene=dict(aspectratio=dict(x=1, y=1, z=0.7))
)

# ===============================
# Display Plotly chart
# ===============================
plot = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

# ===============================
# Handle click via session_state
# ===============================
if plot is not None:
    # Streamlit does not natively capture click data yet.
    # Use st.session_state to store the clicked point manually
    # Users can input a point if needed, or future upgrade: add click capture via Dash.
    pass
