# from fastapi import FastAPI, HTTPException, Query
# from pydantic import BaseModel, Field
# from typing import List, Optional,Dict
# from datetime import datetime
# from collections import Counter, defaultdict
# import pandas as pd


# app = FastAPI()

# class Borrower(BaseModel):
#     name: str
#     age: Optional[int]
#     gender: Optional[str]
#     address: Optional[str]
#     mobile: Optional[int]
#     category: str
#     borrow_days: Optional[int] = None

# class BookData(BaseModel):
#     title: str
#     author: str
#     copies: int
#     max_borrow_days: int

# class BorrowedRecord(BaseModel):
#     user_name: str
#     user_age: Optional[int]
#     user_gender: Optional[str]
#     user_address: Optional[str]
#     user_mobile: Optional[int]
#     title: str
#     author: str
#     borrow_days: int
#     borrow_time: datetime



# books = {
#     "spiritual": [
#         BookData(title="Autobiograpy of Yogi", author="Paramahansa Yogananda", copies=3, max_borrow_days=7),
#         BookData(title="Bhagavad Gita", author="Ved Vyasa", copies=2, max_borrow_days=5)
#     ],
#     "murder-mystry": [
#         BookData(title="Sherlock Holmes", author="Arthur Conan Doyle", copies=2, max_borrow_days=5),
#         BookData(title="Gone Girl", author="Gillian Flynn", copies=1, max_borrow_days=4)
#     ],
#     "realistic": [
#         BookData(title="Rich Dad Poor Dad", author="Robert Kiyosaki", copies=4, max_borrow_days=10),
#         BookData(title="The Alchemist", author="Paulo Coelho", copies=2, max_borrow_days=6)
#     ]
# }
# books=pd.DataFrame
# borrowed_data: List[BorrowedRecord] = []

# @app.get("/categories")
# def get_categories():
#     return {"available_categories": list(books.keys())}
# @app.get("/category/{category_name}")
# def get_books_in_category(category_name: str):
#     category = category_name.lower()
#     category_books = books.get(category)
#     if not category_books:
#         raise HTTPException(status_code=404, detail="Category not found")
#     return {
#         "category": category,
#         "books": [
#             {
#                 "title": book.title,
#                 "author": book.author,
#                 "available_copies": book.copies,
#                 "max_borrow_days": book.max_borrow_days
#             }
#             for book in category_books
#         ]
#     }

# @app.post("/borrow")
# def borrow_book(borrower: Borrower, book_title: str = Query(...)):
#     category_books = books.get(borrower.category.lower())
#     if not category_books:
#         raise HTTPException(status_code=400, detail="Invalid category")

#     selected_book = next((b for b in category_books if b.title.lower() == book_title.lower()), None)
#     if not selected_book:
#         raise HTTPException(status_code=404, detail="Book not found in this category")

#     if selected_book.copies <= 0:
#         raise HTTPException(status_code=409, detail="No copies left to borrow")

#     selected_book.copies -= 1
#     record = BorrowedRecord(
#         user_name=borrower.name,
#         user_age=borrower.age,
#         user_gender=borrower.gender,
#         user_address=borrower.address,
#         user_mobile=borrower.mobile,
#         title=selected_book.title,
#         author=selected_book.author,
#         borrow_days=borrower.borrow_days or selected_book.max_borrow_days,
#         borrow_time=datetime.now()
#     )
#     borrowed_data.append(record)

#     return {
#         "message": f"{borrower.name} successfully borrowed '{selected_book.title}'",
#         "remaining_copies": selected_book.copies,
#         "record": record
#     }
   

# @app.get("/borrowed/{user_name}")
# def books_by_user(user_name: str):
#     user_books = [b for b in borrowed_data if b.user_name.lower() == user_name.lower()]
#     if not user_books:
#         return {"message": f"No books borrowed by {user_name}"}
#     return {"borrowed_books": user_books}
# @app.get("/stats")
# def book_statistics() -> Dict[str, Dict[str, List[Dict]]]:
#     borrow_counter = Counter()

#     stats = {}
#     for category, book_list in books.items():
#         stats[category] = []
#         for book in book_list:
#             stats[category].append({
#                 "title": book.title,
#                 "author": book.author,
#                 "available_copies": book.copies,
#                 "times_borrowed": borrow_counter.get(book.title, 0)
#             })

#     return {"book_statistics": stats} 

# @app.get("/common")
# def common_books():
#     from collections import defaultdict
#     title_map = defaultdict(set)
#     for entry in borrowed_data:
#         title_map[entry.title].add(entry.user_name)

#     common = {title: list(users) for title, users in title_map.items() if len(users) > 1}
#     return {"common_books": common}
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from collections import Counter, defaultdict
import pandas as pd

app = FastAPI()

# 📘 Models
class Borrower(BaseModel):
    name: str
    age: Optional[int]
    gender: Optional[str]
    address: Optional[str]
    mobile: Optional[int]
    category: str
    borrow_days: Optional[int] = None

class BookData(BaseModel):
    title: str
    author: str
    copies: int
    max_borrow_days: int

class BorrowedRecord(BaseModel):
    user_name: str
    user_age: Optional[int]
    user_gender: Optional[str]
    user_address: Optional[str]
    user_mobile: Optional[int]
    title: str
    author: str
    borrow_days: int
    borrow_time: datetime

# 📚 Book Inventory
books = {
    "spiritual": [
        BookData(title="Autobiograpy of Yogi", author="Paramahansa Yogananda", copies=3, max_borrow_days=7),
        BookData(title="Bhagavad Gita", author="Ved Vyasa", copies=2, max_borrow_days=5)
    ],
    "murder-mystry": [
        BookData(title="Sherlock Holmes", author="Arthur Conan Doyle", copies=2, max_borrow_days=5),
        BookData(title="Gone Girl", author="Gillian Flynn", copies=1, max_borrow_days=4)
    ],
    "realistic": [
        BookData(title="Rich Dad Poor Dad", author="Robert Kiyosaki", copies=4, max_borrow_days=10),
        BookData(title="The Alchemist", author="Paulo Coelho", copies=2, max_borrow_days=6)
    ]
}

borrowed_data: List[BorrowedRecord] = []

# 📂 Endpoints

@app.get("/categories")
def get_categories():
    return {"available_categories": list(books.keys())}

@app.get("/category/{category_name}")
def get_books_in_category(category_name: str):
    category = category_name.lower()
    category_books = books.get(category)
    if not category_books:
        raise HTTPException(status_code=404, detail="Category not found")
    return {
        "category": category,
        "books": [
            {
                "title": book.title,
                "author": book.author,
                "available_copies": book.copies,
                "max_borrow_days": book.max_borrow_days
            }
            for book in category_books
        ]
    }

@app.post("/borrow")
def borrow_book(borrower: Borrower, book_title: str = Query(...)):
    category_books = books.get(borrower.category.lower())
    if not category_books:
        raise HTTPException(status_code=400, detail="Invalid category")

    selected_book = next((b for b in category_books if b.title.lower() == book_title.lower()), None)
    if not selected_book:
        raise HTTPException(status_code=404, detail="Book not found in this category")

    if selected_book.copies <= 0:
        raise HTTPException(status_code=409, detail="No copies left to borrow")

    selected_book.copies -= 1
    record = BorrowedRecord(
        user_name=borrower.name,
        user_age=borrower.age,
        user_gender=borrower.gender,
        user_address=borrower.address,
        user_mobile=borrower.mobile,
        title=selected_book.title,
        author=selected_book.author,
        borrow_days=borrower.borrow_days or selected_book.max_borrow_days,
        borrow_time=datetime.now()
    )
    borrowed_data.append(record)

    return {
        "message": f"{borrower.name} successfully borrowed '{selected_book.title}'",
        "remaining_copies": selected_book.copies,
        "record": record
    }

@app.get("/borrowed/{user_name}")
def books_by_user(user_name: str):
    user_books = [b for b in borrowed_data if b.user_name.lower() == user_name.lower()]
    if not user_books:
        return {"message": f"No books borrowed by {user_name}"}
    return {"borrowed_books": user_books}

@app.get("/stats")
def book_statistics() -> Dict[str, Dict[str, List[Dict]]]:
    borrow_counter = Counter([record.title for record in borrowed_data])
    stats = {}
    for category, book_list in books.items():
        stats[category] = []
        for book in book_list:
            stats[category].append({
                "title": book.title,
                "author": book.author,
                "available_copies": book.copies,
                "times_borrowed": borrow_counter.get(book.title, 0)
            })
    return {"book_statistics": stats}

@app.get("/common")
def common_books():
    title_map = defaultdict(set)
    for entry in borrowed_data:
        title_map[entry.title].add(entry.user_name)

    common = {title: list(users) for title, users in title_map.items() if len(users) > 1}
    return {"common_books": common}



@app.get("/borrowed/table/html", response_class=HTMLResponse)
def borrowed_table_html():
    rows = []

    for category, book_list in books.items():
        for book in book_list:
            for record in borrowed_data:
                if record.title == book.title and record.author == book.author:
                    rows.append({
                        "Category": category,
                        "Book Title": book.title,
                        "Author": book.author,
                        "Available Copies": book.copies,
                        "Max Borrow Days": book.max_borrow_days,
                        "Borrower Name": record.user_name,
                        "Age": record.user_age,
                        "Gender": record.user_gender,
                        "Address": record.user_address,
                        "Mobile": record.user_mobile,
                        "Borrow Days": record.borrow_days,
                        "Borrow Time": record.borrow_time.strftime("%Y-%m-%d %H:%M:%S")
                    })

    df = pd.DataFrame(rows)
    html_table = df.to_html(index=False, border=1)
    return f"<html><body><h2>Borrowed Book Records</h2>{html_table}</body></html>"

