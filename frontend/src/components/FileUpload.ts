import { LitElement, html, css } from 'lit';
import { predict } from '../services/api';

export class FileUpload extends LitElement {
    static styles = css`
        :host {
            display: block;
            border: 2px dashed #ccc;
            border-radius: 8px;
            padding: 32px;
            text-align: center;
            cursor: pointer;
            transition: border-color 0.2s;
        }
        :host(:hover) {
            border-color: var(--md-sys-color-primary, #006a6a);
        }
        input {
            display: none;
        }
        .instruction {
            font-size: 1.1rem;
            margin-bottom: 8px;
        }
        .sub {
            color: #666;
            font-size: 0.9rem;
        }
    `;

    render() {
        return html`
            <div @click=${this.triggerUpload} @dragover=${this.handleDragOver} @drop=${this.handleDrop}>
                <div class="instruction">Drag & Drop Ultrasound Image Here</div>
                <div class="sub">or click to browse (PNG, JPG)</div>
                <input type="file" id="fileInput" accept="image/png, image/jpeg" @change=${this.handleFileSelect} />
            </div>
        `;
    }

    triggerUpload() {
        this.shadowRoot?.querySelector<HTMLInputElement>('#fileInput')?.click();
    }

    handleDragOver(e: DragEvent) {
        e.preventDefault();
    }

    handleDrop(e: DragEvent) {
        e.preventDefault();
        const files = e.dataTransfer?.files;
        if (files && files.length > 0) {
            this.processFile(files[0]);
        }
    }

    handleFileSelect(e: Event) {
        const input = e.target as HTMLInputElement;
        if (input.files && input.files.length > 0) {
            this.processFile(input.files[0]);
        }
    }

    async processFile(file: File) {
        try {
            const result = await predict(file);
            
            // Add local file url for display
            const reader = new FileReader();
            reader.onload = (e) => {
                const fullResult = { ...result, originalImage: e.target?.result as string };
                this.dispatchEvent(new CustomEvent('file-uploaded', { 
                    detail: fullResult,
                    bubbles: true,
                    composed: true
                }));
            };
            reader.readAsDataURL(file);
            
        } catch (err) {
            console.error(err);
            alert("Prediction failed. See console.");
        }
    }
}
