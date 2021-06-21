import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../_services/auth.service';
import { AdminService } from '../_services/admin.service';
import { NotificationService } from '../_services/notification.service';
import { User } from '../_models/user';
import { Role } from '../_models/role';
import { DocumentType } from '../_models/documentType';
import { TermCode} from '../_models/termCode';

@Component({
  selector: 'app-admin-page',
  templateUrl: './admin-page.component.html',
  styleUrls: ['./admin-page.component.css']
})
export class AdminPageComponent implements OnInit {
  currentUser: User;
  public Role = Role;
  documentTypes: DocumentType[];
  users: User[];
  termCodes: TermCode[];
  validUser: Boolean = false;
  validDocType: any;
  validTermCode: any;
  validUserName: any;
  roles = ["admin", "standard"];

  constructor(private router: Router,
              private authService: AuthService,
              private adminService: AdminService,
              private notifService: NotificationService) { 
    // get current user
    this.authService.currentUser.subscribe(x => {
      this.currentUser = x;
        console.log(this.currentUser.roleString);
        if(this.currentUser.documentTypes){
          this.documentTypes = this.currentUser.documentTypes.sort((n1,n2) => {
            if (n1.documentType.toLowerCase() > n2.documentType.toLowerCase()) {
                return 1;
            }
            if (n1.documentType.toLowerCase() < n2.documentType.toLowerCase()) {
                return -1;
            }
            return 0;
          });
        }
        if(this.currentUser.termCodes){
          this.termCodes = this.currentUser.termCodes.sort((n1,n2) => {
            if (n1.termCode > n2.termCode) {
                return 1;
            }
            if (n1.termCode < n2.termCode) {
                return -1;
            }
            return 0;
          });
        }

        if(this.currentUser.userList){
          this.users = this.currentUser.userList.sort((n1,n2) => {
            if (n1.username.toLowerCase() > n2.username.toLowerCase()) {
                return 1;
            }
            if (n1.username.toLowerCase() < n2.username.toLowerCase()) {
                return -1;
            }
            return 0;
          });
        }
    });

    if(this.currentUser.username){
      this.authService.getUserInfo(this.currentUser.username)
        .subscribe(user => {
          if(!user.username){
            this.authService.logout();
            this.router.navigate(['/login']);
          }
        },
        error => {  
          console.log(error);
          this.notifService.showNotif(error, 'error');
          this.router.navigate(['/login']);
        });
    }
  }
  
  ngOnInit(): void { }

  /**
   * reloads current user to match data in the database
   * this function will be called after any add/remove/change of document types, term codes, and users
   */
  private loadUser() {
    this.authService.getUserInfo(this.currentUser.username).subscribe(data => {
      this.authService.currentUser.subscribe(x => {
        this.currentUser = x;
        this.documentTypes = this.currentUser.documentTypes.sort((n1,n2) => {
          if (n1.documentType > n2.documentType) {
              return 1;
          }
          if (n1.documentType < n2.documentType) {
              return -1;
          }
          return 0;
        });
        this.termCodes = this.currentUser.termCodes.sort((n1,n2) => {
          if (n1.termCode > n2.termCode) {
              return 1;
          }
          if (n1.termCode < n2.termCode) {
              return -1;
          }
          return 0;
        });
        this.users = this.currentUser.userList.sort((n1,n2) => {
          if (n1.username > n2.username) {
              return 1;
          }
          if (n1.username < n2.username) {
              return -1;
          }
          return 0;
        });
      });
    },
    error => {
      console.log(error);
    });;
    
  }

  /**
   * routes user back to parsing page
   */
  routeToParsePage(): void {
    this.router.navigate(['/'])
    .then(() => {
      //might need to change this
      window.location.reload();
    });
  }

  /**
   * Add a new doc type
   * @param value Name of doc type
   */
  addDocType(value: any): void {
    
    this.adminService.addDocumentType(value, this.currentUser.college).subscribe(
      res =>{
        const documentType = {documentType: value, id: res};
        this.documentTypes.push(documentType);
        this.loadUser();
        this.notifService.showNotif("Document Type added", 'OK');
      },
      error => {
        this.notifService.showNotif(error, 'error');
      }
    );
  }

  /**
   * Remove an existing doc type
   * @param index index for removal
   */
  removeDocType(index: number): void {
    const documentType = this.documentTypes[index];
    
    this.adminService.removeDocumentType(documentType.id).subscribe(
      res =>{
        this.documentTypes.splice(index, 1);
        this.loadUser();
        this.notifService.showNotif("Document Type removed", 'OK');
      },
      error => {
        this.notifService.showNotif(error, 'error');
      }
    );
  }

  /**
   * Add a new term code
   * @param value string of term code
   */
  addTermCode(value: string): void {
    
    this.adminService.addTermCode(value, this.currentUser.college).subscribe(
      res =>{
        const termCode = {termCode: value, id: res};
        this.termCodes.push(termCode);
        this.loadUser();
        this.notifService.showNotif("Term code added", 'OK');
      },
      error => {
        this.notifService.showNotif(error, 'error');
      }
    );
  }

  /**
   * Remove an existing term code
   * @param index index for removal
   */
  removeTermCode(index: number): void {
    const termCode = this.termCodes[index];
    
    this.adminService.removeTermCode(termCode.id).subscribe(
      res =>{
        this.termCodes.splice(index, 1);
        this.loadUser();
        this.notifService.showNotif("Term code removed", 'OK');
      },
      error => {
        this.notifService.showNotif(error, 'error');
      }
    );
  }

  /**
   * enables button once user type is selected
   */
  selected(): void {
    this.validUser = true;
  }

  /**
   * Adds a user to the users list
   * @param name user name
   * @param role role
   */
  addUser(name: string, role: Role) {
    let user = new User();
    user.username = name;
    user.role = role;
    user.college = this.currentUser.college;
    this.adminService.addUser(user).subscribe(
      res =>{
        this.users.push(user);
        this.loadUser();
        this.notifService.showNotif("New user added", 'OK');
      },
      error => {
        this.notifService.showNotif(error, 'error');
      }
    );
  }

  /**
   * Removes user from the list
   * @param index index of the user in the list
   */
  removeUser(index: number) {
    const user = this.users[index];
    
    this.adminService.removeUser(user.id, user.username).subscribe(
      res =>{
        this.users.splice(index, 1);
        this.loadUser();
        this.notifService.showNotif("User was removed", 'OK');
      },
      error => {
        this.notifService.showNotif(error, 'error');
      }
    );
  }

  /**
   * changes users role
   * @param user user who role is being changed
   * @param role new role of the user
   */
  changeRole(username: string, role: string) {
    
    this.adminService.changeUserRole(username, role).subscribe(
      res =>{
        this.users = null;
        this.loadUser();
        this.notifService.showNotif(`User role was changed to ${role}`, 'OK');
      },
      error => {
        this.notifService.showNotif(error, 'error');
      }
    );
    console.log(this.users);
  }
}
