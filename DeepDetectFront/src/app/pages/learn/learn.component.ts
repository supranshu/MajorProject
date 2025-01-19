import { Component, ElementRef, ViewChild} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common'; 

@Component({
  selector: 'app-learn',
  templateUrl: './learn.component.html',
  styleUrls: ['./learn.component.css'],
  standalone: true,
  imports: [FormsModule, CommonModule], 
})
export class LearnComponent {
  query: string = '';
  messages: { text: string, type: 'user' | 'bot' }[] = [];

  @ViewChild('chatMessages', { static: false }) chatMessages!: ElementRef;

  constructor(private http: HttpClient) {}


  askDeepfake() {
    if (!this.query.trim()) return;

    // Add user message
    this.messages.push({ text: this.query, type: 'user' });

    

    // Send request to backend
    this.http.post<{ response: string }>("http://localhost:8000/ask-deepfake/", { question: this.query })
      .subscribe({
        next: (res) => {
          this.messages.push({ text: res.response, type: 'bot' });
          setTimeout(() => this.scrollToBottom(), 10);
        },
        error: () => {
          this.messages.push({ text: "Error fetching response. Try again later.", type: 'bot' });
          setTimeout(() => this.scrollToBottom(), 10);
        }
      });

    // Clear input field after the request is sent
    this.query = ''; 
  }
  autoScrollEnabled = true;
  scrollToBottom() {
    if (this.chatMessages) {
      this.chatMessages.nativeElement.scrollTop = this.chatMessages.nativeElement.scrollHeight;
    }
  }
  toggleAutoScroll() {
    this.autoScrollEnabled = !this.autoScrollEnabled;
  }
  
}
