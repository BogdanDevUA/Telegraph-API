from telegraph_api import Client, Poster

with Client("Alex") as client:
	poster = Poster(client)

post = poster.create_post("Simple Page", "It's simple page in <b>Telegraph</b> with use <b>HTML</b>!")

print(post.text)

# Output: It's simple page in <b>Telegraph</b> with use <b>HTML</b>!