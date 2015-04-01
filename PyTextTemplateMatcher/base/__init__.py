class BaseMatcher(object):
    def __init__(self):
        self.text = None

    def load(self, filename):
        """
        Loads text from file
        :param str filename: the file from which text data should be loaded
        """
        with open(filename, "r") as f:
            text = f.read()
        self.loads(text)

    def loads(self, text):
        """
        Loads text from string
        :param str text: the text data
        """
        self.text = text

    def train(self, text=None):
        """
        Train a model given text data
        :param str text: Train a model using this text
        """
        print("super")
        text = text or self.text
        if text is None:
            raise ValueError("No text is loaded/provided, use load/loads(text) or train(text=text).")

class BaseSimpleRepr(object):
    def __repr__(self):
        return "<{:},{:}>".format(self.__class__.__name__, self.__dict__.__str__())