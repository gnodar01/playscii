
# mutate!
# change a random tile on a random layer

x = randint(0, self.width-1)
y = randint(0, self.height-1)
layer = randint(0, self.layers-1)
char = randint(0, 128)
color_index = self.palette.get_random_color_index()
self.set_char_index_at(0, layer, x, y, char)
self.set_color_at(0, layer, x, y, color_index)
color_index = self.palette.get_random_color_index()
self.set_color_at(0, layer, x, y, color_index, False)
