import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-fitbit-data',
  templateUrl: './fitbit-data.component.html',
  styleUrls: ['./fitbit-data.component.css']
})
export class FitbitDataComponent implements OnInit {

  columnDefs = []
  rowData = []

  constructor() { }

  ngOnInit(): void {

    this.columnDefs = [
      {headerName: 'Make', field: 'make' },
      {headerName: 'Model', field: 'model' },
      {headerName: 'Price', field: 'price'}
    ];

    this.rowData = [
      { make: 'Toyota', model: 'Celica', price: 35000 },
      { make: 'Ford', model: 'Mondeo', price: 32000 },
      { make: 'Porsche', model: 'Boxter', price: 72000 }
    ];

  }

}
