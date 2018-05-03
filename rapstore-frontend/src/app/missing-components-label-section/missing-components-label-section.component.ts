import {Component, OnDestroy, OnInit} from '@angular/core';
import {BrowserIntegrationService} from '../browser-integration.service';
import {Subscription} from 'rxjs/Subscription';

@Component({
  selector: 'app-missing-components-label-section',
  templateUrl: './missing-components-label-section.component.html',
  styleUrls: ['./missing-components-label-section.component.css']
})
export class MissingComponentsLabelSectionComponent implements OnInit, OnDestroy {

  private $subscriptionExtension: Subscription;
  private $subscriptionHost: Subscription;

  protected extensionAvailable = true;
  protected nativeMessagingHostAvailable = true;

  constructor(private browserIntegrationService: BrowserIntegrationService) {
  }

  ngOnInit(): void {

    this.$subscriptionExtension = this.browserIntegrationService.isExtensionAvailable()
      .subscribe(updatedBool => {
        this.extensionAvailable = updatedBool;
      });

    this.$subscriptionHost = this.browserIntegrationService.isNativeMessagingHostAvailable()
      .subscribe(updatedBool => {
        this.nativeMessagingHostAvailable = updatedBool;
      });
  }

  ngOnDestroy(): void {
    this.$subscriptionExtension.unsubscribe();
    this.$subscriptionHost.unsubscribe();
  }

}
