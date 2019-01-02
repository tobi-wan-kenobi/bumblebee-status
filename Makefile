DEBIAN_ROOT = build/debian/bumblebee-status/

deb:
	mkdir -p $(DEBIAN_ROOT)/DEBIAN
	mkdir -p $(DEBIAN_ROOT)/usr/share/bumblebee-status/modules
	mkdir -p $(DEBIAN_ROOT)/usr/share/bumblebee-status/themes
	cp build/debian/control $(DEBIAN_ROOT)/DEBIAN/
	cp bumblebee-status $(DEBIAN_ROOT)/usr/share/bumblebee-status/
	cp bumblebee/modules/*.py $(DEBIAN_ROOT)/usr/share/bumblebee-status/modules/
	cp -r themes/* $(DEBIAN_ROOT)/usr/share/bumblebee-status/themes
	cp LICENSE $(DEBIAN_ROOT)/usr/share/bumblebee-status/
	dpkg-deb --build $(DEBIAN_ROOT)
	cp build/debian/bumblebee-status.deb .

clean:
	rm -rf $(DEBIAN_ROOT)
	rm -f build/debian/*.deb
	rm -f *.deb
