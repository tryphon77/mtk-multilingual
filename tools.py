# -*- coding: utf-8 -*-

import os
from buffer import Buffer
from surface import Surface4bpp
import png
import numpy as np


temp_dir = "temp"

def load_png_8(path):
	def cvt_(col):
		r, g, b = col
		return ((b // 32) << 9) + ((g // 32) << 5) + ((r // 32) << 1)

	r = png.Reader(filename=path)
	w, h, arr, info = r.read()
	
	palette = [cvt_(col) for col in info['palette'][:64]]
	arr = np.array(list(arr), dtype=np.uint8)
	arr.shape = (h, w)

	return arr, palette


def get_pattern(ptrn, patterns, base_tile, pal_id, priority, check_policy):
	first_free_slot = -1

	for i, p in enumerate(patterns):
		if p is None and first_free_slot == -1:
			first_free_slot = i
		if isinstance(p, Surface4bpp):
			if check_policy == 1 and ptrn.equals(p):
				return (priority << 15) | (pal_id << 13) | (base_tile + i)
			elif check_policy == 2:
				check = ptrn.equals_with_flips(p)
				if check:
					vflip, hflip = check
					return (priority << 15) | (pal_id << 13) | (vflip << 12) | (hflip << 11) | (base_tile + i)

	if first_free_slot == -1:
		i = len(patterns)
		patterns.append(ptrn)
	else:
		i = first_free_slot
		patterns[i] = ptrn

	return (priority << 15) | (pal_id << 13) | (base_tile + i)
			

def get_tile(tile, tile_size, tileset, patterns, base_tile, pal_id, priority, check_policy):
	tw, th = tile_size
	ts = (tw // 8)*(th // 8)
		
	for i, t in enumerate(tileset):
		if tile.equals(t["surface"]):
			found = True
			for _ in range(ts):				
				if t["priority"] != priority and t["pal_id"] != pal_id:
					found = False
					break
			if found:
				tile_id = i
				break

	else:
		new_tile = {
			"surface": tile,
			"priority": priority,
			"pal_id": pal_id,
			"attrs": []
		}
		tile_id = len(tileset)
		tileset.append(new_tile)

		for y in range(0, th, 8):
			for x in range(0, tw, 8):
				ptrn = tile.subsurface((x, y, 8, 8))
				ptrn_id = get_pattern(ptrn, patterns, base_tile, pal_id, priority)
				new_tile["attrs"].append(ptrn_id)

	return tile_id

# palette_1 = Palette.from_md_values([0x222, 0x22E, 0xEEE, 0x82E, 0x0C6, 0x2CE, 0xCC0, 0xEE0, 0xE62, 0xA42, 0x820, 0xE0E, 0x60E, 0xE64, 0x84E, 0x000])

def make_map(src, patterns=None, tileset=None, tilemap=None, size=(8,8), base_tile=0, check_policy=2):
	"""
	make_map
	Parameters
	----------
	src : np.array 
	    source image
	patterns : list, optional
		list of patterns data (if not, generated). The default is None.
		if an item is set to None, the corresponding pattern is considered free
		if the item is something other than None, the corresponding pattern
		is considered unavailable
	tileset : list, optional
		if size != (8,8), tiles description. The default is None.
		A tile is described as a dict
	tilemap : buffer, optional
		if size != (8,8), tilemap description in terms of tiles.
		if size == (8,8), tilemap description in terms of attributed patterns. 
		The default is None.
	size : tuple, optional
		size of tiles. If (8,8) the tilemap is generated in terms of
		attributed patterns. The default is (8,8).
	base_tile : int, optional
		start of patterns tileset in VRAM. The default is 0.
	check_policy: int, optional, default=2
		0: doesn't check identical patterns
		1: check identical patterns, without considering flips
		2: check identical patterns, considering flips

	Returns
	-------
	None.

	"""
	
	if patterns is None:
		patterns = []

	if tileset is None:
		tileset = []
	
	if tilemap is None:
		tilemap = Buffer()
	
	h, w = src.shape
	tw, th = size

	for y in range(0, h, th):
		for x in range(0, w, tw):
			tile_array = src[y : y + th, x: x + tw]
			
			pal_id = np.max((tile_array >> 4))
			priority = (tile_array >> 6).any()
			
			tile_surf = Surface4bpp(data = tile_array & 15)
			
#			print("tile at (%d, %d): pal_id=%d, priority=%d" % (x, y, pal_id, priority))
			
			if size == (8, 8):
				map_data = get_pattern(tile_surf, patterns, base_tile, pal_id, priority, check_policy)
			
			else:
				raise Exception()
				map_data = get_tile(tile_surf, size, tileset, patterns, base_tile, pal_id, priority, check_policy)

			tilemap.write_w(map_data)

	return {
		"patterns": patterns,
		"tileset": tileset, 
		"tilemap": tilemap
	}

def write_patterns(buf, patterns):	
	for i, ptrn in enumerate(patterns):
#		print(ptrn)
		if isinstance(ptrn, Surface4bpp):
#			ptrn.save("dbg/pattern_%03X.png" % i, palette=palette_1)
			ptrn_buf = ptrn.to_buffer()
#			ptrn_buf.save("dbg/pattern_%03X.bin" % i)
			buf.write(ptrn_buf)
	
	if False:
		ptrn_buf.save("patterns.bin")

def write_to_VRAM(pos):
	cmd = 1
	res = ((cmd & 3) << 30) + ((pos & 0xFFF) << 16) + (((cmd >> 4) & 15) << 4) + ((pos >> 14) & 3)
#	print("pos=%X, to VDP_ctrl: %08X" % (pos, res))
	return res

def include(buf, path, symbols={}):
	res = ["%s equ %s\n" % (k, symbols[k]) for k in symbols]
	
	with open(path) as f:
		res = res + f.readlines()
	
	with open("__temp__.asm", 'w') as f:
		f.write(''.join(res))

	dirname = os.getcwd()
	print("bin\\asm68k.exe /ps '%s\\__temp__.asm','%s\\__temp__.s','%s\\__temp__.sym'"\
			  % (dirname, temp_dir, temp_dir))
#	os.system("bin\\asm68k.exe /ps '%s\\__temp__.asm','%s\\__temp__.s','%s\\__temp__.sym'"\
#			  % (dirname, dirname, dirname))
#	os.system("bin\\asm68k.exe /ps '%s/__temp__.asm','%s/__temp__.s','%s/__temp__.sym'" % (dirname, dirname, dirname))
	os.system("bin\\asm68k.exe /ps __temp__.asm,__temp__.s,__temp__.sym")
	
	with open("__temp__.s") as f:
		lines = f.readlines()
	
	for line in lines:
		line = line.strip()
		if line.startswith("S"):
			line_type = line[1]
			if line_type == "3":
				line_ln = int(line[2:4], 16)
				line_addr = int(line[4:12], 16)
				line_data = line[12:4+2*line_ln-2]
				print("%X: %s" % (line_addr, line_data))
				buf.write(line_data, line_addr)


def write_tm(tm, text, encoding):
	res = Buffer()
	res.write_w(tm.read_w())
	res.write_w(tm.read_w())
	
	for i, c in enumerate(text):
		if i%2 == 0:
			cs = tm.read_w()
		
		if c == "*":
			if i%2 == 0:
				res.write_w(cs)
		elif c == " ":
			res.write_w(0x8000)
		elif c in encoding:
			k = encoding.index(c)
			res.write_w(0x8022 + k)
			if c == "$":
				pass
#				print("$: 0x%X" % (0x8022 + k))
		else:
			raise Exception("Character |%s| not found" % c)

	return res

def write_tm_2(tm, pos, text, width, attrs, space, encoding, offset=0):
	x, y = pos
	tm.set_index(offset + y*width*2 + x*2)
	for c in text:
		if c == " ":
			p = tm.index
			tm.write_w(space)
			tm.write_w(space, pos = p + width*2)

		else:
			code = attrs + 2*encoding.index(c)
			p = tm.index
			tm.write_w(code)
			tm.write_w(code + 1, pos = p + width*2)


def write_dialogs_1(buf, symbol_table, language, dialog_id, text, encoding):
	addr = buf.read_l(0x1330a + 4*dialog_id)
	
	symbol_table["data%x%s" % (addr, language)] = buf.index
	tm = Buffer.load("dump/%x.bin" % addr)
	tm_eng = write_tm(tm, text, encoding)
	tm_eng.align(4)
#	tm_eng.save("%x%s.bin" % (addr, language))
	buf.write_w(len(tm_eng) // 4 - 1)
	buf.write(tm_eng)

def write_dialogs_2(buf, symbol_table, language, dialog_id, text, encoding):
	address = buf.read_l(0xc71a + 4*dialog_id)
	print(hex(address))
	
	buf.align(4)
	symbol_table["data%x%s" % (address, language)] = buf.index
	tm = Buffer.load("dump/%x.bin" % address)
	tm_eng = write_tm(tm, text, encoding)

	symbol_table["dataSize%x%s" % (address, language)] = len(tm_eng) - 4

	tm_eng.align(4)
#	tm_eng.save("%x.bin" % address)
	buf.write_w(len(tm_eng) // 4 - 1)
	buf.write(tm_eng)

def write_stage_scene(buf, symbol_table, stage_id, language, text, encoding, edge=1):	
	width = max([len(t) for t in text]) + 2*edge
	if width & 1:
		width += 1
	
	top = 4
	left = 20 - width//2
	height = 2*len(text) + 3 + 2
	
	tm = Buffer()
	
	tm.write_b(width - 1)
	tm.write_b(height - 1)
	vpos = 0xc000 + 2*(64*top + left)
	tm.write_l(write_to_VRAM(vpos))
	offset = tm.index
	
	stage_row_1 = "81 E1 81 E2 81 E3 81 E4 81 E5 81 E6 81 E7 81 E8 81 E9 81 EA 80 02 80 02 81 %02X 81 %02X" % (0xC7 + 2*stage_id, 0xC8 + 2*stage_id)
	stage_row_2 = "81 F1 81 F2 81 F3 81 F4 81 F5 81 F6 81 F7 81 F8 81 F9 81 FA 80 02 80 02 81 %02X 81 %02X" % (0xD7 + 2*stage_id, 0xD8 + 2*stage_id)
	stage_width = (len(stage_row_1) + 1)//6
	
	tm.write("8002"*width*3)
	tm.write("8001"*width*(height - 3))
	
	tm.write(stage_row_1, pos=offset + 2*((width - stage_width)//2))
	tm.write(stage_row_2, pos=offset + 2*width + 2*((width - stage_width)//2))
	
	y = 4
	for t in text:
		w = len(t)
		x = (width - w)//2
#		print("(%d, %d): %s" % (x, y, t))
		write_tm_2(tm, (x, y), t, width, 0x8023, 0x8001, encoding, offset=offset)
		y += 2
	
	base_buf_addr = buf.read_l(pos=0xf848 + 4*(stage_id - 1))	
#	tm.save("%x.bin" % base_buf_addr)
	buf.align(4)
	symbol_table["data%x%s" % (base_buf_addr, language)] = buf.index
	buf.write_w(len(tm) // 4)
	buf.write(tm)

def make_font(buf, symbol_table, language, font):
	symbol_table['font%s' % language] = buf.index
	chars = font.split(size=(8, 16))
	symbol_table['FontSize%s' % language] = len(chars)*2
	print("%s font size: 0x%X" % (language, len(chars)*2))

	for c in chars:
		buf.write(c.to_buffer())

def make_magics(buf, symbol_table, surf, language, texts=[], encoding=None):
	h, w = surf.shape
	tw, th = w//8, h//8
	magics = make_map(surf)
	
	buf.align(4)
	symbol_table["magics%sTiles" % language] = buf.index
	symbol_table["nbMagics%sTiles" % language] = len(magics["patterns"])
	write_patterns(buf, magics["patterns"])

	src_tm = magics["tilemap"]
#	src_tm.save("src_tm.bin")
	src_tm.set_index(0)
	magics_tm = Buffer.load("res/12854.bin")
	for y in [5, 6, 8, 9, 11, 12]:
		magics_tm.set_index(22*2*y + 7*2)
		for _ in range(tw):
			magics_tm.write_w(0x8068 + src_tm.read_w())
	
	for x, y, text in texts:
		magics_tm.set_index(2*y*22 + x*2)
		for c in text:
			if c not in encoding:
				raise Exception("Character |%s| not found" % c)
			magics_tm.write_w(0x869c + encoding.index(c))
		
#	magics_tm.save("12854%s.bin" % language)
	
	buf.align(4)
	symbol_table["magics%sTileMap" % language] = buf.index
	buf.write_w(len(magics_tm) // 4)
	buf.write(magics_tm)

def make_title_screen(buf, symbol_table, fg_img, bg_img, font_img, language):
	blank_img = np.zeros((8, 8), dtype=np.uint8)

	patterns = [None] + [0]*47 + [None] + [0]*13 + [None] + [0] + [None]*0x30
	symbol_table["titleFontVpos"] = 16 # -32 # len(patterns)
	blank = make_map(blank_img, patterns=patterns)
	font = make_map(font_img, patterns=patterns, check_policy=0)

	# pattern 0 is blank, used as such is PLANE_A option screen
	# font starts at 48, so it's not overwritten during end staff roll
	# font[0] is a space (used as such)
	# font[1..13] is free for title screen tiles
	# font[14] is a dot
	# font[15] is free for title screen tiles
	# font[16] is (c) then letters... 
	patterns[1:48] = [None]*47
	patterns[49:49+13] = [None]*13
	patterns[63] = None
	
	fg = make_map(fg_img, patterns=patterns)

	bg = make_map(bg_img, patterns=patterns)

	symbol_table["nbTitlePtrns%s" % language] = len(patterns)
	
	buf.align(4)
	symbol_table["titleScreenTiles%s" % language] = buf.index
	write_patterns(buf, patterns)
	
	buf.align(4)
	symbol_table["titleScreenTileMapFg%s" % language] = buf.index
	buf.write_w(len(fg["tilemap"]) // 4)
	buf.write(fg["tilemap"])

	buf.align(4)
	symbol_table["titleScreenTileMapBg%s" % language] = buf.index
	buf.write_w(len(bg["tilemap"]) // 4)
	buf.write(bg["tilemap"])


# Decompressors

class Context:
	pass
# Nemesis Decompressor

def nemesis_decode(source, dest):
    number_of_tiles = source.read_w()
    xor_output = (number_of_tiles & 0x8000) != 0
    number_of_tiles &= 0x7FFF
    codes = {}
    decode_header(source, dest, codes)
    decode_internal(source, dest, number_of_tiles, codes, xor_output)


def decode_header(source, dest, codes):
    output_value = 0

    # Loop until a byte with value 0xFF is encountered
    while True:
        input_value = source.read_b()

        if input_value == 0xFF:
            break
        
        if input_value & 0x80:
            output_value = input_value & 0xF
            input_value = source.read_b()

        bincode = source.read_b()
        code = "{0:08b}".format(bincode)[-(input_value & 0xF):]
        rep = ((input_value & 0x70) >> 4) + 1
        
        codes[code] = (output_value, rep)

def decode_internal(source, dest, number_of_tiles, codes, xor_mode):
    context = Context()
    context.xor_mode = xor_mode

    def write_nibbles(col, rep):
        for _ in range(rep):
            context.current_long = (context.current_long << 4) + col
            context.nibble_counter += 1
            if context.nibble_counter == 8:
                if context.xor_mode:
                    context.current_long ^= context.last_long
                dest.write_l(context.current_long)
                context.last_long = context.current_long
                context.written_bits += 32
                context.current_long = 0
                context.nibble_counter = 0
    
    number_of_bits = number_of_tiles * 0x20 * 8
    
    current_code = ""
    while context.written_bits < number_of_bits:
        current_code += str(source.read_bit())

        if current_code == "111111":
            rep = source.read_bits(3) + 1
            col = source.read_bits(4)
            write_nibbles(col, rep)
            current_code = ""

        elif current_code in codes.keys():
            col, rep = codes[current_code]
            write_nibbles(col, rep)
            current_code = ""





# Enigma Decompressor
	
def fun_644(context):
	base = context.a3
	if context.d4 & 0x8000:
		p1 = context.source.read_bit()
		base |= p1*0x1000
	if context.d4 & 0x80000000:
		p2 = context.source.read_bit()
		base |= p2*0x800

	context.d1 = context.source.read_bits(context.a5) + base
	

def func_000(context):
	for _ in range(context.d2 + 1):
		context.dest.write_w(context.a2)
		context.a2 += 1

def func_010(context):
	for _ in range(context.d2 + 1):
		context.dest.write_w(context.a4)

def func_100(context):
	fun_644(context)
	
	for _ in range(context.d2 + 1):
		context.dest.write_w(context.d1)

def func_101(context):
	fun_644(context)
	
	for _ in range(context.d2 + 1):
		context.dest.write_w(context.d1)
		context.d1 += 1

def func_110(context):
	fun_644(context)
	
	for _ in range(context.d2 + 1):
		context.dest.write_w(context.d1)
		context.d1 -= 1

def func_111(context):
	if context.d2 == 15:
		context.done = True
	
	else:
		for _ in range(context.d2 + 1):
			fun_644(context)
			context.dest.write_w(context.d1)

funcs = [func_000, func_000, func_010, func_010, func_100, func_101, func_110, func_111]

def enigma_decompress(source, d0):
	"""Compression used in Magical Taruruto tilemaps"""
	context = Context()
	context.source = source
	context.dest = Buffer()

	context.a3 = d0
	context.a5 = source.read_b()
	d4 = source.read_b()
	context.d4 = ((d4 & 1) << 31) + ((d4 & 2) << 14) + ((d4 & 0xFFFC) >> 2)
	context.a2 = source.read_w() + context.a3
	context.a4 = source.read_w() + context.a3

	context.done = False

	while not context.done:
		context.d1 = source.read_bits(3)
		if context.d1 & 4:
			context.d2 = source.read_bits(4)
		else:
			context.d2 = (context.d1 & 1)*8 + source.read_bits(3)

		funcs[context.d1](context)

	return context.dest
