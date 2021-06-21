import { Component, OnInit } from '@angular/core';
import { FileService } from '../_services/file.service';
import { AuthService } from '../_services/auth.service';
import { NotificationService } from '../_services/notification.service';
import { Router } from '@angular/router';
import { DocumentType } from '../_models/documentType';
import { TermCode } from '../_models/termCode';
import { User } from '../_models/user';
import { Role } from '../_models/role';
import { ParseResponse } from '../_models/parseResponse';

@Component({
  selector: 'app-parsing-page',
  templateUrl: './parsing-page.component.html',
  styleUrls: ['./parsing-page.component.css']
})
export class ParsingPageComponent implements OnInit {
  
  currentUser: User;
  fileToUpload: File = null;
  fileName: string = "";
  validUpload: Boolean = false;
  uploadStarted: Boolean = false;
  documentTypes: DocumentType[];
  termCodes: TermCode[];
  selectedDocumentType: string;
  selectedTermCode: string;
  documentTypeIsSelected: Boolean = false;
  termCodeIsSelected: Boolean = false;
  parsedOutput: string[] = [];

  constructor(private router: Router,
              private fileService: FileService,
              private authService: AuthService,
              private notifService: NotificationService) { 

    //get current user to populate document types and term codes
    this.authService.currentUser.subscribe(x => {
      if(x){
        this.currentUser = x;

        if(x.documentTypes.length){
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

        if(x.termCodes){
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

  //TODO-- Implement this
  get isAdmin() {
    return this.currentUser.role === Role.admin;
  }

  //get method for ensure that current user is populated
  get getUser() { return this.currentUser; }

  /**
   * routes user to admin control page if authorized
   */
  routeToAdminControls(): void {
    this.router.navigate(['/admin-controls']);
  }

  /**
   * upadte the selected value of selectedDocumentType
   */
  selectDocumentTypeHandler (event: any) {
    this.selectedDocumentType = event.value;
    if(this.selectedDocumentType !== ''){
      this.documentTypeIsSelected = true;
    }
    else{
      this.documentTypeIsSelected = false;
    }
  }

  /**
   * upadte the selected value of selectedTermCode
   */
  selectTermCodeHandler (event: any) {
    this.selectedTermCode = event.value;
    if(this.selectedTermCode !== ''){
      this.termCodeIsSelected = true;
    }
    else{
      this.termCodeIsSelected = false;
    }
  }

  /**
   * pre: files input must only contain one file
   * 
   * @param files 
   *    event handler passes files from html input to store selected file in
   *    fileToUpload
   */
  handleFileInput(files: FileList) {
    if(files.length === 1){
      this.fileToUpload = files.item(0);
      this.fileName = this.fileToUpload.name
      this.validUpload = true;
    }
  }

  /**
   * upload file using file.service
   * 
   * sends fileToUpload to file.service post request
   * 
   * return: post request response or error based on post request response
   */
  uploadFile() {
    this.validUpload = false;
    this.uploadStarted = true;
    this.parsedOutput = [];

    this.fileService.postFile(this.fileToUpload, 
    this.selectedDocumentType, 
    this.selectedTermCode).subscribe(
      res => {  //success case
        let response: ParseResponse = res;

        var tempParsedOutput: string[] = [];

        //parse response and create message to display to parse output
        tempParsedOutput.push("Parsing has completed");
        tempParsedOutput.push(`PID's resolved: ${response.num_success}`);
        if(response.successes.length === 0){
          tempParsedOutput.push("None");
        }
        for(var i = 0; i < response.successes.length; i++){
          tempParsedOutput.push(response.successes[i]);
        }

        tempParsedOutput.push(`PID's not resolved: ${response.num_error}`);
        if(response.errors.length === 0){
          tempParsedOutput.push("None");
        }
        for(var i = 0; i < response.errors.length; i++){
          tempParsedOutput.push(response.errors[i]);
        }
        
        this.parsedOutput = tempParsedOutput;
        if(response.file_path){
          this.fileService.getErrorDocsZip(response.file_path).subscribe((data) => {
            this.downloadFile(data, 'application/zip');
          });

        }
        this.validUpload = true;
        this.uploadStarted = false;
      },
      error => { //error case
        this.validUpload = true;
        this.uploadStarted = false;
        //display error message to console
        this.parsedOutput.push(error.error);

        //show notification with error message as well
        this.notifService.showNotif(error.error, 'error');
      }
    );
  }

  /**
   * Helper function to download zip file response from api after parsing.
   * Function will open another window in browser and file should start downloading.
   * 
   * @param data 
   *    data is the response object from the postFile post request call
   * @param type 
   *    type is this case is a zip file 
   */
   downloadFile(data: any, type: string) {
    let blob = new Blob([data], { type: type});
    let url = window.URL.createObjectURL(blob);
    var anchor = document.createElement("a");
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    var currDate = mm + '/' + dd + '/' + yyyy;
    anchor.download = 'erroneous-documents (' + currDate + ')';
    anchor.href = url;
    anchor.click();
  }

  /**
   * logout function calls login procedures in auth service
   * opens logout window from CAS
   */
  logout() {
    this.authService.logout().subscribe(res => {
      window.location.href = res;
    }, 
    error => {
      console.log(error);
    });;
  }
}