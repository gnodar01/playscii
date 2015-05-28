import os

from ui_button import UIButton, TEXT_RIGHT
from ui_edit_panel import GamePanel
from ui_dialog import UIDialog
from ui_colors import UIColors


class ResetObjectButton(UIButton):
    caption = 'Reset object properties'
    caption_justify = TEXT_RIGHT
    def selected(button):
        world = button.element.world
        world.reset_object_in_place(world.selected_objects[0])


class EditObjectPropertyDialog(UIDialog):
    
    "dialog invoked by panel property click, modified at runtime as needed"
    base_title = 'Set %s'
    fields = 1
    field0_base_label = 'New %s for %s:'
    confirm_caption = 'Set'
    game_mode_visible = True
    
    def is_input_valid(self):
        try: self.field0_type(self.get_field_text(0))
        except: return False, ''
        return True, None
    
    def confirm_pressed(self):
        valid, reason = self.is_input_valid()
        if not valid: return
        # set property for selected object(s)
        new_value = self.field0_type(self.get_field_text(0))
        for obj in self.ui.app.gw.selected_objects:
            if hasattr(obj, self.item.prop_name):
                setattr(obj, self.item.prop_name, new_value)
        self.dismiss()


class EditObjectPropertyButton(UIButton):
    caption_justify = TEXT_RIGHT


class PropertyItem:
    multi_value_text = '[various]'
    
    def __init__(self, prop_name):
        self.prop_name = prop_name
        # property value & type filled in after creation
        self.prop_value = None
        self.prop_type = None
    def set_value(self, value):
        # convert value to a button-friendly string
        if type(value) is float:
            valstr = '%.3f' % value
            # non-fixed decimal version may be shorter, if so use it
            if len(str(value)) < len(valstr):
                valstr = str(value)
        elif type(value) is str:
            # file? shorten to basename minus extension
            if os.path.exists:
                valstr = os.path.basename(value)
                valstr = os.path.splitext(valstr)[0]
            else:
                valstr = value
        else:
            valstr = str(value)
        # if values vary across objects use [various]
        if self.prop_value is not None and self.prop_value != valstr:
            self.prop_value = self.multi_value_text
        else:
            self.prop_value = valstr


class EditObjectPanel(GamePanel):
    
    "panel showing info for selected game object"
    tile_width = 32
    tile_height = 18
    snap_right = True
    text_left = False
    base_button_classes = [ResetObjectButton]
    
    def __init__(self, ui):
        self.base_buttons = []
        self.property_buttons = []
        GamePanel.__init__(self, ui)
    
    def create_buttons(self):
        # buttons for persistent unique commands, eg reset object
        for i,button_class in enumerate(self.base_button_classes):
            button = button_class(self)
            button.caption += ' '
            button.width = self.tile_width
            button.y = i + 1
            button.callback = button.selected
            if button.clear_before_caption_draw:
                button.refresh_caption()
            self.base_buttons.append(button)
        def callback(item=None):
            if not item: return
            self.clicked_item(item)
        for y in range(self.tile_height - len(self.base_buttons) - 1):
            button = EditObjectPropertyButton(self)
            button.y = y + len(self.base_buttons) + 1
            # button.cb_arg set in refresh_items
            button.callback = callback
            # below properties reset every update
            button.caption = str(y + 1)
            button.width = 10
            self.property_buttons.append(button)
        self.buttons = self.base_buttons[:] + self.property_buttons[:]
    
    def clicked_item(self, item):
        # if property is a bool just toggle/set it, no need for a dialog
        if item.prop_type is bool:
            for obj in self.world.selected_objects:
                # if multiple object values vary, set it True
                if item.prop_value == PropertyItem.multi_value_text:
                    setattr(obj, item.prop_name, True)
                else:
                    val = getattr(obj, item.prop_name)
                    setattr(obj, item.prop_name, not val)
            return
        # set dialog values appropriate to property being edited
        EditObjectPropertyDialog.title = EditObjectPropertyDialog.base_title % item.prop_name
        EditObjectPropertyDialog.field0_label = EditObjectPropertyDialog.field0_base_label % (item.prop_type.__name__, item.prop_name)
        EditObjectPropertyDialog.field0_type = item.prop_type or str
        x = self.ui.width_tiles - self.tile_width
        x -= EditObjectPropertyDialog.tile_width
        # give dialog a handle to item
        EditObjectPropertyDialog.item = item
        self.ui.open_dialog(EditObjectPropertyDialog, x, self.tile_y)
        self.ui.active_dialog.field0_text = str(item.prop_value)
    
    def get_label(self):
        # if 1 object seleted, show its name; if >1 selected, show #
        selected = len(self.world.selected_objects)
        # panel shouldn't draw when nothing selected, fill in anyway
        if selected == 0:
            return '[nothing selected]'
        elif selected == 1 and self.world.selected_objects[0]:
            return self.world.selected_objects[0].name
        else:
            return '[%s selected]' % selected
    
    def refresh_items(self):
        if len(self.world.selected_objects) == 0:
            return
        # get list of unique properties across all selected objects
        propnames = []
        for obj in self.world.selected_objects:
            for propname in obj.serialized:
                if not propname in propnames:
                    propnames.append(propname)
        # build list of items from properties
        items = []
        for propname in propnames:
            item = PropertyItem(propname)
            for obj in self.world.selected_objects:
                if hasattr(obj, propname):
                    # fill in type and value
                    if item.prop_type is None:
                        item.prop_type = type(getattr(obj, propname))
                    item.set_value(getattr(obj, propname))
            items.append(item)
        # set each line
        for i,b in enumerate(self.property_buttons):
            item = None
            if i < len(items):
                item = items[i]
            self.draw_property_line(b, i, item)
        self.draw_buttons()
    
    def draw_property_line(self, button, button_index, item):
        "set button + label appearance correctly"
        y = button_index + len(self.base_buttons) + 1
        self.art.clear_line(0, 0, y, self.fg_color, self.bg_color)
        if item is None:
            button.caption = ''
            button.cb_arg = None
            button.can_hover = False
            return
        # set button caption, width, x based on value
        button.caption = '%s ' % item.prop_value
        button.width = len(button.caption) + 1
        button.x = self.tile_width - button.width
        button.cb_arg = item
        button.can_hover = True
        # set non-button text to the left correctly
        x = button.x + 1
        label = '%s: ' % item.prop_name
        self.art.write_string(0, 0, x, y, label, UIColors.darkgrey, None, True)
    
    def update(self):
        # redraw contents every update
        self.draw_titlebar()
        #if len(self.world.selected_objects) > 0:
        self.refresh_items()
        GamePanel.update(self)
    
    def render(self):
        if len(self.world.selected_objects) > 0:
            GamePanel.render(self)
