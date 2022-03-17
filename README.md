# Telegraph-API

- It's _very simple_ lib for authomatic posting in [**Telegraph**](https://telegra.ph/)

## Examples
<details>
  <summary>Click to see some basic examples</summary>

### Simple Client

```python
from telegraph_api import Client, Poster

with Client("Alex") as client:
	poster = Poster(client)

post = poster.create_post(
    "Simple Page", 
    "It's simple page in <b>Telegraph</b> with use <b>HTML</b>!")

print(post.text)

# Output: It's simple page in <b>Telegraph</b> with use <b>HTML</b>!
```
</details>