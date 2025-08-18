from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from models.book_model import Book, db
from models.author_model import Author

app = Flask(__name__)
swagger = Swagger(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/books', methods=['GET'])
def get_books():
    """
    Get all books
    ---
    responses:
      200:
        description: List of books
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              author:
                type: string
      500:
        description: Internal server error
    """
    books = Book.query.all()
    books_list = []
    for book in books:
        books_list.append({
            'id': book.id,
            'title': book.title,
            'author': book.author.name
        })
    return jsonify(books_list), 200

@app.route('/authors', methods=['GET'])
def get_author():
    """
    Get all authors
    ---
    responses:
      200:
        description: List of authors
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
      500:
        description: Internal server error
    """
    authors = Author.query.all()
    authors_list = []
    for author in authors:
        authors_list.append({
            'id' : author.id,
            'name' : author.name
        })
    return jsonify(authors_list), 200

@app.route('/books', methods=['POST'])
def add_new_book():
    """
    Add a new book
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - title
            - author
          properties:
            title:
              type: string
              example: War and Peace
            author:
              type: string
              example: Leo Tolstoy
    responses:
      201:
        description: Book created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            author:
              type: string
      400:
        description: Bad request (missing title or author)
      500:
        description: Internal server error
    """
    data = request.get_json()

    if data is None or 'title' not in data or 'author' not in data:
        abort(400, description=f'Title or author not provided')
    title = data['title']
    author_name = data['author']

    author = Author.query.filter_by(name=author_name).first()
    if not author:
        author = Author(name=author_name)
        db.session.add(author)
        db.session.commit()

    new_book = Book(title=title,author_id=author.id)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'id':new_book.id, 'title':new_book.title, 'author': author.name}), 201

@app.route('/authors', methods=['POST'])
def add_new_author():
    """
    Add a new author
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              example: Leo Tolstoy
    responses:
      201:
        description: Author created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
      400:
        description: Bad request (missing name)
      500:
        description: Internal server error
    """
    data = request.get_json()

    if data is None or 'name' not in data:
        abort(400, description='Name not provided')
    name = data['name']
    new_author = Author(name=name)
    db.session.add(new_author)
    db.session.commit()
    return jsonify({'id': new_author.id, 'name': new_author.name}), 201

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    """
    Get a book by ID
    ---
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: ID of the book
    responses:
      200:
        description: Book found
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            author:
              type: string
      404:
        description: Book not found
      500:
        description: Internal server error
    """
    book = db.session.get(Book, book_id)
    if book is None:
        abort(404,'Book not found')
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author.name}), 200

@app.route('/authors/<int:author_id>', methods=['GET'])
def get_author_by_id(author_id):
    """
    Get author by ID
    ---
    parameters:
      - name: author_id
        in: path
        type: integer
        required: true
        description: ID of the author
    responses:
      200:
        description: Author found
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
      404:
        description: Author not found
      500:
        description: Internal server error
    """
    author = db.session.get(Author, author_id)
    if author is None:
        abort(404, 'Author not found')
    return jsonify({'id': author.id, 'name': author.name}), 200

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book_by_id(book_id):
    """
    Update a book by ID
    ---
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: ID of the book
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: Anna Karenina
            author:
              type: string
              example: Leo Tolstoy
    responses:
      200:
        description: Book updated successfully
      400:
        description: Bad request (no data)
      404:
        description: Book not found
      500:
        description: Internal server error
    """
    data = request.get_json()
    if not data:
        abort(400, description='No data')


    book = db.session.get(Book, book_id)
    if not book:
        abort(404, description='Book not found')

    if 'title' in data:
        book.title = data['title']

    if 'author' in data:
        author_name = data['author']
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()
        book.author_id = author.id

    db.session.commit()

    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author.name
    }), 200

@app.route('/authors/<int:author_id>', methods=['PUT'])
def update_author_by_id(author_id):
    """
    Update an author by ID
    ---
    parameters:
      - name: author_id
        in: path
        type: integer
        required: true
        description: ID of the author
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: Fyodor Dostoevsky
    responses:
      200:
        description: Author updated successfully
      400:
        description: Bad request (no data)
      404:
        description: Author not found
      500:
        description: Internal server error
    """
    data = request.get_json()
    if not data:
        abort(400, description='No data')

    author = db.session.get(Author, author_id)
    if not author:
        abort(404, description='Author not found')

    if 'name' in data:
        author.name = data['name']
    db.session.commit()
    return jsonify({'id': author.id, 'name': author.name}), 200



@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book_by_id(book_id):
    """
    Delete a book by ID
    ---
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: ID of the book
    responses:
      200:
        description: Book deleted successfully
      404:
        description: Book not found
      500:
        description: Internal server error
    """
    book = db.session.get(Book, book_id)
    if not book:
        abort(404, description='Book not found')
    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': f'Book with id {book_id} deleted successfully'}), 200
    except Exception as exc:
        abort(500, description=str(exc))

@app.route('/authors/<int:author_id>', methods=['DELETE'])
def delete_author_by_id(author_id):
    """
    Delete an author by ID
    ---
    parameters:
      - name: author_id
        in: path
        type: integer
        required: true
        description: ID of the author
    responses:
      200:
        description: Author deleted successfully
      404:
        description: Author not found
      500:
        description: Internal server error
    """
    author = db.session.get(Author, author_id)
    if not author:
        abort(404, description='Author not found')
    if author.books:
        abort(400, description='Cannot delete author with existing books')
    try:
        db.session.delete(author)
        db.session.commit()
        return jsonify({'message': f'Author with id {author_id} deleted successfully'}), 200
    except Exception as exc:
        abort(500, description=str(exc))


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "message": str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
