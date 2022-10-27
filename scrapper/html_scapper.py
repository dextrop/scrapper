import os, time
from bs4 import BeautifulSoup
from scrapper.css_scrapper import CSSScrapper

class HTMLScrapper():
    def __init__(self, filepath=None, tag=None, tag_id=None):
        self.filepath = filepath
        self.tag = tag
        self.tag_id = tag_id

    def create_style_css(self):
        """
        Use CSS Scrapper to scrap required classes.
        :return:
        """
        scrapper = CSSScrapper(
            css_file_list=self.local_css_files,
            classes_to_scrap=self.classes_to_scrap
        )

        content = scrapper.scrap_css_content()
        open(self.output_dir + "/style.css", "w").write(scrapper.css_content)
        return True

    @property
    def scrap(self):
        """
        Scrap HTML content, creates scrapped output folder with
        assets containing images and index file with HTML code.
        :return:
        """
        if self.filepath == None:
            self.filepath = self.get_html_file

        self.input_path = self.filepath.replace(self.filepath.split("/")[-1], "")
        if self.input_path[-1] == "/":
            self.input_path = self.input_path[:-1]

        if self.tag == None or self.tag_id == None:
            self.tag, self.tag_id = self.get_tag_and_id

        self.output_dir, self.assets_dir = self.get_output_paths
        self.bs4_content = self.get_html_content
        self.classes_to_scrap = self.get_list_of_classes
        self.local_css_files, self.remote_css_files = self.get_stylesheet_files
        self.bs4_content = self.copy_images
        self.create_style_css()

        return self.wrap_index_file

    @property
    def get_output_paths(self):
        """
        Set Output Path, Assets path
        Check if directory exits, else create one.
        :return:
        """
        output_dir = os.getcwd() + "/scrapped-" + str(time.time()).split(".")[0]
        assets_dir = output_dir + "/assets"

        if not os.path.exists(output_dir):
            os.system("mkdir " + output_dir)

        if not os.path.exists(assets_dir):
            os.system("mkdir " + assets_dir)

        return output_dir, assets_dir

    @property
    def get_html_file(self):
        """
        Ask for html file path that needs
        to be scrapped
        :return:
        """
        return input("Input html filepath\n>> ")

    @property
    def get_tag_and_id(self):
        """
        Get HTML tag ID and DOM ID for
        section that needs to be scrapped.
        :return:
        """
        tag = input("Input tag name which need to be scrapped ( eg : div, section etc ) >> ")
        id = input("Input tag ID >> ")
        return tag, id

    @property
    def get_html_content(self):
        """
        Get HTML content that need to be scrapped
        :return: BS4 object
        """
        self.content = open(self.filepath).read()
        soup = BeautifulSoup(self.content, features="html.parser")
        bs4_content_obj = soup.findAll(self.tag, {"id": self.tag_id})
        if len(bs4_content_obj) < 1:
            raise ValueError("No content found for {} with id {}".format(self.tag, self.tag_id))
        return bs4_content_obj[0]

    @property
    def copy_images(self):
        """
        Get list of images link inside from
        content that is required to be scrapped.
        :return: Updated Content
        """
        imagesObj = self.bs4_content.findAll("img")
        images = []
        for imageObj in imagesObj:
            if "https://" not in imageObj:
                images.append(self.input_path + "/" + imageObj["src"])

        content = self.bs4_content.prettify()
        for image in images:
            image_path = self.assets_dir + "/" + image.split("/")[-1]
            image_path_html = "assets/" + image.split("/")[-1]
            os.system("cp {} {}".format(
                image, image_path
            ))
            content = content.replace(image.replace(self.input_path + "/", ""), image_path_html)

        bs4_content = BeautifulSoup(content, features="html.parser")
        return bs4_content

    @property
    def get_stylesheet_files(self):
        """
        get list of css_files from HTML code
        both local files and remote file
        :return: css_files, https_files
        """
        local_css_files = []
        remote_css_files = []
        for line in self.content.split("\n"):
            if "<link" in line and "href=" in line:
                link = (line.split('href="')[1].split('"')[0])
                if "https://" not in link:
                    local_css_files.append(self.input_path + "/" + link)
                else:
                    remote_css_files.append(link)

        return local_css_files, remote_css_files

    @property
    def get_list_of_classes(self):
        """
        Get list of all classes from HTML content.
        :return: class_list
        """
        classes = [value
                   for element in self.bs4_content.find_all(class_=True)
                   for value in element["class"]
                   ]
        unique_class = []
        for class_name in classes:
            if class_name not in unique_class:
                unique_class.append(class_name)
        return unique_class

    @property
    def wrap_index_file(self):
        """
        Write Basic HTML file structure.
        :return:
        """
        index_file_code = '''<html>
    <head>
        <title>Scrapped Project</title>
REMOTE_LINKS
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        HTML_CODE
    </body>
</html>'''
        remote_links = ""
        content = self.bs4_content.prettify()
        for link in self.remote_css_files:
            remote_links += '        <link rel="stylesheet" href="{}">\n'.format(link)


        index_file_code = index_file_code.replace("REMOTE_LINKS", remote_links)
        index_file_code = index_file_code.replace("HTML_CODE", content)
        open(self.output_dir + "/index.html", "w").write(index_file_code)
        return True