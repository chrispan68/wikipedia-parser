import xml.sax
import mwparserfromhell

class WikiXmlHandler(xml.sax.handler.ContentHandler):
    """Content handler for Wiki XML data using SAX"""
    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._people = []

    def get_summary(self, full_text):
        if full_text.find("==") == -1:
            return full_text
        return full_text[:full_text.index("==") - 1]
    def get_birth_year(self, wiki_year_string):
        query_strings = ['Birth date and age|', 'Birth year and age|', 'Birth date|']
        index = -1
        for query in query_strings:
            if wiki_year_string.find(query) > -1:
                index = max(index, wiki_year_string.find(query) + len(query))
        #extracts 4 digit years
        for i in range(index, len(wiki_year_string) - 4):
            if wiki_year_string[i:i+4].isdigit():
                return wiki_year_string[i:i+4]
        return 'ERROR'
    def process_article(self, title, text, template = 'Infobox person'):
        """Process a wikipedia article looking for template"""
        
        # Create a parsing object
        wikicode = mwparserfromhell.parse(text)
        
        # Search through templates for the template
        matches = wikicode.filter_templates(matches = template)
        raw_year_string = 'EMPTY'
        birth_year = 'EMPTY'
        infobox = ''
        if len(matches) >= 1:
            # Extract information from infobox
            for match in matches:
                infobox = str(match)
                for param in match.params:
                    if param.name.strip_code().strip() == 'birth_date':
                        raw_year_string = str(param.value)
                        birth_year = self.get_birth_year(raw_year_string)
            summary = self.get_summary(wikicode.strip_code().strip())
            return (title, birth_year, summary, raw_year_string, infobox)

    def characters(self, content):
        """Characters between opening and closing tags"""
        if self._current_tag:
            self._buffer.append(content)

    def startElement(self, name, attrs):
        """Opening tag of element"""
        if name in ('title', 'text'):
            self._current_tag = name
            self._buffer = []

    def endElement(self, name):
        """Closing tag of element"""
        if name == self._current_tag:
            self._values[name] = ' '.join(self._buffer)

        if name == 'page':
            person = self.process_article(**self._values, 
                               template = 'Infobox person')
            # If article is a book append to the list of books
            if person:
                self._people.append(person)

    