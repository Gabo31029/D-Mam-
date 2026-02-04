
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as ReportLabImage, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os
import requests

# --- 🎨 CONFIGURACIÓN DE ESTILO DEL PDF ---
class PDFStyleConfig:
    # Colores (Hex codes)
    COLOR_TITLE = '#292524'      # Stone 800
    COLOR_SUBTITLE = '#57534e'   # Stone 600
    COLOR_META = '#78716c'       # Stone 500
    COLOR_TEXT = '#000000'       # Black
    
    FONT_TITLE = 'Helvetica-Bold'
    FONT_BODY = 'Helvetica'
    
    SIZE_TITLE_MAIN = 24
    SIZE_TITLE_COVER = 36
    SIZE_HEADING = 16
    SIZE_BODY = 11
    SIZE_META = 10
    
    SPACE_AFTER_TITLE = 30

def get_custom_styles():
    """Genera los estilos basados en la configuración."""
    base_styles = getSampleStyleSheet()
    
    return {
        'Title': ParagraphStyle(
            'CustomTitle',
            parent=base_styles['Heading1'],
            fontSize=PDFStyleConfig.SIZE_TITLE_MAIN,
            spaceAfter=PDFStyleConfig.SPACE_AFTER_TITLE,
            alignment=TA_CENTER,
            fontName=PDFStyleConfig.FONT_TITLE,
            textColor=colors.HexColor(PDFStyleConfig.COLOR_TITLE)
        ),
        'CoverTitle': ParagraphStyle(
            'CoverTitle',
            parent=base_styles['Heading1'],
            fontSize=PDFStyleConfig.SIZE_TITLE_COVER,
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName=PDFStyleConfig.FONT_TITLE,
            textColor=colors.HexColor(PDFStyleConfig.COLOR_TITLE)
        ),
        'Heading2': ParagraphStyle(
            'Heading2Custom',
            parent=base_styles['Heading2'],
            fontSize=PDFStyleConfig.SIZE_HEADING,
            spaceBefore=20,
            spaceAfter=10,
            fontName=PDFStyleConfig.FONT_TITLE,
            textColor=colors.HexColor(PDFStyleConfig.COLOR_SUBTITLE)
        ),
        'Normal': ParagraphStyle(
            'NormalCustom',
            parent=base_styles['Normal'],
            fontSize=PDFStyleConfig.SIZE_BODY,
            leading=16,
            fontName=PDFStyleConfig.FONT_BODY,
            textColor=colors.HexColor(PDFStyleConfig.COLOR_TEXT)
        ),
        'Meta': ParagraphStyle(
            'Meta',
            parent=base_styles['Normal'],
            fontSize=PDFStyleConfig.SIZE_META,
            textColor=colors.HexColor(PDFStyleConfig.COLOR_META),
            alignment=TA_CENTER,
            spaceAfter=20
        ),
        'Description': ParagraphStyle(
            'Desc',
            parent=base_styles['Normal'],
            fontSize=14,
            leading=20,
            alignment=TA_CENTER,
            fontName=PDFStyleConfig.FONT_BODY, 
            spaceAfter=30
        )
    }

def get_image_from_url(url):
    """Descarga imagen de URL y retorna archivo en memoria compatible (BytesIO)."""
    if not url:
        return None
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BytesIO(response.content)
    except Exception as e:
        print(f"Error downloading image {url}: {e}")
        return None

def build_recipe_stories(recipe, author_name, styles):
    """Construye el contenido de una sola receta."""
    story = []

    # Título
    story.append(Paragraph(recipe.title, styles['Title']))
    
    # Metadatos
    meta_text = f"{recipe.country or 'Internacional'} | {recipe.difficulty.capitalize()} | {recipe.preparation_time_minutes} min"
    if author_name:
        meta_text += f" | Por {author_name}"
        
    story.append(Paragraph(meta_text.upper(), styles['Meta']))
    story.append(Spacer(1, 12))

    # Imagen
    if recipe.image_url:
        img_data = get_image_from_url(recipe.image_url)
        
        if img_data:
            try:
                img_data.seek(0)
                utils_img = ImageReader(img_data)
                orig_w, orig_h = utils_img.getSize()
                aspect = orig_h / float(orig_w)
                
                target_w = 4.5 * inch
                target_h = target_w * aspect
                
                if target_h > 5 * inch:
                    target_h = 5 * inch
                    target_w = target_h / aspect

                img_data.seek(0)
                rl_img = ReportLabImage(img_data, width=target_w, height=target_h)
                rl_img.hAlign = 'CENTER'
                story.append(rl_img)
                story.append(Spacer(1, 20))
            except Exception as e:
                print(f"Error processing image for PDF: {e}")

    # Notas
    if recipe.notes:
        story.append(Paragraph("Notas", styles['Heading2']))
        story.append(Paragraph(recipe.notes, styles['Normal']))
        story.append(Spacer(1, 12))

    # Ingredientes
    story.append(Paragraph("Ingredientes", styles['Heading2']))
    
    data = []
    if isinstance(recipe.ingredients, list):
        for ing in recipe.ingredients:
            name = ing.get('name', '')
            amount = ing.get('amount', '')
            unit = ing.get('unit', '')
            
            text = f"• {name}"
            if amount or unit:
                text += f" <font color='#78716c'>({amount} {unit})</font>".strip()
            data.append([Paragraph(text, styles['Normal'])])
            
    elif isinstance(recipe.ingredients, str):
         for ing in recipe.ingredients.split('\n'):
            if ing.strip():
                data.append([Paragraph(f"• {ing.strip()}", styles['Normal'])])
            
    if data:
        t = Table(data, colWidths=[450])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t)

    story.append(Spacer(1, 12))

    # Instrucciones
    story.append(Paragraph("Preparación", styles['Heading2']))
    
    instructions_list = recipe.instructions.split('\n')
    
    if recipe.instructions_format == "numbered":
        for idx, step in enumerate(instructions_list):
            if step.strip():
                step_text = f"<b>{idx + 1}.</b> {step.strip()}"
                story.append(Paragraph(step_text, styles['Normal']))
                story.append(Spacer(1, 8))
    else:
        for step in instructions_list:
            if step.strip():
                story.append(Paragraph(step.strip(), styles['Normal']))
                story.append(Spacer(1, 8))
            
    return story

def generate_recipe_pdf(recipe, author_name):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72, title=recipe.title)
    styles = get_custom_styles()
    story = build_recipe_stories(recipe, author_name, styles)
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()  # Return bytes directly

def generate_cookbook_pdf(cookbook, author_name):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72, title=cookbook.title)
    styles = get_custom_styles()
    story = []
    
    # --- Portada ---
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph(cookbook.title, styles['CoverTitle']))
    story.append(Paragraph(f"Recetario hecho por {author_name}", styles['Meta']))
    story.append(Spacer(1, 0.5*inch))
    
    if cookbook.description:
        story.append(Paragraph(cookbook.description, styles['Description']))
        
    story.append(PageBreak())
    
    # --- Índice ---
    story.append(Paragraph("Índice", styles['Title']))
    story.append(Spacer(1, 20))
    
    if not cookbook.recipes:
        story.append(Paragraph("Sin recetas aún.", styles['Normal']))
    else:
        for i, recipe in enumerate(cookbook.recipes):
            story.append(Paragraph(f"{i+1}. {recipe.title}", styles['Normal']))
            story.append(Spacer(1, 6))
            
    story.append(PageBreak())
    
    # --- Recetas ---
    for i, recipe in enumerate(cookbook.recipes):
        recipe_content = build_recipe_stories(recipe, None, styles)
        story.extend(recipe_content)
        if i < len(cookbook.recipes) - 1:
            story.append(PageBreak())
            
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue() # Return bytes directly
