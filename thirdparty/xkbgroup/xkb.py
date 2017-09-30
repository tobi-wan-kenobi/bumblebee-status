# -*- coding: utf-8 -*-

# #! /bin/sh
#
#
# h2xml -c -o xkb.xml X11/Xlib.h X11/Xlibint.h X11/XKBlib.h
# # The python-ctypeslib packages contains a bug; firstly fix it with the patch
# # from https://sourceforge.net/p/ctypes/mailman/message/25291919/
# xml2py -k defst -o xkb.py -l X11 xkb.xml
#
#
# # Stop interpreter from crying
#
# # P.S. X.h has None and Xlib.h has True and False #defines
# # To use them without overlapping with the Python keywords just add trailing
# # underscores, like None_, True_ and False_
#
# sed -i "s/^None /None_ /" xkb.py
# sed -i "s/'None'/'None_'/" xkb.py
# sed -i "s/^True /True_ /" xkb.py
# sed -i "s/'True'/'True_'/" xkb.py
# sed -i "s/^False /False_ /" xkb.py
# sed -i "s/'False'/'False_'/" xkb.py
# sed -i 's/\( = [0-9]\+\)L/\1/g' xkb.py
#
#
# # Write this script's contents for reference
#
# (sed 's/\(.*\)/# \1/; s/# $/#/' "$0"; echo; cat xkb.py) > tmp
# mv tmp xkbgroup/xkb.py
# rm xkb.py

from ctypes import *

STRING = c_char_p
_libraries = {}
_libraries['libX11.so.6'] = CDLL('libX11.so.6')
WSTRING = c_wchar_p


XIMIsSecondary = 2
XIMIsPrimary = 1
XIMIsInvisible = 0
XIMDontChange = 11
XIMAbsolutePosition = 10
XIMLineEnd = 9
XIMLineStart = 8
XIMNextLine = 6
XIMForwardChar = 0
XIMBitmapType = 1
XIMTextType = 0
XOMOrientation_Context = 4
XOMOrientation_TTB_RTL = 3
XOMOrientation_RTL_TTB = 1
XOMOrientation_LTR_TTB = 0
XIMBackwardWord = 3
P_ALL = 0
XIMForwardWord = 2
P_PID = 1
P_PGID = 2
XIMPreviousLine = 7
XIMCaretDown = 5
XIMCaretUp = 4
XIMBackwardChar = 1
XOMOrientation_TTB_LTR = 2
ETXTBSY = 26 # Variable c_int '26'
GCClipXOrigin = 131072 # Variable c_long '131072l'
XkbSA_SetValMin = 16 # Variable c_int '16'
NoSymbol = 0 # Variable c_long '0l'
ButtonMotionMask = 8192 # Variable c_long '8192l'
XkbSI_LevelOneOnly = 128 # Variable c_int '128'
XkbNoIndicator = 255 # Variable c_int '255'
X_SetSelectionOwner = 22 # Variable c_int '22'
EL3HLT = 46 # Variable c_int '46'
EnterWindowMask = 16 # Variable c_long '16l'
ENOTSOCK = 88 # Variable c_int '88'
XkbSA_GroupAbsolute = 4 # Variable c_long '4l'
XkbLC_AlternateGroup = 4096 # Variable c_long '4096l'
XIMPrimary = 32 # Variable c_long '32l'
XkbSI_OpMask = 127 # Variable c_int '127'
ENOLINK = 67 # Variable c_int '67'
__NFDBITS = 64 # Variable c_int '64'
ColormapInstalled = 1 # Variable c_int '1'
AnyModifier = 32768 # Variable c_int '32768'
X_ImageText16 = 77 # Variable c_int '77'
X_PolyRectangle = 67 # Variable c_int '67'
_DEFAULT_SOURCE = 1 # Variable c_int '1'
ForgetGravity = 0 # Variable c_int '0'
XkbTwoLevelMask = 2 # Variable c_int '2'
sz_xGetPropertyReply = 32 # Variable c_int '32'
KBKey = 64 # Variable c_long '64l'
X_kbSetGeometry = 20 # Variable c_int '20'
MappingFailed = 2 # Variable c_int '2'
EALREADY = 114 # Variable c_int '114'
XIMPreeditArea = 1 # Variable c_long '1l'
XkbAXN_SKReleaseMask = 8 # Variable c_long '8l'
E2BIG = 7 # Variable c_int '7'
CWBorderPixel = 8 # Variable c_long '8l'
EHOSTDOWN = 112 # Variable c_int '112'
GrayScale = 1 # Variable c_int '1'
EBUSY = 16 # Variable c_int '16'
X_GetImage = 73 # Variable c_int '73'
sz_xChangeHostsReq = 8 # Variable c_int '8'
X_FreeCursor = 95 # Variable c_int '95'
ButtonPress = 4 # Variable c_int '4'
sz_xFontProp = 8 # Variable c_int '8'
X_ListExtensions = 99 # Variable c_int '99'
EDQUOT = 122 # Variable c_int '122'
PointerWindow = 0 # Variable c_long '0l'
IsViewable = 2 # Variable c_int '2'
X_QueryTextExtents = 48 # Variable c_int '48'
X_TCP_PORT = 6000 # Variable c_int '6000'
XkbAX_SKPressFBMask = 1 # Variable c_long '1l'
X_FreeGC = 60 # Variable c_int '60'
AllPlanes = 18446744073709551615 # Variable c_ulong '-1ul'
X_ImageText8 = 76 # Variable c_int '76'
ArcPieSlice = 1 # Variable c_int '1'
X_ChangeKeyboardControl = 102 # Variable c_int '102'
EXFULL = 54 # Variable c_int '54'
X_ChangeKeyboardMapping = 100 # Variable c_int '100'
XkbIM_UseNone = 0 # Variable c_int '0'
sz_xLookupColorReq = 12 # Variable c_int '12'
X_ChangeGC = 56 # Variable c_int '56'
XkbPCF_LookupStateWhenGrabbed = 8 # Variable c_long '8l'
EFBIG = 27 # Variable c_int '27'
X_GetKeyboardControl = 103 # Variable c_int '103'
ColormapChangeMask = 8388608 # Variable c_long '8388608l'
XkbAX_StickyKeysFBMask = 32 # Variable c_long '32l'
__WORDSIZE = 64 # Variable c_int '64'
XNStatusDoneCallback = 'statusDoneCallback' # Variable STRING '(const char*)"statusDoneCallback"'
_XOPEN_SOURCE = 700 # Variable c_int '700'
LineOnOffDash = 1 # Variable c_int '1'
XLookupBoth = 4 # Variable c_int '4'
sz_xStoreColorsReq = 8 # Variable c_int '8'
LASTEvent = 36 # Variable c_int '36'
sz_xOpenFontReq = 12 # Variable c_int '12'
__GLIBC__ = 2 # Variable c_int '2'
DefaultExposures = 2 # Variable c_int '2'
XkbSA_LockNoUnlock = 2 # Variable c_long '2l'
sz_xQueryBestSizeReq = 12 # Variable c_int '12'
GXnand = 14 # Variable c_int '14'
sz_xGenericReply = 32 # Variable c_int '32'
Mod2Mask = 16 # Variable c_int '16'
VisibilityNotify = 15 # Variable c_int '15'
_XLOCALE_H = 1 # Variable c_int '1'
XkbSA_SwitchScreen = 13 # Variable c_int '13'
XkbAXN_SKAcceptMask = 2 # Variable c_long '2l'
XkbSymbolsNameMask = 4 # Variable c_int '4'
sz_xPolyText16Req = 16 # Variable c_int '16'
ENOTTY = 25 # Variable c_int '25'
XNQueryIMValuesList = 'queryIMValuesList' # Variable STRING '(const char*)"queryIMValuesList"'
X_AllocColor = 84 # Variable c_int '84'
sz_xGrabKeyboardReply = 32 # Variable c_int '32'
__USE_POSIX2 = 1 # Variable c_int '1'
EMLINK = 31 # Variable c_int '31'
__USE_XOPEN2K8XSI = 1 # Variable c_int '1'
FamilyInternet = 0 # Variable c_int '0'
GXandReverse = 2 # Variable c_int '2'
ECANCELED = 125 # Variable c_int '125'
XNStatusAttributes = 'statusAttributes' # Variable STRING '(const char*)"statusAttributes"'
XIMPreeditCallbacks = 2 # Variable c_long '2l'
XkbExplicitKeyType4Mask = 8 # Variable c_int '8'
XkbKeyTypeNamesMask = 64 # Variable c_int '64'
MappingSuccess = 0 # Variable c_int '0'
XkbXI_IndicatorMapsMask = 8 # Variable c_long '8l'
XkbKeyNamesMask = 512 # Variable c_int '512'
XNDefaultString = 'defaultString' # Variable STRING '(const char*)"defaultString"'
XkbIM_UseBase = 1 # Variable c_long '1l'
XkbPCF_DetectableAutoRepeatMask = 1 # Variable c_long '1l'
XkbAX_DumbBellFBMask = 2048 # Variable c_long '2048l'
sz_xGetFontPathReply = 32 # Variable c_int '32'
Mod3MapIndex = 5 # Variable c_int '5'
X_kbGetDeviceInfo = 24 # Variable c_int '24'
sz_xReply = 32 # Variable c_int '32'
ELOOP = 40 # Variable c_int '40'
SouthGravity = 8 # Variable c_int '8'
sz_xConfigureWindowReq = 12 # Variable c_int '12'
XkbLC_AllComposeControls = 3221225472 # Variable c_uint '3221225472u'
XkbSA_NoAcceleration = 1 # Variable c_long '1l'
GCForeground = 4 # Variable c_long '4l'
XkbSI_NoneOf = 0 # Variable c_int '0'
sz_xListPropertiesReply = 32 # Variable c_int '32'
__W_CONTINUED = 65535 # Variable c_int '65535'
ArcChord = 0 # Variable c_int '0'
XkbAXN_AXKWarning = 6 # Variable c_int '6'
EISNAM = 120 # Variable c_int '120'
sz_xGetScreenSaverReply = 32 # Variable c_int '32'
ColormapNotify = 32 # Variable c_int '32'
X_QueryTree = 15 # Variable c_int '15'
PlaceOnTop = 0 # Variable c_int '0'
XlibDisplayNoXkb = 4 # Variable c_long '4l'
sz_xSetClipRectanglesReq = 12 # Variable c_int '12'
XkbSA_SwitchAbsolute = 4 # Variable c_long '4l'
sz_xCreateCursorReq = 32 # Variable c_int '32'
XkbXI_AllDeviceFeaturesMask = 30 # Variable c_int '30'
sz_xAllocColorCellsReq = 12 # Variable c_int '12'
RetainTemporary = 2 # Variable c_int '2'
_BITS_TYPES_H = 1 # Variable c_int '1'
EILSEQ = 84 # Variable c_int '84'
MapRequest = 20 # Variable c_int '20'
XkbAllGroupsMask = 15 # Variable c_int '15'
ENONET = 64 # Variable c_int '64'
ECHRNG = 44 # Variable c_int '44'
NotifyPointerRoot = 6 # Variable c_int '6'
GCJoinStyle = 128 # Variable c_long '128l'
GCTileStipYOrigin = 8192 # Variable c_long '8192l'
XIMStringConversionLeftEdge = 1 # Variable c_int '1'
ESRCH = 3 # Variable c_int '3'
CWY = 2 # Variable c_int '2'
CWX = 1 # Variable c_int '1'
ReplayKeyboard = 5 # Variable c_int '5'
XkbAllNamesMask = 16383 # Variable c_int '16383'
YXSorted = 2 # Variable c_int '2'
sz_xGetAtomNameReply = 32 # Variable c_int '32'
ENOMSG = 42 # Variable c_int '42'
XkbSA_BreakLatch = 1045249 # Variable c_int '1045249'
EISDIR = 21 # Variable c_int '21'
LockMapIndex = 1 # Variable c_int '1'
XkbGeomPtsPerMM = 10 # Variable c_int '10'
__GNU_LIBRARY__ = 6 # Variable c_int '6'
sz_xImageTextReq = 16 # Variable c_int '16'
EnterNotify = 7 # Variable c_int '7'
X_QueryBestSize = 97 # Variable c_int '97'
X_InstallColormap = 81 # Variable c_int '81'
X_ConvertSelection = 24 # Variable c_int '24'
XkbNoShiftLevel = 255 # Variable c_int '255'
LeaveWindowMask = 32 # Variable c_long '32l'
BadAccess = 10 # Variable c_int '10'
XkbIM_UseAnyGroup = 15 # Variable c_long '15l'
X_AllowEvents = 35 # Variable c_int '35'
EBADRQC = 56 # Variable c_int '56'
StaticColor = 2 # Variable c_int '2'
sz_xGetSelectionOwnerReply = 32 # Variable c_int '32'
sz_xPolyFillRectangleReq = 12 # Variable c_int '12'
sz_xGrabKeyboardReq = 16 # Variable c_int '16'
CWBackingPlanes = 128 # Variable c_long '128l'
XkbSA_ISONoAffectPtr = 16 # Variable c_long '16l'
XkbRGMaxMembers = 12 # Variable c_int '12'
XkbGroupBaseMask = 32 # Variable c_long '32l'
X_InternAtom = 16 # Variable c_int '16'
sz_xSetMappingReply = 32 # Variable c_int '32'
sz_xGrabPointerReq = 24 # Variable c_int '24'
X_GetProperty = 20 # Variable c_int '20'
XkbDfltXIId = 1024 # Variable c_int '1024'
sz_xSendEventReq = 44 # Variable c_int '44'
X_ForceScreenSaver = 115 # Variable c_int '115'
sz_xGrabPointerReply = 32 # Variable c_int '32'
KBBellPercent = 2 # Variable c_long '2l'
sz_xAllocColorReq = 16 # Variable c_int '16'
__FD_SETSIZE = 1024 # Variable c_int '1024'
DisableAccess = 0 # Variable c_int '0'
Button2MotionMask = 512 # Variable c_long '512l'
LOCKED = 1 # Variable c_int '1'
XkbMapNotifyMask = 2 # Variable c_long '2l'
Convex = 2 # Variable c_int '2'
FARCSPERBATCH = 256 # Variable c_int '256'
EMFILE = 24 # Variable c_int '24'
X_UnmapWindow = 10 # Variable c_int '10'
PropertyNotify = 28 # Variable c_int '28'
Button3MotionMask = 1024 # Variable c_long '1024l'
__PTHREAD_MUTEX_HAVE_ELISION = 1 # Variable c_int '1'
XkbNumberErrors = 1 # Variable c_int '1'
MSBFirst = 1 # Variable c_int '1'
WNOHANG = 1 # Variable c_int '1'
sz_xGetModifierMappingReply = 32 # Variable c_int '32'
EXIT_SUCCESS = 0 # Variable c_int '0'
XkbCompatGrabModsMask = 1024 # Variable c_long '1024l'
CWOverrideRedirect = 512 # Variable c_long '512l'
ENOSTR = 60 # Variable c_int '60'
sz_xSetModifierMappingReq = 4 # Variable c_int '4'
__INO_T_MATCHES_INO64_T = 1 # Variable c_int '1'
FamilyDECnet = 1 # Variable c_int '1'
X_Bell = 104 # Variable c_int '104'
X_ListInstalledColormaps = 83 # Variable c_int '83'
X_OpenFont = 45 # Variable c_int '45'
XlibDisplayIOError = 1 # Variable c_long '1l'
InputFocus = 1 # Variable c_long '1l'
sz_xPutImageReq = 24 # Variable c_int '24'
KBBellDuration = 8 # Variable c_long '8l'
CapNotLast = 0 # Variable c_int '0'
XIMPreeditPosition = 4 # Variable c_long '4l'
__SIZEOF_PTHREAD_ATTR_T = 56 # Variable c_int '56'
XkbGrabModsMask = 512 # Variable c_long '512l'
XkbLC_ConsumeKeysOnComposeFail = 536870912 # Variable c_int '536870912'
NotifyHint = 1 # Variable c_int '1'
sz_xQueryFontReply = 60 # Variable c_int '60'
XNQueryInputStyle = 'queryInputStyle' # Variable STRING '(const char*)"queryInputStyle"'
__USE_XOPEN2KXSI = 1 # Variable c_int '1'
ShiftMapIndex = 0 # Variable c_int '0'
XkbAXN_SKAccept = 1 # Variable c_int '1'
XkbNewKeyboardNotifyMask = 1 # Variable c_long '1l'
XlibDisplayDfltRMDB = 128 # Variable c_long '128l'
CWSibling = 32 # Variable c_int '32'
__USE_XOPEN2K8 = 1 # Variable c_int '1'
SelectionNotify = 31 # Variable c_int '31'
BadAtom = 5 # Variable c_int '5'
RAND_MAX = 2147483647 # Variable c_int '2147483647'
XkbSA_NoAction = 0 # Variable c_int '0'
NeedVarargsPrototypes = 1 # Variable c_int '1'
CapButt = 1 # Variable c_int '1'
sz_xCopyAreaReq = 28 # Variable c_int '28'
XkbCompatNameMask = 32 # Variable c_int '32'
sz_xSetFontPathReq = 8 # Variable c_int '8'
XkbAllExtensionDeviceEventsMask = 32799 # Variable c_int '32799'
AllTemporary = 0 # Variable c_long '0l'
ESRMNT = 69 # Variable c_int '69'
X_MapWindow = 8 # Variable c_int '8'
_ISOC99_SOURCE = 1 # Variable c_int '1'
XkbControlsEnabledMask = 2147483648 # Variable c_long '2147483648l'
X_QueryKeymap = 44 # Variable c_int '44'
XkbCompatLookupModsMask = 4096 # Variable c_long '4096l'
X_KillClient = 113 # Variable c_int '113'
sz_xCreateGCReq = 16 # Variable c_int '16'
XkbSA_ISOAffectMask = 120 # Variable c_int '120'
ResizeRedirectMask = 262144 # Variable c_long '262144l'
RaiseLowest = 0 # Variable c_int '0'
X_CreatePixmap = 53 # Variable c_int '53'
XIMPreeditNothing = 8 # Variable c_long '8l'
DefaultBlanking = 2 # Variable c_int '2'
__timer_t_defined = 1 # Variable c_int '1'
XkbGBN_ServerSymbolsMask = 8 # Variable c_long '8l'
sz_xAllocNamedColorReq = 12 # Variable c_int '12'
XNPreeditDoneCallback = 'preeditDoneCallback' # Variable STRING '(const char*)"preeditDoneCallback"'
XkbLC_ControlFallback = 16 # Variable c_int '16'
X_GrabKey = 33 # Variable c_int '33'
GCTile = 1024 # Variable c_long '1024l'
sz_xGetGeometryReply = 32 # Variable c_int '32'
HostInsert = 0 # Variable c_int '0'
AutoRepeatModeDefault = 2 # Variable c_int '2'
XkbSA_MoveAbsoluteY = 4 # Variable c_long '4l'
XkbSA_MoveAbsoluteX = 2 # Variable c_long '2l'
_SIGSET_H_types = 1 # Variable c_int '1'
KBKeyClickPercent = 1 # Variable c_long '1l'
DontPreferBlanking = 0 # Variable c_int '0'
XkbPointerButtonMask = 8192 # Variable c_long '8192l'
GCDashList = 2097152 # Variable c_long '2097152l'
X_ListHosts = 110 # Variable c_int '110'
X_GetPointerMapping = 117 # Variable c_int '117'
CWBitGravity = 16 # Variable c_long '16l'
sz_xGetMotionEventsReply = 32 # Variable c_int '32'
EKEYREJECTED = 129 # Variable c_int '129'
NotifyDetailNone = 7 # Variable c_int '7'
BadLength = 16 # Variable c_int '16'
ENOTCONN = 107 # Variable c_int '107'
InputOnly = 2 # Variable c_int '2'
ENETUNREACH = 101 # Variable c_int '101'
CWEventMask = 2048 # Variable c_long '2048l'
sz_xChangePropertyReq = 24 # Variable c_int '24'
UnmapGravity = 0 # Variable c_int '0'
XkbSA_LockControls = 15 # Variable c_int '15'
MapNotify = 19 # Variable c_int '19'
XNStringConversion = 'stringConversion' # Variable STRING '(const char*)"stringConversion"'
sz_xQueryColorsReply = 32 # Variable c_int '32'
X_FillPoly = 69 # Variable c_int '69'
sz_xConnClientPrefix = 12 # Variable c_int '12'
XkbSA_SetControls = 14 # Variable c_int '14'
X_kbBell = 3 # Variable c_int '3'
XkbName = 'XKEYBOARD' # Variable STRING '(const char*)"XKEYBOARD"'
XkbOD_NonXkbServer = 3 # Variable c_int '3'
XkbSA_ISONoAffectMods = 64 # Variable c_long '64l'
XkbIM_UseAnyMods = 31 # Variable c_long '31l'
ButtonPressMask = 4 # Variable c_long '4l'
XkbSA_MessageGenKeyEvent = 4 # Variable c_long '4l'
X_GetAtomName = 17 # Variable c_int '17'
__SIZEOF_PTHREAD_RWLOCKATTR_T = 8 # Variable c_int '8'
XNStdColormap = 'stdColorMap' # Variable STRING '(const char*)"stdColorMap"'
sz_xResourceReq = 8 # Variable c_int '8'
_LARGEFILE64_SOURCE = 1 # Variable c_int '1'
EastGravity = 6 # Variable c_int '6'
ENOTBLK = 15 # Variable c_int '15'
XkbWrapIntoRange = 0 # Variable c_int '0'
__USE_ISOC11 = 1 # Variable c_int '1'
XkbLC_Partial = 4 # Variable c_long '4l'
X_GetFontPath = 52 # Variable c_int '52'
XIMStringConversionWord = 3 # Variable c_int '3'
ENOPKG = 65 # Variable c_int '65'
XkbBounceKeysMask = 4 # Variable c_long '4l'
LineDoubleDash = 2 # Variable c_int '2'
SyncBoth = 7 # Variable c_int '7'
ESTALE = 116 # Variable c_int '116'
X_ChangeHosts = 109 # Variable c_int '109'
XkbIM_LEDDrivesKB = 32 # Variable c_long '32l'
XkbSA_ISODfltIsGroup = 128 # Variable c_long '128l'
X_kbSetIndicatorMap = 14 # Variable c_int '14'
XkbAllClientInfoMask = 7 # Variable c_int '7'
XIMStringConversionTopEdge = 4 # Variable c_int '4'
XNDestroyCallback = 'destroyCallback' # Variable STRING '(const char*)"destroyCallback"'
XIMStringConversionChar = 4 # Variable c_int '4'
XkbUseCoreKbd = 256 # Variable c_int '256'
XkbComponentNamesMask = 63 # Variable c_int '63'
sz_xPolyFillArcReq = 12 # Variable c_int '12'
XkbAllRequiredTypes = 15 # Variable c_int '15'
__time_t_defined = 1 # Variable c_int '1'
XkbKeycodesNameMask = 1 # Variable c_int '1'
XkbGroup4Mask = 8 # Variable c_int '8'
sz_xFillPolyReq = 16 # Variable c_int '16'
SubstructureNotifyMask = 524288 # Variable c_long '524288l'
XkbModifierLatchMask = 4 # Variable c_long '4l'
ENOTUNIQ = 76 # Variable c_int '76'
XkbKeyAliasesMask = 1024 # Variable c_int '1024'
ELNRNG = 48 # Variable c_int '48'
ERESTART = 85 # Variable c_int '85'
BadRequest = 1 # Variable c_int '1'
XkbLC_ComposeLED = 1073741824 # Variable c_int '1073741824'
CWCursor = 16384 # Variable c_long '16384l'
Mod2MapIndex = 4 # Variable c_int '4'
X_GetSelectionOwner = 23 # Variable c_int '23'
ENOPROTOOPT = 92 # Variable c_int '92'
BadIDChoice = 14 # Variable c_int '14'
True_ = 1 # Variable c_int '1'
XNPreeditDrawCallback = 'preeditDrawCallback' # Variable STRING '(const char*)"preeditDrawCallback"'
X_CopyPlane = 63 # Variable c_int '63'
sz_xPolyRectangleReq = 12 # Variable c_int '12'
XNMissingCharSet = 'missingCharSet' # Variable STRING '(const char*)"missingCharSet"'
XkbGeometryMask = 32 # Variable c_long '32l'
XkbGeometryNameMask = 2 # Variable c_int '2'
XkbAXN_SKRelease = 3 # Variable c_int '3'
XkbKeypadIndex = 3 # Variable c_int '3'
XCONN_CHECK_FREQ = 256 # Variable c_int '256'
XNFocusWindow = 'focusWindow' # Variable STRING '(const char*)"focusWindow"'
GCCapStyle = 64 # Variable c_long '64l'
Button1Mask = 256 # Variable c_int '256'
X_kbSelectEvents = 1 # Variable c_int '1'
CWDontPropagate = 4096 # Variable c_long '4096l'
XkbRedirectIntoRange = 128 # Variable c_int '128'
XNInputStyle = 'inputStyle' # Variable STRING '(const char*)"inputStyle"'
ELIBACC = 79 # Variable c_int '79'
SelectionClear = 29 # Variable c_int '29'
XkbControlsNotifyMask = 8 # Variable c_long '8l'
WestGravity = 4 # Variable c_int '4'
ButtonReleaseMask = 8 # Variable c_long '8l'
FocusIn = 9 # Variable c_int '9'
FontRightToLeft = 1 # Variable c_int '1'
sz_xUngrabKeyReq = 12 # Variable c_int '12'
__WALL = 1073741824 # Variable c_int '1073741824'
ENOTDIR = 20 # Variable c_int '20'
GCLineWidth = 16 # Variable c_long '16l'
CWBackingPixel = 256 # Variable c_long '256l'
XNFontSet = 'fontSet' # Variable STRING '(const char*)"fontSet"'
XkbSA_SetValRelative = 64 # Variable c_int '64'
CWStackMode = 64 # Variable c_int '64'
XkbSA_SwitchApplication = 1 # Variable c_long '1l'
XkbGBN_SymbolsMask = 12 # Variable c_long '12l'
sz_xGetImageReply = 32 # Variable c_int '32'
XkbDF_DisableLocks = 1 # Variable c_int '1'
XkbSI_Exactly = 4 # Variable c_int '4'
XkbLC_KeypadKeys = 1024 # Variable c_long '1024l'
XkbAnyGroupMask = 128 # Variable c_int '128'
Always = 2 # Variable c_int '2'
XIMStatusNothing = 1024 # Variable c_long '1024l'
FUNCPROTO = 15 # Variable c_int '15'
DestroyNotify = 17 # Variable c_int '17'
GCFillRule = 512 # Variable c_long '512l'
XkbSA_UseDfltButton = 0 # Variable c_int '0'
GCArcMode = 4194304 # Variable c_long '4194304l'
ColormapUninstalled = 0 # Variable c_int '0'
EINVAL = 22 # Variable c_int '22'
XkbAnyActionDataSize = 7 # Variable c_int '7'
XkbPerKeyBitArraySize = 32 # Variable c_int '32'
SubstructureRedirectMask = 1048576 # Variable c_long '1048576l'
XkbOverlay2Mask = 2048 # Variable c_long '2048l'
EHOSTUNREACH = 113 # Variable c_int '113'
XkbActionMessage = 9 # Variable c_int '9'
XkbSA_NumActions = 21 # Variable c_int '21'
sz_xQueryTreeReply = 32 # Variable c_int '32'
sz_xAllocColorPlanesReply = 32 # Variable c_int '32'
XkbMouseKeysMask = 16 # Variable c_long '16l'
XkbVirtualModsMask = 64 # Variable c_int '64'
XIMVisibleToBackword = 512 # Variable c_long '512l'
sz_xHostEntry = 4 # Variable c_int '4'
XkbMaxRedirectCount = 8 # Variable c_int '8'
XkbKeyBehaviorsMask = 32 # Variable c_int '32'
XkbKTLevelNamesMask = 128 # Variable c_int '128'
XkbAllXIIds = 1536 # Variable c_int '1536'
XkbNKN_DeviceIDMask = 4 # Variable c_long '4l'
X_kbGetNames = 17 # Variable c_int '17'
XkbUseCorePtr = 512 # Variable c_int '512'
X_CopyArea = 62 # Variable c_int '62'
XkbAccessXOptionsMask = 264 # Variable c_long '264l'
EOPNOTSUPP = 95 # Variable c_int '95'
YXBanded = 3 # Variable c_int '3'
XkbVirtualModMapMask = 128 # Variable c_int '128'
DisableScreenSaver = 0 # Variable c_int '0'
XNStringConversionCallback = 'stringConversionCallback' # Variable STRING '(const char*)"stringConversionCallback"'
__USE_POSIX = 1 # Variable c_int '1'
XkbOneLevelIndex = 0 # Variable c_int '0'
IncludeInferiors = 1 # Variable c_int '1'
X_CloseFont = 46 # Variable c_int '46'
XkbCompatMapNotifyMask = 128 # Variable c_long '128l'
UNLOCKED = 0 # Variable c_int '0'
sz_xCreatePixmapReq = 16 # Variable c_int '16'
__clockid_t_defined = 1 # Variable c_int '1'
GXcopyInverted = 12 # Variable c_int '12'
XkbGBN_KeyNamesMask = 32 # Variable c_long '32l'
BadMatch = 8 # Variable c_int '8'
EREMOTE = 66 # Variable c_int '66'
XIMPreeditUnKnown = 0 # Variable c_long '0l'
__WORDSIZE_TIME64_COMPAT32 = 1 # Variable c_int '1'
AnyButton = 0 # Variable c_long '0l'
_SYS_TYPES_H = 1 # Variable c_int '1'
XkbGroupCompatMask = 2 # Variable c_int '2'
__USE_GNU = 1 # Variable c_int '1'
sz_xGetImageReq = 20 # Variable c_int '20'
WUNTRACED = 2 # Variable c_int '2'
sz_xGetWindowAttributesReply = 44 # Variable c_int '44'
XkbMaxShiftLevel = 63 # Variable c_int '63'
XkbAllControlsMask = 4160757759 # Variable c_uint '4160757759u'
XIMVisibleToCenter = 1024 # Variable c_long '1024l'
SyncPointer = 1 # Variable c_int '1'
PlaceOnBottom = 1 # Variable c_int '1'
_STDLIB_H = 1 # Variable c_int '1'
__ldiv_t_defined = 1 # Variable c_int '1'
XkbInternalModsMask = 268435456 # Variable c_long '268435456l'
NoExpose = 14 # Variable c_int '14'
X_DestroySubwindows = 5 # Variable c_int '5'
CreateNotify = 16 # Variable c_int '16'
GCGraphicsExposures = 65536 # Variable c_long '65536l'
ReparentNotify = 21 # Variable c_int '21'
XkbGroupNamesMask = 4096 # Variable c_int '4096'
sz_xWarpPointerReq = 24 # Variable c_int '24'
XLookupNone = 1 # Variable c_int '1'
sz_xPolySegmentReq = 12 # Variable c_int '12'
GCSubwindowMode = 32768 # Variable c_long '32768l'
XkbNumVirtualMods = 16 # Variable c_int '16'
DontAllowExposures = 0 # Variable c_int '0'
XkbKB_RadioGroup = 2 # Variable c_int '2'
X_kbListComponents = 22 # Variable c_int '22'
sz_xStoreNamedColorReq = 16 # Variable c_int '16'
GrabModeAsync = 1 # Variable c_int '1'
AllowExposures = 1 # Variable c_int '1'
IsUnviewable = 1 # Variable c_int '1'
CWWinGravity = 32 # Variable c_long '32l'
FirstExtensionError = 128 # Variable c_int '128'
LastExtensionError = 255 # Variable c_int '255'
WNOWAIT = 16777216 # Variable c_int '16777216'
PropertyDelete = 1 # Variable c_int '1'
X_GrabButton = 28 # Variable c_int '28'
SouthEastGravity = 9 # Variable c_int '9'
XkbMaxKbdGroup = 3 # Variable c_int '3'
XIMStringConversionBottomEdge = 8 # Variable c_int '8'
EHWPOISON = 133 # Variable c_int '133'
XIMInitialState = 1 # Variable c_long '1l'
X_UnmapSubwindows = 11 # Variable c_int '11'
IsUnmapped = 0 # Variable c_int '0'
QueuedAfterFlush = 2 # Variable c_int '2'
XkbXI_UnsupportedFeatureMask = 32768 # Variable c_long '32768l'
AsyncPointer = 0 # Variable c_int '0'
XkbSA_PtrBtn = 8 # Variable c_int '8'
ConfigureRequest = 23 # Variable c_int '23'
sz_xCopyGCReq = 16 # Variable c_int '16'
XkbSA_LockPtrBtn = 9 # Variable c_int '9'
XkbServerMapMask = 2 # Variable c_long '2l'
__FD_ZERO_STOS = 'stosq' # Variable STRING '(const char*)"stosq"'
DirectColor = 5 # Variable c_int '5'
sz_xTextElt = 2 # Variable c_int '2'
CWBackingStore = 64 # Variable c_long '64l'
XkbExtensionDeviceNotify = 11 # Variable c_int '11'
X_ChangeWindowAttributes = 2 # Variable c_int '2'
ECONNRESET = 104 # Variable c_int '104'
XNPreeditStateNotifyCallback = 'preeditStateNotifyCallback' # Variable STRING '(const char*)"preeditStateNotifyCallback"'
X_ChangeActivePointerGrab = 30 # Variable c_int '30'
GXnoop = 5 # Variable c_int '5'
XkbAllComponentsMask = 127 # Variable c_int '127'
Mod4MapIndex = 6 # Variable c_int '6'
ButtonRelease = 5 # Variable c_int '5'
CoordModePrevious = 1 # Variable c_int '1'
XkbAccessXTimeoutMask = 128 # Variable c_long '128l'
LeaveNotify = 8 # Variable c_int '8'
sz_xUngrabButtonReq = 12 # Variable c_int '12'
ScreenSaverReset = 0 # Variable c_int '0'
Mod1Mask = 8 # Variable c_int '8'
X_kbGetCompatMap = 10 # Variable c_int '10'
sz_xQueryBestSizeReply = 32 # Variable c_int '32'
sz_xColorItem = 12 # Variable c_int '12'
X_CreateGC = 55 # Variable c_int '55'
XlibDisplayClosing = 2 # Variable c_long '2l'
ELFlagFocus = 1 # Variable c_int '1'
NotifyNormal = 0 # Variable c_int '0'
X_SetPointerMapping = 116 # Variable c_int '116'
GCClipYOrigin = 262144 # Variable c_long '262144l'
X_ListFontsWithInfo = 50 # Variable c_int '50'
HostDelete = 1 # Variable c_int '1'
XIMTertiary = 128 # Variable c_long '128l'
GXor = 7 # Variable c_int '7'
XkbRepeatKeysMask = 1 # Variable c_long '1l'
XkbExplicitKeyType2Mask = 2 # Variable c_int '2'
ECHILD = 10 # Variable c_int '10'
__USE_XOPEN2K = 1 # Variable c_int '1'
VisibilityUnobscured = 0 # Variable c_int '0'
XNHotKey = 'hotKey' # Variable STRING '(const char*)"hotKey"'
KeyPressMask = 1 # Variable c_long '1l'
sz_xChangeActivePointerGrabReq = 16 # Variable c_int '16'
__PTHREAD_RWLOCK_INT_FLAGS_SHARED = 1 # Variable c_int '1'
NotifyUngrab = 2 # Variable c_int '2'
sz_xRotatePropertiesReq = 12 # Variable c_int '12'
AlreadyGrabbed = 1 # Variable c_int '1'
BadGC = 13 # Variable c_int '13'
XIMHighlight = 4 # Variable c_long '4l'
PropModeAppend = 2 # Variable c_int '2'
XkbAllXIClasses = 1280 # Variable c_int '1280'
XkbAllExplicitMask = 255 # Variable c_int '255'
XNForeground = 'foreground' # Variable STRING '(const char*)"foreground"'
XkbSA_LockNoLock = 1 # Variable c_long '1l'
sz_xChangeKeyboardMappingReq = 8 # Variable c_int '8'
XkbIM_NoAutomatic = 64 # Variable c_long '64l'
__OFF_T_MATCHES_OFF64_T = 1 # Variable c_int '1'
XkbIndicatorStateNotify = 4 # Variable c_int '4'
GCPlaneMask = 2 # Variable c_long '2l'
XkbNumModifiers = 8 # Variable c_int '8'
Button3Mask = 1024 # Variable c_int '1024'
XkbExtensionDeviceNotifyMask = 2048 # Variable c_long '2048l'
XkbAX_FeatureFBMask = 4 # Variable c_long '4l'
XkbSA_SetValAbsolute = 80 # Variable c_int '80'
XkbPCF_GrabsUseXKBStateMask = 2 # Variable c_long '2l'
X_GetGeometry = 14 # Variable c_int '14'
_STRING_H = 1 # Variable c_int '1'
NotifyNonlinearVirtual = 4 # Variable c_int '4'
XkbGBN_OtherNamesMask = 128 # Variable c_long '128l'
sz_xGetPointerMappingReply = 32 # Variable c_int '32'
XNPreeditCaretCallback = 'preeditCaretCallback' # Variable STRING '(const char*)"preeditCaretCallback"'
XlibDisplayWriting = 64 # Variable c_long '64l'
XkbAllRadioGroupsMask = 4294967295 # Variable c_uint '4294967295u'
__ENUM_IDTYPE_T = 1 # Variable c_int '1'
Mod1MapIndex = 3 # Variable c_int '3'
XkbNamesNotify = 6 # Variable c_int '6'
sz_xListFontsReply = 32 # Variable c_int '32'
NoEventMask = 0 # Variable c_long '0l'
XkbStickyKeysMask = 8 # Variable c_long '8l'
XNPreeditStartCallback = 'preeditStartCallback' # Variable STRING '(const char*)"preeditStartCallback"'
X_CirculateWindow = 13 # Variable c_int '13'
NorthWestGravity = 1 # Variable c_int '1'
sz_xImageText16Req = 16 # Variable c_int '16'
X_StoreColors = 89 # Variable c_int '89'
NeedFunctionPrototypes = 1 # Variable c_int '1'
__LITTLE_ENDIAN = 1234 # Variable c_int '1234'
__have_pthread_attr_t = 1 # Variable c_int '1'
PseudoColor = 3 # Variable c_int '3'
XIMPreeditNone = 16 # Variable c_long '16l'
XkbNoShape = 255 # Variable c_int '255'
XkbSA_SetValMax = 48 # Variable c_int '48'
X_PolySegment = 66 # Variable c_int '66'
XkbAX_TwoKeysMask = 64 # Variable c_long '64l'
X_SetScreenSaver = 107 # Variable c_int '107'
XkbSA_DeviceValuator = 20 # Variable c_int '20'
X_ChangePointerControl = 105 # Variable c_int '105'
XNStatusStartCallback = 'statusStartCallback' # Variable STRING '(const char*)"statusStartCallback"'
BadCursor = 6 # Variable c_int '6'
XkbGroup1Mask = 1 # Variable c_int '1'
CWHeight = 8 # Variable c_int '8'
X_DeleteProperty = 19 # Variable c_int '19'
XIMPreeditEnable = 1 # Variable c_long '1l'
sz_xCreateWindowReq = 32 # Variable c_int '32'
X_PolyLine = 65 # Variable c_int '65'
_BITS_PTHREADTYPES_H = 1 # Variable c_int '1'
SetModeInsert = 0 # Variable c_int '0'
sz_xEvent = 32 # Variable c_int '32'
KBAutoRepeatMode = 128 # Variable c_long '128l'
X_kbGetKbdByName = 23 # Variable c_int '23'
sz_xSetModifierMappingReply = 32 # Variable c_int '32'
XkbAXN_SKReject = 2 # Variable c_int '2'
XkbAXN_BKAcceptMask = 16 # Variable c_long '16l'
GXorInverted = 13 # Variable c_int '13'
XkbGBN_TypesMask = 1 # Variable c_long '1l'
FillSolid = 0 # Variable c_int '0'
XkbAllAccessXEventsMask = 127 # Variable c_int '127'
XkbAXN_SKPressMask = 1 # Variable c_long '1l'
ControlMapIndex = 2 # Variable c_int '2'
sz_xVisualType = 24 # Variable c_int '24'
ENOSPC = 28 # Variable c_int '28'
EBADMSG = 74 # Variable c_int '74'
X_DestroyWindow = 4 # Variable c_int '4'
ELIBBAD = 80 # Variable c_int '80'
X_UninstallColormap = 82 # Variable c_int '82'
X_ClearArea = 61 # Variable c_int '61'
ERANGE = 34 # Variable c_int '34'
Button4MotionMask = 2048 # Variable c_long '2048l'
sz_xQueryPointerReply = 32 # Variable c_int '32'
StippleShape = 2 # Variable c_int '2'
_X11_XLIBINT_H_ = 1 # Variable c_int '1'
XkbGroup1Index = 0 # Variable c_int '0'
PTSPERBATCH = 1024 # Variable c_int '1024'
BadFont = 7 # Variable c_int '7'
XkbOD_Success = 0 # Variable c_int '0'
InputOutput = 1 # Variable c_int '1'
XkbSA_LatchToLock = 2 # Variable c_long '2l'
EUSERS = 87 # Variable c_int '87'
ENODEV = 19 # Variable c_int '19'
X_kbGetGeometry = 19 # Variable c_int '19'
X_GetKeyboardMapping = 101 # Variable c_int '101'
_ERRNO_H = 1 # Variable c_int '1'
__SIZEOF_PTHREAD_MUTEX_T = 40 # Variable c_int '40'
XkbPhysSymbolsNameMask = 8 # Variable c_int '8'
XkbAllStateComponentsMask = 16383 # Variable c_int '16383'
Opposite = 4 # Variable c_int '4'
X_Reply = 1 # Variable c_int '1'
XkbCompatStateMask = 256 # Variable c_long '256l'
XkbMapNotify = 1 # Variable c_int '1'
XkbOD_BadLibraryVersion = 1 # Variable c_int '1'
CursorShape = 0 # Variable c_int '0'
XkbBellNotifyMask = 256 # Variable c_long '256l'
ESHUTDOWN = 108 # Variable c_int '108'
UnmapNotify = 18 # Variable c_int '18'
XIMStringConversionBuffer = 1 # Variable c_int '1'
sz_xRecolorCursorReq = 20 # Variable c_int '20'
XkbIndicatorMapNotify = 5 # Variable c_int '5'
GXset = 15 # Variable c_int '15'
ECONNREFUSED = 111 # Variable c_int '111'
sz_xCharInfo = 12 # Variable c_int '12'
RevertToPointerRoot = 1 # Variable c_int '1'
ENOEXEC = 8 # Variable c_int '8'
EBADF = 9 # Variable c_int '9'
EBADE = 52 # Variable c_int '52'
XNResetState = 'resetState' # Variable STRING '(const char*)"resetState"'
XkbKeyboard = 0 # Variable c_int '0'
__PDP_ENDIAN = 3412 # Variable c_int '3412'
EBADR = 53 # Variable c_int '53'
sz_xArc = 12 # Variable c_int '12'
EXDEV = 18 # Variable c_int '18'
XkbNoModifier = 255 # Variable c_int '255'
QueuedAfterReading = 1 # Variable c_int '1'
_SIGSET_NWORDS = 16 # Variable c_ulong '16ul'
XkbPerKeyRepeatMask = 1073741824 # Variable c_long '1073741824l'
X_GetScreenSaver = 108 # Variable c_int '108'
XkbIM_UseEffective = 8 # Variable c_long '8l'
AnyPropertyType = 0 # Variable c_long '0l'
KeyPress = 2 # Variable c_int '2'
sz_xPolyText8Req = 16 # Variable c_int '16'
NotifyNonlinear = 3 # Variable c_int '3'
GXclear = 0 # Variable c_int '0'
XkbMouseKeysAccelMask = 32 # Variable c_long '32l'
XNFilterEvents = 'filterEvents' # Variable STRING '(const char*)"filterEvents"'
ETOOMANYREFS = 109 # Variable c_int '109'
JoinRound = 1 # Variable c_int '1'
XkbAXN_AXKWarningMask = 64 # Variable c_long '64l'
sz_xChangePointerControlReq = 12 # Variable c_int '12'
PropertyNewValue = 0 # Variable c_int '0'
X_UngrabServer = 37 # Variable c_int '37'
XkbKeySymsMask = 2 # Variable c_int '2'
__WCOREFLAG = 128 # Variable c_int '128'
EINPROGRESS = 115 # Variable c_int '115'
XkbSA_SetMods = 1 # Variable c_int '1'
XkbErr_BadDevice = 255 # Variable c_int '255'
sz_xGrabButtonReq = 24 # Variable c_int '24'
sz_xListFontsReq = 8 # Variable c_int '8'
EL3RST = 47 # Variable c_int '47'
__SIZEOF_PTHREAD_MUTEXATTR_T = 4 # Variable c_int '4'
_POSIX_SOURCE = 1 # Variable c_int '1'
BadName = 15 # Variable c_int '15'
XkbPCF_AllFlagsMask = 31 # Variable c_int '31'
XkbAccessXKeysMask = 64 # Variable c_long '64l'
X_CreateColormap = 78 # Variable c_int '78'
GXinvert = 10 # Variable c_int '10'
OwnerGrabButtonMask = 16777216 # Variable c_long '16777216l'
GCLastBit = 22 # Variable c_int '22'
BadImplementation = 17 # Variable c_int '17'
X_kbUseExtension = 0 # Variable c_int '0'
XNBackgroundPixmap = 'backgroundPixmap' # Variable STRING '(const char*)"backgroundPixmap"'
NeedNestedPrototypes = 1 # Variable c_int '1'
DoGreen = 2 # Variable c_int '2'
sz_xListHostsReq = 4 # Variable c_int '4'
CoordModeOrigin = 0 # Variable c_int '0'
XkbNamesMask = 16 # Variable c_long '16l'
X_PutImage = 72 # Variable c_int '72'
XkbModifierMapMask = 4 # Variable c_int '4'
XkbAccessXFeedbackMask = 256 # Variable c_long '256l'
sz_xListFontsWithInfoReq = 8 # Variable c_int '8'
XkbAX_SKRejectFBMask = 512 # Variable c_long '512l'
NorthGravity = 2 # Variable c_int '2'
GCTileStipXOrigin = 4096 # Variable c_long '4096l'
BUFSIZE = 2048 # Variable c_int '2048'
ERFKILL = 132 # Variable c_int '132'
X_PROTOCOL_REVISION = 0 # Variable c_int '0'
WhenMapped = 1 # Variable c_int '1'
X_NoOperation = 127 # Variable c_int '127'
CirculateNotify = 26 # Variable c_int '26'
X_CreateGlyphCursor = 94 # Variable c_int '94'
sz_xChangeSaveSetReq = 8 # Variable c_int '8'
X_kbSetMap = 9 # Variable c_int '9'
X_AllocColorPlanes = 87 # Variable c_int '87'
XkbNewKeyboardNotify = 0 # Variable c_int '0'
XkbGBN_IndicatorMapMask = 16 # Variable c_long '16l'
_ENDIAN_H = 1 # Variable c_int '1'
sz_xListHostsReply = 32 # Variable c_int '32'
XkbSA_SetValCenter = 32 # Variable c_int '32'
__USE_FORTIFY_LEVEL = 2 # Variable c_int '2'
XkbIndicatorMapNotifyMask = 32 # Variable c_long '32l'
XkbSA_LockGroup = 6 # Variable c_int '6'
sz_xReq = 4 # Variable c_int '4'
XkbAX_SlowWarnFBMask = 8 # Variable c_long '8l'
XkbSI_AutoRepeat = 1 # Variable c_int '1'
XkbAllIndicatorsMask = 4294967295 # Variable c_uint '4294967295u'
XNBaseFontName = 'baseFontName' # Variable STRING '(const char*)"baseFontName"'
GravityNotify = 24 # Variable c_int '24'
sz_xGetKeyboardControlReply = 52 # Variable c_int '52'
XkbLC_FunctionKeys = 2048 # Variable c_long '2048l'
XNPreeditAttributes = 'preeditAttributes' # Variable STRING '(const char*)"preeditAttributes"'
XkbExplicitBehaviorMask = 64 # Variable c_int '64'
GrabSuccess = 0 # Variable c_int '0'
Button5Mask = 4096 # Variable c_int '4096'
FocusChangeMask = 2097152 # Variable c_long '2097152l'
XkbTypesNameMask = 16 # Variable c_int '16'
XkbLC_ConsumeLookupMods = 2 # Variable c_int '2'
sz_xListFontsWithInfoReply = 60 # Variable c_int '60'
EAFNOSUPPORT = 97 # Variable c_int '97'
XkbLC_AllControls = 3221225503 # Variable c_uint '3221225503u'
WLNSPERBATCH = 50 # Variable c_int '50'
X_GetWindowAttributes = 3 # Variable c_int '3'
BadWindow = 3 # Variable c_int '3'
X_kbSetControls = 7 # Variable c_int '7'
NotifyGrab = 1 # Variable c_int '1'
AllocAll = 1 # Variable c_int '1'
sz_xRectangle = 8 # Variable c_int '8'
XkbKeypadMask = 8 # Variable c_int '8'
ENOCSI = 50 # Variable c_int '50'
NeedWidePrototypes = 0 # Variable c_int '0'
__STDLIB_MB_LEN_MAX = 16 # Variable c_int '16'
__WCLONE = 2147483648 # Variable c_uint '2147483648u'
sz_xError = 32 # Variable c_int '32'
XNClientWindow = 'clientWindow' # Variable STRING '(const char*)"clientWindow"'
EAGAIN = 11 # Variable c_int '11'
__error_t_defined = 1 # Variable c_int '1'
X_kbGetState = 4 # Variable c_int '4'
FamilyChaos = 2 # Variable c_int '2'
sz_xSetInputFocusReq = 12 # Variable c_int '12'
ELIBEXEC = 83 # Variable c_int '83'
XkbMinLegalKeyCode = 8 # Variable c_int '8'
X_HAVE_UTF8_STRING = 1 # Variable c_int '1'
XNQueryOrientation = 'queryOrientation' # Variable STRING '(const char*)"queryOrientation"'
XkbSA_UseModMapMods = 4 # Variable c_long '4l'
sz_xConnSetup = 32 # Variable c_int '32'
XkbLC_BeepOnComposeFail = -2147483648 # Variable c_int '-0x00000000080000000'
sz_xLookupColorReply = 32 # Variable c_int '32'
XkbOD_ConnectionRefused = 2 # Variable c_int '2'
X_CreateWindow = 1 # Variable c_int '1'
XkbNumRequiredTypes = 4 # Variable c_int '4'
VisibilityChangeMask = 65536 # Variable c_long '65536l'
XkbSA_ValOpMask = 112 # Variable c_int '112'
XLookupChars = 2 # Variable c_int '2'
EDESTADDRREQ = 89 # Variable c_int '89'
sz_xClearAreaReq = 16 # Variable c_int '16'
KeyReleaseMask = 2 # Variable c_long '2l'
Complex = 0 # Variable c_int '0'
sz_xSetDashesReq = 12 # Variable c_int '12'
EPROTOTYPE = 91 # Variable c_int '91'
XkbExplicitKeyType3Mask = 4 # Variable c_int '4'
X_GetInputFocus = 43 # Variable c_int '43'
XIMStringConversionRetrieval = 2 # Variable c_int '2'
X_LookupColor = 92 # Variable c_int '92'
__GLIBC_MINOR__ = 19 # Variable c_int '19'
XIMStringConversionRightEdge = 2 # Variable c_int '2'
XkbLC_AlphanumericKeys = 256 # Variable c_long '256l'
CWBorderPixmap = 4 # Variable c_long '4l'
XkbNumKbdGroups = 4 # Variable c_int '4'
None_ = 0 # Variable c_long '0l'
X_AllocColorCells = 86 # Variable c_int '86'
XkbMaxRadioGroups = 32 # Variable c_int '32'
DisableScreenInterval = 0 # Variable c_int '0'
FamilyServerInterpreted = 5 # Variable c_int '5'
X_UngrabButton = 29 # Variable c_int '29'
GXxor = 6 # Variable c_int '6'
XkbKB_RGAllowNone = 128 # Variable c_int '128'
XIMSecondary = 64 # Variable c_long '64l'
sz_xPolyArcReq = 12 # Variable c_int '12'
GXnor = 8 # Variable c_int '8'
GCClipMask = 524288 # Variable c_long '524288l'
XNResourceClass = 'resourceClass' # Variable STRING '(const char*)"resourceClass"'
sz_xGrabKeyReq = 16 # Variable c_int '16'
GCStipple = 2048 # Variable c_long '2048l'
XkbKB_Default = 0 # Variable c_int '0'
XkbAXN_SKRejectMask = 4 # Variable c_long '4l'
EFAULT = 14 # Variable c_int '14'
ENOKEY = 126 # Variable c_int '126'
sz_xAllocColorPlanesReq = 16 # Variable c_int '16'
ENODATA = 61 # Variable c_int '61'
XlibSpecificationRelease = 6 # Variable c_int '6'
VisibilityPartiallyObscured = 1 # Variable c_int '1'
XkbLC_IgnoreNewKeyboards = 8 # Variable c_int '8'
LedModeOn = 1 # Variable c_int '1'
X_CopyColormapAndFree = 80 # Variable c_int '80'
X_SendEvent = 25 # Variable c_int '25'
Button5MotionMask = 4096 # Variable c_long '4096l'
_FEATURES_H = 1 # Variable c_int '1'
X_QueryPointer = 38 # Variable c_int '38'
AsyncBoth = 6 # Variable c_int '6'
X_GrabServer = 36 # Variable c_int '36'
sz_xListExtensionsReply = 32 # Variable c_int '32'
X_GrabKeyboard = 31 # Variable c_int '31'
PropertyChangeMask = 4194304 # Variable c_long '4194304l'
KeyRelease = 3 # Variable c_int '3'
XkbLC_ForceLatin1Lookup = 1 # Variable c_int '1'
XkbAX_AllOptionsMask = 4095 # Variable c_int '4095'
EPFNOSUPPORT = 96 # Variable c_int '96'
ConfigureNotify = 22 # Variable c_int '22'
XkbSA_ISONoAffectCtrls = 8 # Variable c_long '8l'
XkbSA_AffectDfltBtn = 1 # Variable c_int '1'
XkbSymInterpMask = 1 # Variable c_int '1'
XkbGroup3Mask = 4 # Variable c_int '4'
X_QueryExtension = 98 # Variable c_int '98'
ShiftMask = 1 # Variable c_int '1'
MappingModifier = 0 # Variable c_int '0'
EL2NSYNC = 45 # Variable c_int '45'
FillTiled = 1 # Variable c_int '1'
LedModeOff = 0 # Variable c_int '0'
MappingNotify = 34 # Variable c_int '34'
sz_xrgb = 8 # Variable c_int '8'
XYBitmap = 0 # Variable c_int '0'
ESTRPIPE = 86 # Variable c_int '86'
CWColormap = 8192 # Variable c_long '8192l'
Mod3Mask = 32 # Variable c_int '32'
XkbGBN_AllComponentsMask = 255 # Variable c_int '255'
EDEADLK = 35 # Variable c_int '35'
FamilyInternet6 = 6 # Variable c_int '6'
JoinBevel = 2 # Variable c_int '2'
XkbModifierLockMask = 8 # Variable c_long '8l'
ControlMask = 4 # Variable c_int '4'
XkbSA_ISOLock = 11 # Variable c_int '11'
XkbAXN_BKReject = 5 # Variable c_int '5'
X_CreateCursor = 93 # Variable c_int '93'
XkbXI_IndicatorNamesMask = 4 # Variable c_long '4l'
XIMStringConversionLine = 2 # Variable c_int '2'
ScreenSaverActive = 1 # Variable c_int '1'
GrabNotViewable = 3 # Variable c_int '3'
ExposureMask = 32768 # Variable c_long '32768l'
XLookupKeySym = 3 # Variable c_int '3'
__USE_LARGEFILE = 1 # Variable c_int '1'
XkbSA_DeviceBtn = 18 # Variable c_int '18'
XkbSA_MovePtr = 7 # Variable c_int '7'
MappingBusy = 1 # Variable c_int '1'
XkbIndicatorStateNotifyMask = 16 # Variable c_long '16l'
XkbKB_Overlay1 = 3 # Variable c_int '3'
XkbKB_Overlay2 = 4 # Variable c_int '4'
SelectionRequest = 30 # Variable c_int '30'
X_FreeColormap = 79 # Variable c_int '79'
sz_xAllowEventsReq = 8 # Variable c_int '8'
__SIZEOF_PTHREAD_BARRIER_T = 32 # Variable c_int '32'
XIMPreeditDisable = 2 # Variable c_long '2l'
XkbAllEventsMask = 4095 # Variable c_int '4095'
sz_xGetInputFocusReply = 32 # Variable c_int '32'
__timespec_defined = 1 # Variable c_int '1'
_STRUCT_TIMEVAL = 1 # Variable c_int '1'
XkbDfltXIClass = 768 # Variable c_int '768'
XkbGroupLatchMask = 64 # Variable c_long '64l'
CirculateRequest = 27 # Variable c_int '27'
BadDrawable = 9 # Variable c_int '9'
__SIZEOF_PTHREAD_BARRIERATTR_T = 4 # Variable c_int '4'
SouthWestGravity = 7 # Variable c_int '7'
XkbAllVirtualModsMask = 65535 # Variable c_int '65535'
XkbModifierBaseMask = 2 # Variable c_long '2l'
X_ConfigureWindow = 12 # Variable c_int '12'
ENFILE = 23 # Variable c_int '23'
EREMCHG = 78 # Variable c_int '78'
__BIT_TYPES_DEFINED__ = 1 # Variable c_int '1'
X_kbGetControls = 6 # Variable c_int '6'
X_SetDashes = 58 # Variable c_int '58'
XkbNKN_GeometryMask = 2 # Variable c_long '2l'
XkbMaxLegalKeyCode = 255 # Variable c_int '255'
ENOMEM = 12 # Variable c_int '12'
X_ListProperties = 21 # Variable c_int '21'
EOWNERDEAD = 130 # Variable c_int '130'
GCFillStyle = 256 # Variable c_long '256l'
CapProjecting = 3 # Variable c_int '3'
AnyKey = 0 # Variable c_long '0l'
XkbAX_IndicatorFBMask = 16 # Variable c_long '16l'
XkbAllModifiersMask = 255 # Variable c_int '255'
GrabModeSync = 0 # Variable c_int '0'
sz_xSetCloseDownModeReq = 4 # Variable c_int '4'
X_kbGetNamedIndicator = 15 # Variable c_int '15'
KBLedMode = 32 # Variable c_long '32l'
XkbKB_Lock = 1 # Variable c_int '1'
PreferBlanking = 1 # Variable c_int '1'
EIO = 5 # Variable c_int '5'
sz_xInternAtomReq = 8 # Variable c_int '8'
GXcopy = 3 # Variable c_int '3'
XIMStringConversionConcealed = 16 # Variable c_int '16'
_SYS_CDEFS_H = 1 # Variable c_int '1'
sz_xSetPointerMappingReply = 32 # Variable c_int '32'
XkbGroup4Index = 3 # Variable c_int '3'
sz_xQueryExtensionReq = 8 # Variable c_int '8'
XkbSI_AnyOfOrNone = 1 # Variable c_int '1'
XkbGeomMaxLabelColors = 3 # Variable c_int '3'
XkbPCF_SendEventUsesXKBState = 16 # Variable c_long '16l'
YSorted = 1 # Variable c_int '1'
_LARGEFILE_SOURCE = 1 # Variable c_int '1'
X_kbGetIndicatorMap = 13 # Variable c_int '13'
XkbTwoLevelIndex = 1 # Variable c_int '1'
XkbSA_ISONoAffectGroup = 32 # Variable c_long '32l'
XkbExplicitVModMapMask = 128 # Variable c_int '128'
FillStippled = 2 # Variable c_int '2'
CenterGravity = 5 # Variable c_int '5'
XkbMaxMouseKeysBtn = 4 # Variable c_int '4'
XkbSA_LockDeviceBtn = 19 # Variable c_int '19'
XNBackground = 'background' # Variable STRING '(const char*)"background"'
XMD_H = 1 # Variable c_int '1'
NotUseful = 0 # Variable c_int '0'
GXequiv = 9 # Variable c_int '9'
RevertToNone = 0 # Variable c_int '0'
ENOLCK = 37 # Variable c_int '37'
XkbSA_ValScaleMask = 7 # Variable c_int '7'
KBLed = 16 # Variable c_long '16l'
Mod4Mask = 64 # Variable c_int '64'
Button3 = 3 # Variable c_int '3'
Button2 = 2 # Variable c_int '2'
Button1 = 1 # Variable c_int '1'
XkbXI_IndicatorsMask = 28 # Variable c_int '28'
Button5 = 5 # Variable c_int '5'
Button4 = 4 # Variable c_int '4'
X_SetModifierMapping = 118 # Variable c_int '118'
sz_xChangeModeReq = 4 # Variable c_int '4'
XkbSI_AnyOf = 2 # Variable c_int '2'
sz_xPolyPointReq = 12 # Variable c_int '12'
X_SetClipRectangles = 59 # Variable c_int '59'
ClientMessage = 33 # Variable c_int '33'
GCBackground = 8 # Variable c_long '8l'
FillOpaqueStippled = 3 # Variable c_int '3'
AutoRepeatModeOff = 0 # Variable c_int '0'
GrabFrozen = 4 # Variable c_int '4'
sz_xSetPointerMappingReq = 4 # Variable c_int '4'
X_PolyText16 = 75 # Variable c_int '75'
GXandInverted = 4 # Variable c_int '4'
XkbSlowKeysMask = 2 # Variable c_long '2l'
sz_xGetKeyboardMappingReq = 8 # Variable c_int '8'
RetainPermanent = 1 # Variable c_int '1'
XNQueryICValuesList = 'queryICValuesList' # Variable STRING '(const char*)"queryICValuesList"'
sz_xTranslateCoordsReply = 32 # Variable c_int '32'
XNOrientation = 'orientation' # Variable STRING '(const char*)"orientation"'
CWBackPixel = 2 # Variable c_long '2l'
ENOBUFS = 105 # Variable c_int '105'
BadValue = 2 # Variable c_int '2'
ResizeRequest = 25 # Variable c_int '25'
XIMStatusNone = 2048 # Variable c_long '2048l'
Button2Mask = 512 # Variable c_int '512'
GCFont = 16384 # Variable c_long '16384l'
__USE_BSD = 1 # Variable c_int '1'
XNArea = 'area' # Variable STRING '(const char*)"area"'
LSBFirst = 0 # Variable c_int '0'
XkbAnyGroup = 254 # Variable c_int '254'
GraphicsExpose = 13 # Variable c_int '13'
MotionNotify = 6 # Variable c_int '6'
XkbAXN_BKRejectMask = 32 # Variable c_long '32l'
errno = (c_int).in_dll(_libraries['libX11.so.6'], 'errno')
X_GetMotionEvents = 39 # Variable c_int '39'
XkbIM_UseLatched = 2 # Variable c_long '2l'
FRCTSPERBATCH = 256 # Variable c_int '256'
sz_xWindowRoot = 40 # Variable c_int '40'
sz_xPropIconSize = 24 # Variable c_int '24'
sz_xSetAccessControlReq = 4 # Variable c_int '4'
PointerRoot = 1 # Variable c_long '1l'
X_GrabPointer = 26 # Variable c_int '26'
X_UngrabPointer = 27 # Variable c_int '27'
XkbIgnoreLockModsMask = 536870912 # Variable c_long '536870912l'
XkbSA_DfltBtnAbsolute = 4 # Variable c_long '4l'
ENOTNAM = 118 # Variable c_int '118'
XIMHotKeyStateOFF = 2 # Variable c_long '2l'
XkbExplicitKeyTypesMask = 15 # Variable c_int '15'
ESPIPE = 29 # Variable c_int '29'
__clock_t_defined = 1 # Variable c_int '1'
CapRound = 2 # Variable c_int '2'
EROFS = 30 # Variable c_int '30'
XkbAudibleBellMask = 512 # Variable c_long '512l'
XNLineSpace = 'lineSpace' # Variable STRING '(const char*)"lineSpace"'
XlibDisplayPrivSync = 8 # Variable c_long '8l'
NotifyPointer = 5 # Variable c_int '5'
Above = 0 # Variable c_int '0'
X_kbSetNamedIndicator = 16 # Variable c_int '16'
_ALLOCA_H = 1 # Variable c_int '1'
sz_xImageText8Req = 16 # Variable c_int '16'
X_kbSetNames = 18 # Variable c_int '18'
XNSpotLocation = 'spotLocation' # Variable STRING '(const char*)"spotLocation"'
XNGeometryCallback = 'geometryCallback' # Variable STRING '(const char*)"geometryCallback"'
XTHREADS = 1 # Variable c_int '1'
ENAVAIL = 119 # Variable c_int '119'
XIMStringConversionWrapped = 32 # Variable c_int '32'
XNVisiblePosition = 'visiblePosition' # Variable STRING '(const char*)"visiblePosition"'
XkbMaxKeyCount = 248 # Variable c_int '248'
XNR6PreeditCallback = 'r6PreeditCallback' # Variable STRING '(const char*)"r6PreeditCallback"'
XNResourceName = 'resourceName' # Variable STRING '(const char*)"resourceName"'
XNDirectionalDependentDrawing = 'directionalDependentDrawing' # Variable STRING '(const char*)"directionalDependentDrawing"'
XkbAccessXNotifyMask = 1024 # Variable c_long '1024l'
LineSolid = 0 # Variable c_int '0'
X_SetInputFocus = 42 # Variable c_int '42'
EOVERFLOW = 75 # Variable c_int '75'
XYPixmap = 1 # Variable c_int '1'
XkbOD_BadServerVersion = 4 # Variable c_int '4'
_ATFILE_SOURCE = 1 # Variable c_int '1'
FocusOut = 10 # Variable c_int '10'
X_MapSubwindows = 9 # Variable c_int '9'
XIMStringConversionSubstitution = 1 # Variable c_int '1'
ENAMETOOLONG = 36 # Variable c_int '36'
NotifyVirtual = 1 # Variable c_int '1'
XkbGroup3Index = 2 # Variable c_int '2'
XkbExplicitKeyType1Mask = 1 # Variable c_int '1'
XkbIndicatorMapMask = 8 # Variable c_long '8l'
XkbNumIndicators = 32 # Variable c_int '32'
Button4Mask = 2048 # Variable c_int '2048'
XkbGBN_CompatMapMask = 2 # Variable c_long '2l'
__SIZEOF_PTHREAD_CONDATTR_T = 4 # Variable c_int '4'
XkbXI_IndicatorStateMask = 16 # Variable c_long '16l'
ClipByChildren = 0 # Variable c_int '0'
X_kbPerClientFlags = 21 # Variable c_int '21'
ParentRelative = 1 # Variable c_long '1l'
EMSGSIZE = 90 # Variable c_int '90'
X_PROTOCOL = 11 # Variable c_int '11'
sz_xConvertSelectionReq = 24 # Variable c_int '24'
False_ = 0 # Variable c_int '0'
sz_xSetSelectionOwnerReq = 16 # Variable c_int '16'
EREMOTEIO = 121 # Variable c_int '121'
XkbXINone = 65280 # Variable c_int '65280'
X_kbGetIndicatorState = 12 # Variable c_int '12'
_BITS_TYPESIZES_H = 1 # Variable c_int '1'
XNRequiredCharSet = 'requiredCharSet' # Variable STRING '(const char*)"requiredCharSet"'
XkbPCF_AutoResetControlsMask = 4 # Variable c_long '4l'
XkbSA_MessageOnPress = 1 # Variable c_long '1l'
X_CopyGC = 57 # Variable c_int '57'
CurrentTime = 0 # Variable c_long '0l'
XkbActionMessageLength = 6 # Variable c_int '6'
XkbXI_ButtonActionsMask = 2 # Variable c_long '2l'
__USE_POSIX199309 = 1 # Variable c_int '1'
ELFlagSameScreen = 2 # Variable c_int '2'
ENOANO = 55 # Variable c_int '55'
EUCLEAN = 117 # Variable c_int '117'
XkbMaxSymsPerKey = 252 # Variable c_int '252'
XNContextualDrawing = 'contextualDrawing' # Variable STRING '(const char*)"contextualDrawing"'
_SVID_SOURCE = 1 # Variable c_int '1'
XNPreeditState = 'preeditState' # Variable STRING '(const char*)"preeditState"'
__lldiv_t_defined = 1 # Variable c_int '1'
X_kbSetCompatMap = 11 # Variable c_int '11'
DestroyAll = 0 # Variable c_int '0'
X_PolyText8 = 74 # Variable c_int '74'
XNHotKeyState = 'hotKeyState' # Variable STRING '(const char*)"hotKeyState"'
sz_xQueryColorsReq = 8 # Variable c_int '8'
sz_xCreateColormapReq = 16 # Variable c_int '16'
CWWidth = 4 # Variable c_int '4'
XIMPreserveState = 2 # Variable c_long '2l'
EPIPE = 32 # Variable c_int '32'
sz_xPolyLineReq = 12 # Variable c_int '12'
EINTR = 4 # Variable c_int '4'
EBFONT = 59 # Variable c_int '59'
XkbErr_BadClass = 254 # Variable c_int '254'
XkbKeyTypesMask = 1 # Variable c_int '1'
XkbControlsMask = 64 # Variable c_long '64l'
XkbSA_SetGroup = 4 # Variable c_int '4'
EADDRINUSE = 98 # Variable c_int '98'
__WNOTHREAD = 536870912 # Variable c_int '536870912'
KBBellPitch = 4 # Variable c_long '4l'
sz_xReparentWindowReq = 16 # Variable c_int '16'
X_RecolorCursor = 96 # Variable c_int '96'
XkbExplicitComponentsMask = 8 # Variable c_int '8'
XkbGBN_GeometryMask = 64 # Variable c_long '64l'
XkbIndicatorNamesMask = 256 # Variable c_int '256'
sz_xPolyTextReq = 16 # Variable c_int '16'
ENOENT = 2 # Variable c_int '2'
__USE_XOPEN_EXTENDED = 1 # Variable c_int '1'
XlibDisplayProcConni = 16 # Variable c_long '16l'
ECOMM = 70 # Variable c_int '70'
X_ChangeProperty = 18 # Variable c_int '18'
XkbAllActionMessagesMask = 1 # Variable c_long '1l'
XNOMAutomatic = 'omAutomatic' # Variable STRING '(const char*)"omAutomatic"'
X_SetFontPath = 51 # Variable c_int '51'
ENOTEMPTY = 39 # Variable c_int '39'
sz_xDepth = 8 # Variable c_int '8'
XkbIM_UseCompat = 16 # Variable c_long '16l'
sz_xQueryTextExtentsReply = 32 # Variable c_int '32'
X_QueryColors = 91 # Variable c_int '91'
sz_xTranslateCoordsReq = 16 # Variable c_int '16'
WEXITED = 4 # Variable c_int '4'
XkbExplicitAutoRepeatMask = 32 # Variable c_int '32'
SetModeDelete = 1 # Variable c_int '1'
__USE_ISOC95 = 1 # Variable c_int '1'
XkbAllNewKeyboardEventsMask = 7 # Variable c_int '7'
__USE_ISOC99 = 1 # Variable c_int '1'
XkbLookupModsMask = 2048 # Variable c_long '2048l'
X_SetCloseDownMode = 112 # Variable c_int '112'
EMEDIUMTYPE = 124 # Variable c_int '124'
X_kbGetMap = 8 # Variable c_int '8'
sz_xSegment = 8 # Variable c_int '8'
WRCTSPERBATCH = 10 # Variable c_int '10'
ZRCTSPERBATCH = 256 # Variable c_int '256'
GenericEvent = 35 # Variable c_int '35'
X_PolyFillArc = 71 # Variable c_int '71'
XkbClientMapMask = 1 # Variable c_long '1l'
EPROTONOSUPPORT = 93 # Variable c_int '93'
XkbExplicitInterpretMask = 16 # Variable c_int '16'
LowerHighest = 1 # Variable c_int '1'
ETIME = 62 # Variable c_int '62'
AllocNone = 0 # Variable c_int '0'
ENETRESET = 102 # Variable c_int '102'
__USE_XOPEN = 1 # Variable c_int '1'
X_TranslateCoords = 40 # Variable c_int '40'
X_GetPointerControl = 106 # Variable c_int '106'
sz_xConnSetupPrefix = 8 # Variable c_int '8'
XkbEventCode = 0 # Variable c_int '0'
XkbSA_ActionMessage = 16 # Variable c_int '16'
sz_xChangeKeyboardControlReq = 8 # Variable c_int '8'
__USE_ATFILE = 1 # Variable c_int '1'
XkbAX_LatchToLockMask = 128 # Variable c_long '128l'
Mod5MapIndex = 7 # Variable c_int '7'
KeymapStateMask = 16384 # Variable c_long '16384l'
EIDRM = 43 # Variable c_int '43'
EADDRNOTAVAIL = 99 # Variable c_int '99'
XkbClampIntoRange = 64 # Variable c_int '64'
XNAreaNeeded = 'areaNeeded' # Variable STRING '(const char*)"areaNeeded"'
EPERM = 1 # Variable c_int '1'
XkbStateNotify = 2 # Variable c_int '2'
Mod5Mask = 128 # Variable c_int '128'
XkbSA_IgnoreVal = 0 # Variable c_int '0'
ENOMEDIUM = 123 # Variable c_int '123'
X_GetModifierMapping = 119 # Variable c_int '119'
sz_xAllocNamedColorReply = 32 # Variable c_int '32'
PointerMotionMask = 64 # Variable c_long '64l'
EvenOddRule = 0 # Variable c_int '0'
XkbAlphabeticIndex = 2 # Variable c_int '2'
PointerMotionHintMask = 128 # Variable c_long '128l'
sz_xPixmapFormat = 8 # Variable c_int '8'
ELIBMAX = 82 # Variable c_int '82'
_POSIX_C_SOURCE = 200809 # Variable c_long '200809l'
EMULTIHOP = 72 # Variable c_int '72'
XkbIgnoreGroupLockMask = 4096 # Variable c_long '4096l'
XNVaNestedList = 'XNVaNestedList' # Variable STRING '(const char*)"XNVaNestedList"'
XkbIM_UseLocked = 4 # Variable c_long '4l'
__USE_SVID = 1 # Variable c_int '1'
XkbKB_Permanent = 128 # Variable c_int '128'
BadColor = 12 # Variable c_int '12'
XkbGroupsWrapMask = 134217728 # Variable c_long '134217728l'
ECONNABORTED = 103 # Variable c_int '103'
X_PolyFillRectangle = 70 # Variable c_int '70'
Success = 0 # Variable c_int '0'
__SIZEOF_PTHREAD_RWLOCK_T = 56 # Variable c_int '56'
NotifyInferior = 2 # Variable c_int '2'
sz_xAllocColorReply = 32 # Variable c_int '32'
XkbGroup2Index = 1 # Variable c_int '1'
XIMStatusArea = 256 # Variable c_long '256l'
XEventSize = 32 # Variable c_ulong '32ul'
RevertToParent = 2 # Variable c_int '2'
XkbNumberEvents = 1 # Variable c_int '1'
XkbStateNotifyMask = 4 # Variable c_long '4l'
XkbMinorVersion = 0 # Variable c_int '0'
__USE_EXTERN_INLINES = 1 # Variable c_int '1'
__SIZEOF_PTHREAD_COND_T = 48 # Variable c_int '48'
X_QueryFont = 47 # Variable c_int '47'
EDOM = 33 # Variable c_int '33'
XIMUnderline = 2 # Variable c_long '2l'
XkbAX_BKRejectFBMask = 1024 # Variable c_long '1024l'
sz_xBellReq = 4 # Variable c_int '4'
XkbGroupLockMask = 128 # Variable c_long '128l'
EnableAccess = 1 # Variable c_int '1'
XIMReverse = 1 # Variable c_long '1l'
_XOPEN_SOURCE_EXTENDED = 1 # Variable c_int '1'
VisibilityFullyObscured = 2 # Variable c_int '2'
XkbErr_BadId = 253 # Variable c_int '253'
XkbSA_LatchMods = 2 # Variable c_int '2'
sz_xGetPointerControlReply = 32 # Variable c_int '32'
LockMask = 2 # Variable c_int '2'
EKEYREVOKED = 128 # Variable c_int '128'
MappingKeyboard = 1 # Variable c_int '1'
EL2HLT = 51 # Variable c_int '51'
GCFunction = 1 # Variable c_long '1l'
sz_xSetScreenSaverReq = 12 # Variable c_int '12'
_BSD_SOURCE = 1 # Variable c_int '1'
XkbBellNotify = 8 # Variable c_int '8'
X_AllocNamedColor = 85 # Variable c_int '85'
XkbSA_Terminate = 12 # Variable c_int '12'
XNSeparatorofNestedList = 'separatorofNestedList' # Variable STRING '(const char*)"separatorofNestedList"'
sz_xKeymapEvent = 32 # Variable c_int '32'
CopyFromParent = 0 # Variable c_long '0l'
__USE_LARGEFILE64 = 1 # Variable c_int '1'
XkbMajorVersion = 1 # Variable c_int '1'
XBufferOverflow = -1 # Variable c_int '-0x00000000000000001'
XkbIM_NoExplicit = 128 # Variable c_long '128l'
XkbKeyActionsMask = 16 # Variable c_int '16'
XkbSA_SetPtrDflt = 10 # Variable c_int '10'
BadAlloc = 11 # Variable c_int '11'
Unsorted = 0 # Variable c_int '0'
XkbGeomMaxPriority = 255 # Variable c_int '255'
X_FreePixmap = 54 # Variable c_int '54'
X_UngrabKeyboard = 32 # Variable c_int '32'
sz_xAllocColorCellsReply = 32 # Variable c_int '32'
XkbSA_MessageOnRelease = 2 # Variable c_long '2l'
EKEYEXPIRED = 127 # Variable c_int '127'
sz_xCirculateWindowReq = 8 # Variable c_int '8'
GXorReverse = 11 # Variable c_int '11'
XkbAllMapComponentsMask = 255 # Variable c_int '255'
CWBorderWidth = 16 # Variable c_int '16'
XkbAX_FBOptionsMask = 3903 # Variable c_int '3903'
XkbSA_LatchGroup = 5 # Variable c_int '5'
EUNATCH = 49 # Variable c_int '49'
XIMHotKeyStateON = 1 # Variable c_long '1l'
sz_xQueryKeymapReply = 40 # Variable c_int '40'
X_Error = 0 # Variable c_int '0'
AutoRepeatModeOn = 1 # Variable c_int '1'
XkbCompatMapMask = 4 # Variable c_long '4l'
CWSaveUnder = 1024 # Variable c_long '1024l'
XkbLC_ModifierKeys = 512 # Variable c_long '512l'
ETIMEDOUT = 110 # Variable c_int '110'
XkbAllGroups = 255 # Variable c_int '255'
ReplayPointer = 2 # Variable c_int '2'
TrueColor = 4 # Variable c_int '4'
XkbAllBellEventsMask = 1 # Variable c_long '1l'
sz_xCreateGlyphCursorReq = 32 # Variable c_int '32'
XlibDisplayReadEvents = 32 # Variable c_long '32l'
XkbSA_ClearLocks = 1 # Variable c_long '1l'
X_ChangeSaveSet = 6 # Variable c_int '6'
ENXIO = 6 # Variable c_int '6'
XkbAXN_SKPress = 0 # Variable c_int '0'
XkbGroupStateMask = 16 # Variable c_long '16l'
__USE_MISC = 1 # Variable c_int '1'
DoRed = 1 # Variable c_int '1'
NorthEastGravity = 3 # Variable c_int '3'
XkbXI_KeyboardsMask = 1 # Variable c_long '1l'
ENOSR = 63 # Variable c_int '63'
X_ListFonts = 49 # Variable c_int '49'
ELIBSCN = 81 # Variable c_int '81'
XlibDisplayReply = 32 # Variable c_long '32l'
__PTHREAD_MUTEX_HAVE_PREV = 1 # Variable c_int '1'
X_WarpPointer = 41 # Variable c_int '41'
_BITS_BYTESWAP_H = 1 # Variable c_int '1'
EBADSLT = 57 # Variable c_int '57'
ZPixmap = 2 # Variable c_int '2'
XIMVisibleToForward = 256 # Variable c_long '256l'
_SYS_SYSMACROS_H = 1 # Variable c_int '1'
X_RotateProperties = 114 # Variable c_int '114'
XkbNamesNotifyMask = 64 # Variable c_long '64l'
X_kbLatchLockState = 5 # Variable c_int '5'
sz_xGetPropertyReq = 24 # Variable c_int '24'
sz_xDeletePropertyReq = 12 # Variable c_int '12'
XkbLC_Hidden = 1 # Variable c_long '1l'
__USE_POSIX199506 = 1 # Variable c_int '1'
__BIG_ENDIAN = 4321 # Variable c_int '4321'
X_kbSetDeviceInfo = 25 # Variable c_int '25'
EACCES = 13 # Variable c_int '13'
MappingPointer = 2 # Variable c_int '2'
GrabInvalidTime = 2 # Variable c_int '2'
sz_xGetMotionEventsReq = 16 # Variable c_int '16'
sz_xQueryTextExtentsReq = 8 # Variable c_int '8'
Expose = 12 # Variable c_int '12'
XkbAlphabeticMask = 4 # Variable c_int '4'
sz_xChangeGCReq = 12 # Variable c_int '12'
X_UngrabKey = 34 # Variable c_int '34'
XNFontInfo = 'fontInfo' # Variable STRING '(const char*)"fontInfo"'
TopIf = 2 # Variable c_int '2'
XkbAllCompatMask = 3 # Variable c_int '3'
XkbControlsNotify = 3 # Variable c_int '3'
StructureNotifyMask = 131072 # Variable c_long '131072l'
WCONTINUED = 8 # Variable c_int '8'
XkbRGNamesMask = 8192 # Variable c_int '8192'
XkbXI_AllFeaturesMask = 31 # Variable c_int '31'
sz_xInternAtomReply = 32 # Variable c_int '32'
XNCursor = 'cursor' # Variable STRING '(const char*)"cursor"'
TileShape = 1 # Variable c_int '1'
WSTOPPED = 2 # Variable c_int '2'
X_SetAccessControl = 111 # Variable c_int '111'
XkbCompatMapNotify = 7 # Variable c_int '7'
XkbMaxKeyTypes = 255 # Variable c_int '255'
ESOCKTNOSUPPORT = 94 # Variable c_int '94'
FontChange = 255 # Variable c_int '255'
CURSORFONT = 'cursor' # Variable STRING '(const char*)"cursor"'
NotifyWhileGrabbed = 3 # Variable c_int '3'
XkbNoModifierMask = 0 # Variable c_int '0'
Below = 1 # Variable c_int '1'
EEXIST = 17 # Variable c_int '17'
sz_xPoint = 4 # Variable c_int '4'
sz_xGetKeyboardMappingReply = 32 # Variable c_int '32'
EPROTO = 71 # Variable c_int '71'
_SYS_SELECT_H = 1 # Variable c_int '1'
sz_xTimecoord = 8 # Variable c_int '8'
XkbGBN_ClientSymbolsMask = 4 # Variable c_long '4l'
_ISOC95_SOURCE = 1 # Variable c_int '1'
XkbActionMessageMask = 512 # Variable c_long '512l'
X_FreeColors = 88 # Variable c_int '88'
XkbAccessXNotify = 10 # Variable c_int '10'
CWBackPixmap = 1 # Variable c_long '1l'
Button1MotionMask = 256 # Variable c_long '256l'
PropModeReplace = 0 # Variable c_int '0'
XUSE_MTSAFE_API = 1 # Variable c_int '1'
XkbAXN_BKAccept = 4 # Variable c_int '4'
__SYSCALL_WORDSIZE = 64 # Variable c_int '64'
WindingRule = 1 # Variable c_int '1'
XkbSA_RedirectKey = 17 # Variable c_int '17'
xFalse = 0 # Variable c_int '0'
sz_xListInstalledColormapsReply = 32 # Variable c_int '32'
ENOTRECOVERABLE = 131 # Variable c_int '131'
XkbAX_SKAcceptFBMask = 2 # Variable c_long '2l'
xTrue = 1 # Variable c_int '1'
sz_xCopyColormapAndFreeReq = 12 # Variable c_int '12'
EADV = 68 # Variable c_int '68'
ENOSYS = 38 # Variable c_int '38'
BottomIf = 3 # Variable c_int '3'
BadPixmap = 4 # Variable c_int '4'
XkbAX_SKReleaseFBMask = 256 # Variable c_long '256l'
ZLNSPERBATCH = 1024 # Variable c_int '1024'
XkbSA_LockMods = 3 # Variable c_int '3'
XIMStatusCallbacks = 512 # Variable c_long '512l'
XkbNKN_KeycodesMask = 1 # Variable c_long '1l'
XkbKeyNameLength = 4 # Variable c_int '4'
XkbSI_LockingKey = 2 # Variable c_int '2'
_ISOC11_SOURCE = 1 # Variable c_int '1'
X_PolyArc = 68 # Variable c_int '68'
X_StoreNamedColor = 90 # Variable c_int '90'
sz_xQueryExtensionReply = 32 # Variable c_int '32'
XkbModifierStateMask = 1 # Variable c_long '1l'
__USE_UNIX98 = 1 # Variable c_int '1'
XkbSA_XFree86Private = 134 # Variable c_int '134'
XkbAllBooleanCtrlsMask = 8191 # Variable c_int '8191'
sz_xFreeColorsReq = 12 # Variable c_int '12'
XkbAX_SKOptionsMask = 192 # Variable c_int '192'
XNColormap = 'colorMap' # Variable STRING '(const char*)"colorMap"'
JoinMiter = 0 # Variable c_int '0'
sz_xChangeWindowAttributesReq = 12 # Variable c_int '12'
sz_xForceScreenSaverReq = 4 # Variable c_int '4'
Nonconvex = 1 # Variable c_int '1'
XkbOneLevelMask = 1 # Variable c_int '1'
GCLineStyle = 32 # Variable c_long '32l'
KeymapNotify = 11 # Variable c_int '11'
XkbSI_AllOf = 3 # Variable c_int '3'
XkbAllServerInfoMask = 248 # Variable c_int '248'
QueuedAlready = 0 # Variable c_int '0'
AsyncKeyboard = 3 # Variable c_int '3'
XkbOverlay1Mask = 1024 # Variable c_long '1024l'
SyncKeyboard = 4 # Variable c_int '4'
X_PolyPoint = 64 # Variable c_int '64'
XkbLC_AlwaysConsumeShiftAndLock = 4 # Variable c_int '4'
XkbKB_OpMask = 127 # Variable c_int '127'
StaticGravity = 10 # Variable c_int '10'
sz_xCopyPlaneReq = 32 # Variable c_int '32'
FontLeftToRight = 0 # Variable c_int '0'
StaticGray = 0 # Variable c_int '0'
ENETDOWN = 100 # Variable c_int '100'
XkbVirtualModNamesMask = 2048 # Variable c_int '2048'
EXIT_FAILURE = 1 # Variable c_int '1'
PropModePrepend = 1 # Variable c_int '1'
XkbGroup2Mask = 2 # Variable c_int '2'
EDOTDOT = 73 # Variable c_int '73'
EBADFD = 77 # Variable c_int '77'
NotifyAncestor = 0 # Variable c_int '0'
DoBlue = 4 # Variable c_int '4'
EISCONN = 106 # Variable c_int '106'
XkbLC_Default = 2 # Variable c_long '2l'
GXand = 1 # Variable c_int '1'
XkbGeomMaxColors = 32 # Variable c_int '32'
X_ReparentWindow = 7 # Variable c_int '7'
GCDashOffset = 1048576 # Variable c_long '1048576l'
XNStatusDrawCallback = 'statusDrawCallback' # Variable STRING '(const char*)"statusDrawCallback"'
X_kbSetDebuggingFlags = 101 # Variable c_int '101'
XID = c_ulong
Mask = c_ulong
Atom = c_ulong
VisualID = c_ulong
Time = c_ulong
Window = XID
Drawable = XID
Font = XID
Pixmap = XID
Cursor = XID
Colormap = XID
GContext = XID
KeySym = XID
KeyCode = c_ubyte
class _XkbAnyEvent(Structure):
    pass
class _XDisplay(Structure):
    pass
Display = _XDisplay
_XkbAnyEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('time', Time),
    ('xkb_type', c_int),
    ('device', c_uint),
]
XkbAnyEvent = _XkbAnyEvent
class _XkbNewKeyboardNotify(Structure):
    pass
_XkbNewKeyboardNotify._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('time', Time),
    ('xkb_type', c_int),
    ('device', c_int),
    ('old_device', c_int),
    ('min_key_code', c_int),
    ('max_key_code', c_int),
    ('old_min_key_code', c_int),
    ('old_max_key_code', c_int),
    ('changed', c_uint),
    ('req_major', c_char),
    ('req_minor', c_char),
]
XkbNewKeyboardNotifyEvent = _XkbNewKeyboardNotify
class _XkbMapNotifyEvent(Structure):
    pass
_XkbMapNotifyEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('time', Time),
    ('xkb_type', c_int),
    ('device', c_int),
    ('changed', c_uint),
    ('flags', c_uint),
    ('first_type', c_int),
    ('num_types', c_int),
    ('min_key_code', KeyCode),
    ('max_key_code', KeyCode),
    ('first_key_sym', KeyCode),
    ('first_key_act', KeyCode),
    ('first_key_behavior', KeyCode),
    ('first_key_explicit', KeyCode),
    ('first_modmap_key', KeyCode),
    ('first_vmodmap_key', KeyCode),
    ('num_key_syms', c_int),
    ('num_key_acts', c_int),
    ('num_key_behaviors', c_int),
    ('num_key_explicit', c_int),
    ('num_modmap_keys', c_int),
    ('num_vmodmap_keys', c_int),
    ('vmods', c_uint),
]
XkbMapNotifyEvent = _XkbMapNotifyEvent
class _XkbStateNotifyEvent(Structure):
    pass
_XkbStateNotifyEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('time', Time),
    ('xkb_type', c_int),
    ('device', c_int),
    ('changed', c_uint),
    ('group', c_int),
    ('base_group', c_int),
    ('latched_group', c_int),
    ('locked_group', c_int),
    ('mods', c_uint),
    ('base_mods', c_uint),
    ('latched_mods', c_uint),
    ('locked_mods', c_uint),
    ('compat_state', c_int),
    ('grab_mods', c_ubyte),
    ('compat_grab_mods', c_ubyte),
    ('lookup_mods', c_ubyte),
    ('compat_lookup_mods', c_ubyte),
    ('ptr_buttons', c_int),
    ('keycode', KeyCode),
    ('event_type', c_char),
    ('req_major', c_char),
    ('req_minor', c_char),
]
XkbStateNotifyEvent = _XkbStateNotifyEvent
class _XkbControlsNotify(Structure):
    pass
_XkbControlsNotify._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('time', Time),
    ('xkb_type', c_int),
    ('device', c_int),
    ('changed_ctrls', c_uint),
    ('enabled_ctrls', c_uint),
    ('enabled_ctrl_changes', c_uint),
    ('num_groups', c_int),
    ('keycode', KeyCode),
    ('event_type', c_char),
    ('req_major', c_char),
    ('req_minor', c_char),
]
XkbControlsNotifyEvent = _XkbControlsNotify
class _XkbIndicatorNotify(Structure):
    pass
_XkbIndicatorNotify._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('time', Time),
    ('xkb_type', c_int),
    ('device', c_int),
    ('changed', c_uint),
    ('state', c_uint),
]
XkbIndicatorNotifyEvent = _XkbIndicatorNotify
class _XkbNamesNotify(Structure):
    pass
_XkbNamesNotify._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('time', Time),
    ('xkb_type', c_int),
    ('device', c_int),
    ('changed', c_uint),
    ('first_type', c_int),
    ('num_types', c_int),
    ('first_lvl', c_int),
    ('num_lvls', c_int),
    ('num_aliases', c_int),
    ('num_radio_groups', c_int),
    ('changed_vmods', c_uint),
    ('changed_groups', c_uint),
    ('changed_indicators', c_uint),
    ('first_key', c_int),
    ('num_keys', c_int),
]
XkbNamesNotifyEvent = _XkbNamesNotify
class _XkbCompatMapNotify(Structure):
    pass
_XkbCompatMapNotify._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('time', Time),
    ('xkb_type', c_int),
    ('device', c_int),
    ('changed_groups', c_uint),
    ('first_si', c_int),
    ('num_si', c_int),
    ('num_total_si', c_int),
]
XkbCompatMapNotifyEvent = _XkbCompatMapNotify
class _XkbBellNotify(Structure):
    pass
_XkbBellNotify._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('time', Time),
    ('xkb_type', c_int),
    ('device', c_int),
    ('percent', c_int),
    ('pitch', c_int),
    ('duration', c_int),
    ('bell_class', c_int),
    ('bell_id', c_int),
    ('name', Atom),
    ('window', Window),
    ('event_only', c_int),
]
XkbBellNotifyEvent = _XkbBellNotify
class _XkbActionMessage(Structure):
    pass
_XkbActionMessage._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('time', Time),
    ('xkb_type', c_int),
    ('device', c_int),
    ('keycode', KeyCode),
    ('press', c_int),
    ('key_event_follows', c_int),
    ('group', c_int),
    ('mods', c_uint),
    ('message', c_char * 7),
]
XkbActionMessageEvent = _XkbActionMessage
class _XkbAccessXNotify(Structure):
    pass
_XkbAccessXNotify._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('time', Time),
    ('xkb_type', c_int),
    ('device', c_int),
    ('detail', c_int),
    ('keycode', c_int),
    ('sk_delay', c_int),
    ('debounce_delay', c_int),
]
XkbAccessXNotifyEvent = _XkbAccessXNotify
class _XkbExtensionDeviceNotify(Structure):
    pass
_XkbExtensionDeviceNotify._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('time', Time),
    ('xkb_type', c_int),
    ('device', c_int),
    ('reason', c_uint),
    ('supported', c_uint),
    ('unsupported', c_uint),
    ('first_btn', c_int),
    ('num_btns', c_int),
    ('leds_defined', c_uint),
    ('led_state', c_uint),
    ('led_class', c_int),
    ('led_id', c_int),
]
XkbExtensionDeviceNotifyEvent = _XkbExtensionDeviceNotify
class _XkbEvent(Union):
    pass
XkbEvent = _XkbEvent
class _XkbKbdDpyState(Structure):
    pass
_XkbKbdDpyState._fields_ = [
]
XkbKbdDpyStatePtr = POINTER(_XkbKbdDpyState)
XkbKbdDpyStateRec = _XkbKbdDpyState
XkbIgnoreExtension = _libraries['libX11.so.6'].XkbIgnoreExtension
XkbIgnoreExtension.restype = c_int
XkbIgnoreExtension.argtypes = [c_int]
XkbOpenDisplay = _libraries['libX11.so.6'].XkbOpenDisplay
XkbOpenDisplay.restype = POINTER(Display)
XkbOpenDisplay.argtypes = [STRING, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
XkbQueryExtension = _libraries['libX11.so.6'].XkbQueryExtension
XkbQueryExtension.restype = c_int
XkbQueryExtension.argtypes = [POINTER(Display), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
XkbUseExtension = _libraries['libX11.so.6'].XkbUseExtension
XkbUseExtension.restype = c_int
XkbUseExtension.argtypes = [POINTER(Display), POINTER(c_int), POINTER(c_int)]
XkbLibraryVersion = _libraries['libX11.so.6'].XkbLibraryVersion
XkbLibraryVersion.restype = c_int
XkbLibraryVersion.argtypes = [POINTER(c_int), POINTER(c_int)]
XkbSetXlibControls = _libraries['libX11.so.6'].XkbSetXlibControls
XkbSetXlibControls.restype = c_uint
XkbSetXlibControls.argtypes = [POINTER(Display), c_uint, c_uint]
XkbGetXlibControls = _libraries['libX11.so.6'].XkbGetXlibControls
XkbGetXlibControls.restype = c_uint
XkbGetXlibControls.argtypes = [POINTER(Display)]
XkbXlibControlsImplemented = _libraries['libX11.so.6'].XkbXlibControlsImplemented
XkbXlibControlsImplemented.restype = c_uint
XkbXlibControlsImplemented.argtypes = []
XkbInternAtomFunc = CFUNCTYPE(Atom, POINTER(Display), STRING, c_int)
XkbGetAtomNameFunc = CFUNCTYPE(STRING, POINTER(Display), Atom)
XkbSetAtomFuncs = _libraries['libX11.so.6'].XkbSetAtomFuncs
XkbSetAtomFuncs.restype = None
XkbSetAtomFuncs.argtypes = [XkbInternAtomFunc, XkbGetAtomNameFunc]
XkbKeycodeToKeysym = _libraries['libX11.so.6'].XkbKeycodeToKeysym
XkbKeycodeToKeysym.restype = KeySym
XkbKeycodeToKeysym.argtypes = [POINTER(Display), KeyCode, c_int, c_int]
XkbKeysymToModifiers = _libraries['libX11.so.6'].XkbKeysymToModifiers
XkbKeysymToModifiers.restype = c_uint
XkbKeysymToModifiers.argtypes = [POINTER(Display), KeySym]
XkbLookupKeySym = _libraries['libX11.so.6'].XkbLookupKeySym
XkbLookupKeySym.restype = c_int
XkbLookupKeySym.argtypes = [POINTER(Display), KeyCode, c_uint, POINTER(c_uint), POINTER(KeySym)]
XkbLookupKeyBinding = _libraries['libX11.so.6'].XkbLookupKeyBinding
XkbLookupKeyBinding.restype = c_int
XkbLookupKeyBinding.argtypes = [POINTER(Display), KeySym, c_uint, STRING, c_int, POINTER(c_int)]
class _XkbDesc(Structure):
    pass
XkbDescPtr = POINTER(_XkbDesc)
XkbTranslateKeyCode = _libraries['libX11.so.6'].XkbTranslateKeyCode
XkbTranslateKeyCode.restype = c_int
XkbTranslateKeyCode.argtypes = [XkbDescPtr, KeyCode, c_uint, POINTER(c_uint), POINTER(KeySym)]
XkbTranslateKeySym = _libraries['libX11.so.6'].XkbTranslateKeySym
XkbTranslateKeySym.restype = c_int
XkbTranslateKeySym.argtypes = [POINTER(Display), POINTER(KeySym), c_uint, STRING, c_int, POINTER(c_int)]
XkbSetAutoRepeatRate = _libraries['libX11.so.6'].XkbSetAutoRepeatRate
XkbSetAutoRepeatRate.restype = c_int
XkbSetAutoRepeatRate.argtypes = [POINTER(Display), c_uint, c_uint, c_uint]
XkbGetAutoRepeatRate = _libraries['libX11.so.6'].XkbGetAutoRepeatRate
XkbGetAutoRepeatRate.restype = c_int
XkbGetAutoRepeatRate.argtypes = [POINTER(Display), c_uint, POINTER(c_uint), POINTER(c_uint)]
XkbChangeEnabledControls = _libraries['libX11.so.6'].XkbChangeEnabledControls
XkbChangeEnabledControls.restype = c_int
XkbChangeEnabledControls.argtypes = [POINTER(Display), c_uint, c_uint, c_uint]
XkbDeviceBell = _libraries['libX11.so.6'].XkbDeviceBell
XkbDeviceBell.restype = c_int
XkbDeviceBell.argtypes = [POINTER(Display), Window, c_int, c_int, c_int, c_int, Atom]
XkbForceDeviceBell = _libraries['libX11.so.6'].XkbForceDeviceBell
XkbForceDeviceBell.restype = c_int
XkbForceDeviceBell.argtypes = [POINTER(Display), c_int, c_int, c_int, c_int]
XkbDeviceBellEvent = _libraries['libX11.so.6'].XkbDeviceBellEvent
XkbDeviceBellEvent.restype = c_int
XkbDeviceBellEvent.argtypes = [POINTER(Display), Window, c_int, c_int, c_int, c_int, Atom]
XkbBell = _libraries['libX11.so.6'].XkbBell
XkbBell.restype = c_int
XkbBell.argtypes = [POINTER(Display), Window, c_int, Atom]
XkbForceBell = _libraries['libX11.so.6'].XkbForceBell
XkbForceBell.restype = c_int
XkbForceBell.argtypes = [POINTER(Display), c_int]
XkbBellEvent = _libraries['libX11.so.6'].XkbBellEvent
XkbBellEvent.restype = c_int
XkbBellEvent.argtypes = [POINTER(Display), Window, c_int, Atom]
XkbSelectEvents = _libraries['libX11.so.6'].XkbSelectEvents
XkbSelectEvents.restype = c_int
XkbSelectEvents.argtypes = [POINTER(Display), c_uint, c_uint, c_uint]
XkbSelectEventDetails = _libraries['libX11.so.6'].XkbSelectEventDetails
XkbSelectEventDetails.restype = c_int
XkbSelectEventDetails.argtypes = [POINTER(Display), c_uint, c_uint, c_ulong, c_ulong]
class _XkbMapChanges(Structure):
    pass
XkbMapChangesPtr = POINTER(_XkbMapChanges)
XkbNoteMapChanges = _libraries['libX11.so.6'].XkbNoteMapChanges
XkbNoteMapChanges.restype = None
XkbNoteMapChanges.argtypes = [XkbMapChangesPtr, POINTER(XkbMapNotifyEvent), c_uint]
class _XkbNameChanges(Structure):
    pass
XkbNameChangesPtr = POINTER(_XkbNameChanges)
XkbNoteNameChanges = _libraries['libX11.so.6'].XkbNoteNameChanges
XkbNoteNameChanges.restype = None
XkbNoteNameChanges.argtypes = [XkbNameChangesPtr, POINTER(XkbNamesNotifyEvent), c_uint]
XkbGetIndicatorState = _libraries['libX11.so.6'].XkbGetIndicatorState
XkbGetIndicatorState.restype = c_int
XkbGetIndicatorState.argtypes = [POINTER(Display), c_uint, POINTER(c_uint)]
XkbGetIndicatorMap = _libraries['libX11.so.6'].XkbGetIndicatorMap
XkbGetIndicatorMap.restype = c_int
XkbGetIndicatorMap.argtypes = [POINTER(Display), c_ulong, XkbDescPtr]
XkbSetIndicatorMap = _libraries['libX11.so.6'].XkbSetIndicatorMap
XkbSetIndicatorMap.restype = c_int
XkbSetIndicatorMap.argtypes = [POINTER(Display), c_ulong, XkbDescPtr]
class _XkbIndicatorMapRec(Structure):
    pass
XkbIndicatorMapPtr = POINTER(_XkbIndicatorMapRec)
XkbGetNamedIndicator = _libraries['libX11.so.6'].XkbGetNamedIndicator
XkbGetNamedIndicator.restype = c_int
XkbGetNamedIndicator.argtypes = [POINTER(Display), Atom, POINTER(c_int), POINTER(c_int), XkbIndicatorMapPtr, POINTER(c_int)]
XkbGetNamedDeviceIndicator = _libraries['libX11.so.6'].XkbGetNamedDeviceIndicator
XkbGetNamedDeviceIndicator.restype = c_int
XkbGetNamedDeviceIndicator.argtypes = [POINTER(Display), c_uint, c_uint, c_uint, Atom, POINTER(c_int), POINTER(c_int), XkbIndicatorMapPtr, POINTER(c_int)]
XkbSetNamedIndicator = _libraries['libX11.so.6'].XkbSetNamedIndicator
XkbSetNamedIndicator.restype = c_int
XkbSetNamedIndicator.argtypes = [POINTER(Display), Atom, c_int, c_int, c_int, XkbIndicatorMapPtr]
XkbSetNamedDeviceIndicator = _libraries['libX11.so.6'].XkbSetNamedDeviceIndicator
XkbSetNamedDeviceIndicator.restype = c_int
XkbSetNamedDeviceIndicator.argtypes = [POINTER(Display), c_uint, c_uint, c_uint, Atom, c_int, c_int, c_int, XkbIndicatorMapPtr]
XkbLockModifiers = _libraries['libX11.so.6'].XkbLockModifiers
XkbLockModifiers.restype = c_int
XkbLockModifiers.argtypes = [POINTER(Display), c_uint, c_uint, c_uint]
XkbLatchModifiers = _libraries['libX11.so.6'].XkbLatchModifiers
XkbLatchModifiers.restype = c_int
XkbLatchModifiers.argtypes = [POINTER(Display), c_uint, c_uint, c_uint]
XkbLockGroup = _libraries['libX11.so.6'].XkbLockGroup
XkbLockGroup.restype = c_int
XkbLockGroup.argtypes = [POINTER(Display), c_uint, c_uint]
XkbLatchGroup = _libraries['libX11.so.6'].XkbLatchGroup
XkbLatchGroup.restype = c_int
XkbLatchGroup.argtypes = [POINTER(Display), c_uint, c_uint]
XkbSetServerInternalMods = _libraries['libX11.so.6'].XkbSetServerInternalMods
XkbSetServerInternalMods.restype = c_int
XkbSetServerInternalMods.argtypes = [POINTER(Display), c_uint, c_uint, c_uint, c_uint, c_uint]
XkbSetIgnoreLockMods = _libraries['libX11.so.6'].XkbSetIgnoreLockMods
XkbSetIgnoreLockMods.restype = c_int
XkbSetIgnoreLockMods.argtypes = [POINTER(Display), c_uint, c_uint, c_uint, c_uint, c_uint]
XkbVirtualModsToReal = _libraries['libX11.so.6'].XkbVirtualModsToReal
XkbVirtualModsToReal.restype = c_int
XkbVirtualModsToReal.argtypes = [XkbDescPtr, c_uint, POINTER(c_uint)]
class _XkbKeyType(Structure):
    pass
XkbKeyTypePtr = POINTER(_XkbKeyType)
XkbComputeEffectiveMap = _libraries['libX11.so.6'].XkbComputeEffectiveMap
XkbComputeEffectiveMap.restype = c_int
XkbComputeEffectiveMap.argtypes = [XkbDescPtr, XkbKeyTypePtr, POINTER(c_ubyte)]
XkbInitCanonicalKeyTypes = _libraries['libX11.so.6'].XkbInitCanonicalKeyTypes
XkbInitCanonicalKeyTypes.restype = c_int
XkbInitCanonicalKeyTypes.argtypes = [XkbDescPtr, c_uint, c_int]
XkbAllocKeyboard = _libraries['libX11.so.6'].XkbAllocKeyboard
XkbAllocKeyboard.restype = XkbDescPtr
XkbAllocKeyboard.argtypes = []
XkbFreeKeyboard = _libraries['libX11.so.6'].XkbFreeKeyboard
XkbFreeKeyboard.restype = None
XkbFreeKeyboard.argtypes = [XkbDescPtr, c_uint, c_int]
XkbAllocClientMap = _libraries['libX11.so.6'].XkbAllocClientMap
XkbAllocClientMap.restype = c_int
XkbAllocClientMap.argtypes = [XkbDescPtr, c_uint, c_uint]
XkbAllocServerMap = _libraries['libX11.so.6'].XkbAllocServerMap
XkbAllocServerMap.restype = c_int
XkbAllocServerMap.argtypes = [XkbDescPtr, c_uint, c_uint]
XkbFreeClientMap = _libraries['libX11.so.6'].XkbFreeClientMap
XkbFreeClientMap.restype = None
XkbFreeClientMap.argtypes = [XkbDescPtr, c_uint, c_int]
XkbFreeServerMap = _libraries['libX11.so.6'].XkbFreeServerMap
XkbFreeServerMap.restype = None
XkbFreeServerMap.argtypes = [XkbDescPtr, c_uint, c_int]
XkbAddKeyType = _libraries['libX11.so.6'].XkbAddKeyType
XkbAddKeyType.restype = XkbKeyTypePtr
XkbAddKeyType.argtypes = [XkbDescPtr, Atom, c_int, c_int, c_int]
XkbAllocIndicatorMaps = _libraries['libX11.so.6'].XkbAllocIndicatorMaps
XkbAllocIndicatorMaps.restype = c_int
XkbAllocIndicatorMaps.argtypes = [XkbDescPtr]
XkbFreeIndicatorMaps = _libraries['libX11.so.6'].XkbFreeIndicatorMaps
XkbFreeIndicatorMaps.restype = None
XkbFreeIndicatorMaps.argtypes = [XkbDescPtr]
XkbGetMap = _libraries['libX11.so.6'].XkbGetMap
XkbGetMap.restype = XkbDescPtr
XkbGetMap.argtypes = [POINTER(Display), c_uint, c_uint]
XkbGetUpdatedMap = _libraries['libX11.so.6'].XkbGetUpdatedMap
XkbGetUpdatedMap.restype = c_int
XkbGetUpdatedMap.argtypes = [POINTER(Display), c_uint, XkbDescPtr]
XkbGetMapChanges = _libraries['libX11.so.6'].XkbGetMapChanges
XkbGetMapChanges.restype = c_int
XkbGetMapChanges.argtypes = [POINTER(Display), XkbDescPtr, XkbMapChangesPtr]
XkbRefreshKeyboardMapping = _libraries['libX11.so.6'].XkbRefreshKeyboardMapping
XkbRefreshKeyboardMapping.restype = c_int
XkbRefreshKeyboardMapping.argtypes = [POINTER(XkbMapNotifyEvent)]
XkbGetKeyTypes = _libraries['libX11.so.6'].XkbGetKeyTypes
XkbGetKeyTypes.restype = c_int
XkbGetKeyTypes.argtypes = [POINTER(Display), c_uint, c_uint, XkbDescPtr]
XkbGetKeySyms = _libraries['libX11.so.6'].XkbGetKeySyms
XkbGetKeySyms.restype = c_int
XkbGetKeySyms.argtypes = [POINTER(Display), c_uint, c_uint, XkbDescPtr]
XkbGetKeyActions = _libraries['libX11.so.6'].XkbGetKeyActions
XkbGetKeyActions.restype = c_int
XkbGetKeyActions.argtypes = [POINTER(Display), c_uint, c_uint, XkbDescPtr]
XkbGetKeyBehaviors = _libraries['libX11.so.6'].XkbGetKeyBehaviors
XkbGetKeyBehaviors.restype = c_int
XkbGetKeyBehaviors.argtypes = [POINTER(Display), c_uint, c_uint, XkbDescPtr]
XkbGetVirtualMods = _libraries['libX11.so.6'].XkbGetVirtualMods
XkbGetVirtualMods.restype = c_int
XkbGetVirtualMods.argtypes = [POINTER(Display), c_uint, XkbDescPtr]
XkbGetKeyExplicitComponents = _libraries['libX11.so.6'].XkbGetKeyExplicitComponents
XkbGetKeyExplicitComponents.restype = c_int
XkbGetKeyExplicitComponents.argtypes = [POINTER(Display), c_uint, c_uint, XkbDescPtr]
XkbGetKeyModifierMap = _libraries['libX11.so.6'].XkbGetKeyModifierMap
XkbGetKeyModifierMap.restype = c_int
XkbGetKeyModifierMap.argtypes = [POINTER(Display), c_uint, c_uint, XkbDescPtr]
XkbGetKeyVirtualModMap = _libraries['libX11.so.6'].XkbGetKeyVirtualModMap
XkbGetKeyVirtualModMap.restype = c_int
XkbGetKeyVirtualModMap.argtypes = [POINTER(Display), c_uint, c_uint, XkbDescPtr]
XkbAllocControls = _libraries['libX11.so.6'].XkbAllocControls
XkbAllocControls.restype = c_int
XkbAllocControls.argtypes = [XkbDescPtr, c_uint]
XkbFreeControls = _libraries['libX11.so.6'].XkbFreeControls
XkbFreeControls.restype = None
XkbFreeControls.argtypes = [XkbDescPtr, c_uint, c_int]
XkbGetControls = _libraries['libX11.so.6'].XkbGetControls
XkbGetControls.restype = c_int
XkbGetControls.argtypes = [POINTER(Display), c_ulong, XkbDescPtr]
XkbSetControls = _libraries['libX11.so.6'].XkbSetControls
XkbSetControls.restype = c_int
XkbSetControls.argtypes = [POINTER(Display), c_ulong, XkbDescPtr]
class _XkbControlsChanges(Structure):
    pass
XkbControlsChangesPtr = POINTER(_XkbControlsChanges)
XkbNoteControlsChanges = _libraries['libX11.so.6'].XkbNoteControlsChanges
XkbNoteControlsChanges.restype = None
XkbNoteControlsChanges.argtypes = [XkbControlsChangesPtr, POINTER(XkbControlsNotifyEvent), c_uint]
XkbAllocCompatMap = _libraries['libX11.so.6'].XkbAllocCompatMap
XkbAllocCompatMap.restype = c_int
XkbAllocCompatMap.argtypes = [XkbDescPtr, c_uint, c_uint]
XkbFreeCompatMap = _libraries['libX11.so.6'].XkbFreeCompatMap
XkbFreeCompatMap.restype = None
XkbFreeCompatMap.argtypes = [XkbDescPtr, c_uint, c_int]
XkbGetCompatMap = _libraries['libX11.so.6'].XkbGetCompatMap
XkbGetCompatMap.restype = c_int
XkbGetCompatMap.argtypes = [POINTER(Display), c_uint, XkbDescPtr]
XkbSetCompatMap = _libraries['libX11.so.6'].XkbSetCompatMap
XkbSetCompatMap.restype = c_int
XkbSetCompatMap.argtypes = [POINTER(Display), c_uint, XkbDescPtr, c_int]
XkbAllocNames = _libraries['libX11.so.6'].XkbAllocNames
XkbAllocNames.restype = c_int
XkbAllocNames.argtypes = [XkbDescPtr, c_uint, c_int, c_int]
XkbGetNames = _libraries['libX11.so.6'].XkbGetNames
XkbGetNames.restype = c_int
XkbGetNames.argtypes = [POINTER(Display), c_uint, XkbDescPtr]
XkbSetNames = _libraries['libX11.so.6'].XkbSetNames
XkbSetNames.restype = c_int
XkbSetNames.argtypes = [POINTER(Display), c_uint, c_uint, c_uint, XkbDescPtr]
XkbChangeNames = _libraries['libX11.so.6'].XkbChangeNames
XkbChangeNames.restype = c_int
XkbChangeNames.argtypes = [POINTER(Display), XkbDescPtr, XkbNameChangesPtr]
XkbFreeNames = _libraries['libX11.so.6'].XkbFreeNames
XkbFreeNames.restype = None
XkbFreeNames.argtypes = [XkbDescPtr, c_uint, c_int]
class _XkbStateRec(Structure):
    pass
XkbStatePtr = POINTER(_XkbStateRec)
XkbGetState = _libraries['libX11.so.6'].XkbGetState
XkbGetState.restype = c_int
XkbGetState.argtypes = [POINTER(Display), c_uint, XkbStatePtr]
XkbSetMap = _libraries['libX11.so.6'].XkbSetMap
XkbSetMap.restype = c_int
XkbSetMap.argtypes = [POINTER(Display), c_uint, XkbDescPtr]
XkbChangeMap = _libraries['libX11.so.6'].XkbChangeMap
XkbChangeMap.restype = c_int
XkbChangeMap.argtypes = [POINTER(Display), XkbDescPtr, XkbMapChangesPtr]
XkbSetDetectableAutoRepeat = _libraries['libX11.so.6'].XkbSetDetectableAutoRepeat
XkbSetDetectableAutoRepeat.restype = c_int
XkbSetDetectableAutoRepeat.argtypes = [POINTER(Display), c_int, POINTER(c_int)]
XkbGetDetectableAutoRepeat = _libraries['libX11.so.6'].XkbGetDetectableAutoRepeat
XkbGetDetectableAutoRepeat.restype = c_int
XkbGetDetectableAutoRepeat.argtypes = [POINTER(Display), POINTER(c_int)]
XkbSetAutoResetControls = _libraries['libX11.so.6'].XkbSetAutoResetControls
XkbSetAutoResetControls.restype = c_int
XkbSetAutoResetControls.argtypes = [POINTER(Display), c_uint, POINTER(c_uint), POINTER(c_uint)]
XkbGetAutoResetControls = _libraries['libX11.so.6'].XkbGetAutoResetControls
XkbGetAutoResetControls.restype = c_int
XkbGetAutoResetControls.argtypes = [POINTER(Display), POINTER(c_uint), POINTER(c_uint)]
XkbSetPerClientControls = _libraries['libX11.so.6'].XkbSetPerClientControls
XkbSetPerClientControls.restype = c_int
XkbSetPerClientControls.argtypes = [POINTER(Display), c_uint, POINTER(c_uint)]
XkbGetPerClientControls = _libraries['libX11.so.6'].XkbGetPerClientControls
XkbGetPerClientControls.restype = c_int
XkbGetPerClientControls.argtypes = [POINTER(Display), POINTER(c_uint)]
XkbCopyKeyType = _libraries['libX11.so.6'].XkbCopyKeyType
XkbCopyKeyType.restype = c_int
XkbCopyKeyType.argtypes = [XkbKeyTypePtr, XkbKeyTypePtr]
XkbCopyKeyTypes = _libraries['libX11.so.6'].XkbCopyKeyTypes
XkbCopyKeyTypes.restype = c_int
XkbCopyKeyTypes.argtypes = [XkbKeyTypePtr, XkbKeyTypePtr, c_int]
XkbResizeKeyType = _libraries['libX11.so.6'].XkbResizeKeyType
XkbResizeKeyType.restype = c_int
XkbResizeKeyType.argtypes = [XkbDescPtr, c_int, c_int, c_int, c_int]
XkbResizeKeySyms = _libraries['libX11.so.6'].XkbResizeKeySyms
XkbResizeKeySyms.restype = POINTER(KeySym)
XkbResizeKeySyms.argtypes = [XkbDescPtr, c_int, c_int]
class _XkbAction(Union):
    pass
XkbAction = _XkbAction
XkbResizeKeyActions = _libraries['libX11.so.6'].XkbResizeKeyActions
XkbResizeKeyActions.restype = POINTER(XkbAction)
XkbResizeKeyActions.argtypes = [XkbDescPtr, c_int, c_int]
XkbChangeTypesOfKey = _libraries['libX11.so.6'].XkbChangeTypesOfKey
XkbChangeTypesOfKey.restype = c_int
XkbChangeTypesOfKey.argtypes = [XkbDescPtr, c_int, c_int, c_uint, POINTER(c_int), XkbMapChangesPtr]
class _XkbChanges(Structure):
    pass
XkbChangesPtr = POINTER(_XkbChanges)
XkbChangeKeycodeRange = _libraries['libX11.so.6'].XkbChangeKeycodeRange
XkbChangeKeycodeRange.restype = c_int
XkbChangeKeycodeRange.argtypes = [XkbDescPtr, c_int, c_int, XkbChangesPtr]
class _XkbComponentList(Structure):
    pass
XkbComponentListPtr = POINTER(_XkbComponentList)
class _XkbComponentNames(Structure):
    pass
XkbComponentNamesPtr = POINTER(_XkbComponentNames)
XkbListComponents = _libraries['libX11.so.6'].XkbListComponents
XkbListComponents.restype = XkbComponentListPtr
XkbListComponents.argtypes = [POINTER(Display), c_uint, XkbComponentNamesPtr, POINTER(c_int)]
XkbFreeComponentList = _libraries['libX11.so.6'].XkbFreeComponentList
XkbFreeComponentList.restype = None
XkbFreeComponentList.argtypes = [XkbComponentListPtr]
XkbGetKeyboard = _libraries['libX11.so.6'].XkbGetKeyboard
XkbGetKeyboard.restype = XkbDescPtr
XkbGetKeyboard.argtypes = [POINTER(Display), c_uint, c_uint]
XkbGetKeyboardByName = _libraries['libX11.so.6'].XkbGetKeyboardByName
XkbGetKeyboardByName.restype = XkbDescPtr
XkbGetKeyboardByName.argtypes = [POINTER(Display), c_uint, XkbComponentNamesPtr, c_uint, c_uint, c_int]
XkbKeyTypesForCoreSymbols = _libraries['libX11.so.6'].XkbKeyTypesForCoreSymbols
XkbKeyTypesForCoreSymbols.restype = c_int
XkbKeyTypesForCoreSymbols.argtypes = [XkbDescPtr, c_int, POINTER(KeySym), c_uint, POINTER(c_int), POINTER(KeySym)]
XkbApplyCompatMapToKey = _libraries['libX11.so.6'].XkbApplyCompatMapToKey
XkbApplyCompatMapToKey.restype = c_int
XkbApplyCompatMapToKey.argtypes = [XkbDescPtr, KeyCode, XkbChangesPtr]
XkbUpdateMapFromCore = _libraries['libX11.so.6'].XkbUpdateMapFromCore
XkbUpdateMapFromCore.restype = c_int
XkbUpdateMapFromCore.argtypes = [XkbDescPtr, KeyCode, c_int, c_int, POINTER(KeySym), XkbChangesPtr]
class _XkbDeviceLedInfo(Structure):
    pass
XkbDeviceLedInfoPtr = POINTER(_XkbDeviceLedInfo)
class _XkbDeviceInfo(Structure):
    pass
XkbDeviceInfoPtr = POINTER(_XkbDeviceInfo)
XkbAddDeviceLedInfo = _libraries['libX11.so.6'].XkbAddDeviceLedInfo
XkbAddDeviceLedInfo.restype = XkbDeviceLedInfoPtr
XkbAddDeviceLedInfo.argtypes = [XkbDeviceInfoPtr, c_uint, c_uint]
XkbResizeDeviceButtonActions = _libraries['libX11.so.6'].XkbResizeDeviceButtonActions
XkbResizeDeviceButtonActions.restype = c_int
XkbResizeDeviceButtonActions.argtypes = [XkbDeviceInfoPtr, c_uint]
XkbAllocDeviceInfo = _libraries['libX11.so.6'].XkbAllocDeviceInfo
XkbAllocDeviceInfo.restype = XkbDeviceInfoPtr
XkbAllocDeviceInfo.argtypes = [c_uint, c_uint, c_uint]
XkbFreeDeviceInfo = _libraries['libX11.so.6'].XkbFreeDeviceInfo
XkbFreeDeviceInfo.restype = None
XkbFreeDeviceInfo.argtypes = [XkbDeviceInfoPtr, c_uint, c_int]
class _XkbDeviceChanges(Structure):
    pass
XkbDeviceChangesPtr = POINTER(_XkbDeviceChanges)
XkbNoteDeviceChanges = _libraries['libX11.so.6'].XkbNoteDeviceChanges
XkbNoteDeviceChanges.restype = None
XkbNoteDeviceChanges.argtypes = [XkbDeviceChangesPtr, POINTER(XkbExtensionDeviceNotifyEvent), c_uint]
XkbGetDeviceInfo = _libraries['libX11.so.6'].XkbGetDeviceInfo
XkbGetDeviceInfo.restype = XkbDeviceInfoPtr
XkbGetDeviceInfo.argtypes = [POINTER(Display), c_uint, c_uint, c_uint, c_uint]
XkbGetDeviceInfoChanges = _libraries['libX11.so.6'].XkbGetDeviceInfoChanges
XkbGetDeviceInfoChanges.restype = c_int
XkbGetDeviceInfoChanges.argtypes = [POINTER(Display), XkbDeviceInfoPtr, XkbDeviceChangesPtr]
XkbGetDeviceButtonActions = _libraries['libX11.so.6'].XkbGetDeviceButtonActions
XkbGetDeviceButtonActions.restype = c_int
XkbGetDeviceButtonActions.argtypes = [POINTER(Display), XkbDeviceInfoPtr, c_int, c_uint, c_uint]
XkbGetDeviceLedInfo = _libraries['libX11.so.6'].XkbGetDeviceLedInfo
XkbGetDeviceLedInfo.restype = c_int
XkbGetDeviceLedInfo.argtypes = [POINTER(Display), XkbDeviceInfoPtr, c_uint, c_uint, c_uint]
XkbSetDeviceInfo = _libraries['libX11.so.6'].XkbSetDeviceInfo
XkbSetDeviceInfo.restype = c_int
XkbSetDeviceInfo.argtypes = [POINTER(Display), c_uint, XkbDeviceInfoPtr]
XkbChangeDeviceInfo = _libraries['libX11.so.6'].XkbChangeDeviceInfo
XkbChangeDeviceInfo.restype = c_int
XkbChangeDeviceInfo.argtypes = [POINTER(Display), XkbDeviceInfoPtr, XkbDeviceChangesPtr]
XkbSetDeviceLedInfo = _libraries['libX11.so.6'].XkbSetDeviceLedInfo
XkbSetDeviceLedInfo.restype = c_int
XkbSetDeviceLedInfo.argtypes = [POINTER(Display), XkbDeviceInfoPtr, c_uint, c_uint, c_uint]
XkbSetDeviceButtonActions = _libraries['libX11.so.6'].XkbSetDeviceButtonActions
XkbSetDeviceButtonActions.restype = c_int
XkbSetDeviceButtonActions.argtypes = [POINTER(Display), XkbDeviceInfoPtr, c_uint, c_uint]
XkbToControl = _libraries['libX11.so.6'].XkbToControl
XkbToControl.restype = c_char
XkbToControl.argtypes = [c_char]
XkbSetDebuggingFlags = _libraries['libX11.so.6'].XkbSetDebuggingFlags
XkbSetDebuggingFlags.restype = c_int
XkbSetDebuggingFlags.argtypes = [POINTER(Display), c_uint, c_uint, STRING, c_uint, c_uint, POINTER(c_uint), POINTER(c_uint)]
XkbApplyVirtualModChanges = _libraries['libX11.so.6'].XkbApplyVirtualModChanges
XkbApplyVirtualModChanges.restype = c_int
XkbApplyVirtualModChanges.argtypes = [XkbDescPtr, c_uint, XkbChangesPtr]
XkbUpdateActionVirtualMods = _libraries['libX11.so.6'].XkbUpdateActionVirtualMods
XkbUpdateActionVirtualMods.restype = c_int
XkbUpdateActionVirtualMods.argtypes = [XkbDescPtr, POINTER(XkbAction), c_uint]
XkbUpdateKeyTypeVirtualMods = _libraries['libX11.so.6'].XkbUpdateKeyTypeVirtualMods
XkbUpdateKeyTypeVirtualMods.restype = None
XkbUpdateKeyTypeVirtualMods.argtypes = [XkbDescPtr, XkbKeyTypePtr, c_uint, XkbChangesPtr]
_Xmblen = _libraries['libX11.so.6']._Xmblen
_Xmblen.restype = c_int
_Xmblen.argtypes = [STRING, c_int]
XPointer = STRING
class _XExtData(Structure):
    pass
_XExtData._fields_ = [
    ('number', c_int),
    ('next', POINTER(_XExtData)),
    ('free_private', CFUNCTYPE(c_int, POINTER(_XExtData))),
    ('private_data', XPointer),
]
XExtData = _XExtData
class XExtCodes(Structure):
    pass
XExtCodes._fields_ = [
    ('extension', c_int),
    ('major_opcode', c_int),
    ('first_event', c_int),
    ('first_error', c_int),
]
class XPixmapFormatValues(Structure):
    pass
XPixmapFormatValues._fields_ = [
    ('depth', c_int),
    ('bits_per_pixel', c_int),
    ('scanline_pad', c_int),
]
class XGCValues(Structure):
    pass
XGCValues._fields_ = [
    ('function', c_int),
    ('plane_mask', c_ulong),
    ('foreground', c_ulong),
    ('background', c_ulong),
    ('line_width', c_int),
    ('line_style', c_int),
    ('cap_style', c_int),
    ('join_style', c_int),
    ('fill_style', c_int),
    ('fill_rule', c_int),
    ('arc_mode', c_int),
    ('tile', Pixmap),
    ('stipple', Pixmap),
    ('ts_x_origin', c_int),
    ('ts_y_origin', c_int),
    ('font', Font),
    ('subwindow_mode', c_int),
    ('graphics_exposures', c_int),
    ('clip_x_origin', c_int),
    ('clip_y_origin', c_int),
    ('clip_mask', Pixmap),
    ('dash_offset', c_int),
    ('dashes', c_char),
]
class _XGC(Structure):
    pass
GC = POINTER(_XGC)
class Visual(Structure):
    pass
Visual._fields_ = [
    ('ext_data', POINTER(XExtData)),
    ('visualid', VisualID),
    ('c_class', c_int),
    ('red_mask', c_ulong),
    ('green_mask', c_ulong),
    ('blue_mask', c_ulong),
    ('bits_per_rgb', c_int),
    ('map_entries', c_int),
]
class Depth(Structure):
    pass
Depth._fields_ = [
    ('depth', c_int),
    ('nvisuals', c_int),
    ('visuals', POINTER(Visual)),
]
class Screen(Structure):
    pass
Screen._fields_ = [
    ('ext_data', POINTER(XExtData)),
    ('display', POINTER(_XDisplay)),
    ('root', Window),
    ('width', c_int),
    ('height', c_int),
    ('mwidth', c_int),
    ('mheight', c_int),
    ('ndepths', c_int),
    ('depths', POINTER(Depth)),
    ('root_depth', c_int),
    ('root_visual', POINTER(Visual)),
    ('default_gc', GC),
    ('cmap', Colormap),
    ('white_pixel', c_ulong),
    ('black_pixel', c_ulong),
    ('max_maps', c_int),
    ('min_maps', c_int),
    ('backing_store', c_int),
    ('save_unders', c_int),
    ('root_input_mask', c_long),
]
class ScreenFormat(Structure):
    pass
ScreenFormat._fields_ = [
    ('ext_data', POINTER(XExtData)),
    ('depth', c_int),
    ('bits_per_pixel', c_int),
    ('scanline_pad', c_int),
]
class XSetWindowAttributes(Structure):
    pass
XSetWindowAttributes._fields_ = [
    ('background_pixmap', Pixmap),
    ('background_pixel', c_ulong),
    ('border_pixmap', Pixmap),
    ('border_pixel', c_ulong),
    ('bit_gravity', c_int),
    ('win_gravity', c_int),
    ('backing_store', c_int),
    ('backing_planes', c_ulong),
    ('backing_pixel', c_ulong),
    ('save_under', c_int),
    ('event_mask', c_long),
    ('do_not_propagate_mask', c_long),
    ('override_redirect', c_int),
    ('colormap', Colormap),
    ('cursor', Cursor),
]
class XWindowAttributes(Structure):
    pass
XWindowAttributes._fields_ = [
    ('x', c_int),
    ('y', c_int),
    ('width', c_int),
    ('height', c_int),
    ('border_width', c_int),
    ('depth', c_int),
    ('visual', POINTER(Visual)),
    ('root', Window),
    ('c_class', c_int),
    ('bit_gravity', c_int),
    ('win_gravity', c_int),
    ('backing_store', c_int),
    ('backing_planes', c_ulong),
    ('backing_pixel', c_ulong),
    ('save_under', c_int),
    ('colormap', Colormap),
    ('map_installed', c_int),
    ('map_state', c_int),
    ('all_event_masks', c_long),
    ('your_event_mask', c_long),
    ('do_not_propagate_mask', c_long),
    ('override_redirect', c_int),
    ('screen', POINTER(Screen)),
]
class XHostAddress(Structure):
    pass
XHostAddress._fields_ = [
    ('family', c_int),
    ('length', c_int),
    ('address', STRING),
]
class XServerInterpretedAddress(Structure):
    pass
XServerInterpretedAddress._fields_ = [
    ('typelength', c_int),
    ('valuelength', c_int),
    ('type', STRING),
    ('value', STRING),
]
class _XImage(Structure):
    pass
class funcs(Structure):
    pass
funcs._fields_ = [
    ('create_image', CFUNCTYPE(POINTER(_XImage), POINTER(_XDisplay), POINTER(Visual), c_uint, c_int, c_int, STRING, c_uint, c_uint, c_int, c_int)),
    ('destroy_image', CFUNCTYPE(c_int, POINTER(_XImage))),
    ('get_pixel', CFUNCTYPE(c_ulong, POINTER(_XImage), c_int, c_int)),
    ('put_pixel', CFUNCTYPE(c_int, POINTER(_XImage), c_int, c_int, c_ulong)),
    ('sub_image', CFUNCTYPE(POINTER(_XImage), POINTER(_XImage), c_int, c_int, c_uint, c_uint)),
    ('add_pixel', CFUNCTYPE(c_int, POINTER(_XImage), c_long)),
]
_XImage._fields_ = [
    ('width', c_int),
    ('height', c_int),
    ('xoffset', c_int),
    ('format', c_int),
    ('data', STRING),
    ('byte_order', c_int),
    ('bitmap_unit', c_int),
    ('bitmap_bit_order', c_int),
    ('bitmap_pad', c_int),
    ('depth', c_int),
    ('bytes_per_line', c_int),
    ('bits_per_pixel', c_int),
    ('red_mask', c_ulong),
    ('green_mask', c_ulong),
    ('blue_mask', c_ulong),
    ('obdata', XPointer),
    ('f', funcs),
]
XImage = _XImage
class XWindowChanges(Structure):
    pass
XWindowChanges._fields_ = [
    ('x', c_int),
    ('y', c_int),
    ('width', c_int),
    ('height', c_int),
    ('border_width', c_int),
    ('sibling', Window),
    ('stack_mode', c_int),
]
class XColor(Structure):
    pass
XColor._fields_ = [
    ('pixel', c_ulong),
    ('red', c_ushort),
    ('green', c_ushort),
    ('blue', c_ushort),
    ('flags', c_char),
    ('pad', c_char),
]
class XSegment(Structure):
    pass
XSegment._fields_ = [
    ('x1', c_short),
    ('y1', c_short),
    ('x2', c_short),
    ('y2', c_short),
]
class XPoint(Structure):
    pass
XPoint._fields_ = [
    ('x', c_short),
    ('y', c_short),
]
class XRectangle(Structure):
    pass
XRectangle._fields_ = [
    ('x', c_short),
    ('y', c_short),
    ('width', c_ushort),
    ('height', c_ushort),
]
class XArc(Structure):
    pass
XArc._fields_ = [
    ('x', c_short),
    ('y', c_short),
    ('width', c_ushort),
    ('height', c_ushort),
    ('angle1', c_short),
    ('angle2', c_short),
]
class XKeyboardControl(Structure):
    pass
XKeyboardControl._fields_ = [
    ('key_click_percent', c_int),
    ('bell_percent', c_int),
    ('bell_pitch', c_int),
    ('bell_duration', c_int),
    ('led', c_int),
    ('led_mode', c_int),
    ('key', c_int),
    ('auto_repeat_mode', c_int),
]
class XKeyboardState(Structure):
    pass
XKeyboardState._fields_ = [
    ('key_click_percent', c_int),
    ('bell_percent', c_int),
    ('bell_pitch', c_uint),
    ('bell_duration', c_uint),
    ('led_mask', c_ulong),
    ('global_auto_repeat', c_int),
    ('auto_repeats', c_char * 32),
]
class XTimeCoord(Structure):
    pass
XTimeCoord._fields_ = [
    ('time', Time),
    ('x', c_short),
    ('y', c_short),
]
class XModifierKeymap(Structure):
    pass
XModifierKeymap._fields_ = [
    ('max_keypermod', c_int),
    ('modifiermap', POINTER(KeyCode)),
]
class _XPrivate(Structure):
    pass
_XPrivate._fields_ = [
]
class _XrmHashBucketRec(Structure):
    pass
_XrmHashBucketRec._fields_ = [
]
class _4DOT_34(Structure):
    pass
_4DOT_34._fields_ = [
    ('ext_data', POINTER(XExtData)),
    ('private1', POINTER(_XPrivate)),
    ('fd', c_int),
    ('private2', c_int),
    ('proto_major_version', c_int),
    ('proto_minor_version', c_int),
    ('vendor', STRING),
    ('private3', XID),
    ('private4', XID),
    ('private5', XID),
    ('private6', c_int),
    ('resource_alloc', CFUNCTYPE(XID, POINTER(_XDisplay))),
    ('byte_order', c_int),
    ('bitmap_unit', c_int),
    ('bitmap_pad', c_int),
    ('bitmap_bit_order', c_int),
    ('nformats', c_int),
    ('pixmap_format', POINTER(ScreenFormat)),
    ('private8', c_int),
    ('release', c_int),
    ('private9', POINTER(_XPrivate)),
    ('private10', POINTER(_XPrivate)),
    ('qlen', c_int),
    ('last_request_read', c_ulong),
    ('request', c_ulong),
    ('private11', XPointer),
    ('private12', XPointer),
    ('private13', XPointer),
    ('private14', XPointer),
    ('max_request_size', c_uint),
    ('db', POINTER(_XrmHashBucketRec)),
    ('private15', CFUNCTYPE(c_int, POINTER(_XDisplay))),
    ('display_name', STRING),
    ('default_screen', c_int),
    ('nscreens', c_int),
    ('screens', POINTER(Screen)),
    ('motion_buffer', c_ulong),
    ('private16', c_ulong),
    ('min_keycode', c_int),
    ('max_keycode', c_int),
    ('private17', XPointer),
    ('private18', XPointer),
    ('private19', c_int),
    ('xdefaults', STRING),
]
_XPrivDisplay = POINTER(_4DOT_34)
class XKeyEvent(Structure):
    pass
XKeyEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('window', Window),
    ('root', Window),
    ('subwindow', Window),
    ('time', Time),
    ('x', c_int),
    ('y', c_int),
    ('x_root', c_int),
    ('y_root', c_int),
    ('state', c_uint),
    ('keycode', c_uint),
    ('same_screen', c_int),
]
XKeyPressedEvent = XKeyEvent
XKeyReleasedEvent = XKeyEvent
class XButtonEvent(Structure):
    pass
XButtonEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('window', Window),
    ('root', Window),
    ('subwindow', Window),
    ('time', Time),
    ('x', c_int),
    ('y', c_int),
    ('x_root', c_int),
    ('y_root', c_int),
    ('state', c_uint),
    ('button', c_uint),
    ('same_screen', c_int),
]
XButtonPressedEvent = XButtonEvent
XButtonReleasedEvent = XButtonEvent
class XMotionEvent(Structure):
    pass
XMotionEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('window', Window),
    ('root', Window),
    ('subwindow', Window),
    ('time', Time),
    ('x', c_int),
    ('y', c_int),
    ('x_root', c_int),
    ('y_root', c_int),
    ('state', c_uint),
    ('is_hint', c_char),
    ('same_screen', c_int),
]
XPointerMovedEvent = XMotionEvent
class XCrossingEvent(Structure):
    pass
XCrossingEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('window', Window),
    ('root', Window),
    ('subwindow', Window),
    ('time', Time),
    ('x', c_int),
    ('y', c_int),
    ('x_root', c_int),
    ('y_root', c_int),
    ('mode', c_int),
    ('detail', c_int),
    ('same_screen', c_int),
    ('focus', c_int),
    ('state', c_uint),
]
XEnterWindowEvent = XCrossingEvent
XLeaveWindowEvent = XCrossingEvent
class XFocusChangeEvent(Structure):
    pass
XFocusChangeEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('window', Window),
    ('mode', c_int),
    ('detail', c_int),
]
XFocusInEvent = XFocusChangeEvent
XFocusOutEvent = XFocusChangeEvent
class XKeymapEvent(Structure):
    pass
XKeymapEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('window', Window),
    ('key_vector', c_char * 32),
]
class XExposeEvent(Structure):
    pass
XExposeEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('window', Window),
    ('x', c_int),
    ('y', c_int),
    ('width', c_int),
    ('height', c_int),
    ('count', c_int),
]
class XGraphicsExposeEvent(Structure):
    pass
XGraphicsExposeEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('drawable', Drawable),
    ('x', c_int),
    ('y', c_int),
    ('width', c_int),
    ('height', c_int),
    ('count', c_int),
    ('major_code', c_int),
    ('minor_code', c_int),
]
class XNoExposeEvent(Structure):
    pass
XNoExposeEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('drawable', Drawable),
    ('major_code', c_int),
    ('minor_code', c_int),
]
class XVisibilityEvent(Structure):
    pass
XVisibilityEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('window', Window),
    ('state', c_int),
]
class XCreateWindowEvent(Structure):
    pass
XCreateWindowEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('parent', Window),
    ('window', Window),
    ('x', c_int),
    ('y', c_int),
    ('width', c_int),
    ('height', c_int),
    ('border_width', c_int),
    ('override_redirect', c_int),
]
class XDestroyWindowEvent(Structure):
    pass
XDestroyWindowEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('event', Window),
    ('window', Window),
]
class XUnmapEvent(Structure):
    pass
XUnmapEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('event', Window),
    ('window', Window),
    ('from_configure', c_int),
]
class XMapEvent(Structure):
    pass
XMapEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('event', Window),
    ('window', Window),
    ('override_redirect', c_int),
]
class XMapRequestEvent(Structure):
    pass
XMapRequestEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('parent', Window),
    ('window', Window),
]
class XReparentEvent(Structure):
    pass
XReparentEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('event', Window),
    ('window', Window),
    ('parent', Window),
    ('x', c_int),
    ('y', c_int),
    ('override_redirect', c_int),
]
class XConfigureEvent(Structure):
    pass
XConfigureEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('event', Window),
    ('window', Window),
    ('x', c_int),
    ('y', c_int),
    ('width', c_int),
    ('height', c_int),
    ('border_width', c_int),
    ('above', Window),
    ('override_redirect', c_int),
]
class XGravityEvent(Structure):
    pass
XGravityEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('event', Window),
    ('window', Window),
    ('x', c_int),
    ('y', c_int),
]
class XResizeRequestEvent(Structure):
    pass
XResizeRequestEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('window', Window),
    ('width', c_int),
    ('height', c_int),
]
class XConfigureRequestEvent(Structure):
    pass
XConfigureRequestEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('parent', Window),
    ('window', Window),
    ('x', c_int),
    ('y', c_int),
    ('width', c_int),
    ('height', c_int),
    ('border_width', c_int),
    ('above', Window),
    ('detail', c_int),
    ('value_mask', c_ulong),
]
class XCirculateEvent(Structure):
    pass
XCirculateEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('event', Window),
    ('window', Window),
    ('place', c_int),
]
class XCirculateRequestEvent(Structure):
    pass
XCirculateRequestEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('parent', Window),
    ('window', Window),
    ('place', c_int),
]
class XPropertyEvent(Structure):
    pass
XPropertyEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('window', Window),
    ('atom', Atom),
    ('time', Time),
    ('state', c_int),
]
class XSelectionClearEvent(Structure):
    pass
XSelectionClearEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('window', Window),
    ('selection', Atom),
    ('time', Time),
]
class XSelectionRequestEvent(Structure):
    pass
XSelectionRequestEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('owner', Window),
    ('requestor', Window),
    ('selection', Atom),
    ('target', Atom),
    ('property', Atom),
    ('time', Time),
]
class XSelectionEvent(Structure):
    pass
XSelectionEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('requestor', Window),
    ('selection', Atom),
    ('target', Atom),
    ('property', Atom),
    ('time', Time),
]
class XColormapEvent(Structure):
    pass
XColormapEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('window', Window),
    ('colormap', Colormap),
    ('c_new', c_int),
    ('state', c_int),
]
class XClientMessageEvent(Structure):
    pass
class N19XClientMessageEvent4DOT_63E(Union):
    pass
N19XClientMessageEvent4DOT_63E._fields_ = [
    ('b', c_char * 20),
    ('s', c_short * 10),
    ('l', c_long * 5),
]
XClientMessageEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('window', Window),
    ('message_type', Atom),
    ('format', c_int),
    ('data', N19XClientMessageEvent4DOT_63E),
]
class XMappingEvent(Structure):
    pass
XMappingEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('window', Window),
    ('request', c_int),
    ('first_keycode', c_int),
    ('count', c_int),
]
class XErrorEvent(Structure):
    pass
XErrorEvent._fields_ = [
    ('type', c_int),
    ('display', POINTER(Display)),
    ('resourceid', XID),
    ('serial', c_ulong),
    ('error_code', c_ubyte),
    ('request_code', c_ubyte),
    ('minor_code', c_ubyte),
]
class XAnyEvent(Structure):
    pass
XAnyEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('window', Window),
]
class XGenericEvent(Structure):
    pass
XGenericEvent._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('extension', c_int),
    ('evtype', c_int),
]
class XGenericEventCookie(Structure):
    pass
XGenericEventCookie._fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', c_int),
    ('display', POINTER(Display)),
    ('extension', c_int),
    ('evtype', c_int),
    ('cookie', c_uint),
    ('data', c_void_p),
]
class _XEvent(Union):
    pass
XEvent = _XEvent
class XCharStruct(Structure):
    pass
XCharStruct._fields_ = [
    ('lbearing', c_short),
    ('rbearing', c_short),
    ('width', c_short),
    ('ascent', c_short),
    ('descent', c_short),
    ('attributes', c_ushort),
]
class XFontProp(Structure):
    pass
XFontProp._fields_ = [
    ('name', Atom),
    ('card32', c_ulong),
]
class XFontStruct(Structure):
    pass
XFontStruct._fields_ = [
    ('ext_data', POINTER(XExtData)),
    ('fid', Font),
    ('direction', c_uint),
    ('min_char_or_byte2', c_uint),
    ('max_char_or_byte2', c_uint),
    ('min_byte1', c_uint),
    ('max_byte1', c_uint),
    ('all_chars_exist', c_int),
    ('default_char', c_uint),
    ('n_properties', c_int),
    ('properties', POINTER(XFontProp)),
    ('min_bounds', XCharStruct),
    ('max_bounds', XCharStruct),
    ('per_char', POINTER(XCharStruct)),
    ('ascent', c_int),
    ('descent', c_int),
]
class XTextItem(Structure):
    pass
XTextItem._fields_ = [
    ('chars', STRING),
    ('nchars', c_int),
    ('delta', c_int),
    ('font', Font),
]
class XChar2b(Structure):
    pass
XChar2b._fields_ = [
    ('byte1', c_ubyte),
    ('byte2', c_ubyte),
]
class XTextItem16(Structure):
    pass
XTextItem16._fields_ = [
    ('chars', POINTER(XChar2b)),
    ('nchars', c_int),
    ('delta', c_int),
    ('font', Font),
]
class XFontSetExtents(Structure):
    pass
XFontSetExtents._fields_ = [
    ('max_ink_extent', XRectangle),
    ('max_logical_extent', XRectangle),
]
class _XOM(Structure):
    pass
_XOM._fields_ = [
]
XOM = POINTER(_XOM)
class _XOC(Structure):
    pass
XOC = POINTER(_XOC)
XFontSet = POINTER(_XOC)
_XOC._fields_ = [
]
class XmbTextItem(Structure):
    pass
XmbTextItem._fields_ = [
    ('chars', STRING),
    ('nchars', c_int),
    ('delta', c_int),
    ('font_set', XFontSet),
]
class XwcTextItem(Structure):
    pass
XwcTextItem._fields_ = [
    ('chars', WSTRING),
    ('nchars', c_int),
    ('delta', c_int),
    ('font_set', XFontSet),
]
class XOMCharSetList(Structure):
    pass
XOMCharSetList._fields_ = [
    ('charset_count', c_int),
    ('charset_list', POINTER(STRING)),
]

# values for enumeration 'XOrientation'
XOrientation = c_int # enum
class XOMOrientation(Structure):
    pass
XOMOrientation._fields_ = [
    ('num_orientation', c_int),
    ('orientation', POINTER(XOrientation)),
]
class XOMFontInfo(Structure):
    pass
XOMFontInfo._fields_ = [
    ('num_font', c_int),
    ('font_struct_list', POINTER(POINTER(XFontStruct))),
    ('font_name_list', POINTER(STRING)),
]
class _XIM(Structure):
    pass
_XIM._fields_ = [
]
XIM = POINTER(_XIM)
class _XIC(Structure):
    pass
XIC = POINTER(_XIC)
_XIC._fields_ = [
]
XIMProc = CFUNCTYPE(None, XIM, XPointer, XPointer)
XICProc = CFUNCTYPE(c_int, XIC, XPointer, XPointer)
XIDProc = CFUNCTYPE(None, POINTER(Display), XPointer, XPointer)
XIMStyle = c_ulong
class XIMStyles(Structure):
    pass
XIMStyles._fields_ = [
    ('count_styles', c_ushort),
    ('supported_styles', POINTER(XIMStyle)),
]
XVaNestedList = c_void_p
class XIMCallback(Structure):
    pass
XIMCallback._fields_ = [
    ('client_data', XPointer),
    ('callback', XIMProc),
]
class XICCallback(Structure):
    pass
XICCallback._fields_ = [
    ('client_data', XPointer),
    ('callback', XICProc),
]
XIMFeedback = c_ulong
class _XIMText(Structure):
    pass
class N8_XIMText4DOT_86E(Union):
    pass
N8_XIMText4DOT_86E._fields_ = [
    ('multi_byte', STRING),
    ('wide_char', WSTRING),
]
_XIMText._fields_ = [
    ('length', c_ushort),
    ('feedback', POINTER(XIMFeedback)),
    ('encoding_is_wchar', c_int),
    ('string', N8_XIMText4DOT_86E),
]
XIMText = _XIMText
XIMPreeditState = c_ulong
class _XIMPreeditStateNotifyCallbackStruct(Structure):
    pass
_XIMPreeditStateNotifyCallbackStruct._fields_ = [
    ('state', XIMPreeditState),
]
XIMPreeditStateNotifyCallbackStruct = _XIMPreeditStateNotifyCallbackStruct
XIMResetState = c_ulong
XIMStringConversionFeedback = c_ulong
class _XIMStringConversionText(Structure):
    pass
class N24_XIMStringConversionText4DOT_87E(Union):
    pass
N24_XIMStringConversionText4DOT_87E._fields_ = [
    ('mbs', STRING),
    ('wcs', WSTRING),
]
_XIMStringConversionText._fields_ = [
    ('length', c_ushort),
    ('feedback', POINTER(XIMStringConversionFeedback)),
    ('encoding_is_wchar', c_int),
    ('string', N24_XIMStringConversionText4DOT_87E),
]
XIMStringConversionText = _XIMStringConversionText
XIMStringConversionPosition = c_ushort
XIMStringConversionType = c_ushort
XIMStringConversionOperation = c_ushort

# values for enumeration 'XIMCaretDirection'
XIMCaretDirection = c_int # enum
class _XIMStringConversionCallbackStruct(Structure):
    pass
_XIMStringConversionCallbackStruct._fields_ = [
    ('position', XIMStringConversionPosition),
    ('direction', XIMCaretDirection),
    ('operation', XIMStringConversionOperation),
    ('factor', c_ushort),
    ('text', POINTER(XIMStringConversionText)),
]
XIMStringConversionCallbackStruct = _XIMStringConversionCallbackStruct
class _XIMPreeditDrawCallbackStruct(Structure):
    pass
_XIMPreeditDrawCallbackStruct._fields_ = [
    ('caret', c_int),
    ('chg_first', c_int),
    ('chg_length', c_int),
    ('text', POINTER(XIMText)),
]
XIMPreeditDrawCallbackStruct = _XIMPreeditDrawCallbackStruct

# values for enumeration 'XIMCaretStyle'
XIMCaretStyle = c_int # enum
class _XIMPreeditCaretCallbackStruct(Structure):
    pass
_XIMPreeditCaretCallbackStruct._fields_ = [
    ('position', c_int),
    ('direction', XIMCaretDirection),
    ('style', XIMCaretStyle),
]
XIMPreeditCaretCallbackStruct = _XIMPreeditCaretCallbackStruct

# values for enumeration 'XIMStatusDataType'
XIMStatusDataType = c_int # enum
class _XIMStatusDrawCallbackStruct(Structure):
    pass
class N28_XIMStatusDrawCallbackStruct4DOT_91E(Union):
    pass
N28_XIMStatusDrawCallbackStruct4DOT_91E._fields_ = [
    ('text', POINTER(XIMText)),
    ('bitmap', Pixmap),
]
_XIMStatusDrawCallbackStruct._fields_ = [
    ('type', XIMStatusDataType),
    ('data', N28_XIMStatusDrawCallbackStruct4DOT_91E),
]
XIMStatusDrawCallbackStruct = _XIMStatusDrawCallbackStruct
class _XIMHotKeyTrigger(Structure):
    pass
_XIMHotKeyTrigger._fields_ = [
    ('keysym', KeySym),
    ('modifier', c_int),
    ('modifier_mask', c_int),
]
XIMHotKeyTrigger = _XIMHotKeyTrigger
class _XIMHotKeyTriggers(Structure):
    pass
_XIMHotKeyTriggers._fields_ = [
    ('num_hot_key', c_int),
    ('key', POINTER(XIMHotKeyTrigger)),
]
XIMHotKeyTriggers = _XIMHotKeyTriggers
XIMHotKeyState = c_ulong
class XIMValuesList(Structure):
    pass
XIMValuesList._fields_ = [
    ('count_values', c_ushort),
    ('supported_values', POINTER(STRING)),
]
_Xdebug = (c_int).in_dll(_libraries['libX11.so.6'], '_Xdebug')
XLoadQueryFont = _libraries['libX11.so.6'].XLoadQueryFont
XLoadQueryFont.restype = POINTER(XFontStruct)
XLoadQueryFont.argtypes = [POINTER(Display), STRING]
XQueryFont = _libraries['libX11.so.6'].XQueryFont
XQueryFont.restype = POINTER(XFontStruct)
XQueryFont.argtypes = [POINTER(Display), XID]
XGetMotionEvents = _libraries['libX11.so.6'].XGetMotionEvents
XGetMotionEvents.restype = POINTER(XTimeCoord)
XGetMotionEvents.argtypes = [POINTER(Display), Window, Time, Time, POINTER(c_int)]
XDeleteModifiermapEntry = _libraries['libX11.so.6'].XDeleteModifiermapEntry
XDeleteModifiermapEntry.restype = POINTER(XModifierKeymap)
XDeleteModifiermapEntry.argtypes = [POINTER(XModifierKeymap), KeyCode, c_int]
XGetModifierMapping = _libraries['libX11.so.6'].XGetModifierMapping
XGetModifierMapping.restype = POINTER(XModifierKeymap)
XGetModifierMapping.argtypes = [POINTER(Display)]
XInsertModifiermapEntry = _libraries['libX11.so.6'].XInsertModifiermapEntry
XInsertModifiermapEntry.restype = POINTER(XModifierKeymap)
XInsertModifiermapEntry.argtypes = [POINTER(XModifierKeymap), KeyCode, c_int]
XNewModifiermap = _libraries['libX11.so.6'].XNewModifiermap
XNewModifiermap.restype = POINTER(XModifierKeymap)
XNewModifiermap.argtypes = [c_int]
XCreateImage = _libraries['libX11.so.6'].XCreateImage
XCreateImage.restype = POINTER(XImage)
XCreateImage.argtypes = [POINTER(Display), POINTER(Visual), c_uint, c_int, c_int, STRING, c_uint, c_uint, c_int, c_int]
XInitImage = _libraries['libX11.so.6'].XInitImage
XInitImage.restype = c_int
XInitImage.argtypes = [POINTER(XImage)]
XGetImage = _libraries['libX11.so.6'].XGetImage
XGetImage.restype = POINTER(XImage)
XGetImage.argtypes = [POINTER(Display), Drawable, c_int, c_int, c_uint, c_uint, c_ulong, c_int]
XGetSubImage = _libraries['libX11.so.6'].XGetSubImage
XGetSubImage.restype = POINTER(XImage)
XGetSubImage.argtypes = [POINTER(Display), Drawable, c_int, c_int, c_uint, c_uint, c_ulong, c_int, POINTER(XImage), c_int, c_int]
XOpenDisplay = _libraries['libX11.so.6'].XOpenDisplay
XOpenDisplay.restype = POINTER(Display)
XOpenDisplay.argtypes = [STRING]
XrmInitialize = _libraries['libX11.so.6'].XrmInitialize
XrmInitialize.restype = None
XrmInitialize.argtypes = []
XFetchBytes = _libraries['libX11.so.6'].XFetchBytes
XFetchBytes.restype = STRING
XFetchBytes.argtypes = [POINTER(Display), POINTER(c_int)]
XFetchBuffer = _libraries['libX11.so.6'].XFetchBuffer
XFetchBuffer.restype = STRING
XFetchBuffer.argtypes = [POINTER(Display), POINTER(c_int), c_int]
XGetAtomName = _libraries['libX11.so.6'].XGetAtomName
XGetAtomName.restype = STRING
XGetAtomName.argtypes = [POINTER(Display), Atom]
XGetAtomNames = _libraries['libX11.so.6'].XGetAtomNames
XGetAtomNames.restype = c_int
XGetAtomNames.argtypes = [POINTER(Display), POINTER(Atom), c_int, POINTER(STRING)]
XGetDefault = _libraries['libX11.so.6'].XGetDefault
XGetDefault.restype = STRING
XGetDefault.argtypes = [POINTER(Display), STRING, STRING]
XDisplayName = _libraries['libX11.so.6'].XDisplayName
XDisplayName.restype = STRING
XDisplayName.argtypes = [STRING]
XKeysymToString = _libraries['libX11.so.6'].XKeysymToString
XKeysymToString.restype = STRING
XKeysymToString.argtypes = [KeySym]
XSynchronize = _libraries['libX11.so.6'].XSynchronize
XSynchronize.restype = CFUNCTYPE(c_int, POINTER(Display))
XSynchronize.argtypes = [POINTER(Display), c_int]
XSetAfterFunction = _libraries['libX11.so.6'].XSetAfterFunction
XSetAfterFunction.restype = CFUNCTYPE(c_int, POINTER(Display))
XSetAfterFunction.argtypes = [POINTER(Display), CFUNCTYPE(c_int, POINTER(Display))]
XInternAtom = _libraries['libX11.so.6'].XInternAtom
XInternAtom.restype = Atom
XInternAtom.argtypes = [POINTER(Display), STRING, c_int]
XInternAtoms = _libraries['libX11.so.6'].XInternAtoms
XInternAtoms.restype = c_int
XInternAtoms.argtypes = [POINTER(Display), POINTER(STRING), c_int, c_int, POINTER(Atom)]
XCopyColormapAndFree = _libraries['libX11.so.6'].XCopyColormapAndFree
XCopyColormapAndFree.restype = Colormap
XCopyColormapAndFree.argtypes = [POINTER(Display), Colormap]
XCreateColormap = _libraries['libX11.so.6'].XCreateColormap
XCreateColormap.restype = Colormap
XCreateColormap.argtypes = [POINTER(Display), Window, POINTER(Visual), c_int]
XCreatePixmapCursor = _libraries['libX11.so.6'].XCreatePixmapCursor
XCreatePixmapCursor.restype = Cursor
XCreatePixmapCursor.argtypes = [POINTER(Display), Pixmap, Pixmap, POINTER(XColor), POINTER(XColor), c_uint, c_uint]
XCreateGlyphCursor = _libraries['libX11.so.6'].XCreateGlyphCursor
XCreateGlyphCursor.restype = Cursor
XCreateGlyphCursor.argtypes = [POINTER(Display), Font, Font, c_uint, c_uint, POINTER(XColor), POINTER(XColor)]
XCreateFontCursor = _libraries['libX11.so.6'].XCreateFontCursor
XCreateFontCursor.restype = Cursor
XCreateFontCursor.argtypes = [POINTER(Display), c_uint]
XLoadFont = _libraries['libX11.so.6'].XLoadFont
XLoadFont.restype = Font
XLoadFont.argtypes = [POINTER(Display), STRING]
XCreateGC = _libraries['libX11.so.6'].XCreateGC
XCreateGC.restype = GC
XCreateGC.argtypes = [POINTER(Display), Drawable, c_ulong, POINTER(XGCValues)]
XGContextFromGC = _libraries['libX11.so.6'].XGContextFromGC
XGContextFromGC.restype = GContext
XGContextFromGC.argtypes = [GC]
XFlushGC = _libraries['libX11.so.6'].XFlushGC
XFlushGC.restype = None
XFlushGC.argtypes = [POINTER(Display), GC]
XCreatePixmap = _libraries['libX11.so.6'].XCreatePixmap
XCreatePixmap.restype = Pixmap
XCreatePixmap.argtypes = [POINTER(Display), Drawable, c_uint, c_uint, c_uint]
XCreateBitmapFromData = _libraries['libX11.so.6'].XCreateBitmapFromData
XCreateBitmapFromData.restype = Pixmap
XCreateBitmapFromData.argtypes = [POINTER(Display), Drawable, STRING, c_uint, c_uint]
XCreatePixmapFromBitmapData = _libraries['libX11.so.6'].XCreatePixmapFromBitmapData
XCreatePixmapFromBitmapData.restype = Pixmap
XCreatePixmapFromBitmapData.argtypes = [POINTER(Display), Drawable, STRING, c_uint, c_uint, c_ulong, c_ulong, c_uint]
XCreateSimpleWindow = _libraries['libX11.so.6'].XCreateSimpleWindow
XCreateSimpleWindow.restype = Window
XCreateSimpleWindow.argtypes = [POINTER(Display), Window, c_int, c_int, c_uint, c_uint, c_uint, c_ulong, c_ulong]
XGetSelectionOwner = _libraries['libX11.so.6'].XGetSelectionOwner
XGetSelectionOwner.restype = Window
XGetSelectionOwner.argtypes = [POINTER(Display), Atom]
XCreateWindow = _libraries['libX11.so.6'].XCreateWindow
XCreateWindow.restype = Window
XCreateWindow.argtypes = [POINTER(Display), Window, c_int, c_int, c_uint, c_uint, c_uint, c_int, c_uint, POINTER(Visual), c_ulong, POINTER(XSetWindowAttributes)]
XListInstalledColormaps = _libraries['libX11.so.6'].XListInstalledColormaps
XListInstalledColormaps.restype = POINTER(Colormap)
XListInstalledColormaps.argtypes = [POINTER(Display), Window, POINTER(c_int)]
XListFonts = _libraries['libX11.so.6'].XListFonts
XListFonts.restype = POINTER(STRING)
XListFonts.argtypes = [POINTER(Display), STRING, c_int, POINTER(c_int)]
XListFontsWithInfo = _libraries['libX11.so.6'].XListFontsWithInfo
XListFontsWithInfo.restype = POINTER(STRING)
XListFontsWithInfo.argtypes = [POINTER(Display), STRING, c_int, POINTER(c_int), POINTER(POINTER(XFontStruct))]
XGetFontPath = _libraries['libX11.so.6'].XGetFontPath
XGetFontPath.restype = POINTER(STRING)
XGetFontPath.argtypes = [POINTER(Display), POINTER(c_int)]
XListExtensions = _libraries['libX11.so.6'].XListExtensions
XListExtensions.restype = POINTER(STRING)
XListExtensions.argtypes = [POINTER(Display), POINTER(c_int)]
XListProperties = _libraries['libX11.so.6'].XListProperties
XListProperties.restype = POINTER(Atom)
XListProperties.argtypes = [POINTER(Display), Window, POINTER(c_int)]
XListHosts = _libraries['libX11.so.6'].XListHosts
XListHosts.restype = POINTER(XHostAddress)
XListHosts.argtypes = [POINTER(Display), POINTER(c_int), POINTER(c_int)]
XKeycodeToKeysym = _libraries['libX11.so.6'].XKeycodeToKeysym
XKeycodeToKeysym.restype = KeySym
XKeycodeToKeysym.argtypes = [POINTER(Display), KeyCode, c_int]
XLookupKeysym = _libraries['libX11.so.6'].XLookupKeysym
XLookupKeysym.restype = KeySym
XLookupKeysym.argtypes = [POINTER(XKeyEvent), c_int]
XGetKeyboardMapping = _libraries['libX11.so.6'].XGetKeyboardMapping
XGetKeyboardMapping.restype = POINTER(KeySym)
XGetKeyboardMapping.argtypes = [POINTER(Display), KeyCode, c_int, POINTER(c_int)]
XStringToKeysym = _libraries['libX11.so.6'].XStringToKeysym
XStringToKeysym.restype = KeySym
XStringToKeysym.argtypes = [STRING]
XMaxRequestSize = _libraries['libX11.so.6'].XMaxRequestSize
XMaxRequestSize.restype = c_long
XMaxRequestSize.argtypes = [POINTER(Display)]
XExtendedMaxRequestSize = _libraries['libX11.so.6'].XExtendedMaxRequestSize
XExtendedMaxRequestSize.restype = c_long
XExtendedMaxRequestSize.argtypes = [POINTER(Display)]
XResourceManagerString = _libraries['libX11.so.6'].XResourceManagerString
XResourceManagerString.restype = STRING
XResourceManagerString.argtypes = [POINTER(Display)]
XScreenResourceString = _libraries['libX11.so.6'].XScreenResourceString
XScreenResourceString.restype = STRING
XScreenResourceString.argtypes = [POINTER(Screen)]
XDisplayMotionBufferSize = _libraries['libX11.so.6'].XDisplayMotionBufferSize
XDisplayMotionBufferSize.restype = c_ulong
XDisplayMotionBufferSize.argtypes = [POINTER(Display)]
XVisualIDFromVisual = _libraries['libX11.so.6'].XVisualIDFromVisual
XVisualIDFromVisual.restype = VisualID
XVisualIDFromVisual.argtypes = [POINTER(Visual)]
XInitThreads = _libraries['libX11.so.6'].XInitThreads
XInitThreads.restype = c_int
XInitThreads.argtypes = []
XLockDisplay = _libraries['libX11.so.6'].XLockDisplay
XLockDisplay.restype = None
XLockDisplay.argtypes = [POINTER(Display)]
XUnlockDisplay = _libraries['libX11.so.6'].XUnlockDisplay
XUnlockDisplay.restype = None
XUnlockDisplay.argtypes = [POINTER(Display)]
XInitExtension = _libraries['libX11.so.6'].XInitExtension
XInitExtension.restype = POINTER(XExtCodes)
XInitExtension.argtypes = [POINTER(Display), STRING]
XAddExtension = _libraries['libX11.so.6'].XAddExtension
XAddExtension.restype = POINTER(XExtCodes)
XAddExtension.argtypes = [POINTER(Display)]
XFindOnExtensionList = _libraries['libX11.so.6'].XFindOnExtensionList
XFindOnExtensionList.restype = POINTER(XExtData)
XFindOnExtensionList.argtypes = [POINTER(POINTER(XExtData)), c_int]
class XEDataObject(Union):
    pass
XEDataObject._fields_ = [
    ('display', POINTER(Display)),
    ('gc', GC),
    ('visual', POINTER(Visual)),
    ('screen', POINTER(Screen)),
    ('pixmap_format', POINTER(ScreenFormat)),
    ('font', POINTER(XFontStruct)),
]
XEHeadOfExtensionList = _libraries['libX11.so.6'].XEHeadOfExtensionList
XEHeadOfExtensionList.restype = POINTER(POINTER(XExtData))
XEHeadOfExtensionList.argtypes = [XEDataObject]
XRootWindow = _libraries['libX11.so.6'].XRootWindow
XRootWindow.restype = Window
XRootWindow.argtypes = [POINTER(Display), c_int]
XDefaultRootWindow = _libraries['libX11.so.6'].XDefaultRootWindow
XDefaultRootWindow.restype = Window
XDefaultRootWindow.argtypes = [POINTER(Display)]
XRootWindowOfScreen = _libraries['libX11.so.6'].XRootWindowOfScreen
XRootWindowOfScreen.restype = Window
XRootWindowOfScreen.argtypes = [POINTER(Screen)]
XDefaultVisual = _libraries['libX11.so.6'].XDefaultVisual
XDefaultVisual.restype = POINTER(Visual)
XDefaultVisual.argtypes = [POINTER(Display), c_int]
XDefaultVisualOfScreen = _libraries['libX11.so.6'].XDefaultVisualOfScreen
XDefaultVisualOfScreen.restype = POINTER(Visual)
XDefaultVisualOfScreen.argtypes = [POINTER(Screen)]
XDefaultGC = _libraries['libX11.so.6'].XDefaultGC
XDefaultGC.restype = GC
XDefaultGC.argtypes = [POINTER(Display), c_int]
XDefaultGCOfScreen = _libraries['libX11.so.6'].XDefaultGCOfScreen
XDefaultGCOfScreen.restype = GC
XDefaultGCOfScreen.argtypes = [POINTER(Screen)]
XBlackPixel = _libraries['libX11.so.6'].XBlackPixel
XBlackPixel.restype = c_ulong
XBlackPixel.argtypes = [POINTER(Display), c_int]
XWhitePixel = _libraries['libX11.so.6'].XWhitePixel
XWhitePixel.restype = c_ulong
XWhitePixel.argtypes = [POINTER(Display), c_int]
XAllPlanes = _libraries['libX11.so.6'].XAllPlanes
XAllPlanes.restype = c_ulong
XAllPlanes.argtypes = []
XBlackPixelOfScreen = _libraries['libX11.so.6'].XBlackPixelOfScreen
XBlackPixelOfScreen.restype = c_ulong
XBlackPixelOfScreen.argtypes = [POINTER(Screen)]
XWhitePixelOfScreen = _libraries['libX11.so.6'].XWhitePixelOfScreen
XWhitePixelOfScreen.restype = c_ulong
XWhitePixelOfScreen.argtypes = [POINTER(Screen)]
XNextRequest = _libraries['libX11.so.6'].XNextRequest
XNextRequest.restype = c_ulong
XNextRequest.argtypes = [POINTER(Display)]
XLastKnownRequestProcessed = _libraries['libX11.so.6'].XLastKnownRequestProcessed
XLastKnownRequestProcessed.restype = c_ulong
XLastKnownRequestProcessed.argtypes = [POINTER(Display)]
XServerVendor = _libraries['libX11.so.6'].XServerVendor
XServerVendor.restype = STRING
XServerVendor.argtypes = [POINTER(Display)]
XDisplayString = _libraries['libX11.so.6'].XDisplayString
XDisplayString.restype = STRING
XDisplayString.argtypes = [POINTER(Display)]
XDefaultColormap = _libraries['libX11.so.6'].XDefaultColormap
XDefaultColormap.restype = Colormap
XDefaultColormap.argtypes = [POINTER(Display), c_int]
XDefaultColormapOfScreen = _libraries['libX11.so.6'].XDefaultColormapOfScreen
XDefaultColormapOfScreen.restype = Colormap
XDefaultColormapOfScreen.argtypes = [POINTER(Screen)]
XDisplayOfScreen = _libraries['libX11.so.6'].XDisplayOfScreen
XDisplayOfScreen.restype = POINTER(Display)
XDisplayOfScreen.argtypes = [POINTER(Screen)]
XScreenOfDisplay = _libraries['libX11.so.6'].XScreenOfDisplay
XScreenOfDisplay.restype = POINTER(Screen)
XScreenOfDisplay.argtypes = [POINTER(Display), c_int]
XDefaultScreenOfDisplay = _libraries['libX11.so.6'].XDefaultScreenOfDisplay
XDefaultScreenOfDisplay.restype = POINTER(Screen)
XDefaultScreenOfDisplay.argtypes = [POINTER(Display)]
XEventMaskOfScreen = _libraries['libX11.so.6'].XEventMaskOfScreen
XEventMaskOfScreen.restype = c_long
XEventMaskOfScreen.argtypes = [POINTER(Screen)]
XScreenNumberOfScreen = _libraries['libX11.so.6'].XScreenNumberOfScreen
XScreenNumberOfScreen.restype = c_int
XScreenNumberOfScreen.argtypes = [POINTER(Screen)]
XErrorHandler = CFUNCTYPE(c_int, POINTER(Display), POINTER(XErrorEvent))
XSetErrorHandler = _libraries['libX11.so.6'].XSetErrorHandler
XSetErrorHandler.restype = XErrorHandler
XSetErrorHandler.argtypes = [XErrorHandler]
XIOErrorHandler = CFUNCTYPE(c_int, POINTER(Display))
XSetIOErrorHandler = _libraries['libX11.so.6'].XSetIOErrorHandler
XSetIOErrorHandler.restype = XIOErrorHandler
XSetIOErrorHandler.argtypes = [XIOErrorHandler]
XListPixmapFormats = _libraries['libX11.so.6'].XListPixmapFormats
XListPixmapFormats.restype = POINTER(XPixmapFormatValues)
XListPixmapFormats.argtypes = [POINTER(Display), POINTER(c_int)]
XListDepths = _libraries['libX11.so.6'].XListDepths
XListDepths.restype = POINTER(c_int)
XListDepths.argtypes = [POINTER(Display), c_int, POINTER(c_int)]
XReconfigureWMWindow = _libraries['libX11.so.6'].XReconfigureWMWindow
XReconfigureWMWindow.restype = c_int
XReconfigureWMWindow.argtypes = [POINTER(Display), Window, c_int, c_uint, POINTER(XWindowChanges)]
XGetWMProtocols = _libraries['libX11.so.6'].XGetWMProtocols
XGetWMProtocols.restype = c_int
XGetWMProtocols.argtypes = [POINTER(Display), Window, POINTER(POINTER(Atom)), POINTER(c_int)]
XSetWMProtocols = _libraries['libX11.so.6'].XSetWMProtocols
XSetWMProtocols.restype = c_int
XSetWMProtocols.argtypes = [POINTER(Display), Window, POINTER(Atom), c_int]
XIconifyWindow = _libraries['libX11.so.6'].XIconifyWindow
XIconifyWindow.restype = c_int
XIconifyWindow.argtypes = [POINTER(Display), Window, c_int]
XWithdrawWindow = _libraries['libX11.so.6'].XWithdrawWindow
XWithdrawWindow.restype = c_int
XWithdrawWindow.argtypes = [POINTER(Display), Window, c_int]
XGetCommand = _libraries['libX11.so.6'].XGetCommand
XGetCommand.restype = c_int
XGetCommand.argtypes = [POINTER(Display), Window, POINTER(POINTER(STRING)), POINTER(c_int)]
XGetWMColormapWindows = _libraries['libX11.so.6'].XGetWMColormapWindows
XGetWMColormapWindows.restype = c_int
XGetWMColormapWindows.argtypes = [POINTER(Display), Window, POINTER(POINTER(Window)), POINTER(c_int)]
XSetWMColormapWindows = _libraries['libX11.so.6'].XSetWMColormapWindows
XSetWMColormapWindows.restype = c_int
XSetWMColormapWindows.argtypes = [POINTER(Display), Window, POINTER(Window), c_int]
XFreeStringList = _libraries['libX11.so.6'].XFreeStringList
XFreeStringList.restype = None
XFreeStringList.argtypes = [POINTER(STRING)]
XSetTransientForHint = _libraries['libX11.so.6'].XSetTransientForHint
XSetTransientForHint.restype = c_int
XSetTransientForHint.argtypes = [POINTER(Display), Window, Window]
XActivateScreenSaver = _libraries['libX11.so.6'].XActivateScreenSaver
XActivateScreenSaver.restype = c_int
XActivateScreenSaver.argtypes = [POINTER(Display)]
XAddHost = _libraries['libX11.so.6'].XAddHost
XAddHost.restype = c_int
XAddHost.argtypes = [POINTER(Display), POINTER(XHostAddress)]
XAddHosts = _libraries['libX11.so.6'].XAddHosts
XAddHosts.restype = c_int
XAddHosts.argtypes = [POINTER(Display), POINTER(XHostAddress), c_int]
XAddToExtensionList = _libraries['libX11.so.6'].XAddToExtensionList
XAddToExtensionList.restype = c_int
XAddToExtensionList.argtypes = [POINTER(POINTER(_XExtData)), POINTER(XExtData)]
XAddToSaveSet = _libraries['libX11.so.6'].XAddToSaveSet
XAddToSaveSet.restype = c_int
XAddToSaveSet.argtypes = [POINTER(Display), Window]
XAllocColor = _libraries['libX11.so.6'].XAllocColor
XAllocColor.restype = c_int
XAllocColor.argtypes = [POINTER(Display), Colormap, POINTER(XColor)]
XAllocColorCells = _libraries['libX11.so.6'].XAllocColorCells
XAllocColorCells.restype = c_int
XAllocColorCells.argtypes = [POINTER(Display), Colormap, c_int, POINTER(c_ulong), c_uint, POINTER(c_ulong), c_uint]
XAllocColorPlanes = _libraries['libX11.so.6'].XAllocColorPlanes
XAllocColorPlanes.restype = c_int
XAllocColorPlanes.argtypes = [POINTER(Display), Colormap, c_int, POINTER(c_ulong), c_int, c_int, c_int, c_int, POINTER(c_ulong), POINTER(c_ulong), POINTER(c_ulong)]
XAllocNamedColor = _libraries['libX11.so.6'].XAllocNamedColor
XAllocNamedColor.restype = c_int
XAllocNamedColor.argtypes = [POINTER(Display), Colormap, STRING, POINTER(XColor), POINTER(XColor)]
XAllowEvents = _libraries['libX11.so.6'].XAllowEvents
XAllowEvents.restype = c_int
XAllowEvents.argtypes = [POINTER(Display), c_int, Time]
XAutoRepeatOff = _libraries['libX11.so.6'].XAutoRepeatOff
XAutoRepeatOff.restype = c_int
XAutoRepeatOff.argtypes = [POINTER(Display)]
XAutoRepeatOn = _libraries['libX11.so.6'].XAutoRepeatOn
XAutoRepeatOn.restype = c_int
XAutoRepeatOn.argtypes = [POINTER(Display)]
XBell = _libraries['libX11.so.6'].XBell
XBell.restype = c_int
XBell.argtypes = [POINTER(Display), c_int]
XBitmapBitOrder = _libraries['libX11.so.6'].XBitmapBitOrder
XBitmapBitOrder.restype = c_int
XBitmapBitOrder.argtypes = [POINTER(Display)]
XBitmapPad = _libraries['libX11.so.6'].XBitmapPad
XBitmapPad.restype = c_int
XBitmapPad.argtypes = [POINTER(Display)]
XBitmapUnit = _libraries['libX11.so.6'].XBitmapUnit
XBitmapUnit.restype = c_int
XBitmapUnit.argtypes = [POINTER(Display)]
XCellsOfScreen = _libraries['libX11.so.6'].XCellsOfScreen
XCellsOfScreen.restype = c_int
XCellsOfScreen.argtypes = [POINTER(Screen)]
XChangeActivePointerGrab = _libraries['libX11.so.6'].XChangeActivePointerGrab
XChangeActivePointerGrab.restype = c_int
XChangeActivePointerGrab.argtypes = [POINTER(Display), c_uint, Cursor, Time]
XChangeGC = _libraries['libX11.so.6'].XChangeGC
XChangeGC.restype = c_int
XChangeGC.argtypes = [POINTER(Display), GC, c_ulong, POINTER(XGCValues)]
XChangeKeyboardControl = _libraries['libX11.so.6'].XChangeKeyboardControl
XChangeKeyboardControl.restype = c_int
XChangeKeyboardControl.argtypes = [POINTER(Display), c_ulong, POINTER(XKeyboardControl)]
XChangeKeyboardMapping = _libraries['libX11.so.6'].XChangeKeyboardMapping
XChangeKeyboardMapping.restype = c_int
XChangeKeyboardMapping.argtypes = [POINTER(Display), c_int, c_int, POINTER(KeySym), c_int]
XChangePointerControl = _libraries['libX11.so.6'].XChangePointerControl
XChangePointerControl.restype = c_int
XChangePointerControl.argtypes = [POINTER(Display), c_int, c_int, c_int, c_int, c_int]
XChangeProperty = _libraries['libX11.so.6'].XChangeProperty
XChangeProperty.restype = c_int
XChangeProperty.argtypes = [POINTER(Display), Window, Atom, Atom, c_int, c_int, POINTER(c_ubyte), c_int]
XChangeSaveSet = _libraries['libX11.so.6'].XChangeSaveSet
XChangeSaveSet.restype = c_int
XChangeSaveSet.argtypes = [POINTER(Display), Window, c_int]
XChangeWindowAttributes = _libraries['libX11.so.6'].XChangeWindowAttributes
XChangeWindowAttributes.restype = c_int
XChangeWindowAttributes.argtypes = [POINTER(Display), Window, c_ulong, POINTER(XSetWindowAttributes)]
XCheckIfEvent = _libraries['libX11.so.6'].XCheckIfEvent
XCheckIfEvent.restype = c_int
XCheckIfEvent.argtypes = [POINTER(Display), POINTER(XEvent), CFUNCTYPE(c_int, POINTER(Display), POINTER(XEvent), XPointer), XPointer]
XCheckMaskEvent = _libraries['libX11.so.6'].XCheckMaskEvent
XCheckMaskEvent.restype = c_int
XCheckMaskEvent.argtypes = [POINTER(Display), c_long, POINTER(XEvent)]
XCheckTypedEvent = _libraries['libX11.so.6'].XCheckTypedEvent
XCheckTypedEvent.restype = c_int
XCheckTypedEvent.argtypes = [POINTER(Display), c_int, POINTER(XEvent)]
XCheckTypedWindowEvent = _libraries['libX11.so.6'].XCheckTypedWindowEvent
XCheckTypedWindowEvent.restype = c_int
XCheckTypedWindowEvent.argtypes = [POINTER(Display), Window, c_int, POINTER(XEvent)]
XCheckWindowEvent = _libraries['libX11.so.6'].XCheckWindowEvent
XCheckWindowEvent.restype = c_int
XCheckWindowEvent.argtypes = [POINTER(Display), Window, c_long, POINTER(XEvent)]
XCirculateSubwindows = _libraries['libX11.so.6'].XCirculateSubwindows
XCirculateSubwindows.restype = c_int
XCirculateSubwindows.argtypes = [POINTER(Display), Window, c_int]
XCirculateSubwindowsDown = _libraries['libX11.so.6'].XCirculateSubwindowsDown
XCirculateSubwindowsDown.restype = c_int
XCirculateSubwindowsDown.argtypes = [POINTER(Display), Window]
XCirculateSubwindowsUp = _libraries['libX11.so.6'].XCirculateSubwindowsUp
XCirculateSubwindowsUp.restype = c_int
XCirculateSubwindowsUp.argtypes = [POINTER(Display), Window]
XClearArea = _libraries['libX11.so.6'].XClearArea
XClearArea.restype = c_int
XClearArea.argtypes = [POINTER(Display), Window, c_int, c_int, c_uint, c_uint, c_int]
XClearWindow = _libraries['libX11.so.6'].XClearWindow
XClearWindow.restype = c_int
XClearWindow.argtypes = [POINTER(Display), Window]
XCloseDisplay = _libraries['libX11.so.6'].XCloseDisplay
XCloseDisplay.restype = c_int
XCloseDisplay.argtypes = [POINTER(Display)]
XConfigureWindow = _libraries['libX11.so.6'].XConfigureWindow
XConfigureWindow.restype = c_int
XConfigureWindow.argtypes = [POINTER(Display), Window, c_uint, POINTER(XWindowChanges)]
XConnectionNumber = _libraries['libX11.so.6'].XConnectionNumber
XConnectionNumber.restype = c_int
XConnectionNumber.argtypes = [POINTER(Display)]
XConvertSelection = _libraries['libX11.so.6'].XConvertSelection
XConvertSelection.restype = c_int
XConvertSelection.argtypes = [POINTER(Display), Atom, Atom, Atom, Window, Time]
XCopyArea = _libraries['libX11.so.6'].XCopyArea
XCopyArea.restype = c_int
XCopyArea.argtypes = [POINTER(Display), Drawable, Drawable, GC, c_int, c_int, c_uint, c_uint, c_int, c_int]
XCopyGC = _libraries['libX11.so.6'].XCopyGC
XCopyGC.restype = c_int
XCopyGC.argtypes = [POINTER(Display), GC, c_ulong, GC]
XCopyPlane = _libraries['libX11.so.6'].XCopyPlane
XCopyPlane.restype = c_int
XCopyPlane.argtypes = [POINTER(Display), Drawable, Drawable, GC, c_int, c_int, c_uint, c_uint, c_int, c_int, c_ulong]
XDefaultDepth = _libraries['libX11.so.6'].XDefaultDepth
XDefaultDepth.restype = c_int
XDefaultDepth.argtypes = [POINTER(Display), c_int]
XDefaultDepthOfScreen = _libraries['libX11.so.6'].XDefaultDepthOfScreen
XDefaultDepthOfScreen.restype = c_int
XDefaultDepthOfScreen.argtypes = [POINTER(Screen)]
XDefaultScreen = _libraries['libX11.so.6'].XDefaultScreen
XDefaultScreen.restype = c_int
XDefaultScreen.argtypes = [POINTER(Display)]
XDefineCursor = _libraries['libX11.so.6'].XDefineCursor
XDefineCursor.restype = c_int
XDefineCursor.argtypes = [POINTER(Display), Window, Cursor]
XDeleteProperty = _libraries['libX11.so.6'].XDeleteProperty
XDeleteProperty.restype = c_int
XDeleteProperty.argtypes = [POINTER(Display), Window, Atom]
XDestroyWindow = _libraries['libX11.so.6'].XDestroyWindow
XDestroyWindow.restype = c_int
XDestroyWindow.argtypes = [POINTER(Display), Window]
XDestroySubwindows = _libraries['libX11.so.6'].XDestroySubwindows
XDestroySubwindows.restype = c_int
XDestroySubwindows.argtypes = [POINTER(Display), Window]
XDoesBackingStore = _libraries['libX11.so.6'].XDoesBackingStore
XDoesBackingStore.restype = c_int
XDoesBackingStore.argtypes = [POINTER(Screen)]
XDoesSaveUnders = _libraries['libX11.so.6'].XDoesSaveUnders
XDoesSaveUnders.restype = c_int
XDoesSaveUnders.argtypes = [POINTER(Screen)]
XDisableAccessControl = _libraries['libX11.so.6'].XDisableAccessControl
XDisableAccessControl.restype = c_int
XDisableAccessControl.argtypes = [POINTER(Display)]
XDisplayCells = _libraries['libX11.so.6'].XDisplayCells
XDisplayCells.restype = c_int
XDisplayCells.argtypes = [POINTER(Display), c_int]
XDisplayHeight = _libraries['libX11.so.6'].XDisplayHeight
XDisplayHeight.restype = c_int
XDisplayHeight.argtypes = [POINTER(Display), c_int]
XDisplayHeightMM = _libraries['libX11.so.6'].XDisplayHeightMM
XDisplayHeightMM.restype = c_int
XDisplayHeightMM.argtypes = [POINTER(Display), c_int]
XDisplayKeycodes = _libraries['libX11.so.6'].XDisplayKeycodes
XDisplayKeycodes.restype = c_int
XDisplayKeycodes.argtypes = [POINTER(Display), POINTER(c_int), POINTER(c_int)]
XDisplayPlanes = _libraries['libX11.so.6'].XDisplayPlanes
XDisplayPlanes.restype = c_int
XDisplayPlanes.argtypes = [POINTER(Display), c_int]
XDisplayWidth = _libraries['libX11.so.6'].XDisplayWidth
XDisplayWidth.restype = c_int
XDisplayWidth.argtypes = [POINTER(Display), c_int]
XDisplayWidthMM = _libraries['libX11.so.6'].XDisplayWidthMM
XDisplayWidthMM.restype = c_int
XDisplayWidthMM.argtypes = [POINTER(Display), c_int]
XDrawArc = _libraries['libX11.so.6'].XDrawArc
XDrawArc.restype = c_int
XDrawArc.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, c_uint, c_uint, c_int, c_int]
XDrawArcs = _libraries['libX11.so.6'].XDrawArcs
XDrawArcs.restype = c_int
XDrawArcs.argtypes = [POINTER(Display), Drawable, GC, POINTER(XArc), c_int]
XDrawImageString = _libraries['libX11.so.6'].XDrawImageString
XDrawImageString.restype = c_int
XDrawImageString.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, STRING, c_int]
XDrawImageString16 = _libraries['libX11.so.6'].XDrawImageString16
XDrawImageString16.restype = c_int
XDrawImageString16.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, POINTER(XChar2b), c_int]
XDrawLine = _libraries['libX11.so.6'].XDrawLine
XDrawLine.restype = c_int
XDrawLine.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, c_int, c_int]
XDrawLines = _libraries['libX11.so.6'].XDrawLines
XDrawLines.restype = c_int
XDrawLines.argtypes = [POINTER(Display), Drawable, GC, POINTER(XPoint), c_int, c_int]
XDrawPoint = _libraries['libX11.so.6'].XDrawPoint
XDrawPoint.restype = c_int
XDrawPoint.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int]
XDrawPoints = _libraries['libX11.so.6'].XDrawPoints
XDrawPoints.restype = c_int
XDrawPoints.argtypes = [POINTER(Display), Drawable, GC, POINTER(XPoint), c_int, c_int]
XDrawRectangle = _libraries['libX11.so.6'].XDrawRectangle
XDrawRectangle.restype = c_int
XDrawRectangle.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, c_uint, c_uint]
XDrawRectangles = _libraries['libX11.so.6'].XDrawRectangles
XDrawRectangles.restype = c_int
XDrawRectangles.argtypes = [POINTER(Display), Drawable, GC, POINTER(XRectangle), c_int]
XDrawSegments = _libraries['libX11.so.6'].XDrawSegments
XDrawSegments.restype = c_int
XDrawSegments.argtypes = [POINTER(Display), Drawable, GC, POINTER(XSegment), c_int]
XDrawString = _libraries['libX11.so.6'].XDrawString
XDrawString.restype = c_int
XDrawString.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, STRING, c_int]
XDrawString16 = _libraries['libX11.so.6'].XDrawString16
XDrawString16.restype = c_int
XDrawString16.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, POINTER(XChar2b), c_int]
XDrawText = _libraries['libX11.so.6'].XDrawText
XDrawText.restype = c_int
XDrawText.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, POINTER(XTextItem), c_int]
XDrawText16 = _libraries['libX11.so.6'].XDrawText16
XDrawText16.restype = c_int
XDrawText16.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, POINTER(XTextItem16), c_int]
XEnableAccessControl = _libraries['libX11.so.6'].XEnableAccessControl
XEnableAccessControl.restype = c_int
XEnableAccessControl.argtypes = [POINTER(Display)]
XEventsQueued = _libraries['libX11.so.6'].XEventsQueued
XEventsQueued.restype = c_int
XEventsQueued.argtypes = [POINTER(Display), c_int]
XFetchName = _libraries['libX11.so.6'].XFetchName
XFetchName.restype = c_int
XFetchName.argtypes = [POINTER(Display), Window, POINTER(STRING)]
XFillArc = _libraries['libX11.so.6'].XFillArc
XFillArc.restype = c_int
XFillArc.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, c_uint, c_uint, c_int, c_int]
XFillArcs = _libraries['libX11.so.6'].XFillArcs
XFillArcs.restype = c_int
XFillArcs.argtypes = [POINTER(Display), Drawable, GC, POINTER(XArc), c_int]
XFillPolygon = _libraries['libX11.so.6'].XFillPolygon
XFillPolygon.restype = c_int
XFillPolygon.argtypes = [POINTER(Display), Drawable, GC, POINTER(XPoint), c_int, c_int, c_int]
XFillRectangle = _libraries['libX11.so.6'].XFillRectangle
XFillRectangle.restype = c_int
XFillRectangle.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, c_uint, c_uint]
XFillRectangles = _libraries['libX11.so.6'].XFillRectangles
XFillRectangles.restype = c_int
XFillRectangles.argtypes = [POINTER(Display), Drawable, GC, POINTER(XRectangle), c_int]
XFlush = _libraries['libX11.so.6'].XFlush
XFlush.restype = c_int
XFlush.argtypes = [POINTER(Display)]
XForceScreenSaver = _libraries['libX11.so.6'].XForceScreenSaver
XForceScreenSaver.restype = c_int
XForceScreenSaver.argtypes = [POINTER(Display), c_int]
XFree = _libraries['libX11.so.6'].XFree
XFree.restype = c_int
XFree.argtypes = [c_void_p]
XFreeColormap = _libraries['libX11.so.6'].XFreeColormap
XFreeColormap.restype = c_int
XFreeColormap.argtypes = [POINTER(Display), Colormap]
XFreeColors = _libraries['libX11.so.6'].XFreeColors
XFreeColors.restype = c_int
XFreeColors.argtypes = [POINTER(Display), Colormap, POINTER(c_ulong), c_int, c_ulong]
XFreeCursor = _libraries['libX11.so.6'].XFreeCursor
XFreeCursor.restype = c_int
XFreeCursor.argtypes = [POINTER(Display), Cursor]
XFreeExtensionList = _libraries['libX11.so.6'].XFreeExtensionList
XFreeExtensionList.restype = c_int
XFreeExtensionList.argtypes = [POINTER(STRING)]
XFreeFont = _libraries['libX11.so.6'].XFreeFont
XFreeFont.restype = c_int
XFreeFont.argtypes = [POINTER(Display), POINTER(XFontStruct)]
XFreeFontInfo = _libraries['libX11.so.6'].XFreeFontInfo
XFreeFontInfo.restype = c_int
XFreeFontInfo.argtypes = [POINTER(STRING), POINTER(XFontStruct), c_int]
XFreeFontNames = _libraries['libX11.so.6'].XFreeFontNames
XFreeFontNames.restype = c_int
XFreeFontNames.argtypes = [POINTER(STRING)]
XFreeFontPath = _libraries['libX11.so.6'].XFreeFontPath
XFreeFontPath.restype = c_int
XFreeFontPath.argtypes = [POINTER(STRING)]
XFreeGC = _libraries['libX11.so.6'].XFreeGC
XFreeGC.restype = c_int
XFreeGC.argtypes = [POINTER(Display), GC]
XFreeModifiermap = _libraries['libX11.so.6'].XFreeModifiermap
XFreeModifiermap.restype = c_int
XFreeModifiermap.argtypes = [POINTER(XModifierKeymap)]
XFreePixmap = _libraries['libX11.so.6'].XFreePixmap
XFreePixmap.restype = c_int
XFreePixmap.argtypes = [POINTER(Display), Pixmap]
XGeometry = _libraries['libX11.so.6'].XGeometry
XGeometry.restype = c_int
XGeometry.argtypes = [POINTER(Display), c_int, STRING, STRING, c_uint, c_uint, c_uint, c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
XGetErrorDatabaseText = _libraries['libX11.so.6'].XGetErrorDatabaseText
XGetErrorDatabaseText.restype = c_int
XGetErrorDatabaseText.argtypes = [POINTER(Display), STRING, STRING, STRING, STRING, c_int]
XGetErrorText = _libraries['libX11.so.6'].XGetErrorText
XGetErrorText.restype = c_int
XGetErrorText.argtypes = [POINTER(Display), c_int, STRING, c_int]
XGetFontProperty = _libraries['libX11.so.6'].XGetFontProperty
XGetFontProperty.restype = c_int
XGetFontProperty.argtypes = [POINTER(XFontStruct), Atom, POINTER(c_ulong)]
XGetGCValues = _libraries['libX11.so.6'].XGetGCValues
XGetGCValues.restype = c_int
XGetGCValues.argtypes = [POINTER(Display), GC, c_ulong, POINTER(XGCValues)]
XGetGeometry = _libraries['libX11.so.6'].XGetGeometry
XGetGeometry.restype = c_int
XGetGeometry.argtypes = [POINTER(Display), Drawable, POINTER(Window), POINTER(c_int), POINTER(c_int), POINTER(c_uint), POINTER(c_uint), POINTER(c_uint), POINTER(c_uint)]
XGetIconName = _libraries['libX11.so.6'].XGetIconName
XGetIconName.restype = c_int
XGetIconName.argtypes = [POINTER(Display), Window, POINTER(STRING)]
XGetInputFocus = _libraries['libX11.so.6'].XGetInputFocus
XGetInputFocus.restype = c_int
XGetInputFocus.argtypes = [POINTER(Display), POINTER(Window), POINTER(c_int)]
XGetKeyboardControl = _libraries['libX11.so.6'].XGetKeyboardControl
XGetKeyboardControl.restype = c_int
XGetKeyboardControl.argtypes = [POINTER(Display), POINTER(XKeyboardState)]
XGetPointerControl = _libraries['libX11.so.6'].XGetPointerControl
XGetPointerControl.restype = c_int
XGetPointerControl.argtypes = [POINTER(Display), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
XGetPointerMapping = _libraries['libX11.so.6'].XGetPointerMapping
XGetPointerMapping.restype = c_int
XGetPointerMapping.argtypes = [POINTER(Display), POINTER(c_ubyte), c_int]
XGetScreenSaver = _libraries['libX11.so.6'].XGetScreenSaver
XGetScreenSaver.restype = c_int
XGetScreenSaver.argtypes = [POINTER(Display), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
XGetTransientForHint = _libraries['libX11.so.6'].XGetTransientForHint
XGetTransientForHint.restype = c_int
XGetTransientForHint.argtypes = [POINTER(Display), Window, POINTER(Window)]
XGetWindowProperty = _libraries['libX11.so.6'].XGetWindowProperty
XGetWindowProperty.restype = c_int
XGetWindowProperty.argtypes = [POINTER(Display), Window, Atom, c_long, c_long, c_int, Atom, POINTER(Atom), POINTER(c_int), POINTER(c_ulong), POINTER(c_ulong), POINTER(POINTER(c_ubyte))]
XGetWindowAttributes = _libraries['libX11.so.6'].XGetWindowAttributes
XGetWindowAttributes.restype = c_int
XGetWindowAttributes.argtypes = [POINTER(Display), Window, POINTER(XWindowAttributes)]
XGrabButton = _libraries['libX11.so.6'].XGrabButton
XGrabButton.restype = c_int
XGrabButton.argtypes = [POINTER(Display), c_uint, c_uint, Window, c_int, c_uint, c_int, c_int, Window, Cursor]
XGrabKey = _libraries['libX11.so.6'].XGrabKey
XGrabKey.restype = c_int
XGrabKey.argtypes = [POINTER(Display), c_int, c_uint, Window, c_int, c_int, c_int]
XGrabKeyboard = _libraries['libX11.so.6'].XGrabKeyboard
XGrabKeyboard.restype = c_int
XGrabKeyboard.argtypes = [POINTER(Display), Window, c_int, c_int, c_int, Time]
XGrabPointer = _libraries['libX11.so.6'].XGrabPointer
XGrabPointer.restype = c_int
XGrabPointer.argtypes = [POINTER(Display), Window, c_int, c_uint, c_int, c_int, Window, Cursor, Time]
XGrabServer = _libraries['libX11.so.6'].XGrabServer
XGrabServer.restype = c_int
XGrabServer.argtypes = [POINTER(Display)]
XHeightMMOfScreen = _libraries['libX11.so.6'].XHeightMMOfScreen
XHeightMMOfScreen.restype = c_int
XHeightMMOfScreen.argtypes = [POINTER(Screen)]
XHeightOfScreen = _libraries['libX11.so.6'].XHeightOfScreen
XHeightOfScreen.restype = c_int
XHeightOfScreen.argtypes = [POINTER(Screen)]
XIfEvent = _libraries['libX11.so.6'].XIfEvent
XIfEvent.restype = c_int
XIfEvent.argtypes = [POINTER(Display), POINTER(XEvent), CFUNCTYPE(c_int, POINTER(Display), POINTER(XEvent), XPointer), XPointer]
XImageByteOrder = _libraries['libX11.so.6'].XImageByteOrder
XImageByteOrder.restype = c_int
XImageByteOrder.argtypes = [POINTER(Display)]
XInstallColormap = _libraries['libX11.so.6'].XInstallColormap
XInstallColormap.restype = c_int
XInstallColormap.argtypes = [POINTER(Display), Colormap]
XKeysymToKeycode = _libraries['libX11.so.6'].XKeysymToKeycode
XKeysymToKeycode.restype = KeyCode
XKeysymToKeycode.argtypes = [POINTER(Display), KeySym]
XKillClient = _libraries['libX11.so.6'].XKillClient
XKillClient.restype = c_int
XKillClient.argtypes = [POINTER(Display), XID]
XLookupColor = _libraries['libX11.so.6'].XLookupColor
XLookupColor.restype = c_int
XLookupColor.argtypes = [POINTER(Display), Colormap, STRING, POINTER(XColor), POINTER(XColor)]
XLowerWindow = _libraries['libX11.so.6'].XLowerWindow
XLowerWindow.restype = c_int
XLowerWindow.argtypes = [POINTER(Display), Window]
XMapRaised = _libraries['libX11.so.6'].XMapRaised
XMapRaised.restype = c_int
XMapRaised.argtypes = [POINTER(Display), Window]
XMapSubwindows = _libraries['libX11.so.6'].XMapSubwindows
XMapSubwindows.restype = c_int
XMapSubwindows.argtypes = [POINTER(Display), Window]
XMapWindow = _libraries['libX11.so.6'].XMapWindow
XMapWindow.restype = c_int
XMapWindow.argtypes = [POINTER(Display), Window]
XMaskEvent = _libraries['libX11.so.6'].XMaskEvent
XMaskEvent.restype = c_int
XMaskEvent.argtypes = [POINTER(Display), c_long, POINTER(XEvent)]
XMaxCmapsOfScreen = _libraries['libX11.so.6'].XMaxCmapsOfScreen
XMaxCmapsOfScreen.restype = c_int
XMaxCmapsOfScreen.argtypes = [POINTER(Screen)]
XMinCmapsOfScreen = _libraries['libX11.so.6'].XMinCmapsOfScreen
XMinCmapsOfScreen.restype = c_int
XMinCmapsOfScreen.argtypes = [POINTER(Screen)]
XMoveResizeWindow = _libraries['libX11.so.6'].XMoveResizeWindow
XMoveResizeWindow.restype = c_int
XMoveResizeWindow.argtypes = [POINTER(Display), Window, c_int, c_int, c_uint, c_uint]
XMoveWindow = _libraries['libX11.so.6'].XMoveWindow
XMoveWindow.restype = c_int
XMoveWindow.argtypes = [POINTER(Display), Window, c_int, c_int]
XNextEvent = _libraries['libX11.so.6'].XNextEvent
XNextEvent.restype = c_int
XNextEvent.argtypes = [POINTER(Display), POINTER(XEvent)]
XNoOp = _libraries['libX11.so.6'].XNoOp
XNoOp.restype = c_int
XNoOp.argtypes = [POINTER(Display)]
XParseColor = _libraries['libX11.so.6'].XParseColor
XParseColor.restype = c_int
XParseColor.argtypes = [POINTER(Display), Colormap, STRING, POINTER(XColor)]
XParseGeometry = _libraries['libX11.so.6'].XParseGeometry
XParseGeometry.restype = c_int
XParseGeometry.argtypes = [STRING, POINTER(c_int), POINTER(c_int), POINTER(c_uint), POINTER(c_uint)]
XPeekEvent = _libraries['libX11.so.6'].XPeekEvent
XPeekEvent.restype = c_int
XPeekEvent.argtypes = [POINTER(Display), POINTER(XEvent)]
XPeekIfEvent = _libraries['libX11.so.6'].XPeekIfEvent
XPeekIfEvent.restype = c_int
XPeekIfEvent.argtypes = [POINTER(Display), POINTER(XEvent), CFUNCTYPE(c_int, POINTER(Display), POINTER(XEvent), XPointer), XPointer]
XPending = _libraries['libX11.so.6'].XPending
XPending.restype = c_int
XPending.argtypes = [POINTER(Display)]
XPlanesOfScreen = _libraries['libX11.so.6'].XPlanesOfScreen
XPlanesOfScreen.restype = c_int
XPlanesOfScreen.argtypes = [POINTER(Screen)]
XProtocolRevision = _libraries['libX11.so.6'].XProtocolRevision
XProtocolRevision.restype = c_int
XProtocolRevision.argtypes = [POINTER(Display)]
XProtocolVersion = _libraries['libX11.so.6'].XProtocolVersion
XProtocolVersion.restype = c_int
XProtocolVersion.argtypes = [POINTER(Display)]
XPutBackEvent = _libraries['libX11.so.6'].XPutBackEvent
XPutBackEvent.restype = c_int
XPutBackEvent.argtypes = [POINTER(Display), POINTER(XEvent)]
XPutImage = _libraries['libX11.so.6'].XPutImage
XPutImage.restype = c_int
XPutImage.argtypes = [POINTER(Display), Drawable, GC, POINTER(XImage), c_int, c_int, c_int, c_int, c_uint, c_uint]
XQLength = _libraries['libX11.so.6'].XQLength
XQLength.restype = c_int
XQLength.argtypes = [POINTER(Display)]
XQueryBestCursor = _libraries['libX11.so.6'].XQueryBestCursor
XQueryBestCursor.restype = c_int
XQueryBestCursor.argtypes = [POINTER(Display), Drawable, c_uint, c_uint, POINTER(c_uint), POINTER(c_uint)]
XQueryBestSize = _libraries['libX11.so.6'].XQueryBestSize
XQueryBestSize.restype = c_int
XQueryBestSize.argtypes = [POINTER(Display), c_int, Drawable, c_uint, c_uint, POINTER(c_uint), POINTER(c_uint)]
XQueryBestStipple = _libraries['libX11.so.6'].XQueryBestStipple
XQueryBestStipple.restype = c_int
XQueryBestStipple.argtypes = [POINTER(Display), Drawable, c_uint, c_uint, POINTER(c_uint), POINTER(c_uint)]
XQueryBestTile = _libraries['libX11.so.6'].XQueryBestTile
XQueryBestTile.restype = c_int
XQueryBestTile.argtypes = [POINTER(Display), Drawable, c_uint, c_uint, POINTER(c_uint), POINTER(c_uint)]
XQueryColor = _libraries['libX11.so.6'].XQueryColor
XQueryColor.restype = c_int
XQueryColor.argtypes = [POINTER(Display), Colormap, POINTER(XColor)]
XQueryColors = _libraries['libX11.so.6'].XQueryColors
XQueryColors.restype = c_int
XQueryColors.argtypes = [POINTER(Display), Colormap, POINTER(XColor), c_int]
XQueryExtension = _libraries['libX11.so.6'].XQueryExtension
XQueryExtension.restype = c_int
XQueryExtension.argtypes = [POINTER(Display), STRING, POINTER(c_int), POINTER(c_int), POINTER(c_int)]
XQueryKeymap = _libraries['libX11.so.6'].XQueryKeymap
XQueryKeymap.restype = c_int
XQueryKeymap.argtypes = [POINTER(Display), STRING]
XQueryPointer = _libraries['libX11.so.6'].XQueryPointer
XQueryPointer.restype = c_int
XQueryPointer.argtypes = [POINTER(Display), Window, POINTER(Window), POINTER(Window), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_uint)]
XQueryTextExtents = _libraries['libX11.so.6'].XQueryTextExtents
XQueryTextExtents.restype = c_int
XQueryTextExtents.argtypes = [POINTER(Display), XID, STRING, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(XCharStruct)]
XQueryTextExtents16 = _libraries['libX11.so.6'].XQueryTextExtents16
XQueryTextExtents16.restype = c_int
XQueryTextExtents16.argtypes = [POINTER(Display), XID, POINTER(XChar2b), c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(XCharStruct)]
XQueryTree = _libraries['libX11.so.6'].XQueryTree
XQueryTree.restype = c_int
XQueryTree.argtypes = [POINTER(Display), Window, POINTER(Window), POINTER(Window), POINTER(POINTER(Window)), POINTER(c_uint)]
XRaiseWindow = _libraries['libX11.so.6'].XRaiseWindow
XRaiseWindow.restype = c_int
XRaiseWindow.argtypes = [POINTER(Display), Window]
XReadBitmapFile = _libraries['libX11.so.6'].XReadBitmapFile
XReadBitmapFile.restype = c_int
XReadBitmapFile.argtypes = [POINTER(Display), Drawable, STRING, POINTER(c_uint), POINTER(c_uint), POINTER(Pixmap), POINTER(c_int), POINTER(c_int)]
XReadBitmapFileData = _libraries['libX11.so.6'].XReadBitmapFileData
XReadBitmapFileData.restype = c_int
XReadBitmapFileData.argtypes = [STRING, POINTER(c_uint), POINTER(c_uint), POINTER(POINTER(c_ubyte)), POINTER(c_int), POINTER(c_int)]
XRebindKeysym = _libraries['libX11.so.6'].XRebindKeysym
XRebindKeysym.restype = c_int
XRebindKeysym.argtypes = [POINTER(Display), KeySym, POINTER(KeySym), c_int, POINTER(c_ubyte), c_int]
XRecolorCursor = _libraries['libX11.so.6'].XRecolorCursor
XRecolorCursor.restype = c_int
XRecolorCursor.argtypes = [POINTER(Display), Cursor, POINTER(XColor), POINTER(XColor)]
XRefreshKeyboardMapping = _libraries['libX11.so.6'].XRefreshKeyboardMapping
XRefreshKeyboardMapping.restype = c_int
XRefreshKeyboardMapping.argtypes = [POINTER(XMappingEvent)]
XRemoveFromSaveSet = _libraries['libX11.so.6'].XRemoveFromSaveSet
XRemoveFromSaveSet.restype = c_int
XRemoveFromSaveSet.argtypes = [POINTER(Display), Window]
XRemoveHost = _libraries['libX11.so.6'].XRemoveHost
XRemoveHost.restype = c_int
XRemoveHost.argtypes = [POINTER(Display), POINTER(XHostAddress)]
XRemoveHosts = _libraries['libX11.so.6'].XRemoveHosts
XRemoveHosts.restype = c_int
XRemoveHosts.argtypes = [POINTER(Display), POINTER(XHostAddress), c_int]
XReparentWindow = _libraries['libX11.so.6'].XReparentWindow
XReparentWindow.restype = c_int
XReparentWindow.argtypes = [POINTER(Display), Window, Window, c_int, c_int]
XResetScreenSaver = _libraries['libX11.so.6'].XResetScreenSaver
XResetScreenSaver.restype = c_int
XResetScreenSaver.argtypes = [POINTER(Display)]
XResizeWindow = _libraries['libX11.so.6'].XResizeWindow
XResizeWindow.restype = c_int
XResizeWindow.argtypes = [POINTER(Display), Window, c_uint, c_uint]
XRestackWindows = _libraries['libX11.so.6'].XRestackWindows
XRestackWindows.restype = c_int
XRestackWindows.argtypes = [POINTER(Display), POINTER(Window), c_int]
XRotateBuffers = _libraries['libX11.so.6'].XRotateBuffers
XRotateBuffers.restype = c_int
XRotateBuffers.argtypes = [POINTER(Display), c_int]
XRotateWindowProperties = _libraries['libX11.so.6'].XRotateWindowProperties
XRotateWindowProperties.restype = c_int
XRotateWindowProperties.argtypes = [POINTER(Display), Window, POINTER(Atom), c_int, c_int]
XScreenCount = _libraries['libX11.so.6'].XScreenCount
XScreenCount.restype = c_int
XScreenCount.argtypes = [POINTER(Display)]
XSelectInput = _libraries['libX11.so.6'].XSelectInput
XSelectInput.restype = c_int
XSelectInput.argtypes = [POINTER(Display), Window, c_long]
XSendEvent = _libraries['libX11.so.6'].XSendEvent
XSendEvent.restype = c_int
XSendEvent.argtypes = [POINTER(Display), Window, c_int, c_long, POINTER(XEvent)]
XSetAccessControl = _libraries['libX11.so.6'].XSetAccessControl
XSetAccessControl.restype = c_int
XSetAccessControl.argtypes = [POINTER(Display), c_int]
XSetArcMode = _libraries['libX11.so.6'].XSetArcMode
XSetArcMode.restype = c_int
XSetArcMode.argtypes = [POINTER(Display), GC, c_int]
XSetBackground = _libraries['libX11.so.6'].XSetBackground
XSetBackground.restype = c_int
XSetBackground.argtypes = [POINTER(Display), GC, c_ulong]
XSetClipMask = _libraries['libX11.so.6'].XSetClipMask
XSetClipMask.restype = c_int
XSetClipMask.argtypes = [POINTER(Display), GC, Pixmap]
XSetClipOrigin = _libraries['libX11.so.6'].XSetClipOrigin
XSetClipOrigin.restype = c_int
XSetClipOrigin.argtypes = [POINTER(Display), GC, c_int, c_int]
XSetClipRectangles = _libraries['libX11.so.6'].XSetClipRectangles
XSetClipRectangles.restype = c_int
XSetClipRectangles.argtypes = [POINTER(Display), GC, c_int, c_int, POINTER(XRectangle), c_int, c_int]
XSetCloseDownMode = _libraries['libX11.so.6'].XSetCloseDownMode
XSetCloseDownMode.restype = c_int
XSetCloseDownMode.argtypes = [POINTER(Display), c_int]
XSetCommand = _libraries['libX11.so.6'].XSetCommand
XSetCommand.restype = c_int
XSetCommand.argtypes = [POINTER(Display), Window, POINTER(STRING), c_int]
XSetDashes = _libraries['libX11.so.6'].XSetDashes
XSetDashes.restype = c_int
XSetDashes.argtypes = [POINTER(Display), GC, c_int, STRING, c_int]
XSetFillRule = _libraries['libX11.so.6'].XSetFillRule
XSetFillRule.restype = c_int
XSetFillRule.argtypes = [POINTER(Display), GC, c_int]
XSetFillStyle = _libraries['libX11.so.6'].XSetFillStyle
XSetFillStyle.restype = c_int
XSetFillStyle.argtypes = [POINTER(Display), GC, c_int]
XSetFont = _libraries['libX11.so.6'].XSetFont
XSetFont.restype = c_int
XSetFont.argtypes = [POINTER(Display), GC, Font]
XSetFontPath = _libraries['libX11.so.6'].XSetFontPath
XSetFontPath.restype = c_int
XSetFontPath.argtypes = [POINTER(Display), POINTER(STRING), c_int]
XSetForeground = _libraries['libX11.so.6'].XSetForeground
XSetForeground.restype = c_int
XSetForeground.argtypes = [POINTER(Display), GC, c_ulong]
XSetFunction = _libraries['libX11.so.6'].XSetFunction
XSetFunction.restype = c_int
XSetFunction.argtypes = [POINTER(Display), GC, c_int]
XSetGraphicsExposures = _libraries['libX11.so.6'].XSetGraphicsExposures
XSetGraphicsExposures.restype = c_int
XSetGraphicsExposures.argtypes = [POINTER(Display), GC, c_int]
XSetIconName = _libraries['libX11.so.6'].XSetIconName
XSetIconName.restype = c_int
XSetIconName.argtypes = [POINTER(Display), Window, STRING]
XSetInputFocus = _libraries['libX11.so.6'].XSetInputFocus
XSetInputFocus.restype = c_int
XSetInputFocus.argtypes = [POINTER(Display), Window, c_int, Time]
XSetLineAttributes = _libraries['libX11.so.6'].XSetLineAttributes
XSetLineAttributes.restype = c_int
XSetLineAttributes.argtypes = [POINTER(Display), GC, c_uint, c_int, c_int, c_int]
XSetModifierMapping = _libraries['libX11.so.6'].XSetModifierMapping
XSetModifierMapping.restype = c_int
XSetModifierMapping.argtypes = [POINTER(Display), POINTER(XModifierKeymap)]
XSetPlaneMask = _libraries['libX11.so.6'].XSetPlaneMask
XSetPlaneMask.restype = c_int
XSetPlaneMask.argtypes = [POINTER(Display), GC, c_ulong]
XSetPointerMapping = _libraries['libX11.so.6'].XSetPointerMapping
XSetPointerMapping.restype = c_int
XSetPointerMapping.argtypes = [POINTER(Display), POINTER(c_ubyte), c_int]
XSetScreenSaver = _libraries['libX11.so.6'].XSetScreenSaver
XSetScreenSaver.restype = c_int
XSetScreenSaver.argtypes = [POINTER(Display), c_int, c_int, c_int, c_int]
XSetSelectionOwner = _libraries['libX11.so.6'].XSetSelectionOwner
XSetSelectionOwner.restype = c_int
XSetSelectionOwner.argtypes = [POINTER(Display), Atom, Window, Time]
XSetState = _libraries['libX11.so.6'].XSetState
XSetState.restype = c_int
XSetState.argtypes = [POINTER(Display), GC, c_ulong, c_ulong, c_int, c_ulong]
XSetStipple = _libraries['libX11.so.6'].XSetStipple
XSetStipple.restype = c_int
XSetStipple.argtypes = [POINTER(Display), GC, Pixmap]
XSetSubwindowMode = _libraries['libX11.so.6'].XSetSubwindowMode
XSetSubwindowMode.restype = c_int
XSetSubwindowMode.argtypes = [POINTER(Display), GC, c_int]
XSetTSOrigin = _libraries['libX11.so.6'].XSetTSOrigin
XSetTSOrigin.restype = c_int
XSetTSOrigin.argtypes = [POINTER(Display), GC, c_int, c_int]
XSetTile = _libraries['libX11.so.6'].XSetTile
XSetTile.restype = c_int
XSetTile.argtypes = [POINTER(Display), GC, Pixmap]
XSetWindowBackground = _libraries['libX11.so.6'].XSetWindowBackground
XSetWindowBackground.restype = c_int
XSetWindowBackground.argtypes = [POINTER(Display), Window, c_ulong]
XSetWindowBackgroundPixmap = _libraries['libX11.so.6'].XSetWindowBackgroundPixmap
XSetWindowBackgroundPixmap.restype = c_int
XSetWindowBackgroundPixmap.argtypes = [POINTER(Display), Window, Pixmap]
XSetWindowBorder = _libraries['libX11.so.6'].XSetWindowBorder
XSetWindowBorder.restype = c_int
XSetWindowBorder.argtypes = [POINTER(Display), Window, c_ulong]
XSetWindowBorderPixmap = _libraries['libX11.so.6'].XSetWindowBorderPixmap
XSetWindowBorderPixmap.restype = c_int
XSetWindowBorderPixmap.argtypes = [POINTER(Display), Window, Pixmap]
XSetWindowBorderWidth = _libraries['libX11.so.6'].XSetWindowBorderWidth
XSetWindowBorderWidth.restype = c_int
XSetWindowBorderWidth.argtypes = [POINTER(Display), Window, c_uint]
XSetWindowColormap = _libraries['libX11.so.6'].XSetWindowColormap
XSetWindowColormap.restype = c_int
XSetWindowColormap.argtypes = [POINTER(Display), Window, Colormap]
XStoreBuffer = _libraries['libX11.so.6'].XStoreBuffer
XStoreBuffer.restype = c_int
XStoreBuffer.argtypes = [POINTER(Display), STRING, c_int, c_int]
XStoreBytes = _libraries['libX11.so.6'].XStoreBytes
XStoreBytes.restype = c_int
XStoreBytes.argtypes = [POINTER(Display), STRING, c_int]
XStoreColor = _libraries['libX11.so.6'].XStoreColor
XStoreColor.restype = c_int
XStoreColor.argtypes = [POINTER(Display), Colormap, POINTER(XColor)]
XStoreColors = _libraries['libX11.so.6'].XStoreColors
XStoreColors.restype = c_int
XStoreColors.argtypes = [POINTER(Display), Colormap, POINTER(XColor), c_int]
XStoreName = _libraries['libX11.so.6'].XStoreName
XStoreName.restype = c_int
XStoreName.argtypes = [POINTER(Display), Window, STRING]
XStoreNamedColor = _libraries['libX11.so.6'].XStoreNamedColor
XStoreNamedColor.restype = c_int
XStoreNamedColor.argtypes = [POINTER(Display), Colormap, STRING, c_ulong, c_int]
XSync = _libraries['libX11.so.6'].XSync
XSync.restype = c_int
XSync.argtypes = [POINTER(Display), c_int]
XTextExtents = _libraries['libX11.so.6'].XTextExtents
XTextExtents.restype = c_int
XTextExtents.argtypes = [POINTER(XFontStruct), STRING, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(XCharStruct)]
XTextExtents16 = _libraries['libX11.so.6'].XTextExtents16
XTextExtents16.restype = c_int
XTextExtents16.argtypes = [POINTER(XFontStruct), POINTER(XChar2b), c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(XCharStruct)]
XTextWidth = _libraries['libX11.so.6'].XTextWidth
XTextWidth.restype = c_int
XTextWidth.argtypes = [POINTER(XFontStruct), STRING, c_int]
XTextWidth16 = _libraries['libX11.so.6'].XTextWidth16
XTextWidth16.restype = c_int
XTextWidth16.argtypes = [POINTER(XFontStruct), POINTER(XChar2b), c_int]
XTranslateCoordinates = _libraries['libX11.so.6'].XTranslateCoordinates
XTranslateCoordinates.restype = c_int
XTranslateCoordinates.argtypes = [POINTER(Display), Window, Window, c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(Window)]
XUndefineCursor = _libraries['libX11.so.6'].XUndefineCursor
XUndefineCursor.restype = c_int
XUndefineCursor.argtypes = [POINTER(Display), Window]
XUngrabButton = _libraries['libX11.so.6'].XUngrabButton
XUngrabButton.restype = c_int
XUngrabButton.argtypes = [POINTER(Display), c_uint, c_uint, Window]
XUngrabKey = _libraries['libX11.so.6'].XUngrabKey
XUngrabKey.restype = c_int
XUngrabKey.argtypes = [POINTER(Display), c_int, c_uint, Window]
XUngrabKeyboard = _libraries['libX11.so.6'].XUngrabKeyboard
XUngrabKeyboard.restype = c_int
XUngrabKeyboard.argtypes = [POINTER(Display), Time]
XUngrabPointer = _libraries['libX11.so.6'].XUngrabPointer
XUngrabPointer.restype = c_int
XUngrabPointer.argtypes = [POINTER(Display), Time]
XUngrabServer = _libraries['libX11.so.6'].XUngrabServer
XUngrabServer.restype = c_int
XUngrabServer.argtypes = [POINTER(Display)]
XUninstallColormap = _libraries['libX11.so.6'].XUninstallColormap
XUninstallColormap.restype = c_int
XUninstallColormap.argtypes = [POINTER(Display), Colormap]
XUnloadFont = _libraries['libX11.so.6'].XUnloadFont
XUnloadFont.restype = c_int
XUnloadFont.argtypes = [POINTER(Display), Font]
XUnmapSubwindows = _libraries['libX11.so.6'].XUnmapSubwindows
XUnmapSubwindows.restype = c_int
XUnmapSubwindows.argtypes = [POINTER(Display), Window]
XUnmapWindow = _libraries['libX11.so.6'].XUnmapWindow
XUnmapWindow.restype = c_int
XUnmapWindow.argtypes = [POINTER(Display), Window]
XVendorRelease = _libraries['libX11.so.6'].XVendorRelease
XVendorRelease.restype = c_int
XVendorRelease.argtypes = [POINTER(Display)]
XWarpPointer = _libraries['libX11.so.6'].XWarpPointer
XWarpPointer.restype = c_int
XWarpPointer.argtypes = [POINTER(Display), Window, Window, c_int, c_int, c_uint, c_uint, c_int, c_int]
XWidthMMOfScreen = _libraries['libX11.so.6'].XWidthMMOfScreen
XWidthMMOfScreen.restype = c_int
XWidthMMOfScreen.argtypes = [POINTER(Screen)]
XWidthOfScreen = _libraries['libX11.so.6'].XWidthOfScreen
XWidthOfScreen.restype = c_int
XWidthOfScreen.argtypes = [POINTER(Screen)]
XWindowEvent = _libraries['libX11.so.6'].XWindowEvent
XWindowEvent.restype = c_int
XWindowEvent.argtypes = [POINTER(Display), Window, c_long, POINTER(XEvent)]
XWriteBitmapFile = _libraries['libX11.so.6'].XWriteBitmapFile
XWriteBitmapFile.restype = c_int
XWriteBitmapFile.argtypes = [POINTER(Display), STRING, Pixmap, c_uint, c_uint, c_int, c_int]
XSupportsLocale = _libraries['libX11.so.6'].XSupportsLocale
XSupportsLocale.restype = c_int
XSupportsLocale.argtypes = []
XSetLocaleModifiers = _libraries['libX11.so.6'].XSetLocaleModifiers
XSetLocaleModifiers.restype = STRING
XSetLocaleModifiers.argtypes = [STRING]
XOpenOM = _libraries['libX11.so.6'].XOpenOM
XOpenOM.restype = XOM
XOpenOM.argtypes = [POINTER(Display), POINTER(_XrmHashBucketRec), STRING, STRING]
XCloseOM = _libraries['libX11.so.6'].XCloseOM
XCloseOM.restype = c_int
XCloseOM.argtypes = [XOM]
XSetOMValues = _libraries['libX11.so.6'].XSetOMValues
XSetOMValues.restype = STRING
XSetOMValues.argtypes = [XOM]
XGetOMValues = _libraries['libX11.so.6'].XGetOMValues
XGetOMValues.restype = STRING
XGetOMValues.argtypes = [XOM]
XDisplayOfOM = _libraries['libX11.so.6'].XDisplayOfOM
XDisplayOfOM.restype = POINTER(Display)
XDisplayOfOM.argtypes = [XOM]
XLocaleOfOM = _libraries['libX11.so.6'].XLocaleOfOM
XLocaleOfOM.restype = STRING
XLocaleOfOM.argtypes = [XOM]
XCreateOC = _libraries['libX11.so.6'].XCreateOC
XCreateOC.restype = XOC
XCreateOC.argtypes = [XOM]
XDestroyOC = _libraries['libX11.so.6'].XDestroyOC
XDestroyOC.restype = None
XDestroyOC.argtypes = [XOC]
XOMOfOC = _libraries['libX11.so.6'].XOMOfOC
XOMOfOC.restype = XOM
XOMOfOC.argtypes = [XOC]
XSetOCValues = _libraries['libX11.so.6'].XSetOCValues
XSetOCValues.restype = STRING
XSetOCValues.argtypes = [XOC]
XGetOCValues = _libraries['libX11.so.6'].XGetOCValues
XGetOCValues.restype = STRING
XGetOCValues.argtypes = [XOC]
XCreateFontSet = _libraries['libX11.so.6'].XCreateFontSet
XCreateFontSet.restype = XFontSet
XCreateFontSet.argtypes = [POINTER(Display), STRING, POINTER(POINTER(STRING)), POINTER(c_int), POINTER(STRING)]
XFreeFontSet = _libraries['libX11.so.6'].XFreeFontSet
XFreeFontSet.restype = None
XFreeFontSet.argtypes = [POINTER(Display), XFontSet]
XFontsOfFontSet = _libraries['libX11.so.6'].XFontsOfFontSet
XFontsOfFontSet.restype = c_int
XFontsOfFontSet.argtypes = [XFontSet, POINTER(POINTER(POINTER(XFontStruct))), POINTER(POINTER(STRING))]
XBaseFontNameListOfFontSet = _libraries['libX11.so.6'].XBaseFontNameListOfFontSet
XBaseFontNameListOfFontSet.restype = STRING
XBaseFontNameListOfFontSet.argtypes = [XFontSet]
XLocaleOfFontSet = _libraries['libX11.so.6'].XLocaleOfFontSet
XLocaleOfFontSet.restype = STRING
XLocaleOfFontSet.argtypes = [XFontSet]
XContextDependentDrawing = _libraries['libX11.so.6'].XContextDependentDrawing
XContextDependentDrawing.restype = c_int
XContextDependentDrawing.argtypes = [XFontSet]
XDirectionalDependentDrawing = _libraries['libX11.so.6'].XDirectionalDependentDrawing
XDirectionalDependentDrawing.restype = c_int
XDirectionalDependentDrawing.argtypes = [XFontSet]
XContextualDrawing = _libraries['libX11.so.6'].XContextualDrawing
XContextualDrawing.restype = c_int
XContextualDrawing.argtypes = [XFontSet]
XExtentsOfFontSet = _libraries['libX11.so.6'].XExtentsOfFontSet
XExtentsOfFontSet.restype = POINTER(XFontSetExtents)
XExtentsOfFontSet.argtypes = [XFontSet]
XmbTextEscapement = _libraries['libX11.so.6'].XmbTextEscapement
XmbTextEscapement.restype = c_int
XmbTextEscapement.argtypes = [XFontSet, STRING, c_int]
XwcTextEscapement = _libraries['libX11.so.6'].XwcTextEscapement
XwcTextEscapement.restype = c_int
XwcTextEscapement.argtypes = [XFontSet, WSTRING, c_int]
Xutf8TextEscapement = _libraries['libX11.so.6'].Xutf8TextEscapement
Xutf8TextEscapement.restype = c_int
Xutf8TextEscapement.argtypes = [XFontSet, STRING, c_int]
XmbTextExtents = _libraries['libX11.so.6'].XmbTextExtents
XmbTextExtents.restype = c_int
XmbTextExtents.argtypes = [XFontSet, STRING, c_int, POINTER(XRectangle), POINTER(XRectangle)]
XwcTextExtents = _libraries['libX11.so.6'].XwcTextExtents
XwcTextExtents.restype = c_int
XwcTextExtents.argtypes = [XFontSet, WSTRING, c_int, POINTER(XRectangle), POINTER(XRectangle)]
Xutf8TextExtents = _libraries['libX11.so.6'].Xutf8TextExtents
Xutf8TextExtents.restype = c_int
Xutf8TextExtents.argtypes = [XFontSet, STRING, c_int, POINTER(XRectangle), POINTER(XRectangle)]
XmbTextPerCharExtents = _libraries['libX11.so.6'].XmbTextPerCharExtents
XmbTextPerCharExtents.restype = c_int
XmbTextPerCharExtents.argtypes = [XFontSet, STRING, c_int, POINTER(XRectangle), POINTER(XRectangle), c_int, POINTER(c_int), POINTER(XRectangle), POINTER(XRectangle)]
XwcTextPerCharExtents = _libraries['libX11.so.6'].XwcTextPerCharExtents
XwcTextPerCharExtents.restype = c_int
XwcTextPerCharExtents.argtypes = [XFontSet, WSTRING, c_int, POINTER(XRectangle), POINTER(XRectangle), c_int, POINTER(c_int), POINTER(XRectangle), POINTER(XRectangle)]
Xutf8TextPerCharExtents = _libraries['libX11.so.6'].Xutf8TextPerCharExtents
Xutf8TextPerCharExtents.restype = c_int
Xutf8TextPerCharExtents.argtypes = [XFontSet, STRING, c_int, POINTER(XRectangle), POINTER(XRectangle), c_int, POINTER(c_int), POINTER(XRectangle), POINTER(XRectangle)]
XmbDrawText = _libraries['libX11.so.6'].XmbDrawText
XmbDrawText.restype = None
XmbDrawText.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, POINTER(XmbTextItem), c_int]
XwcDrawText = _libraries['libX11.so.6'].XwcDrawText
XwcDrawText.restype = None
XwcDrawText.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, POINTER(XwcTextItem), c_int]
Xutf8DrawText = _libraries['libX11.so.6'].Xutf8DrawText
Xutf8DrawText.restype = None
Xutf8DrawText.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, POINTER(XmbTextItem), c_int]
XmbDrawString = _libraries['libX11.so.6'].XmbDrawString
XmbDrawString.restype = None
XmbDrawString.argtypes = [POINTER(Display), Drawable, XFontSet, GC, c_int, c_int, STRING, c_int]
XwcDrawString = _libraries['libX11.so.6'].XwcDrawString
XwcDrawString.restype = None
XwcDrawString.argtypes = [POINTER(Display), Drawable, XFontSet, GC, c_int, c_int, WSTRING, c_int]
Xutf8DrawString = _libraries['libX11.so.6'].Xutf8DrawString
Xutf8DrawString.restype = None
Xutf8DrawString.argtypes = [POINTER(Display), Drawable, XFontSet, GC, c_int, c_int, STRING, c_int]
XmbDrawImageString = _libraries['libX11.so.6'].XmbDrawImageString
XmbDrawImageString.restype = None
XmbDrawImageString.argtypes = [POINTER(Display), Drawable, XFontSet, GC, c_int, c_int, STRING, c_int]
XwcDrawImageString = _libraries['libX11.so.6'].XwcDrawImageString
XwcDrawImageString.restype = None
XwcDrawImageString.argtypes = [POINTER(Display), Drawable, XFontSet, GC, c_int, c_int, WSTRING, c_int]
Xutf8DrawImageString = _libraries['libX11.so.6'].Xutf8DrawImageString
Xutf8DrawImageString.restype = None
Xutf8DrawImageString.argtypes = [POINTER(Display), Drawable, XFontSet, GC, c_int, c_int, STRING, c_int]
XOpenIM = _libraries['libX11.so.6'].XOpenIM
XOpenIM.restype = XIM
XOpenIM.argtypes = [POINTER(Display), POINTER(_XrmHashBucketRec), STRING, STRING]
XCloseIM = _libraries['libX11.so.6'].XCloseIM
XCloseIM.restype = c_int
XCloseIM.argtypes = [XIM]
XGetIMValues = _libraries['libX11.so.6'].XGetIMValues
XGetIMValues.restype = STRING
XGetIMValues.argtypes = [XIM]
XSetIMValues = _libraries['libX11.so.6'].XSetIMValues
XSetIMValues.restype = STRING
XSetIMValues.argtypes = [XIM]
XDisplayOfIM = _libraries['libX11.so.6'].XDisplayOfIM
XDisplayOfIM.restype = POINTER(Display)
XDisplayOfIM.argtypes = [XIM]
XLocaleOfIM = _libraries['libX11.so.6'].XLocaleOfIM
XLocaleOfIM.restype = STRING
XLocaleOfIM.argtypes = [XIM]
XCreateIC = _libraries['libX11.so.6'].XCreateIC
XCreateIC.restype = XIC
XCreateIC.argtypes = [XIM]
XDestroyIC = _libraries['libX11.so.6'].XDestroyIC
XDestroyIC.restype = None
XDestroyIC.argtypes = [XIC]
XSetICFocus = _libraries['libX11.so.6'].XSetICFocus
XSetICFocus.restype = None
XSetICFocus.argtypes = [XIC]
XUnsetICFocus = _libraries['libX11.so.6'].XUnsetICFocus
XUnsetICFocus.restype = None
XUnsetICFocus.argtypes = [XIC]
XwcResetIC = _libraries['libX11.so.6'].XwcResetIC
XwcResetIC.restype = WSTRING
XwcResetIC.argtypes = [XIC]
XmbResetIC = _libraries['libX11.so.6'].XmbResetIC
XmbResetIC.restype = STRING
XmbResetIC.argtypes = [XIC]
Xutf8ResetIC = _libraries['libX11.so.6'].Xutf8ResetIC
Xutf8ResetIC.restype = STRING
Xutf8ResetIC.argtypes = [XIC]
XSetICValues = _libraries['libX11.so.6'].XSetICValues
XSetICValues.restype = STRING
XSetICValues.argtypes = [XIC]
XGetICValues = _libraries['libX11.so.6'].XGetICValues
XGetICValues.restype = STRING
XGetICValues.argtypes = [XIC]
XIMOfIC = _libraries['libX11.so.6'].XIMOfIC
XIMOfIC.restype = XIM
XIMOfIC.argtypes = [XIC]
XFilterEvent = _libraries['libX11.so.6'].XFilterEvent
XFilterEvent.restype = c_int
XFilterEvent.argtypes = [POINTER(XEvent), Window]
XmbLookupString = _libraries['libX11.so.6'].XmbLookupString
XmbLookupString.restype = c_int
XmbLookupString.argtypes = [XIC, POINTER(XKeyPressedEvent), STRING, c_int, POINTER(KeySym), POINTER(c_int)]
XwcLookupString = _libraries['libX11.so.6'].XwcLookupString
XwcLookupString.restype = c_int
XwcLookupString.argtypes = [XIC, POINTER(XKeyPressedEvent), WSTRING, c_int, POINTER(KeySym), POINTER(c_int)]
Xutf8LookupString = _libraries['libX11.so.6'].Xutf8LookupString
Xutf8LookupString.restype = c_int
Xutf8LookupString.argtypes = [XIC, POINTER(XKeyPressedEvent), STRING, c_int, POINTER(KeySym), POINTER(c_int)]
XVaCreateNestedList = _libraries['libX11.so.6'].XVaCreateNestedList
XVaCreateNestedList.restype = XVaNestedList
XVaCreateNestedList.argtypes = [c_int]
XRegisterIMInstantiateCallback = _libraries['libX11.so.6'].XRegisterIMInstantiateCallback
XRegisterIMInstantiateCallback.restype = c_int
XRegisterIMInstantiateCallback.argtypes = [POINTER(Display), POINTER(_XrmHashBucketRec), STRING, STRING, XIDProc, XPointer]
XUnregisterIMInstantiateCallback = _libraries['libX11.so.6'].XUnregisterIMInstantiateCallback
XUnregisterIMInstantiateCallback.restype = c_int
XUnregisterIMInstantiateCallback.argtypes = [POINTER(Display), POINTER(_XrmHashBucketRec), STRING, STRING, XIDProc, XPointer]
XConnectionWatchProc = CFUNCTYPE(None, POINTER(Display), XPointer, c_int, c_int, POINTER(XPointer))
XInternalConnectionNumbers = _libraries['libX11.so.6'].XInternalConnectionNumbers
XInternalConnectionNumbers.restype = c_int
XInternalConnectionNumbers.argtypes = [POINTER(Display), POINTER(POINTER(c_int)), POINTER(c_int)]
XProcessInternalConnection = _libraries['libX11.so.6'].XProcessInternalConnection
XProcessInternalConnection.restype = None
XProcessInternalConnection.argtypes = [POINTER(Display), c_int]
XAddConnectionWatch = _libraries['libX11.so.6'].XAddConnectionWatch
XAddConnectionWatch.restype = c_int
XAddConnectionWatch.argtypes = [POINTER(Display), XConnectionWatchProc, XPointer]
XRemoveConnectionWatch = _libraries['libX11.so.6'].XRemoveConnectionWatch
XRemoveConnectionWatch.restype = None
XRemoveConnectionWatch.argtypes = [POINTER(Display), XConnectionWatchProc, XPointer]
XSetAuthorization = _libraries['libX11.so.6'].XSetAuthorization
XSetAuthorization.restype = None
XSetAuthorization.argtypes = [STRING, c_int, STRING, c_int]
_Xmbtowc = _libraries['libX11.so.6']._Xmbtowc
_Xmbtowc.restype = c_int
_Xmbtowc.argtypes = [WSTRING, STRING, c_int]
_Xwctomb = _libraries['libX11.so.6']._Xwctomb
_Xwctomb.restype = c_int
_Xwctomb.argtypes = [STRING, c_wchar]
XGetEventData = _libraries['libX11.so.6'].XGetEventData
XGetEventData.restype = c_int
XGetEventData.argtypes = [POINTER(Display), POINTER(XGenericEventCookie)]
XFreeEventData = _libraries['libX11.so.6'].XFreeEventData
XFreeEventData.restype = None
XFreeEventData.argtypes = [POINTER(Display), POINTER(XGenericEventCookie)]
_XGC._fields_ = [
    ('ext_data', POINTER(XExtData)),
    ('gid', GContext),
    ('rects', c_int),
    ('dashes', c_int),
    ('dirty', c_ulong),
    ('values', XGCValues),
]
class _XFreeFuncs(Structure):
    pass
class _XSQEvent(Structure):
    pass
class _XExten(Structure):
    pass
class _xEvent(Structure):
    pass
xEvent = _xEvent
class _XLockInfo(Structure):
    pass
class _XInternalAsync(Structure):
    pass
class _XLockPtrs(Structure):
    pass
class _XKeytrans(Structure):
    pass
class _XDisplayAtoms(Structure):
    pass
class _XContextDB(Structure):
    pass
class xError(Structure):
    pass
class N9_XDisplay5DOT_252E(Structure):
    pass
N9_XDisplay5DOT_252E._fields_ = [
    ('defaultCCCs', XPointer),
    ('clientCmaps', XPointer),
    ('perVisualIntensityMaps', XPointer),
]
class _XIMFilter(Structure):
    pass
class _XConnectionInfo(Structure):
    pass
class _XConnWatchInfo(Structure):
    pass
class _XkbInfoRec(Structure):
    pass
class _XtransConnInfo(Structure):
    pass
class _X11XCBPrivate(Structure):
    pass
_XDisplay._fields_ = [
    ('ext_data', POINTER(XExtData)),
    ('free_funcs', POINTER(_XFreeFuncs)),
    ('fd', c_int),
    ('conn_checker', c_int),
    ('proto_major_version', c_int),
    ('proto_minor_version', c_int),
    ('vendor', STRING),
    ('resource_base', XID),
    ('resource_mask', XID),
    ('resource_id', XID),
    ('resource_shift', c_int),
    ('resource_alloc', CFUNCTYPE(XID, POINTER(_XDisplay))),
    ('byte_order', c_int),
    ('bitmap_unit', c_int),
    ('bitmap_pad', c_int),
    ('bitmap_bit_order', c_int),
    ('nformats', c_int),
    ('pixmap_format', POINTER(ScreenFormat)),
    ('vnumber', c_int),
    ('release', c_int),
    ('head', POINTER(_XSQEvent)),
    ('tail', POINTER(_XSQEvent)),
    ('qlen', c_int),
    ('last_request_read', c_ulong),
    ('request', c_ulong),
    ('last_req', STRING),
    ('buffer', STRING),
    ('bufptr', STRING),
    ('bufmax', STRING),
    ('max_request_size', c_uint),
    ('db', POINTER(_XrmHashBucketRec)),
    ('synchandler', CFUNCTYPE(c_int, POINTER(_XDisplay))),
    ('display_name', STRING),
    ('default_screen', c_int),
    ('nscreens', c_int),
    ('screens', POINTER(Screen)),
    ('motion_buffer', c_ulong),
    ('flags', c_ulong),
    ('min_keycode', c_int),
    ('max_keycode', c_int),
    ('keysyms', POINTER(KeySym)),
    ('modifiermap', POINTER(XModifierKeymap)),
    ('keysyms_per_keycode', c_int),
    ('xdefaults', STRING),
    ('scratch_buffer', STRING),
    ('scratch_length', c_ulong),
    ('ext_number', c_int),
    ('ext_procs', POINTER(_XExten)),
    ('event_vec', CFUNCTYPE(c_int, POINTER(Display), POINTER(XEvent), POINTER(xEvent)) * 128),
    ('wire_vec', CFUNCTYPE(c_int, POINTER(Display), POINTER(XEvent), POINTER(xEvent)) * 128),
    ('lock_meaning', KeySym),
    ('lock', POINTER(_XLockInfo)),
    ('async_handlers', POINTER(_XInternalAsync)),
    ('bigreq_size', c_ulong),
    ('lock_fns', POINTER(_XLockPtrs)),
    ('idlist_alloc', CFUNCTYPE(None, POINTER(Display), POINTER(XID), c_int)),
    ('key_bindings', POINTER(_XKeytrans)),
    ('cursor_font', Font),
    ('atoms', POINTER(_XDisplayAtoms)),
    ('mode_switch', c_uint),
    ('num_lock', c_uint),
    ('context_db', POINTER(_XContextDB)),
    ('error_vec', CFUNCTYPE(c_int, POINTER(Display), POINTER(XErrorEvent), POINTER(xError))),
    ('cms', N9_XDisplay5DOT_252E),
    ('im_filters', POINTER(_XIMFilter)),
    ('qfree', POINTER(_XSQEvent)),
    ('next_event_serial_num', c_ulong),
    ('flushes', POINTER(_XExten)),
    ('im_fd_info', POINTER(_XConnectionInfo)),
    ('im_fd_length', c_int),
    ('conn_watchers', POINTER(_XConnWatchInfo)),
    ('watcher_count', c_int),
    ('filedes', XPointer),
    ('savedsynchandler', CFUNCTYPE(c_int, POINTER(Display))),
    ('resource_max', XID),
    ('xcmisc_opcode', c_int),
    ('xkb_info', POINTER(_XkbInfoRec)),
    ('trans_conn', POINTER(_XtransConnInfo)),
    ('xcb', POINTER(_X11XCBPrivate)),
    ('next_cookie', c_uint),
    ('generic_event_vec', CFUNCTYPE(c_int, POINTER(Display), POINTER(XGenericEventCookie), POINTER(xEvent)) * 128),
    ('generic_event_copy_vec', CFUNCTYPE(c_int, POINTER(Display), POINTER(XGenericEventCookie), POINTER(XGenericEventCookie)) * 128),
    ('cookiejar', c_void_p),
]
_XLockInfo._fields_ = [
]
_XKeytrans._fields_ = [
]
_XDisplayAtoms._fields_ = [
]
_XContextDB._fields_ = [
]
_XIMFilter._fields_ = [
]
_XkbInfoRec._fields_ = [
]
_XtransConnInfo._fields_ = [
]
_X11XCBPrivate._fields_ = [
]
_XEvent._fields_ = [
    ('type', c_int),
    ('xany', XAnyEvent),
    ('xkey', XKeyEvent),
    ('xbutton', XButtonEvent),
    ('xmotion', XMotionEvent),
    ('xcrossing', XCrossingEvent),
    ('xfocus', XFocusChangeEvent),
    ('xexpose', XExposeEvent),
    ('xgraphicsexpose', XGraphicsExposeEvent),
    ('xnoexpose', XNoExposeEvent),
    ('xvisibility', XVisibilityEvent),
    ('xcreatewindow', XCreateWindowEvent),
    ('xdestroywindow', XDestroyWindowEvent),
    ('xunmap', XUnmapEvent),
    ('xmap', XMapEvent),
    ('xmaprequest', XMapRequestEvent),
    ('xreparent', XReparentEvent),
    ('xconfigure', XConfigureEvent),
    ('xgravity', XGravityEvent),
    ('xresizerequest', XResizeRequestEvent),
    ('xconfigurerequest', XConfigureRequestEvent),
    ('xcirculate', XCirculateEvent),
    ('xcirculaterequest', XCirculateRequestEvent),
    ('xproperty', XPropertyEvent),
    ('xselectionclear', XSelectionClearEvent),
    ('xselectionrequest', XSelectionRequestEvent),
    ('xselection', XSelectionEvent),
    ('xcolormap', XColormapEvent),
    ('xclient', XClientMessageEvent),
    ('xmapping', XMappingEvent),
    ('xerror', XErrorEvent),
    ('xkeymap', XKeymapEvent),
    ('xgeneric', XGenericEvent),
    ('xcookie', XGenericEventCookie),
    ('pad', c_long * 24),
]
_XSQEvent._fields_ = [
    ('next', POINTER(_XSQEvent)),
    ('event', XEvent),
    ('qserial_num', c_ulong),
]
_XQEvent = _XSQEvent
class _LockInfoRec(Structure):
    pass
LockInfoPtr = POINTER(_LockInfoRec)
_LockInfoRec._fields_ = [
]
_XLockPtrs._fields_ = [
    ('lock_display', CFUNCTYPE(None, POINTER(Display))),
    ('unlock_display', CFUNCTYPE(None, POINTER(Display))),
]
_XCreateMutex_fn = (CFUNCTYPE(None, LockInfoPtr)).in_dll(_libraries['libX11.so.6'], '_XCreateMutex_fn')
_XFreeMutex_fn = (CFUNCTYPE(None, LockInfoPtr)).in_dll(_libraries['libX11.so.6'], '_XFreeMutex_fn')
_XLockMutex_fn = (CFUNCTYPE(None, LockInfoPtr)).in_dll(_libraries['libX11.so.6'], '_XLockMutex_fn')
_XUnlockMutex_fn = (CFUNCTYPE(None, LockInfoPtr)).in_dll(_libraries['libX11.so.6'], '_XUnlockMutex_fn')
_Xglobal_lock = (LockInfoPtr).in_dll(_libraries['libX11.so.6'], '_Xglobal_lock')
CARD8 = c_ubyte
size_t = c_ulong
_XGetRequest = _libraries['libX11.so.6']._XGetRequest
_XGetRequest.restype = c_void_p
_XGetRequest.argtypes = [POINTER(Display), CARD8, size_t]
_XFlushGCCache = _libraries['libX11.so.6']._XFlushGCCache
_XFlushGCCache.restype = None
_XFlushGCCache.argtypes = [POINTER(Display), GC]
_XData32 = _libraries['libX11.so.6']._XData32
_XData32.restype = c_int
_XData32.argtypes = [POINTER(Display), POINTER(c_long), c_uint]
_XRead32 = _libraries['libX11.so.6']._XRead32
_XRead32.restype = None
_XRead32.argtypes = [POINTER(Display), POINTER(c_long), c_long]
class xReply(Union):
    pass
_XInternalAsync._fields_ = [
    ('next', POINTER(_XInternalAsync)),
    ('handler', CFUNCTYPE(c_int, POINTER(Display), POINTER(xReply), STRING, c_int, XPointer)),
    ('data', XPointer),
]
_XAsyncHandler = _XInternalAsync
class _XAsyncEState(Structure):
    pass
_XAsyncEState._fields_ = [
    ('min_sequence_number', c_ulong),
    ('max_sequence_number', c_ulong),
    ('error_code', c_ubyte),
    ('major_opcode', c_ubyte),
    ('minor_opcode', c_ushort),
    ('last_error_received', c_ubyte),
    ('error_count', c_int),
]
_XAsyncErrorState = _XAsyncEState
_XDeqAsyncHandler = _libraries['libX11.so.6']._XDeqAsyncHandler
_XDeqAsyncHandler.restype = None
_XDeqAsyncHandler.argtypes = [POINTER(Display), POINTER(_XAsyncHandler)]
FreeFuncType = CFUNCTYPE(None, POINTER(Display))
FreeModmapType = CFUNCTYPE(c_int, POINTER(XModifierKeymap))
_XFreeFuncs._fields_ = [
    ('atoms', FreeFuncType),
    ('modifiermap', FreeModmapType),
    ('key_bindings', FreeFuncType),
    ('context_db', FreeFuncType),
    ('defaultCCCs', FreeFuncType),
    ('clientCmaps', FreeFuncType),
    ('intensityMaps', FreeFuncType),
    ('im_filters', FreeFuncType),
    ('xkb', FreeFuncType),
]
_XFreeFuncRec = _XFreeFuncs
CreateGCType = CFUNCTYPE(c_int, POINTER(Display), GC, POINTER(XExtCodes))
CopyGCType = CFUNCTYPE(c_int, POINTER(Display), GC, POINTER(XExtCodes))
FlushGCType = CFUNCTYPE(c_int, POINTER(Display), GC, POINTER(XExtCodes))
FreeGCType = CFUNCTYPE(c_int, POINTER(Display), GC, POINTER(XExtCodes))
CreateFontType = CFUNCTYPE(c_int, POINTER(Display), POINTER(XFontStruct), POINTER(XExtCodes))
FreeFontType = CFUNCTYPE(c_int, POINTER(Display), POINTER(XFontStruct), POINTER(XExtCodes))
CloseDisplayType = CFUNCTYPE(c_int, POINTER(Display), POINTER(XExtCodes))
ErrorType = CFUNCTYPE(c_int, POINTER(Display), POINTER(xError), POINTER(XExtCodes), POINTER(c_int))
ErrorStringType = CFUNCTYPE(STRING, POINTER(Display), c_int, POINTER(XExtCodes), STRING, c_int)
PrintErrorType = CFUNCTYPE(None, POINTER(Display), POINTER(XErrorEvent), c_void_p)
BeforeFlushType = CFUNCTYPE(None, POINTER(Display), POINTER(XExtCodes), STRING, c_long)
_XExten._fields_ = [
    ('next', POINTER(_XExten)),
    ('codes', XExtCodes),
    ('create_GC', CreateGCType),
    ('copy_GC', CopyGCType),
    ('flush_GC', FlushGCType),
    ('free_GC', FreeGCType),
    ('create_Font', CreateFontType),
    ('free_Font', FreeFontType),
    ('close_display', CloseDisplayType),
    ('error', ErrorType),
    ('error_string', ErrorStringType),
    ('name', STRING),
    ('error_values', PrintErrorType),
    ('before_flush', BeforeFlushType),
    ('next_flush', POINTER(_XExten)),
]
_XExtension = _XExten
_XError = _libraries['libX11.so.6']._XError
_XError.restype = c_int
_XError.argtypes = [POINTER(Display), POINTER(xError)]
_XIOError = _libraries['libX11.so.6']._XIOError
_XIOError.restype = c_int
_XIOError.argtypes = [POINTER(Display)]
_XIOErrorFunction = (CFUNCTYPE(c_int, POINTER(Display))).in_dll(_libraries['libX11.so.6'], '_XIOErrorFunction')
_XErrorFunction = (CFUNCTYPE(c_int, POINTER(Display), POINTER(XErrorEvent))).in_dll(_libraries['libX11.so.6'], '_XErrorFunction')
_XEatData = _libraries['libX11.so.6']._XEatData
_XEatData.restype = None
_XEatData.argtypes = [POINTER(Display), c_ulong]
_XEatDataWords = _libraries['libX11.so.6']._XEatDataWords
_XEatDataWords.restype = None
_XEatDataWords.argtypes = [POINTER(Display), c_ulong]
_XAllocScratch = _libraries['libX11.so.6']._XAllocScratch
_XAllocScratch.restype = STRING
_XAllocScratch.argtypes = [POINTER(Display), c_ulong]
_XAllocTemp = _libraries['libX11.so.6']._XAllocTemp
_XAllocTemp.restype = STRING
_XAllocTemp.argtypes = [POINTER(Display), c_ulong]
_XFreeTemp = _libraries['libX11.so.6']._XFreeTemp
_XFreeTemp.restype = None
_XFreeTemp.argtypes = [POINTER(Display), STRING, c_ulong]
_XVIDtoVisual = _libraries['libX11.so.6']._XVIDtoVisual
_XVIDtoVisual.restype = POINTER(Visual)
_XVIDtoVisual.argtypes = [POINTER(Display), VisualID]
class xGenericReply(Structure):
    pass
_XSetLastRequestRead = _libraries['libX11.so.6']._XSetLastRequestRead
_XSetLastRequestRead.restype = c_ulong
_XSetLastRequestRead.argtypes = [POINTER(Display), POINTER(xGenericReply)]
_XGetHostname = _libraries['libX11.so.6']._XGetHostname
_XGetHostname.restype = c_int
_XGetHostname.argtypes = [STRING, c_int]
_XScreenOfWindow = _libraries['libX11.so.6']._XScreenOfWindow
_XScreenOfWindow.restype = POINTER(Screen)
_XScreenOfWindow.argtypes = [POINTER(Display), Window]
_XAsyncErrorHandler = _libraries['libX11.so.6']._XAsyncErrorHandler
_XAsyncErrorHandler.restype = c_int
_XAsyncErrorHandler.argtypes = [POINTER(Display), POINTER(xReply), STRING, c_int, XPointer]
_XGetAsyncReply = _libraries['libX11.so.6']._XGetAsyncReply
_XGetAsyncReply.restype = STRING
_XGetAsyncReply.argtypes = [POINTER(Display), STRING, POINTER(xReply), STRING, c_int, c_int, c_int]
_XGetAsyncData = _libraries['libX11.so.6']._XGetAsyncData
_XGetAsyncData.restype = None
_XGetAsyncData.argtypes = [POINTER(Display), STRING, STRING, c_int, c_int, c_int, c_int]
_XFlush = _libraries['libX11.so.6']._XFlush
_XFlush.restype = None
_XFlush.argtypes = [POINTER(Display)]
_XEventsQueued = _libraries['libX11.so.6']._XEventsQueued
_XEventsQueued.restype = c_int
_XEventsQueued.argtypes = [POINTER(Display), c_int]
_XReadEvents = _libraries['libX11.so.6']._XReadEvents
_XReadEvents.restype = None
_XReadEvents.argtypes = [POINTER(Display)]
_XRead = _libraries['libX11.so.6']._XRead
_XRead.restype = c_int
_XRead.argtypes = [POINTER(Display), STRING, c_long]
_XReadPad = _libraries['libX11.so.6']._XReadPad
_XReadPad.restype = None
_XReadPad.argtypes = [POINTER(Display), STRING, c_long]
_XSend = _libraries['libX11.so.6']._XSend
_XSend.restype = None
_XSend.argtypes = [POINTER(Display), STRING, c_long]
_XReply = _libraries['libX11.so.6']._XReply
_XReply.restype = c_int
_XReply.argtypes = [POINTER(Display), POINTER(xReply), c_int, c_int]
_XEnq = _libraries['libX11.so.6']._XEnq
_XEnq.restype = None
_XEnq.argtypes = [POINTER(Display), POINTER(xEvent)]
_XDeq = _libraries['libX11.so.6']._XDeq
_XDeq.restype = None
_XDeq.argtypes = [POINTER(Display), POINTER(_XQEvent), POINTER(_XQEvent)]
_XUnknownWireEvent = _libraries['libX11.so.6']._XUnknownWireEvent
_XUnknownWireEvent.restype = c_int
_XUnknownWireEvent.argtypes = [POINTER(Display), POINTER(XEvent), POINTER(xEvent)]
_XUnknownWireEventCookie = _libraries['libX11.so.6']._XUnknownWireEventCookie
_XUnknownWireEventCookie.restype = c_int
_XUnknownWireEventCookie.argtypes = [POINTER(Display), POINTER(XGenericEventCookie), POINTER(xEvent)]
_XUnknownCopyEventCookie = _libraries['libX11.so.6']._XUnknownCopyEventCookie
_XUnknownCopyEventCookie.restype = c_int
_XUnknownCopyEventCookie.argtypes = [POINTER(Display), POINTER(XGenericEventCookie), POINTER(XGenericEventCookie)]
_XUnknownNativeEvent = _libraries['libX11.so.6']._XUnknownNativeEvent
_XUnknownNativeEvent.restype = c_int
_XUnknownNativeEvent.argtypes = [POINTER(Display), POINTER(XEvent), POINTER(xEvent)]
_XWireToEvent = _libraries['libX11.so.6']._XWireToEvent
_XWireToEvent.restype = c_int
_XWireToEvent.argtypes = [POINTER(Display), POINTER(XEvent), POINTER(xEvent)]
_XDefaultWireError = _libraries['libX11.so.6']._XDefaultWireError
_XDefaultWireError.restype = c_int
_XDefaultWireError.argtypes = [POINTER(Display), POINTER(XErrorEvent), POINTER(xError)]
_XPollfdCacheInit = _libraries['libX11.so.6']._XPollfdCacheInit
_XPollfdCacheInit.restype = c_int
_XPollfdCacheInit.argtypes = [POINTER(Display)]
_XPollfdCacheAdd = _libraries['libX11.so.6']._XPollfdCacheAdd
_XPollfdCacheAdd.restype = None
_XPollfdCacheAdd.argtypes = [POINTER(Display), c_int]
_XPollfdCacheDel = _libraries['libX11.so.6']._XPollfdCacheDel
_XPollfdCacheDel.restype = None
_XPollfdCacheDel.argtypes = [POINTER(Display), c_int]
_XAllocID = _libraries['libX11.so.6']._XAllocID
_XAllocID.restype = XID
_XAllocID.argtypes = [POINTER(Display)]
_XAllocIDs = _libraries['libX11.so.6']._XAllocIDs
_XAllocIDs.restype = None
_XAllocIDs.argtypes = [POINTER(Display), POINTER(XID), c_int]
_XFreeExtData = _libraries['libX11.so.6']._XFreeExtData
_XFreeExtData.restype = c_int
_XFreeExtData.argtypes = [POINTER(XExtData)]
XESetCreateGC = _libraries['libX11.so.6'].XESetCreateGC
XESetCreateGC.restype = CFUNCTYPE(c_int, POINTER(Display), GC, POINTER(XExtCodes))
XESetCreateGC.argtypes = [POINTER(Display), c_int, CFUNCTYPE(c_int, POINTER(Display), GC, POINTER(XExtCodes))]
XESetCopyGC = _libraries['libX11.so.6'].XESetCopyGC
XESetCopyGC.restype = CFUNCTYPE(c_int, POINTER(Display), GC, POINTER(XExtCodes))
XESetCopyGC.argtypes = [POINTER(Display), c_int, CFUNCTYPE(c_int, POINTER(Display), GC, POINTER(XExtCodes))]
XESetFlushGC = _libraries['libX11.so.6'].XESetFlushGC
XESetFlushGC.restype = CFUNCTYPE(c_int, POINTER(Display), GC, POINTER(XExtCodes))
XESetFlushGC.argtypes = [POINTER(Display), c_int, CFUNCTYPE(c_int, POINTER(Display), GC, POINTER(XExtCodes))]
XESetFreeGC = _libraries['libX11.so.6'].XESetFreeGC
XESetFreeGC.restype = CFUNCTYPE(c_int, POINTER(Display), GC, POINTER(XExtCodes))
XESetFreeGC.argtypes = [POINTER(Display), c_int, CFUNCTYPE(c_int, POINTER(Display), GC, POINTER(XExtCodes))]
XESetCreateFont = _libraries['libX11.so.6'].XESetCreateFont
XESetCreateFont.restype = CFUNCTYPE(c_int, POINTER(Display), POINTER(XFontStruct), POINTER(XExtCodes))
XESetCreateFont.argtypes = [POINTER(Display), c_int, CFUNCTYPE(c_int, POINTER(Display), POINTER(XFontStruct), POINTER(XExtCodes))]
XESetFreeFont = _libraries['libX11.so.6'].XESetFreeFont
XESetFreeFont.restype = CFUNCTYPE(c_int, POINTER(Display), POINTER(XFontStruct), POINTER(XExtCodes))
XESetFreeFont.argtypes = [POINTER(Display), c_int, CFUNCTYPE(c_int, POINTER(Display), POINTER(XFontStruct), POINTER(XExtCodes))]
XESetCloseDisplay = _libraries['libX11.so.6'].XESetCloseDisplay
XESetCloseDisplay.restype = CFUNCTYPE(c_int, POINTER(Display), POINTER(XExtCodes))
XESetCloseDisplay.argtypes = [POINTER(Display), c_int, CFUNCTYPE(c_int, POINTER(Display), POINTER(XExtCodes))]
XESetError = _libraries['libX11.so.6'].XESetError
XESetError.restype = CFUNCTYPE(c_int, POINTER(Display), POINTER(xError), POINTER(XExtCodes), POINTER(c_int))
XESetError.argtypes = [POINTER(Display), c_int, CFUNCTYPE(c_int, POINTER(Display), POINTER(xError), POINTER(XExtCodes), POINTER(c_int))]
XESetErrorString = _libraries['libX11.so.6'].XESetErrorString
XESetErrorString.restype = CFUNCTYPE(STRING, POINTER(Display), c_int, POINTER(XExtCodes), STRING, c_int)
XESetErrorString.argtypes = [POINTER(Display), c_int, CFUNCTYPE(STRING, POINTER(Display), c_int, POINTER(XExtCodes), STRING, c_int)]
XESetPrintErrorValues = _libraries['libX11.so.6'].XESetPrintErrorValues
XESetPrintErrorValues.restype = CFUNCTYPE(None, POINTER(Display), POINTER(XErrorEvent), c_void_p)
XESetPrintErrorValues.argtypes = [POINTER(Display), c_int, CFUNCTYPE(None, POINTER(Display), POINTER(XErrorEvent), c_void_p)]
XESetWireToEvent = _libraries['libX11.so.6'].XESetWireToEvent
XESetWireToEvent.restype = CFUNCTYPE(c_int, POINTER(Display), POINTER(XEvent), POINTER(xEvent))
XESetWireToEvent.argtypes = [POINTER(Display), c_int, CFUNCTYPE(c_int, POINTER(Display), POINTER(XEvent), POINTER(xEvent))]
XESetWireToEventCookie = _libraries['libX11.so.6'].XESetWireToEventCookie
XESetWireToEventCookie.restype = CFUNCTYPE(c_int, POINTER(Display), POINTER(XGenericEventCookie), POINTER(xEvent))
XESetWireToEventCookie.argtypes = [POINTER(Display), c_int, CFUNCTYPE(c_int, POINTER(Display), POINTER(XGenericEventCookie), POINTER(xEvent))]
XESetCopyEventCookie = _libraries['libX11.so.6'].XESetCopyEventCookie
XESetCopyEventCookie.restype = CFUNCTYPE(c_int, POINTER(Display), POINTER(XGenericEventCookie), POINTER(XGenericEventCookie))
XESetCopyEventCookie.argtypes = [POINTER(Display), c_int, CFUNCTYPE(c_int, POINTER(Display), POINTER(XGenericEventCookie), POINTER(XGenericEventCookie))]
XESetEventToWire = _libraries['libX11.so.6'].XESetEventToWire
XESetEventToWire.restype = CFUNCTYPE(c_int, POINTER(Display), POINTER(XEvent), POINTER(xEvent))
XESetEventToWire.argtypes = [POINTER(Display), c_int, CFUNCTYPE(c_int, POINTER(Display), POINTER(XEvent), POINTER(xEvent))]
XESetWireToError = _libraries['libX11.so.6'].XESetWireToError
XESetWireToError.restype = CFUNCTYPE(c_int, POINTER(Display), POINTER(XErrorEvent), POINTER(xError))
XESetWireToError.argtypes = [POINTER(Display), c_int, CFUNCTYPE(c_int, POINTER(Display), POINTER(XErrorEvent), POINTER(xError))]
XESetBeforeFlush = _libraries['libX11.so.6'].XESetBeforeFlush
XESetBeforeFlush.restype = CFUNCTYPE(None, POINTER(Display), POINTER(XExtCodes), STRING, c_long)
XESetBeforeFlush.argtypes = [POINTER(Display), c_int, CFUNCTYPE(None, POINTER(Display), POINTER(XExtCodes), STRING, c_long)]
_XInternalConnectionProc = CFUNCTYPE(None, POINTER(Display), c_int, XPointer)
_XRegisterInternalConnection = _libraries['libX11.so.6']._XRegisterInternalConnection
_XRegisterInternalConnection.restype = c_int
_XRegisterInternalConnection.argtypes = [POINTER(Display), c_int, _XInternalConnectionProc, XPointer]
_XUnregisterInternalConnection = _libraries['libX11.so.6']._XUnregisterInternalConnection
_XUnregisterInternalConnection.restype = None
_XUnregisterInternalConnection.argtypes = [POINTER(Display), c_int]
_XProcessInternalConnection = _libraries['libX11.so.6']._XProcessInternalConnection
_XProcessInternalConnection.restype = None
_XProcessInternalConnection.argtypes = [POINTER(Display), POINTER(_XConnectionInfo)]
_XConnectionInfo._fields_ = [
    ('fd', c_int),
    ('read_callback', _XInternalConnectionProc),
    ('call_data', XPointer),
    ('watch_data', POINTER(XPointer)),
    ('next', POINTER(_XConnectionInfo)),
]
_XConnWatchInfo._fields_ = [
    ('fn', XConnectionWatchProc),
    ('client_data', XPointer),
    ('next', POINTER(_XConnWatchInfo)),
]
_XTextHeight = _libraries['libX11.so.6']._XTextHeight
_XTextHeight.restype = c_int
_XTextHeight.argtypes = [POINTER(XFontStruct), STRING, c_int]
_XTextHeight16 = _libraries['libX11.so.6']._XTextHeight16
_XTextHeight16.restype = c_int
_XTextHeight16.argtypes = [POINTER(XFontStruct), POINTER(XChar2b), c_int]
_XEventToWire = _libraries['libX11.so.6']._XEventToWire
_XEventToWire.restype = c_int
_XEventToWire.argtypes = [POINTER(Display), POINTER(XEvent), POINTER(xEvent)]
_XF86LoadQueryLocaleFont = _libraries['libX11.so.6']._XF86LoadQueryLocaleFont
_XF86LoadQueryLocaleFont.restype = c_int
_XF86LoadQueryLocaleFont.argtypes = [POINTER(Display), STRING, POINTER(POINTER(XFontStruct)), POINTER(Font)]
class xChangeWindowAttributesReq(Structure):
    pass
_XProcessWindowAttributes = _libraries['libX11.so.6']._XProcessWindowAttributes
_XProcessWindowAttributes.restype = None
_XProcessWindowAttributes.argtypes = [POINTER(Display), POINTER(xChangeWindowAttributesReq), c_ulong, POINTER(XSetWindowAttributes)]
_XDefaultError = _libraries['libX11.so.6']._XDefaultError
_XDefaultError.restype = c_int
_XDefaultError.argtypes = [POINTER(Display), POINTER(XErrorEvent)]
_XDefaultIOError = _libraries['libX11.so.6']._XDefaultIOError
_XDefaultIOError.restype = c_int
_XDefaultIOError.argtypes = [POINTER(Display)]
_XSetClipRectangles = _libraries['libX11.so.6']._XSetClipRectangles
_XSetClipRectangles.restype = None
_XSetClipRectangles.argtypes = [POINTER(Display), GC, c_int, c_int, POINTER(XRectangle), c_int, c_int]
_XGetWindowAttributes = _libraries['libX11.so.6']._XGetWindowAttributes
_XGetWindowAttributes.restype = c_int
_XGetWindowAttributes.argtypes = [POINTER(Display), Window, POINTER(XWindowAttributes)]
_XPutBackEvent = _libraries['libX11.so.6']._XPutBackEvent
_XPutBackEvent.restype = c_int
_XPutBackEvent.argtypes = [POINTER(Display), POINTER(XEvent)]
_XIsEventCookie = _libraries['libX11.so.6']._XIsEventCookie
_XIsEventCookie.restype = c_int
_XIsEventCookie.argtypes = [POINTER(Display), POINTER(XEvent)]
_XFreeEventCookies = _libraries['libX11.so.6']._XFreeEventCookies
_XFreeEventCookies.restype = None
_XFreeEventCookies.argtypes = [POINTER(Display)]
_XStoreEventCookie = _libraries['libX11.so.6']._XStoreEventCookie
_XStoreEventCookie.restype = None
_XStoreEventCookie.argtypes = [POINTER(Display), POINTER(XEvent)]
_XFetchEventCookie = _libraries['libX11.so.6']._XFetchEventCookie
_XFetchEventCookie.restype = c_int
_XFetchEventCookie.argtypes = [POINTER(Display), POINTER(XGenericEventCookie)]
_XCopyEventCookie = _libraries['libX11.so.6']._XCopyEventCookie
_XCopyEventCookie.restype = c_int
_XCopyEventCookie.argtypes = [POINTER(Display), POINTER(XGenericEventCookie), POINTER(XGenericEventCookie)]
xlocaledir = _libraries['libX11.so.6'].xlocaledir
xlocaledir.restype = None
xlocaledir.argtypes = [STRING, c_int]
INT64 = c_long
INT32 = c_int
INT16 = c_short
INT8 = c_byte
CARD64 = c_ulong
CARD32 = c_uint
CARD16 = c_ushort
BITS32 = CARD32
BITS16 = CARD16
BYTE = CARD8
BOOL = CARD8
KeyButMask = CARD16
class xConnClientPrefix(Structure):
    pass
xConnClientPrefix._fields_ = [
    ('byteOrder', CARD8),
    ('pad', BYTE),
    ('majorVersion', CARD16),
    ('minorVersion', CARD16),
    ('nbytesAuthProto', CARD16),
    ('nbytesAuthString', CARD16),
    ('pad2', CARD16),
]
class xConnSetupPrefix(Structure):
    pass
xConnSetupPrefix._fields_ = [
    ('success', CARD8),
    ('lengthReason', BYTE),
    ('majorVersion', CARD16),
    ('minorVersion', CARD16),
    ('length', CARD16),
]
class xConnSetup(Structure):
    pass
xConnSetup._fields_ = [
    ('release', CARD32),
    ('ridBase', CARD32),
    ('ridMask', CARD32),
    ('motionBufferSize', CARD32),
    ('nbytesVendor', CARD16),
    ('maxRequestSize', CARD16),
    ('numRoots', CARD8),
    ('numFormats', CARD8),
    ('imageByteOrder', CARD8),
    ('bitmapBitOrder', CARD8),
    ('bitmapScanlineUnit', CARD8),
    ('bitmapScanlinePad', CARD8),
    ('minKeyCode', CARD8),
    ('maxKeyCode', CARD8),
    ('pad2', CARD32),
]
class xPixmapFormat(Structure):
    pass
xPixmapFormat._fields_ = [
    ('depth', CARD8),
    ('bitsPerPixel', CARD8),
    ('scanLinePad', CARD8),
    ('pad1', CARD8),
    ('pad2', CARD32),
]
class xDepth(Structure):
    pass
xDepth._fields_ = [
    ('depth', CARD8),
    ('pad1', CARD8),
    ('nVisuals', CARD16),
    ('pad2', CARD32),
]
class xVisualType(Structure):
    pass
xVisualType._fields_ = [
    ('visualID', CARD32),
    ('c_class', CARD8),
    ('bitsPerRGB', CARD8),
    ('colormapEntries', CARD16),
    ('redMask', CARD32),
    ('greenMask', CARD32),
    ('blueMask', CARD32),
    ('pad', CARD32),
]
class xWindowRoot(Structure):
    pass
xWindowRoot._fields_ = [
    ('windowId', CARD32),
    ('defaultColormap', CARD32),
    ('whitePixel', CARD32),
    ('blackPixel', CARD32),
    ('currentInputMask', CARD32),
    ('pixWidth', CARD16),
    ('pixHeight', CARD16),
    ('mmWidth', CARD16),
    ('mmHeight', CARD16),
    ('minInstalledMaps', CARD16),
    ('maxInstalledMaps', CARD16),
    ('rootVisualID', CARD32),
    ('backingStore', CARD8),
    ('saveUnders', BOOL),
    ('rootDepth', CARD8),
    ('nDepths', CARD8),
]
class xTimecoord(Structure):
    pass
xTimecoord._fields_ = [
    ('time', CARD32),
    ('x', INT16),
    ('y', INT16),
]
class xHostEntry(Structure):
    pass
xHostEntry._fields_ = [
    ('family', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
]
class xCharInfo(Structure):
    pass
xCharInfo._fields_ = [
    ('leftSideBearing', INT16),
    ('rightSideBearing', INT16),
    ('characterWidth', INT16),
    ('ascent', INT16),
    ('descent', INT16),
    ('attributes', CARD16),
]
class xFontProp(Structure):
    pass
xFontProp._fields_ = [
    ('name', CARD32),
    ('value', CARD32),
]
class xTextElt(Structure):
    pass
xTextElt._fields_ = [
    ('len', CARD8),
    ('delta', INT8),
]
class xColorItem(Structure):
    pass
xColorItem._fields_ = [
    ('pixel', CARD32),
    ('red', CARD16),
    ('green', CARD16),
    ('blue', CARD16),
    ('flags', CARD8),
    ('pad', CARD8),
]
class xrgb(Structure):
    pass
xrgb._fields_ = [
    ('red', CARD16),
    ('green', CARD16),
    ('blue', CARD16),
    ('pad', CARD16),
]
KEYCODE = CARD8
xGenericReply._fields_ = [
    ('type', BYTE),
    ('data1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('data00', CARD32),
    ('data01', CARD32),
    ('data02', CARD32),
    ('data03', CARD32),
    ('data04', CARD32),
    ('data05', CARD32),
]
class xGetWindowAttributesReply(Structure):
    pass
xGetWindowAttributesReply._fields_ = [
    ('type', BYTE),
    ('backingStore', CARD8),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('visualID', CARD32),
    ('c_class', CARD16),
    ('bitGravity', CARD8),
    ('winGravity', CARD8),
    ('backingBitPlanes', CARD32),
    ('backingPixel', CARD32),
    ('saveUnder', BOOL),
    ('mapInstalled', BOOL),
    ('mapState', CARD8),
    ('override', BOOL),
    ('colormap', CARD32),
    ('allEventMasks', CARD32),
    ('yourEventMask', CARD32),
    ('doNotPropagateMask', CARD16),
    ('pad', CARD16),
]
class xGetGeometryReply(Structure):
    pass
xGetGeometryReply._fields_ = [
    ('type', BYTE),
    ('depth', CARD8),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('root', CARD32),
    ('x', INT16),
    ('y', INT16),
    ('width', CARD16),
    ('height', CARD16),
    ('borderWidth', CARD16),
    ('pad1', CARD16),
    ('pad2', CARD32),
    ('pad3', CARD32),
]
class xQueryTreeReply(Structure):
    pass
xQueryTreeReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('root', CARD32),
    ('parent', CARD32),
    ('nChildren', CARD16),
    ('pad2', CARD16),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
]
class xInternAtomReply(Structure):
    pass
xInternAtomReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('atom', CARD32),
    ('pad2', CARD32),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
]
class xGetAtomNameReply(Structure):
    pass
xGetAtomNameReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('nameLength', CARD16),
    ('pad2', CARD16),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
    ('pad7', CARD32),
]
class xGetPropertyReply(Structure):
    pass
xGetPropertyReply._fields_ = [
    ('type', BYTE),
    ('format', CARD8),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('propertyType', CARD32),
    ('bytesAfter', CARD32),
    ('nItems', CARD32),
    ('pad1', CARD32),
    ('pad2', CARD32),
    ('pad3', CARD32),
]
class xListPropertiesReply(Structure):
    pass
xListPropertiesReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('nProperties', CARD16),
    ('pad2', CARD16),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
    ('pad7', CARD32),
]
class xGetSelectionOwnerReply(Structure):
    pass
xGetSelectionOwnerReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('owner', CARD32),
    ('pad2', CARD32),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
]
class xGrabPointerReply(Structure):
    pass
xGrabPointerReply._fields_ = [
    ('type', BYTE),
    ('status', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('pad1', CARD32),
    ('pad2', CARD32),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
]
xGrabKeyboardReply = xGrabPointerReply
class xQueryPointerReply(Structure):
    pass
xQueryPointerReply._fields_ = [
    ('type', BYTE),
    ('sameScreen', BOOL),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('root', CARD32),
    ('child', CARD32),
    ('rootX', INT16),
    ('rootY', INT16),
    ('winX', INT16),
    ('winY', INT16),
    ('mask', CARD16),
    ('pad1', CARD16),
    ('pad', CARD32),
]
class xGetMotionEventsReply(Structure):
    pass
xGetMotionEventsReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('nEvents', CARD32),
    ('pad2', CARD32),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
]
class xTranslateCoordsReply(Structure):
    pass
xTranslateCoordsReply._fields_ = [
    ('type', BYTE),
    ('sameScreen', BOOL),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('child', CARD32),
    ('dstX', INT16),
    ('dstY', INT16),
    ('pad2', CARD32),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
]
class xGetInputFocusReply(Structure):
    pass
xGetInputFocusReply._fields_ = [
    ('type', BYTE),
    ('revertTo', CARD8),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('focus', CARD32),
    ('pad1', CARD32),
    ('pad2', CARD32),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
]
class xQueryKeymapReply(Structure):
    pass
xQueryKeymapReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('map', BYTE * 32),
]
class _xQueryFontReply(Structure):
    pass
_xQueryFontReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('minBounds', xCharInfo),
    ('walign1', CARD32),
    ('maxBounds', xCharInfo),
    ('walign2', CARD32),
    ('minCharOrByte2', CARD16),
    ('maxCharOrByte2', CARD16),
    ('defaultChar', CARD16),
    ('nFontProps', CARD16),
    ('drawDirection', CARD8),
    ('minByte1', CARD8),
    ('maxByte1', CARD8),
    ('allCharsExist', BOOL),
    ('fontAscent', INT16),
    ('fontDescent', INT16),
    ('nCharInfos', CARD32),
]
xQueryFontReply = _xQueryFontReply
class xQueryTextExtentsReply(Structure):
    pass
xQueryTextExtentsReply._fields_ = [
    ('type', BYTE),
    ('drawDirection', CARD8),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('fontAscent', INT16),
    ('fontDescent', INT16),
    ('overallAscent', INT16),
    ('overallDescent', INT16),
    ('overallWidth', INT32),
    ('overallLeft', INT32),
    ('overallRight', INT32),
    ('pad', CARD32),
]
class xListFontsReply(Structure):
    pass
xListFontsReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('nFonts', CARD16),
    ('pad2', CARD16),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
    ('pad7', CARD32),
]
class xListFontsWithInfoReply(Structure):
    pass
xListFontsWithInfoReply._fields_ = [
    ('type', BYTE),
    ('nameLength', CARD8),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('minBounds', xCharInfo),
    ('walign1', CARD32),
    ('maxBounds', xCharInfo),
    ('walign2', CARD32),
    ('minCharOrByte2', CARD16),
    ('maxCharOrByte2', CARD16),
    ('defaultChar', CARD16),
    ('nFontProps', CARD16),
    ('drawDirection', CARD8),
    ('minByte1', CARD8),
    ('maxByte1', CARD8),
    ('allCharsExist', BOOL),
    ('fontAscent', INT16),
    ('fontDescent', INT16),
    ('nReplies', CARD32),
]
class xGetFontPathReply(Structure):
    pass
xGetFontPathReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('nPaths', CARD16),
    ('pad2', CARD16),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
    ('pad7', CARD32),
]
class xGetImageReply(Structure):
    pass
xGetImageReply._fields_ = [
    ('type', BYTE),
    ('depth', CARD8),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('visual', CARD32),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
    ('pad7', CARD32),
]
class xListInstalledColormapsReply(Structure):
    pass
xListInstalledColormapsReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('nColormaps', CARD16),
    ('pad2', CARD16),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
    ('pad7', CARD32),
]
class xAllocColorReply(Structure):
    pass
xAllocColorReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('red', CARD16),
    ('green', CARD16),
    ('blue', CARD16),
    ('pad2', CARD16),
    ('pixel', CARD32),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
]
class xAllocNamedColorReply(Structure):
    pass
xAllocNamedColorReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('pixel', CARD32),
    ('exactRed', CARD16),
    ('exactGreen', CARD16),
    ('exactBlue', CARD16),
    ('screenRed', CARD16),
    ('screenGreen', CARD16),
    ('screenBlue', CARD16),
    ('pad2', CARD32),
    ('pad3', CARD32),
]
class xAllocColorCellsReply(Structure):
    pass
xAllocColorCellsReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('nPixels', CARD16),
    ('nMasks', CARD16),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
    ('pad7', CARD32),
]
class xAllocColorPlanesReply(Structure):
    pass
xAllocColorPlanesReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('nPixels', CARD16),
    ('pad2', CARD16),
    ('redMask', CARD32),
    ('greenMask', CARD32),
    ('blueMask', CARD32),
    ('pad3', CARD32),
    ('pad4', CARD32),
]
class xQueryColorsReply(Structure):
    pass
xQueryColorsReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('nColors', CARD16),
    ('pad2', CARD16),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
    ('pad7', CARD32),
]
class xLookupColorReply(Structure):
    pass
xLookupColorReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('exactRed', CARD16),
    ('exactGreen', CARD16),
    ('exactBlue', CARD16),
    ('screenRed', CARD16),
    ('screenGreen', CARD16),
    ('screenBlue', CARD16),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
]
class xQueryBestSizeReply(Structure):
    pass
xQueryBestSizeReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('width', CARD16),
    ('height', CARD16),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
    ('pad7', CARD32),
]
class xQueryExtensionReply(Structure):
    pass
xQueryExtensionReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('present', BOOL),
    ('major_opcode', CARD8),
    ('first_event', CARD8),
    ('first_error', CARD8),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
    ('pad7', CARD32),
]
class xListExtensionsReply(Structure):
    pass
xListExtensionsReply._fields_ = [
    ('type', BYTE),
    ('nExtensions', CARD8),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('pad2', CARD32),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
    ('pad7', CARD32),
]
class xSetMappingReply(Structure):
    pass
xSetMappingReply._fields_ = [
    ('type', BYTE),
    ('success', CARD8),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('pad2', CARD32),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
    ('pad7', CARD32),
]
xSetPointerMappingReply = xSetMappingReply
xSetModifierMappingReply = xSetMappingReply
class xGetPointerMappingReply(Structure):
    pass
xGetPointerMappingReply._fields_ = [
    ('type', BYTE),
    ('nElts', CARD8),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('pad2', CARD32),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
    ('pad7', CARD32),
]
class xGetKeyboardMappingReply(Structure):
    pass
xGetKeyboardMappingReply._fields_ = [
    ('type', BYTE),
    ('keySymsPerKeyCode', CARD8),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('pad2', CARD32),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
    ('pad7', CARD32),
]
class xGetModifierMappingReply(Structure):
    pass
xGetModifierMappingReply._fields_ = [
    ('type', BYTE),
    ('numKeyPerModifier', CARD8),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('pad1', CARD32),
    ('pad2', CARD32),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
]
class xGetKeyboardControlReply(Structure):
    pass
xGetKeyboardControlReply._fields_ = [
    ('type', BYTE),
    ('globalAutoRepeat', BOOL),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('ledMask', CARD32),
    ('keyClickPercent', CARD8),
    ('bellPercent', CARD8),
    ('bellPitch', CARD16),
    ('bellDuration', CARD16),
    ('pad', CARD16),
    ('map', BYTE * 32),
]
class xGetPointerControlReply(Structure):
    pass
xGetPointerControlReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('accelNumerator', CARD16),
    ('accelDenominator', CARD16),
    ('threshold', CARD16),
    ('pad2', CARD16),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
]
class xGetScreenSaverReply(Structure):
    pass
xGetScreenSaverReply._fields_ = [
    ('type', BYTE),
    ('pad1', BYTE),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('timeout', CARD16),
    ('interval', CARD16),
    ('preferBlanking', BOOL),
    ('allowExposures', BOOL),
    ('pad2', CARD16),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
]
class xListHostsReply(Structure):
    pass
xListHostsReply._fields_ = [
    ('type', BYTE),
    ('enabled', BOOL),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('nHosts', CARD16),
    ('pad1', CARD16),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
    ('pad7', CARD32),
]
xError._fields_ = [
    ('type', BYTE),
    ('errorCode', BYTE),
    ('sequenceNumber', CARD16),
    ('resourceID', CARD32),
    ('minorCode', CARD16),
    ('majorCode', CARD8),
    ('pad1', BYTE),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
    ('pad7', CARD32),
]
class N7_xEvent5DOT_146E(Union):
    pass
class N7_xEvent5DOT_1465DOT_147E(Structure):
    pass
N7_xEvent5DOT_1465DOT_147E._fields_ = [
    ('type', BYTE),
    ('detail', BYTE),
    ('sequenceNumber', CARD16),
]
class N7_xEvent5DOT_1465DOT_148E(Structure):
    pass
N7_xEvent5DOT_1465DOT_148E._fields_ = [
    ('pad00', CARD32),
    ('time', CARD32),
    ('root', CARD32),
    ('event', CARD32),
    ('child', CARD32),
    ('rootX', INT16),
    ('rootY', INT16),
    ('eventX', INT16),
    ('eventY', INT16),
    ('state', KeyButMask),
    ('sameScreen', BOOL),
    ('pad1', BYTE),
]
class N7_xEvent5DOT_1465DOT_149E(Structure):
    pass
N7_xEvent5DOT_1465DOT_149E._fields_ = [
    ('pad00', CARD32),
    ('time', CARD32),
    ('root', CARD32),
    ('event', CARD32),
    ('child', CARD32),
    ('rootX', INT16),
    ('rootY', INT16),
    ('eventX', INT16),
    ('eventY', INT16),
    ('state', KeyButMask),
    ('mode', BYTE),
    ('flags', BYTE),
]
class N7_xEvent5DOT_1465DOT_150E(Structure):
    pass
N7_xEvent5DOT_1465DOT_150E._fields_ = [
    ('pad00', CARD32),
    ('window', CARD32),
    ('mode', BYTE),
    ('pad1', BYTE),
    ('pad2', BYTE),
    ('pad3', BYTE),
]
class N7_xEvent5DOT_1465DOT_151E(Structure):
    pass
N7_xEvent5DOT_1465DOT_151E._fields_ = [
    ('pad00', CARD32),
    ('window', CARD32),
    ('x', CARD16),
    ('y', CARD16),
    ('width', CARD16),
    ('height', CARD16),
    ('count', CARD16),
    ('pad2', CARD16),
]
class N7_xEvent5DOT_1465DOT_152E(Structure):
    pass
N7_xEvent5DOT_1465DOT_152E._fields_ = [
    ('pad00', CARD32),
    ('drawable', CARD32),
    ('x', CARD16),
    ('y', CARD16),
    ('width', CARD16),
    ('height', CARD16),
    ('minorEvent', CARD16),
    ('count', CARD16),
    ('majorEvent', BYTE),
    ('pad1', BYTE),
    ('pad2', BYTE),
    ('pad3', BYTE),
]
class N7_xEvent5DOT_1465DOT_153E(Structure):
    pass
N7_xEvent5DOT_1465DOT_153E._fields_ = [
    ('pad00', CARD32),
    ('drawable', CARD32),
    ('minorEvent', CARD16),
    ('majorEvent', BYTE),
    ('bpad', BYTE),
]
class N7_xEvent5DOT_1465DOT_154E(Structure):
    pass
N7_xEvent5DOT_1465DOT_154E._fields_ = [
    ('pad00', CARD32),
    ('window', CARD32),
    ('state', CARD8),
    ('pad1', BYTE),
    ('pad2', BYTE),
    ('pad3', BYTE),
]
class N7_xEvent5DOT_1465DOT_155E(Structure):
    pass
N7_xEvent5DOT_1465DOT_155E._fields_ = [
    ('pad00', CARD32),
    ('parent', CARD32),
    ('window', CARD32),
    ('x', INT16),
    ('y', INT16),
    ('width', CARD16),
    ('height', CARD16),
    ('borderWidth', CARD16),
    ('override', BOOL),
    ('bpad', BYTE),
]
class N7_xEvent5DOT_1465DOT_156E(Structure):
    pass
N7_xEvent5DOT_1465DOT_156E._fields_ = [
    ('pad00', CARD32),
    ('event', CARD32),
    ('window', CARD32),
]
class N7_xEvent5DOT_1465DOT_157E(Structure):
    pass
N7_xEvent5DOT_1465DOT_157E._fields_ = [
    ('pad00', CARD32),
    ('event', CARD32),
    ('window', CARD32),
    ('fromConfigure', BOOL),
    ('pad1', BYTE),
    ('pad2', BYTE),
    ('pad3', BYTE),
]
class N7_xEvent5DOT_1465DOT_158E(Structure):
    pass
N7_xEvent5DOT_1465DOT_158E._fields_ = [
    ('pad00', CARD32),
    ('event', CARD32),
    ('window', CARD32),
    ('override', BOOL),
    ('pad1', BYTE),
    ('pad2', BYTE),
    ('pad3', BYTE),
]
class N7_xEvent5DOT_1465DOT_159E(Structure):
    pass
N7_xEvent5DOT_1465DOT_159E._fields_ = [
    ('pad00', CARD32),
    ('parent', CARD32),
    ('window', CARD32),
]
class N7_xEvent5DOT_1465DOT_160E(Structure):
    pass
N7_xEvent5DOT_1465DOT_160E._fields_ = [
    ('pad00', CARD32),
    ('event', CARD32),
    ('window', CARD32),
    ('parent', CARD32),
    ('x', INT16),
    ('y', INT16),
    ('override', BOOL),
    ('pad1', BYTE),
    ('pad2', BYTE),
    ('pad3', BYTE),
]
class N7_xEvent5DOT_1465DOT_161E(Structure):
    pass
N7_xEvent5DOT_1465DOT_161E._fields_ = [
    ('pad00', CARD32),
    ('event', CARD32),
    ('window', CARD32),
    ('aboveSibling', CARD32),
    ('x', INT16),
    ('y', INT16),
    ('width', CARD16),
    ('height', CARD16),
    ('borderWidth', CARD16),
    ('override', BOOL),
    ('bpad', BYTE),
]
class N7_xEvent5DOT_1465DOT_162E(Structure):
    pass
N7_xEvent5DOT_1465DOT_162E._fields_ = [
    ('pad00', CARD32),
    ('parent', CARD32),
    ('window', CARD32),
    ('sibling', CARD32),
    ('x', INT16),
    ('y', INT16),
    ('width', CARD16),
    ('height', CARD16),
    ('borderWidth', CARD16),
    ('valueMask', CARD16),
    ('pad1', CARD32),
]
class N7_xEvent5DOT_1465DOT_163E(Structure):
    pass
N7_xEvent5DOT_1465DOT_163E._fields_ = [
    ('pad00', CARD32),
    ('event', CARD32),
    ('window', CARD32),
    ('x', INT16),
    ('y', INT16),
    ('pad1', CARD32),
    ('pad2', CARD32),
    ('pad3', CARD32),
    ('pad4', CARD32),
]
class N7_xEvent5DOT_1465DOT_164E(Structure):
    pass
N7_xEvent5DOT_1465DOT_164E._fields_ = [
    ('pad00', CARD32),
    ('window', CARD32),
    ('width', CARD16),
    ('height', CARD16),
]
class N7_xEvent5DOT_1465DOT_165E(Structure):
    pass
N7_xEvent5DOT_1465DOT_165E._fields_ = [
    ('pad00', CARD32),
    ('event', CARD32),
    ('window', CARD32),
    ('parent', CARD32),
    ('place', BYTE),
    ('pad1', BYTE),
    ('pad2', BYTE),
    ('pad3', BYTE),
]
class N7_xEvent5DOT_1465DOT_166E(Structure):
    pass
N7_xEvent5DOT_1465DOT_166E._fields_ = [
    ('pad00', CARD32),
    ('window', CARD32),
    ('atom', CARD32),
    ('time', CARD32),
    ('state', BYTE),
    ('pad1', BYTE),
    ('pad2', CARD16),
]
class N7_xEvent5DOT_1465DOT_167E(Structure):
    pass
N7_xEvent5DOT_1465DOT_167E._fields_ = [
    ('pad00', CARD32),
    ('time', CARD32),
    ('window', CARD32),
    ('atom', CARD32),
]
class N7_xEvent5DOT_1465DOT_168E(Structure):
    pass
N7_xEvent5DOT_1465DOT_168E._fields_ = [
    ('pad00', CARD32),
    ('time', CARD32),
    ('owner', CARD32),
    ('requestor', CARD32),
    ('selection', CARD32),
    ('target', CARD32),
    ('property', CARD32),
]
class N7_xEvent5DOT_1465DOT_169E(Structure):
    pass
N7_xEvent5DOT_1465DOT_169E._fields_ = [
    ('pad00', CARD32),
    ('time', CARD32),
    ('requestor', CARD32),
    ('selection', CARD32),
    ('target', CARD32),
    ('property', CARD32),
]
class N7_xEvent5DOT_1465DOT_170E(Structure):
    pass
N7_xEvent5DOT_1465DOT_170E._fields_ = [
    ('pad00', CARD32),
    ('window', CARD32),
    ('colormap', CARD32),
    ('c_new', BOOL),
    ('state', BYTE),
    ('pad1', BYTE),
    ('pad2', BYTE),
]
class N7_xEvent5DOT_1465DOT_171E(Structure):
    pass
N7_xEvent5DOT_1465DOT_171E._fields_ = [
    ('pad00', CARD32),
    ('request', CARD8),
    ('firstKeyCode', CARD8),
    ('count', CARD8),
    ('pad1', BYTE),
]
class N7_xEvent5DOT_1465DOT_172E(Structure):
    pass
class N7_xEvent5DOT_1465DOT_1725DOT_173E(Union):
    pass
class N7_xEvent5DOT_1465DOT_1725DOT_1735DOT_174E(Structure):
    pass
N7_xEvent5DOT_1465DOT_1725DOT_1735DOT_174E._fields_ = [
    ('type', CARD32),
    ('longs0', INT32),
    ('longs1', INT32),
    ('longs2', INT32),
    ('longs3', INT32),
    ('longs4', INT32),
]
class N7_xEvent5DOT_1465DOT_1725DOT_1735DOT_175E(Structure):
    pass
N7_xEvent5DOT_1465DOT_1725DOT_1735DOT_175E._fields_ = [
    ('type', CARD32),
    ('shorts0', INT16),
    ('shorts1', INT16),
    ('shorts2', INT16),
    ('shorts3', INT16),
    ('shorts4', INT16),
    ('shorts5', INT16),
    ('shorts6', INT16),
    ('shorts7', INT16),
    ('shorts8', INT16),
    ('shorts9', INT16),
]
class N7_xEvent5DOT_1465DOT_1725DOT_1735DOT_176E(Structure):
    pass
N7_xEvent5DOT_1465DOT_1725DOT_1735DOT_176E._fields_ = [
    ('type', CARD32),
    ('bytes', INT8 * 20),
]
N7_xEvent5DOT_1465DOT_1725DOT_173E._fields_ = [
    ('l', N7_xEvent5DOT_1465DOT_1725DOT_1735DOT_174E),
    ('s', N7_xEvent5DOT_1465DOT_1725DOT_1735DOT_175E),
    ('b', N7_xEvent5DOT_1465DOT_1725DOT_1735DOT_176E),
]
N7_xEvent5DOT_1465DOT_172E._fields_ = [
    ('pad00', CARD32),
    ('window', CARD32),
    ('u', N7_xEvent5DOT_1465DOT_1725DOT_173E),
]
N7_xEvent5DOT_146E._fields_ = [
    ('u', N7_xEvent5DOT_1465DOT_147E),
    ('keyButtonPointer', N7_xEvent5DOT_1465DOT_148E),
    ('enterLeave', N7_xEvent5DOT_1465DOT_149E),
    ('focus', N7_xEvent5DOT_1465DOT_150E),
    ('expose', N7_xEvent5DOT_1465DOT_151E),
    ('graphicsExposure', N7_xEvent5DOT_1465DOT_152E),
    ('noExposure', N7_xEvent5DOT_1465DOT_153E),
    ('visibility', N7_xEvent5DOT_1465DOT_154E),
    ('createNotify', N7_xEvent5DOT_1465DOT_155E),
    ('destroyNotify', N7_xEvent5DOT_1465DOT_156E),
    ('unmapNotify', N7_xEvent5DOT_1465DOT_157E),
    ('mapNotify', N7_xEvent5DOT_1465DOT_158E),
    ('mapRequest', N7_xEvent5DOT_1465DOT_159E),
    ('reparent', N7_xEvent5DOT_1465DOT_160E),
    ('configureNotify', N7_xEvent5DOT_1465DOT_161E),
    ('configureRequest', N7_xEvent5DOT_1465DOT_162E),
    ('gravity', N7_xEvent5DOT_1465DOT_163E),
    ('resizeRequest', N7_xEvent5DOT_1465DOT_164E),
    ('circulate', N7_xEvent5DOT_1465DOT_165E),
    ('property', N7_xEvent5DOT_1465DOT_166E),
    ('selectionClear', N7_xEvent5DOT_1465DOT_167E),
    ('selectionRequest', N7_xEvent5DOT_1465DOT_168E),
    ('selectionNotify', N7_xEvent5DOT_1465DOT_169E),
    ('colormap', N7_xEvent5DOT_1465DOT_170E),
    ('mappingNotify', N7_xEvent5DOT_1465DOT_171E),
    ('clientMessage', N7_xEvent5DOT_1465DOT_172E),
]
_xEvent._fields_ = [
    ('u', N7_xEvent5DOT_146E),
]
class xGenericEvent(Structure):
    pass
xGenericEvent._fields_ = [
    ('type', BYTE),
    ('extension', CARD8),
    ('sequenceNumber', CARD16),
    ('length', CARD32),
    ('evtype', CARD16),
    ('pad2', CARD16),
    ('pad3', CARD32),
    ('pad4', CARD32),
    ('pad5', CARD32),
    ('pad6', CARD32),
    ('pad7', CARD32),
]
class xKeymapEvent(Structure):
    pass
xKeymapEvent._fields_ = [
    ('type', BYTE),
    ('map', BYTE * 31),
]
class _xReq(Structure):
    pass
_xReq._fields_ = [
    ('reqType', CARD8),
    ('data', CARD8),
    ('length', CARD16),
]
xReq = _xReq
class xResourceReq(Structure):
    pass
xResourceReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('id', CARD32),
]
class xCreateWindowReq(Structure):
    pass
xCreateWindowReq._fields_ = [
    ('reqType', CARD8),
    ('depth', CARD8),
    ('length', CARD16),
    ('wid', CARD32),
    ('parent', CARD32),
    ('x', INT16),
    ('y', INT16),
    ('width', CARD16),
    ('height', CARD16),
    ('borderWidth', CARD16),
    ('c_class', CARD16),
    ('visual', CARD32),
    ('mask', CARD32),
]
xChangeWindowAttributesReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('window', CARD32),
    ('valueMask', CARD32),
]
class xChangeSaveSetReq(Structure):
    pass
xChangeSaveSetReq._fields_ = [
    ('reqType', CARD8),
    ('mode', BYTE),
    ('length', CARD16),
    ('window', CARD32),
]
class xReparentWindowReq(Structure):
    pass
xReparentWindowReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('window', CARD32),
    ('parent', CARD32),
    ('x', INT16),
    ('y', INT16),
]
class xConfigureWindowReq(Structure):
    pass
xConfigureWindowReq._fields_ = [
    ('reqType', CARD8),
    ('pad', CARD8),
    ('length', CARD16),
    ('window', CARD32),
    ('mask', CARD16),
    ('pad2', CARD16),
]
class xCirculateWindowReq(Structure):
    pass
xCirculateWindowReq._fields_ = [
    ('reqType', CARD8),
    ('direction', CARD8),
    ('length', CARD16),
    ('window', CARD32),
]
class xInternAtomReq(Structure):
    pass
xInternAtomReq._fields_ = [
    ('reqType', CARD8),
    ('onlyIfExists', BOOL),
    ('length', CARD16),
    ('nbytes', CARD16),
    ('pad', CARD16),
]
class xChangePropertyReq(Structure):
    pass
xChangePropertyReq._fields_ = [
    ('reqType', CARD8),
    ('mode', CARD8),
    ('length', CARD16),
    ('window', CARD32),
    ('property', CARD32),
    ('type', CARD32),
    ('format', CARD8),
    ('pad', BYTE * 3),
    ('nUnits', CARD32),
]
class xDeletePropertyReq(Structure):
    pass
xDeletePropertyReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('window', CARD32),
    ('property', CARD32),
]
class xGetPropertyReq(Structure):
    pass
xGetPropertyReq._fields_ = [
    ('reqType', CARD8),
    ('c_delete', BOOL),
    ('length', CARD16),
    ('window', CARD32),
    ('property', CARD32),
    ('type', CARD32),
    ('longOffset', CARD32),
    ('longLength', CARD32),
]
class xSetSelectionOwnerReq(Structure):
    pass
xSetSelectionOwnerReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('window', CARD32),
    ('selection', CARD32),
    ('time', CARD32),
]
class xConvertSelectionReq(Structure):
    pass
xConvertSelectionReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('requestor', CARD32),
    ('selection', CARD32),
    ('target', CARD32),
    ('property', CARD32),
    ('time', CARD32),
]
class xSendEventReq(Structure):
    pass
xSendEventReq._fields_ = [
    ('reqType', CARD8),
    ('propagate', BOOL),
    ('length', CARD16),
    ('destination', CARD32),
    ('eventMask', CARD32),
    ('event', xEvent),
]
class xGrabPointerReq(Structure):
    pass
xGrabPointerReq._fields_ = [
    ('reqType', CARD8),
    ('ownerEvents', BOOL),
    ('length', CARD16),
    ('grabWindow', CARD32),
    ('eventMask', CARD16),
    ('pointerMode', BYTE),
    ('keyboardMode', BYTE),
    ('confineTo', CARD32),
    ('cursor', CARD32),
    ('time', CARD32),
]
class xGrabButtonReq(Structure):
    pass
xGrabButtonReq._fields_ = [
    ('reqType', CARD8),
    ('ownerEvents', BOOL),
    ('length', CARD16),
    ('grabWindow', CARD32),
    ('eventMask', CARD16),
    ('pointerMode', BYTE),
    ('keyboardMode', BYTE),
    ('confineTo', CARD32),
    ('cursor', CARD32),
    ('button', CARD8),
    ('pad', BYTE),
    ('modifiers', CARD16),
]
class xUngrabButtonReq(Structure):
    pass
xUngrabButtonReq._fields_ = [
    ('reqType', CARD8),
    ('button', CARD8),
    ('length', CARD16),
    ('grabWindow', CARD32),
    ('modifiers', CARD16),
    ('pad', CARD16),
]
class xChangeActivePointerGrabReq(Structure):
    pass
xChangeActivePointerGrabReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('cursor', CARD32),
    ('time', CARD32),
    ('eventMask', CARD16),
    ('pad2', CARD16),
]
class xGrabKeyboardReq(Structure):
    pass
xGrabKeyboardReq._fields_ = [
    ('reqType', CARD8),
    ('ownerEvents', BOOL),
    ('length', CARD16),
    ('grabWindow', CARD32),
    ('time', CARD32),
    ('pointerMode', BYTE),
    ('keyboardMode', BYTE),
    ('pad', CARD16),
]
class xGrabKeyReq(Structure):
    pass
xGrabKeyReq._fields_ = [
    ('reqType', CARD8),
    ('ownerEvents', BOOL),
    ('length', CARD16),
    ('grabWindow', CARD32),
    ('modifiers', CARD16),
    ('key', CARD8),
    ('pointerMode', BYTE),
    ('keyboardMode', BYTE),
    ('pad1', BYTE),
    ('pad2', BYTE),
    ('pad3', BYTE),
]
class xUngrabKeyReq(Structure):
    pass
xUngrabKeyReq._fields_ = [
    ('reqType', CARD8),
    ('key', CARD8),
    ('length', CARD16),
    ('grabWindow', CARD32),
    ('modifiers', CARD16),
    ('pad', CARD16),
]
class xAllowEventsReq(Structure):
    pass
xAllowEventsReq._fields_ = [
    ('reqType', CARD8),
    ('mode', CARD8),
    ('length', CARD16),
    ('time', CARD32),
]
class xGetMotionEventsReq(Structure):
    pass
xGetMotionEventsReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('window', CARD32),
    ('start', CARD32),
    ('stop', CARD32),
]
class xTranslateCoordsReq(Structure):
    pass
xTranslateCoordsReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('srcWid', CARD32),
    ('dstWid', CARD32),
    ('srcX', INT16),
    ('srcY', INT16),
]
class xWarpPointerReq(Structure):
    pass
xWarpPointerReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('srcWid', CARD32),
    ('dstWid', CARD32),
    ('srcX', INT16),
    ('srcY', INT16),
    ('srcWidth', CARD16),
    ('srcHeight', CARD16),
    ('dstX', INT16),
    ('dstY', INT16),
]
class xSetInputFocusReq(Structure):
    pass
xSetInputFocusReq._fields_ = [
    ('reqType', CARD8),
    ('revertTo', CARD8),
    ('length', CARD16),
    ('focus', CARD32),
    ('time', CARD32),
]
class xOpenFontReq(Structure):
    pass
xOpenFontReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('fid', CARD32),
    ('nbytes', CARD16),
    ('pad1', BYTE),
    ('pad2', BYTE),
]
class xQueryTextExtentsReq(Structure):
    pass
xQueryTextExtentsReq._fields_ = [
    ('reqType', CARD8),
    ('oddLength', BOOL),
    ('length', CARD16),
    ('fid', CARD32),
]
class xListFontsReq(Structure):
    pass
xListFontsReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('maxNames', CARD16),
    ('nbytes', CARD16),
]
xListFontsWithInfoReq = xListFontsReq
class xSetFontPathReq(Structure):
    pass
xSetFontPathReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('nFonts', CARD16),
    ('pad1', BYTE),
    ('pad2', BYTE),
]
class xCreatePixmapReq(Structure):
    pass
xCreatePixmapReq._fields_ = [
    ('reqType', CARD8),
    ('depth', CARD8),
    ('length', CARD16),
    ('pid', CARD32),
    ('drawable', CARD32),
    ('width', CARD16),
    ('height', CARD16),
]
class xCreateGCReq(Structure):
    pass
xCreateGCReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('gc', CARD32),
    ('drawable', CARD32),
    ('mask', CARD32),
]
class xChangeGCReq(Structure):
    pass
xChangeGCReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('gc', CARD32),
    ('mask', CARD32),
]
class xCopyGCReq(Structure):
    pass
xCopyGCReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('srcGC', CARD32),
    ('dstGC', CARD32),
    ('mask', CARD32),
]
class xSetDashesReq(Structure):
    pass
xSetDashesReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('gc', CARD32),
    ('dashOffset', CARD16),
    ('nDashes', CARD16),
]
class xSetClipRectanglesReq(Structure):
    pass
xSetClipRectanglesReq._fields_ = [
    ('reqType', CARD8),
    ('ordering', BYTE),
    ('length', CARD16),
    ('gc', CARD32),
    ('xOrigin', INT16),
    ('yOrigin', INT16),
]
class xClearAreaReq(Structure):
    pass
xClearAreaReq._fields_ = [
    ('reqType', CARD8),
    ('exposures', BOOL),
    ('length', CARD16),
    ('window', CARD32),
    ('x', INT16),
    ('y', INT16),
    ('width', CARD16),
    ('height', CARD16),
]
class xCopyAreaReq(Structure):
    pass
xCopyAreaReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('srcDrawable', CARD32),
    ('dstDrawable', CARD32),
    ('gc', CARD32),
    ('srcX', INT16),
    ('srcY', INT16),
    ('dstX', INT16),
    ('dstY', INT16),
    ('width', CARD16),
    ('height', CARD16),
]
class xCopyPlaneReq(Structure):
    pass
xCopyPlaneReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('srcDrawable', CARD32),
    ('dstDrawable', CARD32),
    ('gc', CARD32),
    ('srcX', INT16),
    ('srcY', INT16),
    ('dstX', INT16),
    ('dstY', INT16),
    ('width', CARD16),
    ('height', CARD16),
    ('bitPlane', CARD32),
]
class xPolyPointReq(Structure):
    pass
xPolyPointReq._fields_ = [
    ('reqType', CARD8),
    ('coordMode', BYTE),
    ('length', CARD16),
    ('drawable', CARD32),
    ('gc', CARD32),
]
xPolyLineReq = xPolyPointReq
class xPolySegmentReq(Structure):
    pass
xPolySegmentReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('drawable', CARD32),
    ('gc', CARD32),
]
xPolyArcReq = xPolySegmentReq
xPolyRectangleReq = xPolySegmentReq
xPolyFillRectangleReq = xPolySegmentReq
xPolyFillArcReq = xPolySegmentReq
class _FillPolyReq(Structure):
    pass
_FillPolyReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('drawable', CARD32),
    ('gc', CARD32),
    ('shape', BYTE),
    ('coordMode', BYTE),
    ('pad1', CARD16),
]
xFillPolyReq = _FillPolyReq
class _PutImageReq(Structure):
    pass
_PutImageReq._fields_ = [
    ('reqType', CARD8),
    ('format', CARD8),
    ('length', CARD16),
    ('drawable', CARD32),
    ('gc', CARD32),
    ('width', CARD16),
    ('height', CARD16),
    ('dstX', INT16),
    ('dstY', INT16),
    ('leftPad', CARD8),
    ('depth', CARD8),
    ('pad', CARD16),
]
xPutImageReq = _PutImageReq
class xGetImageReq(Structure):
    pass
xGetImageReq._fields_ = [
    ('reqType', CARD8),
    ('format', CARD8),
    ('length', CARD16),
    ('drawable', CARD32),
    ('x', INT16),
    ('y', INT16),
    ('width', CARD16),
    ('height', CARD16),
    ('planeMask', CARD32),
]
class xPolyTextReq(Structure):
    pass
xPolyTextReq._fields_ = [
    ('reqType', CARD8),
    ('pad', CARD8),
    ('length', CARD16),
    ('drawable', CARD32),
    ('gc', CARD32),
    ('x', INT16),
    ('y', INT16),
]
xPolyText8Req = xPolyTextReq
xPolyText16Req = xPolyTextReq
class xImageTextReq(Structure):
    pass
xImageTextReq._fields_ = [
    ('reqType', CARD8),
    ('nChars', BYTE),
    ('length', CARD16),
    ('drawable', CARD32),
    ('gc', CARD32),
    ('x', INT16),
    ('y', INT16),
]
xImageText8Req = xImageTextReq
xImageText16Req = xImageTextReq
class xCreateColormapReq(Structure):
    pass
xCreateColormapReq._fields_ = [
    ('reqType', CARD8),
    ('alloc', BYTE),
    ('length', CARD16),
    ('mid', CARD32),
    ('window', CARD32),
    ('visual', CARD32),
]
class xCopyColormapAndFreeReq(Structure):
    pass
xCopyColormapAndFreeReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('mid', CARD32),
    ('srcCmap', CARD32),
]
class xAllocColorReq(Structure):
    pass
xAllocColorReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('cmap', CARD32),
    ('red', CARD16),
    ('green', CARD16),
    ('blue', CARD16),
    ('pad2', CARD16),
]
class xAllocNamedColorReq(Structure):
    pass
xAllocNamedColorReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('cmap', CARD32),
    ('nbytes', CARD16),
    ('pad1', BYTE),
    ('pad2', BYTE),
]
class xAllocColorCellsReq(Structure):
    pass
xAllocColorCellsReq._fields_ = [
    ('reqType', CARD8),
    ('contiguous', BOOL),
    ('length', CARD16),
    ('cmap', CARD32),
    ('colors', CARD16),
    ('planes', CARD16),
]
class xAllocColorPlanesReq(Structure):
    pass
xAllocColorPlanesReq._fields_ = [
    ('reqType', CARD8),
    ('contiguous', BOOL),
    ('length', CARD16),
    ('cmap', CARD32),
    ('colors', CARD16),
    ('red', CARD16),
    ('green', CARD16),
    ('blue', CARD16),
]
class xFreeColorsReq(Structure):
    pass
xFreeColorsReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('cmap', CARD32),
    ('planeMask', CARD32),
]
class xStoreColorsReq(Structure):
    pass
xStoreColorsReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('cmap', CARD32),
]
class xStoreNamedColorReq(Structure):
    pass
xStoreNamedColorReq._fields_ = [
    ('reqType', CARD8),
    ('flags', CARD8),
    ('length', CARD16),
    ('cmap', CARD32),
    ('pixel', CARD32),
    ('nbytes', CARD16),
    ('pad1', BYTE),
    ('pad2', BYTE),
]
class xQueryColorsReq(Structure):
    pass
xQueryColorsReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('cmap', CARD32),
]
class xLookupColorReq(Structure):
    pass
xLookupColorReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('cmap', CARD32),
    ('nbytes', CARD16),
    ('pad1', BYTE),
    ('pad2', BYTE),
]
class xCreateCursorReq(Structure):
    pass
xCreateCursorReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('cid', CARD32),
    ('source', CARD32),
    ('mask', CARD32),
    ('foreRed', CARD16),
    ('foreGreen', CARD16),
    ('foreBlue', CARD16),
    ('backRed', CARD16),
    ('backGreen', CARD16),
    ('backBlue', CARD16),
    ('x', CARD16),
    ('y', CARD16),
]
class xCreateGlyphCursorReq(Structure):
    pass
xCreateGlyphCursorReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('cid', CARD32),
    ('source', CARD32),
    ('mask', CARD32),
    ('sourceChar', CARD16),
    ('maskChar', CARD16),
    ('foreRed', CARD16),
    ('foreGreen', CARD16),
    ('foreBlue', CARD16),
    ('backRed', CARD16),
    ('backGreen', CARD16),
    ('backBlue', CARD16),
]
class xRecolorCursorReq(Structure):
    pass
xRecolorCursorReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('cursor', CARD32),
    ('foreRed', CARD16),
    ('foreGreen', CARD16),
    ('foreBlue', CARD16),
    ('backRed', CARD16),
    ('backGreen', CARD16),
    ('backBlue', CARD16),
]
class xQueryBestSizeReq(Structure):
    pass
xQueryBestSizeReq._fields_ = [
    ('reqType', CARD8),
    ('c_class', CARD8),
    ('length', CARD16),
    ('drawable', CARD32),
    ('width', CARD16),
    ('height', CARD16),
]
class xQueryExtensionReq(Structure):
    pass
xQueryExtensionReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('nbytes', CARD16),
    ('pad1', BYTE),
    ('pad2', BYTE),
]
class xSetModifierMappingReq(Structure):
    pass
xSetModifierMappingReq._fields_ = [
    ('reqType', CARD8),
    ('numKeyPerModifier', CARD8),
    ('length', CARD16),
]
class xSetPointerMappingReq(Structure):
    pass
xSetPointerMappingReq._fields_ = [
    ('reqType', CARD8),
    ('nElts', CARD8),
    ('length', CARD16),
]
class xGetKeyboardMappingReq(Structure):
    pass
xGetKeyboardMappingReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('firstKeyCode', CARD8),
    ('count', CARD8),
    ('pad1', CARD16),
]
class xChangeKeyboardMappingReq(Structure):
    pass
xChangeKeyboardMappingReq._fields_ = [
    ('reqType', CARD8),
    ('keyCodes', CARD8),
    ('length', CARD16),
    ('firstKeyCode', CARD8),
    ('keySymsPerKeyCode', CARD8),
    ('pad1', CARD16),
]
class xChangeKeyboardControlReq(Structure):
    pass
xChangeKeyboardControlReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('mask', CARD32),
]
class xBellReq(Structure):
    pass
xBellReq._fields_ = [
    ('reqType', CARD8),
    ('percent', INT8),
    ('length', CARD16),
]
class xChangePointerControlReq(Structure):
    pass
xChangePointerControlReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('accelNum', INT16),
    ('accelDenum', INT16),
    ('threshold', INT16),
    ('doAccel', BOOL),
    ('doThresh', BOOL),
]
class xSetScreenSaverReq(Structure):
    pass
xSetScreenSaverReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('timeout', INT16),
    ('interval', INT16),
    ('preferBlank', BYTE),
    ('allowExpose', BYTE),
    ('pad2', CARD16),
]
class xChangeHostsReq(Structure):
    pass
xChangeHostsReq._fields_ = [
    ('reqType', CARD8),
    ('mode', BYTE),
    ('length', CARD16),
    ('hostFamily', CARD8),
    ('pad', BYTE),
    ('hostLength', CARD16),
]
class xListHostsReq(Structure):
    pass
xListHostsReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
]
class xChangeModeReq(Structure):
    pass
xChangeModeReq._fields_ = [
    ('reqType', CARD8),
    ('mode', BYTE),
    ('length', CARD16),
]
xSetAccessControlReq = xChangeModeReq
xSetCloseDownModeReq = xChangeModeReq
xForceScreenSaverReq = xChangeModeReq
class xRotatePropertiesReq(Structure):
    pass
xRotatePropertiesReq._fields_ = [
    ('reqType', CARD8),
    ('pad', BYTE),
    ('length', CARD16),
    ('window', CARD32),
    ('nAtoms', CARD16),
    ('nPositions', INT16),
]
class _xSegment(Structure):
    pass
_xSegment._fields_ = [
    ('x1', INT16),
    ('y1', INT16),
    ('x2', INT16),
    ('y2', INT16),
]
xSegment = _xSegment
class _xPoint(Structure):
    pass
_xPoint._fields_ = [
    ('x', INT16),
    ('y', INT16),
]
xPoint = _xPoint
class _xRectangle(Structure):
    pass
_xRectangle._fields_ = [
    ('x', INT16),
    ('y', INT16),
    ('width', CARD16),
    ('height', CARD16),
]
xRectangle = _xRectangle
class _xArc(Structure):
    pass
_xArc._fields_ = [
    ('x', INT16),
    ('y', INT16),
    ('width', CARD16),
    ('height', CARD16),
    ('angle1', INT16),
    ('angle2', INT16),
]
xArc = _xArc
_XkbStateRec._fields_ = [
    ('group', c_ubyte),
    ('locked_group', c_ubyte),
    ('base_group', c_ushort),
    ('latched_group', c_ushort),
    ('mods', c_ubyte),
    ('base_mods', c_ubyte),
    ('latched_mods', c_ubyte),
    ('locked_mods', c_ubyte),
    ('compat_state', c_ubyte),
    ('grab_mods', c_ubyte),
    ('compat_grab_mods', c_ubyte),
    ('lookup_mods', c_ubyte),
    ('compat_lookup_mods', c_ubyte),
    ('ptr_buttons', c_ushort),
]
XkbStateRec = _XkbStateRec
class _XkbMods(Structure):
    pass
_XkbMods._fields_ = [
    ('mask', c_ubyte),
    ('real_mods', c_ubyte),
    ('vmods', c_ushort),
]
XkbModsPtr = POINTER(_XkbMods)
XkbModsRec = _XkbMods
class _XkbKTMapEntry(Structure):
    pass
_XkbKTMapEntry._fields_ = [
    ('active', c_int),
    ('level', c_ubyte),
    ('mods', XkbModsRec),
]
XkbKTMapEntryPtr = POINTER(_XkbKTMapEntry)
XkbKTMapEntryRec = _XkbKTMapEntry
_XkbKeyType._fields_ = [
    ('mods', XkbModsRec),
    ('num_levels', c_ubyte),
    ('map_count', c_ubyte),
    ('map', XkbKTMapEntryPtr),
    ('preserve', XkbModsPtr),
    ('name', Atom),
    ('level_names', POINTER(Atom)),
]
XkbKeyTypeRec = _XkbKeyType
class _XkbBehavior(Structure):
    pass
_XkbBehavior._fields_ = [
    ('type', c_ubyte),
    ('data', c_ubyte),
]
XkbBehavior = _XkbBehavior
class _XkbAnyAction(Structure):
    pass
_XkbAnyAction._fields_ = [
    ('type', c_ubyte),
    ('data', c_ubyte * 7),
]
XkbAnyAction = _XkbAnyAction
class _XkbModAction(Structure):
    pass
_XkbModAction._fields_ = [
    ('type', c_ubyte),
    ('flags', c_ubyte),
    ('mask', c_ubyte),
    ('real_mods', c_ubyte),
    ('vmods1', c_ubyte),
    ('vmods2', c_ubyte),
]
XkbModAction = _XkbModAction
class _XkbGroupAction(Structure):
    pass
_XkbGroupAction._fields_ = [
    ('type', c_ubyte),
    ('flags', c_ubyte),
    ('group_XXX', c_char),
]
XkbGroupAction = _XkbGroupAction
class _XkbISOAction(Structure):
    pass
_XkbISOAction._fields_ = [
    ('type', c_ubyte),
    ('flags', c_ubyte),
    ('mask', c_ubyte),
    ('real_mods', c_ubyte),
    ('group_XXX', c_char),
    ('affect', c_ubyte),
    ('vmods1', c_ubyte),
    ('vmods2', c_ubyte),
]
XkbISOAction = _XkbISOAction
class _XkbPtrAction(Structure):
    pass
_XkbPtrAction._fields_ = [
    ('type', c_ubyte),
    ('flags', c_ubyte),
    ('high_XXX', c_ubyte),
    ('low_XXX', c_ubyte),
    ('high_YYY', c_ubyte),
    ('low_YYY', c_ubyte),
]
XkbPtrAction = _XkbPtrAction
class _XkbPtrBtnAction(Structure):
    pass
_XkbPtrBtnAction._fields_ = [
    ('type', c_ubyte),
    ('flags', c_ubyte),
    ('count', c_ubyte),
    ('button', c_ubyte),
]
XkbPtrBtnAction = _XkbPtrBtnAction
class _XkbPtrDfltAction(Structure):
    pass
_XkbPtrDfltAction._fields_ = [
    ('type', c_ubyte),
    ('flags', c_ubyte),
    ('affect', c_ubyte),
    ('valueXXX', c_char),
]
XkbPtrDfltAction = _XkbPtrDfltAction
class _XkbSwitchScreenAction(Structure):
    pass
_XkbSwitchScreenAction._fields_ = [
    ('type', c_ubyte),
    ('flags', c_ubyte),
    ('screenXXX', c_char),
]
XkbSwitchScreenAction = _XkbSwitchScreenAction
class _XkbCtrlsAction(Structure):
    pass
_XkbCtrlsAction._fields_ = [
    ('type', c_ubyte),
    ('flags', c_ubyte),
    ('ctrls3', c_ubyte),
    ('ctrls2', c_ubyte),
    ('ctrls1', c_ubyte),
    ('ctrls0', c_ubyte),
]
XkbCtrlsAction = _XkbCtrlsAction
class _XkbMessageAction(Structure):
    pass
_XkbMessageAction._fields_ = [
    ('type', c_ubyte),
    ('flags', c_ubyte),
    ('message', c_ubyte * 6),
]
XkbMessageAction = _XkbMessageAction
class _XkbRedirectKeyAction(Structure):
    pass
_XkbRedirectKeyAction._fields_ = [
    ('type', c_ubyte),
    ('new_key', c_ubyte),
    ('mods_mask', c_ubyte),
    ('mods', c_ubyte),
    ('vmods_mask0', c_ubyte),
    ('vmods_mask1', c_ubyte),
    ('vmods0', c_ubyte),
    ('vmods1', c_ubyte),
]
XkbRedirectKeyAction = _XkbRedirectKeyAction
class _XkbDeviceBtnAction(Structure):
    pass
_XkbDeviceBtnAction._fields_ = [
    ('type', c_ubyte),
    ('flags', c_ubyte),
    ('count', c_ubyte),
    ('button', c_ubyte),
    ('device', c_ubyte),
]
XkbDeviceBtnAction = _XkbDeviceBtnAction
class _XkbDeviceValuatorAction(Structure):
    pass
_XkbDeviceValuatorAction._fields_ = [
    ('type', c_ubyte),
    ('device', c_ubyte),
    ('v1_what', c_ubyte),
    ('v1_ndx', c_ubyte),
    ('v1_value', c_ubyte),
    ('v2_what', c_ubyte),
    ('v2_ndx', c_ubyte),
    ('v2_value', c_ubyte),
]
XkbDeviceValuatorAction = _XkbDeviceValuatorAction
class _XkbControls(Structure):
    pass
_XkbControls._fields_ = [
    ('mk_dflt_btn', c_ubyte),
    ('num_groups', c_ubyte),
    ('groups_wrap', c_ubyte),
    ('internal', XkbModsRec),
    ('ignore_lock', XkbModsRec),
    ('enabled_ctrls', c_uint),
    ('repeat_delay', c_ushort),
    ('repeat_interval', c_ushort),
    ('slow_keys_delay', c_ushort),
    ('debounce_delay', c_ushort),
    ('mk_delay', c_ushort),
    ('mk_interval', c_ushort),
    ('mk_time_to_max', c_ushort),
    ('mk_max_speed', c_ushort),
    ('mk_curve', c_short),
    ('ax_options', c_ushort),
    ('ax_timeout', c_ushort),
    ('axt_opts_mask', c_ushort),
    ('axt_opts_values', c_ushort),
    ('axt_ctrls_mask', c_uint),
    ('axt_ctrls_values', c_uint),
    ('per_key_repeat', c_ubyte * 32),
]
XkbControlsRec = _XkbControls
XkbControlsPtr = POINTER(_XkbControls)
class _XkbServerMapRec(Structure):
    pass
_XkbServerMapRec._fields_ = [
    ('num_acts', c_ushort),
    ('size_acts', c_ushort),
    ('acts', POINTER(XkbAction)),
    ('behaviors', POINTER(XkbBehavior)),
    ('key_acts', POINTER(c_ushort)),
    ('c_explicit', POINTER(c_ubyte)),
    ('vmods', c_ubyte * 16),
    ('vmodmap', POINTER(c_ushort)),
]
XkbServerMapRec = _XkbServerMapRec
XkbServerMapPtr = POINTER(_XkbServerMapRec)
class _XkbSymMapRec(Structure):
    pass
_XkbSymMapRec._fields_ = [
    ('kt_index', c_ubyte * 4),
    ('group_info', c_ubyte),
    ('width', c_ubyte),
    ('offset', c_ushort),
]
XkbSymMapRec = _XkbSymMapRec
XkbSymMapPtr = POINTER(_XkbSymMapRec)
class _XkbClientMapRec(Structure):
    pass
_XkbClientMapRec._fields_ = [
    ('size_types', c_ubyte),
    ('num_types', c_ubyte),
    ('types', XkbKeyTypePtr),
    ('size_syms', c_ushort),
    ('num_syms', c_ushort),
    ('syms', POINTER(KeySym)),
    ('key_sym_map', XkbSymMapPtr),
    ('modmap', POINTER(c_ubyte)),
]
XkbClientMapPtr = POINTER(_XkbClientMapRec)
XkbClientMapRec = _XkbClientMapRec
class _XkbSymInterpretRec(Structure):
    pass
_XkbSymInterpretRec._fields_ = [
    ('sym', KeySym),
    ('flags', c_ubyte),
    ('match', c_ubyte),
    ('mods', c_ubyte),
    ('virtual_mod', c_ubyte),
    ('act', XkbAnyAction),
]
XkbSymInterpretRec = _XkbSymInterpretRec
XkbSymInterpretPtr = POINTER(_XkbSymInterpretRec)
class _XkbCompatMapRec(Structure):
    pass
_XkbCompatMapRec._fields_ = [
    ('sym_interpret', XkbSymInterpretPtr),
    ('groups', XkbModsRec * 4),
    ('num_si', c_ushort),
    ('size_si', c_ushort),
]
XkbCompatMapPtr = POINTER(_XkbCompatMapRec)
XkbCompatMapRec = _XkbCompatMapRec
_XkbIndicatorMapRec._fields_ = [
    ('flags', c_ubyte),
    ('which_groups', c_ubyte),
    ('groups', c_ubyte),
    ('which_mods', c_ubyte),
    ('mods', XkbModsRec),
    ('ctrls', c_uint),
]
XkbIndicatorMapRec = _XkbIndicatorMapRec
class _XkbIndicatorRec(Structure):
    pass
_XkbIndicatorRec._fields_ = [
    ('phys_indicators', c_ulong),
    ('maps', XkbIndicatorMapRec * 32),
]
XkbIndicatorRec = _XkbIndicatorRec
XkbIndicatorPtr = POINTER(_XkbIndicatorRec)
class _XkbKeyNameRec(Structure):
    pass
_XkbKeyNameRec._fields_ = [
    ('name', c_char * 4),
]
XkbKeyNameRec = _XkbKeyNameRec
XkbKeyNamePtr = POINTER(_XkbKeyNameRec)
class _XkbKeyAliasRec(Structure):
    pass
_XkbKeyAliasRec._fields_ = [
    ('real', c_char * 4),
    ('alias', c_char * 4),
]
XkbKeyAliasPtr = POINTER(_XkbKeyAliasRec)
XkbKeyAliasRec = _XkbKeyAliasRec
class _XkbNamesRec(Structure):
    pass
_XkbNamesRec._fields_ = [
    ('keycodes', Atom),
    ('geometry', Atom),
    ('symbols', Atom),
    ('types', Atom),
    ('compat', Atom),
    ('vmods', Atom * 16),
    ('indicators', Atom * 32),
    ('groups', Atom * 4),
    ('keys', XkbKeyNamePtr),
    ('key_aliases', XkbKeyAliasPtr),
    ('radio_groups', POINTER(Atom)),
    ('phys_symbols', Atom),
    ('num_keys', c_ubyte),
    ('num_key_aliases', c_ubyte),
    ('num_rg', c_ushort),
]
XkbNamesPtr = POINTER(_XkbNamesRec)
XkbNamesRec = _XkbNamesRec
class _XkbGeometry(Structure):
    pass
XkbGeometryPtr = POINTER(_XkbGeometry)
_XkbGeometry._fields_ = [
]
_XkbDesc._fields_ = [
    ('dpy', POINTER(_XDisplay)),
    ('flags', c_ushort),
    ('device_spec', c_ushort),
    ('min_key_code', KeyCode),
    ('max_key_code', KeyCode),
    ('ctrls', XkbControlsPtr),
    ('server', XkbServerMapPtr),
    ('map', XkbClientMapPtr),
    ('indicators', XkbIndicatorPtr),
    ('names', XkbNamesPtr),
    ('compat', XkbCompatMapPtr),
    ('geom', XkbGeometryPtr),
]
XkbDescRec = _XkbDesc
_XkbMapChanges._fields_ = [
    ('changed', c_ushort),
    ('min_key_code', KeyCode),
    ('max_key_code', KeyCode),
    ('first_type', c_ubyte),
    ('num_types', c_ubyte),
    ('first_key_sym', KeyCode),
    ('num_key_syms', c_ubyte),
    ('first_key_act', KeyCode),
    ('num_key_acts', c_ubyte),
    ('first_key_behavior', KeyCode),
    ('num_key_behaviors', c_ubyte),
    ('first_key_explicit', KeyCode),
    ('num_key_explicit', c_ubyte),
    ('first_modmap_key', KeyCode),
    ('num_modmap_keys', c_ubyte),
    ('first_vmodmap_key', KeyCode),
    ('num_vmodmap_keys', c_ubyte),
    ('pad', c_ubyte),
    ('vmods', c_ushort),
]
XkbMapChangesRec = _XkbMapChanges
_XkbControlsChanges._fields_ = [
    ('changed_ctrls', c_uint),
    ('enabled_ctrls_changes', c_uint),
    ('num_groups_changed', c_int),
]
XkbControlsChangesRec = _XkbControlsChanges
class _XkbIndicatorChanges(Structure):
    pass
_XkbIndicatorChanges._fields_ = [
    ('state_changes', c_uint),
    ('map_changes', c_uint),
]
XkbIndicatorChangesPtr = POINTER(_XkbIndicatorChanges)
XkbIndicatorChangesRec = _XkbIndicatorChanges
_XkbNameChanges._fields_ = [
    ('changed', c_uint),
    ('first_type', c_ubyte),
    ('num_types', c_ubyte),
    ('first_lvl', c_ubyte),
    ('num_lvls', c_ubyte),
    ('num_aliases', c_ubyte),
    ('num_rg', c_ubyte),
    ('first_key', c_ubyte),
    ('num_keys', c_ubyte),
    ('changed_vmods', c_ushort),
    ('changed_indicators', c_ulong),
    ('changed_groups', c_ubyte),
]
XkbNameChangesRec = _XkbNameChanges
class _XkbCompatChanges(Structure):
    pass
_XkbCompatChanges._fields_ = [
    ('changed_groups', c_ubyte),
    ('first_si', c_ushort),
    ('num_si', c_ushort),
]
XkbCompatChangesPtr = POINTER(_XkbCompatChanges)
XkbCompatChangesRec = _XkbCompatChanges
_XkbChanges._fields_ = [
    ('device_spec', c_ushort),
    ('state_changes', c_ushort),
    ('map', XkbMapChangesRec),
    ('ctrls', XkbControlsChangesRec),
    ('indicators', XkbIndicatorChangesRec),
    ('names', XkbNameChangesRec),
    ('compat', XkbCompatChangesRec),
]
XkbChangesRec = _XkbChanges
_XkbComponentNames._fields_ = [
    ('keymap', STRING),
    ('keycodes', STRING),
    ('types', STRING),
    ('compat', STRING),
    ('symbols', STRING),
    ('geometry', STRING),
]
XkbComponentNamesRec = _XkbComponentNames
class _XkbComponentName(Structure):
    pass
_XkbComponentName._fields_ = [
    ('flags', c_ushort),
    ('name', STRING),
]
XkbComponentNamePtr = POINTER(_XkbComponentName)
XkbComponentNameRec = _XkbComponentName
_XkbComponentList._fields_ = [
    ('num_keymaps', c_int),
    ('num_keycodes', c_int),
    ('num_types', c_int),
    ('num_compat', c_int),
    ('num_symbols', c_int),
    ('num_geometry', c_int),
    ('keymaps', XkbComponentNamePtr),
    ('keycodes', XkbComponentNamePtr),
    ('types', XkbComponentNamePtr),
    ('compat', XkbComponentNamePtr),
    ('symbols', XkbComponentNamePtr),
    ('geometry', XkbComponentNamePtr),
]
XkbComponentListRec = _XkbComponentList
_XkbDeviceLedInfo._fields_ = [
    ('led_class', c_ushort),
    ('led_id', c_ushort),
    ('phys_indicators', c_uint),
    ('maps_present', c_uint),
    ('names_present', c_uint),
    ('state', c_uint),
    ('names', Atom * 32),
    ('maps', XkbIndicatorMapRec * 32),
]
XkbDeviceLedInfoRec = _XkbDeviceLedInfo
_XkbDeviceInfo._fields_ = [
    ('name', STRING),
    ('type', Atom),
    ('device_spec', c_ushort),
    ('has_own_state', c_int),
    ('supported', c_ushort),
    ('unsupported', c_ushort),
    ('num_btns', c_ushort),
    ('btn_acts', POINTER(XkbAction)),
    ('sz_leds', c_ushort),
    ('num_leds', c_ushort),
    ('dflt_kbd_fb', c_ushort),
    ('dflt_led_fb', c_ushort),
    ('leds', XkbDeviceLedInfoPtr),
]
XkbDeviceInfoRec = _XkbDeviceInfo
class _XkbDeviceLedChanges(Structure):
    pass
_XkbDeviceLedChanges._fields_ = [
    ('led_class', c_ushort),
    ('led_id', c_ushort),
    ('defined', c_uint),
    ('next', POINTER(_XkbDeviceLedChanges)),
]
XkbDeviceLedChangesRec = _XkbDeviceLedChanges
XkbDeviceLedChangesPtr = POINTER(_XkbDeviceLedChanges)
_XkbDeviceChanges._fields_ = [
    ('changed', c_uint),
    ('first_btn', c_ushort),
    ('num_btns', c_ushort),
    ('leds', XkbDeviceLedChangesRec),
]
XkbDeviceChangesRec = _XkbDeviceChanges
program_invocation_short_name = (STRING).in_dll(_libraries['libX11.so.6'], 'program_invocation_short_name')
program_invocation_name = (STRING).in_dll(_libraries['libX11.so.6'], 'program_invocation_name')
error_t = c_int
class div_t(Structure):
    pass
div_t._fields_ = [
    ('quot', c_int),
    ('rem', c_int),
]
class ldiv_t(Structure):
    pass
ldiv_t._fields_ = [
    ('quot', c_long),
    ('rem', c_long),
]
class lldiv_t(Structure):
    pass
lldiv_t._fields_ = [
    ('quot', c_longlong),
    ('rem', c_longlong),
]
__ctype_get_mb_cur_max = _libraries['libX11.so.6'].__ctype_get_mb_cur_max
__ctype_get_mb_cur_max.restype = size_t
__ctype_get_mb_cur_max.argtypes = []
strtod = _libraries['libX11.so.6'].strtod
strtod.restype = c_double
strtod.argtypes = [STRING, POINTER(STRING)]
strtof = _libraries['libX11.so.6'].strtof
strtof.restype = c_float
strtof.argtypes = [STRING, POINTER(STRING)]
strtold = _libraries['libX11.so.6'].strtold
strtold.restype = c_longdouble
strtold.argtypes = [STRING, POINTER(STRING)]
strtol = _libraries['libX11.so.6'].strtol
strtol.restype = c_long
strtol.argtypes = [STRING, POINTER(STRING), c_int]
strtoul = _libraries['libX11.so.6'].strtoul
strtoul.restype = c_ulong
strtoul.argtypes = [STRING, POINTER(STRING), c_int]
strtoq = _libraries['libX11.so.6'].strtoq
strtoq.restype = c_longlong
strtoq.argtypes = [STRING, POINTER(STRING), c_int]
strtouq = _libraries['libX11.so.6'].strtouq
strtouq.restype = c_ulonglong
strtouq.argtypes = [STRING, POINTER(STRING), c_int]
strtoll = _libraries['libX11.so.6'].strtoll
strtoll.restype = c_longlong
strtoll.argtypes = [STRING, POINTER(STRING), c_int]
strtoull = _libraries['libX11.so.6'].strtoull
strtoull.restype = c_ulonglong
strtoull.argtypes = [STRING, POINTER(STRING), c_int]
class __locale_struct(Structure):
    pass
__locale_t = POINTER(__locale_struct)
strtol_l = _libraries['libX11.so.6'].strtol_l
strtol_l.restype = c_long
strtol_l.argtypes = [STRING, POINTER(STRING), c_int, __locale_t]
strtoul_l = _libraries['libX11.so.6'].strtoul_l
strtoul_l.restype = c_ulong
strtoul_l.argtypes = [STRING, POINTER(STRING), c_int, __locale_t]
strtoll_l = _libraries['libX11.so.6'].strtoll_l
strtoll_l.restype = c_longlong
strtoll_l.argtypes = [STRING, POINTER(STRING), c_int, __locale_t]
strtoull_l = _libraries['libX11.so.6'].strtoull_l
strtoull_l.restype = c_ulonglong
strtoull_l.argtypes = [STRING, POINTER(STRING), c_int, __locale_t]
strtod_l = _libraries['libX11.so.6'].strtod_l
strtod_l.restype = c_double
strtod_l.argtypes = [STRING, POINTER(STRING), __locale_t]
strtof_l = _libraries['libX11.so.6'].strtof_l
strtof_l.restype = c_float
strtof_l.argtypes = [STRING, POINTER(STRING), __locale_t]
strtold_l = _libraries['libX11.so.6'].strtold_l
strtold_l.restype = c_longdouble
strtold_l.argtypes = [STRING, POINTER(STRING), __locale_t]
atoi = _libraries['libX11.so.6'].atoi
atoi.restype = c_int
atoi.argtypes = [STRING]
atol = _libraries['libX11.so.6'].atol
atol.restype = c_long
atol.argtypes = [STRING]
atoll = _libraries['libX11.so.6'].atoll
atoll.restype = c_longlong
atoll.argtypes = [STRING]
l64a = _libraries['libX11.so.6'].l64a
l64a.restype = STRING
l64a.argtypes = [c_long]
a64l = _libraries['libX11.so.6'].a64l
a64l.restype = c_long
a64l.argtypes = [STRING]
random = _libraries['libX11.so.6'].random
random.restype = c_long
random.argtypes = []
srandom = _libraries['libX11.so.6'].srandom
srandom.restype = None
srandom.argtypes = [c_uint]
initstate = _libraries['libX11.so.6'].initstate
initstate.restype = STRING
initstate.argtypes = [c_uint, STRING, size_t]
setstate = _libraries['libX11.so.6'].setstate
setstate.restype = STRING
setstate.argtypes = [STRING]
class random_data(Structure):
    pass
int32_t = c_int32
random_data._fields_ = [
    ('fptr', POINTER(int32_t)),
    ('rptr', POINTER(int32_t)),
    ('state', POINTER(int32_t)),
    ('rand_type', c_int),
    ('rand_deg', c_int),
    ('rand_sep', c_int),
    ('end_ptr', POINTER(int32_t)),
]
random_r = _libraries['libX11.so.6'].random_r
random_r.restype = c_int
random_r.argtypes = [POINTER(random_data), POINTER(int32_t)]
srandom_r = _libraries['libX11.so.6'].srandom_r
srandom_r.restype = c_int
srandom_r.argtypes = [c_uint, POINTER(random_data)]
initstate_r = _libraries['libX11.so.6'].initstate_r
initstate_r.restype = c_int
initstate_r.argtypes = [c_uint, STRING, size_t, POINTER(random_data)]
setstate_r = _libraries['libX11.so.6'].setstate_r
setstate_r.restype = c_int
setstate_r.argtypes = [STRING, POINTER(random_data)]
rand = _libraries['libX11.so.6'].rand
rand.restype = c_int
rand.argtypes = []
srand = _libraries['libX11.so.6'].srand
srand.restype = None
srand.argtypes = [c_uint]
rand_r = _libraries['libX11.so.6'].rand_r
rand_r.restype = c_int
rand_r.argtypes = [POINTER(c_uint)]
drand48 = _libraries['libX11.so.6'].drand48
drand48.restype = c_double
drand48.argtypes = []
erand48 = _libraries['libX11.so.6'].erand48
erand48.restype = c_double
erand48.argtypes = [POINTER(c_ushort)]
lrand48 = _libraries['libX11.so.6'].lrand48
lrand48.restype = c_long
lrand48.argtypes = []
nrand48 = _libraries['libX11.so.6'].nrand48
nrand48.restype = c_long
nrand48.argtypes = [POINTER(c_ushort)]
mrand48 = _libraries['libX11.so.6'].mrand48
mrand48.restype = c_long
mrand48.argtypes = []
jrand48 = _libraries['libX11.so.6'].jrand48
jrand48.restype = c_long
jrand48.argtypes = [POINTER(c_ushort)]
srand48 = _libraries['libX11.so.6'].srand48
srand48.restype = None
srand48.argtypes = [c_long]
seed48 = _libraries['libX11.so.6'].seed48
seed48.restype = POINTER(c_ushort)
seed48.argtypes = [POINTER(c_ushort)]
lcong48 = _libraries['libX11.so.6'].lcong48
lcong48.restype = None
lcong48.argtypes = [POINTER(c_ushort)]
class drand48_data(Structure):
    pass
drand48_data._fields_ = [
    ('__x', c_ushort * 3),
    ('__old_x', c_ushort * 3),
    ('__c', c_ushort),
    ('__init', c_ushort),
    ('__a', c_ulonglong),
]
drand48_r = _libraries['libX11.so.6'].drand48_r
drand48_r.restype = c_int
drand48_r.argtypes = [POINTER(drand48_data), POINTER(c_double)]
erand48_r = _libraries['libX11.so.6'].erand48_r
erand48_r.restype = c_int
erand48_r.argtypes = [POINTER(c_ushort), POINTER(drand48_data), POINTER(c_double)]
lrand48_r = _libraries['libX11.so.6'].lrand48_r
lrand48_r.restype = c_int
lrand48_r.argtypes = [POINTER(drand48_data), POINTER(c_long)]
nrand48_r = _libraries['libX11.so.6'].nrand48_r
nrand48_r.restype = c_int
nrand48_r.argtypes = [POINTER(c_ushort), POINTER(drand48_data), POINTER(c_long)]
mrand48_r = _libraries['libX11.so.6'].mrand48_r
mrand48_r.restype = c_int
mrand48_r.argtypes = [POINTER(drand48_data), POINTER(c_long)]
jrand48_r = _libraries['libX11.so.6'].jrand48_r
jrand48_r.restype = c_int
jrand48_r.argtypes = [POINTER(c_ushort), POINTER(drand48_data), POINTER(c_long)]
srand48_r = _libraries['libX11.so.6'].srand48_r
srand48_r.restype = c_int
srand48_r.argtypes = [c_long, POINTER(drand48_data)]
seed48_r = _libraries['libX11.so.6'].seed48_r
seed48_r.restype = c_int
seed48_r.argtypes = [POINTER(c_ushort), POINTER(drand48_data)]
lcong48_r = _libraries['libX11.so.6'].lcong48_r
lcong48_r.restype = c_int
lcong48_r.argtypes = [POINTER(c_ushort), POINTER(drand48_data)]
malloc = _libraries['libX11.so.6'].malloc
malloc.restype = c_void_p
malloc.argtypes = [size_t]
calloc = _libraries['libX11.so.6'].calloc
calloc.restype = c_void_p
calloc.argtypes = [size_t, size_t]
realloc = _libraries['libX11.so.6'].realloc
realloc.restype = c_void_p
realloc.argtypes = [c_void_p, size_t]
free = _libraries['libX11.so.6'].free
free.restype = None
free.argtypes = [c_void_p]
cfree = _libraries['libX11.so.6'].cfree
cfree.restype = None
cfree.argtypes = [c_void_p]
valloc = _libraries['libX11.so.6'].valloc
valloc.restype = c_void_p
valloc.argtypes = [size_t]
posix_memalign = _libraries['libX11.so.6'].posix_memalign
posix_memalign.restype = c_int
posix_memalign.argtypes = [POINTER(c_void_p), size_t, size_t]
aligned_alloc = _libraries['libX11.so.6'].aligned_alloc
aligned_alloc.restype = c_void_p
aligned_alloc.argtypes = [size_t, size_t]
abort = _libraries['libX11.so.6'].abort
abort.restype = None
abort.argtypes = []
on_exit = _libraries['libX11.so.6'].on_exit
on_exit.restype = c_int
on_exit.argtypes = [CFUNCTYPE(None, c_int, c_void_p), c_void_p]
exit = _libraries['libX11.so.6'].exit
exit.restype = None
exit.argtypes = [c_int]
quick_exit = _libraries['libX11.so.6'].quick_exit
quick_exit.restype = None
quick_exit.argtypes = [c_int]
_Exit = _libraries['libX11.so.6']._Exit
_Exit.restype = None
_Exit.argtypes = [c_int]
getenv = _libraries['libX11.so.6'].getenv
getenv.restype = STRING
getenv.argtypes = [STRING]
secure_getenv = _libraries['libX11.so.6'].secure_getenv
secure_getenv.restype = STRING
secure_getenv.argtypes = [STRING]
putenv = _libraries['libX11.so.6'].putenv
putenv.restype = c_int
putenv.argtypes = [STRING]
setenv = _libraries['libX11.so.6'].setenv
setenv.restype = c_int
setenv.argtypes = [STRING, STRING, c_int]
unsetenv = _libraries['libX11.so.6'].unsetenv
unsetenv.restype = c_int
unsetenv.argtypes = [STRING]
clearenv = _libraries['libX11.so.6'].clearenv
clearenv.restype = c_int
clearenv.argtypes = []
mktemp = _libraries['libX11.so.6'].mktemp
mktemp.restype = STRING
mktemp.argtypes = [STRING]
mkstemp = _libraries['libX11.so.6'].mkstemp
mkstemp.restype = c_int
mkstemp.argtypes = [STRING]
mkstemp64 = _libraries['libX11.so.6'].mkstemp64
mkstemp64.restype = c_int
mkstemp64.argtypes = [STRING]
mkstemps = _libraries['libX11.so.6'].mkstemps
mkstemps.restype = c_int
mkstemps.argtypes = [STRING, c_int]
mkstemps64 = _libraries['libX11.so.6'].mkstemps64
mkstemps64.restype = c_int
mkstemps64.argtypes = [STRING, c_int]
mkdtemp = _libraries['libX11.so.6'].mkdtemp
mkdtemp.restype = STRING
mkdtemp.argtypes = [STRING]
mkostemp = _libraries['libX11.so.6'].mkostemp
mkostemp.restype = c_int
mkostemp.argtypes = [STRING, c_int]
mkostemp64 = _libraries['libX11.so.6'].mkostemp64
mkostemp64.restype = c_int
mkostemp64.argtypes = [STRING, c_int]
mkostemps = _libraries['libX11.so.6'].mkostemps
mkostemps.restype = c_int
mkostemps.argtypes = [STRING, c_int, c_int]
mkostemps64 = _libraries['libX11.so.6'].mkostemps64
mkostemps64.restype = c_int
mkostemps64.argtypes = [STRING, c_int, c_int]
system = _libraries['libX11.so.6'].system
system.restype = c_int
system.argtypes = [STRING]
canonicalize_file_name = _libraries['libX11.so.6'].canonicalize_file_name
canonicalize_file_name.restype = STRING
canonicalize_file_name.argtypes = [STRING]
__compar_fn_t = CFUNCTYPE(c_int, c_void_p, c_void_p)
comparison_fn_t = __compar_fn_t
__compar_d_fn_t = CFUNCTYPE(c_int, c_void_p, c_void_p, c_void_p)
qsort = _libraries['libX11.so.6'].qsort
qsort.restype = None
qsort.argtypes = [c_void_p, size_t, size_t, __compar_fn_t]
qsort_r = _libraries['libX11.so.6'].qsort_r
qsort_r.restype = None
qsort_r.argtypes = [c_void_p, size_t, size_t, __compar_d_fn_t, c_void_p]
abs = _libraries['libX11.so.6'].abs
abs.restype = c_int
abs.argtypes = [c_int]
labs = _libraries['libX11.so.6'].labs
labs.restype = c_long
labs.argtypes = [c_long]
llabs = _libraries['libX11.so.6'].llabs
llabs.restype = c_longlong
llabs.argtypes = [c_longlong]
div = _libraries['libX11.so.6'].div
div.restype = div_t
div.argtypes = [c_int, c_int]
ldiv = _libraries['libX11.so.6'].ldiv
ldiv.restype = ldiv_t
ldiv.argtypes = [c_long, c_long]
lldiv = _libraries['libX11.so.6'].lldiv
lldiv.restype = lldiv_t
lldiv.argtypes = [c_longlong, c_longlong]
ecvt = _libraries['libX11.so.6'].ecvt
ecvt.restype = STRING
ecvt.argtypes = [c_double, c_int, POINTER(c_int), POINTER(c_int)]
fcvt = _libraries['libX11.so.6'].fcvt
fcvt.restype = STRING
fcvt.argtypes = [c_double, c_int, POINTER(c_int), POINTER(c_int)]
gcvt = _libraries['libX11.so.6'].gcvt
gcvt.restype = STRING
gcvt.argtypes = [c_double, c_int, STRING]
qecvt = _libraries['libX11.so.6'].qecvt
qecvt.restype = STRING
qecvt.argtypes = [c_longdouble, c_int, POINTER(c_int), POINTER(c_int)]
qfcvt = _libraries['libX11.so.6'].qfcvt
qfcvt.restype = STRING
qfcvt.argtypes = [c_longdouble, c_int, POINTER(c_int), POINTER(c_int)]
qgcvt = _libraries['libX11.so.6'].qgcvt
qgcvt.restype = STRING
qgcvt.argtypes = [c_longdouble, c_int, STRING]
ecvt_r = _libraries['libX11.so.6'].ecvt_r
ecvt_r.restype = c_int
ecvt_r.argtypes = [c_double, c_int, POINTER(c_int), POINTER(c_int), STRING, size_t]
fcvt_r = _libraries['libX11.so.6'].fcvt_r
fcvt_r.restype = c_int
fcvt_r.argtypes = [c_double, c_int, POINTER(c_int), POINTER(c_int), STRING, size_t]
qecvt_r = _libraries['libX11.so.6'].qecvt_r
qecvt_r.restype = c_int
qecvt_r.argtypes = [c_longdouble, c_int, POINTER(c_int), POINTER(c_int), STRING, size_t]
qfcvt_r = _libraries['libX11.so.6'].qfcvt_r
qfcvt_r.restype = c_int
qfcvt_r.argtypes = [c_longdouble, c_int, POINTER(c_int), POINTER(c_int), STRING, size_t]
mblen = _libraries['libX11.so.6'].mblen
mblen.restype = c_int
mblen.argtypes = [STRING, size_t]
mbtowc = _libraries['libX11.so.6'].mbtowc
mbtowc.restype = c_int
mbtowc.argtypes = [WSTRING, STRING, size_t]
rpmatch = _libraries['libX11.so.6'].rpmatch
rpmatch.restype = c_int
rpmatch.argtypes = [STRING]
getsubopt = _libraries['libX11.so.6'].getsubopt
getsubopt.restype = c_int
getsubopt.argtypes = [POINTER(STRING), POINTER(STRING), POINTER(STRING)]
posix_openpt = _libraries['libX11.so.6'].posix_openpt
posix_openpt.restype = c_int
posix_openpt.argtypes = [c_int]
grantpt = _libraries['libX11.so.6'].grantpt
grantpt.restype = c_int
grantpt.argtypes = [c_int]
unlockpt = _libraries['libX11.so.6'].unlockpt
unlockpt.restype = c_int
unlockpt.argtypes = [c_int]
ptsname = _libraries['libX11.so.6'].ptsname
ptsname.restype = STRING
ptsname.argtypes = [c_int]
getpt = _libraries['libX11.so.6'].getpt
getpt.restype = c_int
getpt.argtypes = []
getloadavg = _libraries['libX11.so.6'].getloadavg
getloadavg.restype = c_int
getloadavg.argtypes = [POINTER(c_double), c_int]
memccpy = _libraries['libX11.so.6'].memccpy
memccpy.restype = c_void_p
memccpy.argtypes = [c_void_p, c_void_p, c_int, size_t]
memcmp = _libraries['libX11.so.6'].memcmp
memcmp.restype = c_int
memcmp.argtypes = [c_void_p, c_void_p, size_t]
memchr = _libraries['libX11.so.6'].memchr
memchr.restype = c_void_p
memchr.argtypes = [c_void_p, c_int, size_t]
memchr = _libraries['libX11.so.6'].memchr
memchr.restype = c_void_p
memchr.argtypes = [c_void_p, c_int, size_t]
rawmemchr = _libraries['libX11.so.6'].rawmemchr
rawmemchr.restype = c_void_p
rawmemchr.argtypes = [c_void_p, c_int]
rawmemchr = _libraries['libX11.so.6'].rawmemchr
rawmemchr.restype = c_void_p
rawmemchr.argtypes = [c_void_p, c_int]
memrchr = _libraries['libX11.so.6'].memrchr
memrchr.restype = c_void_p
memrchr.argtypes = [c_void_p, c_int, size_t]
memrchr = _libraries['libX11.so.6'].memrchr
memrchr.restype = c_void_p
memrchr.argtypes = [c_void_p, c_int, size_t]
strcmp = _libraries['libX11.so.6'].strcmp
strcmp.restype = c_int
strcmp.argtypes = [STRING, STRING]
strncmp = _libraries['libX11.so.6'].strncmp
strncmp.restype = c_int
strncmp.argtypes = [STRING, STRING, size_t]
strcoll = _libraries['libX11.so.6'].strcoll
strcoll.restype = c_int
strcoll.argtypes = [STRING, STRING]
strxfrm = _libraries['libX11.so.6'].strxfrm
strxfrm.restype = size_t
strxfrm.argtypes = [STRING, STRING, size_t]
strcoll_l = _libraries['libX11.so.6'].strcoll_l
strcoll_l.restype = c_int
strcoll_l.argtypes = [STRING, STRING, __locale_t]
strxfrm_l = _libraries['libX11.so.6'].strxfrm_l
strxfrm_l.restype = size_t
strxfrm_l.argtypes = [STRING, STRING, size_t, __locale_t]
strdup = _libraries['libX11.so.6'].strdup
strdup.restype = STRING
strdup.argtypes = [STRING]
strndup = _libraries['libX11.so.6'].strndup
strndup.restype = STRING
strndup.argtypes = [STRING, size_t]
strchr = _libraries['libX11.so.6'].strchr
strchr.restype = STRING
strchr.argtypes = [STRING, c_int]
strchr = _libraries['libX11.so.6'].strchr
strchr.restype = STRING
strchr.argtypes = [STRING, c_int]
strrchr = _libraries['libX11.so.6'].strrchr
strrchr.restype = STRING
strrchr.argtypes = [STRING, c_int]
strrchr = _libraries['libX11.so.6'].strrchr
strrchr.restype = STRING
strrchr.argtypes = [STRING, c_int]
strchrnul = _libraries['libX11.so.6'].strchrnul
strchrnul.restype = STRING
strchrnul.argtypes = [STRING, c_int]
strchrnul = _libraries['libX11.so.6'].strchrnul
strchrnul.restype = STRING
strchrnul.argtypes = [STRING, c_int]
strcspn = _libraries['libX11.so.6'].strcspn
strcspn.restype = size_t
strcspn.argtypes = [STRING, STRING]
strspn = _libraries['libX11.so.6'].strspn
strspn.restype = size_t
strspn.argtypes = [STRING, STRING]
strpbrk = _libraries['libX11.so.6'].strpbrk
strpbrk.restype = STRING
strpbrk.argtypes = [STRING, STRING]
strpbrk = _libraries['libX11.so.6'].strpbrk
strpbrk.restype = STRING
strpbrk.argtypes = [STRING, STRING]
strstr = _libraries['libX11.so.6'].strstr
strstr.restype = STRING
strstr.argtypes = [STRING, STRING]
strstr = _libraries['libX11.so.6'].strstr
strstr.restype = STRING
strstr.argtypes = [STRING, STRING]
strtok = _libraries['libX11.so.6'].strtok
strtok.restype = STRING
strtok.argtypes = [STRING, STRING]
__strtok_r = _libraries['libX11.so.6'].__strtok_r
__strtok_r.restype = STRING
__strtok_r.argtypes = [STRING, STRING, POINTER(STRING)]
strtok_r = _libraries['libX11.so.6'].strtok_r
strtok_r.restype = STRING
strtok_r.argtypes = [STRING, STRING, POINTER(STRING)]
strcasestr = _libraries['libX11.so.6'].strcasestr
strcasestr.restype = STRING
strcasestr.argtypes = [STRING, STRING]
strcasestr = _libraries['libX11.so.6'].strcasestr
strcasestr.restype = STRING
strcasestr.argtypes = [STRING, STRING]
memmem = _libraries['libX11.so.6'].memmem
memmem.restype = c_void_p
memmem.argtypes = [c_void_p, size_t, c_void_p, size_t]
__mempcpy = _libraries['libX11.so.6'].__mempcpy
__mempcpy.restype = c_void_p
__mempcpy.argtypes = [c_void_p, c_void_p, size_t]
strlen = _libraries['libX11.so.6'].strlen
strlen.restype = size_t
strlen.argtypes = [STRING]
strnlen = _libraries['libX11.so.6'].strnlen
strnlen.restype = size_t
strnlen.argtypes = [STRING, size_t]
strerror = _libraries['libX11.so.6'].strerror
strerror.restype = STRING
strerror.argtypes = [c_int]
strerror_r = _libraries['libX11.so.6'].strerror_r
strerror_r.restype = STRING
strerror_r.argtypes = [c_int, STRING, size_t]
strerror_l = _libraries['libX11.so.6'].strerror_l
strerror_l.restype = STRING
strerror_l.argtypes = [c_int, __locale_t]
__bzero = _libraries['libX11.so.6'].__bzero
__bzero.restype = None
__bzero.argtypes = [c_void_p, size_t]
bcmp = _libraries['libX11.so.6'].bcmp
bcmp.restype = c_int
bcmp.argtypes = [c_void_p, c_void_p, size_t]
index = _libraries['libX11.so.6'].index
index.restype = STRING
index.argtypes = [STRING, c_int]
index = _libraries['libX11.so.6'].index
index.restype = STRING
index.argtypes = [STRING, c_int]
rindex = _libraries['libX11.so.6'].rindex
rindex.restype = STRING
rindex.argtypes = [STRING, c_int]
rindex = _libraries['libX11.so.6'].rindex
rindex.restype = STRING
rindex.argtypes = [STRING, c_int]
ffs = _libraries['libX11.so.6'].ffs
ffs.restype = c_int
ffs.argtypes = [c_int]
ffsl = _libraries['libX11.so.6'].ffsl
ffsl.restype = c_int
ffsl.argtypes = [c_long]
ffsll = _libraries['libX11.so.6'].ffsll
ffsll.restype = c_int
ffsll.argtypes = [c_longlong]
strcasecmp = _libraries['libX11.so.6'].strcasecmp
strcasecmp.restype = c_int
strcasecmp.argtypes = [STRING, STRING]
strncasecmp = _libraries['libX11.so.6'].strncasecmp
strncasecmp.restype = c_int
strncasecmp.argtypes = [STRING, STRING, size_t]
strcasecmp_l = _libraries['libX11.so.6'].strcasecmp_l
strcasecmp_l.restype = c_int
strcasecmp_l.argtypes = [STRING, STRING, __locale_t]
strncasecmp_l = _libraries['libX11.so.6'].strncasecmp_l
strncasecmp_l.restype = c_int
strncasecmp_l.argtypes = [STRING, STRING, size_t, __locale_t]
strsep = _libraries['libX11.so.6'].strsep
strsep.restype = STRING
strsep.argtypes = [POINTER(STRING), STRING]
strsignal = _libraries['libX11.so.6'].strsignal
strsignal.restype = STRING
strsignal.argtypes = [c_int]
__stpcpy = _libraries['libX11.so.6'].__stpcpy
__stpcpy.restype = STRING
__stpcpy.argtypes = [STRING, STRING]
__stpncpy = _libraries['libX11.so.6'].__stpncpy
__stpncpy.restype = STRING
__stpncpy.argtypes = [STRING, STRING, size_t]
strverscmp = _libraries['libX11.so.6'].strverscmp
strverscmp.restype = c_int
strverscmp.argtypes = [STRING, STRING]
strfry = _libraries['libX11.so.6'].strfry
strfry.restype = STRING
strfry.argtypes = [STRING]
memfrob = _libraries['libX11.so.6'].memfrob
memfrob.restype = c_void_p
memfrob.argtypes = [c_void_p, size_t]
basename = _libraries['libX11.so.6'].basename
basename.restype = STRING
basename.argtypes = [STRING]
basename = _libraries['libX11.so.6'].basename
basename.restype = STRING
basename.argtypes = [STRING]
__clock_t = c_long
clock_t = __clock_t
__time_t = c_long
time_t = __time_t
__clockid_t = c_int
clockid_t = __clockid_t
__timer_t = c_void_p
timer_t = __timer_t
class timespec(Structure):
    pass
__syscall_slong_t = c_long
timespec._fields_ = [
    ('tv_sec', __time_t),
    ('tv_nsec', __syscall_slong_t),
]
__errno_location = _libraries['libX11.so.6'].__errno_location
__errno_location.restype = POINTER(c_int)
__errno_location.argtypes = []
pthread_t = c_ulong
class pthread_attr_t(Union):
    pass
class __pthread_internal_list(Structure):
    pass
__pthread_internal_list._fields_ = [
    ('__prev', POINTER(__pthread_internal_list)),
    ('__next', POINTER(__pthread_internal_list)),
]
__pthread_list_t = __pthread_internal_list
class __pthread_mutex_s(Structure):
    pass
__pthread_mutex_s._fields_ = [
    ('__lock', c_int),
    ('__count', c_uint),
    ('__owner', c_int),
    ('__nusers', c_uint),
    ('__kind', c_int),
    ('__spins', c_short),
    ('__elision', c_short),
    ('__list', __pthread_list_t),
]
class N14pthread_cond_t3DOT_6E(Structure):
    pass
N14pthread_cond_t3DOT_6E._fields_ = [
    ('__lock', c_int),
    ('__futex', c_uint),
    ('__total_seq', c_ulonglong),
    ('__wakeup_seq', c_ulonglong),
    ('__woken_seq', c_ulonglong),
    ('__mutex', c_void_p),
    ('__nwaiters', c_uint),
    ('__broadcast_seq', c_uint),
]
pthread_key_t = c_uint
pthread_once_t = c_int
class N16pthread_rwlock_t3DOT_9E(Structure):
    pass
N16pthread_rwlock_t3DOT_9E._fields_ = [
    ('__lock', c_int),
    ('__nr_readers', c_uint),
    ('__readers_wakeup', c_uint),
    ('__writer_wakeup', c_uint),
    ('__nr_readers_queued', c_uint),
    ('__nr_writers_queued', c_uint),
    ('__writer', c_int),
    ('__shared', c_int),
    ('__pad1', c_ulong),
    ('__pad2', c_ulong),
    ('__flags', c_uint),
]
pthread_spinlock_t = c_int
__fdelt_chk = _libraries['libX11.so.6'].__fdelt_chk
__fdelt_chk.restype = c_long
__fdelt_chk.argtypes = [c_long]
__fdelt_warn = _libraries['libX11.so.6'].__fdelt_warn
__fdelt_warn.restype = c_long
__fdelt_warn.argtypes = [c_long]
__sig_atomic_t = c_int
class __sigset_t(Structure):
    pass
__sigset_t._fields_ = [
    ('__val', c_ulong * 16),
]
bsearch = _libraries['libX11.so.6'].bsearch
bsearch.restype = c_void_p
bsearch.argtypes = [c_void_p, c_void_p, size_t, size_t, __compar_fn_t]
atof = _libraries['libX11.so.6'].atof
atof.restype = c_double
atof.argtypes = [STRING]
__realpath_chk = _libraries['libX11.so.6'].__realpath_chk
__realpath_chk.restype = STRING
__realpath_chk.argtypes = [STRING, STRING, size_t]
realpath = _libraries['libX11.so.6'].realpath
realpath.restype = STRING
realpath.argtypes = [STRING, STRING]
__ptsname_r_chk = _libraries['libX11.so.6'].__ptsname_r_chk
__ptsname_r_chk.restype = c_int
__ptsname_r_chk.argtypes = [c_int, STRING, size_t, size_t]
ptsname_r = _libraries['libX11.so.6'].ptsname_r
ptsname_r.restype = c_int
ptsname_r.argtypes = [c_int, STRING, size_t]
__wctomb_chk = _libraries['libX11.so.6'].__wctomb_chk
__wctomb_chk.restype = c_int
__wctomb_chk.argtypes = [STRING, c_wchar, size_t]
wctomb = _libraries['libX11.so.6'].wctomb
wctomb.restype = c_int
wctomb.argtypes = [STRING, c_wchar]
__mbstowcs_chk = _libraries['libX11.so.6'].__mbstowcs_chk
__mbstowcs_chk.restype = size_t
__mbstowcs_chk.argtypes = [WSTRING, STRING, size_t, size_t]
mbstowcs = _libraries['libX11.so.6'].mbstowcs
mbstowcs.restype = size_t
mbstowcs.argtypes = [WSTRING, STRING, size_t]
__wcstombs_chk = _libraries['libX11.so.6'].__wcstombs_chk
__wcstombs_chk.restype = size_t
__wcstombs_chk.argtypes = [STRING, WSTRING, size_t, size_t]
wcstombs = _libraries['libX11.so.6'].wcstombs
wcstombs.restype = size_t
wcstombs.argtypes = [STRING, WSTRING, size_t]
memcpy = _libraries['libX11.so.6'].memcpy
memcpy.restype = c_void_p
memcpy.argtypes = [c_void_p, c_void_p, size_t]
memmove = _libraries['libX11.so.6'].memmove
memmove.restype = c_void_p
memmove.argtypes = [c_void_p, c_void_p, size_t]
mempcpy = _libraries['libX11.so.6'].mempcpy
mempcpy.restype = c_void_p
mempcpy.argtypes = [c_void_p, c_void_p, size_t]
memset = _libraries['libX11.so.6'].memset
memset.restype = c_void_p
memset.argtypes = [c_void_p, c_int, size_t]
bcopy = _libraries['libX11.so.6'].bcopy
bcopy.restype = None
bcopy.argtypes = [c_void_p, c_void_p, size_t]
bzero = _libraries['libX11.so.6'].bzero
bzero.restype = None
bzero.argtypes = [c_void_p, size_t]
strcpy = _libraries['libX11.so.6'].strcpy
strcpy.restype = STRING
strcpy.argtypes = [STRING, STRING]
stpcpy = _libraries['libX11.so.6'].stpcpy
stpcpy.restype = STRING
stpcpy.argtypes = [STRING, STRING]
strncpy = _libraries['libX11.so.6'].strncpy
strncpy.restype = STRING
strncpy.argtypes = [STRING, STRING, size_t]
__stpncpy_chk = _libraries['libX11.so.6'].__stpncpy_chk
__stpncpy_chk.restype = STRING
__stpncpy_chk.argtypes = [STRING, STRING, size_t, size_t]
stpncpy = _libraries['libX11.so.6'].stpncpy
stpncpy.restype = STRING
stpncpy.argtypes = [STRING, STRING, size_t]
strcat = _libraries['libX11.so.6'].strcat
strcat.restype = STRING
strcat.argtypes = [STRING, STRING]
strncat = _libraries['libX11.so.6'].strncat
strncat.restype = STRING
strncat.argtypes = [STRING, STRING, size_t]
class timeval(Structure):
    pass
__suseconds_t = c_long
timeval._fields_ = [
    ('tv_sec', __time_t),
    ('tv_usec', __suseconds_t),
]
__u_char = c_ubyte
__u_short = c_ushort
__u_int = c_uint
__u_long = c_ulong
__int8_t = c_byte
__uint8_t = c_ubyte
__int16_t = c_short
__uint16_t = c_ushort
__int32_t = c_int
__uint32_t = c_uint
__int64_t = c_long
__uint64_t = c_ulong
__quad_t = c_long
__u_quad_t = c_ulong
__dev_t = c_ulong
__uid_t = c_uint
__gid_t = c_uint
__ino_t = c_ulong
__ino64_t = c_ulong
__mode_t = c_uint
__nlink_t = c_ulong
__off_t = c_long
__off64_t = c_long
__pid_t = c_int
class __fsid_t(Structure):
    pass
__fsid_t._fields_ = [
    ('__val', c_int * 2),
]
__rlim_t = c_ulong
__rlim64_t = c_ulong
__id_t = c_uint
__useconds_t = c_uint
__daddr_t = c_int
__key_t = c_int
__blksize_t = c_long
__blkcnt_t = c_long
__blkcnt64_t = c_long
__fsblkcnt_t = c_ulong
__fsblkcnt64_t = c_ulong
__fsfilcnt_t = c_ulong
__fsfilcnt64_t = c_ulong
__fsword_t = c_long
__ssize_t = c_long
__syscall_ulong_t = c_ulong
__loff_t = __off64_t
__qaddr_t = POINTER(__quad_t)
__caddr_t = STRING
__intptr_t = c_long
__socklen_t = c_uint

# values for enumeration 'idtype_t'
idtype_t = c_int # enum
class N4wait5DOT_254E(Structure):
    pass
N4wait5DOT_254E._fields_ = [
    ('__w_termsig', c_uint, 7),
    ('__w_coredump', c_uint, 1),
    ('__w_retcode', c_uint, 8),
    ('', c_uint, 16),
]
class N4wait5DOT_255E(Structure):
    pass
N4wait5DOT_255E._fields_ = [
    ('__w_stopval', c_uint, 8),
    ('__w_stopsig', c_uint, 8),
    ('', c_uint, 16),
]
sigset_t = __sigset_t
__fd_mask = c_long
class fd_set(Structure):
    pass
fd_set._fields_ = [
    ('fds_bits', __fd_mask * 16),
]
fd_mask = __fd_mask
select = _libraries['libX11.so.6'].select
select.restype = c_int
select.argtypes = [c_int, POINTER(fd_set), POINTER(fd_set), POINTER(fd_set), POINTER(timeval)]
pselect = _libraries['libX11.so.6'].pselect
pselect.restype = c_int
pselect.argtypes = [c_int, POINTER(fd_set), POINTER(fd_set), POINTER(fd_set), POINTER(timespec), POINTER(__sigset_t)]
gnu_dev_major = _libraries['libX11.so.6'].gnu_dev_major
gnu_dev_major.restype = c_uint
gnu_dev_major.argtypes = [c_ulonglong]
gnu_dev_minor = _libraries['libX11.so.6'].gnu_dev_minor
gnu_dev_minor.restype = c_uint
gnu_dev_minor.argtypes = [c_ulonglong]
gnu_dev_makedev = _libraries['libX11.so.6'].gnu_dev_makedev
gnu_dev_makedev.restype = c_ulonglong
gnu_dev_makedev.argtypes = [c_uint, c_uint]
u_char = __u_char
u_short = __u_short
u_int = __u_int
u_long = __u_long
quad_t = __quad_t
u_quad_t = __u_quad_t
fsid_t = __fsid_t
loff_t = __loff_t
ino_t = __ino_t
ino64_t = __ino64_t
dev_t = __dev_t
gid_t = __gid_t
mode_t = __mode_t
nlink_t = __nlink_t
uid_t = __uid_t
off_t = __off_t
off64_t = __off64_t
pid_t = __pid_t
id_t = __id_t
ssize_t = __ssize_t
daddr_t = __daddr_t
caddr_t = __caddr_t
key_t = __key_t
useconds_t = __useconds_t
suseconds_t = __suseconds_t
ulong = c_ulong
ushort = c_ushort
uint = c_uint
int8_t = c_int8
int16_t = c_int16
int64_t = c_int64
u_int8_t = c_ubyte
u_int16_t = c_ushort
u_int32_t = c_uint
u_int64_t = c_ulong
register_t = c_long
blksize_t = __blksize_t
blkcnt_t = __blkcnt_t
fsblkcnt_t = __fsblkcnt_t
fsfilcnt_t = __fsfilcnt_t
blkcnt64_t = __blkcnt64_t
fsblkcnt64_t = __fsblkcnt64_t
fsfilcnt64_t = __fsfilcnt64_t
class __locale_data(Structure):
    pass
__locale_struct._fields_ = [
    ('__locales', POINTER(__locale_data) * 13),
    ('__ctype_b', POINTER(c_ushort)),
    ('__ctype_tolower', POINTER(c_int)),
    ('__ctype_toupper', POINTER(c_int)),
    ('__names', STRING * 13),
]
__locale_data._fields_ = [
]
locale_t = __locale_t
ptrdiff_t = c_long
_XkbEvent._fields_ = [
    ('type', c_int),
    ('any', XkbAnyEvent),
    ('new_kbd', XkbNewKeyboardNotifyEvent),
    ('map', XkbMapNotifyEvent),
    ('state', XkbStateNotifyEvent),
    ('ctrls', XkbControlsNotifyEvent),
    ('indicators', XkbIndicatorNotifyEvent),
    ('names', XkbNamesNotifyEvent),
    ('compat', XkbCompatMapNotifyEvent),
    ('bell', XkbBellNotifyEvent),
    ('message', XkbActionMessageEvent),
    ('accessx', XkbAccessXNotifyEvent),
    ('device', XkbExtensionDeviceNotifyEvent),
    ('core', XEvent),
]
xReply._fields_ = [
    ('generic', xGenericReply),
    ('geom', xGetGeometryReply),
    ('tree', xQueryTreeReply),
    ('atom', xInternAtomReply),
    ('atomName', xGetAtomNameReply),
    ('property', xGetPropertyReply),
    ('listProperties', xListPropertiesReply),
    ('selection', xGetSelectionOwnerReply),
    ('grabPointer', xGrabPointerReply),
    ('grabKeyboard', xGrabKeyboardReply),
    ('pointer', xQueryPointerReply),
    ('motionEvents', xGetMotionEventsReply),
    ('coords', xTranslateCoordsReply),
    ('inputFocus', xGetInputFocusReply),
    ('textExtents', xQueryTextExtentsReply),
    ('fonts', xListFontsReply),
    ('fontPath', xGetFontPathReply),
    ('image', xGetImageReply),
    ('colormaps', xListInstalledColormapsReply),
    ('allocColor', xAllocColorReply),
    ('allocNamedColor', xAllocNamedColorReply),
    ('colorCells', xAllocColorCellsReply),
    ('colorPlanes', xAllocColorPlanesReply),
    ('colors', xQueryColorsReply),
    ('lookupColor', xLookupColorReply),
    ('bestSize', xQueryBestSizeReply),
    ('extension', xQueryExtensionReply),
    ('extensions', xListExtensionsReply),
    ('setModifierMapping', xSetModifierMappingReply),
    ('getModifierMapping', xGetModifierMappingReply),
    ('setPointerMapping', xSetPointerMappingReply),
    ('getKeyboardMapping', xGetKeyboardMappingReply),
    ('getPointerMapping', xGetPointerMappingReply),
    ('pointerControl', xGetPointerControlReply),
    ('screenSaver', xGetScreenSaverReply),
    ('hosts', xListHostsReply),
    ('error', xError),
    ('event', xEvent),
]
_XkbAction._fields_ = [
    ('any', XkbAnyAction),
    ('mods', XkbModAction),
    ('group', XkbGroupAction),
    ('iso', XkbISOAction),
    ('ptr', XkbPtrAction),
    ('btn', XkbPtrBtnAction),
    ('dflt', XkbPtrDfltAction),
    ('screen', XkbSwitchScreenAction),
    ('ctrls', XkbCtrlsAction),
    ('msg', XkbMessageAction),
    ('redirect', XkbRedirectKeyAction),
    ('devbtn', XkbDeviceBtnAction),
    ('devval', XkbDeviceValuatorAction),
    ('type', c_ubyte),
]
pthread_attr_t._fields_ = [
    ('__size', c_char * 56),
    ('__align', c_long),
]
__all__ = ['XUnlockDisplay', 'ETXTBSY', '_XEventToWire',
           'GCClipXOrigin', 'XkbSA_SetValMin', 'XMappingEvent',
           'NoSymbol', '__off64_t', '__int16_t', 'ButtonMotionMask',
           'XkbDeviceBell', 'XkbSI_LevelOneOnly', 'XkbNoIndicator',
           'XkbUpdateMapFromCore', 'X_SetSelectionOwner', 'EL3HLT',
           'EnterWindowMask', 'ENOTSOCK', 'XInitThreads', 'CARD64',
           'XkbSA_GroupAbsolute', 'XkbDescPtr', 'xFreeColorsReq',
           'wctomb', 'ErrorType', 'XkbLC_AlternateGroup', 'getpt',
           'XQueryPointer', 'XCreatePixmapFromBitmapData',
           'XIMPrimary', 'getloadavg', 'XkbSI_OpMask', 'GC',
           'XListFonts', 'ENOLINK', '__NFDBITS',
           'XGetKeyboardMapping', 'XFontsOfFontSet',
           'XkbSetDetectableAutoRepeat', 'XDisplayString',
           'ColormapInstalled', 'AnyModifier', 'XGenericEventCookie',
           'X_ImageText16', 'X_PolyRectangle',
           'XCirculateSubwindowsUp', 'xFillPolyReq',
           '__ptsname_r_chk', 'XkbKeyNameRec', 'gnu_dev_makedev',
           'XIMIsSecondary', 'XkbSetMap', '_DEFAULT_SOURCE',
           'XPeekIfEvent', 'XkbMapChangesRec', 'ForgetGravity',
           'XkbTwoLevelMask', 'XkbDeviceChangesPtr',
           'sz_xGetPropertyReply', 'XCheckTypedEvent',
           'XkbDeviceLedChangesRec', 'XkbGetIndicatorState',
           '__uint8_t', '_XRegisterInternalConnection', 'Visual',
           'xGetFontPathReply', 'KBKey', 'XSetOCValues',
           'XCreateWindowEvent', 'XkbGetKeySyms', 'X_kbSetGeometry',
           'MappingFailed', 'xGetKeyboardMappingReq',
           'XGraphicsExposeEvent', '_XIC', 'setstate_r',
           'XLocaleOfIM', '__locale_data', '_XIM', '_XCreateMutex_fn',
           'xGenericReply', 'xCharInfo', 'strerror_l', 'XCloseIM',
           'XBlackPixelOfScreen', 'XChangeProperty', 'xPolyLineReq',
           'XIMPreeditArea', 'XkbAXN_SKReleaseMask', 'E2BIG',
           'xFontProp', 'CWBorderPixel', 'XkbCompatMapNotifyEvent',
           'EHOSTDOWN', 'GrayScale', 'Xutf8DrawImageString', 'EBUSY',
           'XCreateBitmapFromData', 'qecvt', 'xAllocNamedColorReq',
           'XGetPointerControl', 'XESetBeforeFlush', 'X_GetImage',
           'XDefaultDepthOfScreen', 'XDisplayOfOM',
           'sz_xChangeHostsReq', 'X_FreeCursor', 'ButtonPress',
           'sz_xFontProp', 'X_ListExtensions', 'EDQUOT',
           'XSetWindowBorder', 'XkbBounceKeysMask', 'X_ChangeHosts',
           'ino_t', 'X_QueryTextExtents', 'X_TCP_PORT',
           'XkbAX_SKPressFBMask', 'strerror', 'X_FreeGC', 'AllPlanes',
           'X_ImageText8', '_Xglobal_lock', 'ArcPieSlice',
           'X_ChangeKeyboardControl', 'EXFULL',
           'XCopyColormapAndFree', 'X_ChangeKeyboardMapping',
           'XkbIM_UseNone', 'sz_xLookupColorReq', 'XGContextFromGC',
           'bcmp', 'XDisplayPlanes', 'X_ChangeGC',
           'XkbPCF_LookupStateWhenGrabbed', 'EFBIG', 'xListFontsReq',
           'X_GetKeyboardControl', 'ColormapChangeMask',
           'XProtocolVersion', 'XCreatePixmapCursor',
           'XkbAX_StickyKeysFBMask', '_XkbKbdDpyState', 'lrand48',
           'memfrob', 'xChangePointerControlReq', 'XmbTextExtents',
           '__WORDSIZE', 'sz_xGrabButtonReq', '_XOPEN_SOURCE',
           'u_short', 'LineOnOffDash', 'XLookupBoth',
           'sz_xStoreColorsReq', 'LASTEvent', 'XGetAtomName',
           'XRemoveConnectionWatch', 'sz_xOpenFontReq', '__GLIBC__',
           'DefaultExposures', 'XkbSA_LockNoUnlock',
           'sz_xQueryBestSizeReq', 'GXnand', 'XkbLatchModifiers',
           'strerror_r', '__u_int', 'sz_xGenericReply', 'Mod2Mask',
           'VisibilityNotify', '_XLOCALE_H', 'XkbSA_SwitchScreen',
           'XkbAXN_SKAcceptMask', 'XkbSymbolsNameMask', 'strtouq',
           'sz_xPolyText16Req', 'xPutImageReq', '__time_t', 'ENOTTY',
           'strtoul', 'XkbSetDeviceInfo', 'XNQueryIMValuesList',
           'X_AllocColor', 'strtol_l', 'sz_xGrabKeyboardReply',
           'sz_xQueryColorsReply', '__USE_POSIX2', 'XkbPtrAction',
           'EMLINK', '__USE_XOPEN2K8XSI', 'blkcnt_t',
           'FamilyInternet', 'XSetScreenSaver', '_XFreeFuncs',
           'XUnmapEvent', 'XCheckIfEvent', 'XInternAtoms',
           'GXandReverse', 'XkbGetKeyboard', 'XDrawLines',
           'xGenericEvent', 'ECANCELED', 'XNStatusAttributes',
           '_XkbRedirectKeyAction', 'u_char', 'XSelectionClearEvent',
           'N7_xEvent5DOT_1465DOT_158E', 'uid_t', 'u_int64_t',
           'u_int16_t', 'N7_xEvent5DOT_1465DOT_1725DOT_1735DOT_176E',
           'XDrawPoints', 'XIMPreeditCallbacks', 'XKeyboardState',
           'XESetCopyEventCookie', 'XGetSelectionOwner',
           'XkbExplicitKeyType4Mask', 'XSetTSOrigin',
           'XkbKeyTypeNamesMask', 'MappingSuccess',
           'XkbXI_IndicatorMapsMask', 'XkbKeyNamesMask',
           'xQueryTextExtentsReq', 'XAddToExtensionList',
           'XNDefaultString', 'XkbIM_UseBase', 'N9_XDisplay5DOT_252E',
           'BadName', 'XkbAX_DumbBellFBMask',
           'XkbIndicatorChangesRec', 'XkbRedirectKeyAction',
           'sz_xGetFontPathReply', 'div_t', 'xListHostsReq',
           'Mod3MapIndex', 'XkbISOAction', 'X_kbGetDeviceInfo',
           'xGetPropertyReply', 'XkbDeviceLedInfoRec', 'sz_xReply',
           'ELOOP', 'strcspn', 'SouthGravity',
           'sz_xConfigureWindowReq', 'XkbLC_AllComposeControls',
           'free', 'XkbGetKeyBehaviors', 'Cursor', 'xWindowRoot',
           'XkbSA_NoAcceleration', '_XkbMapChanges', 'GCForeground',
           'xError', 'XkbSI_NoneOf', '_XGetAsyncData',
           'XAddConnectionWatch', '__pthread_list_t', 'XDestroyIC',
           'XUndefineCursor', '__rlim64_t', 'sz_xListPropertiesReply',
           'rand', 'XChangeKeyboardControl', '__dev_t', 'XKillClient',
           '__W_CONTINUED', '__blksize_t', 'xSetInputFocusReq',
           'fsblkcnt_t', 'ArcChord', 'XkbAXN_AXKWarning', 'XDrawArcs',
           'XkbAllocNames', 'xConnSetup', 'XStoreName',
           'XQueryBestSize', '_X11XCBPrivate', 'ino64_t',
           'XkbGetDetectableAutoRepeat', 'memcmp', 'EISNAM',
           'xAllowEventsReq', 'sz_xGetScreenSaverReply',
           'ColormapNotify', 'X_QueryTree', '__blkcnt64_t',
           'mkostemp', '_XkbDeviceInfo', 'PlaceOnTop',
           'xRecolorCursorReq', 'XlibDisplayNoXkb',
           'sz_xSetClipRectanglesReq', 'XkbSA_SwitchAbsolute',
           'XOpenIM', 'sz_xCreateCursorReq', 'XRectangle',
           'XkbXI_AllDeviceFeaturesMask', 'XAllocColor',
           'XStoreColor', 'XkbControlsNotifyEvent',
           'sz_xAllocColorCellsReq', 'RetainTemporary',
           'XSetGraphicsExposures', '_BITS_TYPES_H',
           'XkbDeviceBtnAction', 'EILSEQ', 'XkbModsPtr', 'MapRequest',
           '__rlim_t', 'XGetErrorText', 'XkbAllGroupsMask',
           'setstate', 'ENONET', 'ECHRNG', 'NotifyPointerRoot',
           'GCJoinStyle', '_XkbIndicatorNotify', 'GCTileStipYOrigin',
           'XkbDeviceLedChangesPtr', 'XIMStringConversionLeftEdge',
           '__u_char', 'ESRCH', 'CWY', 'CWX', '_XkbEvent',
           'XkbGetAutoResetControls', 'XScreenCount', 'xPolyPointReq',
           'xConnClientPrefix', 'X_kbUseExtension', 'XkbAllNamesMask',
           'XGetIMValues', 'xSendEventReq', 'XkbMapChangesPtr',
           'YXSorted', '_XkbModAction', 'sz_xGetAtomNameReply',
           '__key_t', 'ENOMSG', 'xChangeModeReq', 'XkbSA_BreakLatch',
           'EISDIR', 'LockMapIndex', 'XResetScreenSaver', 'XNoOp',
           'XDefaultColormap', 'random', 'XkbGeomPtsPerMM',
           'XDisplayKeycodes', '_XInternalConnectionProc',
           '__GNU_LIBRARY__', 'sz_xImageTextReq', 'EnterNotify',
           'X_QueryBestSize', 'X_InstallColormap',
           'X_ConvertSelection', 'X_PolyText8', 'LeaveWindowMask',
           'XkbDeviceInfoRec', 'XkbGetNames', 'XESetPrintErrorValues',
           '_XkbChanges', 'BadAccess', 'XkbIM_UseAnyGroup',
           'X_AllowEvents', '_XkbGeometry', 'EBADRQC', 'StaticColor',
           '_XErrorFunction', 'XServerInterpretedAddress',
           'rawmemchr', 'sz_xGetSelectionOwnerReply',
           'XkbExplicitInterpretMask', '_XConnWatchInfo',
           'XkbGetIndicatorMap', 'XGetModifierMapping',
           'XTextWidth16', 'XGetIconName',
           'N7_xEvent5DOT_1465DOT_162E', 'XkbFreeKeyboard',
           'XGetICValues', '_PutImageReq', 'XReadBitmapFile',
           'sz_xGrabKeyboardReq', 'XListExtensions',
           'CWBackingPlanes', 'XSetWMProtocols',
           'XkbSA_ISONoAffectPtr', 'quad_t', 'XkbForceDeviceBell',
           'strncmp', 'XkbRGMaxMembers', 'XkbGroupBaseMask',
           'X_InternAtom', 'mkdtemp', 'XIMForwardChar', 'strcat',
           '_XSetClipRectangles', 'XkbNoteDeviceChanges',
           'sz_xSetMappingReply', 'XMinCmapsOfScreen', '_XkbStateRec',
           'XkbStickyKeysMask', 'X_GetProperty', 'XClearWindow',
           'N7_xEvent5DOT_1465DOT_1725DOT_173E', 'XkbDfltXIId',
           'XLoadQueryFont', 'sz_xSendEventReq', 'X_ForceScreenSaver',
           'Xutf8DrawText', 'sz_xGrabPointerReply', 'KBBellPercent',
           'posix_memalign', 'XDrawRectangles',
           'XkbSetNamedIndicator', 'XkbKeysymToModifiers',
           'sz_xAllocColorReq', 'xGetSelectionOwnerReply',
           '__FD_SETSIZE', 'DisableAccess', 'Button2MotionMask',
           'XChar2b', 'seed48_r', 'XFreeColors', '_XkbClientMapRec',
           'LOCKED', 'xQueryTreeReply', 'XkbMapNotifyMask',
           'XESetCloseDisplay', '_XkbDeviceLedInfo', '_XReadEvents',
           'Convex', '_XAllocIDs', 'XQueryTextExtents',
           'FARCSPERBATCH', 'EMFILE', 'int32_t', 'off64_t',
           'XHeightOfScreen', 'X_UnmapWindow', 'XkbGetKeyModifierMap',
           'PropertyNotify', '_XIMFilter', 'XwcDrawString',
           'Button3MotionMask', 'gnu_dev_major', 'XkbDeviceBellEvent',
           '_XDefaultIOError', '__PTHREAD_MUTEX_HAVE_ELISION',
           'XOrientation', 'XGetAtomNames', 'strsignal',
           'XModifierKeymap', 'XkbNumberErrors', 'XkbKeyTypeRec',
           'MSBFirst', 'XExtData', 'XAllPlanes', 'XLookupColor',
           'WNOHANG', 'sz_xGetModifierMappingReply', 'XOpenOM',
           'XESetWireToEventCookie', 'BYTE', 'bzero', '_XGC',
           'XLocaleOfOM', 'EXIT_SUCCESS', '__suseconds_t',
           '_XProcessWindowAttributes', 'CWOverrideRedirect',
           'VisualID', 'XPointer', 'clearenv', 'XIMCaretDirection',
           'ENOSTR', 'XkbModAction', 'sz_xSetModifierMappingReq',
           '__INO_T_MATCHES_INO64_T', 'XkbGetNamedDeviceIndicator',
           'XIMTextType', 'XContextualDrawing', 'FamilyDECnet',
           'X_Bell', 'XFocusChangeEvent', 'XConfigureEvent',
           'X_ListInstalledColormaps', 'X_OpenFont', 'strnlen',
           'XlibDisplayIOError', 'FirstExtensionError',
           'sz_xPutImageReq', 'XIMHotKeyTrigger', 'KBBellDuration',
           'XTimeCoord', 'CapNotLast', 'XIMPreeditPosition',
           '__SIZEOF_PTHREAD_ATTR_T', 'XkbGrabModsMask',
           'EnableAccess', 'XkbLC_ConsumeKeysOnComposeFail',
           'XkbFreeCompatMap', 'NotifyHint', 'XConfigureRequestEvent',
           'sz_xQueryFontReply', 'XSetModifierMapping', 'wcstombs',
           'XNQueryInputStyle', '_XScreenOfWindow', 'nrand48',
           'xGetGeometryReply', 'XRefreshKeyboardMapping',
           'XWidthMMOfScreen', 'XIMNextLine', '_XVIDtoVisual',
           'XIMDontChange', '__USE_XOPEN2KXSI', 'ShiftMapIndex',
           'XkbAXN_SKAccept', 'XkbNewKeyboardNotifyMask',
           'XlibDisplayDfltRMDB', 'XConvertSelection',
           'XkbGetKeyExplicitComponents', 'pthread_once_t',
           '__timer_t', 'XIMBackwardWord', 'XTextExtents16',
           'XPlanesOfScreen', 'XkbGetDeviceButtonActions',
           'XkbComponentNameRec', 'CWSibling', '__uint32_t',
           '__USE_XOPEN2K8', 'SelectionNotify',
           'XkbUpdateKeyTypeVirtualMods', 'XkbSetDebuggingFlags',
           'BadAtom', 'RAND_MAX', 'XkbSA_NoAction',
           'NeedVarargsPrototypes', 'XDisplayOfScreen',
           'XEnterWindowEvent', 'CapButt', 'sz_xCopyAreaReq',
           'loff_t', 'XkbCompatNameMask', 'XChangeActivePointerGrab',
           'XkbGetUpdatedMap', 'blksize_t', '_XPrivate', '_XExten',
           'sz_xSetFontPathReq', '_XLockMutex_fn', 'XESetFreeFont',
           'XVisibilityEvent', 'XESetCreateGC', 'strstr',
           'XkbAllExtensionDeviceEventsMask', 'gnu_dev_minor',
           'AllTemporary', 'ESRMNT', 'XFillArcs',
           '_XkbMapNotifyEvent', 'X_MapWindow', '_ISOC99_SOURCE',
           'XPointerMovedEvent', 'XBitmapUnit',
           'XkbControlsEnabledMask', 'X_QueryKeymap', 'rpmatch',
           'XkbCompatLookupModsMask', 'X_KillClient',
           'XkbChangeKeycodeRange', 'unlockpt', 'sz_xCreateGCReq',
           '_XF86LoadQueryLocaleFont', 'strcoll_l', 'mblen', '__id_t',
           'XkbSA_ISOAffectMask', '__clock_t', 'XkbGetKeyTypes',
           'ResizeRedirectMask', 'RaiseLowest', 'X_CreatePixmap',
           'XIMPreeditNothing', 'DefaultBlanking',
           '__timer_t_defined', 'select', 'xQueryExtensionReply',
           'XkbGBN_ServerSymbolsMask', 'sz_xAllocNamedColorReq',
           'xListExtensionsReply', 'XFocusOutEvent', 'XMapEvent',
           'XNPreeditDoneCallback', 'XkbLC_ControlFallback',
           '_XkbISOAction', 'X_kbSelectEvents', 'XRemoveHosts',
           'N7_xEvent5DOT_1465DOT_163E', 'XInitImage', 'XIMFeedback',
           '__fsblkcnt_t', 'GCTile', 'strpbrk', 'XCheckWindowEvent',
           'xInternAtomReq', 'XFlushGC', 'sz_xGetImageReply',
           'HostInsert', 'AutoRepeatModeDefault',
           'XkbSA_MoveAbsoluteY', 'XkbSA_MoveAbsoluteX',
           '_SIGSET_H_types', 'KBKeyClickPercent',
           'N16pthread_rwlock_t3DOT_9E', 'DontPreferBlanking',
           'XkbPointerButtonMask', 'GCDashList', 'X_ListHosts',
           '_4DOT_34', 'X_GetPointerMapping', 'XMoveResizeWindow',
           'XArc', 'XAddHosts', 'XkbLockModifiers', 'XwcResetIC',
           'SyncPointer', 'sz_xGetMotionEventsReply', 'XGetCommand',
           '_XkbInfoRec', 'EKEYREJECTED', 'NotifyDetailNone',
           'BadLength', 'ENOTCONN', 'InputOnly', '_XkbIndicatorRec',
           'ENETUNREACH', 'CWEventMask', 'XButtonReleasedEvent',
           'XSetWindowBackgroundPixmap', 'sz_xChangePropertyReq',
           'UnmapGravity', '_XIMStringConversionCallbackStruct',
           'strtoull_l', 'XkbSA_LockControls',
           '_XIMPreeditStateNotifyCallbackStruct', 'XAutoRepeatOn',
           'XkbAllocCompatMap', 'MapNotify', 'XNStringConversion',
           'GCClipYOrigin', 'X_FillPoly', 'sz_xConnClientPrefix',
           'XkbSA_SetControls', 'XCellsOfScreen', 'XDestroyOC',
           'XkbNoteMapChanges', 'XFocusInEvent',
           'sz_xRotatePropertiesReq', 'xSetFontPathReq', 'grantpt',
           'XkbGetPerClientControls', '_XkbMessageAction',
           'initstate', 'XGetKeyboardControl', 'XReparentEvent',
           'XkbName', 'XkbOD_NonXkbServer', 'XSetFontPath',
           'XkbSA_ISONoAffectMods', 'XkbIM_UseAnyMods',
           'posix_openpt', 'lldiv_t', 'memmem', 'ButtonPressMask',
           'XkbSA_MessageGenKeyEvent', '__quad_t', '_XContextDB',
           'XkbBellEvent', 'XkbComponentListRec', 'X_GetAtomName',
           '__SIZEOF_PTHREAD_RWLOCKATTR_T', '__u_quad_t', '__u_short',
           'XEvent', 'XNStdColormap', 'XkbSA_LockPtrBtn',
           'XkbQueryExtension', '_LARGEFILE64_SOURCE',
           'XkbTranslateKeySym', '_XDeq', '_XAsyncErrorState',
           'EastGravity', 'useconds_t', 'XDrawString',
           'PrintErrorType', '__uid_t', 'strtoul_l', 'ENOTBLK',
           '_XAsyncEState', 'XButtonPressedEvent', 'XkbWrapIntoRange',
           '_XUnlockMutex_fn', '__USE_ISOC11', 'XkbLC_Partial',
           'XwcLookupString', 'XkbNoteNameChanges',
           'XkbBellNotifyEvent', 'ErrorStringType', 'X_GetFontPath',
           'XIMStringConversionWord', 'ENOPKG', 'PointerWindow',
           'LineDoubleDash', 'SyncBoth', 'XICCallback', 'XAnyEvent',
           'ESTALE', 'IsViewable', 'qecvt_r', 'XkbIndicatorMapPtr',
           'XSetWindowBackground', 'XkbIM_LEDDrivesKB',
           'XLookupKeysym', 'XIMBackwardChar', 'XkbSA_ISODfltIsGroup',
           'X_kbSetIndicatorMap', 'XkbAllClientInfoMask',
           'XIMStringConversionTopEdge', 'XNDestroyCallback',
           '__bzero', 'XIMStringConversionChar', 'XmbResetIC',
           'XkbUseCoreKbd', 'XkbComponentNamesMask',
           'sz_xPolyFillArcReq', 'XkbAllRequiredTypes',
           '__time_t_defined', 'XkbKeycodesNameMask', 'XSetDashes',
           '_XkbNewKeyboardNotify', 'XkbGroup4Mask',
           'sz_xFillPolyReq', 'SubstructureNotifyMask',
           '_XGetWindowAttributes', 'XkbModifierLatchMask',
           'XkbSetIgnoreLockMods', 'XDefaultRootWindow',
           '_XkbCompatMapNotify', 'XkbDeviceChangesRec',
           'XAllowEvents', 'XInsertModifiermapEntry', 'fsfilcnt_t',
           'div', 'XUngrabServer', 'XIMIsPrimary', 'nrand48_r',
           'N7_xEvent5DOT_1465DOT_156E', 'XSupportsLocale', 'ecvt',
           'ENOTUNIQ', 'XkbKeyAliasesMask', 'ELNRNG', '__stpcpy',
           'XVaNestedList', 'ERESTART', 'N7_xEvent5DOT_1465DOT_164E',
           'BadRequest', 'XkbLC_ComposeLED', 'XkbAX_SlowWarnFBMask',
           'XOMOrientation_RTL_TTB', '__nlink_t', 'ffsll',
           'X_GetSelectionOwner', 'ENOPROTOOPT', '_XAsyncHandler',
           'BadIDChoice', 'XCheckTypedWindowEvent', 'XPropertyEvent',
           'xGetPointerControlReply', 'True_', 'XCloseDisplay',
           'XClearArea', 'XNPreeditDrawCallback', 'XCreateGC',
           'xQueryBestSizeReq', 'XkbNoteControlsChanges',
           'X_CopyPlane', 'XDefaultScreenOfDisplay', 'realloc',
           'XkbGetNamedIndicator', 'sz_xPolyRectangleReq',
           'XDeleteModifiermapEntry', 'strtok',
           'N7_xEvent5DOT_1465DOT_148E', 'XNMissingCharSet',
           '_XEatData', 'XkbGeometryMask', 'XkbGeometryNameMask',
           'XkbAXN_SKRelease', 'XkbKeypadIndex', 'xDepth',
           'xForceScreenSaverReq', 'XPeekEvent',
           'xSetModifierMappingReq', 'XCONN_CHECK_FREQ',
           'XNFocusWindow', 'GCCapStyle', 'XChangePointerControl',
           'XExposeEvent', 'XkbControlsChangesRec', 'Button1Mask',
           'X_GrabKey', 'u_quad_t', 'XkbGetVirtualMods',
           'CWDontPropagate', 'XSetPointerMapping', 'XkbNamesRec',
           'daddr_t', 'XkbRedirectIntoRange', 'strdup',
           'XIMStatusNone', 'XDirectionalDependentDrawing',
           'XSetInputFocus', 'XGetWMProtocols', 'XNInputStyle',
           'ELIBACC', '__int8_t', 'SelectionClear',
           'XkbControlsNotifyMask', 'off_t', '_XTextHeight',
           'WestGravity', 'XICProc', 'XkbGetState',
           'ButtonReleaseMask', 'pthread_key_t', 'FocusIn',
           '_Xwctomb', 'XFillArc', 'u_int8_t', 'FontRightToLeft',
           'sz_xUngrabKeyReq', '__WALL', 'XConnectionWatchProc',
           'ENOTDIR', 'GCLineWidth', 'CWBackingPixel', 'XNFontSet',
           'XkbSA_SetValRelative', 'XQueryFont',
           'xCirculateWindowReq', '__locale_t', 'lcong48',
           'XGetInputFocus', 'CWStackMode', 'XCopyGC',
           'XkbSA_SwitchApplication', 'XkbGBN_SymbolsMask',
           'XStoreBuffer', 'sz_xGetGeometryReply', 'ENETRESET',
           'XDestroyWindowEvent', 'XkbSI_Exactly',
           'XSetAccessControl', 'XkbAllocClientMap',
           'XkbLC_KeypadKeys', 'XkbVirtualModsToReal',
           'XkbAnyGroupMask', 'unsetenv', 'Always',
           'XIMStatusNothing', 'FUNCPROTO', 'DestroyNotify',
           'GCFillRule', 'XkbSA_UseDfltButton', 'uint', 'GCArcMode',
           'xPolySegmentReq', 'N7_xEvent5DOT_1465DOT_161E',
           'strncasecmp_l', 'ColormapUninstalled', 'EINVAL',
           'XkbAnyActionDataSize', 'XSetFillStyle', 'XkbControlsRec',
           'XkbPerKeyBitArraySize', 'SubstructureRedirectMask',
           'xCreateCursorReq', 'XkbOverlay2Mask', 'EHOSTUNREACH',
           '__mempcpy', 'XkbActionMessage', 'XkbSA_NumActions',
           'sz_xQueryTreeReply', 'sz_xAllocColorPlanesReply',
           'XScreenNumberOfScreen', '_XUnregisterInternalConnection',
           'xGrabPointerReq', 'Xutf8TextPerCharExtents',
           'XkbMouseKeysMask', '_XSQEvent', 'size_t', '_XPrivDisplay',
           'XkbVirtualModsMask', 'XIMVisibleToBackword',
           'sz_xHostEntry', 'XkbMaxRedirectCount', 'XKeysymToKeycode',
           '__mbstowcs_chk', '__qaddr_t', '_Xdebug',
           'XkbKeyBehaviorsMask', 'XSetWindowAttributes',
           'XkbKTLevelNamesMask', 'Atom', 'XOMFontInfo',
           'XkbAllXIIds', 'XkbNKN_DeviceIDMask', 'X_kbGetNames',
           'xOpenFontReq', 'XkbUseCorePtr', 'X_CopyArea',
           'XDefaultVisualOfScreen', 'XkbAccessXOptionsMask',
           'EOPNOTSUPP', 'sigset_t', 'XGetWindowProperty', 'seed48',
           'xSetMappingReply', 'YXBanded', 'XkbVirtualModMapMask',
           'DisableScreenSaver', 'XNStringConversionCallback',
           '__USE_POSIX', 'XkbOneLevelIndex', 'XCreateWindow',
           'memchr', 'u_int32_t', 'IncludeInferiors', 'XIDProc',
           '__fd_mask', 'X_CloseFont', 'xTranslateCoordsReply',
           'XIMHotKeyTriggers', 'XkbCompatMapNotifyMask',
           'initstate_r', '__useconds_t', 'XwcDrawImageString',
           'XOMOfOC', 'UNLOCKED', 'FreeFuncType',
           'N7_xEvent5DOT_1465DOT_149E', 'sz_xCreatePixmapReq',
           'xPolyFillRectangleReq', 'xWarpPointerReq',
           '__clockid_t_defined', 'XMaxRequestSize', 'GXcopyInverted',
           'XkbGBN_KeyNamesMask', 'XOMCharSetList', 'XkbCopyKeyType',
           'BadMatch', 'EREMOTE', 'XIMPreeditUnKnown',
           '__WORDSIZE_TIME64_COMPAT32', 'AnyButton',
           'xAllocColorCellsReply', '_SYS_TYPES_H',
           'xGetPointerMappingReply', 'XSetStipple', 'XFetchName',
           'srand48_r', 'XkbGroupCompatMask', '_Xmblen', '__USE_GNU',
           'sz_xGetImageReq', 'WUNTRACED',
           'sz_xGetWindowAttributesReply', 'XkbMaxShiftLevel',
           'XkbStatePtr', 'lldiv', 'XkbAllControlsMask',
           'pthread_attr_t', 'XIMVisibleToCenter', 'CWBitGravity',
           'Xutf8TextEscapement', 'xAllocColorPlanesReq',
           'PlaceOnBottom', 'valloc', 'CreateFontType',
           'XSetLineAttributes', 'XkbCompatChangesPtr',
           'sz_xColorItem', 'XInstallColormap', '__ldiv_t_defined',
           'ScreenFormat', 'XFreeModifiermap', 'strtoll_l',
           'XkbInternalModsMask', 'pthread_t', 'comparison_fn_t',
           'strfry', 'NoExpose', 'XFreeFontNames',
           'X_DestroySubwindows', 'CreateNotify',
           'GCGraphicsExposures', '_XLockInfo', 'FreeModmapType',
           'ReparentNotify', 'XRootWindowOfScreen',
           'XkbGroupNamesMask', 'sz_xWarpPointerReq',
           'XBaseFontNameListOfFontSet', 'XLookupNone',
           'N7_xEvent5DOT_1465DOT_165E', '_XDisplay',
           'sz_xPolySegmentReq', 'GCSubwindowMode',
           'XkbNumVirtualMods', 'xResourceReq', 'FreeFontType',
           '__fsfilcnt64_t', 'XkbSymMapPtr', 'DontAllowExposures',
           'XkbKB_RadioGroup', 'XStoreBytes', 'X_kbListComponents',
           'sz_xStoreNamedColorReq', 'GrabModeAsync',
           'AllowExposures', 'IsUnviewable', 'XkbKTMapEntryRec',
           'CWWinGravity', 'xEvent', 'stpcpy', 'InputFocus',
           'LastExtensionError', 'nlink_t', '_XPollfdCacheDel',
           'XColormapEvent', 'WNOWAIT', 'xSegment', 'PropertyDelete',
           'X_GrabButton', 'xGetAtomNameReply', 'xChangeHostsReq',
           'INT8', 'realpath', 'SouthEastGravity', 'XkbMaxKbdGroup',
           '_XkbDeviceLedChanges', 'XIMStringConversionBottomEdge',
           'XGetDefault', 'EHWPOISON', 'XIMInitialState',
           'X_UnmapSubwindows', 'IsUnmapped', 'XPixmapFormatValues',
           'u_int', 'XESetCopyGC', 'XkbNameChangesRec', 'bcopy',
           'QueuedAfterFlush', 'XkbXI_UnsupportedFeatureMask',
           'AsyncPointer', 'srand48', 'XkbSA_PtrBtn',
           'XkbComponentNamePtr', 'ConfigureRequest', 'strtold_l',
           'sz_xCopyGCReq', 'sz_xResourceReq', 'XkbServerMapMask',
           'XDrawRectangle', 'XAllocNamedColor', '__FD_ZERO_STOS',
           'CopyGCType', '__uint16_t', 'xListInstalledColormapsReply',
           'atol', 'DirectColor', 'XSetWindowBorderPixmap',
           'N14pthread_cond_t3DOT_6E', 'sz_xTextElt', 'secure_getenv',
           'CWBackingStore', 'strtoull', '_XKeytrans',
           'XkbExtensionDeviceNotify', 'X_ChangeWindowAttributes',
           'ECONNRESET', 'XkbLookupKeySym', 'atof',
           'XNPreeditStateNotifyCallback',
           'X_ChangeActivePointerGrab', 'mkstemps', 'GXnoop',
           'XkbAllComponentsMask', 'Mod4MapIndex', 'ButtonRelease',
           'CoordModePrevious', 'XGeometry', 'XIC', 'XID', 'XIM',
           'XListPixmapFormats', 'XkbAccessXTimeoutMask',
           'XkbRefreshKeyboardMapping', 'Xutf8LookupString',
           'LeaveNotify', 'sz_xUngrabButtonReq',
           'XkbChangeDeviceInfo', 'ScreenSaverReset', 'Mod1Mask',
           'XSetICFocus', 'XLastKnownRequestProcessed',
           'X_kbGetCompatMap', 'XkbToControl', 'XExtentsOfFontSet',
           'sz_xQueryBestSizeReply', 'XkbPtrBtnAction', '_STDLIB_H',
           'XkbResizeKeyType', 'X_CreateGC', 'XlibDisplayClosing',
           'ELFlagFocus', '_Xmbtowc', 'NotifyNormal',
           'XGetErrorDatabaseText', 'qgcvt', 'XkbCompatGrabModsMask',
           'XkbSymInterpretRec', 'XkbAllExplicitMask', 'XSetClipMask',
           'X_ListFontsWithInfo', 'HostDelete', 'XIMTertiary', 'GXor',
           'XkbRepeatKeysMask', '_XkbAnyEvent', 'CARD8', 'ldiv_t',
           'XGetWindowAttributes', 'XNResourceClass', 'ECHILD',
           '__USE_XOPEN2K', 'VisibilityUnobscured', 'XkbIndicatorRec',
           'N4wait5DOT_255E', 'XGetSubImage', 'XNHotKey',
           'KeyPressMask', 'XFreeGC', 'XkbSetNames',
           'XSetWindowBorderWidth', '__blkcnt_t', 'XkbKeyAliasPtr',
           'ELIBEXEC', 'XChangeSaveSet', '_XUnknownCopyEventCookie',
           'XkbAccessXNotifyEvent', 'strxfrm',
           '__PTHREAD_RWLOCK_INT_FLAGS_SHARED', 'NotifyUngrab',
           'X_kbBell', 'N7_xEvent5DOT_1465DOT_166E', 'AlreadyGrabbed',
           'BadGC', 'XMaxCmapsOfScreen', 'StippleShape', 'ffsl',
           'PropModeAppend', 'XNForeground', 'aligned_alloc',
           '_XFreeMutex_fn', '_XIOErrorFunction', 'XkbSA_LockNoLock',
           '_XkbAnyAction', 'sz_xChangeKeyboardMappingReq',
           'XDrawString16', 'fcvt_r', 'XkbIM_NoAutomatic',
           'XkbLookupKeyBinding', '__OFF_T_MATCHES_OFF64_T', 'a64l',
           'XkbIndicatorStateNotify', 'GCPlaneMask',
           'XkbNumModifiers', 'Button3Mask',
           'XkbExtensionDeviceNotifyMask', '_XkbControlsNotify',
           'XRotateBuffers', 'XkbAX_FeatureFBMask', 'qfcvt',
           'XkbSA_SetValAbsolute', 'XkbPCF_GrabsUseXKBStateMask',
           '_XkbIndicatorChanges', 'X_GetGeometry', '_STRING_H',
           'NotifyNonlinearVirtual', 'XkbComponentListPtr',
           'XLocaleOfFontSet', 'time_t', 'XkbGBN_OtherNamesMask',
           'XOMOrientation_LTR_TTB', 'EISCONN',
           'sz_xGetPointerMappingReply', 'XNPreeditCaretCallback',
           'qfcvt_r', 'XAllocColorCells', '_XkbAction',
           'fsblkcnt64_t', 'XlibDisplayWriting',
           'XkbOD_ConnectionRefused', '__ENUM_IDTYPE_T',
           'XkbLC_BeepOnComposeFail', 'XSetState', 'XIOErrorHandler',
           'XkbNamesNotify', '_xArc', 'sz_xListFontsReply',
           'XFreeCursor', 'calloc', 'XGetWMColormapWindows',
           'NoEventMask', 'XNoExposeEvent',
           'XProcessInternalConnection', 'EALREADY',
           'XMapRequestEvent', '_xPoint', 'XNPreeditStartCallback',
           'X_CirculateWindow', 'N7_xEvent5DOT_1465DOT_151E',
           '__int64_t', 'XClientMessageEvent', 'NorthWestGravity',
           'XkbUseExtension', 'sz_xImageText16Req', 'FreeGCType',
           'X_StoreColors', '_xReq', 'XQueryBestTile',
           'NeedFunctionPrototypes', 'XSetTile', '__LITTLE_ENDIAN',
           '__have_pthread_attr_t', 'PseudoColor',
           'XkbSetDeviceButtonActions', 'XFetchBytes',
           'XIMPreeditNone', 'XProtocolRevision', 'XkbNoShape',
           'XSynchronize', 'XkbSA_SetValMax', 'X_PolySegment',
           'XkbAX_TwoKeysMask', 'X_SetScreenSaver',
           'XkbSA_DeviceValuator', 'X_ChangePointerControl',
           'XNStatusStartCallback', 'XIMStyle', 'xPolyText16Req',
           'xGetKeyboardMappingReply', 'BadCursor', 'XkbGroup1Mask',
           'CWHeight', 'XCopyPlane', 'X_DeleteProperty',
           'xQueryColorsReq', 'XIMPreeditEnable',
           'sz_xCreateWindowReq', 'X_PolyLine',
           '_BITS_PTHREADTYPES_H', 'XkbSetControls', 'sz_xEvent',
           'KBAutoRepeatMode', 'XFontProp', 'XkbKbdDpyStateRec',
           'X_kbGetKbdByName', 'sz_xSetModifierMappingReply',
           'XSetIMValues', 'XkbAXN_SKReject', 'XkbAXN_BKAcceptMask',
           'XFindOnExtensionList', '_XPollfdCacheAdd',
           'XkbResizeKeySyms', 'XListHosts', 'strcmp',
           'XRestackWindows', 'GXorInverted', '__syscall_ulong_t',
           'XkbGBN_TypesMask', 'XReconfigureWMWindow', 'FillSolid',
           'XkbAllAccessXEventsMask', 'XErrorHandler',
           'XkbAXN_SKPressMask', 'ControlMapIndex',
           'XmbDrawImageString', 'XUngrabPointer', 'sz_xVisualType',
           'ENOSPC', 'EBADMSG', 'N4wait5DOT_254E', 'X_DestroyWindow',
           'XWhitePixelOfScreen', 'ELIBBAD', 'X_UninstallColormap',
           'X_ClearArea', 'ERANGE', 'Button4MotionMask',
           'sz_xQueryPointerReply', 'exit', 'XIMHighlight',
           'mbstowcs', '_XkbSwitchScreenAction', '_X11_XLIBINT_H_',
           'XkbGroup1Index', 'PTSPERBATCH', '_SVID_SOURCE',
           'XkbOD_Success', '_XkbDeviceChanges', 'XTextExtents',
           'XFreeEventData', 'strverscmp',
           'N7_xEvent5DOT_1465DOT_153E', 'InputOutput',
           'XkbSA_LatchToLock', 'XChangeGC', '_XIMHotKeyTrigger',
           'EUSERS', 'xChangeSaveSetReq', 'putenv', 'ENODEV',
           'X_kbGetGeometry', 'XIMPreeditStateNotifyCallbackStruct',
           'XSetAuthorization', 'X_GetKeyboardMapping',
           'XRebindKeysym', 'xCopyPlaneReq', '_ERRNO_H',
           '__SIZEOF_PTHREAD_MUTEX_T', 'XKeymapEvent',
           'XkbControlsChangesPtr', 'XkbPhysSymbolsNameMask',
           'XStoreColors', 'N7_xEvent5DOT_1465DOT_147E',
           'XkbAllStateComponentsMask', 'Opposite', 'X_Reply',
           'XkbCompatStateMask', 'XkbMapNotify', '_XkbPtrBtnAction',
           'XPoint', '__sig_atomic_t', 'XkbOD_BadLibraryVersion',
           'CARD32', 'XNewModifiermap', 'xGrabButtonReq',
           '__fsword_t', 'XDisplayOfIM', 'XkbModsRec', 'CursorShape',
           'XkbBellNotifyMask', 'XKeycodeToKeysym', 'XWithdrawWindow',
           'xrgb', 'ESHUTDOWN', 'xCopyColormapAndFreeReq',
           'UnmapNotify', 'XIMStringConversionBuffer',
           'sz_xRecolorCursorReq', 'XkbIndicatorMapNotify',
           '_XEatDataWords', 'XkbApplyVirtualModChanges', 'GXset',
           '_XIMPreeditDrawCallbackStruct', 'ECONNREFUSED',
           'XkbAXN_SKPress', 'xConnSetupPrefix',
           'RevertToPointerRoot', 'xDeletePropertyReq', 'ENOEXEC',
           'EBADF', 'EBADE', 'XkbDeviceLedInfoPtr',
           'N7_xEvent5DOT_1465DOT_150E', 'XNResetState',
           'XScreenOfDisplay', 'XkbKeyboard', '__PDP_ENDIAN', 'EBADR',
           'sz_xArc', 'mkstemp', 'N7_xEvent5DOT_1465DOT_169E',
           'EXDEV', 'XkbBehavior', 'XkbIndicatorPtr', 'XkbNoModifier',
           'xAllocNamedColorReply', 'QueuedAfterReading',
           'XSetForeground', 'XUnregisterIMInstantiateCallback',
           '_SIGSET_NWORDS', 'XkbPerKeyRepeatMask',
           'X_GetScreenSaver', 'XkbIM_UseEffective',
           'XSelectionEvent', 'XkbComponentNamesRec',
           'XAllocColorPlanes', 'AnyPropertyType', 'KeyPress',
           'XMaskEvent', '_XData32', 'sz_xPolyText8Req',
           'NotifyNonlinear', 'xBellReq', 'GXclear',
           'XkbMouseKeysAccelMask', 'XkbMessageAction',
           '_XSetLastRequestRead', 'XNFilterEvents', 'ETOOMANYREFS',
           'XkbKTMapEntryPtr', 'JoinRound', 'XkbAXN_AXKWarningMask',
           'sz_xChangePointerControlReq', 'XkbSetIndicatorMap',
           'PropertyNewValue', 'X_UngrabServer', 'XkbKeySymsMask',
           'XSetAfterFunction', '__WCOREFLAG', 'EINPROGRESS',
           'XkbSA_SetMods', 'XkbSetAutoRepeatRate', 'KEYCODE',
           '__realpath_chk', 'XkbErr_BadDevice',
           'XkbSetServerInternalMods', 'XNStatusDoneCallback',
           'XParseColor', 'xQueryFontReply',
           'N19XClientMessageEvent4DOT_63E', 'strrchr',
           'XmbTextPerCharExtents', 'sz_xListFontsReq',
           'XKeysymToString', 'EL3RST',
           '__SIZEOF_PTHREAD_MUTEXATTR_T', '_POSIX_SOURCE',
           'XkbPCF_DetectableAutoRepeatMask', 'XRaiseWindow',
           'X_kbLatchLockState', 'XkbAccessXKeysMask',
           'XGravityEvent', 'KeyCode', 'XCreatePixmap',
           'XDisplayWidthMM', 'XForceScreenSaver', 'X_CreateColormap',
           '__uint64_t', 'GXinvert', 'OwnerGrabButtonMask',
           'XIMBitmapType', 'GCLastBit', 'XkbAllocControls', 'ulong',
           'BadImplementation', 'XkbSelectEvents', '__clockid_t',
           'ReplayKeyboard', 'strchrnul', 'XNBackgroundPixmap',
           'xlocaledir', 'NeedNestedPrototypes', 'DoGreen', 'abs',
           'XESetErrorString', 'sz_xListHostsReq', 'CoordModeOrigin',
           'XkbNamesMask', 'SetModeInsert', 'XEventsQueued',
           'XIMPreeditState', 'XGetScreenSaver', '_XError',
           'XkbModifierMapMask', 'XkbAccessXFeedbackMask',
           'XwcDrawText', 'xVisualType', 'stpncpy', 'xLookupColorReq',
           'sz_xListFontsWithInfoReq', 'XBitmapPad',
           'XStoreNamedColor', 'XkbAX_SKRejectFBMask',
           'XEventMaskOfScreen', 'XRootWindow', 'XkbCopyKeyTypes',
           'NorthGravity', 'xStoreColorsReq', 'GCTileStipXOrigin',
           'XkbAllocServerMap', 'BUFSIZE', 'xAllocColorReply',
           'XBell', '_XkbMods', 'ERFKILL', 'XESetError', '__mode_t',
           'XMapWindow', 'xInternAtomReply', 'X_PROTOCOL_REVISION',
           'XGetOMValues', 'WhenMapped', 'X_NoOperation',
           'XContextDependentDrawing', 'CirculateNotify',
           'X_CreateGlyphCursor', '_XDeqAsyncHandler',
           'canonicalize_file_name', '_XkbSymInterpretRec',
           'sz_xChangeSaveSetReq', 'X_kbSetMap', 'X_AllocColorPlanes',
           'XkbNewKeyboardNotify', 'XkbGBN_IndicatorMapMask',
           '_ENDIAN_H', 'sz_xListHostsReply', 'XkbSA_SetValCenter',
           '__USE_FORTIFY_LEVEL', 'XkbIndicatorMapNotifyMask', 'Mask',
           'XkbKeyTypesForCoreSymbols', 'XServerVendor',
           '_xQueryFontReply', 'XkbSA_LockGroup', 'sz_xReq', 'pid_t',
           'CWCursor', 'xListHostsReply', 'XkbSI_AutoRepeat',
           'xChangeKeyboardControlReq', 'XkbChangeEnabledControls',
           'XkbAllIndicatorsMask', 'XWhitePixel', 'XNBaseFontName',
           'GravityNotify', 'sz_xGetKeyboardControlReply',
           'XRemoveFromSaveSet', 'XkbLC_FunctionKeys', 'strlen',
           'XNPreeditAttributes', 'XkbExplicitBehaviorMask',
           'GrabSuccess', 'ClipByChildren', 'mkstemp64',
           'FocusChangeMask', 'XkbTypesNameMask', '__fsid_t',
           'XkbLC_ConsumeLookupMods', 'sz_xListFontsWithInfoReply',
           'EAFNOSUPPORT', 'XkbLC_AllControls', 'XkbKeyAliasRec',
           '_XAllocTemp', 'WLNSPERBATCH', 'mrand48_r',
           'X_GetWindowAttributes', 'XSetFillRule', 'BadWindow',
           'X_kbSetControls', 'NotifyGrab', 'AllocAll',
           'sz_xRectangle', 'int8_t', 'XkbChangesRec',
           '_XkbComponentList', 'XVisualIDFromVisual',
           'XDisplayWidth', 'XmbLookupString', '_XPutBackEvent',
           'XkbBell', 'XkbKeypadMask', 'XEDataObject', 'XIMCaretUp',
           'Xutf8DrawString', '__fsfilcnt_t', 'ENOCSI',
           'NeedWidePrototypes', 'jrand48_r', 'XkbSymInterpretPtr',
           '__STDLIB_MB_LEN_MAX', 'basename', 'XParseGeometry', 'ffs',
           '__WCLONE', 'sz_xError', 'XResourceManagerString',
           'XNClientWindow', 'EAGAIN', '__error_t_defined',
           'X_kbGetState', 'FamilyChaos', 'XOpenDisplay',
           'sz_xSetInputFocusReq', 'sz_xChangeActivePointerGrabReq',
           '_LockInfoRec', 'N8_XIMText4DOT_86E', 'XGetFontProperty',
           'XkbClientMapPtr', 'mkostemps64', 'XkbMinLegalKeyCode',
           '_XkbKeyNameRec', 'KeySym', 'X_HAVE_UTF8_STRING',
           '_FillPolyReq', 'XConfigureWindow', 'XNQueryOrientation',
           'XPutBackEvent', 'XkbSA_UseModMapMods', 'sz_xConnSetup',
           'xAllocColorPlanesReply', 'XkbGetControls', 'Mod1MapIndex',
           'XDisplayHeightMM', 'XkbDeviceValuatorAction',
           'sz_xLookupColorReply', 'XkbAllRadioGroupsMask',
           'xGetMotionEventsReply', 'X_CreateWindow',
           'XkbNumRequiredTypes', 'strcoll', 'VisibilityChangeMask',
           '_XkbNamesRec', 'XNextRequest', 'XkbSA_ValOpMask',
           'XLookupChars', 'XIMStatusDataType', 'XGetGCValues',
           'XkbGetCompatMap', 'EDESTADDRREQ', 'XkbInternAtomFunc',
           'XGrabServer', 'sz_xClearAreaReq',
           'XIMStatusDrawCallbackStruct', 'xQueryBestSizeReply',
           '_XkbKeyType', 'XVaCreateNestedList', 'KeyReleaseMask',
           'Complex', 'xPolyFillArcReq', 'sz_xSetDashesReq',
           'EPROTOTYPE', 'XkbExplicitKeyType3Mask', 'XkbChangesPtr',
           'X_GetInputFocus', 'XIMStringConversionRetrieval',
           'X_LookupColor', '__GLIBC_MINOR__',
           'XIMStringConversionRightEdge', 'XkbLC_AlphanumericKeys',
           'XDestroySubwindows', 'strncpy', 'CWBorderPixmap',
           'XkbNumKbdGroups', 'None_', 'X_AllocColorCells',
           'XkbMaxRadioGroups', 'XExtendedMaxRequestSize',
           '__pthread_internal_list', 'DisableScreenInterval', 'labs',
           'XESetWireToEvent', 'xGetKeyboardControlReply',
           'FamilyServerInterpreted', 'XTranslateCoordinates',
           'XkbControlsPtr', 'XListProperties', 'qsort_r',
           'X_UngrabButton', 'xTextElt', 'GXxor', 'XkbKB_RGAllowNone',
           '_XProcessInternalConnection', 'XFreeFontPath',
           'XIMSecondary', 'XStringToKeysym', 'sz_xPolyArcReq',
           '_XkbBellNotify', 'XFontStruct', 'XIMStyles',
           'XGetFontPath', 'XkbKB_Default', 'XkbLatchGroup',
           'GCClipMask', 'qsort', 'XkbFreeControls', 'XDefaultVisual',
           '_XDisplayAtoms', 'pthread_spinlock_t', 'XUngrabButton',
           'sz_xGrabKeyReq', 'XCrossingEvent',
           'xGetWindowAttributesReply', 'GCStipple', 'timespec',
           'Screen', 'GXnor', 'XkbGetDeviceInfoChanges',
           'XButtonEvent', 'XkbAXN_SKRejectMask', 'memset', 'EFAULT',
           'ENOKEY', '_XOM', 'sz_xAllocColorPlanesReq',
           'XMapSubwindows', 'xPixmapFormat', 'XkbControlsNotify',
           'XlibSpecificationRelease', 'VisibilityPartiallyObscured',
           'XOMOrientation_TTB_LTR', 'XkbLC_IgnoreNewKeyboards',
           'LedModeOn', 'X_CopyColormapAndFree', 'X_SendEvent',
           'XDefaultScreen', 'XESetFlushGC', 'Button5MotionMask',
           'XESetWireToError', '_FEATURES_H', 'X_QueryPointer',
           'AsyncBoth', 'ecvt_r', 'XkbSetPerClientControls',
           'XDefaultColormapOfScreen', 'X_GrabServer',
           'sz_xListExtensionsReply', 'X_GrabKeyboard',
           'PropertyChangeMask', 'KeyRelease',
           'XkbLC_ForceLatin1Lookup', 'strtok_r', 'pselect',
           'XkbAX_AllOptionsMask', 'xListPropertiesReply',
           '_XAllocID', 'EPFNOSUPPORT', 'XkbIgnoreExtension',
           'ConfigureNotify', 'INT32', 'X_SetPointerMapping',
           'XkbAnyEvent', '_XOC', '__USE_POSIX199309',
           'X_ReparentWindow', 'XIMOfIC', 'XkbDescRec',
           'XkbSA_AffectDfltBtn', 'XDefineCursor', 'XInitExtension',
           'xAllocColorCellsReq', 'XkbSymInterpMask',
           'xChangePropertyReq', 'XUnsetICFocus', 'mktemp',
           'XkbGroup3Mask', 'XSetTransientForHint', 'quick_exit',
           'X_QueryExtension', 'CARD16', 'XWriteBitmapFile',
           'XBlackPixel', 'Depth', 'xChangeActivePointerGrabReq',
           'ShiftMask', 'Mod2MapIndex', 'MappingModifier',
           '_XkbPtrAction', 'EL2NSYNC', 'FillTiled',
           'xLookupColorReply', 'XChangeKeyboardMapping',
           'N7_xEvent5DOT_1465DOT_168E', 'XFlush', 'strncasecmp',
           '__pthread_mutex_s', '_XLockPtrs', '_XCopyEventCookie',
           'xGetImageReply', 'XwcTextEscapement', 'xCreatePixmapReq',
           'CloseDisplayType', 'LedModeOff', '_XIMHotKeyTriggers',
           'MappingNotify', 'mode_t', 'XAddExtension', 'XDefaultGC',
           'sz_xrgb', '_Exit', 'XYBitmap',
           'N7_xEvent5DOT_1465DOT_152E', 'XkbEvent', 'XSetArcMode',
           'ESTRPIPE', 'lrand48_r', 'xGetModifierMappingReply',
           'CWColormap', 'xCopyAreaReq', 'Mod3Mask', '__loff_t',
           'XkbGBN_AllComponentsMask', 'EDEADLK', 'FamilyInternet6',
           'id_t', 'XIMResetState', 'XSegment', 'JoinBevel', 'strsep',
           'XkbModifierLockMask', 'ControlMask', 'XkbCompatMapPtr',
           'strtod_l', 'Display', '_XkbCompatChanges',
           'XSetWindowColormap', 'XkbSA_ISOLock', 'XGrabKeyboard',
           'XkbAXN_BKReject', 'X_CreateCursor', 'fd_mask',
           '_XkbBehavior', 'XSetErrorHandler',
           'XkbXI_IndicatorNamesMask', 'XAutoRepeatOff', 'mbtowc',
           'XIMStringConversionLine', 'XLeaveWindowEvent',
           'ScreenSaverActive', 'xTranslateCoordsReq',
           'GrabNotViewable', 'XkbXlibControlsImplemented',
           'ExposureMask', 'XLookupKeySym', '_XkbComponentNames',
           '_XIMPreeditCaretCallbackStruct', '__USE_LARGEFILE',
           'XkbSA_DeviceBtn', 'jrand48', 'Xutf8ResetIC', 'strchr',
           'MappingBusy', 'random_data',
           'XkbIndicatorStateNotifyMask', 'memrchr', 'XkbKB_Overlay1',
           'XkbKB_Overlay2', 'XFreeFontInfo', 'xCopyGCReq',
           'XGrabPointer', 'XDisableAccessControl',
           'XQueryBestStipple', 'SelectionRequest', 'X_FreeColormap',
           'XkbAddDeviceLedInfo', 'XSetClipOrigin',
           'sz_xAllowEventsReq', 'X_kbSetCompatMap',
           'XIMPreeditDisable', 'XOMOrientation_Context',
           'XSetICValues', 'XkbAllEventsMask', '__intptr_t', 'P_PID',
           'NorthEastGravity', '__timespec_defined',
           '_STRUCT_TIMEVAL', 'KeyButMask', 'XkbDfltXIClass',
           'XkbGroupLatchMask', 'XSetSelectionOwner',
           '_XkbDeviceValuatorAction', 'CirculateRequest',
           'BadDrawable', '__SIZEOF_PTHREAD_BARRIERATTR_T',
           'SouthWestGravity', 'XkbAllVirtualModsMask',
           'XkbModifierBaseMask', 'ptsname', 'X_ConfigureWindow',
           '_XDefaultError', 'XkbFreeIndicatorMaps',
           'XkbResizeKeyActions', 'ENFILE', 'EREMCHG', 'XKeyEvent',
           'xGetInputFocusReply', '__BIT_TYPES_DEFINED__',
           'X_kbGetControls', 'X_SetDashes', 'XkbNKN_GeometryMask',
           '__u_long', 'XkbMaxLegalKeyCode', 'XKeyPressedEvent',
           'ENOMEM', 'XQLength', 'X_ListProperties', '_xSegment',
           'EOWNERDEAD', 'GCFillStyle', 'CapProjecting',
           'XIMStringConversionFeedback', 'X_PutImage', 'XExtCodes',
           'XInternalConnectionNumbers', 'AnyKey',
           'XkbAX_IndicatorFBMask', 'XkbAllModifiersMask',
           'GrabModeSync', 'u_long', 'Window', '_XFreeEventCookies',
           'sz_xSetCloseDownModeReq', 'X_kbGetNamedIndicator',
           'XIMCallback', 'XRegisterIMInstantiateCallback',
           'XDisplayCells', 'malloc', 'XGrabKey', 'xUngrabKeyReq',
           'KBLedMode', 'XSetFont', 'XkbKB_Lock', 'XPutImage',
           'xQueryExtensionReq', 'PreferBlanking', 'EIO',
           '_XUnknownWireEvent', 'drand48_data', 'error_t',
           'XGetPointerMapping', 'sz_xInternAtomReq', 'GXcopy',
           'XAddToSaveSet', 'XImageByteOrder',
           'XIMStringConversionConcealed', 'XSetFunction',
           '_SYS_CDEFS_H', '_XkbControls', 'XDoesSaveUnders',
           'sz_xSetPointerMappingReply', 'XkbGroup4Index',
           'XCirculateSubwindows', 'xReq', 'XIMStringConversionType',
           'sz_xQueryExtensionReq', 'XkbSI_AnyOfOrNone',
           'XListDepths', 'XkbGeomMaxLabelColors', 'BITS32',
           'xChangeKeyboardMappingReq', 'srandom_r', 'idtype_t',
           'XkbPCF_SendEventUsesXKBState', 'xCreateWindowReq',
           'program_invocation_short_name', 'xSetCloseDownModeReq',
           'YSorted', 'XkbActionMessageEvent', 'xGrabKeyboardReply',
           '_LARGEFILE_SOURCE', 'xHostEntry', 'suseconds_t',
           'mempcpy', 'X_kbGetIndicatorMap', 'XkbTwoLevelIndex',
           'XkbSA_ISONoAffectGroup', 'XWindowEvent', 'xGetImageReq',
           '_XIsEventCookie', 'XkbExplicitVModMapMask', 'mkstemps64',
           'FillStippled', 'CenterGravity', 'XkbMaxMouseKeysBtn',
           'timeval', 'XkbSA_LockDeviceBtn', 'XCreateOC',
           'XkbSymMapRec', 'XkbLibraryVersion',
           'XkbIndicatorNotifyEvent', 'ldiv', 'XNBackground',
           'Xutf8TextExtents', 'XDoesBackingStore', 'XMD_H',
           'NotUseful', 'GXequiv', 'RevertToNone', 'ENOLCK',
           'XkbSA_ValScaleMask', 'KBLed', 'Mod4Mask',
           'XkbGetAtomNameFunc', 'Button3', 'Button2', 'Button1',
           'XkbXI_IndicatorsMask', 'Button5', 'Button4',
           'X_SetModifierMapping', 'register_t', 'xGetPropertyReq',
           'XCreateImage', 'XReadBitmapFileData', 'sz_xChangeModeReq',
           'XImage', 'XkbSI_AnyOf', 'sz_xPolyPointReq', 'memmove',
           'XIMHotKeyState', 'XFetchBuffer', 'X_SetClipRectangles',
           'ClientMessage', 'GCBackground', 'Font',
           'XkbAllocKeyboard', 'FillOpaqueStippled',
           'AutoRepeatModeOff', 'GrabFrozen',
           'XkbGBN_ClientSymbolsMask', 'XFilterEvent', '_XGetRequest',
           'XkbResizeDeviceButtonActions', 'mrand48',
           'xListFontsReply', '_XkbExtensionDeviceNotify',
           'xChangeGCReq', 'XCopyArea', 'X_PolyText16',
           'GXandInverted', 'XkbSlowKeysMask', 'XkbControlsMask',
           'RetainPermanent', 'XNQueryICValuesList', '__off_t',
           'sz_xTranslateCoordsReply', 'XCirculateEvent',
           'XNOrientation', 'xSetDashesReq', 'CWBackPixel',
           'XKeyReleasedEvent', 'XColor', 'XFontSet', 'ENOBUFS',
           'XkbSetNamedDeviceIndicator', 'XSelectInput',
           'XLockDisplay', 'XSetClipRectangles', 'BadValue',
           'XkbCompatChangesRec', 'ResizeRequest',
           'XkbXI_ButtonActionsMask', 'N7_xEvent5DOT_1465DOT_155E',
           'Button2Mask', 'GCFont', 'XkbGroupAction', '__USE_BSD',
           'XEnableAccessControl', 'rindex', 'bsearch', 'XNArea',
           'XPending', 'LSBFirst', 'XListInstalledColormaps',
           'XkbSetXlibControls', 'XkbAnyGroup', 'xImageTextReq',
           'GraphicsExpose', 'BeforeFlushType', '_XSend',
           'MotionNotify', 'XIMStringConversionCallbackStruct',
           'XkbChangeTypesOfKey', 'XkbAXN_BKRejectMask', 'memccpy',
           'XGenericEvent', 'errno', 'xConvertSelectionReq',
           'xSetAccessControlReq', 'X_GetMotionEvents',
           'XkbIM_UseLatched', 'FRCTSPERBATCH',
           'XkbApplyCompatMapToKey', 'sz_xWindowRoot',
           'sz_xPropIconSize', 'sz_xSetAccessControlReq',
           'PointerRoot', 'X_GrabPointer', 'X_UngrabPointer',
           'XkbIgnoreLockModsMask', 'XkbSA_DfltBtnAbsolute', 'atoi',
           'ENOTNAM', 'xGrabPointerReply', 'XIMHotKeyStateOFF',
           'XkbExplicitKeyTypesMask', 'ESPIPE', 'erand48',
           'XkbFreeComponentList', 'Button1MotionMask', 'BOOL',
           'CapRound', 'EROFS', 'XkbAudibleBellMask', 'blkcnt64_t',
           'XSelectionRequestEvent', 'XNLineSpace', 'XDisplayName',
           'XlibDisplayPrivSync', 'NotifyPointer', 'XkbServerMapRec',
           'Above', 'X_kbSetNamedIndicator', '_ALLOCA_H',
           'xSetPointerMappingReply', 'sz_xImageText8Req',
           'xImageText8Req', 'xCreateGlyphCursorReq', 'X_kbSetNames',
           'N28_XIMStatusDrawCallbackStruct4DOT_91E', 'setenv',
           'XNSpotLocation', 'XNGeometryCallback', 'XTHREADS',
           'ENAVAIL', 'XIMStringConversionWrapped',
           'XNVisiblePosition', 'XkbMaxKeyCount', 'XkbAXN_BKAccept',
           'XNResourceName', 'XNDirectionalDependentDrawing',
           '_XkbPtrDfltAction', 'mkostemp64', 'sz_xPolyTextReq',
           'LineSolid', '__socklen_t', 'X_SetInputFocus', 'EOVERFLOW',
           'P_ALL', 'XYPixmap', '_XExtension', 'XkbGetDeviceLedInfo',
           'XkbOD_BadServerVersion', '_XkbNameChanges', 'funcs',
           'XkbKeyNamePtr', 'xStoreNamedColorReq', 'XFillPolygon',
           '_ATFILE_SOURCE', 'XHeightMMOfScreen', 'XFreePixmap',
           'XSetIconName', 'Time', 'FocusOut', 'X_MapSubwindows',
           'XIMStringConversionSubstitution', 'ENAMETOOLONG',
           'NotifyVirtual', 'XGetImage', 'XkbGroup3Index',
           'XkbExplicitKeyType1Mask', 'XkbIndicatorMapMask',
           'XkbNumIndicators', 'Button4Mask', 'XkbGBN_CompatMapMask',
           '_XFreeFuncRec', '__SIZEOF_PTHREAD_CONDATTR_T',
           'XkbXI_IndicatorStateMask', 'XOMOrientation_TTB_RTL',
           'XFreeColormap', '_XkbKTMapEntry', 'Button5Mask',
           'XkbLockGroup', 'XFillRectangle', 'erand48_r',
           'X_kbPerClientFlags', 'XkbGetMapChanges', 'ParentRelative',
           'EMSGSIZE', 'XkbSwitchScreenAction', 'X_PROTOCOL',
           'sz_xConvertSelectionReq', 'xGrabKeyboardReq',
           'xUngrabButtonReq', 'False_', 'sz_xSetSelectionOwnerReq',
           'EREMOTEIO', 'XkbXINone', 'X_kbGetIndicatorState',
           'xSetModifierMappingReply', '_XkbKeyAliasRec',
           '_BITS_TYPESIZES_H', 'XNRequiredCharSet',
           'XkbGetKeyActions', 'XkbDeviceInfoPtr',
           'XkbPCF_AutoResetControlsMask', 'XkbSA_MessageOnPress',
           'X_CopyGC', 'XIMAbsolutePosition', 'CurrentTime',
           '__errno_location', 'XSetPlaneMask',
           'XkbActionMessageLength', '_XDefaultWireError',
           'XkbComputeEffectiveMap', 'strcasestr',
           'XkbExplicitKeyType2Mask', '__ctype_get_mb_cur_max',
           'XGetMotionEvents', 'XkbSA_ISONoAffectCtrls',
           'N7_xEvent5DOT_1465DOT_154E', 'index', 'ELFlagSameScreen',
           'XFree', '_XUnknownWireEventCookie', 'ENOANO',
           'XkbKbdDpyStatePtr', 'XCharStruct', 'EUCLEAN',
           'XkbSetAutoResetControls', 'XkbMaxSymsPerKey',
           'XNContextualDrawing', 'XFillRectangles', 'BadFont',
           'XGetTransientForHint', 'XkbOpenDisplay',
           '_XkbGroupAction', 'ENOTRECOVERABLE', 'XESetFreeGC',
           '_XkbAccessXNotify', 'XNPreeditState', 'XFontSetExtents',
           '__lldiv_t_defined', '__SIZEOF_PTHREAD_BARRIER_T',
           '_XStoreEventCookie', 'DestroyAll', 'XkbNoShiftLevel',
           'XNHotKeyState', 'sz_xQueryColorsReq', '_XFlushGCCache',
           'XUngrabKey', 'N7_xEvent5DOT_1465DOT_172E', 'XwcTextItem',
           'sz_xCreateColormapReq', '_XkbComponentName',
           '_XkbDeviceBtnAction', 'XkbSetDeviceLedInfo',
           'XkbPtrDfltAction', 'CWWidth', '__stpncpy', '_XImage',
           'XIMPreserveState', 'XDrawText', 'EPIPE', '_XRead',
           'sz_xPolyLineReq', 'XConnectionNumber', 'EINTR', 'EBFONT',
           '_XkbNamesNotify', 'XkbErr_BadClass', 'XkbKeyTypesMask',
           'sz_xGetKeyboardMappingReq', 'XCreateFontSet',
           'XkbSA_SetGroup', 'EADDRINUSE', 'fsid_t', '__WNOTHREAD',
           'KBBellPitch', 'sz_xReparentWindowReq', '_XEventsQueued',
           'X_RecolorCursor', 'fsfilcnt64_t', 'XSetWMColormapWindows',
           'XkbExplicitComponentsMask', 'XQueryColor',
           'XKeyboardControl', 'XAddHost', 'XkbGBN_GeometryMask',
           '_XGetAsyncReply', 'XWindowChanges', '__fsblkcnt64_t',
           'XBitmapBitOrder', 'XkbIndicatorNamesMask',
           'XkbAccessXNotifyMask', 'ENOENT', '__USE_XOPEN_EXTENDED',
           'XlibDisplayProcConni', 'strtold', 'timer_t',
           'XkbGetAutoRepeatRate', 'ECOMM', 'mkostemps',
           'X_ChangeProperty', 'XkbAllActionMessagesMask', 'abort',
           'XNOMAutomatic', 'xGetMotionEventsReq', 'XSetCommand',
           'XkbInitCanonicalKeyTypes', 'X_SetFontPath', 'Pixmap',
           'ENOTEMPTY', 'sz_xDepth', 'XIconifyWindow',
           'XkbIM_UseCompat', 'XHostAddress', 'XDrawArc',
           '_XConnectionInfo', 'sz_xQueryTextExtentsReply', 'strtoll',
           'X_QueryColors', '_XFreeTemp', '_XEnq', '__wcstombs_chk',
           'XQueryColors', '__stpncpy_chk', 'sz_xTranslateCoordsReq',
           'XCreateGlyphCursor', '__wctomb_chk', 'int16_t',
           'XUngrabKeyboard', 'XOMOrientation', 'on_exit', 'xPoint',
           'XRemoveHost', 'XDrawPoint', '_XExtData', 'strncat',
           'WEXITED', 'XkbExplicitAutoRepeatMask', 'SetModeDelete',
           'key_t', '__USE_ISOC95', 'XOC', 'xCreateGCReq',
           'XkbAllNewKeyboardEventsMask', 'XOM', 'GContext',
           '_XFetchEventCookie', '__USE_ISOC99', 'XkbLookupModsMask',
           'X_SetCloseDownMode', 'EMEDIUMTYPE', 'X_kbGetMap',
           'sz_xSegment', 'WRCTSPERBATCH',
           'XkbNewKeyboardNotifyEvent', 'ZRCTSPERBATCH',
           'GenericEvent', 'X_PolyFillArc', 'XDrawSegments',
           'ssize_t', 'fcvt', 'XkbClientMapMask', 'xRectangle',
           'EPROTONOSUPPORT', 'XMoveWindow',
           'sz_xPolyFillRectangleReq', 'XChangeWindowAttributes',
           'LowerHighest', 'XWidthOfScreen', 'ETIME', 'AllocNone',
           'ptsname_r', 'XkbDF_DisableLocks', '_XEvent',
           '__USE_XOPEN', '_xRectangle', 'X_TranslateCoords',
           '_XkbServerMapRec', 'XSync', 'Colormap',
           'X_GetPointerControl', '__syscall_slong_t',
           'sz_xConnSetupPrefix', 'XIMValuesList', 'XIfEvent',
           'XkbEventCode', 'XDrawImageString16',
           'XkbGetKeyVirtualModMap', 'XRotateWindowProperties',
           'XkbSA_ActionMessage', 'sz_xChangeKeyboardControlReq',
           '__USE_ATFILE', 'srandom', 'XkbAX_LatchToLockMask',
           'XSetIOErrorHandler', 'Mod5MapIndex', 'XIMPreviousLine',
           '__int32_t', 'XIMForwardWord', 'EIDRM',
           'sz_xCopyColormapAndFreeReq', 'XkbClampIntoRange',
           '_XRead32', 'XNAreaNeeded', 'EPERM', 'XkbStateNotify',
           'xCreateColormapReq', 'Mod5Mask', 'clock_t', 'xTimecoord',
           'XkbSA_IgnoreVal', 'XkbSA_MovePtr',
           'N7_xEvent5DOT_1465DOT_171E', 'X_GetModifierMapping',
           'XCreateIC', 'XQueryBestCursor', 'xImageText16Req',
           'sz_xAllocNamedColorReply', 'XLoadFont',
           'XIMPreeditDrawCallbackStruct', 'xKeymapEvent',
           '_XTextHeight16', 'XGetEventData', 'PointerMotionMask',
           'XCirculateRequestEvent', 'XLowerWindow', 'EvenOddRule',
           'xPolyTextReq', 'XkbAlphabeticIndex', 'INT16',
           'XkbSetAtomFuncs', 'xChangeWindowAttributesReq',
           'XDisplayMotionBufferSize', 'PointerMotionHintMask',
           'sz_xPixmapFormat', 'XkbMapNotifyEvent', 'XTextItem',
           '_XIMStatusDrawCallbackStruct', 'ELIBMAX',
           '_POSIX_C_SOURCE', 'EMULTIHOP', 'XmbDrawText',
           'XkbIgnoreGroupLockMask', 'XNVaNestedList',
           'xConfigureWindowReq', 'XUnmapSubwindows',
           'XCirculateSubwindowsDown', 'XkbIM_UseLocked',
           '__USE_SVID', 'XGCValues', 'xListFontsWithInfoReq',
           'XkbKB_Permanent', 'N7_xEvent5DOT_1465DOT_157E',
           'XListFontsWithInfo', '_XReply', 'xPolyRectangleReq',
           'system', 'BadColor', 'strcasecmp', '__daddr_t',
           'XkbGroupsWrapMask', 'ECONNABORTED', 'XFreeFontSet',
           'X_PolyFillRectangle', 'Success', 'XFreeFont',
           '__SIZEOF_PTHREAD_RWLOCK_T', 'NotifyInferior', '__caddr_t',
           'XkbFreeNames', 'sz_xAllocColorReply', 'XkbFreeDeviceInfo',
           'xSetClipRectanglesReq', 'XkbGroup2Index', 'XIMStatusArea',
           'XEventSize', 'XQueryTextExtents16', 'RevertToParent',
           'XkbNumberEvents', 'XkbStateNotifyMask', 'XkbMinorVersion',
           'XkbCompatMapRec', '__USE_EXTERN_INLINES',
           '__SIZEOF_PTHREAD_COND_T', 'X_QueryFont', 'XQueryTree',
           'EDOM', 'XResizeWindow', 'XkbStateNotifyEvent',
           'XkbServerMapPtr', 'XIMUnderline', 'XkbAX_BKRejectFBMask',
           'sz_xBellReq', 'XkbGroupLockMask', 'XkbTranslateKeyCode',
           'XCreateColormap', 'XkbIndicatorChangesPtr',
           'XkbAllocIndicatorMaps', 'sz_xGrabPointerReq', 'JoinMiter',
           '_XOPEN_SOURCE_EXTENDED', 'VisibilityFullyObscured',
           'ptrdiff_t', 'XIMLineStart', 'XkbErr_BadId',
           'XkbSA_LatchMods', 'gcvt', 'sz_xGetPointerControlReply',
           'LockMask', 'EKEYREVOKED', 'MappingKeyboard',
           '__fdelt_chk', 'EL2HLT', 'GCFunction', 'XInternAtom',
           '_XAsyncErrorHandler', 'LockInfoPtr', 'XFreeExtensionList',
           'sz_xSetScreenSaverReq', 'XVendorRelease', '_BSD_SOURCE',
           'XkbBellNotify', 'xGrabKeyReq', 'X_AllocNamedColor',
           '_XFreeExtData', 'XkbSA_Terminate',
           'XNSeparatorofNestedList', 'XUnmapWindow',
           'XkbNameChangesPtr', 'sz_xKeymapEvent', 'Nonconvex',
           '_XkbControlsChanges', '__USE_LARGEFILE64',
           'xQueryPointerReply', 'strtol', 'XkbMajorVersion',
           'XBufferOverflow', 'strtod', 'XIMText', 'strtof',
           'XkbIM_NoExplicit', 'XkbComponentNamesPtr',
           'XkbKeyActionsMask', 'strtoq', 'XkbSA_SetPtrDflt',
           'XQueryKeymap', 'XkbAllocDeviceInfo', 'BadAlloc',
           'XScreenResourceString', 'strxfrm_l', 'Unsorted',
           'XkbGeomMaxPriority', 'memcpy', 'X_FreePixmap',
           'XSetOMValues', 'X_UngrabKeyboard',
           'sz_xAllocColorCellsReply', 'XCloseOM',
           'XkbSA_MessageOnRelease', 'XmbDrawString', 'EKEYEXPIRED',
           'xQueryTextExtentsReply', 'sz_xCirculateWindowReq',
           'GXorReverse', 'XMotionEvent', '_XPollfdCacheInit',
           'XkbAllMapComponentsMask', '__ssize_t', 'gid_t',
           'CWBorderWidth', 'program_invocation_name', 'XkbForceBell',
           'lcong48_r', 'XkbAX_FBOptionsMask', 'XkbSA_LatchGroup',
           'EUNATCH', 'xQueryKeymapReply', 'XCreateSimpleWindow',
           '__sigset_t', 'XQueryExtension', 'xSetScreenSaverReq',
           'XIMHotKeyStateON', 'XFreeStringList',
           'xGetScreenSaverReply', 'XTextItem16', 'xPolyText8Req',
           'sz_xQueryKeymapReply', 'N7_xEvent5DOT_146E', 'X_Error',
           'AutoRepeatModeOn', 'XGetOCValues', 'XMapRaised',
           'XkbCompatMapMask', 'XDefaultGCOfScreen', 'XmbTextItem',
           'CWSaveUnder', 'SyncKeyboard', 'ETIMEDOUT', 'XkbAllGroups',
           '_XFlush', 'ReplayPointer', 'ushort', 'TrueColor',
           'XCheckMaskEvent', 'clockid_t',
           'N7_xEvent5DOT_1465DOT_1725DOT_1735DOT_175E',
           'XkbAllBellEventsMask', 'XIMLineEnd',
           'sz_xCreateGlyphCursorReq', 'XlibDisplayReadEvents',
           'caddr_t', 'XkbSA_ClearLocks', 'X_ChangeSaveSet', 'ENXIO',
           'xListFontsWithInfoReply', 'sz_xCharInfo', 'XUnloadFont',
           'XTextWidth', '_XrmHashBucketRec', '_XAllocScratch',
           'XkbGroupStateMask', '__USE_MISC', 'DoRed',
           'N7_xEvent5DOT_1465DOT_170E', '_XGetHostname', 'xReply',
           'FlushGCType', 'getsubopt', 'XESetEventToWire',
           '__compar_d_fn_t', 'sz_xGetInputFocusReply',
           'XkbXI_KeyboardsMask', 'ENOSR', 'X_ListFonts',
           'XkbGeometryPtr', 'ELIBSCN',
           'N7_xEvent5DOT_1465DOT_1725DOT_1735DOT_174E',
           'XwcTextExtents', 'XlibDisplayReply',
           '_XkbStateNotifyEvent', 'XUninstallColormap',
           '__PTHREAD_MUTEX_HAVE_PREV', 'X_WarpPointer',
           'XkbListComponents', 'XIMStringConversionPosition',
           '_BITS_BYTESWAP_H', 'EBADSLT', 'XkbNamesNotifyEvent',
           '_XkbDesc', 'XIMProc', 'ZPixmap', '_XkbCompatMapRec',
           'XSendEvent', 'XIMVisibleToForward', '_SYS_SYSMACROS_H',
           'X_RotateProperties', 'XkbNamesNotifyMask', 'XDrawLine',
           'drand48', 'XkbNamesPtr', 'XkbCtrlsAction',
           'XkbPCF_AllFlagsMask', 'random_r', 'XGrabButton',
           'StaticGray', 'sz_xDeletePropertyReq', 'XkbLC_Hidden',
           '__USE_POSIX199506', 'cfree', '__BIG_ENDIAN', 'srand',
           'X_kbSetDeviceInfo', 'EACCES', 'MappingPointer',
           'XkbSelectEventDetails', 'XSetBackground',
           'GrabInvalidTime', 'sz_xGetMotionEventsReq',
           'XkbAnyAction', '_XkbCtrlsAction',
           'sz_xQueryTextExtentsReq', 'Expose', 'strcasecmp_l',
           'XDeleteProperty', '_XQEvent', 'XkbAlphabeticMask',
           'sz_xChangeGCReq', 'X_UngrabKey', 'PropModePrepend',
           '__strtok_r', 'XNFontInfo', 'xQueryColorsReply', '__ino_t',
           'TopIf', 'XkbAllCompatMask', 'Drawable', 'XIMCaretStyle',
           'XkbSetCompatMap', 'ENODATA', 'StructureNotifyMask',
           'XkbClientMapRec', 'WCONTINUED', 'drand48_r',
           'XkbRGNamesMask', 'XkbXI_AllFeaturesMask',
           'sz_xInternAtomReply', 'XNCursor', 'TileShape', 'xArc',
           'rand_r', 'WSTOPPED', 'X_SetAccessControl',
           'XkbCompatMapNotify', 'XkbMaxKeyTypes', 'XkbChangeNames',
           'ESOCKTNOSUPPORT', '_XtransConnInfo', '_XIOError',
           'XNextEvent', 'FontChange', 'XDrawImageString', 'atoll',
           '_XkbIndicatorMapRec', 'P_PGID', 'CURSORFONT',
           'XkbKeycodeToKeysym', 'NotifyWhileGrabbed',
           'XkbNoModifierMask', '__ino64_t', 'XEHeadOfExtensionList',
           'XkbFreeServerMap', 'Below', 'EEXIST', 'XkbAddKeyType',
           'sz_xPoint', 'sz_xGetKeyboardMappingReply', 'EPROTO',
           '_SYS_SELECT_H', 'XkbKeyTypePtr', 'sz_xTimecoord',
           'sz_xSetPointerMappingReq', '_XIMStringConversionText',
           '_ISOC95_SOURCE', 'XkbActionMessageMask', 'X_FreeColors',
           'strcpy', 'xSetSelectionOwnerReq', '__compar_fn_t',
           'XIMStringConversionText', 'XkbAccessXNotify',
           'XWindowAttributes', 'fd_set', '__fdelt_warn', 'llabs',
           'CWBackPixmap', '__clock_t_defined', '__pid_t',
           '_XkbActionMessage', 'XResizeRequestEvent',
           'PropModeReplace', 'XUSE_MTSAFE_API',
           'XNR6PreeditCallback', '__SYSCALL_WORDSIZE',
           'xRotatePropertiesReq', 'WindingRule',
           'XkbExtensionDeviceNotifyEvent', 'XkbSA_RedirectKey',
           'xReparentWindowReq', 'XkbGetXlibControls', 'xFalse',
           'XkbChangeMap', 'int64_t', '_XkbSymMapRec',
           'sz_xListInstalledColormapsReply', 'XkbGetMap',
           'KeymapStateMask', 'XkbGetKeyboardByName', 'strtof_l',
           'XGetGeometry', 'XkbAX_SKAcceptFBMask', 'INT64', 'xTrue',
           'EADDRNOTAVAIL', 'EADV', 'ENOSYS', 'XSetCloseDownMode',
           'N7_xEvent5DOT_1465DOT_167E', 'BottomIf', 'BadPixmap',
           'XkbAX_SKReleaseFBMask', 'ZLNSPERBATCH', 'XkbSA_LockMods',
           'XIMStringConversionOperation', 'XIMStatusCallbacks',
           'GXand', 'XkbKeyNameLength', 'XkbSI_LockingKey',
           '_ISOC11_SOURCE', 'XrmInitialize', 'X_PolyArc',
           'XkbIndicatorMapRec', 'xColorItem', 'X_StoreNamedColor',
           'sz_xQueryExtensionReply', 'XkbModifierStateMask',
           '__USE_UNIX98', 'dev_t', 'XRecolorCursor',
           'XkbSA_XFree86Private', '__gid_t', 'XCreateFontCursor',
           'XIMPreeditCaretCallbackStruct', 'XkbAllBooleanCtrlsMask',
           '__locale_struct', 'XkbUpdateActionVirtualMods',
           'sz_xFreeColorsReq', 'XkbAX_SKOptionsMask', 'BITS16',
           'XNColormap', 'l64a', 'XIMReverse', 'XDrawText16',
           'sz_xChangeWindowAttributesReq', 'getenv', 'XkbAction',
           'XkbFreeClientMap', 'locale_t', 'sz_xForceScreenSaverReq',
           'CopyFromParent', 'XkbOneLevelMask', 'GCLineStyle',
           '_XIMText', 'KeymapNotify', 'XkbSI_AllOf',
           'XkbAllServerInfoMask', 'QueuedAlready', 'AsyncKeyboard',
           'XkbOverlay1Mask', 'strspn', 'xPolyArcReq',
           'XkbLC_ModifierKeys', 'XkbGetDeviceInfo', '_XWireToEvent',
           'X_PolyPoint', 'XkbLC_AlwaysConsumeShiftAndLock',
           'XReparentWindow', 'XErrorEvent', 'XkbKB_OpMask',
           'strndup', 'StaticGravity', 'sz_xCopyPlaneReq',
           'FontLeftToRight', '_XInternalAsync',
           'XwcTextPerCharExtents', 'sz_xGetPropertyReq', 'ENETDOWN',
           'N7_xEvent5DOT_1465DOT_159E', 'XWarpPointer',
           'XkbVirtualModNamesMask', 'XNStatusDrawCallback',
           'XIMIsInvisible', 'XDefaultDepth', 'XDestroyWindow',
           'CreateGCType', 'XkbGroup2Mask', 'EDOTDOT', 'EBADFD',
           'XDisplayHeight', 'NotifyAncestor', 'XESetCreateFont',
           'DoBlue', 'xClearAreaReq', 'xSetPointerMappingReq',
           'N24_XIMStringConversionText4DOT_87E', 'ENOMEDIUM',
           'XkbLC_Default', 'XActivateScreenSaver', 'XkbStateRec',
           'XIMCaretDown', 'XmbTextEscapement', 'XSetLocaleModifiers',
           'XkbNKN_KeycodesMask', '_XReadPad', 'XkbGeomMaxColors',
           'XkbAllXIClasses', 'N7_xEvent5DOT_1465DOT_160E',
           'GCDashOffset', 'XSetSubwindowMode', 'EXIT_FAILURE',
           '_XUnknownNativeEvent', 'X_kbSetDebuggingFlags',
           'xAllocColorReq', '_xEvent']
