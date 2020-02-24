import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Rx'
import  { HttpClient } from '@angular/common/http'
import { map, catchError } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class PortfolioAnalyticsService {

  constructor(private http: HttpClient) {}

  public getPortfolioData(BasketDetails:{}): Observable<any> {
    let portfolioAPI = 'https://c1h9ea61fi.execute-api.eu-west-1.amazonaws.com/1st';
    var results = this.http.post(portfolioAPI,BasketDetails)
  return results;
}

private handleError(error:Response){
  return Observable.throw(error.status)
}

}
