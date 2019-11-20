from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm

default = getSampleStyleSheet()

_42_ai = getSampleStyleSheet()

_42_ai.add(
    ParagraphStyle(
        name="_p",
        parent=_42_ai["Normal"],
        fontSize=11,
        leading=13,
    )
)

_42_ai.add(
    ParagraphStyle(
        name="_li",
        parent=_42_ai["Normal"],
        fontSize=11,
        leading=15,
        bulletText="•",
        bulletFontSize=11,
    )
)

_42_ai.add(
    ParagraphStyle(
        name="main_title",
        parent=_42_ai["Normal"],
        leading=30,
        alignment=TA_CENTER,
        fontSize=40,
        fontName="Helvetica-Bold",
    )
)

_42_ai.add(
    ParagraphStyle(
        name="_h1",
        parent=_42_ai["Normal"],
        leading=30,
        alignment=TA_CENTER,
        fontSize=30,
        fontName="Helvetica-Bold",
    )
)

_42_ai.add(
    ParagraphStyle(
        name="_h2",
        parent=_42_ai["Normal"],
        leading=20,
        alignment=TA_LEFT,
        fontSize=20,
        fontName="Helvetica-Bold",
    )
)

_42_ai.add(
    ParagraphStyle(
        name="_h3",
        parent=_42_ai["Normal"],
        leading=14,
        alignment=TA_LEFT,
        fontSize=14,
        fontName="Helvetica-Bold",
    )
)

_42_ai.add(
    ParagraphStyle(
        name="_code",
        parent=_42_ai["Normal"],
        fontName="Courier",
        backColor="#303030",
        textColor="white",
        borderPadding=0.1 * cm,
    )
)

styles = {
    '42-ai': _42_ai,
    'default': default
}
