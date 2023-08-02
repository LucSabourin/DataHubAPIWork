class Messages:
    """ Class to facilitate collecting error messages.  Supports error message templates,
    severity indicators, and formatting.

    Parameters:
        templates: a dictionary whose keys are the template messages names, and whose items
        are 2 item tuples with the first item being a template string, the second item being
        an integer error severity.
    """

    def __init__(self, templates) -> None:
        self.templates = {}
        self.errors = []
        self.templates.update(templates)

    def add_message(self, template_key: str, *args):
        """Appends a formatted error message to the list of errors"""
        if template_key in self.templates.keys():
            template, severity = self.templates[template_key]
            message = str(severity) + ' -> ' + template.format(*args)
            self.errors.append(message)
        else:
            raise MissingMessageTemplate(template_key)

class MissingMessageTemplate(Exception):
    """
    """

    def __init__(self, template_key):
        self.message = '***!!No Message Template Exists For {}!!***'.format(template_key)
        super().__init__(self.message)

