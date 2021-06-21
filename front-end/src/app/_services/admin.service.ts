import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { User } from '../_models/user';
import { Role } from '../_models/role';

@Injectable({
    providedIn: 'root'
})
export class AdminService {

    constructor(private http: HttpClient) {}
    
    /**
     * post request to send new document type to backend
     * 
     * @param documentType
     *    newly created document type to send to backend
     */
    addDocumentType(documentType: string, collegeName: string) {
        return this.http.post(`/api/admin/addtype`, {documentType, collegeName}, { responseType: 'text' });      
    }

    /**
     * post request to send new user to backend
     * 
     * @param user
     *    newly created user to send to backend
     */
    addUser(user: User) {
        return this.http.post(`/api/admin/adduser`, user, { responseType: 'text' });      
    }

    /**
     * post request to send new term code to backend
     * 
     * @param termCode
     *    newly created term code  to send to backend
     */
    addTermCode(termCode: string, collegeName: string) {
        return this.http.post(`/api/admin/addterm`, {termCode, collegeName}, { responseType: 'text' });      
    }

    /**
     * post request to change user's role
     * 
     * @param user
     *    user who's role is being changed
     */
     changeUserRole(username: string, role: string) {
        return this.http.post(`/api/admin/changerole`, {params: {user: username, role: role}});      
    }
    
    /**
     * delete request to delete document type from backend
     * 
     * @param documentType
     *    document type to delete from backend
     */
     removeDocumentType(id: string) {
        return this.http.post(`/api/admin/removetype`, {params: {id: id}});      
    }

    /**
     * delete request to delete user from backend
     * 
     * @param user
     *    user to delete from backend
     */
    removeUser(id: string, username: string) {
        return this.http.post(`/api/admin/removeuser`, {params: {id: id, username: username}});      
    }

    /**
     * delete request to send delete term code from backend
     * 
     * @param termCode
     *    term code  to delete from backend
     */
    removeTermCode(id: string) {
        return this.http.post(`/api/admin/removeterm`, {params: {id: id}});      
    }
}