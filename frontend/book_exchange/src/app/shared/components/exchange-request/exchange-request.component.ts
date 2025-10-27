import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ExchangeRequestService } from '../../../core/services/exchange_request/exchange-request.service';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  imports: [ReactiveFormsModule, CommonModule],
  selector: 'app-exchange-request',
  templateUrl: './exchange-request.component.html',
  styleUrls: ['./exchange-request.component.css']
})
export class ExchangeRequestComponent {
  exchangeForm: FormGroup;
  successMessage = '';
  errorMessage = '';
  exchangeRequests: any[] = [];

  constructor(
    private fb: FormBuilder,
    private exchangeService: ExchangeRequestService
  ) {
    this.exchangeForm = this.fb.group({
      to_email: ['', [Validators.required, Validators.email]],
      requested_book_id: ['', Validators.required],
      offered_book_id: [''],
      exchange_type: [''],
      message: ['']
    });
  }

  ngOnInit() {
    this.loadRequests();
  }

  loadRequests() {
    this.exchangeService.getExchangeRequests().subscribe({
      next: data => this.exchangeRequests = data,
      error: err => console.error(err)
    });
  }

  onSubmit() {
    if (this.exchangeForm.invalid) return;

    const userEmail = localStorage.getItem('email');
    const requestData = {
      from_email: userEmail,
      ...this.exchangeForm.value
    };

    this.exchangeService.createExchangeRequest(requestData).subscribe({
      next: (res) => {
        this.successMessage = 'Exchange request sent successfully!';
        this.errorMessage = '';
        this.exchangeForm.reset();
        this.loadRequests();
      },
      error: (err) => {
        this.successMessage = '';
        this.errorMessage = err.error?.error || 'Failed to send exchange request.';
      }
    });
  }
}
