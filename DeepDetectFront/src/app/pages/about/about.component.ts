import { Component, HostListener } from '@angular/core';

@Component({
  selector: 'app-about',
  standalone: false,
  
  templateUrl: './about.component.html',
  styleUrl: './about.component.css'
})
export class AboutComponent {

  isMenuOpen = false;
    isNavbarTransparent = true;
  
    
  
   
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



    team = [
      {
          name: "Supranshu Singh",
          role: "Backend & AI Developer",
          description: "Focuses on FastAPI and deepfake detection AI.",
          image: "C:\Users\ss445\OneDrive\Desktop\Major\DeepDetectFront\public\profilepic.jpg"
      },
      {
          name: "Developer 2",
          role: "Frontend Developer",
          description: "Handles UI/UX and Angular integration.",
          image: "assets/images/dev2.jpg"
      },
      {
          name: "Developer 3",
          role: "Full Stack Developer",
          description: "Works on database and API connections.",
          image: "assets/images/dev3.jpg"
      },
      {
          name: "Developer 4",
          role: "Data Scientist",
          description: "Ensures accurate AI training and dataset handling.",
          image: "assets/images/dev4.jpg"
      }
  ];
  

}
