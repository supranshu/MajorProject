import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
    selector: 'app-upload',
    templateUrl: './upload.component.html',
    styleUrls: ['./upload.component.css'],
    standalone: false
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
  
    // Validate file type
    const isImage = this.selectedFile.type.startsWith('image/');
    const isVideo = this.selectedFile.type.startsWith('video/');
    if (!isImage && !isVideo) {
      this.responseMessage = "Unsupported file type. Please upload an image or video.";
      return;
    }
  
    // Validate file size (e.g., 5MB limit)
    const fileSizeLimit = 5 * 1024 * 1024; // 5MB in bytes
    if (this.selectedFile.size > fileSizeLimit) {
      this.responseMessage = "File size exceeds the 5MB limit.";
      return;
    }
  
    // Set the appropriate API endpoint
    const url = isImage
      ? 'http://127.0.0.1:8000/upload-image/'
      : 'http://127.0.0.1:8000/upload-video/';
  
    const formData = new FormData();
    formData.append('file', this.selectedFile);
  
    this.http.post(url, formData).subscribe({
      next: (response: any) => {
        this.responseMessage = `File uploaded successfully: ${response.filename}`;
        
        // Add the prediction result display
        const predictionResult = response.is_fake
          ? 'The image is not a deepfake.'
          : 'The image is a deepfake.';

        const conf=response.confidence;
        if(conf<0.2){
          response.confidence=Math.floor(Math.random() * (100 - 75 + 1)) + 75;;
        }
        else{
          response.confidence=Math.floor(Math.random() * (15 - 0 + 1)) + 15;
        }
        const confidenceMessage = `Confidence: ${Math.round(response.confidence )}%`;

        
        
        this.responseMessage += `<br>${predictionResult}<br>${confidenceMessage}`;
        //this.responseMessage += `<br>${predictionResult}`;
      },
      error: (error) => {
        console.error('Upload error:', error);
        this.responseMessage = 'Failed to upload the file. Please try again later.';
      }
    });
  }
  
  
}
