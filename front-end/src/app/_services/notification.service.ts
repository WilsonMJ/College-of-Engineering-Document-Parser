import {Injectable, NgZone} from '@angular/core';
import {MatSnackBar} from '@angular/material/snack-bar';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {

  constructor(public snackBar: MatSnackBar,
              private zone: NgZone) {}
  
  /**
   * function to show snackbar or notification
   * 
   * @param message message to display 
   * @param action button name
   * @param duration how long to display notification
   */
  public showNotif(message, action = 'error', duration = 4000): void {
    this.snackBar.open(message, action, { duration }).onAction().subscribe(() => {
      console.log('Notififcation action performed');
    });
  }

  /**
   * development method to pop a notification informing the user that a feature is not yet implemented
   * 
   * @param message name of function or feature that is not implemented
   * @param duration how long to display notification
   */
  public notImplementedWarning(message, duration = 4000): void {
    this.snackBar.open(`"${message}" is not implemented`, 'error', { duration }).onAction().subscribe(() => {
    });
  }
}

