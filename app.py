import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

st.set_page_config(page_title="Generador de Firmas - Grupo AYASA", page_icon="📝")

st.title("Generador de Firma de Correo")
st.write("Complete sus datos para generar la firma institucional con el formato oficial.")

# Formulario (ya sin el teléfono fijo, porque se agregó al código como texto fijo)
with st.form("formulario_firma"):
    nombre = st.text_input("Nombre completo", placeholder="Ej. Ing. Arturo Villegas Garcia")
    puesto = st.text_input("Puesto de trabajo", placeholder="Ej. Coordinador de sistemas")
    telefono_movil_ext = st.text_input("Teléfono móvil o Extensión", placeholder="Ej. 560 o 921 123 4567")
    correo = st.text_input("Correo corporativo", placeholder="Ej. sistemas@grupoayasa.com")
    
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
                fuente_nombre = ImageFont.truetype("arialbd.ttf", 22)
                fuente_puesto = ImageFont.truetype("arial.ttf", 16)
                fuente_datos = ImageFont.truetype("arialbd.ttf", 18)
            except OSError:
                st.error("Error: No se encontraron las fuentes Arial.")
                st.stop()

            # --- CENTRADO DINÁMICO (Nombre y Puesto) ---
            # El panel derecho de la firma va aprox. de X=380 a X=797. Su centro visual es ~588.
            centro_x = 588
            
            # Calculamos el ancho de las palabras para centrarlas perfectamente
            ancho_nombre = draw.textlength(nombre, font=fuente_nombre)
            ancho_puesto = draw.textlength(puesto, font=fuente_puesto)
            
            x_nombre = centro_x - (ancho_nombre / 2)
            x_puesto = centro_x - (ancho_puesto / 2)

            # Imprimimos el nombre y el puesto en sus nuevas posiciones centradas
            draw.text((x_nombre, 30), nombre, font=fuente_nombre, fill="black")
            draw.text((x_puesto, 60), puesto, font=fuente_puesto, fill="black")
            
            # --- ALINEACIÓN DE DATOS DE CONTACTO ---
            # Acercamos el texto a los íconos (X=420) y los subimos para no pisar el pie de página
            x_datos = 365       
            # Teléfono fijo hardcodeado (ya no se pide en el formulario)
            draw.text((x_datos, 95), "921 215-7017/18/21", font=fuente_datos, fill="black")
            
            # Extensión / Móvil
            if telefono_movil_ext:
                draw.text((x_datos, 125), telefono_movil_ext, font=fuente_datos, fill="black")
                
            # Correo y Web
            draw.text((x_datos, 155), correo, font=fuente_datos, fill="black")
            draw.text((x_datos, 185), "www.grupoayasa.com", font=fuente_datos, fill="black")

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