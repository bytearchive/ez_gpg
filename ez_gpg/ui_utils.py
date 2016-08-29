# vim:ff=unix ts=4 sw=4 expandtab

import gi
import sys
import traceback

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

class UiUtils(object):
    @staticmethod
    def show_unimplemented_message_box(window):
        UiUtils.show_dialog(window,
                            "This functionality is not yet implemented!",
                            "Not Implemented")

    @staticmethod
    def show_dialog(window, message, title="EzGpG", message_type=Gtk.MessageType.WARNING):
        dialog = Gtk.MessageDialog(window, 0,
                                   message_type,
                                   Gtk.ButtonsType.OK,
                                   title)
        dialog.format_secondary_text(message)

        response = dialog.run()

        dialog.destroy()

    @staticmethod
    def _set_keyfile_filter(dialog):
        filter_keys = Gtk.FileFilter()
        filter_keys.set_name("Armored keys")
        filter_keys.add_pattern("*.asc")
        filter_keys.add_pattern("*.key")
        filter_keys.add_pattern("*.pub")
        dialog.add_filter(filter_keys)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    @staticmethod
    def get_filename(window, title="Open..."):
        dialog = Gtk.FileChooserDialog(title,
                                       window,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN,
                                        Gtk.ResponseType.OK))

        dialog.set_default_response(Gtk.ResponseType.OK)
        UiUtils._set_keyfile_filter(dialog)

        response = dialog.run()

        filename = None
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()

        dialog.destroy()
        return filename

    @staticmethod
    def _set_save_keyfile_filter(dialog):
        filter_armor_key = Gtk.FileFilter()
        filter_armor_key.set_name("Armored key")
        filter_armor_key.add_pattern("*.asc")
        dialog.add_filter(filter_armor_key)

        filter_binary_key = Gtk.FileFilter()
        filter_binary_key.set_name("Encoded key")
        filter_binary_key.add_pattern("*.gpg")
        dialog.add_filter(filter_binary_key)

    def get_save_filename(window, filename, title="Save..."):
        print(filename)
        dialog = Gtk.FileChooserDialog(title,
                                       window,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE,
                                        Gtk.ResponseType.ACCEPT))

        dialog.set_default_response(Gtk.ResponseType.OK)
        dialog.set_do_overwrite_confirmation(True)
        dialog.set_filename(filename)
        UiUtils._set_save_keyfile_filter(dialog)

        response = dialog.run()

        filename = None
        armor = True
        if response == Gtk.ResponseType.ACCEPT:
            filename = dialog.get_filename()

            if dialog.get_filter().get_name() == 'Encoded key':
                armor = False

            # Suffix the filename
            if not (filename.endswith('.asc') or filename.endswith('.gpg')):
                suffix = '.asc'
                if not armor:
                    suffix = '.gpg'

                filename += suffix

            print("Filename chosen as:", filename)

        dialog.destroy()
        return filename, armor

    @staticmethod
    def confirm_dialog(window, message):
        dialog = Gtk.MessageDialog(window, 0,
                                   Gtk.MessageType.QUESTION,
                                   Gtk.ButtonsType.YES_NO,
                                   "EzGPG")

        dialog.format_secondary_text(message)
        dialog.set_default_response(Gtk.ResponseType.NO)

        response = dialog.run()
        dialog.destroy()

        return response == Gtk.ResponseType.YES

class error_wrapper(object):
    """Error handler decorator"""
    def __init__(self, func):
        self.func = func

    def _show_error(self, error, stack_trace):
        # Print details on console
        traceback.print_exception(*stack_trace)

        msg = Gtk.MessageDialog(message_type=Gtk.MessageType.ERROR,
                                buttons=Gtk.ButtonsType.CLOSE,
                                message_format="Type: %s" % error.__class__.__name__)
        msg.set_title("Unhandled Error")
        msg.format_secondary_text("Description: %s" % error.__str__())

        msg.run()
        msg.destroy()

    def __call__(self, *args, **kargs):
        try:
            return self.func(*args, **kargs)
        except Exception as error:
            exc_info = sys.exc_info()
            self._show_error(error, exc_info)
