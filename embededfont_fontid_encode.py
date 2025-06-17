from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from fontTools.ttLib import TTFont as ttlibFont

def create_custom_glyph_pdf(output_path, font_path):
    pdfmetrics.registerFont(TTFont('RF2', font_path))
    
    ttfont = ttlibFont(font_path)
    
    glyph_name_to_id = {}
    for i, name in enumerate(ttfont.getGlyphOrder()):
        glyph_name_to_id[name] = i
    
    cmap = ttfont.getBestCmap()
    char_to_glyph_id = {}
    for char_code, glyph_name in cmap.items():
        if '.' in glyph_name:
            base_name = glyph_name.split('.')[0]
            char_to_glyph_id[char_code] = glyph_name_to_id.get(base_name, 0)
        else:
            char_to_glyph_id[char_code] = glyph_name_to_id.get(glyph_name, 0)
    
    c = canvas.Canvas(output_path, pageCompression=0)
    
    #c.setFont("Helvetica", 10)
    #c.drawString(72, 680, "原始文本:")
    #c.setFont("RF2", 12)
    #c.drawString(72, 660, "hello world%%%%%%%%%%%%%%%%%%")
    
    text_glyph_ids = []
    for char in "hello world":
        char_code = ord(char)
        glyph_id = char_to_glyph_id.get(char_code, 0)
        text_glyph_ids.append(f"{glyph_id:04X}")
    
    percent_glyph_id = char_to_glyph_id.get(ord('%'), 0)
    percent_glyphs = []
    
    if percent_glyph_id > 0:
        glyph_name = ttfont.getGlyphOrder()[percent_glyph_id]
        glyph = ttfont['glyf'][glyph_name]
        
        if hasattr(glyph, 'components'):
            components = glyph.components
            for comp in components:
                comp_glyph_id = glyph_name_to_id.get(comp.glyphName, 0)
                percent_glyphs.append(f"{comp_glyph_id:04X}")
        else:
            percent_glyphs = [f"{percent_glyph_id:04X}"]
    else:
        percent_glyphs = ["0000"]
    
    percent_sequence = []
    for _ in range(26):
        percent_sequence.extend(percent_glyphs)
    
    content = [
        "BT",                          # Begin text object
        "1 0 0 1 72 640 Tm",           # Set text position matrix
        "/RF2 12 Tf",                  # Set font: RF2, 12pt
        "<",                           # Start hex string for glyph IDs
        
        *text_glyph_ids,
        
        # *percent_sequence,
        
        "> Tj",                        # Show text (glyph IDs)
        "T*",                          # Move to next line (down)
        "ET"                           # End text object
    ]
    
    c._code.append("\n".join(content))
    
    c.save()
    print(f"PDF: {output_path}")

if __name__ == "__main__":
    font_path = "rf2.ttf"
    output_path = "embededfont_fontid_encode.pdf"
    
    create_custom_glyph_pdf(output_path, font_path)

    exit()

    from fontTools.ttLib import TTFont
    ttfont = TTFont(font_path)
    print(f"\n字体 {font_path} 调试信息:")
    print(f"总字形数: {len(ttfont.getGlyphOrder())}")
    
    for char in "hello world":
        char_code = ord(char)
        cmap = ttfont.getBestCmap()
        glyph_name = cmap.get(char_code)
        
        if glyph_name:
            try:
                glyph_id = ttfont.getGlyphOrder().index(glyph_name)
                print(f"字符 '{char}' (U+{char_code:04X}) → 字形名称 '{glyph_name}' → 字形ID {glyph_id}")
            except ValueError:
                print(f"字符 '{char}' (U+{char_code:04X}) 的字形名称 '{glyph_name}' 不在字形列表中")
        else:
            print(f"字符 '{char}' (U+{char_code:04X}) 未在CMAP中找到")
    
    percent_char = '%'
    percent_code = ord(percent_char)
    if percent_code in cmap:
        percent_glyph_name = cmap[percent_code]
        percent_glyph = ttfont['glyf'][percent_glyph_name]
        if hasattr(percent_glyph, 'components'):
            print(f"\n百分号字形是复合字形，包含组件:")
            for comp in percent_glyph.components:
                print(f"  - 组件: {comp.glyphName}")
