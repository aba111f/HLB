import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Book } from '../../interface/book-user';
import { BookService } from '../../../core/services/book/book.service';
@Component({
  selector: 'app-profile-books',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './profile-books.component.html',
  styleUrls: ['./profile-books.component.css']
})
export class ProfileBooksComponent implements OnInit{
  books: Book[] = [];
  book: Book = {
    title: '',
    author: '',
    genre: '',
    description: '',
    condition: '',
    availability: '',
    book_image: null
  };

  constructor(private book_service: BookService){}

  ngOnInit(): void {
    this.get_books();
  }

  get_books(){
    this.book_service.get_books().subscribe({
      next: (res) => {
        this.books = res;
        
        console.log(this.books + ' success');
      },
      error: (err) => {
        console.log('Error in getting books' + err);
      } 
    });
  }

  previewUrl: string | ArrayBuffer | null = null;

  onFileSelected(event: Event): void {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file) return;

    this.book.book_image = file;

    const reader = new FileReader();
    reader.onload = () => {
      this.previewUrl = reader.result;
    };
    reader.readAsDataURL(file);
  }

  onsubmit(){
    console.log('proceeding');
    this.book_service.create_book(this.book).subscribe({
      next: (res) => {
        console.log(res + ' success');
      },
      error: (err) => {
        console.log('Error in create book '+err);
      }
    });
  }
}
