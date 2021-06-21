import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './_guards/auth.guard';
import { Role } from './_models/role';
import { LoginPageComponent } from './login-page/login-page.component';
import { ParsingPageComponent } from './parsing-page/parsing-page.component';
import { AdminPageComponent } from './admin-page/admin-page.component';
import { RedirectingComponent } from './redirecting/redirecting.component';

// const routes: Routes = [
//   //TODO: add auth guard to protected routes
//   {path: '', component: ParsingPageComponent},
//   {path: 'login', component: LoginPageComponent},
//   {path: 'admin-controls', component: AdminPageComponent},
//   {path: 'redirecting', component: RedirectingComponent}];

const routes: Routes = [
  //TODO: add auth guard to protected routes
  {path: '', component: ParsingPageComponent, canActivate: [AuthGuard], data: { roles: [Role.admin, Role.standard] }},
  {path: 'login', component: LoginPageComponent},
  {path: 'admin-controls', component: AdminPageComponent, canActivate: [AuthGuard], data: { roles: [Role.admin] }},
  {path: 'redirecting', component: RedirectingComponent},
  { path: '**', redirectTo: '' }];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
