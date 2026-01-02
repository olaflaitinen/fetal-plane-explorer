import { LitElement, html, css } from 'lit';
import { property, state } from 'lit/decorators.js';

export class ExplanationOverlay extends LitElement {
    static styles = css`
        :host {
            display: block;
            position: relative;
            max-width: 100%;
            max-height: 500px;
            overflow: hidden;
            border-radius: 8px;
        }
        .container {
            position: relative;
            display: inline-block;
        }
        img {
            display: block;
            max-width: 100%;
            height: auto;
        }
        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            mix-blend-mode: multiply; 
            /* Simple blend for dummy heatmap checks, real GradCAM usually uses distinct colormaps */
            pointer-events: none;
        }
        .controls {
            margin-top: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
    `;

    @property({ type: Object }) data: { originalImage: string, heatmap?: string } | null = null;
    @state() opacity = 0.5;

    render() {
        if (!this.data) return html``;

        return html`
            <div class="container">
                <img src="${this.data.originalImage}" alt="Original" />
                ${this.data.heatmap ? html`
                    <img class="overlay" 
                         src="data:image/png;base64,${this.data.heatmap}" 
                         style="opacity: ${this.opacity}" />
                ` : ''}
            </div>
            <div class="controls">
                <label>Overlay Opacity</label>
                <input type="range" min="0" max="1" step="0.1" 
                       .value=${this.opacity} 
                       @input=${(e: any) => this.opacity = e.target.value} />
            </div>
        `;
    }
}
