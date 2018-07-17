class Factory(object):
    def create(self, page_type):
        return eval(page_type.capitalize())()
