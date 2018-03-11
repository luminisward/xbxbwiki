import dokuwiki

wiki = dokuwiki.DokuWiki('http://siteurl','USERNAME','PASSWORD')

print(wiki.title)
