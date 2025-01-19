import { Component, OnInit, HostListener } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
  standalone: false
})
export class HomeComponent implements OnInit {
  isMenuOpen = false;
  isNavbarTransparent = true;

  ngOnInit(): void {
    // Initialize component
  }

  // Toggle menu for mobile
  toggleMenu(): void {
    this.isMenuOpen = !this.isMenuOpen;
  }

  // Close menu
  closeMenu(): void {
    this.isMenuOpen = false;
  }

  // Handle scroll events for navbar transparency
  @HostListener('window:scroll', ['$event'])
  onWindowScroll() {
    const scrollPosition = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;
    this.isNavbarTransparent = scrollPosition < 50;
  }
}