export interface UserPost {
    email: string,
    username: string,
    city: string,
    password: string,
    user_image: File | null
}

export interface UserGet {
    id: string,
    date_joined: Date,
    is_active: boolean,
    is_staff: boolean,
    is_superuser: boolean,
    last_login: Date,
    user: UserPost
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
