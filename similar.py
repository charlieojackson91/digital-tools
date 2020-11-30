from difflib import SequenceMatcher

def how_similar(pre_urls,post_urls):
    # split pre and post urls
    split_pre = pre_urls.split('\n')  # this is a list
    split_post = post_urls.split('\n') # this is a list
    # iterate through lists
    if len(split_pre) > 1000 or len(split_post) > 1000:
        return "please enter less than 1000 urls"
    if split_pre[0] == "" or split_post[0] == "":
        return "please enter some urls into the text fields"
    else:
        lst = []
        for pre in split_pre:
            match = -1
            pre = pre.strip()
            for post in split_post:
                post = post.strip()
                # get match
                get_ratio = SequenceMatcher(None, pre, post).ratio()
                # assign highest to match
                if get_ratio > match:
                    match = get_ratio
                    output = pre + " ; " + post + " ; " + str(match) + "\n"
            lst.append(output)
        return lst


# FOR CANNI TOOL

def canni_check(data,brand):
    split_data = data.split('\n') # splits into lines
    if len(split_data) > 1000:
        return "please enter less than 1,000 lines of data"
    else:
        key_list = []
        for line in split_data:
            split_lines = line.split(';') # ['keyword','url']
            key_list.append(split_lines) #  append to list
        count_keywords = count_keys(key_list) # pass list to funtion to count keywords
        dic_to_list = count_keywords.items() # convert dictionary to list
        final_list = []
        for i in dic_to_list:
            key, count = i
            for ii in key_list:
                keyword, url = ii
                if key != keyword:
                    continue
                if count < 2:
                    continue
                if brand == key:
                    continue
                else:
                    concat = keyword + " ; " + url + "\n"
                    final_list.append(concat)
                    
        return final_list

# count the keywords
def count_keys(keyword_counter):
    counter = dict()
    for iteration in keyword_counter:
        keyword, url = iteration
        counter[keyword] = counter.get(keyword,0) + 1 # count how many times keyword is in list
    return counter
