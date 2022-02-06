from app.core.models import Book


class TestPostBooks:
    def test_returns_200_and_creates_book_when_payload_is_valid(
            self, client, session
    ):
        payload = {
            "title": "Harry Potter and the Philosopher's Stone",
            "author": "J. K. Rowling"
        }
        response = client.post(
            "/books/",
            json=payload,
        )

        assert response.status_code == 200
        assert session.query(Book).count() == 1

    def test_returns_422_when_book_title_already_exists(
            self, client, session
    ):
        payload = {
            "title": "Harry Potter and the Philosopher's Stone",
            "author": "J. K. Rowling"
        }
        response = client.post("/books/", json=payload)

        assert response.status_code == 200

        response = client.post("/books/", json=payload)
        assert response.status_code == 422
        assert response.json()["detail"] == "A book with title Harry Potter and " \
                                            "the Philosopher's Stone already exists."

    def test_returns_422_when_payload_is_invalid(
            self, client, session
    ):
        payload = {
            "key": "value",
        }
        response = client.post(
            "/books/",
            json=payload,
        )

        assert response.status_code == 422
        assert session.query(Book).count() == 0


class TestGetBooks:
    def test_returns_200_and_books_when_valid(
            self, client, book, session
    ):
        response = client.get(
            "/books/",
        )

        assert response.status_code == 200
        assert session.query(Book).count() == 1
        assert response.json()[0] == {
            "title": "J. K. Rowling",
            "author": "Harry Potter and the Philosopher's Stone",
            "pages": 223,
            "id": 1
        }
