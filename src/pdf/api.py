# -*- coding: utf-8 -*-

"""
The add bookmark api for a pdf file.

public:

- class: Pdf(path)

"""

import os

from pypdf import PdfWriter, PdfReader


class Pdf(object):
    """
    Add bookmarks to a pdf file.

    Usage:

    >>> from src.pdf import Pdf

    read a exist pdf file:
    >>> p = Pdf('D:\\1.pdf')

    add a bookmark:
    >>> b0 = p.add_bookmark('First bookmark', 1)

    add a child bookmark to b0:
    >>> p.add_bookmark('Child bookmark', 2, parent=b0)

    save pdf:
    >>> p.save_pdf()

    the new pdf file will save to save directory with '1_new.pdf'

    """
    def __init__(self, path):
        self.path = path
        reader = PdfReader(open(path, "rb"), strict=False)
        self.writer = PdfWriter()
        # `clone_from=reader (clone_document_from_reader)` is slow when pdf is complex
        # `append_pages_from_reader` is fast but will lose annotations in pdf
        self.writer.append(reader)
        # Temporarily remove exist outline,
        # to prevent `'DictionaryObject' object has no attribute 'insert_child'` error
        # when adding bookmarks to some pdf which already have outline
        self.writer._root_object.pop("/Outlines", None)


    @property
    def _new_path(self):
        name, ext = os.path.splitext(self.path)
        return name + '_new' + ext

    def add_bookmark(self, title, pagenum, parent=None):
        """
        add a bookmark to pdf file with title and page num.
        if it's a child bookmark, add a parent argument.

        :Args

        title: str, the bookmark title.
        pagenum: int, the page num this bookmark refer to.
        parent: IndirectObject(the addBookmark() return object), the parent of this bookmark, the default is None.

        """
        return self.writer.add_outline_item(title, pagenum, parent=parent)

    def save_pdf(self):
        """save the writer to a pdf file with name 'name_new.pdf' """
        if os.path.exists(self._new_path):
            os.remove(self._new_path)
        with open(self._new_path, 'wb') as out:
            self.writer.write(out)
        return self._new_path
