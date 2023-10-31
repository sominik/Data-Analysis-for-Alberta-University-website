from BaseCrawler import BaseCrawler
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger('__main__')


class UAlberta(BaseCrawler):
    Course_Page_Url = 'https://calendar.ualberta.ca/content.php?catoid=36&navoid=11383'
    University = "Alberta University"
    Abbreviation = "UAlberta"
    University_Homepage = "https://www.ualberta.ca/index.html"
    Courses_default_page = 'https://calendar.ualberta.ca/'

    # Below fields didn't find in the website
    Professor = None
    Objective = None
    Required_Skills = None
    Outcome = None
    References = None
    Scores = None
    Projects = None
    Professor_Homepage = None

    def get_course_data(self, course):
        units = None
        faculty = None
        department = None
        description = None
        prerequisite = None
        html_content = requests.get(course).text
        soup = BeautifulSoup(html_content, 'html.parser')
        strong_tags = soup.find_all('strong')
        for tag in strong_tags:
            if tag.text == 'Units':
                units = tag.next_sibling
            elif tag.text == 'Faculty':
                faculty = tag.next_sibling
            elif tag.text == 'Department':
                department = tag.next_sibling
            elif tag.text == 'Description':
                description_txt = tag.next_sibling.next_sibling.text
                split_word = None
                if "Prerequisite:" in description_txt:
                    split_word = "Prerequisite:"
                elif "Prerequisites:" in description_txt:
                    split_word = "Prerequisites:"
                elif "Pre or corequisites:" in description_txt:
                    split_word = "Pre or corequisites:"
                elif "Corequisites:" in description_txt:
                    split_word = "Corequisites:"
                if split_word is None:
                    description = description_txt
                else:
                    splited_description = description_txt.split(split_word)
                    description = splited_description[0]
                    prerequisite = splited_description[1]
        print('course data: ', units, faculty, department, description)
        return units, faculty, department, description, prerequisite

    def handler(self):
        self.write_headers()
        for i in range(1, 81):
            html_content = requests.get(self.Course_Page_Url).text
            soup = BeautifulSoup(html_content, 'html.parser')
            courses = soup.find_all("table", {"class": 'table_default'})[-1].select('tr')[2:]
            del courses[len(courses)-1]
            for course in courses:
                course_title = course.text.strip()[2:]
                print(course_title)
                course_link = course.find_all('a')
                if course_link:
                    link = self.Courses_default_page + course_link[0]['href']
                    print(link)
                    units, faculty, department, description, prerequisite = self.get_course_data(link)
                    if units is not None:
                        self.save_course_data(
                            self.University, self.Abbreviation, department, course_title, units, self.Professor,
                            self.Objective, prerequisite, self.Required_Skills, self.Outcome, self.References,
                            self.Scores, description, self.Projects, self.University_Homepage, link,
                            self.Professor_Homepage)
                logger.info(f"{self.Abbreviation}: {department} department's data was crawled successfully.")
            logger.info(f"{self.Abbreviation}: Total {self.course_count} courses were crawled successfully.")
            if i != 80:
                next_page = soup.find("a", {"aria-label": "Page " + str(i + 1)})
                next_page_url = "https://calendar.ualberta.ca" + next_page.get('href')
                self.Course_Page_Url = next_page_url
