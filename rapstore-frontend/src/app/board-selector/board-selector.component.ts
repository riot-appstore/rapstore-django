import {Component, Input, OnInit, Output, EventEmitter} from '@angular/core';
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
  @Input() selectedBoard: Board;
  @Output() notify: EventEmitter<Board> = new EventEmitter<Board>();

  constructor(private boardService: BoardService, private route: ActivatedRoute) {
  }

  ngOnInit() {
    const id = +this.route.snapshot.paramMap.get('id');
    this.boardService.getSupported(id)
      .subscribe(boards => {
        this.boards = boards;
        this.selectedBoard = boards[0];
        this.onChange();
      });
  }

  onChange() {
    this.notify.emit(this.selectedBoard);
  }

}
