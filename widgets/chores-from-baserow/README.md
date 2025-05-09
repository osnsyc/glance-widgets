# Chores from Baserow

show upcoming chores from Baserow sheets

![](preview.png)

```yaml
- type: custom-api
  title: Upcoming Chores
  cache: 1d
  url: ${BASEROW_ENDPOINT}
  headers:
    Authorization: ${BASEROW_TOKEN}
    Accept: application/json
  template: |
    {{ $count := .JSON.Int "count" }}
    {{ if eq $count 0 }}
      <li class="flex items-center color-primary size-h3">
        <span class="grow min-width-0"> All Done</span>
        <span class="shrink-0 text-right">
          <div class="monitor-site-status-icon-compact">
            <svg fill="var(--color-positive)" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm3.857-9.809a.75.75 0 0 0-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 1 0-1.06 1.061l2.5 2.5a.75.75 0 0 0 1.137-.089l4-5.5Z" clip-rule="evenodd" />
            </svg>
          </div>
        </span>
      </li>
    {{ else }}
      {{ range $i, $v := .JSON.Array "results" }}
        {{ $name := $v.String "Name" }}
        {{ $nextday := $v.String "下次执行" }}
        {{ $lastday := $v.String "Rollup" }}
        {{ $expired := $v.Bool "Expired" }}

        <li class="flex items-center color-primary size-h3">
          <span class="grow min-width-0"> {{$name}} </span>
          <span class="shrink-0 text-right">
            <div class="monitor-site-status-icon-compact" title="{{ $lastday }}">
              {{ if $expired }}
                <svg fill="var(--color-negative)" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495ZM10 5a.75.75 0 0 1 .75.75v3.5a.75.75 0 0 1-1.5 0v-3.5A.75.75 0 0 1 10 5Zm0 9a1 1 0 1 0 0-2 1 1 0 0 0 0 2Z" clip-rule="evenodd" />
                </svg>                        
              {{ else }}
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="var(--color-positive)" class="size-6">
                  <path d="M5.85 3.5a.75.75 0 0 0-1.117-1 9.719 9.719 0 0 0-2.348 4.876.75.75 0 0 0 1.479.248A8.219 8.219 0 0 1 5.85 3.5ZM19.267 2.5a.75.75 0 1 0-1.118 1 8.22 8.22 0 0 1 1.987 4.124.75.75 0 0 0 1.48-.248A9.72 9.72 0 0 0 19.266 2.5Z" />
                  <path fill-rule="evenodd" d="M12 2.25A6.75 6.75 0 0 0 5.25 9v.75a8.217 8.217 0 0 1-2.119 5.52.75.75 0 0 0 .298 1.206c1.544.57 3.16.99 4.831 1.243a3.75 3.75 0 1 0 7.48 0 24.583 24.583 0 0 0 4.83-1.244.75.75 0 0 0 .298-1.205 8.217 8.217 0 0 1-2.118-5.52V9A6.75 6.75 0 0 0 12 2.25ZM9.75 18c0-.034 0-.067.002-.1a25.05 25.05 0 0 0 4.496 0l.002.1a2.25 2.25 0 1 1-4.5 0Z" clip-rule="evenodd" />
                </svg>
              {{ end }}
            </div>
          </span>
        </li>
        <li class="flex items-center">
          Expire: {{$nextday}}
        </li>
      {{ end }}
    {{ end }}
```
## Environment variables

- `${BASEROW_ENDPOINT}` - like `http://192.168.1.1:8000/api/database/rows/table/1/?user_field_names=true&view_id=22`.
- `${BASEROW_TOKEN}` like `Token xxxxxxxxxxxxxxxxxxx`