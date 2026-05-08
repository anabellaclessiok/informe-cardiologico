import streamlit as st
import streamlit.components.v1 as components
from datetime import date
from database import guardar_informe, buscar_informes, obtener_todos, obtener_informe_por_id

st.set_page_config(
    page_title="Informe Ecocardiográfico",
    page_icon="🫀",
    layout="wide"
)

st.markdown("""
<style>
    .stButton button {
        width: 100% !important;
        min-height: 50px !important;
        background-color: #1a3a5c !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        background-color: #1a3a5c !important;
        color: white !important;
        box-shadow: 0 0 12px 3px rgba(100, 160, 255, 0.7) !important;
        transform: translateY(-1px) !important;
    }
    .stButton {
        display: flex !important;
        justify-content: center !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Inicializar estado ──
if "paso" not in st.session_state:
    st.session_state.paso = 1
if "datos" not in st.session_state:
    st.session_state.datos = {}

def menu_navegacion():
    with st.expander("Ir a una sección"):
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            if st.button("Datos paciente", key="nav1"):
                st.session_state.paso = 1
                st.rerun()
        with c2:
            if st.button("Mediciones Bid.", key="nav2"):
                st.session_state.paso = 2
                st.rerun()
        with c3:
            if st.button("Doppler medic.", key="nav3"):
                st.session_state.paso = 3
                st.rerun()
        with c4:
            if st.button("Hallazgos", key="nav4"):
                st.session_state.paso = 4
                st.rerun()
        with c5:
            if st.button("Doppler texto", key="nav5"):
                st.session_state.paso = 5
                st.rerun()
        c6, c7, c8, c9 = st.columns(4)
        with c6:
            if st.button("Conclusión", key="nav6"):
                st.session_state.paso = 6
                st.rerun()
        with c7:
            if st.button("Imágenes", key="nav7"):
                st.session_state.paso = 7
                st.rerun()
        with c8:
            if st.button("🔍 Buscar informe", key="nav_buscar"):
                st.session_state.paso = 9
                st.rerun()
        with c9:
            if st.button("Nuevo informe", key="nav8"):
                st.session_state.paso = 1
                st.session_state.datos = {}
                st.rerun()

col_form, col_prev = st.columns([1, 1], gap="large")

with col_form:

    # ── PASO 1: Datos del paciente ──
    if st.session_state.paso == 1:
        menu_navegacion()
        st.markdown("Paso 1 — Datos del Paciente")

        fecha = st.date_input(
            "Fecha",
            value=date.today(),
            format="DD/MM/YYYY"
        )

        paciente        = st.text_input("Apellido y Nombre del paciente",
                            value=st.session_state.datos.get("paciente", ""))
        edad            = st.text_input("Edad",
                            value=st.session_state.datos.get("edad", ""))
        obra_social     = st.text_input("Obra Social",
                            value=st.session_state.datos.get("obra_social", ""))
        medico_solicita = st.text_input("Médico que solicita",
                            value=st.session_state.datos.get("medico_solicita", ""))

        if st.button("Siguiente →"):
            st.session_state.datos["paciente"]        = paciente
            st.session_state.datos["edad"]            = edad
            st.session_state.datos["fecha"]           = fecha.strftime('%d/%m/%Y')
            st.session_state.datos["obra_social"]     = obra_social
            st.session_state.datos["medico_solicita"] = medico_solicita
            st.session_state.paso = 2
            st.rerun()

    # ── PASO 2: Mediciones Bidimensional ──
    elif st.session_state.paso == 2:
        menu_navegacion()
        st.markdown("Paso 2 — Mediciones Bidimensional y Modo M")

        c1, c2 = st.columns(2)
        with c1:
            ddvi    = st.text_input("Diámetro fin de diástole VI",    value=st.session_state.datos.get("ddvi", ""))
            dsvi    = st.text_input("Diámetro fin de sístole VI",     value=st.session_state.datos.get("dsvi", ""))
            fa      = st.text_input("Fracción Acortamiento (%)",      value=st.session_state.datos.get("fa", ""))
            fe      = st.text_input("Fracción de Eyección (%)",       value=st.session_state.datos.get("fe", ""))
            sep     = st.text_input("Espesor Septal",                 value=st.session_state.datos.get("sep", ""))
            pp      = st.text_input("Espesor Pared Posterior",        value=st.session_state.datos.get("pp", ""))
        with c2:
            vd      = st.text_input("Diámetro del VD",                value=st.session_state.datos.get("vd", ""))
            ao      = st.text_input("Diámetro Raíz Aorta (cm)",       value=st.session_state.datos.get("ao", ""))
            ai      = st.text_input("Diámetro de AI",                 value=st.session_state.datos.get("ai", ""))
            ai_area = st.text_input("Área AI (cm²)",                  value=st.session_state.datos.get("ai_area", ""))
            ai_vol  = st.text_input("Volumen AI (ml/m²)",             value=st.session_state.datos.get("ai_vol", ""))
            imvi    = st.text_input("Índice Masa VI (g/m²)",          value=st.session_state.datos.get("imvi", ""))

        def guardar_paso2():
            st.session_state.datos["ddvi"]    = ddvi
            st.session_state.datos["dsvi"]    = dsvi
            st.session_state.datos["fa"]      = fa
            st.session_state.datos["fe"]      = fe
            st.session_state.datos["sep"]     = sep
            st.session_state.datos["pp"]      = pp
            st.session_state.datos["vd"]      = vd
            st.session_state.datos["ao"]      = ao
            st.session_state.datos["ai"]      = ai
            st.session_state.datos["ai_area"] = ai_area
            st.session_state.datos["ai_vol"]  = ai_vol
            st.session_state.datos["imvi"]    = imvi

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Anterior"):
                guardar_paso2()
                st.session_state.paso = 1
                st.rerun()
        with col2:
            if st.button("Siguiente →"):
                guardar_paso2()
                st.session_state.paso = 3
                st.rerun()

    # ── PASO 3: Mediciones Doppler ──
    elif st.session_state.paso == 3:
        menu_navegacion()
        st.markdown("Paso 3 — Mediciones Doppler")

        c1, c2 = st.columns(2)
        with c1:
            vel_ao   = st.text_input("Velocidad Pico Ao cm/s – TSVI",      value=st.session_state.datos.get("vel_ao", ""))
            vel_pul  = st.text_input("Velocidad Pico Pulmonar cm/s",        value=st.session_state.datos.get("vel_pul", ""))
            onda_e   = st.text_input("Onda E Mitral cm/seg",                value=st.session_state.datos.get("onda_e", ""))
            psap     = st.text_input("Presión Sistólica VD y Pul. mmHg",   value=st.session_state.datos.get("psap", ""))
        with c2:
            grad_ao  = st.text_input("Gradiente Aorta (mmHg)",              value=st.session_state.datos.get("grad_ao", ""))
            grad_pul = st.text_input("Gradiente Pulmonar mmHg",             value=st.session_state.datos.get("grad_pul", ""))
            onda_a   = st.text_input("Onda A Mitral cm/seg",                value=st.session_state.datos.get("onda_a", ""))

        def guardar_paso3():
            st.session_state.datos["vel_ao"]   = vel_ao
            st.session_state.datos["grad_ao"]  = grad_ao
            st.session_state.datos["vel_pul"]  = vel_pul
            st.session_state.datos["grad_pul"] = grad_pul
            st.session_state.datos["onda_e"]   = onda_e
            st.session_state.datos["onda_a"]   = onda_a
            st.session_state.datos["psap"]     = psap

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Anterior"):
                guardar_paso3()
                st.session_state.paso = 2
                st.rerun()
        with col2:
            if st.button("Siguiente →"):
                guardar_paso3()
                st.session_state.paso = 4
                st.rerun()

    # ── PASO 4: Hallazgos ──
    elif st.session_state.paso == 4:
        menu_navegacion()
        st.markdown("Paso 4 — Hallazgos")
        hallazgos = st.text_area("Hallazgos", height=250,
                        value=st.session_state.datos.get("hallazgos", ""))

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Anterior"):
                st.session_state.datos["hallazgos"] = hallazgos
                st.session_state.paso = 3
                st.rerun()
        with col2:
            if st.button("Siguiente →"):
                st.session_state.datos["hallazgos"] = hallazgos
                st.session_state.paso = 5
                st.rerun()

    # ── PASO 5: Doppler ──
    elif st.session_state.paso == 5:
        menu_navegacion()
        st.markdown("Paso 5 — Doppler")
        doppler = st.text_area("Doppler", height=200,
                    value=st.session_state.datos.get("doppler", ""))

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Anterior"):
                st.session_state.datos["doppler"] = doppler
                st.session_state.paso = 4
                st.rerun()
        with col2:
            if st.button("Siguiente →"):
                st.session_state.datos["doppler"] = doppler
                st.session_state.paso = 6
                st.rerun()

    # ── PASO 6: Conclusión ──
    elif st.session_state.paso == 6:
        menu_navegacion()
        st.markdown("Paso 6 — Conclusión")
        conclusion = st.text_area("Conclusión", height=200,
                        value=st.session_state.datos.get("conclusion", ""))

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Anterior"):
                st.session_state.datos["conclusion"] = conclusion
                st.session_state.paso = 5
                st.rerun()
        with col2:
            if st.button("Siguiente →"):
                st.session_state.datos["conclusion"] = conclusion
                st.session_state.paso = 7
                st.rerun()

    # ── PASO 7: Imágenes ──
    elif st.session_state.paso == 7:
        st.markdown("Paso 7 — Imágenes")
        imagenes = st.file_uploader(
            "Cargar imágenes del estudio",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="uploader_imagenes"
        )

        if imagenes:
            import base64
            from PIL import Image as PILImage
            from io import BytesIO
            imagenes_b64 = []
            for img in imagenes:
                try:
                    img.seek(0)
                    pil_img = PILImage.open(img).convert("RGB")
                    buf = BytesIO()
                    pil_img.save(buf, format="JPEG", quality=90)
                    buf.seek(0)
                    b64 = base64.b64encode(buf.read()).decode()
                    imagenes_b64.append(f"data:image/jpeg;base64,{b64}")
                except Exception as e:
                    st.warning(f"No se pudo cargar {img.name}: {e}")

            st.session_state.datos["imagenes_b64"] = imagenes_b64
            st.session_state["imagenes_b64_backup"] = imagenes_b64

            cols = st.columns(4)
            for i, b64 in enumerate(imagenes_b64):
                with cols[i % 4]:
                    st.image(b64, use_container_width=True)

        elif st.session_state.datos.get("imagenes_b64"):
            st.info("✅ Ya tenés imágenes cargadas. Si subís nuevas reemplazarán las anteriores.")
            cols = st.columns(4)
            for i, b64 in enumerate(st.session_state.datos["imagenes_b64"]):
                with cols[i % 4]:
                    st.image(b64, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Anterior"):
                st.session_state.paso = 6
                st.rerun()

        if st.session_state.datos.get("imagenes_b64"):
            st.success(f"✅ {len(st.session_state.datos['imagenes_b64'])} imagen(es) cargada(s) correctamente")
            if st.button("📄 Guardar imágenes y generar pdf", key="btn_pdf_imagenes"):
                guardar_informe(st.session_state.datos)
                from pdf_generator import generar_pdf
                pdf = generar_pdf(st.session_state.datos)
                nombre = st.session_state.datos.get('paciente', 'paciente').replace(' ', '_')
                st.download_button(
                    label="⬇ Descargar PDF",
                    data=pdf,
                    file_name=f"Informe_{nombre}.pdf",
                    mime="application/pdf",
                    key="pdf_paso7_download"
                )

        st.markdown("---")
        st.markdown("**¿Querés modificar alguna sección?**")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("Datos paciente", key="p7_nav1"):
                st.session_state.paso = 1
                st.rerun()
        with c2:
            if st.button("Mediciones Bid.", key="p7_nav2"):
                st.session_state.paso = 2
                st.rerun()
        with c3:
            if st.button("Doppler medic.", key="p7_nav3"):
                st.session_state.paso = 3
                st.rerun()
        with c4:
            if st.button("Hallazgos", key="p7_nav4"):
                st.session_state.paso = 4
                st.rerun()
        c5, c6, c7, c8 = st.columns(4)
        with c5:
            if st.button("Doppler texto", key="p7_nav5"):
                st.session_state.paso = 5
                st.rerun()
        with c6:
            if st.button("Conclusión", key="p7_nav6"):
                st.session_state.paso = 6
                st.rerun()
        with c7:
            if st.button("🗑 Nuevo informe", key="p7_nav8"):
                st.session_state.paso = 1
                st.session_state.datos = {}
                st.rerun()

# ── PASO 8: Buscador — FUERA del with col_form ──
if st.session_state.paso == 8:
    st.markdown("### 🔍 Buscar informes anteriores")
    busqueda = st.text_input("Escribí el nombre del paciente")
    if busqueda:
        resultados = buscar_informes(busqueda)
        if resultados:
            st.success(f"Se encontraron {len(resultados)} informe(s)")
            for r in resultados:
                with st.expander(f"{r['paciente']} — {r['fecha']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Paciente:** {r['paciente']}")
                        st.write(f"**Edad:** {r['edad']}")
                        st.write(f"**Fecha:** {r['fecha']}")
                        st.write(f"**Obra Social:** {r['obra_social']}")
                    with col2:
                        st.write(f"**Médico:** {r['medico_solicita']}")
                    if st.button("Cargar este informe", key=f"cargar_{r['id']}"):
                        st.session_state.datos = r
                        st.session_state.paso = 1
                        st.rerun()
        else:
            st.warning("No se encontraron informes para ese paciente.")
    if st.button("← Volver"):
        st.session_state.paso = 1
        st.rerun()


# ── VISTA PREVIA ──
with col_prev:
    st.markdown("👁 Vista previa")
    d = st.session_state.datos

    medico_solicita = d.get("medico_solicita", "")
    es_dr_raya = any(x in medico_solicita.lower() for x in ["raya", "rubén", "ruben"])
    nombre_preview = "Dr. Rubén Raya" if es_dr_raya else medico_solicita
    matricula_preview = "MP: 3595" if es_dr_raya else ""
    
    html = f"""
    <link href="https://fonts.googleapis.com/css2?family=Pinyon+Script&display=swap" rel="stylesheet">
    <div style="font-family: Arial, sans-serif; border: 1px solid #ccc;
                padding: 30px; background: white; color: black; font-size: 12px;">

        <div style="text-align:center; margin-bottom:10px;">
            <div style="font-weight:bold; text-decoration:underline; font-size:15px;">CONSULTORIO CARDIOLÓGICO</div>
            <div style="font-family: 'Pinyon Script', cursive; font-size:28px;">{nombre_preview}</div>
            <div style="font-size:11px;">{matricula_preview}</div>
            <div style="font-weight:bold; text-decoration:underline; font-size:13px; margin-top:4px;">INFORME ECOCARDIOGRAFICO</div>
        </div>

        <hr style="border:1px solid black;">

        <table style="width:100%; font-size:12px; margin-top:8px;">
            <tr>
                <td><b>Fecha:</b> {d.get('fecha','')}</td>
                <td><b>Edad:</b> {d.get('edad','')}</td>
            </tr>
            <tr>
                <td><b>Paciente:</b> {d.get('paciente','')}</td>
                <td><b>Obra Social:</b> {d.get('obra_social','')}</td>
            </tr>
            <tr>
                <td colspan="2"><b>Médico que Solicita:</b> {d.get('medico_solicita','')}</td>
            </tr>
        </table>

        <br>
        <div style="font-weight:bold; margin-bottom:6px;">MEDICIONES BIDIMENSIONAL Y MODO M (cm)</div>
        <table style="width:100%; border-collapse:collapse; font-size:11px;">
            <tr style="background:#f0f0f0;">
                <th style="border:1px solid black; padding:4px; text-align:left;">Medición</th>
                <th style="border:1px solid black; padding:4px;">Valor</th>
                <th style="border:1px solid black; padding:4px;">Normal</th>
                <th style="border:1px solid black; padding:4px; text-align:left;">Medición</th>
                <th style="border:1px solid black; padding:4px;">Valor</th>
                <th style="border:1px solid black; padding:4px;">Normal</th>
            </tr>
            <tr>
                <td style="border:1px solid black; padding:4px;">Diámetro fin de diástole VI</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('ddvi','')}</b></td>
                <td style="border:1px solid black; padding:4px; text-align:center;">4,2-5,7</td>
                <td style="border:1px solid black; padding:4px;">Diámetro del VD</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('vd','')}</b></td>
                <td style="border:1px solid black; padding:4px; text-align:center;">2,7-3,3</td>
            </tr>
            <tr>
                <td style="border:1px solid black; padding:4px;">Diámetro fin de sístole VI</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('dsvi','')}</b></td>
                <td style="border:1px solid black; padding:4px; text-align:center;">2,4-3,5</td>
                <td style="border:1px solid black; padding:4px;">Diámetro Raíz Aorta (cm)</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('ao','')}</b></td>
                <td style="border:1px solid black; padding:4px; text-align:center;">2,8-4</td>
            </tr>
            <tr>
                <td style="border:1px solid black; padding:4px;">Fracción Acortamiento (%)</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('fa','')}</b></td>
                <td style="border:1px solid black; padding:4px; text-align:center;">25-43</td>
                <td style="border:1px solid black; padding:4px;">Diámetro de AI</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('ai','')}</b></td>
                <td style="border:1px solid black; padding:4px; text-align:center;">3-4</td>
            </tr>
            <tr>
                <td style="border:1px solid black; padding:4px;">Fracción de Eyección (%)</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('fe','')}</b></td>
                <td style="border:1px solid black; padding:4px; text-align:center;">&gt;55</td>
                <td style="border:1px solid black; padding:4px;">Área AI (cm²)</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('ai_area','')}</b></td>
                <td style="border:1px solid black; padding:4px; text-align:center;">&lt;20</td>
            </tr>
            <tr>
                <td style="border:1px solid black; padding:4px;">Espesor Septal</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('sep','')}</b></td>
                <td style="border:1px solid black; padding:4px; text-align:center;">0,6-1,1</td>
                <td style="border:1px solid black; padding:4px;">Volumen AI (ml/m²)</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('ai_vol','')}</b></td>
                <td style="border:1px solid black; padding:4px; text-align:center;">16-34</td>
            </tr>
            <tr>
                <td style="border:1px solid black; padding:4px;">Espesor Pared Posterior</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('pp','')}</b></td>
                <td style="border:1px solid black; padding:4px; text-align:center;">0,6-1,1</td>
                <td style="border:1px solid black; padding:4px;">Índice Masa VI (g/m²)</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('imvi','')}</b></td>
                <td style="border:1px solid black; padding:4px; text-align:center;">&lt;130 H &lt;110 M</td>
            </tr>
        </table>
        <div style="font-size:10px; margin-top:4px; font-style:italic;">
            Consenso Sociedad Americana de Ecocardiografía (ASE), Sociedad Europea de Cardiología 2010
        </div>

        <br>
        <div style="font-weight:bold; margin-bottom:6px;">MEDICIONES DOPPLER</div>
        <table style="width:100%; border-collapse:collapse; font-size:11px;">
            <tr style="background:#f0f0f0;">
                <th style="border:1px solid black; padding:4px; text-align:left;">Medición</th>
                <th style="border:1px solid black; padding:4px;">Valor</th>
                <th style="border:1px solid black; padding:4px; text-align:left;">Medición</th>
                <th style="border:1px solid black; padding:4px;">Valor</th>
            </tr>
            <tr>
                <td style="border:1px solid black; padding:4px;">Velocidad Pico Ao cm/s – TSVI</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('vel_ao','')}</b></td>
                <td style="border:1px solid black; padding:4px;">Gradiente Aorta (mmHg)</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('grad_ao','')}</b></td>
            </tr>
            <tr>
                <td style="border:1px solid black; padding:4px;">Velocidad Pico Pulmonar cm/s</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('vel_pul','')}</b></td>
                <td style="border:1px solid black; padding:4px;">Gradiente Pulmonar mmHg</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('grad_pul','')}</b></td>
            </tr>
            <tr>
                <td style="border:1px solid black; padding:4px;">Onda E Mitral cm/seg</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('onda_e','')}</b></td>
                <td style="border:1px solid black; padding:4px;">Onda A Mitral cm/seg</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('onda_a','')}</b></td>
            </tr>
            <tr>
                <td style="border:1px solid black; padding:4px;">Presión Sistólica VD y Pul. mmHg</td>
                <td style="border:1px solid black; padding:4px; text-align:center;"><b>{d.get('psap','')}</b></td>
                <td style="border:1px solid black; padding:4px;"></td>
                <td style="border:1px solid black; padding:4px;"></td>
            </tr>
        </table>

        <br>
        <div><b>HALLAZGOS:</b></div>
        <div style="margin-top:6px; white-space:pre-wrap;">{d.get('hallazgos','')}</div>

        <br>
        <div><b>DOPPLER:</b></div>
        <div style="margin-top:6px; white-space:pre-wrap;">{d.get('doppler','')}</div>

        <br>
        <div><b>CONCLUSIÓN:</b></div>
        <div style="margin-top:6px; white-space:pre-wrap;">{d.get('conclusion','')}</div>

        <br>
        <div style="font-weight:bold; text-align:center; text-decoration:underline; margin-bottom:10px;">
            IMÁGENES ECOCARDIOGRÁFICAS
        </div>
        <div style="font-size:11px; text-align:left; margin-bottom:8px;">
            <b>Paciente:</b> {d.get('paciente','')}
        </div>
        
        <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:10px; margin-top:10px;">
            {''.join([f'<img src="{src}" style="width:100%; border:1px solid #ccc;"/>' for src in d.get('imagenes_b64',[])])}
        </div>

    </div>
    """

    components.html(html, height=900, scrolling=True)