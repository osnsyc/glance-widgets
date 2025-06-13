This is a collection of custom widgets for [Glance](https://github.com/glanceapp/glance) using the `custom-api` and `extension` widgets.

### What's the difference between a `custom-api` and `extension` widget?

Custom API widgets are much easier to setup and usually only require a copy-paste into your config. Extension widgets are a bit more involved and require running a separate server or Docker container.

## Custom API Widgets

`custom-api`
- [Chores](widgets/chores-from-baserow/README.md) - show upcoming chores from Baserow sheets
- [Server Stats from Glances](widgets/server-stats-from-glances/README.md) - show server stats from glances, check api for more info
- [Healthchecks stats](widgets/healthchecks-stats/README.md) - show stats from Healthchecks 
- [Twikoo Comments](widgets/recent-twikoo-comments/README.md) - show latest comments from Twikoo 
- [Steam Specials](widgets/steam-specials/README.md) - show a list of discounted games on Steam
- [Recent Plex](widgets/recent-plex/README.md) - show recent activities(TV or Movie) from Plex
- [Cloudflare Stats](widgets/cloudflare-stats/README.md) - show cloudflare Stats
- [Tiny Tiny RSS Stats](widgets/ttrss-stats/README.md) - show stats from Tiny Tiny RSS, 5 lables and health check
- [N8N Error Report](widgets/n8n-error-report/README.md) - show error executions in n8n

`extension`
- [Recent-MoonReader](widgets/recent-moonreader/README.md) - show recent activities from android app MoonReader by parsing cache files
- [Flood Stats](widgets/flood-stats/README.md) - show stats from Flood torrent client
- [Sspai Stats](widgets/sspai-stats/README.md) - show stats of author from site sspai.com
- [Immich Photo](widgets/immich-photo/README.md) - show photo from immich
- [China Gasoline Prices](widgets/China-gasoline-prices/README.md) - show gasoline prices in China (for Chinese users only)

### Customize API 

#TODO
I would recommend [n8n](http://github.com/n8n-io/n8n) to customize api quickly without separate server or container

## More..

- [glanceapp/community-widgets](https://github.com/glanceapp/community-widgets)