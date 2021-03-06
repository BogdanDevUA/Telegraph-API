# Telegraph-API

- It's _very simple_ lib for authomatic posting in [**Telegraph**](https://telegra.ph/)

## Examples

<details>
  <summary>Client</summary>

### Simple Client

```python
from telegraph_api import Client, Poster

poster = None
async def main():
  with Client("Alex") as client:
    poster = Poster(client)
    post = await poster.create_post(
      "Simple Page", 
      "It's simple page in <b>Telegraph</b> with use <b>HTML</b>!")

  print(post.text)

poster.run(main())
# Output: It's simple page in <b>Telegraph</b> with use <b>HTML</b>!
```

</details>

<details>
  <summary>Poster</summary>

### Page downloader

```python
from telegraph_api import Client, Poster
from telegraph_api.types import Post

client = Client("Alex")
poster = Poster(client)

page = "https://telegra.ph/Simple-page-02-10"

poster.run(poster.get_page(page))

# Out: ...
```

</details>
