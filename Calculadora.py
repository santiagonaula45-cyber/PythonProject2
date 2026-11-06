
import streamlit as st
import sympy as sp
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math

# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Calculadora Científica Universitaria",
    page_icon="🧮",
    layout="wide"
)

# Estilos
st.markdown("""
<style>
.main {
    background-color: #101827;
}
h1, h2, h3 {
    color: #60A5FA;
}
.stButton>button {
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🧮 CALCULADORA CIENTÍFICA UNIVERSITARIA")
st.markdown("### Herramienta matemática para Ingeniería y Ciencias")

st.caption("Python | Streamlit | SymPy | NumPy | Plotly")

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

x, y, z = sp.symbols("x y z")

def calcular(expresion, grados=False):
    expresion = expresion.replace("^", "**")

    funciones = {
        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,
        "asin": sp.asin,
        "acos": sp.acos,
        "atan": sp.atan,
        "sqrt": sp.sqrt,
        "log": sp.log,
        "ln": sp.log,
        "exp": sp.exp,
        "abs": sp.Abs,
        "pi": sp.pi,
        "E": sp.E,
        "factorial": sp.factorial,
        "sinh": sp.sinh,
        "cosh": sp.cosh,
        "tanh": sp.tanh
    }

    resultado = sp.sympify(expresion, locals=funciones)

    if grados:
        resultado = resultado.subs({
            sp.sin(x): sp.sin(x * sp.pi / 180)
        })

    return resultado


def mostrar_resultado(resultado):
    st.success("Resultado: " + str(resultado))
    try:
        st.info("Valor decimal: " + str(sp.N(resultado, 12)))
    except Exception:
        pass


def leer_matriz(texto):
    filas = texto.strip().split("\n")
    matriz = []

    for fila in filas:
        valores = fila.replace(",", " ").split()
        matriz.append([float(v) for v in valores])

    if not matriz or any(len(f) != len(matriz[0]) for f in matriz):
        raise ValueError("La matriz debe tener filas del mismo tamaño.")

    return sp.Matrix(matriz)


# ==========================================
# MENÚ LATERAL
# ==========================================

st.sidebar.title("⚙️ Configuración")

modo = st.sidebar.radio(
    "Seleccionar módulo",
    [
        "Calculadora básica",
        "Funciones científicas",
        "Cálculo diferencial e integral",
        "Matrices y determinantes",
        "Ecuaciones y sistemas",
        "Estadística",
        "Conversor de unidades",
        "Gráficas matemáticas"
    ]
)

grados = st.sidebar.selectbox(
    "Unidad angular",
    ["Grados", "Radianes"]
) == "Grados"

st.sidebar.divider()
st.sidebar.markdown("### 📚 Herramienta universitaria")
st.sidebar.caption("Diseñada para Matemáticas, Física e Ingeniería Civil.")

# ==========================================
# HISTORIAL
# ==========================================

if "historial" not in st.session_state:
    st.session_state.historial = []

def guardar_historial(operacion, resultado):
    st.session_state.historial.append({
        "Operación": operacion,
        "Resultado": str(resultado)
    })

# ==========================================
# 1. CALCULADORA BÁSICA
# ==========================================

if modo == "Calculadora básica":

    st.header("🔢 Calculadora básica")

    expresion = st.text_input(
        "Introduce tu operación matemática:",
        placeholder="Ejemplo: (25 + 15) * 3 / 2"
    )

    st.caption(
        "Puedes utilizar +, -, *, /, ^, paréntesis y números decimales."
    )

    if st.button("CALCULAR", type="primary"):
        try:
            resultado = calcular(expresion)
            mostrar_resultado(resultado)
            guardar_historial(expresion, resultado)
        except Exception as e:
            st.error(f"Operación no válida: {e}")

    st.markdown("#### Ejemplos")
    st.code("""
25 + 15
(20 * 5) / 2
2^8
sqrt(144)
factorial(5)
""")

# ==========================================
# 2. FUNCIONES CIENTÍFICAS
# ==========================================

elif modo == "Funciones científicas":

    st.header("📐 Funciones científicas")

    st.markdown("### Trigonometría, logaritmos y potencias")

    expresion = st.text_input(
        "Escribe la función:",
        placeholder="Ejemplo: sin(30) + cos(60)"
    )

    if st.button("RESOLVER FUNCIÓN", type="primary"):
        try:
            expresion = expresion.replace("^", "**")

            if grados:
                expresion = expresion.replace(
                    "sin(", "sin(pi/180*"
                ).replace(
                    "cos(", "cos(pi/180*"
                ).replace(
                    "tan(", "tan(pi/180*"
                )

            resultado = calcular(expresion)
            mostrar_resultado(resultado)
            guardar_historial(expresion, resultado)

        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("### Funciones disponibles")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **Trigonometría**
        - sin(x)
        - cos(x)
        - tan(x)
        - asin(x)
        - acos(x)
        - atan(x)
        """)

    with col2:
        st.markdown("""
        **Logaritmos**
        - log(x)
        - ln(x)
        - log(x, 2)
        - exp(x)
        """)

    with col3:
        st.markdown("""
        **Otras funciones**
        - sqrt(x)
        - factorial(x)
        - sinh(x)
        - cosh(x)
        - tanh(x)
        - abs(x)
        """)

    st.info("Constantes disponibles: pi y E.")

# ==========================================
# 3. CÁLCULO DIFERENCIAL E INTEGRAL
# ==========================================

elif modo == "Cálculo diferencial e integral":

    st.header("∫ Cálculo diferencial e integral")

    operacion = st.selectbox(
        "Selecciona la operación",
        [
            "Derivada",
            "Segunda derivada",
            "Integral indefinida",
            "Integral definida",
            "Límite"
        ]
    )

    funcion = st.text_input(
        "Introduce la función f(x):",
        value="x^2 + 3*x + 2"
    )

    if operacion == "Límite":
        punto = st.number_input("Punto al que tiende x:", value=0.0)

        lado = st.selectbox(
            "Dirección",
            ["Ambos lados", "Por la derecha", "Por la izquierda"]
        )

    if operacion == "Integral definida":
        a = st.number_input("Límite inferior:", value=0.0)
        b = st.number_input("Límite superior:", value=1.0)

    if st.button("RESOLVER CÁLCULO", type="primary"):

        try:
            f = calcular(funcion)
            resultado = None

            if operacion == "Derivada":
                resultado = sp.diff(f, x)

            elif operacion == "Segunda derivada":
                resultado = sp.diff(f, x, 2)

            elif operacion == "Integral indefinida":
                resultado = sp.integrate(f, x)

            elif operacion == "Integral definida":
                resultado = sp.integrate(f, (x, a, b))

            elif operacion == "Límite":

                if lado == "Por la derecha":
                    resultado = sp.limit(f, x, punto, dir="+")

                elif lado == "Por la izquierda":
                    resultado = sp.limit(f, x, punto, dir="-")

                else:
                    resultado = sp.limit(f, x, punto)

            st.success("Resultado matemático:")
            st.latex(sp.latex(resultado))
            st.write("Valor decimal:", sp.N(resultado))
            guardar_historial(operacion + ": " + funcion, resultado)

        except Exception as e:
            st.error(f"No se pudo resolver: {e}")

# ==========================================
# 4. MATRICES Y DETERMINANTES
# ==========================================

elif modo == "Matrices y determinantes":

    st.header("🔲 Álgebra matricial")

    st.markdown("""
    Introduce una matriz escribiendo una fila por línea
    y separando los números con espacios.
    """)

    texto_a = st.text_area(
        "Matriz A",
        "1 2\n3 4",
        height=100
    )

    texto_b = st.text_area(
        "Matriz B",
        "5 6\n7 8",
        height=100
    )

    operacion = st.selectbox(
        "Operación matricial",
        [
            "Determinante de A",
            "Matriz inversa de A",
            "Transpuesta de A",
            "Suma A + B",
            "Resta A - B",
            "Multiplicación A × B",
            "Rango de A",
            "Valores propios de A"
        ]
    )

    if st.button("CALCULAR MATRIZ", type="primary"):

        try:
            A = leer_matriz(texto_a)
            B = leer_matriz(texto_b)

            if operacion == "Determinante de A":
                if A.rows != A.cols:
                    raise ValueError("A debe ser cuadrada.")
                resultado = A.det()

            elif operacion == "Matriz inversa de A":
                resultado = A.inv()

            elif operacion == "Transpuesta de A":
                resultado = A.T

            elif operacion == "Suma A + B":
                resultado = A + B

            elif operacion == "Resta A - B":
                resultado = A - B

            elif operacion == "Multiplicación A × B":
                resultado = A * B

            elif operacion == "Rango de A":
                resultado = A.rank()

            else:
                if A.rows != A.cols:
                    raise ValueError("A debe ser cuadrada.")
                resultado = A.eigenvals()

            st.success("Resultado:")
            st.write(resultado)
            guardar_historial(operacion, resultado)

        except Exception as e:
            st.error(f"Error matricial: {e}")

# ==========================================
# 5. ECUACIONES Y SISTEMAS
# ==========================================

elif modo == "Ecuaciones y sistemas":

    st.header("📘 Resolución de ecuaciones")

    tipo = st.radio(
        "Tipo de problema",
        ["Ecuación de una variable", "Sistema de dos ecuaciones"]
    )

    if tipo == "Ecuación de una variable":

        ecuacion = st.text_input(
            "Introduce la ecuación igualada a cero:",
            "x^2 - 5*x + 6"
        )

        if st.button("RESOLVER ECUACIÓN", type="primary"):
            try:
                expresion = calcular(ecuacion)
                soluciones = sp.solve(expresion, x)

                st.success("Soluciones encontradas:")
                for i, sol in enumerate(soluciones, 1):
                    st.write(f"Solución {i}:")
                    st.latex("x = " + sp.latex(sol))

                guardar_historial(ecuacion, soluciones)

            except Exception as e:
                st.error(str(e))

    else:

        st.markdown("Ejemplo: 2x + 3y = 8")

        ecuacion1 = st.text_input(
            "Primera ecuación (igualada a cero):",
            "2*x + 3*y - 8"
        )

        ecuacion2 = st.text_input(
            "Segunda ecuación (igualada a cero):",
            "x - y - 1"
        )

        if st.button("RESOLVER SISTEMA", type="primary"):
            try:
                f1 = calcular(ecuacion1)
                f2 = calcular(ecuacion2)

                resultado = sp.solve(
                    [f1, f2], (x, y), dict=True
                )

                st.success("Solución del sistema:")
                st.write(resultado)
                guardar_historial("Sistema de ecuaciones", resultado)

            except Exception as e:
                st.error(str(e))

# ==========================================
# 6. ESTADÍSTICA
# ==========================================

elif modo == "Estadística":

    st.header("📊 Estadística descriptiva")

    datos_texto = st.text_area(
        "Introduce los datos separados por comas:",
        "10, 20, 30, 40, 50, 60"
    )

    if st.button("ANALIZAR DATOS", type="primary"):

        try:
            datos = [
                float(v.strip())
                for v in datos_texto.split(",")
                if v.strip()
            ]

            if not datos:
                raise ValueError("Introduce al menos un dato.")

            serie = pd.Series(datos)

            media = serie.mean()
            mediana = serie.median()
            moda = serie.mode().tolist()
            varianza = serie.var(ddof=1) if len(datos)>1 else 0
            desviacion = serie.std(ddof=1) if len(datos)>1 else 0

            c1, c2, c3 = st.columns(3)

            c1.metric("Media", f"{media:.4f}")
            c2.metric("Mediana", f"{mediana:.4f}")
            c3.metric("Desviación estándar", f"{desviacion:.4f}")

            st.write("**Moda:**", moda)
            st.write("**Varianza muestral:**", varianza)
            st.write("**Mínimo:**", serie.min())
            st.write("**Máximo:**", serie.max())
            st.write("**Cantidad de datos:**", len(datos))

            fig = go.Figure()
            fig.add_trace(go.Histogram(x=datos, nbinsx=15))
            fig.update_layout(
                title="Histograma de frecuencias",
                xaxis_title="Valores",
                yaxis_title="Frecuencia"
            )
            st.plotly_chart(fig, use_container_width=True)

            guardar_historial("Análisis estadístico", media)

        except Exception as e:
            st.error(f"Error en los datos: {e}")

# ==========================================
# 7. CONVERSOR DE UNIDADES
# ==========================================

elif modo == "Conversor de unidades":

    st.header("📏 Conversor de unidades")

    unidades = {
        "Longitud": {
            "Metro (m)": 1,
            "Kilómetro (km)": 1000,
            "Centímetro (cm)": 0.01,
            "Milímetro (mm)": 0.001,
            "Pulgada (in)": 0.0254,
            "Pie (ft)": 0.3048,
            "Yarda (yd)": 0.9144
        },
        "Masa": {
            "Kilogramo (kg)": 1,
            "Gramo (g)": 0.001,
            "Tonelada (t)": 1000,
            "Libra (lb)": 0.45359237
        },
        "Área": {
            "Metro cuadrado (m²)": 1,
            "Centímetro cuadrado (cm²)": 0.0001,
            "Hectárea (ha)": 10000,
            "Kilómetro cuadrado (km²)": 1000000,
            "Pie cuadrado (ft²)": 0.09290304
        },
        "Volumen": {
            "Metro cúbico (m³)": 1,
            "Litro (L)": 0.001,
            "Mililitro (mL)": 0.000001,
            "Pie cúbico (ft³)": 0.02831685
        },
        "Velocidad": {
            "Metro por segundo (m/s)": 1,
            "Kilómetro por hora (km/h)": 1/3.6,
            "Milla por hora (mph)": 0.44704
        },
        "Fuerza": {
            "Newton (N)": 1,
            "Kilonewton (kN)": 1000,
            "Libra-fuerza (lbf)": 4.448221615
        },
        "Presión": {
            "Pascal (Pa)": 1,
            "Kilopascal (kPa)": 1000,
            "Megapascal (MPa)": 1000000,
            "Bar": 100000,
            "Atmósfera (atm)": 101325
        }
    }

    categoria = st.selectbox(
        "Categoría",
        list(unidades.keys())
    )

    opciones = list(unidades[categoria].keys())

    col1, col2 = st.columns(2)

    with col1:
        valor = st.number_input("Cantidad", value=1.0)
        origen = st.selectbox("Convertir desde", opciones)

    with col2:
        destino = st.selectbox("Convertir hacia", opciones)

    if st.button("CONVERTIR", type="primary"):

        resultado = (
            valor * unidades[categoria][origen]
            / unidades[categoria][destino]
        )

        st.success(f"Resultado: {resultado:.10g}")
        guardar_historial(
            f"{valor} {origen} a {destino}",
            resultado
        )

    st.divider()

    st.markdown("### 🌡️ Conversión de temperatura")

    temp = st.number_input("Temperatura", value=25.0)
    origen_temp = st.selectbox(
        "Desde",
        ["Celsius", "Fahrenheit", "Kelvin"]
    )

    destino_temp = st.selectbox(
        "Hacia",
        ["Celsius", "Fahrenheit", "Kelvin"]
    )

    if st.button("CONVERTIR TEMPERATURA"):

        if origen_temp == "Celsius":
            c = temp
        elif origen_temp == "Fahrenheit":
            c = (temp - 32) * 5/9
        else:
            c = temp - 273.15

        if destino_temp == "Celsius":
            resultado = c
        elif destino_temp == "Fahrenheit":
            resultado = c * 9/5 + 32
        else:
            resultado = c + 273.15

        st.success(f"{resultado:.4f} {destino_temp}")

# ==========================================
# 8. GRÁFICAS MATEMÁTICAS
# ==========================================

elif modo == "Gráficas matemáticas":

    st.header("📈 Graficador de funciones")

    funcion = st.text_input(
        "Introduce f(x):",
        "x^2 - 4"
    )

    col1, col2 = st.columns(2)

    with col1:
        xmin = st.number_input("Valor mínimo de X", value=-10.0)

    with col2:
        xmax = st.number_input("Valor máximo de X", value=10.0)

    if st.button("GENERAR GRÁFICA", type="primary"):

        try:
            expresion = calcular(funcion)

            funcion_numerica = sp.lambdify(
                x, expresion, modules=["numpy"]
            )

            valores_x = np.linspace(xmin, xmax, 1000)

            with np.errstate(all="ignore"):
                valores_y = funcion_numerica(valores_x)

            if np.isscalar(valores_y):
                valores_y = np.full_like(valores_x, valores_y)

            valores_y = np.asarray(valores_y, dtype=float)

            if valores_y.ndim == 0:
                valores_y = np.full_like(valores_x, valores_y)

            if valores_y.shape != valores_x.shape:
                raise ValueError("La función no produce una curva válida.")

            valores_y[~np.isfinite(valores_y)] = np.nan

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=valores_x,
                y=valores_y,
                mode="lines",
                name=f"f(x) = {funcion}"
            ))

            fig.update_layout(
                title=f"Gráfica de f(x) = {funcion}",
                xaxis_title="Eje X",
                yaxis_title="Eje Y",
                template="plotly_dark",
                height=550
            )

            fig.update_xaxes(showgrid=True, zeroline=True)
            fig.update_yaxes(showgrid=True, zeroline=True)

            st.plotly_chart(fig, use_container_width=True)

            st.success("Gráfica generada correctamente.")

        except Exception as e:
            st.error(f"No se pudo generar la gráfica: {e}")

# ==========================================
# HISTORIAL GENERAL
# ==========================================

st.divider()

st.header("📜 Historial de operaciones")

if st.session_state.historial:

    df = pd.DataFrame(st.session_state.historial)

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Descargar historial CSV",
        data=csv,
        file_name="historial_calculadora.csv",
        mime="text/csv"
    )

    if st.button("🗑️ Borrar historial"):
        st.session_state.historial = []
        st.rerun()

else:
    st.info("Todavía no existen operaciones registradas.")

st.divider()

st.caption(
    "Calculadora Científica Universitaria | "
    "Desarrollada con Python y Streamlit"
)
