import requests


def parse_sentence(sentence):
    url = "http://corenlp.run/"
    params = {
        "properties": '{"annotators": "tokenize,ssplit,pos,parse"}',
        "pipelineLanguage": "en",
    }

    try:
        response = requests.post(url, params=params, data=sentence.encode("utf-8"))
        response.raise_for_status()  # Raise HTTPError for bad responses

        data = response.json()

        # Adjust this line based on the actual structure of 'data'
        parse_tree = data["sentences"][0]["parse"]
        return parse_tree

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Request error occurred: {err}")


def tree_to_sentence(tree):
    return " ".join(tree.leaves())
