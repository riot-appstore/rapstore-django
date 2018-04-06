import {Injectable} from '@angular/core';
import {Observable} from 'rxjs/Observable';
import {Subject} from 'rxjs/Subject';

@Injectable()
export class BrowserIntegrationService {

  private $subjectExtension = new Subject<boolean>();
  private $subjectHost = new Subject<boolean>();

  constructor() {}

  public isExtensionAvailable(): Observable<boolean> {

    setTimeout(() => this.checkBrowserIntegration, 500);

    setTimeout(() => {
      this.checkBrowserIntegration();
    }, 1000);

    return this.$subjectExtension.asObservable();
  }

  public isNativeMessagingHostAvailable(): Observable<boolean> {

    setTimeout(() => {
      this.checkBrowserIntegration();
    }, 1000);

    return this.$subjectHost.asObservable();
  }

  private checkBrowserIntegration(): void {

    this.$subjectExtension.next(document.body.classList.contains('rapstore_extension_installed'));
    this.$subjectHost.next(document.body.classList.contains('rapstore_native_messaging_host_installed'));
  }

}
