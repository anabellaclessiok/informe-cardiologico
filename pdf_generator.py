from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image as RLImage, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from io import BytesIO
from PIL import Image as PILImage
import base64

# ── Colores ──
NEGRO = colors.black
GRIS  = colors.HexColor('#f0f0f0')
BLANCO = colors.white

# 2. CONFIGURACIÓN DE RUTAS Y REGISTRO DE FUENTE (Antes del def)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_FUENTE = os.path.join(BASE_DIR, "ITCEDSCR.TTF")

# Registramos la fuente globalmente
try:
    if os.path.exists(PATH_FUENTE):
        pdfmetrics.registerFont(TTFont('Edwardian-Script-Real', PATH_FUENTE))
        FUENTE_DOCTOR = 'Edwardian-Script-Real'
    else:
        FUENTE_DOCTOR = 'Helvetica-Oblique'
except:
    FUENTE_DOCTOR = 'Helvetica-Oblique'
def generar_pdf(d):
    buffer = BytesIO()
    PAGE_W, PAGE_H = A4
    MARGIN = 20*mm

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=15*mm, bottomMargin=15*mm,
        title=f"Informe Ecocardiográfico - {d.get('paciente', '')}",
        author="Consultorio Cardiológico Dr. Rubén Raya",
    )

    story = []
    CONTENT_W = PAGE_W - 2 * MARGIN

    # 1. Registro de la fuente (Hazlo justo antes de definir los estilos)
    base_dir = os.path.dirname(os.path.abspath(__file__))
# Usamos el nombre exacto del archivo que vimos en tu captura
    font_path = os.path.join(base_dir, "ITCEDSCR.TTF") 

    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('Edwardian-Script', font_path))
        fuente_doctor = 'Edwardian-Script'
    else:
        fuente_doctor = 'Helvetica-Oblique' # Plan B si el archivo no está

# 2. Definición de estilos corregida
    titulo = ParagraphStyle("titulo", fontName="Helvetica-Bold",
    fontSize=13, alignment=TA_CENTER, underlineProportion=0.05,
    underlineWidth=1, underlineOffset=-2)

# Aquí cambiamos la fuente por la de la carpeta y subimos el tamaño a 32
    cursiva = ParagraphStyle("cursiva", fontName=fuente_doctor,
    fontSize=32, alignment=TA_CENTER, leading=35)

    normal_c = ParagraphStyle("normal_c", fontName="Helvetica",
    fontSize=10, alignment=TA_CENTER)

    subtitulo = ParagraphStyle("subtitulo", fontName="Helvetica-Bold",
    fontSize=11, alignment=TA_CENTER, underlineProportion=0.05,
    underlineWidth=1, underlineOffset=-2)

    negrita = ParagraphStyle("negrita", fontName="Helvetica-Bold", fontSize=10)
    normal  = ParagraphStyle("normal",  fontName="Helvetica", fontSize=10, leftIndent=10)

    small   = ParagraphStyle("small",   fontName="Helvetica", fontSize=8,
    alignment=TA_CENTER, textColor=colors.HexColor('#555555'))

    body    = ParagraphStyle("body",    fontName="Helvetica", fontSize=10,
    leading=16)

    # ── ENCABEZADO ──
    medico_solicita = d.get("medico_solicita", "")
    es_dr_raya = any(x in medico_solicita.lower() for x in ["raya", "rubén", "ruben"])

    try:
        import streamlit as st
        matricula     = st.secrets["MATRICULA"] if es_dr_raya else ""
        nombre_medico = f"Dr. {st.secrets['MEDICO_NOMBRE']}" if es_dr_raya else medico_solicita
    except:
        matricula     = "MP: 3595" if es_dr_raya else ""
        nombre_medico = "Dr. Rubén Raya" if es_dr_raya else medico_solicita

    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("<u>CONSULTORIO CARDIOLÓGICO</u>", titulo))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(nombre_medico, cursiva))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(matricula, normal_c))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("<u>INFORME ECOCARDIOGRAFICO</u>", subtitulo))
    story.append(Spacer(1, 4*mm))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=NEGRO))
    story.append(Spacer(1, 6*mm))

    # ── DATOS DEL PACIENTE ──
    story.append(Spacer(1, 3*mm))
    CW1 = CONTENT_W * 0.55
    CW2 = CONTENT_W * 0.45
    pac_data = [
        [Paragraph(f"<b>Paciente:</b> {d.get('paciente','')}", normal),
         Paragraph(f"<b>Edad:</b> {d.get('edad','')}", normal)],
        [Paragraph(f"<b>Fecha:</b> {d.get('fecha','')}", normal),
         Paragraph(f"<b>Obra Social:</b> {d.get('obra_social','')}", normal)],
        [Paragraph(f"<b>Médico que Solicita:</b> {d.get('medico_solicita','')}", normal),
         Paragraph("", normal)],
    ]
    pac_table = Table(pac_data, colWidths=[CW1, CW2])
    pac_table.setStyle(TableStyle([
        ('TOPPADDING',    (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,-1), (-1,-1), 0, colors.white),
    ]))
    story.append(pac_table)
    story.append(Spacer(1, 6*mm))

    # ── MEDICIONES BIDIMENSIONAL ──
    story.append(Paragraph("<b>MEDICIONES BIDIMENSIONAL Y MODO M (cm)</b>", negrita))
    story.append(Spacer(1, 2*mm))

    CW6 = CONTENT_W / 6
    header_style = ParagraphStyle("hs", fontName="Helvetica-Bold", fontSize=8, alignment=TA_CENTER)
    cell_style   = ParagraphStyle("cs", fontName="Helvetica", fontSize=8)
    val_style    = ParagraphStyle("vs", fontName="Helvetica-Bold", fontSize=8, alignment=TA_CENTER)
    norm_style   = ParagraphStyle("ns", fontName="Helvetica", fontSize=8, alignment=TA_CENTER)

    med_data = [
        [Paragraph("Medición", header_style), Paragraph("Valor", header_style),
         Paragraph("Normal", header_style), Paragraph("Medición", header_style),
         Paragraph("Valor", header_style), Paragraph("Normal", header_style)],
        [Paragraph("Diámetro fin de diástole VI", cell_style), Paragraph(d.get('ddvi',''), val_style), Paragraph("4,2-5,7", norm_style),
         Paragraph("Diámetro del VD", cell_style), Paragraph(d.get('vd',''), val_style), Paragraph("2,7-3,3", norm_style)],
        [Paragraph("Diámetro fin de sístole VI", cell_style), Paragraph(d.get('dsvi',''), val_style), Paragraph("2,4-3,5", norm_style),
         Paragraph("Diámetro Raíz Aorta (cm)", cell_style), Paragraph(d.get('ao',''), val_style), Paragraph("2,8-4", norm_style)],
        [Paragraph("Fracción Acortamiento (%)", cell_style), Paragraph(d.get('fa',''), val_style), Paragraph("25-43", norm_style),
         Paragraph("Diámetro de AI", cell_style), Paragraph(d.get('ai',''), val_style), Paragraph("3-4", norm_style)],
        [Paragraph("Fracción de Eyección (%)", cell_style), Paragraph(d.get('fe',''), val_style), Paragraph(">55", norm_style),
         Paragraph("Área AI (cm²)", cell_style), Paragraph(d.get('ai_area',''), val_style), Paragraph("<20", norm_style)],
        [Paragraph("Espesor Septal", cell_style), Paragraph(d.get('sep',''), val_style), Paragraph("0,6-1,1", norm_style),
         Paragraph("Volumen AI (ml/m²)", cell_style), Paragraph(d.get('ai_vol',''), val_style), Paragraph("16-34", norm_style)],
        [Paragraph("Espesor Pared Posterior", cell_style), Paragraph(d.get('pp',''), val_style), Paragraph("0,6-1,1", norm_style),
         Paragraph("Índice Masa VI (g/m²)", cell_style), Paragraph(d.get('imvi',''), val_style), Paragraph("<130 H<br/><110 M", norm_style)],
    ]

    med_table = Table(med_data, colWidths=[CONTENT_W*0.30, CONTENT_W*0.09, CONTENT_W*0.13, CONTENT_W*0.25, CONTENT_W*0.09, CONTENT_W*0.13])
    med_table.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), GRIS),
        ('BOX',           (0,0), (-1,-1), 0.5, NEGRO),
        ('INNERGRID',     (0,0), (-1,-1), 0.5, NEGRO),
        ('TOPPADDING',    (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING',   (0,0), (-1,-1), 4),
        ('RIGHTPADDING',  (0,0), (-1,-1), 4),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(med_table)
    story.append(Paragraph("Consenso Sociedad Americana de Ecocardiografía (ASE), Sociedad Europea de Cardiología 2010", small))
    story.append(Spacer(1, 4*mm))

    # ── MEDICIONES DOPPLER ──
    story.append(Paragraph("<b>MEDICIONES DOPPLER</b>", negrita))
    story.append(Spacer(1, 2*mm))

    CW4 = CONTENT_W / 4
    dop_data = [
        [Paragraph("Medición", header_style), Paragraph("Valor", header_style),
         Paragraph("Medición", header_style), Paragraph("Valor", header_style)],
        [Paragraph("Velocidad Pico Ao cm/s – TSVI", cell_style), Paragraph(d.get('vel_ao',''), val_style),
         Paragraph("Gradiente Aorta (mmHg)", cell_style), Paragraph(d.get('grad_ao',''), val_style)],
        [Paragraph("Velocidad Pico Pulmonar cm/s", cell_style), Paragraph(d.get('vel_pul',''), val_style),
         Paragraph("Gradiente Pulmonar mmHg", cell_style), Paragraph(d.get('grad_pul',''), val_style)],
        [Paragraph("Onda E Mitral cm/seg", cell_style), Paragraph(d.get('onda_e',''), val_style),
         Paragraph("Onda A Mitral cm/seg", cell_style), Paragraph(d.get('onda_a',''), val_style)],
        [Paragraph("Presión Sistólica VD y Pul. mmHg", cell_style), Paragraph(d.get('psap',''), val_style),
         Paragraph("", cell_style), Paragraph("", val_style)],
    ]

    dop_table = Table(dop_data, colWidths=[CW4*1.5, CW4*0.5, CW4*1.5, CW4*0.5])
    dop_table.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), GRIS),
        ('BOX',           (0,0), (-1,-1), 0.5, NEGRO),
        ('INNERGRID',     (0,0), (-1,-1), 0.5, NEGRO),
        ('TOPPADDING',    (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING',   (0,0), (-1,-1), 4),
        ('RIGHTPADDING',  (0,0), (-1,-1), 4),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(dop_table)
    story.append(Spacer(1, 4*mm))

    # ── HALLAZGOS ──
    story.append(Paragraph("<b>HALLAZGOS:</b>", negrita))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(d.get('hallazgos','').replace('\n', '<br/>'), body))
    story.append(Spacer(1, 4*mm))

    # ── DOPPLER ──
    story.append(Paragraph("<b>DOPPLER:</b>", negrita))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(d.get('doppler','').replace('\n', '<br/>'), body))
    story.append(Spacer(1, 4*mm))

    # ── CONCLUSIÓN ──
    story.append(Paragraph("<b>CONCLUSIÓN:</b>", negrita))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(d.get('conclusion','').replace('\n', '<br/>'), body))
    

    # -- SECCIÓN DE IMÁGENES --
    imagenes_b64 = d.get('imagenes_b64', [])
    if imagenes_b64:
        story.append(Spacer(1, 6*mm))
        story.append(Paragraph("<u>IMÁGENES ECOCARDIOGRÁFICAS</u>", 
                     ParagraphStyle("img_titulo", fontName="Helvetica-Bold", fontSize=12, alignment=TA_CENTER)))
        story.append(Spacer(1, 3*mm))
        story.append(Paragraph(f"Paciente: {d.get('paciente','')}", 
                     ParagraphStyle("img_pac", fontName="Helvetica", fontSize=10, alignment=TA_LEFT)))
        story.append(Spacer(1, 4*mm))

        IMG_W = 90*mm
        IMG_H = 65*mm
        COL_W = 95*mm

        row = []
        for i, b64 in enumerate(imagenes_b64):
            try:
                data = b64.split(',', 1)[1] if ',' in b64 else b64
                img_bytes = base64.b64decode(data)
                img_pil = PILImage.open(BytesIO(img_bytes))
                img_pil.thumbnail((int(IMG_W * 3.78), int(IMG_H * 3.78)), 1)
                
                buf = BytesIO()
                img_pil.save(buf, format='JPEG', quality=95)
                buf.seek(0)
                
                row.append(RLImage(buf, width=IMG_W, height=IMG_H))

                # Si llenamos una fila de 2, la creamos y la añadimos de inmediato
                if len(row) == 2:
                    t_fila = Table([row], colWidths=[COL_W, COL_W])
                    t_fila.setStyle(TableStyle([
                        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ('LEFTPADDING', (0,0), (-1,-1), 5),
                        ('RIGHTPADDING', (0,0), (-1,-1), 5),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 15),
                    ]))
                    story.append(t_fila) # Se añade AQUÍ adentro
                    row = []
            except Exception as e:
                print(f"Error imagen: {e}")

        # Manejo de la última imagen si el total es impar
        if row:
            while len(row) < 2:
                row.append("") # Celda vacía
            t_final = Table([row], colWidths=[COL_W, COL_W])
            t_final.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('LEFTPADDING', (0,0), (-1,-1), 5),
                ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(t_final) # Se añade AQUÍ adentro


    def agregar_firma(canvas, doc):
        if es_dr_raya:
            canvas.saveState()
            firma_path = 'firma.png'
            if os.path.exists(firma_path):
                canvas.drawImage(
                    firma_path,
                    x=doc.pagesize[0] - 20*mm - 55*mm,
                    y=10*mm,
                    width=55*mm,
                    height=28*mm,
                    preserveAspectRatio=True,
                    mask='auto'
                )
            canvas.restoreState()

    doc.build(story, onFirstPage=agregar_firma, onLaterPages=agregar_firma)
    buffer.seek(0)
    return buffer.read()