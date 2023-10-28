# -*- coding: utf-8 -*-
from buffer import Buffer
from tools import enigma_decompress

buf = Buffer.load("rom\\Magical Taruruuto-kun (Japan).md")

for pos in [
			0x13aa6, 0x13c94, 0x13df4, 0x13ff0, 0x137bc, 0x138c0, # dialogs with portraits
			0x4c5fc, 0x4c6ca, 0x4c48e, 0x4c552, 0x4c646, 0x4c754, # encounters
			]:
	buf.set_index(pos)
	res = enigma_decompress(buf, 0)
	res.save("dump/%x.bin" % pos)
