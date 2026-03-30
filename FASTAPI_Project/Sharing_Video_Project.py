from fastapi import FastAPI,HTTPException
from schema import PostCreate
app = FastAPI()
'''
# simple hello world example.
# @app.get("/hello-world") # app object is used as decorator along with the endpoint of url.
# def hello_world():
#     return {"message" : "Hello World"}
'''
text_post = {1:[{"title":"New Post","content":"cool test post"},
             {"title":"New Post","content":"cool test post"},
             {"title":"New Post","content":"cool test post"},
             {"title":"New Post","content":"cool test post"},
             {"title":"New Post","content":"cool test post"},
             {"title":"New Post","content":"cool test post"},
             {"title":"New Post","content":"cool test post"},
             {"title":"New Post","content":"cool test post"},
             {"title":"New Post","content":"cool test post"},
             {"title":"New Post","content":"cool test post"},
             {"title":"New Post","content":"cool test post"},
             {"title":"New Post","content":"cool test post"},
             {"title":"New Post","content":"cool test post"},
             {"title":"New Post","content":"cool test post"},
             
]}

@app.get("/posts")
def get_all_posts(limit : int=None):   # path parameters.
    if limit:
        return list(text_post.values())[0][:limit]
    return text_post

@app.get("/posts/{id}")
def get_posts(id : int):   # Query parameters 
    if id not in text_post:
        raise HTTPException(status_code=404,detail="Post not found")
    
    return text_post.get(id)

@app.post("/posts")
def create_posts(post: PostCreate) -> PostCreate:   # create body 
    new_post = {"title":post.title, "content" : post.content}
    text_post[1].append(new_post)
    return new_post

