import requests
from .mysql import get_all_pages_from_database
def get_compare_page_prompt(pic1, pic2):
    prompt =  "You are an assistant to determine whether two screenshots are the same software page. \n"
    prompt += "Please help determine if it is the same page. Please note that sometimes the same page can be slightly different."
    prompt += f"Please help to determine whether {pic1} and {pic2} are screenshots of the same page."
    prompt += f"{pic1} is an image stored locally to the project."
    prompt += "\n\n"

    prompt += "### Output format ###\n"
    prompt += "Your output consists of the following two parts:\n"
    prompt += "### Judgment basis ### \n Please give some descriptions of the two pages."
    prompt += "### Conclusion ### \n Your output format is: True or False\n"
    return prompt


def get_same_page_id_prompt(pic, all_page_from_db):
    prompt = "You are an assistant to decide which image is most similar to the one in the database. \n"
    prompt += f"{pic} is a screenshot from the phone, {all_page_from_db} are all pages about the app.\n"
    prompt += "The table headers are id, page_name, page_key, full_address, app_type, os_type, belongs_to, base_line, desc, ext."
    prompt += "Please help to determine whether the s3 linked page in the table contains the screenshot of similar pages. If yes, return the page id."

    prompt += "### Output format ###\n"
    prompt += "### Conclusion ###\n True or False\n"
    prompt += "If the conclusion is True, you also need to return the same page id in the database. Below the ### id ###"
    prompt += "For example, if you find the same image in the table with id 5, you should return the following format : \n"
    prompt += "### Conclusion ###\n"
    prompt += "True\n"
    prompt += "### id ###\n"
    prompt += "5\n"
    return prompt


def get_element_judge_prompt(current_page_id, element, window_dump, all_pages):
    prompt = "You are an assistant to determine whether the element on the page is clickable, and if so, which page in the database is the page after the click. \n"
    prompt += "The table headers are id, page_name, page_key, full_address, app_type, os_type, belongs_to, base_line, desc, ext."
    prompt += f"The id of the current page is {current_page_id}.\n"
    prompt += f"Element {element} is a file on the current page. Determine whether {element} is a clickable element based on the xml file {window_dump}. \n"
    prompt += f"Find {element} in the xml file and use the clickable field to determine if you can click it. \n"
    prompt += f"If the element can click, return the page id of which page in the table {all_pages} is the page after the click."

    prompt += "### Output format ###\n"
    prompt += "### Clickable ### \n True or False\n"
    prompt += "If the element is click, you also need to return the next page id in the database. Below the ### id ### "
    return prompt



def judge_same_page(comp_page, dest_page, model, API_url, token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {
        "model": model,
        "messages": [],
        "max_tokens": 2048,
        'temperature': 0.0,
        "seed": 1234
    }

    content = get_compare_page_prompt(comp_page, dest_page)
    data["messages"].append({"role": "system", "content": content})

    while True:
        try:
            res = requests.post(API_url, headers=headers, json=data)
            res_json = res.json()
            res_content = res_json['choices'][0]['message']['content']
        except:
            print("Network Error:")
            try:
                print(res.json())
            except:
                print("Request Failed")
        else:
            break

    return res_content

def find_same_pages_id(comp_page, dest_pages_from_db, model, API_url, token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {
        "model": model,
        "messages": [],
        "max_tokens": 2048,
        'temperature': 0.0,
        "seed": 1234
    }

    content = get_same_page_id_prompt(comp_page, dest_pages_from_db)
    data["messages"].append({"role": "system", "content": content})

    while True:
        try:
            res = requests.post(API_url, headers=headers, json=data)
            res_json = res.json()
            res_content = res_json['choices'][0]['message']['content']
        except:
            print("Network Error:")
            try:
                print(res.json())
            except:
                print("Request Failed")
        else:
            break

    return res_content


def judge_element(current_page, element, window_dump, app_type, model, API_url, token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {
        "model": model,
        "messages": [],
        "max_tokens": 2048,
        'temperature': 0.0,
        "seed": 1234
    }

    all_pages = get_all_pages_from_database(app_type)
    content = get_element_judge_prompt(current_page, element, window_dump, all_pages)

    data["messages"].append({"role": "system", "content": content})

    while True:
        try:
            res = requests.post(API_url, headers=headers, json=data)
            res_json = res.json()
            res_content = res_json['choices'][0]['message']['content']
        except:
            print("Network Error:")
            try:
                print(res.json())
            except:
                print("Request Failed")
        else:
            break
    return res_content


def find_a_baseline_page(appType, pic, model, API_url, token):
    # appType = 1 众包，appType = 3  专送
    ret = ""
    if appType == 1:
        all_crowdsourcing_pages = get_all_pages_from_database(1)
        ret = find_same_pages_id(pic, all_crowdsourcing_pages, model, API_url, token)
        # print(all_crowdsourcing_pages)
    elif appType == 3:
        all_jiameng_pages = get_all_pages_from_database(3)
        ret = find_same_pages_id(pic, all_jiameng_pages, model, API_url, token)
        # print("\n\n\n\n\n:", ret)
    else:
        print("Please input correct appType. 1 represent crowdsourcing. 3 represent jiameng.")
    return ret





