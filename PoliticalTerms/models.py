from django.db import models
import datetime
import feedparser

# Create your models here.
from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.contents import RichTextContent
from feincms.module.medialibrary.contents import MediaFileContent

Page.register_extensions(
    'feincms.extensions.ct_tracker',
    'feincms.module.page.extensions.navigationgroups',
    'feincms.extensions.seo',
    'feincms.module.page.extensions.symlinks',


)  # Example set of extensions

Page.register_templates({
    'title': _('Political Terms'),
    'path': 'base.html',
    'regions': (
        ('Header',_('Header'),'inherited'),
        ('LSidebar', _('Left Sidebar'), 'inherited'),
        ('Content', _('Main Content'), 'inherited'),
        ('RSidebar', _('Right Sidebar'), 'inherited'),
        ('Footer',_('Footer'),'inherited'),
        ('SubFooter',_('SubFooter'),'inherited'),
    ),
})

class PoliticalParty(models.Model):
    Party = models.CharField(max_length=200,primary_key=True)
    PoliticalPosition = models.CharField(max_length=200)
    Leader = models.CharField(max_length=200)
    # Membership Count
    UKHouseofCommons = models.IntegerField(verbose_name="UK House Of Commons Member Count")
    ScottishParliament = models.IntegerField(verbose_name="Scottish Parliament Member Count")
    NationalAssemblyforWales = models.IntegerField(verbose_name="Welsh Assembly Member Count")
    NorthernIrelandAssembly = models.IntegerField(verbose_name="Northern Ireland Assembly Membership Count")
    LondonAssembly = models.IntegerField(verbose_name="Northern Ireland Assembly Membership Count")
    EuropeanParliament = models.IntegerField(verbose_name="European Parliament Membership Count")
    LocalGovernment = models.IntegerField(verbose_name="Local Council Seats Held")
    PartyMembers = models.IntegerField(verbose_name="Total Party Members")
    LatestElectionVoteShare = models.FloatField()
    Notes = models.TextField()

class PrimeMinister(models.Model):

    FirstName = models.CharField(max_length=200)
    Surname = models.CharField(max_length=200,primary_key=True)
    PortraitURL = models.URLField()
    Honorifics = models.CharField(max_length=200)
    Constituency = models.CharField(max_length=200)
    Birth = models.DateField(verbose_name="Birth Date")
    Death = models.DateField(verbose_name="Date of Death")
    PoliticalParty = models.ForeignKey(PoliticalParty)
    CoalitionDeputyOnly = models.BooleanField(default=False,verbose_name="Was Only Ever A Coalition Deputy Prime Minister?")

    def __str__(self):
        return str(self.FirstName + self.Surname)

    def __unicode__(self):
        return str(self.FirstName + self.Surname)

class LegislationTypes(models.Model):
    Description = models.TextField()
    DocumentMainType = models.CharField(max_length=300)
    DocTypeCode = models.CharField(max_length=5,primary_key=True)

    def __str__(self):
        return self.Description

    def __unicode__(self):
            return self.Description


class PoliticalTerm(models.Model):
    TermStart = models.DateField('Political Term Start')
    TermEnd = models.DateField('Political Term End')
    PrimeMinister = models.ForeignKey(PrimeMinister)
    PartyMajority = models.ForeignKey(PoliticalParty)
    Type = models.ForeignKey(LegislationTypes)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.cleaned_data()['TermStart'].strftime('%d%m%y') + self.cleaned_data()['TermStart'].strftime('%d%m%y')

    def __str__(self):
            return self.cleaned_data()['TermStart'].strftime('%d%m%y') + self.cleaned_data()['TermStart'].strftime('%d%m%y')

    def get_government_name(self):
        return str(self.cleaned_data()['PrimeMinister']) + " " + self.cleaned_data()['TermStart'].strftime('%d%m%y') + self.cleaned_data()['TermStart'].strftime('%d%m%y')


    def render(self,**kwargs):
        url = 'http://www.legislation.gov.uk/search?type=%s&start-year=%s&end-year=%i&start-number=%i&end-number=%i&version=%i' % (str(self.type),datetime.date(self.TermStart).year,datetime.date(self.TermEnd).year)
        # http://www.legislation.gov.uk/search?type={type}&start-year={year}&end-year={year}&start-number={number}&end-number={number}&version={version}

        return feedparser.parse(url)


Page.create_content_type(RichTextContent)
Page.create_content_type(PoliticalTerm)
Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    # ('default', _('default')),
    ('lightbox', _('lightbox')),
))

"""
# Very stupid etag function, a page is supposed the unchanged as long
# as its id and slug do not change. You definitely want something more
# involved, like including last change dates or whatever.
def my_etag(page, request):
    return 'PAGE-%d-%s' % ( page.id, page.slug )
Page.etag = my_etag


Page.register_request_processors(Page.etag_request_processor)
Page.register_response_processors(Page.etag_response_processor)
"""