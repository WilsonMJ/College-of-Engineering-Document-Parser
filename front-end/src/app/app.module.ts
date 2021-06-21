import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { MaterialModule } from './material-module';
import { FormsModule} from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { LoginPageComponent } from './login-page/login-page.component';
import { ParsingPageComponent } from './parsing-page/parsing-page.component';
import { AdminPageComponent } from './admin-page/admin-page.component';
import { RedirectingComponent } from './redirecting/redirecting.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginPageComponent,
    ParsingPageComponent,
    AdminPageComponent,
    RedirectingComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MaterialModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
