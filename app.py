import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

st.set_page_config(page_title="Generador de Firmas - Grupo AYASA", page_icon="📝")

st.title("Generador de Firma de Correo")
st.write("Complete sus datos para generar la firma empresarial con el formato oficial.")

# Formulario
with st.form("formulario_firma"):
    nombre = st.text_input(
        "Título y Nombre completo", 
        placeholder="Ej. Ing. Arturo Villegas Garcia"
    )
    puesto = st.text_input("Puesto de trabajo", placeholder="Ej. Coordinador Sistemas")
    
    col1, col2 = st.columns(2)
    with col1:
        telefono_movil = st.text_input("Número de Celular si es que aplica", placeholder="Ej. 921785748")
    with col2:
        num_extension = st.text_input("Número de Extensión", placeholder="Ej. 530")
        
    correo = st.text_input("Correo corporativo", placeholder="Ej. sistemas@grupoayasa.com")
    
    submit = st.form_submit_button("Generar Firma")

if submit:
    # Validaciones independientes para cada campo faltante
    campos_faltantes = []
    if not nombre:
        campos_faltantes.append("Título y Nombre completo")
    if not puesto:
        campos_faltantes.append("Puesto de trabajo")
    if not correo:
        campos_faltantes.append("Correo corporativo")

    if campos_faltantes:
        # Muestra una advertencia detallada indicando todos los campos que el usuario dejó vacíos
        st.warning(f"Por favor, complete los siguientes campos obligatorios: **{', '.join(campos_faltantes)}**.")
    else:
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

            # --- CENTRADO DINÁMICO (Nombre y Puesto con Título) ---
            centro_x = 588
            
            ancho_nombre = draw.textlength(nombre, font=fuente_nombre)
            ancho_puesto = draw.textlength(puesto, font=fuente_puesto)
            
            x_nombre = centro_x - (ancho_nombre / 2)
            x_puesto = centro_x - (ancho_puesto / 2)

            draw.text((x_nombre, 30), nombre, font=fuente_nombre, fill="black")
            draw.text((x_puesto, 60), puesto, font=fuente_puesto, fill="black")
            
            # --- CONCATENACIÓN DE TELÉFONO FIJO Y EXTENSIÓN ---
            # Agrega "EXT." al número fijo si el usuario escribió una extensión
            if num_extension:
                texto_fijo_ext = f"921 215-7017/18/21 ext. {num_extension}"
            else:
                texto_fijo_ext = "921 215-7017/18/21"

            # --- ALINEACIÓN DE DATOS DE CONTACTO (Intactas) ---
            x_datos = 365       
            y_inicial = 103 
            espaciado = 26 
            
            # 1. Teléfono fijo corporativo con su extensión al lado
            draw.text((x_datos, y_inicial), texto_fijo_ext, font=fuente_datos, fill="black")
            
            # 2. Celular (Se imprime solo en el segundo renglón si se proporciona)
            if telefono_movil:
                draw.text((x_datos, y_inicial + espaciado), telefono_movil, font=fuente_datos, fill="black")
                
            # 3. Correo y Web
            draw.text((x_datos, y_inicial + (espaciado * 2)), correo, font=fuente_datos, fill="black")
            draw.text((x_datos, y_inicial + (espaciado * 3)), "www.grupoayasa.com", font=fuente_datos, fill="black")

            # Guardar y mostrar
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.success("¡Firma generada con éxito!")
            st.image(byte_im, caption=f"Firma_{nombre.split()[-1]}.png")

            st.download_button(
                label="Descargar Firma PNG",
                data=byte_im,
                file_name=f"Firma_{nombre.replace(' ', '_')}.png",
                mime="image/png"
            )
            
        except Exception as e:
            st.error(f"Error inesperado: {e}")