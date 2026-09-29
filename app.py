import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

st.set_page_config(page_title="Generador de Firmas - Grupo AYASA", page_icon="📝")

st.title("Generador de Firma de Correo")
st.write("Complete sus datos para generar la firma institucional con el formato oficial.")

with st.form("formulario_firma"):
    nombre = st.text_input("Nombre completo", placeholder="Ej. Lic. Alfredo César Montes Patricio")
    puesto = st.text_input("Puesto de trabajo", placeholder="Ej. Asistente de Recursos Humanos")
    telefono_fijo = st.text_input("Teléfono fijo", value="921 215-7017/18/21")
    telefono_movil_ext = st.text_input("Teléfono móvil o Extensión", placeholder="Ej. 921 215 7017 EXT.204")
    correo = st.text_input("Correo corporativo", placeholder="Ej. capacitacion@grupoayasa.com")
    
    submit = st.form_submit_button("Generar Firma")

if submit:
    if nombre and puesto and correo:
        try:
            if not os.path.exists("plantilla_base.png"):
                st.error("Error: No se encontró 'plantilla_base.png'.")
                st.stop()
                
            img = Image.open("plantilla_base.png").convert("RGBA")
            draw = ImageDraw.Draw(img)
            
            try:
                # Tamaños de fuente ajustados a la imagen original
                fuente_nombre = ImageFont.truetype("arialbd.ttf", 22) # Negrita más grande
                fuente_puesto = ImageFont.truetype("arial.ttf", 16)   # Normal
                fuente_datos = ImageFont.truetype("arialbd.ttf", 18)  # Negrita para los datos
            except OSError:
                st.error("Error: No se encontraron las fuentes Arial.")
                st.stop()

            # --- COORDENADAS AJUSTADAS ---
            # X=470 alinea el texto justo a la derecha de los íconos
            x_datos = 470 
            
            # 1. Nombre y Puesto (centrados visualmente en el bloque superior)
            draw.text((450, 30), nombre, font=fuente_nombre, fill="black")
            draw.text((490, 60), puesto, font=fuente_puesto, fill="black")
            
            # 2. Datos de contacto alineados a los íconos (ajusta la Y si quedan muy arriba o abajo)
            draw.text((x_datos, 120), telefono_fijo, font=fuente_datos, fill="black")
            
            if telefono_movil_ext:
                draw.text((x_datos, 155), telefono_movil_ext, font=fuente_datos, fill="black")
                
            draw.text((x_datos, 190), correo, font=fuente_datos, fill="black")
            draw.text((x_datos, 225), "www.grupoayasa.com", font=fuente_datos, fill="black")

            # Guardar y mostrar
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.success("¡Firma generada con éxito!")
            st.image(byte_im, caption=f"Firma_{nombre.split()[0]}.png")

            st.download_button(
                label="Descargar Firma PNG",
                data=byte_im,
                file_name=f"Firma_{nombre.replace(' ', '_')}.png",
                mime="image/png"
            )
            
        except Exception as e:
            st.error(f"Error inesperado: {e}")
    else:
        st.warning("Complete el Nombre, Puesto y Correo.")