from bs4 import BeautifulSoup as bs
from datetime import date
import urllib.request

from config import config
from utils import check_keyword, to_label
from github import Github

ISSUE_BODY_LIMIT_LENGTH = 65536
new_sub_url = 'https://arxiv.org/list/{category}/new'
arxiv_base = "https://arxiv.org/abs/"


def main():
    today = date.today()
    issue_title = 'New papers for {}!'.format(today.strftime('%Y-%m-%d %a'))
    
    filtered_paper_dict = {}
    issue_bodies = ['']
    issue_labels = set()

    git = Github(config['auth_token'])
    repo = git.get_repo(f"{config['repo_owner']}/{config['repo_name']}")
    
    for category, keyword_list in config['keyword_list'].items():
        page = urllib.request.urlopen(new_sub_url.format(category=category))
        soup = bs(page, 'html.parser')
        content = soup.body.find('div', {'id' : 'content'})

        dt_list = content.dl.find_all("dt")
        dd_list = content.dl.find_all("dd")

        assert len(dt_list) == len(dd_list)

        filtered_paper_dict[category] = {
            to_label(keyword) : [] for keyword in keyword_list
        }

        issue_labels = issue_labels.union(set(filtered_paper_dict[category].keys()))

        for i in range(len(dt_list)):
            paper = {}
            paper_number = dt_list[i].text.strip().split(" ")[2].split(":")[-1]
            paper['main_page'] = arxiv_base + paper_number
            paper['pdf'] = arxiv_base.replace('abs', 'pdf') + paper_number

            paper['title'] = dd_list[i].find("div", {"class": "list-title mathjax"}).text.replace("Title: ", "").strip()
            paper['authors'] = dd_list[i].find("div", {"class": "list-authors"}).text.replace("Authors:\n", "").replace("\n", "").strip()
            paper['subjects'] = dd_list[i].find("div", {"class": "list-subjects"}).text.replace("Subjects: ", "").strip()
            paper['abstract'] = dd_list[i].find("p", {"class": "mathjax"}).text.replace("\n", " ").strip()

            for keyword in keyword_list:
                if check_keyword(keyword, paper):
                    filtered_paper_dict[category][to_label(keyword)].append(paper)

        issue_bodies[-1] += '# {} {}\n'.format(config['emoji']['category'], category)
        for keyword, papers in filtered_paper_dict[category].items():
            category_body = ''
            category_body += '## {} {} (total: {})\n'.format(config['emoji']['keyword'], keyword, len(papers))

            if len(papers) == 0:
                category_body += 'No results\n'

            for paper in papers:
                paper_desc = '### {} {}\n'.format(config['emoji']['paper'], paper['title'])
                paper_desc += '- **Authors:** {}\n'.format(paper['authors'])
                paper_desc += '- **Subjects:** {}\n'.format(paper['subjects'])
                paper_desc += '- **Arxiv link:** {}\n'.format(paper['main_page'])
                paper_desc += '- **Pdf link:** {}\n'.format(paper['pdf'])
                paper_desc += '- **Abstract:**\n {}\n'.format(paper['abstract'])
                category_body += paper_desc
            
            # Github issue REST api supports only 65536 characters on body of issue.
            # To handle this problem, in case of 'body > 65536', split bodies into small segments and make them the comments on the issue!
            if len(issue_bodies[-1]) + len(category_body) >= ISSUE_BODY_LIMIT_LENGTH:
                issue_bodies.append(category_body)
            else:
                issue_bodies[-1] += category_body

    # Create issues       
    issue = repo.create_issue(
        title=issue_title,
        body=issue_bodies[0],
        assignees=[config['github_user_id']],
        labels=list(issue_labels)
    )
    
    # If issue_bodies are left, handle them as the comments of the issue!
    for issue_body in issue_bodies[1:]:
        issue.create_comment(issue_body)

if __name__ == '__main__':
    main()

