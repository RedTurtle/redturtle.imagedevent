# -*- coding: utf-8 -*-

def uninstall(portal):
    setup_tool = portal.portal_setup
    setup_tool.setBaselineContext('profile-redturtle.imagedevent:uninstall')
    setup_tool.runAllImportStepsFromProfile('profile-redturtle.imagedevent:uninstall')
    return "Ran all uninstall steps."
