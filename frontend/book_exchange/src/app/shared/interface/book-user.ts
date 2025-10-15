import { UserGet } from "./interface";


export interface BookUser {
  username: string;
  city: string;
  book_title: string;
  genre: string;
  exchange_type: string;
  user_image?: File | null;
}

export interface Book{
    id: string,
    owner: UserGet,
    title: string,
    author: string,
    genre: string,
    description: string,
    condition: string,
    availability: string,
    created_at: Date,
    book_image: File | null
}