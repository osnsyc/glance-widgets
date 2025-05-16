# Random photo from Immich

show photo from immich

![](preview.png)

```yaml
- type: custom-api
  title: Immich Memory
  hide-header: true
  cache: 1h
  template: |
    <div>
      <img loading="lazy" src="/assets/memory.png" style="width: 100%; display: block; margin: 0 auto;">
    </div>
```
## Styling a photo

- Set the variables `FONT`,`EXPORT_PATH`,`BASE_URL`,`API_KEY`,`PAYLOAD` in `styling_img.py`
- Run the script to generate a polaroid-like photo `python styling_img.py` (test in `python 3.10`)
- For scheduled execution (e.g., daily at 7:05 AM), add to crontab: `5 7 * * * cd /path/to/script && python styling_img.py`
- Modify `PAYLOAD` to filter different photo sets.
