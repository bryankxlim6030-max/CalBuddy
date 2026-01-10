import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Vector Lab", layout="wide")

# ==========================
# Sidebar for page navigation
# ==========================
page = st.sidebar.radio(
    "📚 Pages",
    ["Function of Two Variables", "Partial Derivatives", "Gradient & Steepest Ascent", "Interactive Calculator"]
)

# ==========================
# Common variables
# ==========================
x, y = sp.symbols("x y")

# ==========================
# Page 1: Function of Two Variables
# ==========================
if page == "Function of Two Variables":
    st.title("Function of Two Variables")
    st.subheader("Formal Definition")
    st.markdown(r"""
A **function of two variables** is a rule that assigns to each ordered pair \((x, y)\) exactly one real number \(z\).  
We write:

$$
f: \mathbb{R}^2 \to \mathbb{R}, \quad (x,y) \mapsto f(x,y)
$$

Here, \(z = f(x, y)\) is called the **output** or **height**.
""")
    st.subheader("Explanation")
    st.markdown("""
Imagine a **hill or landscape**. At each position `(x, y)` on the ground, the height `z` tells you how high you are.  
The function `f(x, y)` describes this terrain.
""")

    # Example 3D surface
    st.subheader("Example Surface")
    X, Y = np.meshgrid(np.linspace(-4,4,50), np.linspace(-4,4,50))
    Z = X**2 + Y**2
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Blues', opacity=0.7, showscale=False)])
    fig.update_layout(scene=dict(aspectratio=dict(x=1,y=1,z=0.7)), margin=dict(t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

# ==========================
# Page 2: Partial Derivatives
# ==========================
elif page == "Partial Derivatives":
    st.title("Partial Derivatives")
    st.subheader("Formal Definition")
    st.markdown(r"""
The **partial derivative** of \(f(x, y)\) with respect to \(x\) is:

$$
f_x(x,y) = \frac{\partial f}{\partial x} = \lim_{h \to 0} \frac{f(x+h, y) - f(x, y)}{h}
$$

Similarly, with respect to \(y\):

$$
f_y(x,y) = \frac{\partial f}{\partial y} = \lim_{h \to 0} \frac{f(x, y+h) - f(x, y)}{h}
$$
""")
    st.subheader("Explanation")
    st.markdown("""
Partial derivatives measure **slope along one direction at a time**.  
- \(f_x\) → slope if you move only in the x-direction  
- \(f_y\) → slope if you move only in the y-direction  

Imagine hiking on the hill while only moving along x or y — these tell you how steep it is.
""")

    # Example surface with gradient in x/y directions
    st.subheader("Example Surface")
    X, Y = np.meshgrid(np.linspace(-4,4,50), np.linspace(-4,4,50))
    Z = X**2 + Y**2
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Blues', opacity=0.7, showscale=False)])
    fig.update_layout(scene=dict(aspectratio=dict(x=1,y=1,z=0.7)), margin=dict(t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

# ==========================
# Page 3: Gradient & Steepest Ascent
# ==========================
elif page == "Gradient & Steepest Ascent":
    st.title("Gradient and Steepest Ascent")
    st.subheader("Formal Definition")
    st.markdown(r"""
The **gradient vector** of \(f(x, y)\) is:

$$
\nabla f(x, y) = \langle f_x(x,y), f_y(x,y) \rangle
$$

It points in the **direction of steepest increase** of the function.
""")
    st.subheader("Explanation")
    st.markdown("""
Think of the gradient as a **horizontal compass**: it shows which way to walk on the hill to increase height fastest.  
Its magnitude gives the **rate of increase**.
""")

    # Example surface with arrows (static)
    st.subheader("Example Surface")
    X, Y = np.meshgrid(np.linspace(-2,2,20), np.linspace(-2,2,20))
    Z = X**2 + Y**2
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Blues', opacity=0.7, showscale=False)])
    # Example arrow
    fig.add_trace(go.Cone(x=[0], y=[0], z=[0],
                          u=[1], v=[1], w=[0],
                          sizemode="scaled", sizeref=0.5,
                          anchor="tail", colorscale=[[0,'red'],[1,'red']]))
    fig.update_layout(scene=dict(aspectratio=dict(x=1,y=1,z=0.7)), margin=dict(t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

# ==========================
# Page 4: Interactive Calculator
# ==========================
else:
    st.title("Interactive Calculator")

    # Function input
    func_input = st.text_input("Enter a function f(x, y):", "x**2 + y**2")
    try:
        f_expr = sp.sympify(func_input)
    except:
        st.error("Invalid function expression")
        st.stop()

    # Partial derivatives
    fx_expr = sp.diff(f_expr, x)
    fy_expr = sp.diff(f_expr, y)
    f_func = sp.lambdify((x, y), f_expr, "numpy")
    fx_func = sp.lambdify((x, y), fx_expr, "numpy")
    fy_func = sp.lambdify((x, y), fy_expr, "numpy")

    # Coordinate input
    col1, col2 = st.columns(2)
    with col1:
        x_val = st.number_input("x-coordinate", value=1.0)
    with col2:
        y_val = st.number_input("y-coordinate", value=1.0)

    # Evaluate
    z_val = f_func(x_val, y_val)
    fx_val = fx_func(x_val, y_val)
    fy_val = fy_func(x_val, y_val)

    st.markdown(f"**f(x,y) = {z_val:.4f}**")
    st.markdown(f"**fₓ = {fx_val:.4f}**")
    st.markdown(f"**fᵧ = {fy_val:.4f}**")
    st.markdown(f"**Gradient vector = ({fx_val:.4f}, {fy_val:.4f})**")

    # 3D surface mesh
    R = 4
    N = 60
    xs = np.linspace(-R, R, N)
    ys = np.linspace(-R, R, N)
    X, Y = np.meshgrid(xs, ys)
    Z = f_func(X, Y)

    fig = go.Figure()
    # Surface
    fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale='Blues', opacity=0.7, showscale=False))

    # Point on surface
    fig.add_trace(go.Scatter3d(x=[x_val], y=[y_val], z=[z_val],
                               mode="markers", marker=dict(size=5, color='gold'),
                               name="Selected Point"))

    # Partial derivative lines
    s = 0.8
    fig.add_trace(go.Scatter3d(x=[x_val - s, x_val + s], y=[y_val, y_val],
                               z=[z_val - fx_val * s, z_val + fx_val * s],
                               mode="lines", line=dict(color="red", width=6), name="∂f/∂x"))

    fig.add_trace(go.Scatter3d(x=[x_val, x_val], y=[y_val - s, y_val + s],
                               z=[z_val - fy_val * s, z_val + fy_val * s],
                               mode="lines", line=dict(color="green", width=6), name="∂f/∂y"))

    # Gradient arrow (steepest ascent)
    mag = np.hypot(fx_val, fy_val) or 1
    dx = fx_val / mag
    dy = fy_val / mag
    fig.add_trace(go.Scatter3d(x=[x_val, x_val + dx], y=[y_val, y_val + dy],
                               z=[z_val, z_val], mode="lines+markers",
                               line=dict(color="black", width=8), marker=dict(size=4),
                               name="Gradient"))

    # Tangent plane
    P = 1.2
    u = np.linspace(-P, P, 15)
    v = np.linspace(-P, P, 15)
    U, V = np.meshgrid(u, v)
    Zp = z_val + fx_val * U + fy_val * V
    fig.add_trace(go.Surface(x=x_val + U, y=y_val + V, z=Zp,
                             colorscale=[[0, "#1e3a8a"], [1, "#1e3a8a"]],
                             opacity=0.5, showscale=False, name="Tangent Plane"))

    fig.update_layout(scene=dict(aspectratio=dict(x=1, y=1, z=0.7)), margin=dict(t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)
