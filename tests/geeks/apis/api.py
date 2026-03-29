from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


# With Rest-Ful API

#The Defined Class has to be a ch

#All HTTP Methods are  Defined as Methods in the Class

books = [
    {"id": 1, "title": "Concept of Physics", "author": "H.C Verma"},
    {"id": 2, "title": "Gunahon ka Devta", "author": "Dharamvir Bharti"},
    {"id": 3, "title": "Problems in General Physics", "author": "I.E Irodov"}
]


"""
Understanding API Methods:

GET /books – Returns the complete list of books.
GET /books/<book_id> – Retrieves details of a single book by ID.
POST /books – Adds a new book to the list.
PUT /books/<book_id> – Updates an existing book’s information.
DELETE /books/<book_id> – Removes a book from the list

"""

class BookResource(Resource):
    def get(self, book_id=None):

        # Handling Case where no ID is gived
        if book_id is None:
            return books, 200

        # Checking if book_id is existing
        for book in books:
            if book['id'] == book_id:
                return book, 200 # Returning the book if valud
            
        return {'Error':'Book Not Found'}, 404 # book not found

    def post(self):
        new_book = request.json
        books.append(new_book)
        return new_book, 201 # Status Code Created

    def put(self, book_id): #Updating Existing Books
        for book in books:
            if book['id'] == book_id:
                data = request.json
                book.update(data)
                return book, 200
        return {'error':'Book not found'}, 404


    def delete(self, book_id):
        global books
        index = 0 # index Counter
        for book in books:
            if book['id'] == book_id:
                books.pop(index)
                return books, 200
                
            index += 1

        return {"Error":"Book Not Found"}, 200
        
        

# Making API a inherit resource

class GFG(Resource):
    def get(self):
        return {'Message': "Hello, Get Request"}



# Linking Created API resource to the  Router '/'
api.add_resource(GFG, '/gfg')

#Adding Multiple Resouces to API

api.add_resource(BookResource, '/books', '/books/<int:book_id>')

if __name__ == "__main__":
    app.run(debug=True)