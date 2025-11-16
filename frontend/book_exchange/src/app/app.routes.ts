import { Routes } from '@angular/router';
import { ProfileComponent } from './shared/components/profile/profile.component';
import { HomepageComponent } from './shared/components/homepage/homepage.component';
import { RegisterComponent } from './shared/components/register/register.component';
import { LoginComponent } from './shared/components/login/login.component';
import { UserSearchComponent } from './shared/components/user-search/user-search.component';
import { ProfileBooksComponent } from './shared/components/profile-books/profile-books.component';
import { ExchangeRequestComponent } from './shared/components/exchange-request/exchange-request.component';

export const routes: Routes = [
    {
        path:'',
        component: HomepageComponent
    },
    {
        path: 'profile',
        component: ProfileComponent
    },
    // {
    //     path:'books', 
    //     component: ProfileBooksComponent 
    // },
    {
        path:'register',
        component: RegisterComponent
    },
    {
        path:'login',
        component: LoginComponent
    },
    {
        path:'user-search', 
        component: UserSearchComponent 
    },
    
    {
        path:'exchange-requests',
        component: ExchangeRequestComponent
    }

];
