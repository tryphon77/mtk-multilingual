# -*- coding: utf-8 -*-

from buffer import Buffer
from tools import include, write_to_VRAM

symbol_table = {}

buf = Buffer.load("rom\\Magical Taruruuto-kun (Japan).md")

# ============================================================================




buf.set_index(0x80000)
symbol_table = {}


if True:
	print("Disable checksum...")
	buf.save_state()
	buf.set_index(0x802)
	buf.write_hex("4E71 4E71 4E71 4E71 4E71 4E71 4E71 6014")
	buf.restore_state()
	print("done")


if True:
	print("Include font tilemap")

	buf.align(4)
	symbol_table["data133f2"] = buf.index
	tm = Buffer.load("res/133f2.bin")
	buf.write_w(len(tm) // 4 - 1)
	buf.write(tm)

	
if True:
	print("Include dialog table")
	# Meeting Honmaru and Iyona	
	buf.align(4)
	symbol_table["data4c2d2"] = buf.index
	tm = Buffer.load("res/4c2d2.bin")
	buf.write_w(len(tm) // 4 - 1)
	buf.write(tm)

	print("done")

if True:
	print("English texts")
	import english
	english.process(buf, symbol_table)

if True:
	print("French texts")
	import french
	french.process(buf, symbol_table)
	
assert(buf.index < 0x98000)

if True:
	print("Including asm hacks...")
	print("Symbol table:")
	for key in symbol_table:
		print("%s: %X" % (key, symbol_table[key]))
	include(buf, "hacks.asm", symbol_table)
	print("done")

if True:
	print("Build option menu")

	# change max menu items on selection
	buf.write_w(7, pos=0xb160)
	buf.write_w(6, pos=0xb18e)
	
	# default map is 0
	buf.write_w(0, pos=0xb9e8)
	buf.write("4E71"*9, pos=0xb14c)

	# change menu items position
	buf.write_l(write_to_VRAM(0xC320), pos=0xba52) # OPTIONS
	buf.write_l(write_to_VRAM(0xC416), pos=0xba5e) # CONTROL
	buf.write_l(write_to_VRAM(0xC616), pos=0xba6a) # BGM
	buf.write_l(write_to_VRAM(0xC716), pos=0xba72) # SE
	buf.write_l(write_to_VRAM(0xC816), pos=0xba7a) # VOICE
	buf.write_l(write_to_VRAM(0xCB16), pos=0xba84) # EXIT
	buf.write_l(write_to_VRAM(0xC916), pos=0xba8e) # MAP
#	buf.write_l(write_to_VRAM(0xC320), pos=0xba52) # OPTIONS

	buf.write_l(write_to_VRAM(0xC428), pos=0xb2de) # A-MAGIC
	buf.write_l(write_to_VRAM(0xC528), pos=0xb2ec) # 
	buf.write_l(write_to_VRAM(0xC428), pos=0xb2fa) # 
	buf.write_l(write_to_VRAM(0xC4a8), pos=0xb308) # 
	buf.write_l(write_to_VRAM(0xC528), pos=0xb316) # 
	buf.write_l(write_to_VRAM(0xC428), pos=0xb324) # 
	buf.write_l(write_to_VRAM(0xC4a8), pos=0xb332) # 
	buf.write_l(write_to_VRAM(0xC528), pos=0xb340) # 

	# change BGM, SE and VOICE digits positions
	buf.write_l(write_to_VRAM(0xC628), pos=0xb03a) # BGM 
	buf.write_l(write_to_VRAM(0xC728), pos=0xb04c) # SE
	buf.write_l(write_to_VRAM(0xC828), pos=0xb05e) # VOICE
	
	# change maps names positions
	buf.write_l(write_to_VRAM(0xC928), pos=0xb554)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb580)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb58a)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb594)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb5a6)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb5b0)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb5c2)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb5d2)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb5dc)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb5e6)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb5f0)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb5fa)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb604)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb60e)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb618)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb626)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb63a)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb644)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb64e)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb658)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb66a)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb674)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb67e)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb68e)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb6a0)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb6aa)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb6b4)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb6c4)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb6dc)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb6e6)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb6f0)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb6fa)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb70c)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb716)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb732)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb742)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb74c)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb756)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb760)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb76a)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb776)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb782)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb78e)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb79a)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb7a6)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb7b2)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb7bc)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb7c8)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb7da)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb7e8)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb7f6)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb804)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb812)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb820)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb82e)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb83c)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb84a)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb858)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb866)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb874)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb882)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb890)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb89e)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb8b0)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb8be)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb8cc)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb8da)
	buf.write_l(write_to_VRAM(0xC928), pos=0xb8e6)

buf.save("rom\\out.md")
