import { LitElement, html, css } from 'lit';
import { property } from 'lit/decorators.js';

export class AppBar extends LitElement {
    static styles = css`
        :host {
            display: block;
            background-color: var(--md-sys-color-surface-container, #e0e2ec);
            color: var(--md-sys-color-on-surface, #191c1d);
            padding: 16px 24px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            margin: 0;
            font-size: 1.5rem;
            font-weight: 500;
        }
    `;

    @property({ type: String }) title = "Fetal Plane Explorer";

    render() {
        return html`
            <div class="container">
                <h1>${this.title}</h1>
                <!-- Theme toggle placeholder -->
                <button @click=${this.toggleTheme}>Toggle Theme</button>
            </div>
        `;
    }

    toggleTheme() {
        // Implement theme switching logic
        console.log("Toggle theme");
    }
}
