from SubProviders.OpenSubtitles import IOpenSubtitlesProvider
from SubProviders.OpenSubtitles.IOpenSubtitlesProvider import OPENSUBTITLES_LANGUAGES, OPENSUBTITLES_PAGES

class OpenSubtitlesProvider(IOpenSubtitlesProvider.IOpenSubtitlesProvider):
    PROVIDER_NAME = 'Norwegian - www.opensubtitles.org'

    def __init__(self):
        #Set the language
        OPENSUBTITLES_PAGES.LANGUAGE = OPENSUBTITLES_LANGUAGES.NORWEGIAN
        #Call to the ctor of the IOpenSubtitlesProvider
        super(OpenSubtitlesProvider, self).__init__()