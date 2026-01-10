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
# Sidebar — Definitions
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
        Imagine hiking a 3D terrain defined by  
        **f(x, y)** — hills, valleys, and plateaus.

        Each point `(x, y)` has a height `z`.

        👉 Click on the surface to explore how it slopes.
        """)

    elif tab == "Component Slopes":
        st.markdown("""
        ### Partial Derivatives
        - **Red**: slope in the **x-direction** → \( f_x \)
        - **Green**: slope in the **y-direction** → \( f_y \)

        You move **only one direction at a time** to measure these slopes.
        """)

    else:
        st.markdown("""
        ### Steepest Horizontal Gradient
        The gradient acts like a **horizontal compass**.

        It points in the **xy-plane direction** where height increases fastest.

        \[
        \vec{v}_{steepest} = (f_x, f_y)
        \]
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

expr_input = st.text_input("Enter function f(x, y):", "x^2 + y^2")

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
# Click state
# ===============================
if "point" not in st.session_state:
    st.session_state.point = None

# ===============================
# Plot
# ===============================
fig = go.Figure()

fig.add_surface(
    x=X, y=Y, z=Z,
    opacity=0.75,
    colorscale="Blues",
    showscale=False
)

# ===============================
# Add analysis visuals
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

    # ∂f/∂x line (red)
    fig.add_trace(go.Scatter3d(
        x=[a - s, a + s],
        y=[b, b],
        z=[z0 - fx0 * s, z0 + fx0 * s],
        mode="lines",
        line=dict(color="red", width=6),
        name="∂f/∂x"
    ))

    # ∂f/∂y line (green)
    fig.add_trace(go.Scatter3d(
        x=[a, a],
        y=[b - s, b + s],
        z=[z0 - fy0 * s, z0 + fy0 * s],
        mode="lines",
        line=dict(color="green", width=6),
        name="∂f/∂y"
    ))

    # Gradient arrow
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
    Zp = z0 + fx0 * (U) + fy0 * (V)

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

click = st.plotly_chart(fig, use_container_width=True)

# ===============================
# Click handler
# ===============================
if click and "points" in click:
    p = click["points"][0]
    st.session_state.point = (p["x"], p["y"])
