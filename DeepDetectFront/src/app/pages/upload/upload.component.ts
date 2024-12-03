import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent {
  selectedFile: File | null = null;
  responseMessage: string | null = null;

  constructor(private http: HttpClient) {}

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      this.selectedFile = input.files[0];
      this.responseMessage = null; // Clear previous message
    }
  }

  uploadFile(): void {
    if (!this.selectedFile) {
      this.responseMessage = "Please select a file first.";
      return;
    }

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    const url = this.selectedFile.type.startsWith('image/')
      ? 'http://127.0.0.1:8000/upload-image/'
      : 'http://127.0.0.1:8000/upload-video/';

    this.http.post(url, formData).subscribe({
      next: (response: any) => {
        this.responseMessage = `File uploaded successfully: ${response.filename}`;
      },
      error: (error) => {
        console.error('Upload error:', error);
        this.responseMessage = 'Failed to upload the file.';
      }
    });
  }
}
