import requests
import time

class GradientAPI:
    def __init__(self, request_delay: int = 5):
        self.session = self._create_session()
        self.request_delay = request_delay
    
    def _parse_headers(self):
        with open('gradient-headers.txt', 'r') as file:
            header_text = file.read()

        # Split the header text into lines
        lines = header_text.strip().split('\n')

        # Initialize dictionaries for headers and cookies
        headers = {}
        cookies = {}

        # Parse each line
        for line in lines[1:]:  # Skip the first line (GET /api/subjects HTTP/1.1)
            if ': ' in line:
                key, value = line.split(': ', 1)
                if key.lower() == 'cookie':
                    # Parse cookies
                    cookie_pairs = value.split('; ')
                    for pair in cookie_pairs:
                        cookie_key, cookie_value = pair.split('=', 1)
                        cookies[cookie_key] = cookie_value
                else:
                    # Add to headers
                    headers[key] = value

        return headers, cookies

    def _create_session(self):
        session = requests.Session()
        headers, cookies = self._parse_headers()
        session.headers.update(headers)
        session.cookies.update(cookies)
        return session

    def _make_api_request(self, endpoint, body=None):
        url = f'https://gradient.ncsu.edu/api/{endpoint}'
        response = self.session.get(url, json=body)
        if response.status_code != 200:
            raise Exception("Request error (tokens in <gradient-headers.txt> may have expired):\n", response.status_code, response.reason, "\n", response.text)
        return response.json()
    
    def _get_courses(self, subject):
        results = self._make_api_request(f'courses?subject={subject}')
        return list(filter(lambda course: course["value"] < "500", results))
    
    def get_subject_distrubutions(self, subject, last_course: str = None):
        for course in self._get_courses(subject):
            if last_course and course["value"] <= last_course:
                continue
            yield self._make_api_request(f'course-distributions?subject={subject}&course={course["value"]}')
            time.sleep(self.request_delay)
