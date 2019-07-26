all: pack

pack:
	zip --quiet CCcamTester ./*.py
	zip --quiet --junk-paths CCcamTester ./__main__.py
	echo '#!/usr/bin/env python' > CCcamTester
	cat CCcamTester.zip >> CCcamTester
	rm CCcamTester.zip
	chmod a+x CCcamTester

clean:
	rm -f CCcamTester

install:
	cp CCcamTester /usr/local/bin/

uninstall:
	rm -f /usr/local/bin/CCcamTester