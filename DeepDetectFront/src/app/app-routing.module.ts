import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { UploadComponent } from './pages/upload/upload.component';
import { LearnComponent } from './pages/learn/learn.component';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
    pathMatch: 'full'
  },
  {
    path: 'upload',
    component: UploadComponent,
    pathMatch: 'full'
  },
  {
    path:'learn',
    component:LearnComponent,
    pathMatch:'full'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
