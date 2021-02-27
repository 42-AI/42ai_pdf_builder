FROM pandoc/latex

RUN apk update \
	&& apk add python3 \
	&& apk add py3-pip \
	&& apk add git \
	&& pip install git+https://github.com/42-AI/42ai_pdf_builder.git \
	&& tlmgr option repository http://mirror.ctan.org/systems/texlive/tlnet \
	&& tlmgr update --self \
	&& tlmgr install fvextra \
	&& tlmgr install sectsty \
	&& tlmgr install titlesec \
    && tlmgr install ucs \
    && tlmgr install cancel