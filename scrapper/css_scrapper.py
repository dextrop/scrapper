import cssutils

HTML_TAGS = ["a", "abbr", "acronym", "address", "applet", "area", "article", "aside", "audio", "b", "base", "basefont", "bdi", "bdo", "big", "blockquote", "body", "br", "button", "canvas", "caption", "center", "cite", "code", "col", "colgroup", "data", "datalist", "dd", "del", "details", "dfn", "dialog", "dir", "div", "dl", "dt", "em", "embed", "fieldset", "figcaption", "figure", "font", "footer", "form", "frame", "frameset", "h1", "head", "header", "hr", "html", "i", "iframe", "img", "input", "ins", "kbd", "label", "legend", "li", "link", "main", "map", "mark", "meta", "meter", "nav", "noframes", "noscript", "object", "ol", "optgroup", "option", "output", "p", "param", "picture", "pre", "progress", "q", "rp", "rt", "ruby", "s", "samp", "script", "section", "select", "small", "source", "span", "strike", "strong", "style", "sub", "summary", "sup", "svg", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time", "title", "tr", "track", "tt", "u", "ul", "var", "video", "wbr"]
class CSSScrapper():
    def __init__(self, css_file_list, classes_to_scrap):
        self.css_file_list = css_file_list
        self.classes_to_scrap = classes_to_scrap
        self.css_content = ""

    def get_selectors(self, rule, class_name):
        try:
            selectors = str(rule.selectorText)
            selectors_arr = selectors.replace("#", "=#") \
                .replace(".", "=.").replace(" ", "") \
                .replace(">", "=").replace("~", "=") \
                .replace("+", "=").replace(",", "=").split("=")
            all_classes = []
            for selector in selectors_arr:
                if len(selector) > 0:
                    all_classes.append(selector.split(":")[0])

            return self.does_selector_exits(class_name, all_classes)
        except Exception as e:
            return None

    def does_selector_exits(self, class_name, selectors):
        """
        Check if class is present in selector
        2 rules for checking classname
        - .CLASSNAME exits ( eg .someclass )
        - .CLASSNAME: exits ( eg .someclass:focus )
        :param class_name: name of class to find
        :param selectors: list of all selectors
        :return: True / False
        """
        if "." + class_name in selectors:
            return True

        if "." + class_name + ":" in selectors:
            return True

        if "" in selectors:
            return True

        status = False

        for selector in selectors:
            if selector in HTML_TAGS:
                status = True

        return status

    def check_for_class(self, class_name, css_sheet):
        """
        Name of class whoes content is to be checked and copied from css_sheet
        :param class_name:
        :param css_sheet: parseString from cssutils
        :return: None or content.
        """
        contents = ""
        for rule in css_sheet:
            selectors = self.get_selectors(rule, class_name)
            if selectors:
                contents += (str(rule.cssText)) + "\n\n"
        return contents

    def get_class_content(self, css_file_path):
        """
        Get all class property from CSS file for given classes.
        :param classes_name: list of classes
        :param css_file_path: css file path
        :return: dict ( class_name: class_property )
        """
        content = open(css_file_path).read()
        sheet = cssutils.parseString(content)
        for class_name in self.classes_to_scrap:
            if class_name in content:
                class_info = self.check_for_class(class_name, sheet)
                self.css_content += class_info

    def scrap_css_content(self):
        for file in self.css_file_list:
            self.get_class_content(file)
        return True