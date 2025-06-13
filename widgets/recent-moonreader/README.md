# Recent-MoonReader

show recent activities from android app MoonReader by parsing cache files

![](preview.png)

```yaml
- type: custom-api
  title: 近期阅读
  cache: 2h
  url: ${MOONREADER_STATS_ENDPOINT}
  headers:
    Accept: application/json
  template: |
    <div>
        {{ $title := .JSON.String "title" }}
        {{ $author_sort := .JSON.String "author_sort" }}
        {{ $percentage := .JSON.Float "percentage" }}
        {{ $last_modified := .JSON.String "last_modified" }}
        {{ $last_note := .JSON.String "last_note.text" }}

        <li style="display: flex; align-items: center; gap: 8px;>">
          <img loading="lazy" src="/assets/mr.jpg"  style="width: 64px; border-radius: var(--border-radius); margin-right: 10px;">
          <div>
            <span class="size-h3 color-primary">{{ $title }}</span><br>
            {{if $last_note}}
              <span class="size-h5 color-highlight">{{ $author_sort }}</span><br>
              <div style="overflow: auto; max-height: 4rem; scrollbar-width: none;">{{ $last_note }}</div>
              <span class="size-h5 color-subdue">进度{{ $percentage }}% · {{ $last_modified }}</span>
            {{ else}}
              <span class="size-h3 color-highlight">{{ $author_sort }}</span><br>
              <span class="size-h3 color-subdue">进度{{ $percentage }}% · {{ $last_modified }}</span>
            {{end}}
            
          </div>
        </li>
    </div>
```
## Environment variables

- `${MOONREADER_STATS_ENDPOINT}` - `http://LOCALHOST:GLANCE_PORT/assets/moonreader.json`.

## Prepare data

```bash
git clone https://github.com/osnsyc/MoonReader_tools.git
```

Copy `get_activities.py` to `/MoonReader_tools`

```bash
python get_activities.py
```

Paths `MOONREADER_CACHE`, `CALIBRE_DB`, `CALIBRE_LIB` and `GLANCE_ASSETS` in `get_activities.py` are hardcoded — adjust them.

This will create or update the file: `/path/to/glance/assets/moonreader.json`

To also retrieve the book's author and copy its cover image (`cover.jpg`) from the Calibre library:

```bash
python get_activities.py --cover
```

This will:

-  Look up the book by title in the Calibre SQLite database (`metadata.db`)
-  Copy the corresponding `cover.jpg` to: `/path/to/glance/assets/mr.jpg`
-  Add the author's name to the JSON file

