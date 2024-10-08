
import os, time, json

from PIL import Image

from texture import Texture
from ui_chooser_dialog import ChooserDialog, ChooserItem, ChooserItemButton
from ui_console import OpenCommand, LoadCharSetCommand, LoadPaletteCommand
from ui_art_dialog import PaletteFromFileDialog, ImportOptionsDialog
from art import ART_DIR, ART_FILE_EXTENSION, THUMBNAIL_CACHE_DIR, SCRIPT_FILE_EXTENSION, ART_SCRIPT_DIR
from palette import Palette, PALETTE_DIR, PALETTE_EXTENSIONS
from charset import CharacterSet, CHARSET_DIR, CHARSET_FILE_EXTENSION
from image_export import write_thumbnail


class BaseFileChooserItem(ChooserItem):
    
    hide_file_extension = False
    
    def get_short_dir_name(self):
        # name should end in / but don't assume
        dir_name = self.name[:-1] if self.name.endswith('/') else self.name
        return os.path.basename(dir_name) + '/'
    
    def get_label(self):
        if os.path.isdir(self.name):
            return self.get_short_dir_name()
        else:
            label = os.path.basename(self.name)
            if self.hide_file_extension:
                return os.path.splitext(label)[0]
            else:
                return label
    
    def get_description_lines(self):
        if os.path.isdir(self.name):
            if self.name == '..':
                return ['[parent folder]']
            # TODO: # of items in dir?
            return []
        return None
    
    def picked(self, element):
        # if this is different from the last clicked item, pick it
        if element.selected_item_index != self.index:
            ChooserItem.picked(self, element)
            element.first_selection_made = True
            return
        # if we haven't yet clicked something in this view, require another
        # click before opening it (consistent double click behavior for
        # initial selections)
        if not element.first_selection_made:
            element.first_selection_made = True
            return
        if self.name == '..' and self.name != '/':
            new_dir = os.path.abspath(os.path.abspath(element.current_dir) + '/..')
            element.change_current_dir(new_dir)
        elif os.path.isdir(self.name):
            new_dir = element.current_dir + self.get_short_dir_name()
            element.change_current_dir(new_dir)
        else:
            element.confirm_pressed()
        element.first_selection_made = False

class BaseFileChooserDialog(ChooserDialog):
    
    "base class for choosers whose items correspond with files"
    chooser_item_class = BaseFileChooserItem
    show_filenames = True
    file_extensions = []
    
    def set_initial_dir(self):
        self.current_dir = self.ui.app.documents_dir
        self.field_texts[self.active_field] = self.current_dir
    
    def get_filenames(self):
        "subclasses override: get list of desired filenames"
        return self.get_sorted_dir_list()
    
    def get_sorted_dir_list(self):
        "common code for getting sorted directory + file lists"
        # list parent, then dirs, then filenames with extension(s)
        parent = [] if self.current_dir == '/' else ['..']
        if not os.path.exists(self.current_dir):
            return parent
        dirs, files = [], []
        for filename in os.listdir(self.current_dir):
            # skip unix-hidden files
            if filename.startswith('.'):
                continue
            full_filename = self.current_dir + filename
            # if no extensions specified, take any file
            if len(self.file_extensions) == 0:
                self.file_extensions = ['']
            for ext in self.file_extensions:
                if os.path.isdir(full_filename):
                    dirs += [full_filename + '/']
                    break
                elif filename.lower().endswith(ext.lower()):
                    files += [full_filename]
                    break
        dirs.sort(key=lambda x: x.lower())
        files.sort(key=lambda x: x.lower())
        return parent + dirs + files
    
    def get_items(self):
        "populate and return items from list of files, loading as needed"
        items = []
        # find all suitable files (images)
        filenames = self.get_filenames()
        # use manual counter, as we skip past some files that don't fit
        i = 0
        for filename in filenames:
            item = self.chooser_item_class(i, filename)
            if not item.valid:
                continue
            items.append(item)
            i += 1
        return items


#
# art chooser
#

class ArtChooserItem(BaseFileChooserItem):
    
    # set in load()
    art_width = None
    hide_file_extension = True
    
    def get_description_lines(self):
        lines = BaseFileChooserItem.get_description_lines(self)
        if lines is not None:
            return lines
        if not self.art_width:
            return []
        mod_time = time.gmtime(self.art_mod_time)
        mod_time = time.strftime('%Y-%m-%d %H:%M:%S', mod_time)
        lines = ['last change: %s' % mod_time]
        line = '%s x %s, ' % (self.art_width, self.art_height)
        line += '%s frame' % self.art_frames
        # pluralize properly
        line += 's' if self.art_frames > 1 else ''
        line += ', %s layer' % self.art_layers
        line += 's' if self.art_layers > 1 else ''
        lines += [line]
        lines += ['char: %s, pal: %s' % (self.art_charset, self.art_palette)]
        return lines
    
    def get_preview_texture(self, app):
        if os.path.isdir(self.name):
            return
        thumbnail_filename = app.cache_dir + THUMBNAIL_CACHE_DIR + self.art_hash + '.png'
        # create thumbnail if it doesn't exist
        if not os.path.exists(thumbnail_filename):
            write_thumbnail(app, self.name, thumbnail_filename)
        # read thumbnail
        img = Image.open(thumbnail_filename)
        img = img.convert('RGBA')
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        return Texture(img.tobytes(), *img.size)
    
    def load(self, app):
        if os.path.isdir(self.name):
            return
        if not os.path.exists(self.name):
            return
        # get last modified time for description
        self.art_mod_time = os.path.getmtime(self.name)
        # get file's hash for unique thumbnail name
        self.art_hash = app.get_file_hash(self.name)
        # rather than load the entire art, just get some high level stats
        d = json.load(open(self.name))
        self.art_width, self.art_height = d['width'], d['height']
        self.art_frames = len(d['frames'])
        self.art_layers = len(d['frames'][0]['layers'])
        self.art_charset = d['charset']
        self.art_palette = d['palette']


class ArtChooserDialog(BaseFileChooserDialog):
    
    title = 'Open art'
    confirm_caption = 'Open'
    cancel_caption = 'Cancel'
    chooser_item_class = ArtChooserItem
    flip_preview_y = False
    directory_aware = True
    file_extensions = [ART_FILE_EXTENSION]
    
    def set_initial_dir(self):
        # TODO: IF no art in Documents dir yet, start in app/art/ for examples?
        # get last opened dir, else start in docs/game art dir
        if self.ui.app.last_art_dir:
            self.current_dir = self.ui.app.last_art_dir
        else:
            self.current_dir = self.ui.app.gw.game_dir if self.ui.app.gw.game_dir else self.ui.app.documents_dir
            self.current_dir += ART_DIR
        self.field_texts[self.active_field] = self.current_dir
    
    def confirm_pressed(self):
        if not os.path.exists(self.field_texts[0]):
            return
        self.ui.app.last_art_dir = self.current_dir
        OpenCommand.execute(self.ui.console, [self.field_texts[0]])
        self.dismiss()


#
# generic file chooser for importers
#
class GenericImportChooserDialog(BaseFileChooserDialog):
    
    title = 'Import %s'
    confirm_caption = 'Import'
    cancel_caption = 'Cancel'
    # allowed extensions set by invoking 
    file_extensions = []
    show_preview_image = False
    directory_aware = True
    
    def __init__(self, ui, options):
        self.title %= ui.app.importer.format_name
        self.file_extensions = ui.app.importer.allowed_file_extensions
        BaseFileChooserDialog.__init__(self, ui, options)
    
    def set_initial_dir(self):
        if self.ui.app.last_import_dir:
            self.current_dir = self.ui.app.last_import_dir
        else:
            self.current_dir = self.ui.app.documents_dir
        self.field_texts[self.active_field] = self.current_dir
    
    def confirm_pressed(self):
        filename = self.field_texts[0]
        if not os.path.exists(filename):
            return
        self.ui.app.last_import_dir = self.current_dir
        self.dismiss()
        # importer might offer a dialog for options
        if self.ui.app.importer.options_dialog_class:
            options = {'filename': filename}
            self.ui.open_dialog(self.ui.app.importer.options_dialog_class,
                                options)
        else:
            ImportOptionsDialog.do_import(self.ui.app, filename, {})


class ImageChooserItem(BaseFileChooserItem):
    
    def get_preview_texture(self, app):
        if os.path.isdir(self.name):
            return
        # may not be a valid image file
        try:
            img = Image.open(self.name)
        except:
            return
        try:
            img = img.convert('RGBA')
        except:
            # (probably) PIL bug: some images just crash! return None
            return
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        return Texture(img.tobytes(), *img.size)

class ImageFileChooserDialog(BaseFileChooserDialog):
    
    cancel_caption = 'Cancel'
    chooser_item_class = ImageChooserItem
    flip_preview_y = False
    directory_aware = True
    file_extensions = ['png', 'jpg', 'jpeg', 'bmp', 'gif']

class PaletteFromImageChooserDialog(ImageFileChooserDialog):
    
    title = 'Palette from image'
    confirm_caption = 'Choose'
    
    def confirm_pressed(self):
        if not os.path.exists(self.field_texts[0]):
            return
        # open new dialog, pipe our field 0 into its field 0
        filename = self.field_texts[0]
        self.dismiss()
        self.ui.open_dialog(PaletteFromFileDialog)
        self.ui.active_dialog.field_texts[0] = filename
        # base new palette filename on source image
        palette_filename = os.path.basename(filename)
        palette_filename = os.path.splitext(palette_filename)[0]
        self.ui.active_dialog.field_texts[1] = palette_filename

#
# palette chooser
#

class PaletteChooserItem(BaseFileChooserItem):
    
    def get_label(self):
        return os.path.splitext(self.name)[0]
    
    def get_description_lines(self):
        colors = len(self.palette.colors)
        return ['Unique colors: %s' % str(colors - 1)]
    
    def get_preview_texture(self, app):
        return self.palette.src_texture
    
    def load(self, app):
        self.palette = app.load_palette(self.name)


class PaletteChooserDialog(BaseFileChooserDialog):
    
    title = 'Choose palette'
    chooser_item_class = PaletteChooserItem
    
    def get_initial_selection(self):
        if not self.ui.active_art:
            return 0
        for item in self.items:
            # depend on label being same as palette's internal name,
            # eg filename minus extension
            if item.label == self.ui.active_art.palette.name:
                return item.index
        #print("couldn't find initial selection for %s, returning 0" % self.__class__.__name__)
        return 0
    
    def get_filenames(self):
        filenames = []
        # search all files in dirs with appropriate extensions
        for dirname in self.ui.app.get_dirnames(PALETTE_DIR, False):
            for filename in os.listdir(dirname):
                for ext in PALETTE_EXTENSIONS:
                    if filename.lower().endswith(ext.lower()):
                        filenames.append(filename)
        filenames.sort(key=lambda x: x.lower())
        return filenames
    
    def confirm_pressed(self):
        item = self.get_selected_item()
        self.ui.active_art.set_palette(item.palette, log=True)
        self.ui.popup.set_active_palette(item.palette)

#
# charset chooser
#

class CharsetChooserItem(BaseFileChooserItem):
    
    def get_label(self):
        return os.path.splitext(self.name)[0]
    
    def get_description_lines(self):
        # first comment in file = description
        lines = []
        for line in open(self.charset.filename, encoding='utf-8').readlines():
            line = line.strip()
            if line.startswith('//'):
                lines.append(line[2:])
                break
        lines.append('Characters: %s' % str(self.charset.last_index))
        return lines
    
    def get_preview_texture(self, app):
        return self.charset.texture
    
    def load(self, app):
        self.charset = app.load_charset(self.name)


class CharSetChooserDialog(BaseFileChooserDialog):
    
    title = 'Choose character set'
    flip_preview_y = False
    chooser_item_class = CharsetChooserItem
    
    def get_initial_selection(self):
        if not self.ui.active_art:
            return 0
        for item in self.items:
            if item.label == self.ui.active_art.charset.name:
                return item.index
        #print("couldn't find initial selection for %s, returning 0" % self.__class__.__name__)
        return 0
    
    def get_filenames(self):
        filenames = []
        # search all files in dirs with appropriate extensions
        for dirname in self.ui.app.get_dirnames(CHARSET_DIR, False):
            for filename in os.listdir(dirname):
                if filename.lower().endswith(CHARSET_FILE_EXTENSION.lower()):
                    filenames.append(filename)
        filenames.sort(key=lambda x: x.lower())
        return filenames
    
    def confirm_pressed(self):
        item = self.get_selected_item()
        self.ui.active_art.set_charset(item.charset, log=True)
        self.ui.popup.set_active_charset(item.charset)
        # change in charset aspect should be treated as a resize
        # for purposes of grid, camera, cursor, overlay
        self.ui.adjust_for_art_resize(self.ui.active_art)


class ArtScriptChooserItem(BaseFileChooserItem):
    
    def get_label(self):
        label = os.path.splitext(self.name)[0]
        return os.path.basename(label)
    
    def get_description_lines(self):
        lines = []
        # read every comment line until a non-comment line is encountered
        for line in self.script.readlines():
            line = line.strip()
            if not line:
                continue
            if not line.startswith('#'):
                break
            # snip #
            line = line[line.index('#')+1:]
            lines.append(line)
        return lines
    
    def load(self, app):
        self.script = open(self.name)


class RunArtScriptDialog(BaseFileChooserDialog):
    
    title = 'Run Artscript'
    tile_width, big_width = 70, 90
    tile_height, big_height = 15, 25
    chooser_item_class = ArtScriptChooserItem
    show_preview_image = False
    
    def get_filenames(self):
        filenames = []
        # search all files in dirs with appropriate extensions
        for dirname in self.ui.app.get_dirnames(ART_SCRIPT_DIR, False):
            for filename in os.listdir(dirname):
                if filename.lower().endswith(SCRIPT_FILE_EXTENSION.lower()):
                    filenames.append(dirname + filename)
        filenames.sort(key=lambda x: x.lower())
        return filenames
    
    def confirm_pressed(self):
        item = self.get_selected_item()
        self.ui.app.last_art_script = item.name
        self.ui.active_art.run_script(item.name, log=False)
        self.dismiss()


class OverlayImageFileChooserDialog(ImageFileChooserDialog):
    
    title = 'Choose overlay image'
    confirm_caption = 'Choose'
    
    def confirm_pressed(self):
        filename = self.field_texts[0]
        self.ui.app.set_overlay_image(filename)
        self.dismiss()
