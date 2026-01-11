import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application
)

st.set_page_config(page_title="Vector Lab", layout="wide")

# ==========================
# Sidebar navigation
# ==========================
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
A **function of two variables** assigns each point \((x,y)\) in the plane exactly one real number \(z\).

\[
f:\mathbb{R}^2 \to \mathbb{R}, \quad z = f(x,y)
\]
""")

    st.subheader("Geometric Interpretation")
    st.markdown("""
Think of a **landscape or hill**.  
Each point \((x,y)\) gives a height \(z\), forming a surface.
""")

    examples = {
        r"f(x,y)=x^2+y^2": lambda X,Y: X**2 + Y**2,
        r"f(x,y)=2x+3y+5": lambda X,Y: 2*X + 3*Y + 5,
        r"f(x,y)=\sin x + \cos y": lambda X,Y: np.sin(X) + np.cos(Y),
        r"f(x,y)=\sqrt{|x|}+\sqrt{|y|}": lambda X,Y: np.sqrt(np.abs(X)) + np.sqrt(np.abs(Y)),
        r"f(x,y)=\frac{x}{y+1}": lambda X,Y: X/(Y+1)
    }

    for label, func in examples.items():
        st.latex(label)
        X, Y = np.meshgrid(np.linspace(-4,4,50), np.linspace(-4,4,50))
        Z = func(X,Y)
        fig = go.Figure(go.Surface(x=X, y=Y, z=Z, colorscale="Blues", opacity=0.7, showscale=False))
        fig.update_layout(scene=dict(aspectratio=dict(x=1,y=1,z=0.7)), margin=dict(t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

# ==========================
# Page 2
# ==========================
elif page == "Partial Derivatives":
    st.title("Partial Derivatives")

    st.subheader("Formal Definition")
    st.latex(r"""
f_x(x,y)=\lim_{h\to0}\frac{f(x+h,y)-f(x,y)}{h},\quad
f_y(x,y)=\lim_{h\to0}\frac{f(x,y+h)-f(x,y)}{h}
""")

    st.subheader("Interpretation")
    st.markdown("""
Partial derivatives represent **rates of change** along coordinate directions.
""")

    st.latex(r"f(x,y)=x^2+y^2")

    X, Y = np.meshgrid(np.linspace(-4,4,50), np.linspace(-4,4,50))
    Z = X**2 + Y**2
    px, py = 2, 2
    z = px**2 + py**2

    fig = go.Figure()
    fig.add_surface(x=X, y=Y, z=Z, colorscale="Blues", opacity=0.7, showscale=False)
    fig.add_scatter3d(x=[px], y=[py], z=[z], mode="markers", marker=dict(size=5, color="gold"))

    s = 0.8
    fig.add_scatter3d(
        x=[px-s, px+s], y=[py, py], z=[z-2*px*s, z+2*px*s],
        mode="lines", line=dict(color="red", width=6)
    )
    fig.add_scatter3d(
        x=[px, px], y=[py-s, py+s], z=[z-2*py*s, z+2*py*s],
        mode="lines", line=dict(color="green", width=6)
    )

    fig.update_layout(scene=dict(aspectratio=dict(x=1,y=1,z=0.7)), margin=dict(t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

# ==========================
# Page 3
# ==========================
elif page == "Gradient & Steepest Ascent":
    st.title("Gradient and Steepest Ascent")

    st.latex(r"""
\nabla f(x,y)=\langle f_x(x,y), f_y(x,y)\rangle
""")

    st.latex(r"f(x,y)=x^2+y^2")

    X, Y = np.meshgrid(np.linspace(-4,4,50), np.linspace(-4,4,50))
    Z = X**2 + Y**2
    px, py = 2, 2
    z = px**2 + py**2

    fig = go.Figure()
    fig.add_surface(x=X, y=Y, z=Z, colorscale="Blues", opacity=0.7, showscale=False)
    fig.add_scatter3d(x=[px], y=[py], z=[z], mode="markers", marker=dict(size=5, color="gold"))

    grad = np.array([2*px, 2*py])
    grad /= np.linalg.norm(grad)

    fig.add_scatter3d(
        x=[px, px+grad[0]], y=[py, py+grad[1]], z=[z, z],
        mode="lines+markers", line=dict(color="black", width=8)
    )

    fig.update_layout(scene=dict(aspectratio=dict(x=1,y=1,z=0.7)), margin=dict(t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

# ==========================
# Page 4
# ==========================
else:
    st.title("Interactive Calculator")

    left, right = st.columns([3, 1])

    with right:
        tab1, tab2, tab3 = st.tabs(["Function", "Symbolic", "Point"])

        with tab1:
            func_input = st.text_input("f(x,y) =", "x^2 + y^2")
            func_input = func_input.replace("^", "**")

        transformations = standard_transformations + (implicit_multiplication_application,)
        f_expr = parse_expr(func_input, transformations=transformations)

        fx_expr = sp.diff(f_expr, x)
        fy_expr = sp.diff(f_expr, y)

        with tab2:
            st.latex(rf"f(x,y)={sp.latex(f_expr)}")
            st.latex(rf"f_x={sp.latex(fx_expr)}")
            st.latex(rf"f_y={sp.latex(fy_expr)}")

        with tab3:
            x_val = st.number_input("x", value=1.0)
            y_val = st.number_input("y", value=1.0)

    f = sp.lambdify((x,y), f_expr, "numpy")
    z_val = f(x_val, y_val)

    xs = ys = np.linspace(-4,4,60)
    X, Y = np.meshgrid(xs, ys)
    Z = f(X,Y)

    with left:
        fig = go.Figure()
        fig.add_surface(x=X, y=Y, z=Z, colorscale="Blues", opacity=0.7, showscale=False)
        fig.add_scatter3d(x=[x_val], y=[y_val], z=[z_val],
                           mode="markers", marker=dict(size=5, color="gold"))
        fig.update_layout(scene=dict(aspectratio=dict(x=1,y=1,z=0.7)), margin=dict(t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
