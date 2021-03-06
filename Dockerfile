FROM pandoc/latex

RUN apk update \
	&& apk add python3 \
	&& apk add git \
	&& git clone https://github.com/fxbabin/pdf_builder . \
	&& tlmgr option repository http://mirror.ctan.org/systems/texlive/tlnet \
	&& tlmgr update --self \
	&& tlmgr install fvextra \
	&& tlmgr install sectsty \
	&& tlmgr install titlesec \
    && tlmgr install ucs \
    && tlmgr install cancel
