import pandas as pd
from ast import literal_eval
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
import random
import cmd
import re
import datetime
import requests


def run_model():
    # load data
    df = pd.read_csv(***YOUR_PATH_HERE***)
    # translate response var into true list
    df['bot_responses'] = df['bot_responses'].apply(lambda x: literal_eval(x))
    # Use 100% of the data
    X_train = df['user_phrases']
    y_train = df['tags'].values
    # vectorize data
    vectorizer = CountVectorizer(min_df=1)
    X_train_counts = vectorizer.fit_transform(X_train).toarray()
    model = SVC(kernel='rbf', C=1000, gamma=0.001, random_state=33)
    model.fit(X_train_counts, y_train)
    return model, df, vectorizer

def init_encoding_data():
    # read file for encoding data
    filepath = ***YOUR_PATH_HERE***
    with open(filepath) as f:
        data = f.read()
    # read in text as a dict structure
    ecoding_dict = literal_eval(data)
    # generate lists from encoding
    neighborhood_list = [p['desc'].lower() for p in ecoding_dict['body']['geographicareas']]
    parks_list = [p['desc'].lower() for p in ecoding_dict['body']['centers']]
    activities_list = [p['desc'].lower() for p in ecoding_dict['body']['othercategories']]
    # separate out the keyword from the activity item i.e. sports - soccer == soccer
    activities_list = [a.replace(' ', '').split('-')[1] for a in activities_list]
    return parks_list, neighborhood_list, activities_list, data

def init_web_data_structures():
    cookies = {
        'chicagoparkdistrict_LOGGED_JSESSIONID': '',
        'chicagoparkdistrict_locale': 'en-US',
        'chicagoparkdistrict_FullPageView': 'true',
        'chicagoparkdistrict_JSESSIONID': 'node0ljrgnlb7u8v2i2zd0s791sfe193778.node0',
        's_fid': '6A7C662ECCD7EDD0-3B914F505EC7FBC9',
        's_cc': 'true',
        '_ga': 'GA1.2.865154137.1677515525',
        '_gid': 'GA1.2.291037019.1677515525',
        's_vi': '[CS]v1|31FE6D82E91ED67C-40001F6DA1EBD7E1[CE]',
        'JSESSIONID': 'node01j0dmet4zv0x3cxgak7flhumr307136.node0',
        'utag_main': 'v_id:018693b7844c0065d5d07feefdb805075009806d00942$_sn:4$_se:1$_ss:1$_st:1677599121755$vapi_domain:activecommunities.com$ses_id:1677597321755%3Bexp-session$_pn:1%3Bexp-session',
        'BIGipServer~activenet~anc_prod_chicagoparkdistrict': '!XlPwTaq0I8h5kTOnJbE2j7L6XIQ605bmSpJ/lR0ZmQxpdFxSBrjFh1HRpO+eLuy/pszwgd+jFjWsT+I=',
        'BIGipServer~activenet~activenet_newcui_rush_pool_ats': '!CorM8i1WR5zMuranJbE2j7L6XIQ60/gYGMXeuoHFEvzPrADty3vBwJA7xR5RksT2syng91WM6/bx9w==',
        's_sq': '%5B%5BB%5D%5D',
    }
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=utf-8',
        # 'Cookie': 'chicagoparkdistrict_LOGGED_JSESSIONID=; chicagoparkdistrict_locale=en-US; chicagoparkdistrict_FullPageView=true; chicagoparkdistrict_JSESSIONID=node0ljrgnlb7u8v2i2zd0s791sfe193778.node0; s_fid=6A7C662ECCD7EDD0-3B914F505EC7FBC9; s_cc=true; _ga=GA1.2.865154137.1677515525; _gid=GA1.2.291037019.1677515525; s_vi=[CS]v1|31FE6D82E91ED67C-40001F6DA1EBD7E1[CE]; JSESSIONID=node01j0dmet4zv0x3cxgak7flhumr307136.node0; utag_main=v_id:018693b7844c0065d5d07feefdb805075009806d00942$_sn:4$_se:1$_ss:1$_st:1677599121755$vapi_domain:activecommunities.com$ses_id:1677597321755%3Bexp-session$_pn:1%3Bexp-session; BIGipServer~activenet~anc_prod_chicagoparkdistrict=!XlPwTaq0I8h5kTOnJbE2j7L6XIQ605bmSpJ/lR0ZmQxpdFxSBrjFh1HRpO+eLuy/pszwgd+jFjWsT+I=; BIGipServer~activenet~activenet_newcui_rush_pool_ats=!CorM8i1WR5zMuranJbE2j7L6XIQ60/gYGMXeuoHFEvzPrADty3vBwJA7xR5RksT2syng91WM6/bx9w==; s_sq=%5B%5BB%5D%5D',
        'Origin': 'https://anc.apm.activecommunities.com',
        'Referer': 'https://anc.apm.activecommunities.com/chicagoparkdistrict/activity/search?onlineSiteId=0&locale=en-US&activity_select_param=2&open_spots=1&viewMode=list',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'X-CSRF-Token': 'ec601414-dd82-402c-9c55-c617c0045255',
        'X-Requested-With': 'XMLHttpRequest',
        'page_info': '{"order_by":"","page_number":1,"total_records_per_page":20}',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }
    params = {
        'locale': 'en-US',
    }
    json_data = {
        'activity_search_pattern': {
            'skills': [],
            'time_after_str': '',
            'days_of_week': None,
            'activity_select_param': 2,
            'center_ids': [],
            'time_before_str': '',
            'open_spots': 1,
            'activity_id': None,
            'activity_category_ids': [],
            'date_before': '',
            'min_age': None,
            'date_after': '',
            'activity_type_ids': [],
            'site_ids': [],
            'for_map': False,
            'geographic_area_ids': [],
            'season_ids': [],
            'activity_department_ids': [],
            'activity_other_category_ids': [],
            'child_season_ids': [],
            'activity_keyword': '',
            'instructor_ids': [],
            'max_age': None,
            'custom_price_from': '',
            'custom_price_to': '',
        },
        'activity_transfer_pattern': {},
    }
    return cookies, headers, params, json_data

def bake_cookies(cookies):
    url = 'https://anc.apm.activecommunities.com/chicagoparkdistrict/activity/search?onlineSiteId=0&locale=en-US&activity_select_param=2&open_spots=1&viewMode=list'
    cookies_list = list(requests.get(url).cookies)
    # handle issues with cookies
    if len(cookies_list) != 6:
        print('WARNING: Cookies not properly collected, please enter quit and resolve the issue with bake_cookies function.')
    else:
        # chicagoparkdistrict_JSESSIONID
        cpd_JSESSIONID = str(cookies_list[0]).split('=')[1].split(' ')[0]
        # BIGipServer~activenet~activenet_newcui_rush_pool_ats
        B1 = str(cookies_list[3]).split('=')[1].split(' ')[0]
        # BIGipServer~activenet~anc_prod_chicagoparkdistrict
        B2 = str(cookies_list[4]).split('=')[1].split(' ')[0]
        # JSESSIONID
        JSESSIONID = str(cookies_list[5]).split('=')[1].split(' ')[0]
        # rename cookies var for better tracking and troubleshooting
        baked_cookies = cookies
        # set cookie variables to fresh cookies
        baked_cookies['chicagoparkdistrict_JSESSIONID'] = cpd_JSESSIONID
        baked_cookies['BIGipServer~activenet~activenet_newcui_rush_pool_ats'] = B1
        baked_cookies['BIGipServer~activenet~anc_prod_chicagoparkdistrict'] = B2
        baked_cookies['JSESSIONID'] = JSESSIONID
        return baked_cookies


def find_my_park(p_list):
    # query user for their closest park to their house
    print('Please enter the name of the park closest to your house below')
    mypark = input("My Park: ")
    mp_counter = 0
    while True:
        if mypark.lower() in p_list:
            break
        else:
            mp_counter += 1
            print('Whoops! Looks like you may have misspelled your park, or your park is not in the database.')
            mypark = input("My Park: ")
            if mypark.lower() in p_list:
                break
        if mp_counter > 1:
            print('Not sure about your park? Try visiting this link to search for your park:')
            print('https://www.chicagoparkdistrict.com/parks-facilities/find-park-facility?_ga=2.216488533.291037019.1677515525-865154137.1677515525')
            print('')
            mypark = input("My Park: ")
    return mypark

def find_my_neighborhood(n_list):
    # query user for their closest park to their house
    print('Please enter the name of your neighborhood')
    mynhood = input("My Neighborhood: ")
    mn_counter = 0
    while True:
        if mynhood.lower() in n_list:
            break
        else:
            mn_counter += 1
            print('Whoops! Looks like you may have misspelled your Neighborhood, or your Neighborhood is not in the database.')
            mynhood = input("My Neighborhood: ")
            if mynhood.lower() in n_list:
                break
        if mn_counter > 1:
            # display list of neighborhoods
            cli = cmd.Cmd()
            print("List Of Chicago Neighborhoods:")
            print('-' * 80)
            cli.columnize(n_list, displaywidth=80)
            print('-' * 80)
            print('')
            mynhood = input("My Neighborhood: ")

    return mynhood

def grab_dates():
    # regex pattern to check against
    pattern = "\d{4}[/-]\d{2}[/-]\d{2}"
    print('Oh, hey- it looks like you are trying to search for two specific dates, unfortunately I need them in the')
    print('specific format: YYYY-MM-DD.')
    print('')
    # collect the start date from the user in the correct formatting
    while True:
        start_date = input('Please enter your first date (earliest date):')
        if len(re.findall(pattern, start_date)) == 1:
            break
        else:
            print('Looks like something is wrong, double check your date formatting (YYYY-MM-DD)')
    # collect the end date in the correct formatting
    while True:
        end_date = input('Please enter your last date (end date):')
        if len(re.findall(pattern, end_date)) == 1:
            break
        else:
            print('Looks like something is wrong, double check your date formatting (YYYY-MM-DD)')
    return start_date, end_date

def extract_kw(u_response, predicted_tag, mypark, myn, output, encoding, p_list, n_list, a_list, json_data):
    # swap keyword for park
    if predicted_tag == 'My Park':
        # handle my-park logic
        output = output.replace('$my_park', mypark)
    # swap keyword for neighborhood
    if predicted_tag == 'My Neighborhood':
        # handle my-park logic
        output = output.replace('$my_neighborhood', myn)
    # tags with scraping
    scrape_tags = ['My Park Activities General','Parks Activities Near Me','Parks Near Me By Activity','Parks Where',
                   'Parks Where Neighborhood','Parks Activities When Specific Dates','Parks Specific Activities When Month',
                   'Parks Activities When This Week','Parks Activities When Day Of Week','Parks Activities When Month']
    if predicted_tag not in scrape_tags:
        json_data = 'skip'
    else:
        # initialize month object
        m_dict = {'january': ['2023-01-01', '2023-01-31'], 'february': ['2023-02-01', '2023-02-28'],
                  'march': ['2023-03-01', '2023-03-31'], 'april': ['2023-04-01', '2023-04-30'],
                  'may': ['2023-05-01', '2023-05-31'], 'june': ['2023-06-01', '2023-06-30'],
                  'july': ['2023-07-01', '2023-07-31'], 'august': ['2023-08-01', '2023-08-31'],
                  'september': ['2023-09-01', '2023-09-30'], 'october': ['2023-10-01', '2023-10-31'],
                  'november': ['2023-11-01', '2023-11-30'], 'december': ['2023-12-01', '2023-12-31']}
        # initialize days of week object
        w_dict = {'sunday': '1000000', 'monday': '0100000', 'tuesday': '0010000', 'wednesday': '0001000',
                  'thursday': '0000100',
                  'friday': '0000010', 'saturday': '0000001'}
        if predicted_tag == 'My Park Activities General':
            # edit json data to search for activities given my park
            json_data['center_ids'] = encoding['body']['centers']['desc' == mypark]['id']
        # edit json data to include the id for their neighborhood
        elif predicted_tag == 'Parks Activities Near Me':
            json_data['geographic_area_ids'] = encoding['body']['geographicareas']['desc' == myn]['id']
        # edit json data to include the id for their neighborhood and also extract the activity they wish to do
        elif predicted_tag == 'Parks Near Me By Activity':
            json_data['geographic_area_ids'] = encoding['body']['geographicareas']['desc' == myn]['id']
            # initialize user_activity for error handling
            user_activity = 0
            # extract activity word
            for i in a_list:
                if i in u_response.lower():
                    user_activity = i
            # set json data as activity id
            if user_activity != 0:
                json_data['activity_other_category_ids'] = encoding['body']['othercategories']['desc' == user_activity]['id']
        elif predicted_tag == 'Parks Where':
            # initialize user_parks for error handling
            user_parks = 0
            # extract park word
            for i in p_list:
                if i in u_response.lower():
                    user_parks = i
            # set json data as park id
            if user_parks != 0:
                json_data['center_ids'] = encoding['body']['centers']['desc' == user_parks]['id']
        elif predicted_tag == 'Parks Where Neighborhood':
            # initialize user_neighborhood for error handling
            user_neighborhood = 0
            # extract neighborhood word
            for i in n_list:
                if i in u_response.lower():
                    user_neighborhood = i
            # set json data as neighborhood id
            if user_neighborhood != 0:
                json_data['geographic_area_ids'] = encoding['body']['geographicareas']['desc' == user_neighborhood]['id']
        elif predicted_tag == 'Parks Activities When Specific Dates':
            # collect dates from user input, handling errors
            start_date, end_date = grab_dates()
            # enter dates into json data
            json_data['date_after'] = start_date
            json_data['date_before'] = end_date
        elif predicted_tag == 'Parks Specific Activities When Month':
            # use date range from indexed month to output dates
            for i in m_dict:
                if i in u_response.lower():
                    json_data['date_after'] = m_dict[i][0]
                    json_data['date_before'] = m_dict[i][1]
            # initialize user_activity for error handling
            user_activity = 0
            # extract activity word
            for i in a_list:
                if i in u_response.lower():
                    user_activity = i
            # set json data as activity id
            if user_activity != 0:
                json_data['activity_other_category_ids'] = encoding['body']['othercategories']['desc' == user_activity]['id']
        elif predicted_tag == 'Parks Activities When This Week':
            json_data['date_after'] = datetime.date.today()
            json_data['date_before'] = datetime.date.today() + datetime.timedelta(days = 7)
        elif predicted_tag == 'Parks Activities When Day Of Week':
            user_d_week = 0
            # find the day of the week within the user output and link to day of week code json data
            for i in w_dict:
                if i in u_response.lower():
                    user_d_week = w_dict[i]
            if user_d_week != 0:
                json_data['days_of_week'] = user_d_week
            user_activity = 0
            # extract activity word
            for i in a_list:
                if i in output.lower():
                    user_activity = i
            # set json data as activity id
            if user_activity != 0:
                json_data['activity_other_category_ids'] = encoding['body']['othercategories']['desc' == user_activity]['id']
        elif predicted_tag == 'Parks Activities When Month':
            # use date range from indexed month to output dates
            for i in m_dict:
                if i in u_response.lower():
                    json_data['date_after'] = m_dict[i][0]
                    json_data['date_before'] = m_dict[i][1]
    new_json_data = json_data
    return new_json_data, output


def enter_scrape(json_data, raw_cookies, headers, params):
    # initialize page_turner to allow for proper looping
    turn_page = 'y'
    # initialize page counter
    page_count = 1
    while True:
        if turn_page.lower() == 'y' or turn_page.lower() == 'yes':
            pass
        else:
            break
        baked_cookies = bake_cookies(raw_cookies)
        while True:
            # collect page dict from json formatting
            p = literal_eval(headers['page_info'])
            # enter the current page count
            p['page_number'] = page_count
            # re-format page info for json encoding
            headers['page_info'] = str(p).replace("'", '"').replace(' ', '')
            # post using formatted json to query site using generated cookies
            response = requests.post(
                'https://anc.apm.activecommunities.com/chicagoparkdistrict/rest/activities/list',
                params=params,
                cookies=baked_cookies,
                headers=headers,
                json=json_data,
            )
            # if the cookies have expired, rerun cookies by breaking out of current loop and back to prev loop
            if response.json()['headers']['response_code'] == '0011':
                break
            # Print out list of activities
            for i in range(0, len(response.json()['body']['activity_items'])):
                item = response.json()['body']['activity_items'][i]
                print('{}. {} | {} | {} | {} | {}'.format(
                    i, item['name'], item['location']['label'], item['fee']['label'], item['time_range'], item['days_of_week']))
            # print out page divider
            print(f'Page {page_count} ----------------------------------')
            # query user for next page of activities
            print('Would you like to see the next page of results? (y/n)')
            turn_page = input('You: ')
            if turn_page.lower() == 'y' or turn_page.lower() == 'yes':
                page_count += 1
            else:
                break


def enter_chat():
    # initialize model
    model, df, vectorizer = run_model()
    # initialize parks data
    parks_list, neighborhoods_list, activities_list, encoding_data = init_encoding_data()
    # initialize json structure for web scraping
    cookies, headers, params, json_data = init_web_data_structures()
    # query user to log the closest park to their house for embedding $mypark
    mypark = find_my_park(parks_list)
    # query user to log their neighborhood for embedding $near me
    myn = find_my_neighborhood(neighborhoods_list)
    while True:
        # begin chat
        user_response = input('You:')
        if user_response == 'exit':
            break
        # predict user intent
        X_user_counts = vectorizer.transform([user_response]).toarray()
        pred = model.predict(X_user_counts)
        # match predicted tag with db
        response = list(df[df.tags == pred[0]].bot_responses)[0]
        # select a random response
        output = response[random.randint(0, len(response) - 1)]
        # extract keywords from user_response and generate new json data
        new_json_data, output = extract_kw(user_response, pred, mypark, myn, output, parks_list, neighborhoods_list,
                                           activities_list, encoding_data, json_data)
        # print output while scraping
        print(f'Bot: {output}')
        if new_json_data == 'skip':
            pass
        else:
            # scrape website
            enter_scrape(new_json_data, cookies, headers, params)


enter_chat()





