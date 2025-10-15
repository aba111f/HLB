export interface UserPost {
    email: string,
    username: string,
    city: string,
    password: string,
    user_image: File | null
}

export interface UserGet {
    id: string,
    date_joined: Date | null,
    // is_active: boolean | null,
    // last_login: Date | null,
    user: UserPost
}

export interface UserData {
    id: string,
    email: string,
    password: string,
    date_joined: Date | null,
    username: string,
    user_image: File | null,
    city: string
}


