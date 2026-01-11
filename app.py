import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application
)

st.set_page_config(page_title="Vector Lab", layout="wide")

page = st.sidebar.radio(
    "📚 Pages",
    ["Function of Two Variables", "Partial Derivatives", "Gradient & Steepest Ascent", "Interactive Calculator"]
)

x, y = sp.symbols("x y")

# ==========================
# Page 1
# ==========================
if page == "Function of Two Variables":
    st.title("Function of Two Variables")

    st.subheader("Formal Definition")
    st.markdown(r"""
A **function of two variables** assigns to each ordered pair \((x,y)\) exactly one real number \(z\).

\[
f: \mathbb{R}^2 \to \mathbb{R}, \quad (x,y) \mapsto f(x,y)
\]
""")

    st.subheader("Explanation")
    st.markdown("""
Imagine a **hill or landscape**.  
At each position \((x,y)\), the height \(z\) represents the value of the function.
""")

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
# Page 2
# ==========================
elif page == "Partial Derivatives":
    st.title("Partial Derivatives")

    st.markdown(r"""
\[
f_x(x,y)=\lim_{h\to0}\frac{f(x+h,y)-f(x,y)}{h}, \quad
f_y(x,y)=\lim_{h\to0}\frac{f(x,y+h)-f(x,y)}{h}
\]
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
        mode="lines", line=dict(color="red", width=6)
    ))

    fig.add_trace(go.Scatter3d(
        x=[px, px], y=[py-s, py+s], z=[z-fy_val*s, z+fy_val*s],
        mode="lines", line=dict(color="green", width=6)
    ))

    fig.update_layout(scene=dict(aspectratio=dict(x=1,y=1,z=0.7)), margin=dict(t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

# ==========================
# Page 3
# ==========================
elif page == "Gradient & Steepest Ascent":
    st.title("Gradient and Steepest Ascent")

    st.markdown(r"""
\[
\nabla f(x,y)=\langle f_x(x,y), f_y(x,y) \rangle
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
# Page 4
# ==========================
else:
    st.title("Interactive Calculator")

    left, right = st.columns([3, 1])

    with right:
        tab, = st.tabs(["Input & Interpretation"])

        with tab:
            func_input = st.text_input("f(x,y) =", "x^2 + y^2").replace("^","**")
            transformations = standard_transformations + (implicit_multiplication_application,)
            f_expr = parse_expr(func_input, transformations=transformations)

            fx_expr = sp.diff(f_expr, x)
            fy_expr = sp.diff(f_expr, y)

            st.latex(rf"f(x,y)={sp.latex(f_expr)}")
            st.latex(rf"f_x(x,y)={sp.latex(fx_expr)}")
            st.latex(rf"f_y(x,y)={sp.latex(fy_expr)}")
            st.latex(rf"\nabla f(x,y)=\langle {sp.latex(fx_expr)}, {sp.latex(fy_expr)} \rangle")

            x_val = st.number_input("x", value=1.0)
            y_val = st.number_input("y", value=1.0)

    f_func = sp.lambdify((x,y), f_expr, "numpy")
    fx_func = sp.lambdify((x,y), fx_expr, "numpy")
    fy_func = sp.lambdify((x,y), fy_expr, "numpy")

    z_val = f_func(x_val, y_val)
    fx_val = fx_func(x_val, y_val)
    fy_val = fy_func(x_val, y_val)

    with left:
        st.markdown(f"""
**Numerical Values**
- \(f(x,y)={z_val:.4f}\)
- \(f_x={fx_val:.4f}\)
- \(f_y={fy_val:.4f}\)
- \(\nabla f=\langle {fx_val:.4f},{fy_val:.4f}\rangle\)
""")

        X, Y = np.meshgrid(np.linspace(-4,4,60), np.linspace(-4,4,60))
        Z = f_func(X, Y)

        fig = go.Figure()
        fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale="Blues", opacity=0.7, showscale=False))
        fig.add_trace(go.Scatter3d(x=[x_val], y=[y_val], z=[z_val],
                                   mode="markers", marker=dict(size=5, color="gold")))

        fig.update_layout(scene=dict(aspectratio=dict(x=1,y=1,z=0.7)), margin=dict(t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
