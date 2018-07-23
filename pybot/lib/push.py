import os
import sys
from dokuwiki import DokuWiki, DokuWikiError
from tqdm import tqdm
from lib.page import PageFactory
from lib.parser import ParserFactory

class Push():
    def __init__(self, page_type=None, data=None, wiki_config=None):
        self.__data = data
        self.parser = ParserFactory(page_type).create()
        self.page = PageFactory(page_type).create()
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
            sys.exit('Invalid site.')

        except DokuWikiError:
            sys.exit('Username or password is wrong ,can\'t access wiki.')

        except ModuleNotFoundError:
            sys.exit('找不到config')

        else:
            return wiki

    def execute(self, dry_run=False):

        self.preprocess()

        data = tqdm(self.__data, position=1, dynamic_ncols=True)

        for data_row in data:
            self.page.data = data_row
            self.page.build_wikitext()

            space_line = ' ' * os.get_terminal_size().columns

            if dry_run:
                tqdm.write('Checking: {}'.format(self.page.path), end='\r')
                remote_wikitext = self.wiki.pages.get(self.page.path)
                tqdm.write(space_line, end='\r')

                if not remote_wikitext == self.page.get_wikitext():
                    tqdm.write(self.page.path)

            else:
                # flush last line and print new line
                tqdm.write(space_line, end='\r')
                tqdm.write('Pushing: {}'.format(self.page.path), end='\r')

                self.wiki.pages.set(self.page.path, self.page.get_wikitext())

        tqdm.write('\n')
