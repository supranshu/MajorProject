import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-learn',
  templateUrl: './learn.component.html',
  styleUrls: ['./learn.component.css'],
  standalone: true, 
  imports: [FormsModule], 
})
export class LearnComponent {
  query: string = '';
  response: string = '';

  constructor(private http: HttpClient) {}

  askDeepfake() {
    if (!this.query.trim()) {
      this.response = "Please enter a question.";
      return;
    }

    // Send as JSON object
    this.http.post<{ response: string }>("http://localhost:8000/ask-deepfake/", { question: this.query })
      .subscribe({
        next: (res) => this.response = res.response,
        error: () => this.response = "Error fetching response. Try again later."
      });
  }
}
