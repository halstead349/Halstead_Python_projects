from fastapi import FastAPI,Request,HTTPException,status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
# from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates # to import the template files.-> template files a text files including html logics in jinja syntaxs.
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

# Basic fastapi app:
# posts: list[dict] = [ 
#     {
#         "id": 1,
#         "author": "Corey Schafer",
#         "title": "FastAPI is Awesome",
#         "content": "This framework is really easy to use and super fast.",
#         "date_posted": "April 20, 2025",
#     },
#     {
#         "id": 2,
#         "author": "Jane Doe",
#         "title": "Python is Great for Web Development",
#         "content": "Python is a great language for web development, and FastAPI makes it even better",
#         "date_posted": "April 21, 2025",
#     },
# ]

# @app.get("/",response_class=HTMLResponse,include_in_schema=False) #root directory api.
# @app.get("/posts",response_class=HTMLResponse,include_in_schema=False)
# def home():
#     # return {"message" : "Hello wrold"}
#     return f"<h1>{posts[0]['title']}</h1>"

# @app.get("/api/posts")
# def get_posts():
#     return posts

posts: list[dict] = [ 
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better",
        "date_posted": "April 21, 2025",
    },
]

templates = Jinja2Templates(directory="templates") # assigning template files directory

app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/",include_in_schema=False,name="home")
@app.get("/posts",include_in_schema=False, name="posts")
def home(request : Request ):
    return templates.TemplateResponse(request , "home.html",{"posts":posts,"title":"Home"})

@app.get("/api/posts/{post_id}") # path parameter -> given to the path signature .eg is { post_id }
def get_post(post_id : int): # type hint is important in fastapi to validate the parameter.
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= "Post not found") # error handling.

@app.get("/posts/{post_id}",include_in_schema=False) # path parameter -> given to the path signature .eg is { post_id }
def post_page(post_id : int , request:Request): # type hint is important in fastapi to validate the parameter.
    for post in posts:
        if post.get("id") == post_id:
            title = post["title"][:50]
            return templates.TemplateResponse(request , "post.html",{"post":post,"title":title})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= "Post not found") # error handling.

## StarlettleHTTPException Handler
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request,exception : StarletteHTTPException):
    message =(exception.detail
              if exception.detail
              else "An error occured. Please check your request and try again."
              ) # ternary operator or conditional expression. () is used here for implicit line joining.
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail":message}
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        { # context dictionary
            "status_code" : exception.status_code,
            "title" : exception.status_code,
            "message": message
        },
        status_code=exception.status_code,
    )

## RequestValidationError Handler:

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        { # context -> dictionary
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title" : status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message" : "Invalid request.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
    