# -*- coding: utf-8 -*-

import os

from zope.interface import implements
from zope.component import getUtility
from Products.Five.browser import BrowserView
from Products.CMFCore import utils
from Products.CMFCore.utils import getToolByName

from Products.Archetypes.Field import FileField, StringField, TextField

from Products.Archetypes.Storage import AttributeStorage
from Products.Archetypes.Storage.annotation import AnnotationStorage

class ImagedEventView(BrowserView):
    """An event view with the image and caption"""
    



