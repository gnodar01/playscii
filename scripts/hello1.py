# hello1 test art script

#
# sets some test data. assumes: 8x8, 1 layer
#

self.add_layer(0.25)
self.add_layer(0.5)

# clear 1st layer to black, 2nd and 3rd to transparent
self.clear_frame_layer(0, 0, self.palette.darkest_index)
self.clear_frame_layer(0, 1)
self.clear_frame_layer(0, 2)
# write white text onto 3 layers
color = self.palette.lightest_index
self.write_string(0, 0, 1, 1, 'Hello.', color)
# draw snaky ring thingy
# color ramp: 2, 10, 6, 13, 14, 12, 3, back to 2
# top
self.set_tile_at(0, 1, 1, 3, 119, 2)
self.set_tile_at(0, 1, 2, 3, 102, 10)
self.set_tile_at(0, 1, 3, 3, 102, 6)
self.set_tile_at(0, 1, 4, 3, 102, 13)
self.set_tile_at(0, 1, 5, 3, 120, 14)
# sides
self.set_tile_at(0, 1, 1, 4, 145, 3)
self.set_tile_at(0, 1, 5, 4, 145, 12)
self.set_tile_at(0, 1, 1, 5, 145, 12)
self.set_tile_at(0, 1, 5, 5, 145, 3)
# bottom
self.set_tile_at(0, 1, 1, 6, 121, 14)
self.set_tile_at(0, 1, 2, 6, 102, 13)
self.set_tile_at(0, 1, 3, 6, 102, 6)
self.set_tile_at(0, 1, 4, 6, 102, 10)
self.set_tile_at(0, 1, 5, 6, 122, 2)
# :]
char = self.charset.get_char_index(':')
self.set_tile_at(0, 2, 3, 4, char, color)
char = self.charset.get_char_index(']')
self.set_tile_at(0, 2, 4, 4, char, color)

# add frames and animate 'em
self.duplicate_frame(0)
self.duplicate_frame(0)
self.duplicate_frame(0)
self.duplicate_frame(0)
self.duplicate_frame(0)
self.duplicate_frame(0)

# cycle capitals through "hello" text
h = self.charset.get_char_index('h')
char = self.charset.get_char_index('E')
self.set_char_index_at(1, 0, 2, 1, char)
self.set_char_index_at(1, 0, 1, 1, h)
char = self.charset.get_char_index('L')
self.set_char_index_at(2, 0, 3, 1, char)
self.set_char_index_at(2, 0, 1, 1, h)
self.set_char_index_at(3, 0, 4, 1, char)
self.set_char_index_at(3, 0, 1, 1, h)
char = self.charset.get_char_index('O')
self.set_char_index_at(4, 0, 5, 1, char)
self.set_char_index_at(4, 0, 1, 1, h)
char = self.charset.get_char_index('!')
self.set_char_index_at(5, 0, 6, 1, char)
self.set_char_index_at(5, 0, 1, 1, h)
self.set_char_index_at(6, 0, 1, 1, h)
# make smiley go from ;] to :D
char = self.charset.get_char_index(';')
self.set_char_index_at(3, 2, 3, 4, char)
self.set_char_index_at(4, 2, 3, 4, char)
self.set_char_index_at(5, 2, 3, 4, char)
char = self.charset.get_char_index('D')
self.set_char_index_at(3, 2, 4, 4, char)
self.set_char_index_at(4, 2, 4, 4, char)
self.set_char_index_at(5, 2, 4, 4, char)
# cycle colors for snaky thing
#
# frame 1 top
#
self.set_color_at(1, 1, 1, 3, 10)
self.set_color_at(1, 1, 2, 3, 6)
self.set_color_at(1, 1, 3, 3, 13)
self.set_color_at(1, 1, 4, 3, 14)
self.set_color_at(1, 1, 5, 3, 12)
# frame 1 sides
self.set_color_at(1, 1, 1, 4, 2)
self.set_color_at(1, 1, 5, 4, 3)
self.set_color_at(1, 1, 1, 5, 3)
self.set_color_at(1, 1, 5, 5, 2)
# frame 1 bottom
self.set_color_at(1, 1, 1, 6, 12)
self.set_color_at(1, 1, 2, 6, 14)
self.set_color_at(1, 1, 3, 6, 13)
self.set_color_at(1, 1, 4, 6, 6)
self.set_color_at(1, 1, 5, 6, 10)
#
# frame 2 top
#
self.set_color_at(2, 1, 1, 3, 6)
self.set_color_at(2, 1, 2, 3, 13)
self.set_color_at(2, 1, 3, 3, 14)
self.set_color_at(2, 1, 4, 3, 12)
self.set_color_at(2, 1, 5, 3, 3)
# frame 2 sides
self.set_color_at(2, 1, 1, 4, 10)
self.set_color_at(2, 1, 5, 4, 2)
self.set_color_at(2, 1, 1, 5, 2)
self.set_color_at(2, 1, 5, 5, 10)
# frame 2 bottom
self.set_color_at(2, 1, 1, 6, 3)
self.set_color_at(2, 1, 2, 6, 12)
self.set_color_at(2, 1, 3, 6, 14)
self.set_color_at(2, 1, 4, 6, 13)
self.set_color_at(2, 1, 5, 6, 6)
#
# frame 3 top
#
self.set_color_at(3, 1, 1, 3, 13)
self.set_color_at(3, 1, 2, 3, 14)
self.set_color_at(3, 1, 3, 3, 12)
self.set_color_at(3, 1, 4, 3, 3)
self.set_color_at(3, 1, 5, 3, 2)
# frame 3 sides
self.set_color_at(3, 1, 1, 4, 6)
self.set_color_at(3, 1, 5, 4, 10)
self.set_color_at(3, 1, 1, 5, 10)
self.set_color_at(3, 1, 5, 5, 6)
# frame 3 bottom
self.set_color_at(3, 1, 1, 6, 2)
self.set_color_at(3, 1, 2, 6, 3)
self.set_color_at(3, 1, 3, 6, 12)
self.set_color_at(3, 1, 4, 6, 14)
self.set_color_at(3, 1, 5, 6, 13)
#
# frame 4 top
#
self.set_color_at(4, 1, 1, 3, 14)
self.set_color_at(4, 1, 2, 3, 12)
self.set_color_at(4, 1, 3, 3, 3)
self.set_color_at(4, 1, 4, 3, 2)
self.set_color_at(4, 1, 5, 3, 10)
# frame 4 sides
self.set_color_at(4, 1, 1, 4, 13)
self.set_color_at(4, 1, 5, 4, 6)
self.set_color_at(4, 1, 1, 5, 6)
self.set_color_at(4, 1, 5, 5, 13)
# frame 4 bottom
self.set_color_at(4, 1, 1, 6, 10)
self.set_color_at(4, 1, 2, 6, 2)
self.set_color_at(4, 1, 3, 6, 3)
self.set_color_at(4, 1, 4, 6, 12)
self.set_color_at(4, 1, 5, 6, 14)
#
# frame 5 top
#
self.set_color_at(5, 1, 1, 3, 12)
self.set_color_at(5, 1, 2, 3, 3)
self.set_color_at(5, 1, 3, 3, 2)
self.set_color_at(5, 1, 4, 3, 10)
self.set_color_at(5, 1, 5, 3, 6)
# frame 5 sides
self.set_color_at(5, 1, 1, 4, 14)
self.set_color_at(5, 1, 5, 4, 13)
self.set_color_at(5, 1, 1, 5, 13)
self.set_color_at(5, 1, 5, 5, 14)
# frame 5 bottom
self.set_color_at(5, 1, 1, 6, 6)
self.set_color_at(5, 1, 2, 6, 10)
self.set_color_at(5, 1, 3, 6, 2)
self.set_color_at(5, 1, 4, 6, 3)
self.set_color_at(5, 1, 5, 6, 12)
#
# frame 6 top
#
self.set_color_at(6, 1, 1, 3, 3)
self.set_color_at(6, 1, 2, 3, 2)
self.set_color_at(6, 1, 3, 3, 10)
self.set_color_at(6, 1, 4, 3, 6)
self.set_color_at(6, 1, 5, 3, 13)
# frame 6 sides
self.set_color_at(6, 1, 1, 4, 12)
self.set_color_at(6, 1, 5, 4, 14)
self.set_color_at(6, 1, 1, 5, 14)
self.set_color_at(6, 1, 5, 5, 12)
# frame 6 bottom
self.set_color_at(6, 1, 1, 6, 13)
self.set_color_at(6, 1, 2, 6, 6)
self.set_color_at(6, 1, 3, 6, 10)
self.set_color_at(6, 1, 4, 6, 2)
self.set_color_at(6, 1, 5, 6, 3)
