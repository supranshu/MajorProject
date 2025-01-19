import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HomeComponent } from './pages/home/home.component';
import { UploadComponent } from './pages/upload/upload.component';
import { HttpClientModule } from '@angular/common/http';
import { LearnComponent } from './pages/learn/learn.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    UploadComponent,
  
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    BrowserAnimationsModule,
    ReactiveFormsModule,
    HttpClientModule,
    LearnComponent 
  ],
  providers: [
    provideClientHydration(), provideAnimationsAsync()
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
