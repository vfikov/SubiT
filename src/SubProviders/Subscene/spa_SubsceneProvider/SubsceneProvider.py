from SubProviders.Subscene import ISubsceneProvider

class SubsceneProvider(ISubsceneProvider.ISubsceneProvider):
    PROVIDER_NAME = 'Spanish - www.subscene.com'
    SELECTED_LANGUAGE = ISubsceneProvider.SUBSCENE_LANGUAGES.SPANISH

    def __init__(self):
        # Set the language
        super(SubsceneProvider, self).__init__()