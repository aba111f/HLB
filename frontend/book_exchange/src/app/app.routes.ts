import { Routes } from '@angular/router';
import { ProfileComponent } from './shared/components/profile/profile.component';
import { AppComponent } from './app.component';

export const routes: Routes = [
    {
        path:'',
        component: AppComponent
    },
    {
        path: 'profile',
        component: ProfileComponent
    },

];
