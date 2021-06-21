import { Component, OnInit } from '@angular/core';
import { AuthService } from '../_services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.css']
})
export class LoginPageComponent implements OnInit {

  constructor(private authService: AuthService,
              private router: Router) { }

  ngOnInit(): void {
  }

  login(){
    this.authService.login().subscribe(res => {
      console.log(res);
      if(res.substring(0,5) === 'https'){
        this.routeToCas(res.toString());
      }
      else if(res !== ''){
        this.authService.getUserInfo(res)
        .subscribe(data => {
          this.router.navigate(['/']);
        },
        error => {
          console.log(error);
        });
      }
      else{
        this.router.navigate(['/redirecting']);
      }
    }, 
    error => {
      console.log(error);
    });;
  }


  routeToCas(url: string) {
    window.location.href = url;
  }
}
