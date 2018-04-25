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
  @Output() notify: EventEmitter<number> = new EventEmitter<number>();
  constructor(private boardService: BoardService, private route: ActivatedRoute) { }

  ngOnInit() {
    const id = +this.route.snapshot.paramMap.get('id');
    this.boardService.getAll()
    .subscribe(boards => {this.boards = boards; this.notify.emit(boards[0].id)});
  }
  onChange(value) {
    this.notify.emit(value);
  }

}
