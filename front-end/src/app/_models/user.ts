import { Role } from './role';
import { DocumentType } from '../_models/documentType';
import { TermCode } from '../_models/termCode';

export class User {
    username: string;
    id: string;
    role: Role;
    roleString: string;
    college: string;
    documentTypes: DocumentType[];
    userList: User[];
    termCodes: TermCode[];
}
