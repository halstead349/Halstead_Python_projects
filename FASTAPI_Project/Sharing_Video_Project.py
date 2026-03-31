from fastapi import FastAPI,HTTPException,File ,UploadFile,Form,Depends
from schema import PostCreate
from db import Post,create_db_and_tables,get_asyncsession
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import shutil
import os
import tempfile


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
# app = FastAPI()   # old declaration 

app = FastAPI(lifespan=lifespan) #new app declaration with database .
'''
# simple hello world example.
# @app.get("/hello-world") # app object is used as decorator along with the endpoint of url.
# def hello_world():
#     return {"message" : "Hello World"}
'''
'''
#Accessing datas from the code as database.
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
'''

# Using extenal databases:
#creating Posts and saving to database.
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption : str = Form(""),
    session: AsyncSession = Depends(get_asyncsession)  # depency injection.
):
    temp_file_path = None
    
    try:
        with tempfile.NamedTemporaryFile(delete=False,suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)
            
        with open(temp_file_path, "rb") as f:
            upload_result = imagekit.upload_file(
                file=f,
                file_name=file.filename
            )
        print(upload_result)
        print(dir(imagekit))
        data = upload_result.response_metadata.raw
        if upload_result.response_metadata.http_status_code == 200:
            
            post = Post(
                caption = caption,
                url = data["url"],
                file_type = "video" if file.content_type.startswith("video/") else "image",
                file_name = data["name"]
            )
            # add to the database:
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()

# retreiving data from db 
@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_asyncsession)
):
    result = await session.execute(select(Post)) # trurns tuple of Posts.
    posts = [row[0] for row in result.all()]
    
    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption" : post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created.isoformat()
            }
        )
        
    return {"posts": posts_data}
