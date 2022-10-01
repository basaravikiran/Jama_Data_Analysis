import requests
import json
import pandas as pd

base_url = "https://xyz.jamacloud.com"
api_version='/rest/latest/'
client_id = 'abcd'
client_secret = 'efgh'
data = {'grant_type': 'client_credentials'}
rest_url = base_url + api_version
oauth_url = base_url + '/rest/oauth/token'

class JamaRestData(object):
    def __init__(self):
        response = requests.post(oauth_url, data=data, auth=(client_id, client_secret))
        token_raw = json.loads(response.text)
        token = token_raw["access_token"]
        self.headers = {"Authorization": "Bearer {}".format(token)}

    def pagination_results(self,resource,*query_params):
        if query_params:
            query_string = ''
            for query in query_params:
                query_string = query_string + '&' + query

        allowed_results = 20
        max_results = "maxResults=" + str(allowed_results)
        result_count = -1
        start_index = 0
        results = []
        while result_count != 0:
            startAt = "startAt=" + str(start_index)
            url = rest_url + resource + "?" + startAt + "&" + max_results + query_string
            response = requests.get(url=url, headers=self.headers)
            json_response = json.loads(response.text)
            page_info = json_response["meta"]["pageInfo"]
            start_index = page_info["startIndex"] + allowed_results
            result_count = page_info["resultCount"]
            results = results + json_response["data"]
        return results

    def get_tags_from_item(self,item_id):
        resource = 'items/'+str(item_id)+'/tags'
        url =  rest_url + resource
        response = requests.get(url=url, headers=self.headers)
        return response.text

    def get_defects_from_item(self,item_id):
        resource = 'items/'+str(item_id)+'/children'
        results = self.pagination_results(resource)
        fields = []
        for result in results:
            fields.append(result['fields'])
        return fields







if __name__ == '__main__':
    jama_rest_connect = JamaRestData()
    print(jama_rest_connect.get_tags_from_item(17856940))
#    defects_json=jama_rest_connect.get_defects_from_item(14167882)
#    print(json.dumps(defects_json))
#    print(jama_rest_connect.pagination_results('filters', 'project=336'))





