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

