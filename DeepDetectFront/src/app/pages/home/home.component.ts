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
  }

 
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