import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ParseResponse } from '../_models/parseResponse';

@Injectable({
  providedIn: 'root'
})
export class FileService {

  constructor(private http: HttpClient) {}

  /**
   * post request to send file to the parser's backend
   * 
   * @param fileToUpload 
   *    file to upload to backend server
   */
  postFile(fileToUpload: File, documentType: string, termCode: string) {
    // TODO: need to setup post request and test it with POST MAN
    const endpoint = '/api/file/upload';
    const formData: FormData = new FormData();
    formData.append('fileKey', fileToUpload, fileToUpload.name);
    const options = {params: {documentType: documentType, termCode: termCode}}
    console.log(documentType)
    console.log(termCode)
    return this.http.post<ParseResponse>(endpoint, formData, options);      
  }

  getErrorDocsZip(filePath: string){
    return this.http.post('/api/file/download', {params: {file_path: filePath}}, {responseType: 'blob'});
  }
}
