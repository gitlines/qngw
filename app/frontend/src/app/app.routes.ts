import {Routes} from '@angular/router';
import {AppComponent} from './app.component';

export const ROUTES: Routes = [
  // routes from pages
  {path: '/home', component: AppComponent, data: {title: 'Home'}},

  // default redirect
  {path: '**', redirectTo: '/'}
];
