import { Component, ElementRef, ViewChild, HostListener } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

interface ChatMessage {
  text: string;
  type: 'user' | 'bot';
}

@Component({
  selector: 'app-learn',
  templateUrl: './learn.component.html',
  styleUrls: ['./learn.component.css'],
  standalone: true,
  imports: [FormsModule, CommonModule],
})
export class LearnComponent {
  // Chat properties
  query: string = '';
  messages: ChatMessage[] = [];
  isLoading: boolean = false;

  // Navigation properties
  isMenuOpen: boolean = false;
  isNavbarTransparent: boolean = true;

  @ViewChild('chatMessages') chatMessages!: ElementRef;

  constructor(private http: HttpClient) {}

  // Chat methods
  async askDeepfake() {
    const trimmedQuery = this.query.trim();
    if (!trimmedQuery || this.isLoading) return;

    this.isLoading = true;
    this.messages.push({ text: trimmedQuery, type: 'user' });
    this.query = '';
    this.scrollToBottom();

    try {
      const response = await this.http
        .post<{ response: string }>('http://localhost:8000/ask-deepfake/', {
          question: trimmedQuery
        })
        .toPromise();

      if (response?.response) {
        this.messages.push({ text: response.response, type: 'bot' });
      }
    } catch (error) {
      this.messages.push({
        text: 'Sorry, I encountered an error. Please try again later.',
        type: 'bot'
      });
    } finally {
      this.isLoading = false;
      this.scrollToBottom();
    }
  }

  private scrollToBottom(): void {
    setTimeout(() => {
      const element = this.chatMessages.nativeElement;
      element.scrollTop = element.scrollHeight;
    }, 100);
  }

  // Navigation methods
  toggleMenu(): void {
    this.isMenuOpen = !this.isMenuOpen;
  }

  closeMenu(): void {
    this.isMenuOpen = false;
  }

  @HostListener('window:scroll', ['$event'])
  onWindowScroll() {
    const scrollPosition = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;
    this.isNavbarTransparent = scrollPosition < 50;
  }
}