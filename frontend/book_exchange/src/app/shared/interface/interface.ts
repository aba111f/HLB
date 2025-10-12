export interface User {
    id: string,
    email: string,
    username: string,
    date_joined: Date,
    city: string,
    is_active: boolean,
    is_staff: boolean,
    is_superuser: boolean,
    password: string,
    last_login: Date
}


export interface Book{
    id: string,
    owner: User,
    title: string,
    author: string,
    genre: string,
    description: string,
    conditino: string,
    availability: string,
    created_at: Date
}
