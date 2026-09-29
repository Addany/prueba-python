import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

# Configuración de la página
st.set_page_config(page_title="Generador de Firmas - Grupo AYASA", page_icon="📝")

st.title("Generador de Firma de Correo")
st.write("Complete sus datos para generar la firma institucional con el formato oficial.")

# Formulario para evitar recargas constantes
with st.form("formulario_firma"):
    nombre = st.text_input("Nombre completo", placeholder="Ej. ARTURO VILLEGAS GARCIA")
    puesto = st.text_input("Puesto de trabajo", placeholder="Ej. Coordinador de Sistemas")
    telefono = st.text_input("Número de teléfono", placeholder="Ej. 921 215-7017 /18 /21")
    extension = st.text_input("Extensión (opcional)", placeholder="Ej. 510")
    correo = st.text_input("Correo corporativo", placeholder="Ej. sistemas@grupoayasa.com")
    
    submit = st.form_submit_button("Generar Firma")

if submit:
    if nombre and puesto and correo:
        try:
            # 1. Cargar la plantilla base de 797x387 pixeles
            if not os.path.exists("plantilla_base.png"):
                st.error("Error: No se encontró el archivo 'plantilla_base.png' en el servidor.")
                st.stop()
                
            img = Image.open("plantilla_base.png").convert("RGBA")
            draw = ImageDraw.Draw(img)
            
            # 2. Cargar las fuentes (deben estar en la misma carpeta)
            try:
                fuente_nombre = ImageFont.truetype("arialbd.ttf", 20)
                fuente_puesto = ImageFont.truetype("arialbd.ttf", 16)
                fuente_texto = ImageFont.truetype("arial.ttf", 14)
            except OSError:
                st.error("Error: No se encontraron los archivos de fuente 'arial.ttf' o 'arialbd.ttf'.")
                st.stop()

            # 3. Superponer textos en las coordenadas correspondientes
            draw.text((380, 50), nombre.upper(), font=fuente_nombre, fill="black")
            draw.text((410, 80), puesto, font=fuente_puesto, fill="black")
            draw.text((400, 110), telefono, font=fuente_texto, fill="black")
            
            if extension:
                draw.text((600, 110), f"EXT. {extension}", font=fuente_texto, fill="black")
                
            draw.text((400, 140), correo, font=fuente_texto, fill="black")

            # 4. Guardar la imagen en memoria
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()

            # 5. Mostrar resultados
            st.success("¡Firma generada con éxito!")
            st.image(byte_im, caption=f"Firma_{nombre.title()}.png")

            st.download_button(
                label="Descargar Firma PNG",
                data=byte_im,
                file_name=f"Firma_{nombre.title().replace(' ', '_')}.png",
                mime="image/png"
            )
            
        except Exception as e:
            st.error(f"Ocurrió un error inesperado: {e}")
    else:
        st.warning("Por favor, complete los campos obligatorios (Nombre, Puesto, Correo).")