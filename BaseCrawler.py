import csv
import logging

logger = logging.getLogger('__main__')


class BaseCrawler:
    Course_Page_Url = None
    University = None
    Abbreviation = None
    University_Homepage = None

    output_file = csv.writer(open('./result.csv', 'w'))
    course_count = 0


    def write_headers (self):
        self.output_file.writerow(['university', 'abbreviation', 'department_name', 'course_title', 'unit_count', 'professor',
                                   'objective', 'prerequisite', 'required_skills', 'outcome', 'references', 'scores',
                                  'description', 'projects', 'university_homepage', 'course_homepage', 'professor_homepage'])

    def get_courses_of_department(self, department):
        ...

    def get_course_data(self, course):
        ...

    def save_course_data(self, university, abbreviation, department_name, course_title, unit_count, professor,
                         objective, prerequisite, required_skills, outcome, references, scores, description, projects,
                         university_homepage, course_homepage, professor_homepage):
        try:

            self.output_file.writerow([university, abbreviation, department_name, course_title, unit_count, professor,
                                       objective, prerequisite, required_skills, outcome, references, scores,
                                       description, projects, university_homepage, course_homepage, professor_homepage])

            self.course_count += 1
        except Exception as e:
            logger.error(
                f"{abbreviation} - {department_name} - {course_title}: An error occurred while saving course data: {e}"
            )

    def handler(self):
        ...