from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def embed_full_font():
    font_name = "RF2Full"
    ttf_font = TTFont(font_name, "rf2.ttf")
    pdfmetrics.registerFont(ttf_font)
    
    c = canvas.Canvas("embededfont.pdf", pageCompression=0)
    c.setFont(font_name, 12)

    c.drawString(72, 720, "hello world%%%%%%%%%%%%%%%%%%")
    
    c.setFillColorRGB(1, 1, 1)
    
    for y_pos in range(720, 620, -20):
        c.drawString(-1000, y_pos, ''.join(chr(i) for i in range(32, 127)))
        
        c.drawString(-1000, y_pos-10, ''.join(chr(i) for i in range(160, 256)))
        
        c.drawString(-1000, y_pos-20, ''.join(chr(i) for i in range(0x2000, 0x2070)))
    
    c.save()

embed_full_font()
