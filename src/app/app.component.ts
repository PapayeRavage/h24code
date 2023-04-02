import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'h24code';
constructor(private http: HttpClient){}
  name:any;
  file:any;
  base_url ="http://127.0.0.1:5000"

  getName(name:string){
    this.name =name
  }
  getFile(event:any){
    this.file = event.target.files[0];
    console.log('file', this.file)
  }

  submitData(){
    let formData:FormData = new FormData();
    formData.append('file', this.file, this.file.name);
    console.log(formData);
    this.http.post(this.base_url+'/upload', formData).subscribe(response => {
    console.log(response);
  })

}
}
