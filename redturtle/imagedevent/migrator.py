# -*- coding: utf-8 -*-

from plone.app.blob.migrations import migrate

def migrateImagedEvent(context):
    return migrate(context, meta_type = "ATEvent")
