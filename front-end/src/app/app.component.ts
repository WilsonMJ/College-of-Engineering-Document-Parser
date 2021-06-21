import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './_services/auth.service';
//import {NotificationService} from './_services/notification.service';
import {User} from './_models/user';
import {Role} from './_models/role';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'front-end';
 
  constructor(private router: Router,
              private authService: AuthService) {}

  
}
