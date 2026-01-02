import './styles/tokens.css'
import './styles/main.css'
import { AppBar } from './components/AppBar'
import { FileUpload } from './components/FileUpload'
import { ResultsPanel } from './components/ResultsPanel'
import { ExplanationOverlay } from './components/ExplanationOverlay'

// Define custom elements
customElements.define('app-bar', AppBar);
customElements.define('file-upload', FileUpload);
customElements.define('results-panel', ResultsPanel);
customElements.define('explanation-overlay', ExplanationOverlay);

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <app-bar></app-bar>
  <main class="content">
      <file-upload id="uploader"></file-upload>
      <div id="results-area" class="hidden">
        <results-panel id="results"></results-panel>
        <explanation-overlay id="overlay"></explanation-overlay>
      </div>
  </main>
`

// Simple orchestrator
const uploadElement = document.querySelector('#uploader') as any;
const resultsArea = document.querySelector('#results-area') as HTMLDivElement;
const resultsPanel = document.querySelector('#results') as any;
const overlayPanel = document.querySelector('#overlay') as any;

uploadElement.addEventListener('file-uploaded', (e: CustomEvent) => {
    const data = e.detail; // PredictionResponse
    resultsArea.classList.remove('hidden');
    resultsPanel.data = data;
    overlayPanel.data = {
       originalImage: data.originalImage, // Passed from upload for display
       heatmap: data.explanation.heatmap_base64
    };
});
