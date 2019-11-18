#! python3

import argparse
import os
import fnmatch
import random
import string

from reportlab.lib.pagesizes import letter

from reportlab.lib import colors

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import Image
from reportlab.platypus import PageBreak, CondPageBreak
from reportlab.platypus import Table
from reportlab.platypus import TableStyle

from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from mdloader import MDLoader, HTMLTag
from config import styles

def format_rl_attrs(attrs):
    new_attrs = []
    height = 0
    align = False
    for attr in attrs:
        if attr[0] == 'alt':
            continue
        if attr[0] == 'align':
            align = attr[1]
        else:
            new_attrs.append(attr)
        if attr[0] == 'height':
            height = attr[1]
    if align == 'middle':
        new_attrs.append(('valign', -(float(height) / 2)))
    return new_attrs

def convert_HTMLTag_toRl(htmlTag):
    if type(htmlTag) != HTMLTag:
        return htmlTag.replace('\n', '<br/>')
    attrs = format_rl_attrs(htmlTag.attrs)
    rl_data = f"<{htmlTag.tag}{' ' if attrs else ''}{' '.join([f'{key}={value}' for key, value in attrs])}{' ' if attrs else ''}"
    if htmlTag.children:
        rl_data += f">{''.join([convert_HTMLTag_toRl(child) if type(child) == HTMLTag else child for child in htmlTag.children])}</{htmlTag.tag}>"
    else:
        rl_data += '/>'
    return rl_data

def extract_table(content):
    table = []
    for elem in content:
        for row in elem.children:
            table.append([])
            empty = True
            for item in row.children:
                value = [convert_HTMLTag_toRl(child) for child in item.children]
                table[-1].append(''.join(value))
                if value:
                    empty = False
            if empty:
                table.pop()

    return table


class PDFBuilder:
    def __init__(self, file, styles, background, logo):
        self.name = file
        self.background = os.path.dirname(os.path.realpath(__file__)) + background
        self.logo = os.path.dirname(os.path.realpath(__file__)) + logo
        self.pdf_name = file.strip('\\/') + ".pdf"
        self.doc = SimpleDocTemplate(
            self.pdf_name,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=42,
        )
        self.styles = styles
        self.add = {
            'p': self.addParagraph,
            'img': self.addImage,
            'pre': self.addCode,
            'h1': self.addHeader,
            'h2': self.addHeader,
            'h3': self.addHeader,
            'table': self.addTable,
            'ul': self.addList,
            'ol': self.addList,
        }
    
    def backgroundSetup(self):
        background = self.background

        def bgSetup(canvas, doc):
            canvas.saveState()
            width, height = letter
            canvas.drawImage(background, 0, 0, width, height)
            canvas.setFont('Times-Roman', 10)
            if doc.page > 1:
                canvas.drawString(width / 2, 38, f"Page {doc.page}")
            canvas.restoreState()

        return bgSetup

    def addPDFHead(self, Story, title):
        def split_title(title):
            split = title.split()
            splitted = []
            for sub in split:
                if not splitted or len(splitted[-1]) > 7:
                    splitted.append(sub)
                else:
                    splitted[-1] += f' {sub}'
            return splitted

        splitted = split_title(title)

        Story.append(Spacer(1, 2 * cm))

        for i, sub in enumerate(splitted):
            if i > 0:
                Story.append(Spacer(1, 12))
            Story.append(Paragraph(sub, self.styles["main_title"]))

        Story.append(Spacer(1, 4 * cm))

        logo = Image(self.logo, 7.55 * cm, 6 * cm)

        Story.append(logo)

        Story.append(PageBreak())

    def addPDFPage(self, Story, filename, with_compilation):
        tmp_name = '.' + ''.join(
            random.choices(string.ascii_lowercase + string.digits, k=16)
        ) + '.md'

        if with_compilation is True:
            os.system(f'python3 -m readme2tex --nocdn \
                      --output {tmp_name} {filename}')
            filename = tmp_name

        data = MDLoader(filename).read()

        if with_compilation is True:
            os.remove(tmp_name)

        for i, htmlTag in enumerate(data):
            if i > 0:
                Story.append(Spacer(1, 12))
            self.add[htmlTag.tag](Story, htmlTag)

        _, height = letter
        Story.append(CondPageBreak(height - 50))

    def addHeader(self, Story, htmlTag):
        content = [convert_HTMLTag_toRl(child) for child in htmlTag.children]

        Story.append(Paragraph(''.join(content), self.styles[f"_{htmlTag.tag}"]))

        Story.append(Spacer(1, cm / (int(htmlTag.tag[-1]) + 2)))
        if htmlTag.tag == 'h1':
            Story.append(Spacer(1, cm - cm / (int(htmlTag.tag[-1]) + 2)))


    def addImage(self, Story, htmlTag):
        m_width, m_height = 12 * cm, 8 * cm

        style = [
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
        ]

        table = Table(
            data=[[Image(htmlTag.attrs[0][1], m_width, m_height)]],
            colWidths=12*cm,
            rowHeights=8*cm,
            style=style
        )
        Story.append(table)

    def TableFormater(self, content):
        table = []
        for line in content:
            table.append([Paragraph(elem, self.styles["_p"]) for elem in line])
        return table

    def addTable(self, Story, htmlTag):
        content = extract_table(htmlTag.children)
        table = Table(
            self.TableFormater(content), colWidths=[5 * cm, 10 * cm], hAlign="CENTER"
        )
        table.setStyle(
            TableStyle(
                [
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ]
            )
        )
        Story.append(table)

    def addCode(self, Story, htmlTag):
        content = [convert_HTMLTag_toRl(child) for child in htmlTag.children[0].children]
        para = Paragraph(''.join(content), self.styles["_code"])
        Story.append(CondPageBreak(self.styles['_code'].leading * (''.join(content).count('<br/>') + 1)))
        Story.append(para)

    def addList(self, Story, htmlTag):
        for li in htmlTag.children:
            content = [convert_HTMLTag_toRl(child) for child in li.children]
            Story.append(Paragraph(''.join(content), self.styles["_li"]))

    def addParagraph(self, Story, htmlTag):
        content = [convert_HTMLTag_toRl(child) for child in htmlTag.children]

        alignment = TA_LEFT

        for attr in htmlTag.attrs:
            if attr[0] == 'align' and attr[1] == 'center':
                alignment = TA_CENTER

        max_height = 0
        for child in htmlTag.children:
            if type(child) == HTMLTag:
                for attr in child.attrs:
                    if attr[0] == 'height' and float(attr[1]) > max_height:
                        max_height = float(attr[1])

        style = ParagraphStyle(
            name='_p' + ''.join(
                random.choices(string.ascii_lowercase + string.digits, k=5)
            ),
            parent=self.styles['_p'],
            leading=max_height or 15,
            alignment=alignment
        )

        Story.append(Paragraph(''.join(content), style))
        Story.append(Spacer(1, 5))

    def savePDF(self, Story, with_optimization):
        print('Saving PDF as', self.pdf_name)

        tmp_name = '.' + ''.join(
            random.choices(string.ascii_lowercase + string.digits, k=16)
        ) + '.pdf' 

        if with_optimization is True:
            self.doc.filename = tmp_name

        self.doc.build(
            Story,
            onFirstPage=self.backgroundSetup(),
            onLaterPages=self.backgroundSetup(),
        )

        if with_optimization is True:
            old_size = os.path.getsize(tmp_name) / 1000000
            os.system(f'gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
                -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH \
                -sOutputFile={self.pdf_name} {tmp_name}')
            new_size = os.path.getsize(self.pdf_name) / 1000000
            print(f'  size was {old_size:.2f} mb -> {new_size:.2f} mb')
            os.remove(tmp_name)


    def setMetaData(self, metadata):
        self.doc.title = self.pdf_name
        self.doc.author = metadata['author']
        self.doc.creator = metadata['creator']
        self.doc.subject = metadata['subject']
        self.doc.keywords = list(metadata['keywords'])

    def build(self, title, options, metadata):

        print('\nStarting creation of', self.pdf_name)
        self.setMetaData(metadata)

        files = []
        if not os.path.isdir(self.name):
            files.append(self.name)
        else:
            for root, dirnames, filenames in os.walk(self.name):
                for filename in fnmatch.filter(filenames, '*.md'):
                    files.append(os.path.join(root, filename))
            files.sort(key=lambda x: (x.replace(self.name, '').count('/'), x))
            
        print('.md files detected:\n ', '\n  '.join(files))

        Story = []
        self.addPDFHead(Story, title)
        for filename in files:
            self.addPDFPage(Story, filename, options['compile'])

        self.savePDF(Story, options['optimize'])






if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('file', type=str, nargs='+', help='a directory or a .md file')
    parser.add_argument('-mt', '--main-title', type=str, default='A 42 AI project', help='main title for a pdf')
    parser.add_argument('-l', '--latex', action='store_true', help='compile latex for every .md file using readme2tex library')
    parser.add_argument('-o', '--optimize', action='store_true', help='optimize .pdf size with ghostscript')

    parser.add_argument('-a', '--author', type=str,  help='pdf author metadata', default='42-ai')
    parser.add_argument('-c', '--creator', type=str,  help='pdf creator metadata', default='42-ai')
    parser.add_argument('-s', '--subject', type=str,  help='pdf subject metadata', default='Python exercises')
    parser.add_argument('-k', '--keywords', nargs='+', help='pdf keywords metadata', default=[])

    parser.add_argument('-bg', '--background', type=str, help='pdf background', default='/assets/background-42-ai.png')
    parser.add_argument('-lg', '--logo', type=str, help='main page logo', default='/assets/logo-42-ai.png')
    parser.add_argument('-st', '--style', type=str, help='overall style used', default='42-ai')

    args = parser.parse_args()

    options = {
        'optimize': args.optimize,
        'compile': args.latex,
    }
    metadata = {
        'subject': args.subject,
        'author': args.author,
        'creator': args.creator,
        'keywords': set(['python', '42-ai', 'coding', 'learning', 'training'] + args.keywords)
    }

    print('Thanks for using the pdfbuilder made by 42-ai')
    print()
    print('------  Infos  ------')
    print(f'Title: {args.main_title!r}')
    print(f'Logo: {args.logo!r}')
    print(f'Background: {args.background!r}')
    print(f'Style: {args.style!r}')
    print('Number of PDF:', len(args.file))
    print(
        'Options:',
        f"  - latex compilation: {options['compile']}",
        f"  - reduce pdf size: {options['optimize']}",
        sep='\n'
    )
    print(
        'Metadata:',
        f"  - author: {metadata['author']!r}",
        f"  - creator: {metadata['creator']!r}",
        f"  - subject: {metadata['subject']!r}",
        f"  - keywords: {metadata['keywords']}",
        sep='\n'
    )
    print('---------------------')

    for filename in args.file:
        pdf = PDFBuilder(filename, styles[args.style], args.background, args.logo)
        pdf.build(args.main_title, options, metadata)


