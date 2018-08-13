import { Component, OnInit, Input } from '@angular/core';
import { AppAvatarService } from './app-avatar.service';

@Component({
  selector: 'app-avatar',
  templateUrl: './app-avatar.component.html',
  styleUrls: ['./app-avatar.component.css']
})

export class AppAvatarComponent implements OnInit {

  @Input('name') name: string = "Riot App";

  constructor(private avatarService: AppAvatarService) { }

  ngOnInit() {
  }

  getColor(value: string): string {
    return this.avatarService.getRandomColor(value);
  }

  getFirstLetter(): string {
    return this.name.charAt(0);
  }

}
