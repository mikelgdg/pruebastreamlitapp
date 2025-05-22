from PIL import Image
import streamlit as st
import pandas as pd
from streamlit_drawable_canvas import st_canvas

st.set_page_config(
    page_title="Streamlit Drawable Canvas",
    page_icon="✏️",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("Streamlit Drawable Canvas")
st.markdown(
    """
    This is a simple example of using the `streamlit-drawable-canvas` component.
    You can draw on the canvas, and the drawing will be displayed in real-time.
    """
)


drawing_mode = st.sidebar.selectbox(
    "Drawing tool:",
    ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
)
stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
if drawing_mode == "point":
    point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color hex: ")
bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
#bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
realtime_update = st.sidebar.checkbox("Update in realtime", True)

uploaded_file = st.sidebar.file_uploader(" ", label_visibility="collapsed", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image=image.resize((300, 300), resample=Image.Resampling.LANCZOS)


    from PIL import Image, ImageDraw
    import matplotlib.pyplot as plt

# Cargar imagen (usa tu propia ruta)

    draw = ImageDraw.Draw(image)

    # Bounding box: (x, y, ancho, alto)
    x, y, w, h = 100, 100, 50, 50

    # Dibujar bbox
    draw.rectangle([x, y, x + w, y + h], outline="red", width=3)

    # Calcular centro inferior
    cx, cy = x + w / 2, y + h

    # Dibujar el punto central inferior
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill="blue")

    # Mostrar imagen con matplotlib
    plt.imshow(image)
    plt.axis("off")
    plt.show()



# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=image,
    height=300,
    width=300,
    update_streamlit=realtime_update,
    drawing_mode=drawing_mode,
    point_display_radius=point_display_radius if drawing_mode == "point" else 0,
    display_toolbar=st.sidebar.checkbox("Display toolbar", True),
    key="full_app",
)

coords=[]
    
if canvas_result.json_data is not None:
    print(f"JSON: {canvas_result.json_data}")
    objects = canvas_result.json_data.get("objects", [])
    
    # Buscar el primer objeto tipo 'path' (polígono)
    for obj in objects:
        if obj.get("type") == "path":
            coords = [(cmd[1], 300-cmd[2]) for cmd in obj["path"] if cmd[0] in ("M", "L")]
            
            if len(coords) >= 3:  # Ya hay suficientes puntos para un polígono
                st.success("¡Polígono finalizado!")
                st.write("Coordenadas:", coords)
            else:
                st.info("Dibuja al menos 3 puntos para formar el polígono.")
            
    
            print(coords)


#PARTE DOS

bbox = (100, 100, 50, 50)  # x, y, width, height

from shapely.geometry import Polygon, Point

# Tu polígono
polygon = Polygon(coords)

# Tu bbox
x, y, w, h = 100, 100, 50, 50
bottom_center = (x + w / 2, y + h)
point = Point(bottom_center)

# Verifica si el punto está dentro del polígono
if polygon.contains(point):
    print("El centro inferior de la bbox está DENTRO del polígono. Realizar inferencia.")
else:
    print("El centro inferior de la bbox está FUERA del polígono. No hacer nada.")

