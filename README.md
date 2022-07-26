# daily-arxiv-paper
This repository is adapted from https://github.com/kobiso/get-daily-arxiv-noti.

You can be notifed new submitted papers on arxiv.org with filtering by pre-defined keywords. (More than **500** new papers are uploaded on arxiv everyday.)

## What's new?
- Use `PyGithub` package
- Support **domain-by-keywords** (not only `cs` domain)
- Support **AND**, **OR** filtering options
- Handle an error for the limit of issue content's length
  - The length of issue description can not exceed 65,536

## Installation
- python >= 3.x
- PyGithub

```python
git clone 
pip install PyGithub
```

## Usage
### 1. Create a new repository to get notification of new papers
The notification is save by creating a github issue. see an [example](https://github.com/yhytoto12/daily-arxiv-paper/issues/1)  

### 2. Set a configuration
Refer to [config.py](https://github.com/yhytoto12/daily-arxiv-paper/blob/main/config.py) and set your configuration. 

You can change `keyword_list` on your preference. The keys of `keyword_list` are categories of arxiv papers (see [this](https://arxiv.org/)). Also, there are **3 keyword options** to filter papers.
- **str** - check if a keyword is in paper's title or abstract
- **tuple** - check if all keywords are in paper's title or abstract
- **list** - check if any keyword is in paper's title or abstract  

```python
config = {
  # For github issue api
  'repo_name' : 'your-github-repo',
  'repo_owner' : 'yhytoto12',
  'github_user_id' : 'yhytoto12',
  
  # Do not keep this pulbic
  'auth_token' : 'your-auth-token',

  # Cute emoji
  'emoji' : {
    'category' : '💻',
    'keyword' : '📚',
    'paper' : '📃',
  },

  # Keyword list --> 'key' : category, 'value' : list of keywords
  # str   --> check if a keyword is in paper's title or abstract
  # tuple --> check if all keywords are in paper's title or abstract
  # list  --> check if any keyword is in paper's title or abstract
  'keyword_list': {
    'cs': [
      'mask',
      ['multimodal', 'multi-modal', 'multiple modalities'],
      'navigation',
      'self-supervised',
    ],
    
    'stat': [
      'bayesian',
      'mutual information',
    ],
  },
}
```

### 3. Set a crontab as below
[crontab](https://crontab.guru/) for linux can manage your services by running your codes periodically. The arxiv.org announces the new submission papers according to the [announcement schedule](https://arxiv.org/help/availability).
```bash
crontab -e
0 11 * * mon-fri python /path/to/dir/daily-arxiv-paper/main.py
```


 
