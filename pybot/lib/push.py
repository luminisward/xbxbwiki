from dokuwiki import DokuWiki, DokuWikiError
from lib.page import PageFactory
from lib.parser import ParserFactory

class Push():
    def __init__(self, page_type=None, data=None, wiki_config=None):
        self.__data = data
        self.parser = ParserFactory().create(page_type)
        self.page = PageFactory().create(page_type)
        self.wiki = self.create_wiki_instance(wiki_config)

    def preprocess(self):
        self.parser.source_data = self.__data
        self.parser.process()
        self.__data = self.parser.result

    @staticmethod
    def create_wiki_instance(site_config):
        try:
            wiki = DokuWiki(
                site_config['SITEURL'],
                site_config['USERNAME'],
                site_config['PASSWORD'],
                cookieAuth=True
            )

        except KeyError:
            # 未匹配到mywiki.py配置中的站点
            print('Invalid site.')

        except DokuWikiError:
            print('Username or password is wrong ,can\'t access wiki.')

        except ModuleNotFoundError:
            print('找不到config')

        else:
            return wiki

    def execute(self):

        self.preprocess()

        for data_row in self.__data:
            self.page.data = data_row
            self.page.build_wikitext()
            self.wiki.pages.set(self.page.path, self.page.get_wikitext())
            print(self.page.path)
