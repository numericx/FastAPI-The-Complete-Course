from datetime import date
from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status


class Book:
    """
    A class to represent a book.

    Attributes
    ----------
    id : int
        unique identifier for the book
    title : str
        title of the book
    author : str
        author of the book
    description : str
        description of the book
    rating : int
        rating of the book
    publish_date : int
        publish date of the book
    """    
    id: int
    title: str
    author: str
    description: str
    rating: int
    publish_date: int

    def __init__(self, id, title, author, description, rating, publish_date):
        """
        Constructs all the necessary attributes for the book object.

        Parameters
        ----------
            id : int
                unique identifier for the book
            title : str
                title of the book
            author : str
                author of the book
            description : str
                description of the book
            rating : int
                rating of the book
            publish_date : int
                publish date of the book
        """        
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date

class BookRequest(BaseModel):
    """
    A class to represent a book request.

    Attributes
    ----------
    id : Optional[int]
        unique identifier for the book
    title : str
        title of the book
    author : str
        author of the book
    description : str
        description of the book
    rating : int
        rating of the book
    publish_date : int
        publish date of the book
    """    
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    publish_date: int = Field(gt=1499, lt=date.today().year + 1)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'codingwithroby',
                'description': 'A new description of a book',
                'rating': 5,
                'publish_date': 2022
            }
        }   

# List of books    
BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithcody', 'A very nice book!', 5, 2012),
    Book(2, 'Be Fast with FastAPI', 'codingwithcody', 'A great book!', 5, 2022),
    Book(3, 'Master Endpoints', 'codingwithcody', 'A awesome book!', 5, 1992),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2000),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2022),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2023)
]

app = FastAPI()

def find_book_id(book: Book):
    """
    Function to find the book id.

    Parameters
    ----------
    book : Book
        an instance of the Book class

    Returns
    -------
    Book
        an instance of the Book class with updated id
    """    

    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    return book

@app.get(path="/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    """
    Endpoint to get all books.

    Returns
    -------
    list
        a list of all books
    """    
    return BOOKS

@app.get(path="/books/", status_code=status.HTTP_200_OK)
async def read_books_by_rating(rating: int = Query(gt=0, lt=6)):
    """
    Endpoint to get books by rating.

    Parameters
    ----------
    rating : int
        rating of the book

    Returns
    -------
    list
        a list of books with the specified rating
    """    
    return [book for book in BOOKS if book.rating == rating]

@app.get(path="/books/{book_id}")
async def get_book_by_id(book_id: int = Path(gt=0)):
    """
    Endpoint to get a book by id.

    Parameters
    ----------
    book_id : int
        unique identifier for the book

    Returns
    -------
    Book
        an instance of the Book class with the specified id

    Raises
    ------
    HTTPException
        if the book with the specified id is not found
    """    
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found.")
        
@app.get(path="/books/publish/", status_code=status.HTTP_200_OK)
async def get_books_by_date(publish_date: int = Query(gt=1499, lt=date.today().year + 1)):
    """
    Endpoint to get books by publish date.

    Parameters
    ----------
    publish_date : int
        publish date of the book

    Returns
    -------
    list
        a list of books with the specified publish date
    """    
    return [book for book in BOOKS if book.publish_date == publish_date]        
        
@app.put(path="/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(update_book: BookRequest):
    """
    Endpoint to update a book.

    Parameters
    ----------
    update_book : BookRequest
        an instance of the BookRequest class

    Raises
    ------
    HTTPException
        if the book with the specified id is not found
    """    
    updated = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == update_book.id:
            BOOKS[i] = update_book
            updated = True
            break
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found.")

@app.put(path="/books/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    """
    Endpoint to create a book.

    Parameters
    ----------
    book_request : BookRequest
        an instance of the BookRequest class
    """    
    book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(book))

@app.delete(path="/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0), status_code=status.HTTP_204_NO_CONTENT):
    """
    Endpoint to delete a book.

    Parameters
    ----------
    book_id : int
        unique identifier for the book

    Raises
    ------
    HTTPException
        if the book with the specified id is not found
    """    
    deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            del BOOKS[i]
            deleted = True
            break
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found.")