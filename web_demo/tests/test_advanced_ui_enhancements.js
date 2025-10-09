/**
 * Test suite for advanced UI/UX enhancements
 */

// Mock DOM for testing
const mockDOM = `
  <div class="header"></div>
  <div class="card">
    <div class="card-body">
      <button id="testButton" class="btn-holomesh">Test Button</button>
    </div>
  </div>
  <div id="testContainer"></div>
`;

// Setup mock DOM
document.body.innerHTML = mockDOM;

// Import the UI enhancements module
import { HoloMeshUIEnhancements } from '../static/js/ui_enhancements.js';

describe('HoloMeshUIEnhancements', () => {
  let uiEnhancer;

  beforeEach(() => {
    uiEnhancer = new HoloMeshUIEnhancements();
  });

  describe('AI Recommendations', () => {
    test('should create AI recommendation container', () => {
      uiEnhancer.setupAIRecommendations();
      const recommendationContainer = document.querySelector('.ai-recommendation-container');
      expect(recommendationContainer).toBeTruthy();
      expect(recommendationContainer.querySelector('.ai-recommendation-header')).toBeTruthy();
      expect(recommendationContainer.querySelector('.ai-apply-btn')).toBeTruthy();
    });

    test('should show AI feedback', () => {
      uiEnhancer.showAIRecommendationFeedback('Test message');
      const feedback = document.querySelector('.ai-feedback');
      expect(feedback).toBeTruthy();
      expect(feedback.textContent).toBe('Test message');
    });
  });

  describe('Predictive UI', () => {
    test('should setup predictive UI elements', () => {
      // Create a mock loading element
      const loadingElement = document.createElement('div');
      loadingElement.className = 'loading';
      document.body.appendChild(loadingElement);
      
      uiEnhancer.setupPredictiveUI();
      const predictiveBar = loadingElement.querySelector('.predictive-progress');
      expect(predictiveBar).toBeTruthy();
      expect(predictiveBar.querySelector('.predictive-progress-bar')).toBeTruthy();
      expect(predictiveBar.querySelector('.predictive-text')).toBeTruthy();
    });
  });

  describe('Emotional Design', () => {
    test('should add emotional indicators to cards', () => {
      uiEnhancer.setupEmotionalDesign();
      const emotionIndicator = document.querySelector('.emotion-indicator');
      expect(emotionIndicator).toBeTruthy();
      expect(emotionIndicator.innerHTML).toContain('fa-heart');
    });

    test('should show emotional feedback', () => {
      uiEnhancer.showEmotionalFeedback(100, 200);
      const emotion = document.querySelector('.emotional-feedback');
      expect(emotion).toBeTruthy();
      expect(emotion.style.left).toBe('100px');
      expect(emotion.style.top).toBe('200px');
    });
  });

  describe('Biometric Feedback', () => {
    test('should create biometric indicators', () => {
      uiEnhancer.setupBiometricFeedback();
      const biometricIndicator = document.querySelector('.biometric-indicator');
      expect(biometricIndicator).toBeTruthy();
      expect(biometricIndicator.querySelectorAll('.biometric-item').length).toBe(2);
    });
  });

  describe('Neural Interface', () => {
    test('should create neural interface toggle', () => {
      uiEnhancer.setupNeuralInterface();
      const neuralToggle = document.querySelector('.neural-interface-toggle');
      expect(neuralToggle).toBeTruthy();
      expect(neuralToggle.innerHTML).toContain('fa-brain');
    });

    test('should toggle neural interface', () => {
      uiEnhancer.setupNeuralInterface();
      const neuralToggle = document.querySelector('.neural-interface-toggle');
      
      // Initial state
      expect(document.body.classList.contains('neural-interface-active')).toBeFalsy();
      
      // Toggle on
      neuralToggle.click();
      expect(document.body.classList.contains('neural-interface-active')).toBeTruthy();
      
      // Toggle off
      neuralToggle.click();
      expect(document.body.classList.contains('neural-interface-active')).toBeFalsy();
    });
  });

  describe('Quantum UI', () => {
    test('should add quantum indicators to cards', () => {
      uiEnhancer.setupQuantumUI();
      const quantumIndicator = document.querySelector('.quantum-indicator');
      expect(quantumIndicator).toBeTruthy();
      expect(quantumIndicator.innerHTML).toContain('fa-atom');
    });
  });

  describe('Holographic Elements', () => {
    test('should add holographic class to elements', () => {
      uiEnhancer.setupHolographicElements();
      const holographicElement = document.querySelector('.holographic');
      expect(holographicElement).toBeTruthy();
    });
  });

  describe('Adaptive Layout', () => {
    test('should optimize layout based on screen size', () => {
      // Mock window dimensions
      Object.defineProperty(window, 'innerWidth', { writable: true, configurable: true, value: 1920 });
      Object.defineProperty(window, 'innerHeight', { writable: true, configurable: true, value: 1080 });
      
      uiEnhancer.optimizeLayout();
      
      // Check for landscape layout
      expect(document.body.classList.contains('landscape-layout')).toBeTruthy();
      expect(document.body.classList.contains('ultra-wide-layout')).toBeTruthy();
    });
  });

  describe('Cognitive Load Optimization', () => {
    test('should add cognitive load indicators', () => {
      // Create a mock section
      const section = document.createElement('section');
      document.body.appendChild(section);
      
      uiEnhancer.setupCognitiveLoadOptimization();
      const cognitiveIndicator = section.querySelector('.cognitive-load-indicator');
      expect(cognitiveIndicator).toBeTruthy();
      expect(cognitiveIndicator.innerHTML).toContain('Cognitive Load: Low');
    });
  });

  describe('Neuro-Visual Enhancement', () => {
    test('should create neuro-visual toggle', () => {
      uiEnhancer.setupNeuroVisualEnhancement();
      const neuroToggle = document.querySelector('.neuro-visual-toggle');
      expect(neuroToggle).toBeTruthy();
      expect(neuroToggle.innerHTML).toContain('fa-eye');
    });

    test('should toggle neuro-visual enhancement', () => {
      uiEnhancer.setupNeuroVisualEnhancement();
      const neuroToggle = document.querySelector('.neuro-visual-toggle');
      
      // Initial state
      expect(document.body.classList.contains('neuro-visual-enhanced')).toBeFalsy();
      
      // Toggle on
      neuroToggle.click();
      expect(document.body.classList.contains('neuro-visual-enhanced')).toBeTruthy();
      
      // Toggle off
      neuroToggle.click();
      expect(document.body.classList.contains('neuro-visual-enhanced')).toBeFalsy();
    });
  });

  describe('Advanced Voice Commands', () => {
    test('should create voice training button', () => {
      uiEnhancer.setupAdvancedVoiceCommands();
      const trainingButton = document.querySelector('.voice-training-btn');
      expect(trainingButton).toBeTruthy();
      expect(trainingButton.innerHTML).toContain('fa-graduation-cap');
    });

    test('should show voice training interface', () => {
      uiEnhancer.showVoiceTrainingInterface();
      const trainingModal = document.querySelector('.voice-training-modal');
      expect(trainingModal).toBeTruthy();
      expect(trainingModal.querySelector('.voice-training-content')).toBeTruthy();
      expect(trainingModal.querySelectorAll('.train-btn').length).toBe(3);
    });

    test('should train voice command', () => {
      const consoleSpy = jest.spyOn(console, 'log');
      uiEnhancer.trainVoiceCommand('test command');
      expect(consoleSpy).toHaveBeenCalledWith('Training voice command: test command');
    });
  });
});

// Run the tests
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { HoloMeshUIEnhancements };
}