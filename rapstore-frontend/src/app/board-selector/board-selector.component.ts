import {Component, Input, OnInit} from '@angular/core';
import {Board} from '../models';
import {ActivatedRoute} from '@angular/router';
import {BoardService} from '../board.service';

@Component({
  selector: 'app-board-selector',
  templateUrl: './board-selector.component.html',
  styleUrls: ['./board-selector.component.css']
})

export class BoardSelectorComponent implements OnInit {
  @Input() boards: Board[];
  constructor(private BoardService: BoardService, private route: ActivatedRoute) { }

  ngOnInit() {
    const id = +this.route.snapshot.paramMap.get('id');
    this.BoardService.getAll()
      .subscribe(boards => this.boards = boards);
  }

}
