PREFIX ?= /usr

all:
	@echo Run \'sudo make install\' to install Sequestrum.

install:
	@mkdir -p $(DESTDIR)$(PREFIX)/bin
	@cp -p sequestrum $(DESTDIR)$(PREFIX)/bin/sequestrum
	@chmod 755 $(DESTDIR)$(PREFIX)/bin/sequestrum

uninstall:
	@rm -rf $(DESTDIR)$(PREFIX)/bin/sequestrum
