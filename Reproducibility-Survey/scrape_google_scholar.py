#import the liberary
import requests
from time import sleep
import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import sys
import argparse

# The code is adpated from https://medium.com/@nandinisaini021/scraping-publications-of-aerial-image-research-papers-on-google-scholar-using-python-a0dee9744728

# this function for the getting inforamtion of the web page
def get_paperinfo(paper_url):

    #download the page
    response=requests.get(paper_url)
    # check successful response
    if response.status_code != 200:
        print('Status code:', response.status_code)
        raise Exception('Failed to fetch web page ')

    #parse using beautiful soup
    paper_doc = BeautifulSoup(response.text,'html.parser')

    return paper_doc

# this function for the extracting information of the tags
def get_tags(doc):
    paper_tag = doc.select('[data-lid]')
    cite_tag = doc.select('[title=Cite] + a')
    link_tag = doc.find_all('h3',{"class" : "gs_rt"})
    author_tag = doc.find_all("div", {"class": "gs_a"})

    return paper_tag,cite_tag,link_tag,author_tag

# it will return the title of the paper
def get_papertitle(paper_tag):

    paper_names = []

    for tag in paper_tag:
        try:
            paper_title = tag.select('h3')[0].get_text()  
        except:
            paper_title ="xx"
            print('Exception: Empty Paper Title')
            pass
        paper_names.append(paper_title)

    return paper_names

# it will return the number of citation of the paper
def get_citecount(cite_tag):
    cite_count = []
    for i in cite_tag:
        cite = i.text
        if i is None or cite is None:  # if paper has no citatation then consider 0
            cite_count.append(0)
        else:
            tmp = re.search(r'\d+', cite) # its handle the None type object error and re use to remove the string " cited by " and return only integer value
            if tmp is None :
                cite_count.append(0)
            else :
                cite_count.append(int(tmp.group()))

    return cite_count

# function for the getting link information
def get_link(link_tag):

    links = []

    for i in range(len(link_tag)) :
        try:
            links.append(link_tag[i].a['href'])
        except:
            links.append("xx")
            print('Exception: Empty Link')
            pass

    return links

# function for the getting autho , year and publication information
def get_author_year_publi_info(authors_tag):
    years = []
    publication = []
    authors = []
    for i in range(len(authors_tag)):
        authortag_text = (authors_tag[i].text).split()
        try:
            year = int(re.search(r'\d+', authors_tag[i].text).group())
        except:
            year= "xx"
            print('Exception: Empty Year')
            pass
        years.append(year)
        publication.append(authortag_text[-1])
        author = authortag_text[0] + ' ' + re.sub(',','', authortag_text[1])
        authors.append(author)

    return years , publication, authors

# creating final dictional for storing the result
paper_repos_dict = {
    'PaperTitle' : [],
    'Year' : [],
    'Author' : [],
    'Citation' : [],
    'Publication' : [],
    'URL' : []
}

# adding information in the dictionary
def add_in_paper_repo(papername,year,author,cite,publi,link):
    if papername in paper_repos_dict['PaperTitle']:
        print('Paper name exists: Duplicate')
        return
    paper_repos_dict['PaperTitle'].extend(papername)
    paper_repos_dict['Year'].extend(year)
    paper_repos_dict['Author'].extend(author)
    paper_repos_dict['Citation'].extend(cite)
    paper_repos_dict['Publication'].extend(publi)
    paper_repos_dict['URL'].extend(link)
    df = pd.DataFrame.from_dict(paper_repos_dict, orient='index')
    df = df.transpose()

    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword_search_term", help="Enter the keyword search term")
    parser.add_argument("outputfile", help="Enter the name of the csv file where the output will be written")
    args = parser.parse_args()

    # Config Parameters for the Google Scholar URL
    end_year  = 2021
    max_pages = 11
    language = 'en'

    keyword_search_term = '"' + args.keyword_search_term+ '"'
    outputfile = args.outputfile

    pages = np.arange(0,(max_pages*10),10)

    for page in pages:
        url = 'https://scholar.google.com/scholar?start={}&q={}+&hl={}&as_sdt=0,5&as_yhi={}'.format(page, keyword_search_term, language, end_year)
        # url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0,5&q={}'.format(keyword_search_term)

        print(f"Scraping page {int(page/10) + 1} for the keyword search term '{keyword_search_term}' with the url {url}")

        # function for the get content
        doc = get_paperinfo(url)

        # function for the collecting tags
        paper_tag,cite_tag,link_tag,author_tag = get_tags(doc)
        if not paper_tag:
            print(f"Finished scraping at page {int(page/10)}")
            break

        # paper titles
        papernames = get_papertitle(paper_tag)

        # year , author , publication of the papers
        year, publication , author = get_author_year_publi_info(author_tag)

        # cite count of the papers
        cite = get_citecount(cite_tag)

        # url of the papers
        link = get_link(link_tag)

        df = add_in_paper_repo(papernames,year,author,cite,publication,link)

        # use sleep to avoid status code 429
        sleep(30)

    # Print the result to the output csv file
    print(f"Writing the results to the file: '{outputfile}'")
    df.to_csv(outputfile, mode='w', index=False)


if __name__ == "__main__":
    main()
