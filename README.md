# website
Repo for the group website

## Publications

All papers live in **`data/publications.json`**. Nobody edits the paper lists in the HTML by hand anymore:

- `python gen_people.py` builds each person's page, `people/<slug>/index.html`. The "Selected publications" list contains every paper whose `people` field includes that slug.
- `python gen_papers.py` builds `papers.html`. It contains every paper from `since_year` (set in `data/members.json`) onwards, unless the paper has `"on_lab_page": false`.

### Automatic updates

Every Monday, `.github/workflows/update-publications.yml` runs `fetch_publications.py`. This script reads the [DBLP](https://dblp.org) profile of everyone in `data/members.json`. DBLP also lists arXiv preprints, so these are included. If the script finds something new, it opens a **pull request** with a summary. Someone reviews the PR and merges it; nothing goes online without review.

What the script does:
- **Adds new papers.**
- **Adds lab members** to the `people` field of papers that are already in the file.
- **Fills in a missing link**, if a paper has none.
- **Never rewrites a paper that is already in the file.** When a preprint gets published, the PR only reports it; change `venue`, `url` and `label` by hand.

### Reviewing the pull request
- **Wrong paper:** in the PR, delete its entry from `data/publications.json`, then merge. Its DBLP key stays in `seen_dblp_keys`, so it will not come back.
- **Wrong DBLP profile** (listed under "DBLP profiles found"): fix `dblp_pid` in `data/members.json`.
- **Cosmetic fixes** (title, author surnames, venue): edit the entry directly.

### Editing papers by hand
Each entry looks like this:

```json
{"title": "...", "authors": "Surname, Surname", "venue": "NeurIPS 2026", "year": 2026,
 "label": "NeurIPS", "url": "https://...", "people": ["bortolussi", "candussio"],
 "on_lab_page": true, "order": 10}
```

- `label` is the small text on the left in `papers.html`: a month (`JUL`), a venue (`RV`) or a year.
- `order` sets the position within a year. A lower number puts the paper higher.
- A paper you add by hand is never overwritten by the script.

After editing, run `python gen_people.py && python gen_papers.py`.

### Members
To track a new person, add them to `data/members.json`. Leave `dblp_pid` empty: on the next run, the script looks the person up on DBLP by exact name. To stop tracking someone, set `"fetch": false`.

### One-time setup on GitHub
1. In the repo, go to Settings → Actions → General → Workflow permissions. Select "Read and write permissions" and tick "Allow GitHub Actions to create and approve pull requests".
2. Start the first run by hand: Actions → Update publications → Run workflow.
   - **Bootstrap:** ticking "bootstrap" marks everything that is on DBLP today as already seen. After that, only new papers show up.
   - **No bootstrap:** the first PR proposes every DBLP paper since `since_year` that the site does not list yet.
