import http.client
import json

def find_new_data(articles, last_headline_id, file_path):
    results = []

    # Find new data based on data-headlineid in reverse order
    for article in reversed(articles):  # Iterate in reverse order
        headline_id = article['data-headlineid']
        if headline_id != '0' and (last_headline_id is None or int(headline_id) > int(last_headline_id)):
            parent_title = article.find('p', class_='headline-title')
            if parent_title is not None:
                anchor_element = parent_title.find('a') or parent_title.find('span')
                if anchor_element is not None:
                    text_inside_a_tag = anchor_element.text.strip()
                    results.append({'idData': headline_id, 'title': text_inside_a_tag})
                    # SEND TO SERVER
                    data = {
                        "title": text_inside_a_tag
                    }
                    json_data = json.dumps(data)
                    conn = http.client.HTTPConnection("localhost", 3000)
                    headers = {
                        'Content-Type': 'application/json'
                    }
                    conn.request("POST", "/", json_data, headers)

    # Update the last_headline_id
    if articles:
        last_headline_id = articles[-1]['data-headlineid']

    if results:
        with open(file_path, "w") as file:
            file.write(results[0]['idData'])

    return results
