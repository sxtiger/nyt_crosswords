import json
import os
from tkinter import Tk, filedialog
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Frame, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

# 自定义页面尺寸（单位为 pt）
page_width = 162 / 25.4 * 72  
page_height = 216 / 25.4 * 72 
pagesize = (page_width, page_height)


def draw_grid(c, grid, gridnums, size, fill_answers=False, font_size=10):
    cell_size = 25
    margin = 50
    width, height = size['cols'], size['rows']
    top = pagesize[1] - margin
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1.2)

    for y in range(height):
        for x in range(width):
            idx = y * width + x
            ch = grid[idx]
            num = gridnums[idx]
            left = margin + x * cell_size
            bottom = top - (y + 1) * cell_size
            c.rect(left, bottom, cell_size, cell_size, fill=0)

            if ch == ".":
                c.setFillGray(0.8)
                c.rect(left, bottom, cell_size, cell_size, fill=1)
                c.setFillGray(0)

            if num > 0:
                c.setFont("Helvetica", 6)
                c.drawString(left + 2, bottom + cell_size - 8, str(num))

            if fill_answers and ch != ".":
                c.setFont("Helvetica-Bold", font_size)
                c.drawCentredString(left + cell_size / 2, bottom + 7, ch.upper())

def render_clues_page(c, clues):
    c.showPage()
    style = ParagraphStyle('clueStyle', fontName='Helvetica', fontSize=9, leading=11, spaceAfter=3)
    # 页边距（你可以根据需要调整）
    margin_x = 30
    margin_y = 50

    # 两栏之间的间距
    gutter = 20

    # 可用宽度和高度
    usable_width = page_width - 2 * margin_x
    usable_height = page_height - 2 * margin_y

    # 每栏宽度
    frame_width = (usable_width - gutter) / 2

    # Frame 定位
    col1 = Frame(
        margin_x,
        margin_y,
        frame_width,
        usable_height,
        showBoundary=0
    )
    col2 = Frame(
        margin_x + frame_width + gutter,
        margin_y,
        frame_width,
        usable_height,
        showBoundary=0
    )

    def make_clue_paragraphs(title, clue_list):
        paras = [Paragraph(f"<b>{title}</b>", style), Spacer(1, 6)]
        for clue in clue_list:
            clue = clue.replace("“", '"').replace("”", '"')
            paras.append(Paragraph(clue, style))
        return paras

    left_clues = make_clue_paragraphs("Across", clues.get("across", []))
    right_clues = make_clue_paragraphs("Down", clues.get("down", []))

    col1.addFromList(left_clues, c)
    col2.addFromList(right_clues, c)

def generate_puzzle_pdf(json_path, data):
    # 读取json中相应内容参数
    grid = data['grid']
    gridnums = data['gridnums']
    clues = data["clues"]
    #clues_across = data['clues']['across']
    #clues_down = data['clues']['down']
    size = data['size']

    base = os.path.splitext(json_path)[0]
    output_pdf = base + "_crossword.pdf"
    c = canvas.Canvas(output_pdf, pagesize=pagesize)

    # 📄 Page 1: Puzzle Grid
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(pagesize[0] / 2, pagesize[1] - 30, "NYT Crossword Puzzle (" + os.path.splitext(os.path.basename(json_path))[0] + ")")
    draw_grid(c, grid, gridnums, size)
    #c.showPage()

    # 📝 Page 2: Clues
    render_clues_page(c, clues)

    c.save()
    print("✅ Puzzle PDF 生成成功：", output_pdf)

def generate_solution_pdf(json_path, data):
    grid = data['grid']
    gridnums = data['gridnums']
    size = data['size']

    base = os.path.splitext(json_path)[0]
    output_pdf = base + "_crossword_answers.pdf"
    c = canvas.Canvas(output_pdf, pagesize=pagesize)

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(pagesize[0] / 2, pagesize[1] - 30, "NYT Crossword Answer Key")

    draw_grid(c, grid, gridnums, size, fill_answers=True, font_size=14)
    c.save()
    print("✅ 答案 PDF 生成成功：", output_pdf)

def main():
    Tk().withdraw()
    json_path = filedialog.askopenfilename(title="选择NYT Crossword JSON文件", filetypes=[("JSON 文件", "*.json")])
    if not json_path:
        print("❌ 未选择文件")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)


    generate_puzzle_pdf(json_path, data)
    generate_solution_pdf(json_path, data)

if __name__ == "__main__":
    main()
