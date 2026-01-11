import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application
)

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

\[
f: \mathbb{R}^2 \to \mathbb{R}, \quad (x,y) \mapsto f(x,y)
\]

Here, \(z = f(x,y)\) is interpreted as height.
""")

    st.subheader("Explanation")
    st.markdown("""
Imagine a **hill or landscape**.  
At each position \((x,y)\) on the ground, the height \(z\) tells you how high the surface is at that point.
""")

    st.subheader("Example Surfaces")
    examples = {
        "Quadratic": lambda X, Y: X**2 + Y**2,
        "Linear": lambda X, Y: 2*X + 3*Y + 5,
        "Trigonometric": lambda X, Y: np.sin(X) + np.cos(Y),
        "Root": lambda X, Y: np.sqrt(np.abs(X)) + np.sqrt(np.abs(Y)),
        "Rational": lambda X, Y: X / (Y + 1)
    }

    for name, func in examples.items():
        st.markdown(f"**{name} function**")
        X, Y = np.meshgrid(np.linspace(-4,4,50), np.linspace(-4,4,50))
        Z = func(X, Y)
        fig = go.Figure(go.Surface(z=Z, x=X, y=Y, colorscale="Blues", opacity=0.7, showscale=False))
        fig.update_layout(scene=dict(aspectratio=dict(x=1,y=1,z=0.7)), margin=dict(t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

# ==========================
# Page 2: Partial Derivatives
# ==========================
elif page == "Partial Derivatives":
    st.title("Partial Derivatives")

    st.subheader("Formal Definition")
    st.markdown(r"""
\[
f_x(x,y) = \lim_{h\to 0} \frac{f(x+h,y)-f(x,y)}{h}, \quad
f_y(x,y) = \lim_{h\to 0} \frac{f(x,y+h)-f(x,y)}{h}
\]
""")

    st.subheader("Explanation")
    st.markdown("""
Partial derivatives measure **rates of change along coordinate directions**, while holding the other variable constant.
""")

    X, Y = np.meshgrid(np.linspace(-4,4,50), np.linspace(-4,4,50))
    Z = X**2 + Y**2

    px, py = 2, 2
    z = px**2 + py**2
    fx_val, fy_val = 2*px, 2*py
    s = 0.8

    fig = go.Figure()
    fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale="Blues", opacity=0.7, showscale=False))
    fig.add_trace(go.Scatter3d(x=[px], y=[py], z=[z], mode="markers",
                               marker=dict(size=5, color="gold")))

    fig.add_trace(go.Scatter3d(
        x=[px-s, px+s], y=[py, py], z=[z-fx_val*s, z+fx_val*s],
        mode="lines", line=dict(color="red", width=6), name="∂f/∂x"
    ))

    fig.add_trace(go.Scatter3d(
        x=[px, px], y=[py-s, py+s], z=[z-fy_val*s, z+fy_val*s],
        mode="lines", line=dict(color="green", width=6), name="∂f/∂y"
    ))

    fig.update_layout(scene=dict(aspectratio=dict(x=1,y=1,z=0.7)), margin=dict(t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

# ==========================
# Page 3: Gradient & Steepest Ascent
# ==========================
elif page == "Gradient & Steepest Ascent":
    st.title("Gradient and Steepest Ascent")

    st.markdown(r"""
\[
\nabla f(x,y) = \langle f_x(x,y), f_y(x,y) \rangle
\]
""")

    X, Y = np.meshgrid(np.linspace(-4,4,50), np.linspace(-4,4,50))
    Z = X**2 + Y**2

    px, py = 2, 2
    z = px**2 + py**2
    fx_val, fy_val = 2*px, 2*py

    fig = go.Figure()
    fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale="Blues", opacity=0.7, showscale=False))
    fig.add_trace(go.Scatter3d(x=[px], y=[py], z=[z], mode="markers",
                               marker=dict(size=5, color="gold")))

    mag = np.hypot(fx_val, fy_val)
    dx, dy = fx_val/mag, fy_val/mag

    fig.add_trace(go.Scatter3d(
        x=[px, px+dx], y=[py, py+dy], z=[z, z],
        mode="lines+markers", line=dict(color="black", width=8)
    ))

    P = 1.2
    u, v = np.linspace(-P,P,15), np.linspace(-P,P,15)
    U, V = np.meshgrid(u,v)
    Zp = z + fx_val*U + fy_val*V

    fig.add_trace(go.Surface(
        x=px+U, y=py+V, z=Zp,
        colorscale=[[0,"#1e3a8a"],[1,"#1e3a8a"]],
        opacity=0.5, showscale=False
    ))

    fig.update_layout(scene=dict(aspectratio=dict(x=1,y=1,z=0.7)), margin=dict(t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

# ==========================
# Page 4: Interactive Calculator
# ==========================
else:
    st.title("Interactive Calculator")

    func_input = st.text_input("Enter a function f(x, y):", "x^2 + y^2")
    func_input = func_input.replace("^", "**")

    transformations = standard_transformations + (implicit_multiplication_application,)
    f_expr = parse_expr(func_input, transformations=transformations)

    fx_expr = sp.diff(f_expr, x)
    fy_expr = sp.diff(f_expr, y)

    st.subheader("Symbolic Interpretation")
    st.latex(rf"f(x,y) = {sp.latex(f_expr)}")
    st.latex(rf"f_x(x,y) = {sp.latex(fx_expr)}")
    st.latex(rf"f_y(x,y) = {sp.latex(fy_expr)}")
    st.latex(rf"\nabla f(x,y) = \langle {sp.latex(fx_expr)}, {sp.latex(fy_expr)} \rangle")

    f_func = sp.lambdify((x,y), f_expr, "numpy")
    fx_func = sp.lambdify((x,y), fx_expr, "numpy")
    fy_func = sp.lambdify((x,y), fy_expr, "numpy")

    col1, col2 = st.columns(2)
    x_val = col1.number_input("x-coordinate", value=1.0)
    y_val = col2.number_input("y-coordinate", value=1.0)

    z_val = f_func(x_val, y_val)
    fx_val = fx_func(x_val, y_val)
    fy_val = fy_func(x_val, y_val)

    st.subheader("Numerical Evaluation")
    st.markdown(f"""
- \(f(x,y) = {z_val:.4f}\)
- \(f_x = {fx_val:.4f}\)
- \(f_y = {fy_val:.4f}\)
- \(\nabla f = \langle {fx_val:.4f}, {fy_val:.4f} \rangle\)
""")

    xs = np.linspace(-4,4,60)
    ys = np.linspace(-4,4,60)
    X, Y = np.meshgrid(xs, ys)
    Z = f_func(X, Y)

    fig = go.Figure()
    fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale="Blues", opacity=0.7, showscale=False))
    fig.add_trace(go.Scatter3d(x=[x_val], y=[y_val], z=[z_val],
                               mode="markers", marker=dict(size=5, color="gold")))

    fig.update_layout(scene=dict(aspectratio=dict(x=1,y=1,z=0.7)), margin=dict(t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)
