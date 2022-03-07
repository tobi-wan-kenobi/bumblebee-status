#include <stdio.h>
#include <stdlib.h>

#include <X11/XKBlib.h>

void err_if(int condition, const char* msg)
{
	if (condition) {
		fprintf(stderr, "fatal: %s\n", msg);
		exit(1);
	}
}

int main(int argc, char** argv)
{
	Display* display = XOpenDisplay(NULL);
	err_if(!display, "unable to open display");

	int kbd = argc == 1 ? XkbUseCoreKbd : atoi(argv[1]);

	XkbStateRec state;
	XkbGetState(display, kbd, &state);

	XkbDescPtr desc = XkbGetKeyboard(display, XkbAllComponentsMask, kbd);
	char* symbols = XGetAtomName(display, desc->names->symbols);
	printf("%s\n", symbols);

#if 0
	char *group = XGetAtomName(display, desc->names->groups[state.group]);
	XFree(group);
#endif
	XFree(symbols);
	XFree(desc);

	XCloseDisplay(display);

	return 0;
}

