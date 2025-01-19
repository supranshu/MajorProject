import { NgModule } from '@angular/core';
import { ServerModule } from '@angular/platform-server';

import { AppModule } from './app.module';
import { AppComponent } from './app.component';
import { LearnComponent } from './pages/learn/learn.component';


@NgModule({
  imports: [
    AppModule,
    ServerModule,
    LearnComponent
  ],
  bootstrap: [AppComponent],
})
export class AppServerModule {}
