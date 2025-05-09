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

- `${MOONREADER_STATS_ENDPOINT}` - #TODO.

