from fpdf import FPDF
from PIL import Image


class PDF(FPDF):
    def __init__(self, pg_num = 1, *args, **kwargs):
        super(PDF, self).__init__(*args, **kwargs)
        self.add_font('Arial', '', r'C:\Windows\Fonts\arial.ttf')
        self.set_left_margin(15)
        self.set_right_margin(15)
        self.pg_num = pg_num

    def header(self):
        self.set_y(0)
        self.image('static/pics/header.png', x = 0, y = 0, w = self.epw+32, h = 200)
        self.image('static/pics/logo.png', x = -17, y = -10, w = 170, h = 200)

    # Page footer
    def footer(self):
        self.set_y(-15)
        self.image('static/pics/footer.png', x = 0, y = 96.9, w = self.epw+32, h = 200)
        self.set_font('Arial', '', 10)
        if self.pg_num == 1:
            self.cell(0, 10, f'Page {self.page_no()} / {{nb}}', align='R')
        elif self.pg_num == 2:
            if self.page_no() == 1:
                page_number = ''
            else:
                page_number = f'Page {self.page_no()} / {{nb}}'
            self.cell(0, 10, page_number, align='R')
        else:
            self.cell(0, 10, '', align='R')

    # Adding chapter title to start of each chapter
    def chapter_title(self, chap_title):
        self.set_font('helvetica', '', 20)
        self.set_xy(15, 45)
        chapter_title = f'{chap_title}'
        self.cell(text=chapter_title, new_x='LMARGIN', new_y='NEXT', fill=False)

    # Chapter content
    def chapter_body(self, chap_title, title, sub_title, txt_to, image_to, minmax):
        self.set_font('helvetica', '', 16)
        if chap_title:
            im_y = 72
            self.set_xy(15, 60)
        else:
            if minmax:
                im_y = 175
                self.set_xy(15, 165)
            else:
                if 'Middle value' in title:
                    im_y = 50
                    self.set_xy(15, 40)
                else:
                    self.set_xy(15, 45)
                    im_y = 55
        self.cell(text=title)
        if sub_title:
            if chap_title:
                im_y = 74
            else:
                im_y = 60
            self.set_font_size(12)
            self.ln()
            self.set_x(15)
            self.cell(w = 0, h = 5, text=sub_title)
        self.image(image_to, x = 15, y = im_y, w=180, keep_aspect_ratio=True)
        with Image.open(image_to) as pic:
            w, h = pic.size
            im_h = h/w*180
        self.set_xy(15, im_h+im_y+8)
        self.set_font_size(12)
        self.multi_cell(w = 0, h = 5, align='J', text=txt_to)
        self.ln()


    def print_chapter(self, chap_title='', title='', sub_title='', txt_to='', image_to='', minmax = 0):
        if not minmax:
            self.add_page()
        if chap_title:
            self.chapter_title(chap_title)
        self.chapter_body(chap_title, title, sub_title, txt_to, image_to, minmax)


def create_table_of_contents(pdf, titles_txt, int_link, ch1_link, ch2_link):
    pdf.add_page()
    pdf.set_font('helvetica', '', 20)
    pdf.set_xy(30,60)
    pdf.cell(text='Contents', new_y='NEXT')
    pdf.set_xy(40,75)
    pdf.set_font_size(16)
    if int_link:
        pdf.cell(text=titles_txt['intro'][0], new_y='NEXT', link = int_link)
        pdf.ln()
        pdf.set_x(40)
    if ch1_link:
        pdf.cell(text='1. Tables', new_y='NEXT', link = ch1_link)
        pdf.ln()
        pdf.set_font_size(12)
        for k, v in titles_txt.items():
            if 'df' in k and v[3].startswith('bl', 0, 2):
                pdf.set_x(50)
                pdf.cell(text=v[0], new_y='NEXT')
                pdf.ln()
    if ch2_link:
        pdf.ln()
        pdf.set_x(40)
        pdf.set_font_size(16)
        pdf.cell(text='2. Charts', new_x='LMARGIN', new_y='NEXT', link = ch2_link)
        pdf.ln()
        pdf.set_font_size(12)
        for k, v in titles_txt.items():
            if 'ch_' in k and v[3].startswith('bl', 0, 2):
                pdf.set_x(50)
                pdf.cell(text=v[0], new_y='NEXT')
                pdf.ln()


def create_intro(pdf, titles_txt):           
    pdf.add_page()
    pdf.set_font('helvetica', '', 20)
    pdf.set_xy(15, 50)
    pdf.cell(text=titles_txt['intro'][0], new_x='LMARGIN', new_y='NEXT')
    if titles_txt['intro'][1]:
        pdf.set_font_size(16)
        pdf.set_xy(15, 70)
        pdf.cell(text=titles_txt['intro'][1], new_x='LMARGIN', new_y='NEXT')
    if titles_txt['intro'][2]:
        pdf.set_font_size(12)
        pdf.set_xy(15, 83)
        pdf.multi_cell(w = 0, h = 5, align='J', text=titles_txt['intro'][2])


def create_cover(pdf, titles_txt):           
    pdf.add_page()
    pdf.set_font('helvetica', '', 30)
    pdf.set_xy(15, 90)
    pdf.multi_cell(w = 0, h = 5, align='C', text=titles_txt['cover_title'][0])
    if titles_txt['cover_title'][1]:
        pdf.set_font_size(16)
        pdf.set_xy(15, 105)
        pdf.multi_cell(w = 0, h = 5, align='C', text=titles_txt['cover_title'][1])
    if titles_txt['cover_title'][2]:
        pdf.set_font_size(12)
        pdf.set_xy(15, 130)
        pdf.multi_cell(w = 0, h = 5, align='C', text=titles_txt['cover_title'][2])


def create_pdf(titles_txt, png_dir, pg_num):
    pdf = PDF(pg_num, 'P', 'mm', 'A4')
    pdf.set_auto_page_break(auto = True, margin = 15)
    start_page_num = 0
    int_link = 0
    if titles_txt['cover_title'][3].startswith('bl', 0, 2):
        pdf.set_title(titles_txt['cover_title'][0])
        start_page_num += 1
        create_cover(pdf, titles_txt)
    pdf.set_author('Real Estate Analyzer Tool')
    if titles_txt['intro'][3].startswith('bl', 0, 2):
        start_page_num += 1
        int_link = pdf.add_link(page = start_page_num + 1)
    df = 0
    ch1_link = ''
    ch2_link = ''
    for k, v in titles_txt.items():
        if not ch1_link and 'df_' in k and v[3].startswith('bl', 0, 2):
            ch1_link = 1
        if not ch2_link and 'ch_' in k and v[3].startswith('bl', 0, 2):
            ch2_link = 1
    if ch1_link:
        for _ in titles_txt:
            if 'df' in _: df += 1
    if ch1_link: ch1_link = pdf.add_link(page = start_page_num + 2)
    if not ch1_link: start_page_num += 1
    if ch2_link and 'df_maxes' in titles_txt and titles_txt['df_maxes'][3].startswith('bl', 0, 2) and 'df_mins' in titles_txt and titles_txt['df_mins'][3].startswith('bl', 0, 2): ch2_link = pdf.add_link(page = start_page_num + 1 + df)
    elif ch2_link: ch2_link = pdf.add_link(page = start_page_num + 1 + df)
    create_table_of_contents(pdf, titles_txt, int_link, ch1_link, ch2_link)
    if titles_txt['intro'][3].startswith('bl', 0, 2):
        create_intro(pdf, titles_txt)
    chapt = ''
    for k, v in titles_txt.items():
        minmax = 0
        if k.startswith('cover_') or k.startswith('intro'):
            continue
        if 'chapter' in k:
            chapt = titles_txt[k]
            continue
        if v[3].startswith('bl', 0, 2):
            if 'df_min' in k and titles_txt['df_maxes'][3].startswith('bl', 0, 2):
                    minmax = 1
            if v[1]:
                pdf.print_chapter(chap_title=chapt, title=titles_txt[k][0], sub_title=titles_txt[k][1], txt_to=titles_txt[k][2], image_to=f'{png_dir}/{k}.png', minmax = minmax)
            else:
                pdf.print_chapter(chap_title=chapt, title=titles_txt[k][0], txt_to=titles_txt[k][2], image_to=f'{png_dir}/{k}.png', minmax = minmax)
            chapt = ''

    pdf.output('static/Real_Estate_analysis.pdf')