from renderable import LAYER_VIS_FULL, LAYER_VIS_DIM, LAYER_VIS_NONE

from ui_tool import PencilTool, EraseTool, RotateTool, GrabTool, TextTool, SelectTool, PasteTool

#
# specific pulldown menu items, eg File > Save, Edit > Copy
#

class PulldownMenuItem:
    # label that displays for this item
    label = 'Test Menu Item'
    # bindable command we look up from InputLord to get binding text from
    command = 'test_command'
    # if not None, passed to button's cb_arg
    cb_arg = None
    # if True, pulldown button creation process won't auto-pad
    no_pad = False
    # if True, item will never be dimmed
    always_active = False
    # if True, pulldown will close when this item is selected
    close_on_select = False
    # item is allowed in Art Mode
    art_mode_allowed = True
    # item is allowed in Game Mode
    game_mode_allowed = True
    def should_dim(app):
        "returns True if this item should be dimmed based on current application state"
        # so many commands are inapplicable with no active art, default to dimming an
        # item if this is the case
        return app.ui.active_art is None
    def get_label(app):
        "returns custom generated label based on app state"
        return None

class SeparatorItem(PulldownMenuItem):
    "menu separator, non-interactive and handled specially by menu drawing"
    pass

class ArtModePulldownMenuItem(PulldownMenuItem):
    # unless overridden, art mode items not allowed in game mode
    game_mode_allowed = False

#
# file menu
#
class FileNewItem(ArtModePulldownMenuItem):
    label = 'New…'
    command = 'new_art'
    always_active = True

class FileOpenItem(ArtModePulldownMenuItem):
    label = 'Open…'
    command = 'open_art'
    always_active = True

class FileSaveItem(ArtModePulldownMenuItem):
    label = 'Save'
    command = 'save_current'
    def should_dim(app):
        return not app.ui.active_art or not app.ui.active_art.unsaved_changes

class FileSaveAsItem(ArtModePulldownMenuItem):
    label = 'Save As…'
    command = 'save_art_as'
    def should_dim(app):
        return app.ui.active_art is None

class FileCloseItem(ArtModePulldownMenuItem):
    label = 'Close'
    command = 'close_art'
    def should_dim(app):
        return app.ui.active_art is None

class FileRevertItem(ArtModePulldownMenuItem):
    label = 'Revert'
    command = 'revert_art'
    def should_dim(app):
        return app.ui.active_art is None or not app.ui.active_art.unsaved_changes

class FileImportItem(ArtModePulldownMenuItem):
    label = 'Import…'
    command = 'import_file'
    always_active = True

class FileExportItem(ArtModePulldownMenuItem):
    label = 'Export…'
    command = 'export_file'
    def should_dim(app):
        return app.ui.active_art is None

class FileExportLastItem(ArtModePulldownMenuItem):
    label = 'Export last'
    command = 'export_file_last'
    def should_dim(app):
        return app.ui.active_art is None

class FileConvertImageItem(ArtModePulldownMenuItem):
    label = 'Convert Image…'
    command = 'convert_image'
    def should_dim(app):
        return app.ui.active_art is None

class FileQuitItem(ArtModePulldownMenuItem):
    label = 'Quit'
    command = 'quit'
    always_active = True
    game_mode_allowed = True

#
# edit menu
#
class EditUndoItem(ArtModePulldownMenuItem):
    label = 'Undo'
    command = 'undo'
    def should_dim(app):
        return not app.ui.active_art or len(app.ui.active_art.command_stack.undo_commands) == 0

class EditRedoItem(ArtModePulldownMenuItem):
    label = 'Redo'
    command = 'redo'
    def should_dim(app):
        return not app.ui.active_art or len(app.ui.active_art.command_stack.redo_commands) == 0

class EditCutItem(ArtModePulldownMenuItem):
    label = 'Cut'
    command = 'cut_selection'
    def should_dim(app):
        return len(app.ui.select_tool.selected_tiles) == 0

class EditCopyItem(ArtModePulldownMenuItem):
    label = 'Copy'
    command = 'copy_selection'
    def should_dim(app):
        return len(app.ui.select_tool.selected_tiles) == 0

class EditPasteItem(ArtModePulldownMenuItem):
    label = 'Paste'
    command = 'select_paste_tool'
    def should_dim(app):
        return len(app.ui.clipboard) == 0

class EditDeleteItem(ArtModePulldownMenuItem):
    label = 'Clear'
    command = 'erase_selection_or_art'

class EditSelectAllItem(ArtModePulldownMenuItem):
    label = 'Select All'
    command = 'select_all'

class EditSelectNoneItem(ArtModePulldownMenuItem):
    label = 'Select None'
    command = 'select_none'

class EditSelectInvertItem(ArtModePulldownMenuItem):
    label = 'Invert Selection'
    command = 'select_invert'

class EditPreferences(ArtModePulldownMenuItem):
    label = 'Preferences…'
    command = 'edit_cfg'

#
# tool menu
#

class ToolTogglePickerItem(ArtModePulldownMenuItem):
    # two spaces in front of each label to leave room for mark
    label = 'Show char/color picker'
    command = 'toggle_picker'

class ToolTogglePickerHoldItem(ArtModePulldownMenuItem):
    label = 'blah'
    command = 'toggle_picker_hold'
    def get_label(app):
        return 'Picker toggle key: %s' % ['press', 'hold'][app.ui.popup_hold_to_show]

class ToolSwapSelectedColors(ArtModePulldownMenuItem):
    label = 'Swap selected fg/bg colors'
    command = 'swap_fg_bg_colors'

class ToolToggleArtToolbar(ArtModePulldownMenuItem):
    label = '  Show toolbar'
    command = 'toggle_art_toolbar'
    def should_mark(ui):
        return ui.art_toolbar.visible

class ToolPaintItem(ArtModePulldownMenuItem):
    # two spaces in front of each label to leave room for mark
    label = '  %s' % PencilTool.button_caption
    command = 'select_pencil_tool'

class ToolEraseItem(ArtModePulldownMenuItem):
    label = '  %s' % EraseTool.button_caption
    command = 'select_erase_tool'

class ToolRotateItem(ArtModePulldownMenuItem):
    label = '  %s' % RotateTool.button_caption
    command = 'select_rotate_tool'

class ToolGrabItem(ArtModePulldownMenuItem):
    label = '  %s' % GrabTool.button_caption
    command = 'select_grab_tool'

class ToolTextItem(ArtModePulldownMenuItem):
    label = '  %s' % TextTool.button_caption
    command = 'select_text_tool'

class ToolSelectItem(ArtModePulldownMenuItem):
    label = '  %s' % SelectTool.button_caption
    command = 'select_select_tool'

class ToolPasteItem(ArtModePulldownMenuItem):
    label = '  %s' % PasteTool.button_caption
    command = 'select_paste_tool'

class ToolIncreaseBrushSizeItem(ArtModePulldownMenuItem):
    label = 'blah'
    command = 'increase_brush_size'
    def should_dim(app):
        # dim this item for tools where brush size doesn't apply
        if not app.ui.active_art or not app.ui.selected_tool.brush_size:
            return True
    def get_label(app):
        if not app.ui.selected_tool.brush_size:
            return 'Increase brush size'
        size = app.ui.selected_tool.brush_size + 1
        return 'Increase brush size to %s' % size

class ToolDecreaseBrushSizeItem(ArtModePulldownMenuItem):
    label = 'blah'
    command = 'decrease_brush_size'
    def should_dim(app):
        if not app.ui.active_art or not app.ui.selected_tool.brush_size:
            return True
        return app.ui.selected_tool.brush_size <= 1
    def get_label(app):
        if not app.ui.selected_tool.brush_size:
            return 'Decrease brush size'
        size = app.ui.selected_tool.brush_size - 1
        return 'Decrease brush size to %s' % size

class ToolSettingsItem(ArtModePulldownMenuItem):
    # base class for tool settings toggle items
    def should_dim(app):
        # blacklist specific tools
        return not app.ui.active_art or type(app.ui.selected_tool) in [SelectTool]

class ToolToggleAffectsCharItem(ToolSettingsItem):
    label = '  Affects: character'
    command = 'toggle_affects_char'
    def should_mark(ui):
        return ui.selected_tool.affects_char

class ToolToggleAffectsFGItem(ToolSettingsItem):
    label = '  Affects: foreground color'
    command = 'toggle_affects_fg'
    def should_mark(ui):
        return ui.selected_tool.affects_fg_color

class ToolToggleAffectsBGItem(ToolSettingsItem):
    label = '  Affects: background color'
    command = 'toggle_affects_bg'
    def should_mark(ui):
        return ui.selected_tool.affects_bg_color

class ToolToggleAffectsXformItem(ToolSettingsItem):
    label = '  Affects: character xform'
    command = 'toggle_affects_xform'
    def should_mark(ui):
        return ui.selected_tool.affects_xform

#
# view  menu
#
class ViewToggleCRTItem(ArtModePulldownMenuItem):
    label = '  CRT filter'
    command = 'toggle_crt'
    game_mode_allowed = True
    def should_dim(app):
        return app.fb.disable_crt
    def should_mark(ui):
        return ui.app.fb.crt

class ViewToggleGridItem(ArtModePulldownMenuItem):
    label = '  Grid'
    command = 'toggle_grid_visibility'
    game_mode_allowed = True
    def should_mark(ui):
        return ui.app.grid.visible

class ViewBGTextureItem(ArtModePulldownMenuItem):
    label = '  Textured background'
    command = 'toggle_bg_texture'
    always_active = True
    def should_mark(ui):
        return ui.app.show_bg_texture

class ViewToggleZoomExtentsItem(ArtModePulldownMenuItem):
    label = '  Zoom to Art extents'
    command = 'toggle_zoom_extents'
    def should_mark(ui):
        return ui.active_art and ui.active_art.camera_zoomed_extents

class ViewZoomInItem(ArtModePulldownMenuItem):
    label = 'Zoom in'
    command = 'camera_zoom_in_proportional'

class ViewZoomOutItem(ArtModePulldownMenuItem):
    label = 'Zoom out'
    command = 'camera_zoom_out_proportional'

class ViewSetZoomItem(ArtModePulldownMenuItem):
    label = 'Set camera zoom…'
    command = 'set_camera_zoom'

class ViewToggleCameraTiltItem(ArtModePulldownMenuItem):
    label = '  Camera tilt'
    command = 'toggle_camera_tilt'
    always_active = True
    game_mode_allowed = True
    def should_mark(ui):
        return ui.app.camera.y_tilt != 0

class ViewSetOverlayImageItem(ArtModePulldownMenuItem):
    label = 'Set overlay image…'
    command = 'select_overlay_image'

class ViewToggleOverlayImageItem(ArtModePulldownMenuItem):
    label = '  Toggle overlay image'
    command = 'toggle_overlay_image'
    def should_mark(ui):
        return ui.app.draw_overlay
    def should_dim(app):
        return app.overlay_renderable is None

class ViewSetOverlayImageOpacityItem(ArtModePulldownMenuItem):
    label = 'Set overlay image opacity…'
    command = 'set_overlay_image_opacity'
    def should_dim(app):
        return app.overlay_renderable is None or not app.draw_overlay

class ViewSetOverlayImageScalingItem(ArtModePulldownMenuItem):
    label = 'blah'
    command = 'set_overlay_image_scaling'
    def get_label(app):
        return 'Overlay image scaling: %s' % ['width', 'height', 'fill'][app.overlay_scale_type]
    def should_dim(app):
        return app.overlay_renderable is None or not app.draw_overlay

#
# art menu
#
class ArtOpenAllGameAssetsItem(ArtModePulldownMenuItem):
    label = 'Open all Game Mode assets'
    command = 'open_all_game_assets'
    def should_dim(app):
        return len(app.gw.objects) == 0

class ArtPreviousItem(ArtModePulldownMenuItem):
    label = 'Previous Art'
    command = 'previous_art'
    def should_dim(app):
        return len(app.art_loaded_for_edit) < 2

class ArtNextItem(ArtModePulldownMenuItem):
    label = 'Next Art'
    command = 'next_art'
    def should_dim(app):
        return len(app.art_loaded_for_edit) < 2

class ArtCropToSelectionItem(ArtModePulldownMenuItem):
    label = 'Crop to selection'
    command = 'crop_to_selection'
    def should_dim(app):
        return len(app.ui.select_tool.selected_tiles) == 0

class ArtResizeItem(ArtModePulldownMenuItem):
    label = 'Resize…'
    command = 'resize_art'

class ArtFlipHorizontal(ArtModePulldownMenuItem):
    label = 'Flip horizontally'
    command = 'art_flip_horizontal'

class ArtFlipVertical(ArtModePulldownMenuItem):
    label = 'Flip vertically'
    command = 'art_flip_vertical'

class ArtToggleFlipAffectsXforms(ArtModePulldownMenuItem):
    label = '  Flip affects xforms'
    command = 'art_toggle_flip_affects_xforms'
    def should_mark(ui):
        return ui.flip_affects_xforms

class ArtRunScriptItem(ArtModePulldownMenuItem):
    label = 'Run Artscript…'
    command = 'run_art_script'
    
class ArtRunLastScriptItem(ArtModePulldownMenuItem):
    label = 'Run last Artscript'
    command = 'run_art_script_last'
    def should_dim(app):
        return app.last_art_script is None

#
# frame menu
#
class FramePreviousItem(ArtModePulldownMenuItem):
    label = 'Previous frame'
    command = 'previous_frame'
    def should_dim(app):
        return not app.ui.active_art or app.ui.active_art.frames < 2

class FrameNextItem(ArtModePulldownMenuItem):
    label = 'Next frame'
    command = 'next_frame'
    def should_dim(app):
        return not app.ui.active_art or app.ui.active_art.frames < 2

class FrameTogglePlaybackItem(ArtModePulldownMenuItem):
    label = 'blah'
    command = 'toggle_anim_playback'
    def should_dim(app):
        return not app.ui.active_art or app.ui.active_art.frames < 2
    def get_label(app):
        if not app.ui.active_art:
            return 'Start animation playback'
        animating = app.ui.active_art.renderables[0].animating
        return ['Start', 'Stop'][animating] + ' animation playback'

class FrameToggleOnionItem(ArtModePulldownMenuItem):
    label = 'blah'
    command = 'toggle_onion_visibility'
    def should_dim(app):
        return not app.ui.active_art or app.ui.active_art.frames < 2
    def get_label(app):
        l = '%s onion skin frames' % ['Show', 'Hide'][app.onion_frames_visible]
        return l

class FrameCycleOnionFramesItem(ArtModePulldownMenuItem):
    label = 'blah'
    command = 'cycle_onion_frames'
    def should_dim(app):
        return not app.ui.active_art or app.ui.active_art.frames < 2
    def get_label(app):
        return 'Number of onion frames: %s' % app.onion_show_frames

class FrameCycleOnionDisplayItem(ArtModePulldownMenuItem):
    label = 'blah'
    command = 'cycle_onion_ahead_behind'
    def should_dim(app):
        return not app.ui.active_art or app.ui.active_art.frames < 2
    def get_label(app):
        if app.onion_show_frames_behind and app.onion_show_frames_ahead:
            display = 'Next & Previous'
        elif app.onion_show_frames_behind:
            display = 'Previous'
        else:
            display = 'Next'
        return 'Onion frames show: %s' % display

class FrameAddFrameItem(ArtModePulldownMenuItem):
    label = 'Add frame…'
    command = 'add_frame'

class FrameDuplicateFrameItem(ArtModePulldownMenuItem):
    label = 'Duplicate this frame…'
    command = 'duplicate_frame'

class FrameChangeDelayItem(ArtModePulldownMenuItem):
    label = "Change this frame's hold time…"
    command = 'change_frame_delay'

class FrameChangeDelayAllItem(ArtModePulldownMenuItem):
    label = "Change all frames' hold times…"
    command = 'change_frame_delay_all'

class FrameChangeIndexItem(ArtModePulldownMenuItem):
    label = "Change this frame's index…"
    command = 'change_frame_index'

class FrameDeleteFrameItem(ArtModePulldownMenuItem):
    label = 'Delete this frame'
    command = 'delete_frame'
    def should_dim(app):
        # don't delete last frame
        return not app.ui.active_art or app.ui.active_art.frames < 2

#
# layer menu
#
class LayerAddItem(ArtModePulldownMenuItem):
    label = "Add layer…"
    command = 'add_layer'

class LayerDuplicateItem(ArtModePulldownMenuItem):
    label = "Duplicate this layer…"
    command = 'duplicate_layer'

class LayerSetNameItem(ArtModePulldownMenuItem):
    label = "Change this layer's name…"
    command = 'change_layer_name'

class LayerSetZItem(ArtModePulldownMenuItem):
    label = "Change this layer's Z-depth…"
    command = 'change_layer_z'

class LayerToggleVisibleItem(ArtModePulldownMenuItem):
    label = 'blah'
    command = 'toggle_layer_visibility'
    def get_label(app):
        if not app.ui.active_art:
            return 'Show this layer (Game Mode)'
        visible = app.ui.active_art.layers_visibility[app.ui.active_art.active_layer]
        return ['Show', 'Hide'][visible] + ' this layer (Game Mode)'

class LayerDeleteItem(ArtModePulldownMenuItem):
    label = "Delete this layer"
    command = 'delete_layer'
    def should_dim(app):
        return not app.ui.active_art or app.ui.active_art.layers < 2

class LayerSetInactiveVizItem(ArtModePulldownMenuItem):
    label = 'blah'
    command = 'cycle_inactive_layer_visibility'
    def should_dim(app):
        return not app.ui.active_art or app.ui.active_art.layers < 2
    def get_label(app):
        l = 'Inactive layers: '
        if app.inactive_layer_visibility == LAYER_VIS_FULL:
            return l + 'Visible'
        elif app.inactive_layer_visibility == LAYER_VIS_DIM:
            return l + 'Dim'
        elif app.inactive_layer_visibility == LAYER_VIS_NONE:
            return l + 'Invisible'

class LayerShowHiddenItem(ArtModePulldownMenuItem):
    label = 'blah'
    command = 'toggle_hidden_layers_visible'
    def get_label(app):
        l = 'Art Mode-only layers: '
        l += ['Hidden', 'Visible'][app.show_hidden_layers]
        return l

class LayerPreviousItem(ArtModePulldownMenuItem):
    label = 'Previous layer'
    command = 'previous_layer'
    def should_dim(app):
        return not app.ui.active_art or app.ui.active_art.layers < 2

class LayerNextItem(ArtModePulldownMenuItem):
    label = 'Next layer'
    command = 'next_layer'
    def should_dim(app):
        return not app.ui.active_art or app.ui.active_art.layers < 2

#
# char/color menu
#
class ChooseCharSetItem(ArtModePulldownMenuItem):
    label = 'Choose character set…'
    command = 'choose_charset'

class ChoosePaletteItem(ArtModePulldownMenuItem):
    label = 'Choose palette…'
    command = 'choose_palette'

class PaletteFromImageItem(ArtModePulldownMenuItem):
    label = 'Palette from image…'
    command = 'palette_from_file'
    always_active = True

#
# help menu
#
class HelpDocsItem(ArtModePulldownMenuItem):
    label = 'Help (in browser)'
    command = 'open_help_docs'
    always_active = True
    close_on_select = True
    game_mode_allowed = True

class HelpGenerateDocsItem(ArtModePulldownMenuItem):
    label = 'Generate documentation'
    command = 'generate_docs'
    close_on_select = True
    def should_dim(app):
        return not app.pdoc_available

class HelpWebsiteItem(ArtModePulldownMenuItem):
    label = 'Playscii website'
    command = 'open_website'
    always_active = True
    close_on_select = True

#
# menu data
#
class PulldownMenuData:
    "data for pulldown menus, eg File, Edit, etc; mainly a list of menu items"
    items = []
    def should_mark_item(item, ui):
        "returns True if this item should be marked, subclasses have custom logic here"
        return False
    def get_items(app):
        """
        returns a list of items generated from app state, used for
        dynamically-generated items
        """
        return []

class FileMenuData(PulldownMenuData):
    items = [FileNewItem, FileOpenItem, FileSaveItem, FileSaveAsItem,
             FileCloseItem, FileRevertItem, SeparatorItem, FileImportItem,
             FileExportItem, FileExportLastItem, SeparatorItem, FileQuitItem]

class EditMenuData(PulldownMenuData):
    items = [EditUndoItem, EditRedoItem, SeparatorItem,
             EditCutItem, EditCopyItem, EditPasteItem, EditDeleteItem,
             SeparatorItem, EditSelectAllItem,
             EditSelectNoneItem, EditSelectInvertItem, SeparatorItem,
             EditPreferences]

class ToolMenuData(PulldownMenuData):
    items = [ToolTogglePickerItem, ToolTogglePickerHoldItem,
             ToolSwapSelectedColors, ToolToggleArtToolbar, SeparatorItem,
             ToolPaintItem, ToolEraseItem, ToolRotateItem, ToolGrabItem,
             ToolTextItem, ToolSelectItem, ToolPasteItem, SeparatorItem,
             ToolIncreaseBrushSizeItem, ToolDecreaseBrushSizeItem,
             ToolToggleAffectsCharItem, ToolToggleAffectsFGItem,
             ToolToggleAffectsBGItem, ToolToggleAffectsXformItem]
             # TODO: cycle char/color/xform items?
    # TODO: generate list from UI.tools instead of manually specified MenuItems
    def should_mark_item(item, ui):
        # if it's a tool setting toggle, use its own mark check function
        if item.__bases__[0] is ToolSettingsItem:
            return item.should_mark(ui)
        elif hasattr(item, 'should_mark'): # toolbar toggle, etc
            return item.should_mark(ui)
        return item.label == '  %s' % ui.selected_tool.button_caption

class ViewMenuData(PulldownMenuData):
    items = [ViewToggleCRTItem, ViewToggleGridItem, ViewBGTextureItem,
             SeparatorItem,
             ViewToggleZoomExtentsItem, ViewZoomInItem, ViewZoomOutItem,
             ViewSetZoomItem, ViewToggleCameraTiltItem, SeparatorItem,
             ViewSetOverlayImageItem, ViewToggleOverlayImageItem,
             ViewSetOverlayImageOpacityItem, ViewSetOverlayImageScalingItem
            ]
    
    def should_mark_item(item, ui):
        if hasattr(item, 'should_mark'):
            return item.should_mark(ui)
        return False

class ArtMenuData(PulldownMenuData):
    items = [ArtResizeItem, ArtCropToSelectionItem,
             ArtFlipHorizontal, ArtFlipVertical, ArtToggleFlipAffectsXforms,
             SeparatorItem,
             ArtRunScriptItem, ArtRunLastScriptItem, SeparatorItem,
             ArtOpenAllGameAssetsItem, SeparatorItem,
             ArtPreviousItem, ArtNextItem, SeparatorItem]
    
    def should_mark_item(item, ui):
        "show checkmark for active art"
        if hasattr(item, 'should_mark'):
            return item.should_mark(ui)
        return ui.active_art and ui.active_art.filename == item.cb_arg
    
    def get_items(app):
        "turn each loaded art into a menu item"
        items = []
        for art in app.art_loaded_for_edit:
            # class just being used to store data, no need to spawn it
            class TempMenuItemClass(ArtModePulldownMenuItem): pass
            item = TempMenuItemClass
            # leave spaces for mark
            item.label = '  %s' % art.filename
            item.command = 'art_switch_to'
            item.cb_arg = art.filename
            # order list by art's time loaded
            item.time_loaded = art.time_loaded
            items.append(item)
        items.sort(key=lambda item: item.time_loaded)
        return items


class FrameMenuData(PulldownMenuData):
    items = [FrameAddFrameItem, FrameDuplicateFrameItem,
             FrameChangeDelayItem, FrameChangeDelayAllItem,
             FrameChangeIndexItem, FrameDeleteFrameItem, SeparatorItem,
             FrameTogglePlaybackItem, FramePreviousItem, FrameNextItem,
             SeparatorItem,
             FrameToggleOnionItem, FrameCycleOnionFramesItem,
             FrameCycleOnionDisplayItem]


class LayerMenuData(PulldownMenuData):
    
    items = [LayerAddItem, LayerDuplicateItem, LayerSetNameItem, LayerSetZItem,
             LayerDeleteItem, SeparatorItem,
             LayerSetInactiveVizItem, LayerPreviousItem,LayerNextItem,
             SeparatorItem, LayerToggleVisibleItem, LayerShowHiddenItem,
             SeparatorItem]
    
    def should_mark_item(item, ui):
        "show checkmark for active art"
        if not ui.active_art:
            return False
        return ui.active_art.active_layer == item.cb_arg
    
    def get_items(app):
        "turn each layer into a menu item"
        items = []
        if not app.ui.active_art:
            return items
        # first determine longest line to set width of items
        longest_line = 0
        for layer_name in app.ui.active_art.layer_names:
            if len(layer_name) > longest_line:
                longest_line = len(layer_name)
        # check non-generated menu items too
        for item in LayerMenuData.items:
            if len(item.label) + 1 > longest_line:
                longest_line = len(item.label) + 1
        # cap at max allowed line length
        longest_line = min(longest_line, 50)
        for i,layer_name in enumerate(app.ui.active_art.layer_names):
            class TempMenuItemClass(ArtModePulldownMenuItem): pass
            item = TempMenuItemClass
            # leave spaces for mark
            item.label = '  %s' % layer_name
            if not app.ui.active_art.layers_visibility[i]:
                item.label += ' (hidden)'
            # pad, put Z depth on far right
            item.label = item.label.ljust(longest_line)
            # trim to keep below a max length
            item.label = item.label[:longest_line]
            # spaces between layer name and z depth
            item.label += 'z:%.2f' % app.ui.active_art.layers_z[i]
            # tell PulldownMenu's button creation process not to auto-pad
            item.no_pad = True
            item.command = 'layer_switch_to'
            item.cb_arg = i
            items.append(item)
        return items

class CharColorMenuData(PulldownMenuData):
    items = [ChooseCharSetItem, ChoosePaletteItem, SeparatorItem,
             PaletteFromImageItem]

class HelpMenuData(PulldownMenuData):
    items = [HelpDocsItem, HelpGenerateDocsItem, HelpWebsiteItem]
