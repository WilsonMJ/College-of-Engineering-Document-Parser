import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject,  Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { User } from '../_models/user';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';

@Injectable({ providedIn: 'root' })
export class AuthService {

  private currentUserSubject: BehaviorSubject<User>;
  public currentUser: Observable<User>;
  ticket: string;
  next: string;
  
  //might need to reload if doc type is added
  constructor(private http: HttpClient,
              private router: Router,
              private route: ActivatedRoute) {
    this.currentUserSubject = new BehaviorSubject<User>(JSON.parse(localStorage.getItem('currentUser')));
    // this is used by app.component.ts
    this.currentUser = this.currentUserSubject.asObservable();
  }

  public get currentUserValue(): User {
    return this.currentUserSubject.value;
  }

  /**
   * login function sends post request with return url to navigate user to
   */
  login() {
    //this is the return url to validate the user after CAS login
    return this.http.get(`/api/login`, { responseType: 'text' });
  }

  /**
   * function to verify that user is authorized to use app
   * to be called after CAS login
   * 
   * @returns string containing url if unauthorized, username of user if authorized
   */
  getUser() {
    this.route.queryParams.subscribe(params => {
      this.ticket = params['ticket'];
      this.next = params['next'];
    });
    console.log(this.ticket);
    return this.http.get(`/api/login`, {params: { ticket: this.ticket, next: this.next } ,  responseType: 'text' })
  }

  /**
   * gets current user and sets current user to user info returned from post request
   * 
   * @pre must a valid user in the database
   * @param username username of the user who's info to fetch
   * @returns returns user object with all info associated with user
   */
  getUserInfo(username: string){
    return this.http.get<User>(`/api/getuser`, {params: {username : username}, responseType: 'json'}).pipe(map(user => {
      if (user) {
          localStorage.setItem('currentUser', JSON.stringify(user));
          this.currentUserSubject.next(user);
      }else{
        localStorage.removeItem('currentUser');
        this.currentUserSubject.next(null);
      }
      
      return user;
    }));
  }

  /**
   * logs user out from current session, removes user from local storage
   * 
   * @returns returns url to finalize logout with CAS
   */
  logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('currentUser');
    this.currentUserSubject.next(null);
    //TODO - need to send something for the backend to remove session at some point
    return this.http.get(`/api/logout`, { responseType: 'text' });
  }
}
