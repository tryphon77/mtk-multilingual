# encoding: utf-8

import sys
sys.path.append('..')

from buffer import Buffer
#from tools.colors import color_to, to_color, Color, regen_palette

import pygame, numpy, png

class Surface4bpp():
	def __init__(self,
				 size = (0, 0),
				 data = None,
				 palette = None,
				 colorkey = None):
		self.width, self.height = size
		self.colorkey = colorkey

		self.checksum = 0
		if data is not None:
			self.height, self.width = data.shape
			self.data = data
			self._compute_checksum()
		else:
			self.data = numpy.zeros((self.height, self.width), dtype = numpy.uint8)

		self.size = (self.width, self.height)
		self.palette = palette

	def __str__(self):
		return '\n'.join([''.join(['%X' % self.data[j, i] 
							 for i in range(self.get_width())])
					for j in range(self.get_height())])


	def copy(self):
		return Surface4bpp(self.size,
						   data = self.data[:,:])


	def flip(self, hflip = False, vflip = False):
		res = self.copy()
		if hflip:
			res.data = res.data[:, ::-1]
		if vflip:
			res.data = res.data[::-1, :]
		return res

	def rotate90(self, counter = False):
		res = Surface4bpp((self.get_height(), self.get_width()),
						   data = self.data.transpose(),
						   palette = self.palette)
		if counter:
			return res.flip(vflip = True)
		return res.flip(hflip = True)

	def equals(self, other):
		return self.checksum == other.checksum \
			and self.size == other.size \
			and numpy.all(self.data == other.data)
	
	def equals_with_flips(self, other):
		if self.checksum == other.checksum and self.size == other.size:
			if numpy.all(self.data == other.data):
				return (False, False)
			if numpy.all(self.data[::-1, :] == other.data):
				return (True, False)
			if numpy.all(self.data[:, ::-1] == other.data):
				return (False, True)
			if numpy.all(self.data[::-1, ::-1] == other.data):
				return (True, True)
		return False

	def set_palette(self, palette):
		self.palette = palette

	def get_palette(self, palette):
		return self.palette

	def get_size(self):
		return (self.width, self.height)

	def get_width(self):
		return self.width

	def get_height(self):
		return self.height

	def get_array(self):
		return self.data

	def subsurface(self, rect):
#		 print 'Surface4bpp.subsurface'
		x, y, w, h = rect
		res = Surface4bpp((w, h))
		res.blit(self, (0, 0), rect)
		return res

	@staticmethod
	def make_surface(a):
		res = Surface4bpp(a.shape,
						  data = a)
		return res

	def get_at(self, pos):
		x, y = pos
		if (0 <= x < self.width) and (0 <= y < self.height):
			return self.data[y, x]
		return 0

	def set_at(self, pos, color):
		x, y = pos
		if 0 <= x < self.width and 0 <= y < self.height:
			self.data[y, x] = (color & 0xF)
			self._compute_checksum()

	def blit(self, src, dest_pos, src_rect = (0, 0)):
		dx, dy = dest_pos
		if dx < 0:
			dx += self.width
		if dy < 0:
			dy += self.height

		if len(src_rect) == 4:
			sx, sy, sw, sh = src_rect
			sw = min(sw, src.width - sx)
			sh = min(sh, src.height - sy)
		else:
			sx, sy = src_rect
			sw, sh = src.size

#		  print 'source:', src.data.shape, (sx, sy, sw, sh), ', colorkey =', src.colorkey
#		  print 'dest:', self.data.shape, (dx, dy)

		if src.colorkey is not None:
			src_data = src.data[sy : sy + sh, sx : sx + sw]
			mask = src_data != src.colorkey
			self.data[dy : sy + sh, dx : dx + sw][mask] = src_data[mask]
		else:
#			 print self.width, self.height, src.width, src.height
#			  print dx, dy, sx, sy, sw, sh
			self.data[dy : sy + sh, dx : dx + sw] = src.data[sy : sy + sh, sx : sx + sw]

		self._compute_checksum()

	def cut(self, rect):
#		 print 'cut:', rect, self.size
		(x, y, w, h) = rect
		x_off = min(x, 0)
		y_off = min(y, 0)
		x = max(x, 0)
		y = max(y, 0)
		res = Surface4bpp((w, h))
		res.blit(self, (-x_off, -y_off), (x, y, w + x_off, h + y_off))
		return res

	def fill(self, color, rect = None):
		if rect is None:
			x, y = 0, 0
			dx, dy = self.size
		else:
			x, y, dx, dy = rect
		self.data[y : y + dy, x : x + dx] = color
		return self


	def get_tile_at(self, pos):
		x, y = pos
		return (self.data[y : y + 8, x : x + 7 : 2] * 0x10 \
				+ self.data[y : y + 8, x + 1: x + 8 : 2]).flatten()

	@staticmethod
	def load_from_png_8(path):
		def cvt_(col):
			r, g, b = col
			return ((b // 32) << 9) + ((g // 32) << 5) + ((r // 32) << 1)
	
		r = png.Reader(filename=path)
		w, h, arr, info = r.read()
		
		res = Surface4bpp((w, h))
		res.data[:] = list(arr)
		palette = [cvt_(col) for col in info['palette'][:64]]
		res.palette = palette

		return res
	
	@staticmethod
	def from_buffer(size, buf):
		res = Surface4bpp(size)

		for y in range(res.get_height()):
			for x in range(res.get_width()):
				if buf.is_eof():
					c = 0
				else:
					c = buf.read_nibble()
				res.set_at((x, y), c)

		return res
	
	@staticmethod
	def from_string(s):
#		 s = s.strip()
		rows = s.split()
		
		t = [r[0] for r in rows]
#		 print len(t)
#		 print ''.join(t)

		n_rows = len(rows)
		n_cols = len(rows[0])
		res = Surface4bpp((n_cols, n_rows))
		
#		 print n_rows, n_cols
#		 print '|\n'.join(rows)
		data = numpy.array([[int(c, 16) for c in row] for row in rows])
		res.data = data
		
		return res

	def to_buffer(self):
		interleaved_data = (self.data[:, ::2] << 4) + self.data[:, 1::2]
		res = Buffer(interleaved_data.flatten())
		return res

	def split(self, size=(8, 8), sprite_order = False):
		res = []
		w, h = size
		x = y = 0
		while True:
			piece = Surface4bpp((w, h), palette = self.palette, colorkey = self.colorkey)
			piece.blit(self, (0, 0), (x, y, w, h))
			res += [piece]

			if sprite_order:
				y += h
				if y >= self.height:
					y = 0
					x += w
					if x >= self.width:
						return res

			else:
				x += w
				if x >= self.width:
					x = 0
					y += h
					if y >= self.height:
						return res

	def _compute_checksum(self):
		self.checksum = self.data.sum()

	def dump(self):
		return '\n'.join([''.join(['%X' % self.get_at((i, j)) for i in range(self.width)]) for j in range(self.height)])
	
	def draw_rect(self, rect, color):
		x, y, w, h = rect
		x0 = max(x, 0)
		y0 = max(y, 0)
		x1 = min(x + w - 1, self.width)
		y1 = min(y + h - 1, self.height)
		
		if x >= 0:
			self.data[y0:y1, x0] = color
		if x < self.width:
			self.data[y0:y1, x0] = color
		if y >= 0:
			self.data[y0, x0:x1] = color
		if y < self.height:
			self.data[y1, x0:x1] = color
	
	def draw_rects(self, rects, color):
		for rect in rects:
			self.fill(color, rect)
#			 self.draw_rect(rect, color)

def make_composite(images, width = 128, height = 1280):
	res = Surface4bpp((width, height))

	x = y = 0
	h = 0
	for img in images:
		if x + img.get_width() > width:
			x = 0
			y += h
			h = 0
		res.blit(img, (x, y), (0, 0))
		x += img.get_width()
		h = max(h, img.get_height())

	return res

class Bitmap(Surface4bpp):
	def __init__(self,
				 size = None,
				 data = None,
				 palette = None):
		if data is not None:
			self.data = data
			self.size = data.shape
			self._compute_checksum()
		else:
			self.data = numpy.zeros(size, dtype = numpy.uint8)
			self.size = size
		self.width, self.height = self.size
		self.colorkey = None

		self.checksum = 0

		self.palette = palette

	@staticmethod
	def from_surface(surf, bg = 0):
		data = numpy.uint8(surf.data != 0)
		return Bitmap(surf.size, data = data)
	
	@staticmethod
	def from_pygame_surface(surface, palette, mode = 'argb', bg = 0):
		return Bitmap.from_surface(\
			Surface4bpp.from_pygame_surface(surface, palette, mode), 
			bg)

	def copy(self):
		return Bitmap(self.size,
					  data = self.data[:,:])

	def fill(self, color = 1, rect = None):
		Surface4bpp.fill(self, color, rect)
	
	def subsurface(self, rect):
#		 print 'Bitmap.subsurface'
		return Bitmap.from_surface(\
			Surface4bpp.subsurface(self, rect))

	@staticmethod
	def from_buffer(size, buf):
		res = Bitmap(size)

		for y in range(res.get_height()):
			for x in range(res.get_width()):
				if buf.is_eof():
					c = 0
				else:
					c = buf.read_bit()
				res.set_at((x, y), c)

		return res

	def to_buffer(self):
		interleaved_data = (self.data[ ::8, :] << 7) \
						 + (self.data[1::8, :] << 6) \
						 + (self.data[2::8, :] << 5) \
						 + (self.data[3::8, :] << 4) \
						 + (self.data[4::8, :] << 3) \
						 + (self.data[5::8, :] << 2) \
						 + (self.data[6::8, :] << 1) \
						 + (self.data[7::8, :])
		res = Buffer(interleaved_data.transpose().flatten())
		return res

if __name__ == '__main__':
	from tools.colors import regen_palette

	surf = pygame.image.load('face-0.png')
	print (surf.get_size())

	test1 = Surface4bpp.from_pygame_surface(surf, regen_palette, mode = 'bgra')
	for j in range(test1.get_height()):
		test1.data[0, j] = j % 16
	print ('%X' % test1.colors_error)
	pygame.image.save(test1.to_pygame_surface(regen_palette, indexed = False), 'md-face-0.png')
	
	s = str(test1)
	print (s)
	test2 = Surface4bpp.from_string(s)
	print ('======================')
	print (str(test2))
	pygame.image.save(test2.to_pygame_surface(regen_palette, indexed = False), 'md-face-1.png')
	
