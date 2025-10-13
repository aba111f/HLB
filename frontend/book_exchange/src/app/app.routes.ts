import { Routes } from '@angular/router';
import { ProfileComponent } from './shared/components/profile/profile.component';
import { HomepageComponent } from './shared/components/homepage/homepage.component';

export const routes: Routes = [
    {
        path:'',
        component: HomepageComponent
    },
    {
        path: 'profile',
        component: ProfileComponent
    },

];
