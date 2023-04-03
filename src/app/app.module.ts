import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { NbThemeModule, NbLayoutModule, NbIconModule } from '@nebular/theme';
import { NbAuthModule , NbPasswordAuthStrategy} from '@nebular/auth';
import { NbSecurityModule } from '@nebular/security';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';


const formSetting: any = {
  redirectDelay: 0,
  showMessages: {
    success: true,
  },
};

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NbThemeModule.forRoot({ name: 'default' }),
    NbLayoutModule,
    NbIconModule,
    NbAuthModule.forRoot({
      strategies: [
      NbPasswordAuthStrategy.setup({
        name: 'email',
        baseEndpoint: 'http://127.0.0.1:5000',
              login: {
                redirect: {
                  success: '/dashboard/',
                  failure: null,
                },
                endpoint: '/auth/login',
                method: 'post'
              },
              register: {
                endpoint: '/auth/register',
                method: 'POST',
                redirect: {
                  success: '/auth/login',
                  failure: null,
                }
              },
              logout: {
                endpoint:'/auth/logout',
                method: 'post'
              },
              resetPass: {
                endpoint: '/auth/resetPassword',
                method: 'post'
              },
              requestPass: {
                endpoint:'/auth/requestPass',
                method: 'post'
              },
      }),
    ],
    forms: {
      login: formSetting,
      register: formSetting,
      logout: {
        redirectDelay: 0,
      },
    },
    
  }),
    NbSecurityModule.forRoot(),
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
