import requests
import json
from typing import Dict, Any, Optional

class RateMyProfessorsAPI:
    def __init__(self):
        self.session = self._create_session()

    def _create_session(self):
        session = requests.Session()
        session.headers.update({
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": "Basic dGVzdDp0ZXN0",
            "content-type": "application/json",
            "sec-ch-ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-rmp-comp-id": "undefined",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
        })
        return session

    def search_school(self, school_name: str) -> Optional[Dict]:
        url = "https://www.ratemyprofessors.com/graphql"
        self.session.headers["Referer"] = "https://www.ratemyprofessors.com/search/professors/"
        
        query = """
        query NewSearchSchoolsQuery(
          $query: SchoolSearchQuery!
        ) {
          newSearch {
            schools(query: $query) {
              edges {
                node {
                  id
                  name
                  city
                  state
                  numRatings
                  avgRatingRounded
                }
              }
            }
          }
        }
        """

        variables = {
            "query": {
                "text": school_name
            }
        }

        payload = {
            "query": query,
            "variables": variables
        }

        response = self.session.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            schools = data['data']['newSearch']['schools']['edges']
            if schools:
                school = schools[0]['node']
                return {
                    'id': school['id'],
                    'name': school['name'],
                    'city': school['city'],
                    'state': school['state'],
                    'num_ratings': school['numRatings'],
                    'avg_rating': school['avgRatingRounded']
                }
        return None

    def search_teachers(self, school_id: str, professor_name: str = "", limit: int = 8, cursor: str = "") -> Dict[str, Any]:
        url = "https://www.ratemyprofessors.com/graphql"
        self.session.headers["Referer"] = f"https://www.ratemyprofessors.com/search/professors/{school_id}?q="
        
        query = """
        query TeacherSearchPaginationQuery(
          $count: Int!
          $cursor: String
          $query: TeacherSearchQuery!
        ) {
          search: newSearch {
            teachers(query: $query, first: $count, after: $cursor) {
              edges {
                node {
                  id
                  firstName
                  lastName
                  department
                  avgRating
                  numRatings
                  wouldTakeAgainPercent
                  avgDifficulty
                  school {
                    name
                    id
                  }
                }
              }
              pageInfo {
                hasNextPage
                endCursor
              }
            }
          }
        }
        """

        variables = {
            "count": limit,
            "cursor": cursor,
            "query": {
                "text": professor_name,
                "schoolID": school_id,
                "fallback": True
            }
        }

        payload = {
            "query": query,
            "variables": variables
        }

        response = self.session.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            teachers = data['data']['search']['teachers']['edges']
            page_info = data['data']['search']['teachers']['pageInfo']
            
            return {
                'teachers': [
                    {
                        'id': teacher['node']['id'],
                        'name': f"{teacher['node']['firstName']} {teacher['node']['lastName']}",
                        'department': teacher['node']['department'],
                        'avg_rating': teacher['node']['avgRating'],
                        'num_ratings': teacher['node']['numRatings'],
                        'would_take_again': teacher['node']['wouldTakeAgainPercent'],
                        'avg_difficulty': teacher['node']['avgDifficulty'],
                        'school': teacher['node']['school']['name']
                    }
                    for teacher in teachers
                ],
                'has_next_page': page_info['hasNextPage'],
                'end_cursor': page_info['endCursor']
            }
        return {'teachers': [], 'has_next_page': False, 'end_cursor': None}
