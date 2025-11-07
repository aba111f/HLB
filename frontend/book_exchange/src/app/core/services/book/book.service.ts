import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Book, BookUser, Result } from '../../../shared/interface/book-user';

@Injectable({
  providedIn: 'root'
})
export class BookService {

  private apiUrl = 'http://localhost:8000/books/';

  constructor(private http: HttpClient) { }

  get_books(): Observable<Book[]>{
    return this.http.get<Book[]>(this.apiUrl + 'get_book_by_user/');
  }

  create_book(book: Book){
    const formData = new FormData();
    formData.append('title', book.title);
    formData.append('author', book.author);
    formData.append('genre', book.genre);
    formData.append('description', book.description);
    if(book.book_image){
      formData.append('book_image', book.book_image);
    }
    formData.append('condition', book.condition);
    formData.append('availability', book.availability);

    return this.http.post(this.apiUrl, formData);
  }
}
