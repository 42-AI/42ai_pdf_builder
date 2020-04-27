# Guidelines for PDF Builder Syntax

If you want to use the `pdfbuilder.py` script, use the following guidelines:

## Main elements

### List

Elements must be separated by one newline:  
```
* {content1}

* {content1}
```

### Image

There are two ways to embed images:  
```
<img src="{image_path}">
![alt text](image_path){width=300px}
```

### Link

```
[inline-style link](http://mylink.com)
```
