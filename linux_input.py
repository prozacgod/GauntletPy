# parts of this file were inherited from evdev.py by Micah Dowty
# many thanks!
from __future__ import print_function, with_statement, absolute_import, division, unicode_literals

import platform
import struct, sys, os, time
from fcntl import ioctl
import select

class EnumDict:
	def __init__(self, numberMap):
		self.numberMap = {}
		self.nameMap = {}
		for key, value in numberMap.iteritems():
			self.numberMap[key] = value
			self.nameMap[value] = key

	def fromString(self, name):
		return self.nameMap.get(name, name)

	def fromNumber(self, num):
		return self.numberMap.get(num, num)
		
	def __getitem__(self, index):
		if (type(index) == int):
			return self.fromNumber(index)
		else:
			return self.fromString(index)


typeMap = EnumDict({
    0x00: "EV_SYN",
    0x01: "EV_KEY",
    0x02: "EV_REL",
    0x03: "EV_ABS",
    0x04: "EV_MSC",
    0x05: "EV_SW",
    0x11: "EV_LED",
    0x12: "EV_SND",
    0x14: "EV_REP",
    0x15: "EV_FF",
    0x16: "EV_PWR",
    0x17: "EV_FF_STATUS",
})

EV_MAX =  0x1f
EV_CNT = (EV_MAX+1)


codeMaps = {
	"EV_KEY": EnumDict({
		0 : "KEY_RESERVED",
		1 : "KEY_ESC",
		2 : "KEY_1",
		3 : "KEY_2",
		4 : "KEY_3",
		5 : "KEY_4",
		6 : "KEY_5",
		7 : "KEY_6",
		8 : "KEY_7",
		9 : "KEY_8",
		10 : "KEY_9",
		11 : "KEY_0",
		12 : "KEY_MINUS",
		13 : "KEY_EQUAL",
		14 : "KEY_BACKSPACE",
		15 : "KEY_TAB",
		16 : "KEY_Q",
		17 : "KEY_W",
		18 : "KEY_E",
		19 : "KEY_R",
		20 : "KEY_T",
		21 : "KEY_Y",
		22 : "KEY_U",
		23 : "KEY_I",
		24 : "KEY_O",
		25 : "KEY_P",
		26 : "KEY_LEFTBRACE",
		27 : "KEY_RIGHTBRACE",
		28 : "KEY_ENTER",
		29 : "KEY_LEFTCTRL",
		30 : "KEY_A",
		31 : "KEY_S",
		32 : "KEY_D",
		33 : "KEY_F",
		34 : "KEY_G",
		35 : "KEY_H",
		36 : "KEY_J",
		37 : "KEY_K",
		38 : "KEY_L",
		39 : "KEY_SEMICOLON",
		40 : "KEY_APOSTROPHE",
		41 : "KEY_GRAVE",
		42 : "KEY_LEFTSHIFT",
		43 : "KEY_BACKSLASH",
		44 : "KEY_Z",
		45 : "KEY_X",
		46 : "KEY_C",
		47 : "KEY_V",
		48 : "KEY_B",
		49 : "KEY_N",
		50 : "KEY_M",
		51 : "KEY_COMMA",
		52 : "KEY_DOT",
		53 : "KEY_SLASH",
		54 : "KEY_RIGHTSHIFT",
		55 : "KEY_KPASTERISK",
		56 : "KEY_LEFTALT",
		57 : "KEY_SPACE",
		58 : "KEY_CAPSLOCK",
		59 : "KEY_F1",
		60 : "KEY_F2",
		61 : "KEY_F3",
		62 : "KEY_F4",
		63 : "KEY_F5",
		64 : "KEY_F6",
		65 : "KEY_F7",
		66 : "KEY_F8",
		67 : "KEY_F9",
		68 : "KEY_F10",
		69 : "KEY_NUMLOCK",
		70 : "KEY_SCROLLLOCK",
		71 : "KEY_KP7",
		72 : "KEY_KP8",
		73 : "KEY_KP9",
		74 : "KEY_KPMINUS",
		75 : "KEY_KP4",
		76 : "KEY_KP5",
		77 : "KEY_KP6",
		78 : "KEY_KPPLUS",
		79 : "KEY_KP1",
		80 : "KEY_KP2",
		81 : "KEY_KP3",
		82 : "KEY_KP0",
		83 : "KEY_KPDOT",
		85 : "KEY_ZENKAKUHANKAKU",
		86 : "KEY_102ND",
		87 : "KEY_F11",
		88 : "KEY_F12",
		89 : "KEY_RO",
		90 : "KEY_KATAKANA",
		91 : "KEY_HIRAGANA",
		92 : "KEY_HENKAN",
		93 : "KEY_KATAKANAHIRAGANA",
		94 : "KEY_MUHENKAN",
		95 : "KEY_KPJPCOMMA",
		96 : "KEY_KPENTER",
		97 : "KEY_RIGHTCTRL",
		98 : "KEY_KPSLASH",
		99 : "KEY_SYSRQ",
		100 : "KEY_RIGHTALT",
		101 : "KEY_LINEFEED",
		102 : "KEY_HOME",
		103 : "KEY_UP",
		104 : "KEY_PAGEUP",
		105 : "KEY_LEFT",
		106 : "KEY_RIGHT",
		107 : "KEY_END",
		108 : "KEY_DOWN",
		109 : "KEY_PAGEDOWN",
		110 : "KEY_INSERT",
		111 : "KEY_DELETE",
		112 : "KEY_MACRO",
		113 : "KEY_MUTE",
		114 : "KEY_VOLUMEDOWN",
		115 : "KEY_VOLUMEUP",
		116 : "KEY_POWER",
		117 : "KEY_KPEQUAL",
		118 : "KEY_KPPLUSMINUS",
		119 : "KEY_PAUSE",
		120 : "KEY_SCALE",
		121 : "KEY_KPCOMMA",
		122 : "KEY_HANGEUL",
		# KEY_HANGEUL : "KEY_HANGUEL",   not sure how to handle this..??  if you need it figure it out on your own :D
		123 : "KEY_HANJA",
		124 : "KEY_YEN",
		125 : "KEY_LEFTMETA",
		126 : "KEY_RIGHTMETA",
		127 : "KEY_COMPOSE",
		128 : "KEY_STOP",
		129 : "KEY_AGAIN",
		130 : "KEY_PROPS",
		131 : "KEY_UNDO",
		132 : "KEY_FRONT",
		133 : "KEY_COPY",
		134 : "KEY_OPEN",
		135 : "KEY_PASTE",
		136 : "KEY_FIND",
		137 : "KEY_CUT",
		138 : "KEY_HELP",
		139 : "KEY_MENU",
		140 : "KEY_CALC",
		141 : "KEY_SETUP",
		142 : "KEY_SLEEP",
		143 : "KEY_WAKEUP",
		144 : "KEY_FILE",
		145 : "KEY_SENDFILE",
		146 : "KEY_DELETEFILE",
		147 : "KEY_XFER",
		148 : "KEY_PROG1",
		149 : "KEY_PROG2",
		150 : "KEY_WWW",
		151 : "KEY_MSDOS",
		152 : "KEY_COFFEE",
		#  KEY_COFFEE : "KEY_SCREENLOCK",   TWO names for one code???
		153 : "KEY_DIRECTION",
		154 : "KEY_CYCLEWINDOWS",
		155 : "KEY_MAIL",
		156 : "KEY_BOOKMARKS",
		157 : "KEY_COMPUTER",
		158 : "KEY_BACK",
		159 : "KEY_FORWARD",
		160 : "KEY_CLOSECD",
		161 : "KEY_EJECTCD",
		162 : "KEY_EJECTCLOSECD",
		163 : "KEY_NEXTSONG",
		164 : "KEY_PLAYPAUSE",
		165 : "KEY_PREVIOUSSONG",
		166 : "KEY_STOPCD",
		167 : "KEY_RECORD",
		168 : "KEY_REWIND",
		169 : "KEY_PHONE",
		170 : "KEY_ISO",
		171 : "KEY_CONFIG",
		172 : "KEY_HOMEPAGE",
		173 : "KEY_REFRESH",
		174 : "KEY_EXIT",
		175 : "KEY_MOVE",
		176 : "KEY_EDIT",
		177 : "KEY_SCROLLUP",
		178 : "KEY_SCROLLDOWN",
		179 : "KEY_KPLEFTPAREN",
		180 : "KEY_KPRIGHTPAREN",
		181 : "KEY_NEW",
		182 : "KEY_REDO",
		183 : "KEY_F13",
		184 : "KEY_F14",
		185 : "KEY_F15",
		186 : "KEY_F16",
		187 : "KEY_F17",
		188 : "KEY_F18",
		189 : "KEY_F19",
		190 : "KEY_F20",
		191 : "KEY_F21",
		192 : "KEY_F22",
		193 : "KEY_F23",
		194 : "KEY_F24",
		200 : "KEY_PLAYCD",
		201 : "KEY_PAUSECD",
		202 : "KEY_PROG3",
		203 : "KEY_PROG4",
		204 : "KEY_DASHBOARD",
		205 : "KEY_SUSPEND",
		206 : "KEY_CLOSE",
		207 : "KEY_PLAY",
		208 : "KEY_FASTFORWARD",
		209 : "KEY_BASSBOOST",
		210 : "KEY_PRINT",
		211 : "KEY_HP",
		212 : "KEY_CAMERA",
		213 : "KEY_SOUND",
		214 : "KEY_QUESTION",
		215 : "KEY_EMAIL",
		216 : "KEY_CHAT",
		217 : "KEY_SEARCH",
		218 : "KEY_CONNECT",
		219 : "KEY_FINANCE",
		220 : "KEY_SPORT",
		221 : "KEY_SHOP",
		222 : "KEY_ALTERASE",
		223 : "KEY_CANCEL",
		224 : "KEY_BRIGHTNESSDOWN",
		225 : "KEY_BRIGHTNESSUP",
		226 : "KEY_MEDIA",
		227 : "KEY_SWITCHVIDEOMODE",
		228 : "KEY_KBDILLUMTOGGLE",
		229 : "KEY_KBDILLUMDOWN",
		230 : "KEY_KBDILLUMUP",
		231 : "KEY_SEND",
		232 : "KEY_REPLY",
		233 : "KEY_FORWARDMAIL",
		234 : "KEY_SAVE",
		235 : "KEY_DOCUMENTS",
		236 : "KEY_BATTERY",
		237 : "KEY_BLUETOOTH",
		238 : "KEY_WLAN",
		239 : "KEY_UWB",
		240 : "KEY_UNKNOWN",
		241 : "KEY_VIDEO_NEXT",
		242 : "KEY_VIDEO_PREV",
		243 : "KEY_BRIGHTNESS_CYCLE",
		244 : "KEY_BRIGHTNESS_ZERO",
		245 : "KEY_DISPLAY_OFF",
		246 : "KEY_WIMAX",
		247 : "KEY_RFKILL",
		0x100 : "BTN_MISC",
		0x100 : "BTN_0",
		0x101 : "BTN_1",
		0x102 : "BTN_2",
		0x103 : "BTN_3",
		0x104 : "BTN_4",
		0x105 : "BTN_5",
		0x106 : "BTN_6",
		0x107 : "BTN_7",
		0x108 : "BTN_8",
		0x109 : "BTN_9",
		0x110 : "BTN_MOUSE",
		0x110 : "BTN_LEFT",
		0x111 : "BTN_RIGHT",
		0x112 : "BTN_MIDDLE",
		0x113 : "BTN_SIDE",
		0x114 : "BTN_EXTRA",
		0x115 : "BTN_FORWARD",
		0x116 : "BTN_BACK",
		0x117 : "BTN_TASK",
		0x120 : "BTN_JOYSTICK",
		0x120 : "BTN_TRIGGER",
		0x121 : "BTN_THUMB",
		0x122 : "BTN_THUMB2",
		0x123 : "BTN_TOP",
		0x124 : "BTN_TOP2",
		0x125 : "BTN_PINKIE",
		0x126 : "BTN_BASE",
		0x127 : "BTN_BASE2",
		0x128 : "BTN_BASE3",
		0x129 : "BTN_BASE4",
		0x12a : "BTN_BASE5",
		0x12b : "BTN_BASE6",
		0x12f : "BTN_DEAD",
		0x130 : "BTN_GAMEPAD",
		0x130 : "BTN_A",
		0x131 : "BTN_B",
		0x132 : "BTN_C",
		0x133 : "BTN_X",
		0x134 : "BTN_Y",
		0x135 : "BTN_Z",
		0x136 : "BTN_TL",
		0x137 : "BTN_TR",
		0x138 : "BTN_TL2",
		0x139 : "BTN_TR2",
		0x13a : "BTN_SELECT",
		0x13b : "BTN_START",
		0x13c : "BTN_MODE",
		0x13d : "BTN_THUMBL",
		0x13e : "BTN_THUMBR",
		0x140 : "BTN_DIGI",
		0x140 : "BTN_TOOL_PEN",
		0x141 : "BTN_TOOL_RUBBER",
		0x142 : "BTN_TOOL_BRUSH",
		0x143 : "BTN_TOOL_PENCIL",
		0x144 : "BTN_TOOL_AIRBRUSH",
		0x145 : "BTN_TOOL_FINGER",
		0x146 : "BTN_TOOL_MOUSE",
		0x147 : "BTN_TOOL_LENS",
		0x14a : "BTN_TOUCH",
		0x14b : "BTN_STYLUS",
		0x14c : "BTN_STYLUS2",
		0x14d : "BTN_TOOL_DOUBLETAP",
		0x14e : "BTN_TOOL_TRIPLETAP",
		0x14f : "BTN_TOOL_QUADTAP",
		0x150 : "BTN_WHEEL",
		0x150 : "BTN_GEAR_DOWN",
		0x151 : "BTN_GEAR_UP",
		0x160 : "KEY_OK",
		0x161 : "KEY_SELECT",
		0x162 : "KEY_GOTO",
		0x163 : "KEY_CLEAR",
		0x164 : "KEY_POWER2",
		0x165 : "KEY_OPTION",
		0x166 : "KEY_INFO",
		0x167 : "KEY_TIME",
		0x168 : "KEY_VENDOR",
		0x169 : "KEY_ARCHIVE",
		0x16a : "KEY_PROGRAM",
		0x16b : "KEY_CHANNEL",
		0x16c : "KEY_FAVORITES",
		0x16d : "KEY_EPG",
		0x16e : "KEY_PVR",
		0x16f : "KEY_MHP",
		0x170 : "KEY_LANGUAGE",
		0x171 : "KEY_TITLE",
		0x172 : "KEY_SUBTITLE",
		0x173 : "KEY_ANGLE",
		0x174 : "KEY_ZOOM",
		0x175 : "KEY_MODE",
		0x176 : "KEY_KEYBOARD",
		0x177 : "KEY_SCREEN",
		0x178 : "KEY_PC",
		0x179 : "KEY_TV",
		0x17a : "KEY_TV2",
		0x17b : "KEY_VCR",
		0x17c : "KEY_VCR2",
		0x17d : "KEY_SAT",
		0x17e : "KEY_SAT2",
		0x17f : "KEY_CD",
		0x180 : "KEY_TAPE",
		0x181 : "KEY_RADIO",
		0x182 : "KEY_TUNER",
		0x183 : "KEY_PLAYER",
		0x184 : "KEY_TEXT",
		0x185 : "KEY_DVD",
		0x186 : "KEY_AUX",
		0x187 : "KEY_MP3",
		0x188 : "KEY_AUDIO",
		0x189 : "KEY_VIDEO",
		0x18a : "KEY_DIRECTORY",
		0x18b : "KEY_LIST",
		0x18c : "KEY_MEMO",
		0x18d : "KEY_CALENDAR",
		0x18e : "KEY_RED",
		0x18f : "KEY_GREEN",
		0x190 : "KEY_YELLOW",
		0x191 : "KEY_BLUE",
		0x192 : "KEY_CHANNELUP",
		0x193 : "KEY_CHANNELDOWN",
		0x194 : "KEY_FIRST",
		0x195 : "KEY_LAST",
		0x196 : "KEY_AB",
		0x197 : "KEY_NEXT",
		0x198 : "KEY_RESTART",
		0x199 : "KEY_SLOW",
		0x19a : "KEY_SHUFFLE",
		0x19b : "KEY_BREAK",
		0x19c : "KEY_PREVIOUS",
		0x19d : "KEY_DIGITS",
		0x19e : "KEY_TEEN",
		0x19f : "KEY_TWEN",
		0x1a0 : "KEY_VIDEOPHONE",
		0x1a1 : "KEY_GAMES",
		0x1a2 : "KEY_ZOOMIN",
		0x1a3 : "KEY_ZOOMOUT",
		0x1a4 : "KEY_ZOOMRESET",
		0x1a5 : "KEY_WORDPROCESSOR",
		0x1a6 : "KEY_EDITOR",
		0x1a7 : "KEY_SPREADSHEET",
		0x1a8 : "KEY_GRAPHICSEDITOR",
		0x1a9 : "KEY_PRESENTATION",
		0x1aa : "KEY_DATABASE",
		0x1ab : "KEY_NEWS",
		0x1ac : "KEY_VOICEMAIL",
		0x1ad : "KEY_ADDRESSBOOK",
		0x1ae : "KEY_MESSENGER",
		0x1af : "KEY_DISPLAYTOGGLE",
		0x1b0 : "KEY_SPELLCHECK",
		0x1b1 : "KEY_LOGOFF",
		0x1b2 : "KEY_DOLLAR",
		0x1b3 : "KEY_EURO",
		0x1b4 : "KEY_FRAMEBACK",
		0x1b5 : "KEY_FRAMEFORWARD",
		0x1b6 : "KEY_CONTEXT_MENU",
		0x1b7 : "KEY_MEDIA_REPEAT",
		0x1c0 : "KEY_DEL_EOL",
		0x1c1 : "KEY_DEL_EOS",
		0x1c2 : "KEY_INS_LINE",
		0x1c3 : "KEY_DEL_LINE",
		0x1d0 : "KEY_FN",
		0x1d1 : "KEY_FN_ESC",
		0x1d2 : "KEY_FN_F1",
		0x1d3 : "KEY_FN_F2",
		0x1d4 : "KEY_FN_F3",
		0x1d5 : "KEY_FN_F4",
		0x1d6 : "KEY_FN_F5",
		0x1d7 : "KEY_FN_F6",
		0x1d8 : "KEY_FN_F7",
		0x1d9 : "KEY_FN_F8",
		0x1da : "KEY_FN_F9",
		0x1db : "KEY_FN_F10",
		0x1dc : "KEY_FN_F11",
		0x1dd : "KEY_FN_F12",
		0x1de : "KEY_FN_1",
		0x1df : "KEY_FN_2",
		0x1e0 : "KEY_FN_D",
		0x1e1 : "KEY_FN_E",
		0x1e2 : "KEY_FN_F",
		0x1e3 : "KEY_FN_S",
		0x1e4 : "KEY_FN_B",
		0x1f1 : "KEY_BRL_DOT1",
		0x1f2 : "KEY_BRL_DOT2",
		0x1f3 : "KEY_BRL_DOT3",
		0x1f4 : "KEY_BRL_DOT4",
		0x1f5 : "KEY_BRL_DOT5",
		0x1f6 : "KEY_BRL_DOT6",
		0x1f7 : "KEY_BRL_DOT7",
		0x1f8 : "KEY_BRL_DOT8",
		0x1f9 : "KEY_BRL_DOT9",
		0x1fa : "KEY_BRL_DOT10",
		0x200 : "KEY_NUMERIC_0",
		0x201 : "KEY_NUMERIC_1",
		0x202 : "KEY_NUMERIC_2",
		0x203 : "KEY_NUMERIC_3",
		0x204 : "KEY_NUMERIC_4",
		0x205 : "KEY_NUMERIC_5",
		0x206 : "KEY_NUMERIC_6",
		0x207 : "KEY_NUMERIC_7",
		0x208 : "KEY_NUMERIC_8",
		0x209 : "KEY_NUMERIC_9",
		0x20a : "KEY_NUMERIC_STAR",
		0x20b : "KEY_NUMERIC_POUND",
		0x210 : "KEY_CAMERA_FOCUS",
		0x211 : "KEY_WPS_BUTTON",
		0x2c0 : "BTN_TRIGGER_HAPPY",
		0x2c0 : "BTN_TRIGGER_HAPPY1",
		0x2c1 : "BTN_TRIGGER_HAPPY2",
		0x2c2 : "BTN_TRIGGER_HAPPY3",
		0x2c3 : "BTN_TRIGGER_HAPPY4",
		0x2c4 : "BTN_TRIGGER_HAPPY5",
		0x2c5 : "BTN_TRIGGER_HAPPY6",
		0x2c6 : "BTN_TRIGGER_HAPPY7",
		0x2c7 : "BTN_TRIGGER_HAPPY8",
		0x2c8 : "BTN_TRIGGER_HAPPY9",
		0x2c9 : "BTN_TRIGGER_HAPPY10",
		0x2ca : "BTN_TRIGGER_HAPPY11",
		0x2cb : "BTN_TRIGGER_HAPPY12",
		0x2cc : "BTN_TRIGGER_HAPPY13",
		0x2cd : "BTN_TRIGGER_HAPPY14",
		0x2ce : "BTN_TRIGGER_HAPPY15",
		0x2cf : "BTN_TRIGGER_HAPPY16",
		0x2d0 : "BTN_TRIGGER_HAPPY17",
		0x2d1 : "BTN_TRIGGER_HAPPY18",
		0x2d2 : "BTN_TRIGGER_HAPPY19",
		0x2d3 : "BTN_TRIGGER_HAPPY20",
		0x2d4 : "BTN_TRIGGER_HAPPY21",
		0x2d5 : "BTN_TRIGGER_HAPPY22",
		0x2d6 : "BTN_TRIGGER_HAPPY23",
		0x2d7 : "BTN_TRIGGER_HAPPY24",
		0x2d8 : "BTN_TRIGGER_HAPPY25",
		0x2d9 : "BTN_TRIGGER_HAPPY26",
		0x2da : "BTN_TRIGGER_HAPPY27",
		0x2db : "BTN_TRIGGER_HAPPY28",
		0x2dc : "BTN_TRIGGER_HAPPY29",
		0x2dd : "BTN_TRIGGER_HAPPY30",
		0x2de : "BTN_TRIGGER_HAPPY31",
		0x2df : "BTN_TRIGGER_HAPPY32",
		0x2e0 : "BTN_TRIGGER_HAPPY33",
		0x2e1 : "BTN_TRIGGER_HAPPY34",
		0x2e2 : "BTN_TRIGGER_HAPPY35",
		0x2e3 : "BTN_TRIGGER_HAPPY36",
		0x2e4 : "BTN_TRIGGER_HAPPY37",
		0x2e5 : "BTN_TRIGGER_HAPPY38",
		0x2e6 : "BTN_TRIGGER_HAPPY39",
		0x2e7 : "BTN_TRIGGER_HAPPY40",
	}),

	"EV_REL": EnumDict({
		0x00: "REL_X",
		0x01: "REL_Y",
		0x02: "REL_Z",
		0x03: "REL_RX",
		0x04: "REL_RY",
		0x05: "REL_RZ",
		0x06: "REL_HWHEEL",
		0x07: "REL_DIAL",
		0x08: "REL_WHEEL",
		0x09: "REL_MISC",
	}),

	"EV_ABS": EnumDict({
		0x00: "ABS_X",
		0x01: "ABS_Y",
		0x02: "ABS_Z",
		0x03: "ABS_RX",
		0x04: "ABS_RY",
		0x05: "ABS_RZ",
		0x06: "ABS_THROTTLE",
		0x07: "ABS_RUDDER",
		0x08: "ABS_WHEEL",
		0x09: "ABS_GAS",
		0x0a: "ABS_BRAKE",
		0x10: "ABS_HAT0X",
		0x11: "ABS_HAT0Y",
		0x12: "ABS_HAT1X",
		0x13: "ABS_HAT1Y",
		0x14: "ABS_HAT2X",
		0x15: "ABS_HAT2Y",
		0x16: "ABS_HAT3X",
		0x17: "ABS_HAT3Y",
		0x18: "ABS_PRESSURE",
		0x19: "ABS_DISTANCE",
		0x1a: "ABS_TILT_X",
		0x1b: "ABS_TILT_Y",
		0x1c: "ABS_TOOL_WIDTH",
		0x20: "ABS_VOLUME",
		0x28: "ABS_MISC",
		0x30: "ABS_MT_TOUCH_MAJOR",
		0x31: "ABS_MT_TOUCH_MINOR",
		0x32: "ABS_MT_WIDTH_MAJOR",
		0x33: "ABS_MT_WIDTH_MINOR",
		0x34: "ABS_MT_ORIENTATION",
		0x35: "ABS_MT_POSITION_X",
		0x36: "ABS_MT_POSITION_Y",
		0x37: "ABS_MT_TOOL_TYPE",
		0x38: "ABS_MT_BLOB_ID",
		0x39: "ABS_MT_TRACKING_ID",
		0x3a: "ABS_MT_PRESSURE",
	}),

	"EV_MSC": EnumDict({
		0x00: "MSC_SERIAL",
		0x01: "MSC_PULSELED",
		0x02: "MSC_GESTURE",
		0x03: "MSC_RAW",
		0x04: "MSC_SCAN",
	}),

	"EV_LED": EnumDict({
		0x00: "LED_NUML",
		0x01: "LED_CAPSL",
		0x02: "LED_SCROLLL",
		0x03: "LED_COMPOSE",
		0x04: "LED_KANA",
		0x05: "LED_SLEEP",
		0x06: "LED_SUSPEND",
		0x07: "LED_MUTE",
		0x08: "LED_MISC",
		0x09: "LED_MAIL",
		0x0A: "LED_CHARGING",
	}),

	"EV_REP": EnumDict({
		0x00: "REP_DELAY",
		0x01: "REP_PERIOD",
	}),

	"EV_SND": EnumDict({
		0x00: "SND_CLICK",
		0x01: "SND_BELL",
		0x02: "SND_TONE"
	}),
}

# evdev ioctl constants. The horrible mess here
# is to silence silly FutureWarnings
EVIOCGNAME_512 = ~int(~0x82004506L & 0xFFFFFFFFL)
EVIOCGID       = ~int(~0x80084502L & 0xFFFFFFFFL)
EVIOCGBIT_512  = ~int(~0x81fe4520L & 0xFFFFFFFFL)
EVIOCGABS_512  = ~int(~0x80144540L & 0xFFFFFFFFL)


# look for errors here, may be platform specific (likely compatible across all x86 architectures though
# taken from <asm/ioctl.h>
_IOC_NONE = 0
_IOC_WRITE = 1
_IOC_READ = 2

_IOC_NRBITS    = 8
_IOC_TYPEBITS  = 8
_IOC_SIZEBITS  = 14
_IOC_DIRBITS   = 2

_IOC_NRMASK    = ((1 << _IOC_NRBITS) - 1)
_IOC_TYPEMASK  = ((1 << _IOC_TYPEBITS) - 1)
_IOC_SIZEMASK  = ((1 << _IOC_SIZEBITS) - 1)
_IOC_DIRMASK   = ((1 << _IOC_DIRBITS) - 1)

_IOC_NRSHIFT   = 0
_IOC_TYPESHIFT = (_IOC_NRSHIFT+_IOC_NRBITS)
_IOC_SIZESHIFT = (_IOC_TYPESHIFT+_IOC_TYPEBITS)
_IOC_DIRSHIFT  = (_IOC_SIZESHIFT+_IOC_SIZEBITS)

def _IOC(dir, type, nr, size):
	return (dir << _IOC_DIRSHIFT) | (type << _IOC_TYPESHIFT) | (nr <<  _IOC_NRSHIFT) | (size << _IOC_SIZESHIFT)

# taken <linux/input.h>

EV_MAX = 0x1f

def EVIOCGBIT(ev, len):
	return _IOC(_IOC_READ, ord('E'), 0x20 + ev, len)

# *****************************************************************************

event_fmt = str("=llhhl")
if (platform.uname()[4] == 'x86_64'):
	event_fmt = str("=qqhhl")

event_size = struct.calcsize(event_fmt)

def parseEvent(data):
	secs, usecs, packedType, packedCode, value = struct.unpack(event_fmt, data)

	timestamp = secs + (usecs / 1000000.0)
	#event_type = typeMap.fromNumber(packedType)

	#if event_type in codeMaps:
	#	code = codeMaps[event_type].fromNumber(packedCode)
	#else:
	#	code = packedCode
	
	return {"time":timestamp, "type": packedType, "code": packedCode, "value": value}
	
def deviceName(fd):
	buffer = "\0"*512
	return ioctl(fd, EVIOCGNAME_512, buffer).replace("\0", '')

def test_bit(bit, array):
	return (ord(array[ bit // 8]) & (1<<(bit%8)))

def deviceEvents(fd):
	buffer = "\0" * EV_MAX
	data = ioctl(fd, EVIOCGBIT(0, EV_MAX), buffer)
	caps = []
	for test in range(EV_MAX):
		if test_bit(test, data):
			caps += [typeMap[test]]

	return caps

class Event():
	def __init__(self, data=None):
		self.__dict__.update(parseEvent(data))
	
	def __str__(self):
		return "t%12.2f t: %5s c: %25s v: %s" % (self.time, self.type, self.code, self.value)

class EventDevice:
	def __init__(self, device):
		self.fd = os.open(device, os.O_RDWR | os.O_NONBLOCK)
		self.name = deviceName(self.fd)
		self.caps = {}
		for event in deviceEvents(self.fd):
			self.caps[event] = None
			if event == 'EV_ABS':
				self.caps[event] = {}
				
				absmap = codeMaps['EV_ABS']
				buffer = "\0" * struct.calcsize(str("iiiii"))
				for name, number in absmap.nameMap.iteritems():
					values = struct.unpack("iiiii", ioctl(self.fd, EVIOCGABS_512 + number, buffer))
					values = dict(zip(( 'value', 'min', 'max', 'fuzz', 'flat' ),values))
					self.caps[event][name] = values

		
	def __del__(self):
		if self.__dict__.has_key('fd'):
			os.close(self.fd)
			
	def read(self):
		data = os.read(self.fd, event_size)
		event = Event(data)
		return event
		
	
	def fileno(self):
		return self.fd
		
if __name__ == "__main__":
	# simple test to show event system works
	device = EventDevice(sys.argv[1])
	print(device.name)
	print(device.caps)
	
	while True:
		fds = select.select([device], [], [], 1)
		if (len(fds[0]) > 0):
			print(device.read())
