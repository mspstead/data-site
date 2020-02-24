import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Rx'
import  { HttpClient } from '@angular/common/http'
import { map, catchError } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class PortfolioAnalyticsService {

  constructor(private http: HttpClient) {}

  public getPortfolioData(BasketDetails:{}) {
    let portfolioAPI = 'https://c1h9ea61fi.execute-api.eu-west-1.amazonaws.com/1st';
    console.log(portfolioAPI)
    console.log(BasketDetails)
    var results = this.http.post(portfolioAPI,BasketDetails).pipe(
      map((response: Response) => {
        return response.json();
      }), catchError( error => {
        return 'Something went wrong!';
      })
   )
   console.log(results)
  return results;
}

private handleError(error:Response){
  return Observable.throw(error.status)
}

}
