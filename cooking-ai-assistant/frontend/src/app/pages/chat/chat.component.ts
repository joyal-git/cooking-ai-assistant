import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../api.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.scss'
})
export class ChatComponent {

  pantry = ''; diet = ''; message = ''; log: string[] = [];

  constructor(private api: ApiService) {}

  send() {
    const payload = {
      message: this.message.trim(),
      pantry: this.pantry.split(',').map(x => x.trim()).filter(Boolean),
      diet: this.diet || null
    };
    if (!payload.message) return;
    this.log.push('You: ' + payload.message);
    this.api.chat(payload).subscribe({ next: (d:any) => {
      this.log.push('Assistant: ' + d.reply);
      this.message = '';
    }});
  }

}
