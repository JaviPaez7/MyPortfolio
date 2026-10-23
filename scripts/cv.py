"""Generate the portfolio CV. Run from any directory: python scripts/cv.py.

Uses the standard PDF Helvetica family, so Windows fonts are not required.
Text is maintained here; public/javi-paez.jpg is the existing portrait.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import argparse

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
NAVY = colors.HexColor('#0B2A44')
YELLOW = colors.HexColor('#F4BC30')
INK = colors.HexColor('#172C40')
MUTED = colors.HexColor('#526A80')
LIGHT = colors.HexColor('#D7E5EE')
WHITE = colors.white


def generate(output: Path):
    pdfmetrics.registerFont(pdfmetrics.Font('CV', 'Helvetica', 'WinAnsiEncoding'))
    pdfmetrics.registerFont(pdfmetrics.Font('CV-Bold', 'Helvetica-Bold', 'WinAnsiEncoding'))
    pdfmetrics.registerFontFamily('CV', normal='CV', bold='CV-Bold',
                                  italic='CV', boldItalic='CV-Bold')
    output.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output), pagesize=A4, invariant=1)
    c.setTitle('CV Javier Páez Toledo - Desarrollador Full Stack')
    c.setAuthor('Javier Páez Toledo')
    c.setSubject('Currículum profesional 2026')
    c.setCreator('MyPortfolio/scripts/cv.py')
    width, height = A4
    c.setFillColor(NAVY)
    c.rect(0, height - 128, width, 128, fill=1, stroke=0)
    c.setFillColor(YELLOW)
    c.rect(0, height - 128, 5, 128, fill=1, stroke=0)

    def text(value, x, y, size=8, color=INK, bold=False):
        c.setFillColor(color)
        c.setFont('CV-Bold' if bold else 'CV', size)
        c.drawString(x, y, value)

    def para(value, x, y, w, size=9.4, color=INK, bold=False, gap=6):
        style = ParagraphStyle('cv', fontName='CV-Bold' if bold else 'CV',
                               fontSize=size, leading=size * 1.36, textColor=color)
        p = Paragraph(escape(value), style)
        _, h = p.wrap(w, height)
        if y - h < 38:
            raise ValueError('CV content exceeds one page; adjust layout before publishing.')
        p.drawOn(c, x, y - h)
        return y - h - gap

    def section(value, x, y, w, sidebar=False):
        text(value, x, y - 11, 10.5, WHITE if sidebar else NAVY, True)
        c.setStrokeColor(YELLOW)
        c.setLineWidth(1)
        c.line(x, y - 18, x + w, y - 18)
        return y - 29

    text('Javier Páez Toledo', 36, height - 48, 27, WHITE, True)
    text('Desarrollador Full Stack · Web e Inteligencia Artificial',
         36, height - 70, 10.7, LIGHT)
    text('Las Palmas, Canarias · 620 871 380 · javipaeztoledo@gmail.com',
         36, height - 94, 8, LIGHT)
    x = 36
    for label, url in [
        ('portfolio.javistudio.dev', 'https://portfolio.javistudio.dev/'),
        ('github.com/JaviPaez7', 'https://github.com/JaviPaez7'),
        ('linkedin.com/in/javipaez', 'https://linkedin.com/in/javipaez'),
    ]:
        text(label, x, height - 109, 8, YELLOW)
        link_w = pdfmetrics.stringWidth(label, 'CV', 8)
        c.linkURL(url, (x, height - 111, x + link_w, height - 101), relative=0)
        x += link_w + 12
    email_x = 36 + pdfmetrics.stringWidth('Las Palmas, Canarias · 620 871 380 · ', 'CV', 8)
    c.linkURL('mailto:javipaeztoledo@gmail.com', (email_x, height - 96,
              email_x + pdfmetrics.stringWidth('javipaeztoledo@gmail.com', 'CV', 8), height - 86))

    # Clip the existing portrait into a circle without altering the source photo.
    px, py, radius = width - 73, height - 64, 35
    c.saveState()
    clip = c.beginPath()
    clip.circle(px, py, radius)
    c.clipPath(clip, stroke=0, fill=0)
    portrait = ImageReader(str(ROOT / 'public' / 'javi-paez.jpg'))
    image_w, image_h = portrait.getSize()
    scale = radius * 2 / min(image_w, image_h)
    draw_w, draw_h = image_w * scale, image_h * scale
    c.drawImage(portrait, px - draw_w / 2, py - draw_h / 2,
                width=draw_w, height=draw_h, mask='auto')
    c.restoreState()
    c.setStrokeColor(YELLOW)
    c.setLineWidth(2.2)
    c.circle(px, py, radius, stroke=1, fill=0)

    left, main_w = 36, 311
    right, side_w = 385, width - 36 - 385 - 16
    y = height - 160
    c.setFillColor(NAVY)
    c.roundRect(369, 36, width - 36 - 369, y + 16 - 36, 8, fill=1, stroke=0)

    main_y = section('PERFIL', left, y, main_w)
    main_y = para('Desarrollador Full Stack con experiencia práctica en productos web e inteligencia artificial. Actualmente desarrollo Hub Bot y Hub Studio en iabot (Iluzona Innova SL) y he puesto en producción un ERP/CRM a medida. Combino frontend, backend, APIs, bases de datos y despliegue para convertir necesidades de producto en soluciones útiles y mantenibles.', left, main_y, main_w)
    main_y = section('EXPERIENCIA', left, main_y - 8, main_w)
    main_y = para('ABRIL 2026 - ACTUALIDAD', left, main_y, main_w, 8, colors.HexColor('#00619A'), gap=3)
    main_y = para('Desarrollador Full Stack · Prácticas', left, main_y, main_w, 10, NAVY, True, 2)
    main_y = para('Iluzona Innova SL · iabot', left, main_y, main_w, 8.8, MUTED)
    for bullet in [
        'Participación en el desarrollo de Hub IAbot, plataforma central del ecosistema, y Hub Bot, un Director General IA que coordina empleados especializados.',
        'Desarrollo de Hub Studio, plataforma de vibe coding para crear aplicaciones web completas mediante lenguaje natural.',
        'Desarrollo y despliegue de Iluzona Control, ERP/CRM con integración de Holded para presupuestos, catálogo y auditoría.',
        'Implementación Full Stack con React, Next.js, Node.js y bases de datos; flujos con LLM, automatización y despliegues en producción.',
    ]:
        text('•', left + 2, main_y - 9, 9, YELLOW)
        main_y = para(bullet, left + 11, main_y, main_w - 11, gap=4)
    main_y -= 5
    main_y = para('ENERO 2023 - ACTUALIDAD', left, main_y, main_w, 8, colors.HexColor('#00619A'), gap=3)
    main_y = para('Desarrollador web freelance', left, main_y, main_w, 10, NAVY, True, 2)
    main_y = para('Proyectos independientes', left, main_y, main_w, 8.8, MUTED, gap=4)
    main_y = para('Aplicaciones con React, Astro, PostgreSQL y APIs; diseño, desarrollo, puesta en producción y mantenimiento.', left, main_y, main_w, color=MUTED, gap=10)
    main_y = para('2020 - 2024', left, main_y, main_w, 8, colors.HexColor('#00619A'), gap=3)
    main_y = para('Manipulador de vidrio plano', left, main_y, main_w, 10, NAVY, True, 2)
    main_y = para('Cristalgana Lanzarote SL', left, main_y, main_w, 8.8, MUTED, gap=4)
    main_y = para('Resolución de incidencias, precisión técnica, cumplimiento de plazos y trabajo coordinado en un entorno industrial.', left, main_y, main_w, color=MUTED)
    main_y = section('PROYECTOS DESTACADOS', left, main_y - 8, main_w)
    c.linkURL('https://tanke.javistudio.dev/', (left, main_y - 14, left + main_w, main_y))
    main_y = para('Tanke · Buscador de gasolineras', left, main_y, main_w, 10, NAVY, True, 3)
    main_y = para('Aplicación Full Stack con React, Express, Prisma y PostgreSQL para comparar precios, guardar favoritos y configurar alertas. Desplegada con Docker en VPS.', left, main_y, main_w, color=MUTED, gap=10)
    c.linkURL('https://dumelis.javistudio.dev/', (left, main_y - 14, left + main_w, main_y))
    main_y = para('Dumelis · Calendarios compartidos en tiempo real', left, main_y, main_w, 10, NAVY, True, 3)
    para('PWA para coordinar turnos y encontrar días libres en común. Cuentas, invitaciones y sincronización en tiempo real con Next.js, WebSocket y SQLite. Desplegada con Docker en VPS.', left, main_y, main_w, color=MUTED)

    side_y = section('FORMACIÓN', right, y, side_w, True)
    for date, title, school in [
        ('DIC. 2025 - OCT. 2026', 'Máster DWA · Desarrollo Web Avanzado Full Stack', 'Nett Digital School · Finalizado · TFM: Tanke'),
        ('ENERO - JUNIO 2024', 'Bootcamp Full Stack Web Development · 300 h', 'Reboot Academy · Con honores'),
        ('2015 - 2017', 'Técnico Superior en Actividad Física y Animación Deportiva', 'I.E.S. Nueva Isleta Tony Gallardo'),
    ]:
        side_y = para(date, right, side_y, side_w, 8, YELLOW, gap=4)
        side_y = para(title, right, side_y, side_w, 9, WHITE, True, 4)
        side_y = para(school, right, side_y, side_w, 9, LIGHT, gap=20)
    side_y = section('TECNOLOGÍAS', right, side_y - 6, side_w, True)
    for label, value in [
        ('Frontend', 'TypeScript · JavaScript · React · Next.js · Astro · Tailwind CSS'),
        ('Backend', 'Node.js · Express · APIs REST'),
        ('Datos', 'PostgreSQL · Prisma · PocketBase'),
        ('Infraestructura', 'Docker · Git · VPS · CI/CD'),
        ('IA', 'Integración de LLMs · agentes · automatización'),
    ]:
        side_y = para(label, right, side_y, side_w, 8.5, YELLOW, gap=3)
        side_y = para(value, right, side_y, side_w, 9, LIGHT, gap=16)
    side_y = section('IDIOMAS', right, side_y - 6, side_w, True)
    side_y = para('Castellano · Nativo', right, side_y, side_w, 9, WHITE, True)
    para('Inglés · B2', right, side_y, side_w, 9, LIGHT)
    c.showPage()
    c.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'public' / 'CV_Javi_Paez.pdf')
    args = parser.parse_args()
    generate(args.output)
    print(args.output.resolve())
