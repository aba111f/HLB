import { HttpInterceptorFn, HttpRequest } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';
import { SharingService } from '../../services/sharing/sharing.service';
import { Inject } from '@angular/core';


export const authInterceptor: HttpInterceptorFn = (req, next) => {
  
  const service = Inject(SharingService);
  const access = service.get_from_storage('access');


  if (req.url.includes('/common/login/') || req.url.includes('common/refresh/')) {
    return next(req);
  }

  return next(access ? addToken(req, access) : req).pipe(
    catchError(error => {
      return throwError(() => error);
    })
  );


  
};

const addToken = (req: HttpRequest<any>, access: string) => {
    return req.clone({
      setHeaders: {
        Authorization: `Bearer ${access}`
      }
    });
  };
