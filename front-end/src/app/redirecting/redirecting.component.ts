import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../_services/auth.service';
import { NotificationService } from '../_services/notification.service';

@Component({
  selector: 'app-redirecting',
  templateUrl: './redirecting.component.html',
  styleUrls: ['./redirecting.component.css']
})
export class RedirectingComponent implements OnInit {

  validUser: Boolean = false; //boolean to determine valid user
  loadedUser: Boolean = false;  //boolean to determine loaded user

  constructor(private authService: AuthService,
              private router: Router,
              private notifService: NotificationService) { 
                
    //after cas login redirect verify that user can access this site
    this.authService.getUser().subscribe(
      res => {  
        //condition for unauthorized user, display unauthorized message
        //function should return url on unauthorized login
        if(res.toString().substring(0,5) === 'https'){
          this.loadedUser = true;
        }
        else if(res !== ''){  //ensure that response is not empty
          this.loadedUser = true;
          this.validUser = true;

          //if user is valid call backend to retreive user info
          this.authService.getUserInfo(res)
          .subscribe(data => {
            //reroute to parse homepage on success
            this.router.navigate(['/']);
          },
          error => {  //error case for user get info call
            this.loadedUser = true;
            console.log(error);
            this.notifService.showNotif(error, 'error');
          });
        }
        else{
          this.loadedUser = true;
        }
      },
      error => { //error case for get user call
        this.loadedUser = true;
        console.log(error);
        this.notifService.showNotif(error, 'error');
      }
    );
  }

  ngOnInit(): void {}
}
