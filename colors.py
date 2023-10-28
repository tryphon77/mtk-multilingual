import pygame
import numpy
import os

class Color():
    def __init__(self,
                 md_value,
                 rgb_value,
                 transparent = False):
        self.md_value = md_value
        self.rgb_value = rgb_value
    
    def __str__(self):
        r, g, b = self.rgb_value
        return '[Color | md_value = %03X | rgb_value: r = %02X, g = %02X, b = %02X]' % (self.md_value, r, g, b)
    
    def get_rgb(self, mode = 'argb'):
        r, g, b = self.rgb_value
        return color_to([r, g, b, 255], mode)
    
    def to_pygame_color(self):
        r, g, b = self.rgb_value
        return pygame.Color(r, g, b, 255)
    
    @staticmethod
    def from_md_value(md_value):
        # algo used by GENS
        b, g, r = (md_value >> 8) * 0x12, ((md_value >> 4) & 0xF) * 0x12, (md_value & 0xF) * 0x12
        return Color(md_value, [r, g, b])
    
    @staticmethod
    def from_rgb_value(value, mode = 'argb'):
        r, g, b, a = to_color(value, mode)
        mr = ((r + 0x12)//0x24) * 2
        mg = ((g + 0x12)//0x24) * 2
        mb = ((b + 0x12)//0x24) * 2
        return Color((mb << 8) + (mg << 4) + mr,
                     [r, g, b])

def color_to(rgba_list, descr):
    r, g, b, a = rgba_list
    return (r << (8 * (3 - descr.index('r')))) + \
        (g << (8 * (3 - descr.index('g')))) + \
        (b << (8 * (3 - descr.index('b')))) + \
        (a << (8 * (3 - descr.index('a'))))

def to_color(val, descr):
    def _byte(p):
        return (val >> 8*p) & 0xFF
    r = _byte(3 - descr.index('r'))
    g = _byte(3 - descr.index('g'))
    b = _byte(3 - descr.index('b'))
    if 'a' in descr:
        a = _byte(3 - descr.index('a'))
    else:
        a = 255
    return (r, g, b, a)
        
def RGB_to_MD(colors):
    def _cvt(x):
        return int(float(x * 14)/255) & 0xE

    res = []

    for (r, g, b, _) in colors:
        res += [(_cvt(b) << 8) + (_cvt(g) << 4) + _cvt(r)]
    
    return res

class Palette():
    _current_id_ = 0
    _registration_ = {}

    def __init__(self, 
                 colors = [], 
                 id_ = -1):

        pygame.init()
        
        self.used_colors = set()

        self.replacement_table = {}
        self.colors = colors
        self.diff_min = 0
        
        if id_ >= 0:
            self.set_id(id_)
        else:
            self.id_ = id_

    @staticmethod
    def from_md_values(vals, id_ = -1):
        return Palette([Color.from_md_value(val) for val in vals], id_ = id_)
    
    @staticmethod
    def from_rgb_values(vals, mode = 'argb', id_ = -1):
        return Palette([Color.from_rgb_value(val, mode) for val in vals], id_ = id_)

    def __str__(self):
        res = '\n'.join([str(col) for col in self.colors])
        return res

    def set_id(self, id_ = -1):
        if id_ >= 0:
            self.id_ = id_
        elif self.id_ < 0:
            self.id_ = Palette._current_id_
            Palette._current_id_ += 1
#        print 'registering palette %d' % self.id_
        Palette._registration_[self.id_] = self
    
    @staticmethod
    def get_by_id(id_):
        if id_ in Palette._registration_.keys():
            return Palette._registration_[id_]
        print ("There's no palette %d" % id_)
        print (Palette._registration_)
        print (Palette._registration_.keys())
#        exit()
    
    @staticmethod
    def get_palettes():
        return Palette._registration_.values()
    
    def to_pygame_palette(self):
        return [pygame.Color(*color.rgb_value) for color in self.colors]
    
    def __getitem__(self, val):
        return self.colors[val]
        
    @staticmethod
    def from_buffer(buf, pos=None):
        if pos:
            buf.save_state()
            buf.set_index(pos)
        res = []
        for _ in range(16):
            color = buf.read_w()
            res += [color]
        if pos:
            buf.restore_state()
        return Palette.from_md_values(res)
    
    def to_surface(self,
                   width = 256,
                   colors_per_row = 8, 
                   crossed = []):
        rgba_pal = [pygame.Color(*color.rgb_value) for color in self.colors] #
        color_square_size = width / colors_per_row
        height = 16 / colors_per_row
        if 16 % colors_per_row:
            height += 1
        height *= color_square_size
        
        res = pygame.Surface((width, height), depth = 8)
        
        x = 0
        y = 0
        for i in range(16):
            res.fill(i, rect = (x, y, color_square_size, color_square_size))
            if i in crossed:
                pygame.draw.line(res, 
                                 0, 
                                 (x + 2, y + 2), 
                                 (x + color_square_size - 2, y + color_square_size - 2), 
                                 2)
                pygame.draw.line(res, 
                                 0, 
                                 (x + color_square_size - 2, y + 2), 
                                 (x + 2, y + color_square_size - 2), 
                                 2)
            x += color_square_size
            if x >= width:
                x = 0
                y += color_square_size
        
        res.set_palette(rgba_pal)
        
        return res
    
    def export_to_bmp(self, path,
                 width = 256,
                 colors_per_row = 8, 
                 crossed = []):
        pygame.image.save(self.to_surface(width, colors_per_row), path, crossed = crossed)
    
    def export_to_png(self, path,
                 width = 256,
                 colors_per_row = 8,
                 crossed = []):
        bmp = self.to_surface(width, colors_per_row, crossed = crossed)
        res = pygame.Surface((bmp.get_width(), bmp.get_height()))
        
        res.blit(bmp, (0, 0))
        pygame.image.save(res, path)
            
    def get_nearest(self, color):
        if color in self.replacement_table:
            indice, diff = self.replacement_table[color]
            self.diff_min = diff
            return indice

        r, g, b = color.rgb_value
        
        diff_min = 1000000
        ind = 0

        for col in self.colors:
            r1, g1, b1 = col.rgb_value
            diff = (r1 - r)**2 + (g1 - g)**2 + (b1 - b)**2
            if diff < diff_min:
                ind_min = ind
                diff_min = diff
            ind += 1
        
        self.replacement_table[color] = (ind_min, diff_min)
        self.diff_min = diff_min
        
        return ind_min
    
    @staticmethod
    def from_png(path,
                 colors_per_row = 8):
        img = pygame.image.load(path)
        
        dx = img.get_width() / colors_per_row
        
        res = []
        x = y = 0
        for i in range(16):
            c = img.get_at((x, y))
            res += [Color.from_rgb_list(c.r, c.g, c.b)] #
            
            x += dx
            if x >= img.get_width():
                x = 0
                y += dx
        
        return Palette(res) #
    
    @staticmethod
    def from_txt(path):
        f = open(path, 'r')
        lines = f.readlines()
        f.close()
        
        res = [(0, 0, 0, 0)] * 16
        for line in lines:
            x = line.index(':')
            i = int(line[:x], 16)
            c = int(line[x + 1:], 16)
            res[i] = c
        
        return Palette.from_rgb_values(res)
    
    def export_to_string(self, show_stats = False):
        res = '// palette\n'
        if self.id_ >= 0:
            res += 'id = %d\n' % self.id_
        for i in range(16):
            res += '%X = %03X' % (i, self.colors[i].md_value)
            if show_stats:
                if i not in self.used_colors:
                    res += '\t// unused'
            res += '\n'
        
        res += '// end palette\n'
        return res
    
    @staticmethod
    def import_from_string(t):
        data = [0] * 16
        id_ = -1
        for field in [f for f in t.split('\n') if not f.startswith('//')]:
#            print 'palette:', field
            if '=' in field:
                left, right = field.split('=')
                
                left = left.strip()
                right = right.strip()
                
                if left in ['0', '1', '2', '3', '4', '5', '6', '7',
                            '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']:
                    data[int(left, 16)] = int(right, 16)
                elif left == 'id':
                    id_ = int(right)
        
        return Palette(colors = [Color.from_md_value(val) for val in data],
                       id_ = id_)
    
    @staticmethod
    def load(path):
        f = open(path, 'r')
        content = f.read()
        f.close()
        
        return Palette.import_from_string(content)
    
    def save(self, path, show_stats = False):
        path, _ = os.path.splitext(path)
        f = open(path + '.palette.txt', 'w')
        f.write(self.export_to_string(show_stats))
        f.close()            
    
regen_palette = Palette.from_md_values([0x000, 0x00A, 0x0A0, 0x0AA,
                                        0xA00, 0xA0A, 0xAA0, 0xAAA,
                                        0xEA7, 0xEAA, 0xEEE, 0x777,
                                        0x444, 0x00E, 0x0E0, 0x0EE])

if __name__ == '__main__':
    c1 = Color.from_md_value(0xACE)
    print (c1)
    
    c2 = Color.from_rgb_value(0x6b0f08)
    print (c2)
    
    for color in regen_palette:
        print (color)
