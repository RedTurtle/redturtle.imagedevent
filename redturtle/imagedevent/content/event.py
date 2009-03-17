"""Definition of the Event content type
"""

from zope.interface import implements, directlyProvides
from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.event import ATEvent
from Products.ATContentTypes.content.event import ATEventSchema

from Products.CMFCore import permissions

from Products.Archetypes.atapi import ImageField
from Products.Archetypes.atapi import ImageWidget
from Products.Archetypes.atapi import AnnotationStorage

from cciaa.contents import contentsMessageFactory as _
from cciaa.contents.interfaces import IEvent
from cciaa.contents.config import PROJECTNAME

from Products.ATContentTypes.configuration import zconf
from Products.validation.config import validation
from Products.validation.validators.SupplValidators import MaxSizeValidator
from Products.validation import V_REQUIRED

validation.register(MaxSizeValidator('checkNewsImageMaxSize',
                                     maxsize=zconf.ATNewsItem.max_file_size))

CCIAAEventSchema = ATEventSchema.copy() + atapi.Schema((

    ImageField('image',
        required = False,
        storage = AnnotationStorage(migrate=True),
        languageIndependent = True,
        max_size = zconf.ATNewsItem.max_image_dimension,
        sizes= {'large'   : (768, 768),
                'preview' : (400, 400),
                'mini'    : (200, 200),
                'thumb'   : (128, 128),
                'tile'    :  (64, 64),
                'icon'    :  (32, 32),
                'listing' :  (16, 16),
               },
        validators = (('isNonEmptyFile', V_REQUIRED),
                             ('checkNewsImageMaxSize', V_REQUIRED)),
        widget = ImageWidget(
            description = _(u'help_news_image', default=u'Will be shown in the news listing, and in the news item itself. Image will be scaled to a sensible size.'),
            label= _(u'label_news_image', default=u'Image'),
            show_content_type = False)
        ),

))

CCIAAEventSchema['title'].storage = atapi.AnnotationStorage()
CCIAAEventSchema['description'].storage = atapi.AnnotationStorage()

CCIAAEventSchema.moveField('image', after='text')

schemata.finalizeATCTSchema(CCIAAEventSchema, moveDiscussion=False)

class CCIAAEvent(ATEvent):
    """Information about an upcoming event, which can be displayed in the calendar."""
    implements(IEvent)

    meta_type = "Event"
    schema = CCIAAEventSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    security       = ClassSecurityInfo()

    security.declareProtected(permissions.View, 'tag')
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        if 'title' not in kwargs:
            kwargs['title'] = self.getImageCaption()
        return self.getField('image').tag(self, **kwargs)

    def __bobo_traverse__(self, REQUEST, name):
        """Transparent access to image scales
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return ATEvent.__bobo_traverse__(self, REQUEST, name)

atapi.registerType(CCIAAEvent, PROJECTNAME)
