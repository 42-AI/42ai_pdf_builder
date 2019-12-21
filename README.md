<p align="center">
  <img src="assets/logo-42-ai.png" width="200" alt="42 AI Logo" />
</p>

<h1 align="center">
  PDF Builder
</h1>
<h3 align="center">
  A PDF builder made to create all our subjects :rocket:
</h3>
<br/>

## Installation

### Requirements


* Python 3.x
* Pillow 6.2.0
* reportlab 3.5.32
* mistletoe 0.7.2
* CairoSVG 2.4.2
* readme2tex 0.0.1b2

And:
* Ghostscript

## Supported elements

The `pdfbuilder` supports the following syntax.

**Warning: if you are using LaTeX syntax, make sure to escape a `$` that is not LaTeX with a backslash.**

### h1 title
```
# {content}
```

### h2 title
```
## {content}
```

### h3 title
```
### {content}
```

### List
```
* {content}
```

### Image
**Warning: any image inserted using `![image info](path/to/img)` is not supported.**
```
<img src="{image_path}" width={image_width} height={image_height}>
```

### Paragraph
**Warning: content of paragraph can only be `<img />` or simple text.**
```
<p>{content}</p>
```

### Code section
**Warning: only Python and bash language are currently supported.**
<pre><code>```{language}
{content}
```</code></pre>

### Table
```
|                  |                  |
| ----------------:| ---------------- |
|   {content}      |   {content}      |
|   {content}      |   {content}      |
|   {content}      |   {content}      |
|   {content}      |   {content}      |
```

### LaTeX
**Warning: use `--latex`.**
```
$$
f(x) = \frac{1} {1 + e^{-x}}
$$
```

### Inline LaTeX
**Warning: use `--latex`.**
```
This is inline LaTeX, $f(x) = -x$
```

### Text formatting
#### Bold
```
text **{bold content}** text
text *{bold content}* text
```

#### Italic
```
text __{italic content}__ text
text _{italic content}_ text
```

#### Code highlight
```
text `{code content}` text
```

## Usage

You just need to `git clone` the project.

```console
git clone https://github.com/42-AI/42ai_pdf_builder
```

And make sure you are using Python 3.

```console
$> python -V
Python 3.7.*
```

Basic usage:
```console
python pdfbuilder.py /path/to/folder_or_md_file
```

With LaTeX compilation:
```console
python pdfbuilder.py --latex /path/to/folder_or_md_file
```

With PDF size optimization:
```console
python pdfbuilder.py --optimize /path/to/folder_or_md_file
```

Build some PDFs:
```console
python pdfbuilder.py /path/to/folder_or_md_file /path/to/folder_or_md_file /path/to/folder_or_md_file
```

Example:
```console
python pdfbuilder.py --main-title "The Best Bootcamp Ever" --optimize --latex --author '42-ai' day00 day01 day02 day03 day04 rush00
```

Available options:
```
  -h, --help            show this help message and exit

  -mt MAIN_TITLE, --main-title MAIN_TITLE
                        main title for a pdf

  -l, --latex           compile latex for every .md file using readme2tex
                        library, default: False

  -o, --optimize        optimize .pdf size with ghostscript, default: False

  -a AUTHOR, --author AUTHOR
                        change pdf author metadata

  -c CREATOR, --creator CREATOR
                        change pdf creator metadata

  -s SUBJECT, --subject SUBJECT
                        change pdf subject metadata

  -k KEYWORDS [KEYWORDS ...], --keywords KEYWORDS [KEYWORDS ...]
                        add pdf keywords metadata

  -bg BACKGROUND, --background BACKGROUND
                        path to pdf background

  -lg LOGO, --logo LOGO
                        path to main page logo

  -st STYLE, --style STYLE
                        overall style used
```

## Acknowledgements

### Contributors

* Maxime Choulika (maxime@42ai.fr)
* Antoine Fourès (afoures@student.42.fr)
