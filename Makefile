NAME=label-guides
VERSION=1.0.0

DESTDIR ?= /usr/share/inkscape/extensions

ZIP=$(NAME)-$(VERSION).zip

SRC_FILES=label_guides.py label_guides.inx

$(ZIP): $(SRC_FILES)
	zip -r $(ZIP) $(SRC_FILES)

.PHONY: clean zip install

clean:
	rm -f $(NAME)-*.zip

zip: $(ZIP)

install:
	mkdir -p $(DESTDIR)
	install -m 755 -t $(DESTDIR) label_guides.py
	install -m 644 -t $(DESTDIR) label_guides.inx
