# Recent Twikoo Comments

show latest comments from Twikoo

![](preview.png)

## Method 1

For those who deploy twikoo in cloudflare.

```yaml
- type: custom-api
  title: Twikoo
  cache: 6h
  url: https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/d1/database/${CF_DB_ID}/query
  headers:
    X-Auth-Email: ${CF_ACCOUNT_MAIL}
    X-Auth-Key: ${CF_API_TOKEN}
  method: POST
  bodyType: json
  body: {"sql":"SELECT * FROM comment ORDER BY created DESC LIMIT 5;"}
  template: |
      <ul class="list list-gap-10 collapsible-container" data-collapse-after="3">
      {{ range $i, $v := .JSON.Array "result.0.results" }}
        <li>
          {{ $nick := $v.String "nick" }}
          {{ $comment := $v.String "comment" }}
          {{ $updated := $v.Int "updated" }}
          {{ $seconds := div $updated 1000 }}
          <div style="width: 90%; margin: auto; word-break: break-word; overflow-wrap: break-word; white-space: normal;">
            <span class="size-base color-positive">{{ $nick }}</span>
            <span class="size-base color-highlight">：{{findSubmatch "<p>(.*?)</p>" $comment}}</span>
          </div>
        </li>
      {{ end }}
      </ul>
```

### Environment variables

- `${CF_ACCOUNT_ID}` - see [find-account-and-zone-ids](https://developers.cloudflare.com/fundamentals/account/find-account-and-zone-ids/)
- `${CF_DB_ID}` - the database ID will be displayed on the overview or settings page for that specific D1 database instance.
- `${CF_ACCOUNT_MAIL}` - cloudflare user's email 
- `${CF_API_TOKEN}` - see [Cloudflare API](https://developers.cloudflare.com/api/)

## Method 2

```yaml
- type: custom-api
  title: Twikoo
  cache: 6h
  url: ${TWIKOO_ENVID}
  headers:
    authority: ${TWIKOO_ENVID}
    content-type: application/json
    Accept: application/json
  method: POST
  bodyType: json
  body: {"event":"COMMENT_GET_FOR_ADMIN","accessToken":"${TWIKOO_TOKEN}","per":5,"page":1,"keyword":"","type":""}
  template: |
      <ul class="list list-gap-10 collapsible-container" data-collapse-after="3">
      {{ range $i, $v := .JSON.Array "data" }}
        <li>
          {{ $nick := $v.String "nick" }}
          {{ $comment := $v.String "comment" }}
          {{ $updated := $v.Int "updated" }}
          {{ $seconds := div $updated 1000 }}
          <div style="width: 90%; margin: auto; word-break: break-word; overflow-wrap: break-word; white-space: normal;">
            <span class="size-base color-positive">{{ $nick }}</span>
            <span class="size-base color-highlight">：{{findSubmatch "<p>(.*?)</p>" $comment}}</span>
          </div>
        </li>
      {{ end }}
      </ul>
```

### Environment variables

- `${TWIKOO_ENVID}` - like `https://comments.osnsyc.top`.
- `${TWIKOO_TOKEN}` - login twikoo account through browser-press`F12`or`CTRL+SHIFT+C`or`Command+SHIFT+C`-`Network`-`Fetch/XHR`-reload login twikoo-click`${TWIKOO_ENVID}`-`paylod`-`accessToken`
