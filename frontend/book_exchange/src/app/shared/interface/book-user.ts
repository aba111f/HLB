import { UserGet } from "./interface";


export interface BookUser {
  username?: string;
  email?: string;
  city?: string;
  title: string;
  genre: string;
  exchange_type?: string;
  user_image?: File | null;
  created_at?: Date;
  description?: string;
  book_image?: File | null;
  condition?: string;
  availability?: string;
  author: string;

}
export interface Result {
  results: BookUser[];
}

export interface Book{
    id?: string,
    owner?: UserGet,
    title: string,
    author: string,
    genre: string,
    description: string,
    condition: string,
    availability: string,
    created_at?: Date,
    book_image: File | null
}