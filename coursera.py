import requests
import openpyxl
import lxml
import re
from bs4 import BeautifulSoup
import logging
import random


logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)


def get_courses_list():
    courses_list = requests.get('https://www.coursera.org/sitemap~www~courses.xml')
    return courses_list


def get_courses_list_tree(courses_list):
    xml_tree_in_courses_list = lxml.etree.XML(courses_list.content)
    return xml_tree_in_courses_list


def get_list_of_courses_urls(xml_tree_in_courses_list, quantity=20):
    return [random.choice(xml_tree_in_courses_list)[0].text for _ in range(quantity)]


def get_course_page(course_url):
    request_params = {'fields': 'courseDerivatives.v1(averageFiveStarRating)',
                      'includes': 'courseDerivatives'}
    course_page = requests.get(course_url, params=request_params).content
    return course_page


def get_parsed_course_page(course_page):
    parsed_course_page = BeautifulSoup(course_page, "lxml")
    return parsed_course_page


def find_course_title(parsed_course_page):
    return parsed_course_page.find('div', {'class': 'title'}).text


def find_course_language(parsed_course_page):
    return parsed_course_page.find('div', {'class': 'language-info'}).text


def find_ld_json_script(parsed_course_page):
    return parsed_course_page.find('script', {'type': 'application/ld+json'})


def find_course_start_date(ld_json_script):
    if ld_json_script:
        start_date = re.findall(r'\"startDate\":\"(.*?)\",', ld_json_script.string)
        if start_date:
            return start_date[0]


def find_course_planned_start_date(parsed_course_page):
    return re.findall(r'\"plannedLaunchDate\":\"(.*?)\"', parsed_course_page.text)[0]


def count_course_duration(parsed_course_page):
    return len(parsed_course_page.find_all('div', {'class': 'week'}))


def find_script_with_course_info(parsed_course_page):
    script_with_course_info = parsed_course_page.find_all('script')[-1]
    return script_with_course_info


def get_course_rating(parsed_course_page):
    course_rating = re.findall(r'\"averageFiveStarRating\":(.*?),', parsed_course_page.text)
    if len(course_rating) > 0:
        return course_rating[0]
    else:
        return None


def get_course_info(course_slug):
    course_info = []
    course_page = get_course_page(course_slug)
    parsed_course_page = get_parsed_course_page(course_page)
    ld_json_script = find_ld_json_script(parsed_course_page)
    course_info.append(find_course_title(parsed_course_page))
    course_info.append(find_course_language(parsed_course_page))
    if ld_json_script:
        course_info.append(find_course_start_date(ld_json_script))
    else:
        course_info.append(find_course_planned_start_date(parsed_course_page))
    course_info.append(count_course_duration(parsed_course_page))
    course_info.append(get_course_rating(parsed_course_page))
    return tuple(course_info)


def output_courses_info_to_xlsx(course_list, filepath):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.append(['Title', 'Language', 'Start date', 'Duration (weeks)', 'Average rating'])
    for course in course_list:
        worksheet.append(course)
    workbook.save(filepath)


if __name__ == '__main__':
    courses_list = get_courses_list()
    courses_list_tree = get_courses_list_tree(courses_list)
    courses_urls = get_list_of_courses_urls(courses_list_tree)
    courses_info_list = []
    for course_url in courses_urls:
        courses_info_list.append(get_course_info(course_url))
    filepath = input('Enter filepath to save courses info: ')
    output_courses_info_to_xlsx(courses_info_list, filepath)



