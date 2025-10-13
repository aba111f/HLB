import { HttpInterceptorFn, HttpRequest } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const access = localStorage.getItem('access');


  if (req.url.includes('/api/login/') || req.url.includes('api/refresh/')) {
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
