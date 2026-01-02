import { LitElement, html, css } from 'lit';
import { property } from 'lit/decorators.js';
import { PredictionResponse } from '../services/api';

export class ResultsPanel extends LitElement {
    static styles = css`
        :host {
            display: block;
            border: 1px solid #eee;
            border-radius: 8px;
            padding: 16px;
            background: white;
            min-width: 300px;
        }
        h2 { margin-top: 0; }
        .row { display: flex; justify-content: space-between; margin-bottom: 8px; }
        .label { font-weight: bold; }
        .val { font-family: monospace; }
        .confidence-bar {
            height: 4px;
            background: #eee;
            margin-top: 4px;
            border-radius: 2px;
        }
        .fill {
            height: 100%;
            background: var(--md-sys-color-primary, #006a6a);
            border-radius: 2px;
        }
    `;

    @property({ type: Object }) data: PredictionResponse | null = null;

    render() {
        if (!this.data) return html``;

        const p = this.data.prediction;
        const u = this.data.uncertainty;

        return html`
            <h2>Prediction</h2>
            <div class="row">
                <span class="label">Class:</span>
                <span>${p.label}</span>
            </div>
            <div class="row">
                <span class="label">Confidence:</span>
                <span class="val">${(p.confidence * 100).toFixed(1)}%</span>
            </div>
            <div class="confidence-bar">
                <div class="fill" style="width: ${p.confidence * 100}%"></div>
            </div>

            <h3>Uncertainty</h3>
            <div class="row">
                <span class="label">Entropy:</span>
                <span class="val">${u.predictive_entropy.toFixed(3)}</span>
            </div>
             <div class="row">
                <span class="label">Calibrated:</span>
                <span class="val">${(u.calibrated_confidence * 100).toFixed(1)}%</span>
            </div>
        `;
    }
}
