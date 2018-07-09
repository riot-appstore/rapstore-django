import {Component, OnInit} from '@angular/core';
import {FeedbackService} from '../feedback.service';

@Component({
  selector: 'feedback',
  templateUrl: './feedback.component.html',
  styleUrls: ['./feedback.component.css']
})
export class FeedbackComponent implements OnInit {

  private feedback: any = {};

  constructor(private feedbackService: FeedbackService) { }

  ngOnInit() {
  }

  feedbackSubmit() {
    this.feedbackService.sendFeedback(this.feedback).subscribe(
      (val) => {
        this.feedback = {};
        alert('Thank you for your feedback!');
      },
      (err) => alert('There was a problem uploading the feedback. Please try again')
    );
  }

  feedbackCancel() {
    this.feedback = {};
  }

}
