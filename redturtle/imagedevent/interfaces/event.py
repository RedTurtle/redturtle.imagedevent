from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from cciaa.contents import contentsMessageFactory as _

from Products.ATContentTypes.interface import IATEvent

class IEvent(IATEvent):
    """Information about an upcoming event, which can be displayed in the calendar."""
