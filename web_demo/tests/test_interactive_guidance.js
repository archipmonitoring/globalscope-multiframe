/**
 * Test suite for interactive guidance system
 */

// Mock DOM for testing
const mockDOM = `
  <div class="header"></div>
  <main>
    <section></section>
    <section></section>
  </main>
  <div class="card">
    <div class="card-body">
      <button id="testButton" class="btn-holomesh">Test Button</button>
      <input type="text" id="testInput" name="testInput">
      <select id="testSelect">
        <option value="1">Option 1</option>
        <option value="2">Option 2</option>
      </select>
    </div>
  </div>
  <div id="testContainer"></div>
`;

// Setup mock DOM
document.body.innerHTML = mockDOM;

// Import the UI enhancements module
import { HoloMeshUIEnhancements } from '../static/js/ui_enhancements.js';

describe('Interactive Guidance System', () => {
  let uiEnhancer;

  beforeEach(() => {
    uiEnhancer = new HoloMeshUIEnhancements();
  });

  describe('Interactive Guidance Container', () => {
    test('should create interactive guidance container', () => {
      uiEnhancer.setupInteractiveGuidance();
      const guidanceContainer = document.querySelector('.interactive-guidance-container');
      expect(guidanceContainer).toBeTruthy();
      expect(guidanceContainer.querySelector('.guidance-header')).toBeTruthy();
      expect(guidanceContainer.querySelector('.next-step-btn')).toBeTruthy();
    });

    test('should advance guidance steps', () => {
      uiEnhancer.setupInteractiveGuidance();
      const guidanceContainer = document.querySelector('.interactive-guidance-container');
      const nextBtn = guidanceContainer.querySelector('.next-step-btn');
      
      // Initial state
      const initialStep = guidanceContainer.querySelector('.current-step').textContent;
      expect(initialStep).toBe('Step 1 of 5: Select CAD Tool');
      
      // Advance to next step
      nextBtn.click();
      const updatedStep = guidanceContainer.querySelector('.current-step').textContent;
      expect(updatedStep).toBe('Step 2 of 5: Choose Interaction Mode');
    });
  });

  describe('Step-by-Step Workflow', () => {
    test('should add step indicators to sections', () => {
      uiEnhancer.setupStepByStepWorkflow();
      const stepIndicators = document.querySelectorAll('.workflow-step-indicator');
      expect(stepIndicators.length).toBe(2);
      expect(stepIndicators[0].querySelector('.step-number').textContent).toBe('1');
      expect(stepIndicators[1].querySelector('.step-number').textContent).toBe('2');
    });
  });

  describe('Real-Time Feedback', () => {
    test('should create feedback container', () => {
      uiEnhancer.setupRealTimeFeedback();
      const feedbackContainer = document.querySelector('.real-time-feedback-container');
      expect(feedbackContainer).toBeTruthy();
    });

    test('should show real-time feedback', () => {
      uiEnhancer.setupRealTimeFeedback();
      uiEnhancer.showRealTimeFeedback('Test feedback message');
      const feedback = document.querySelector('.real-time-feedback');
      expect(feedback).toBeTruthy();
      expect(feedback.textContent).toBe('Test feedback message');
    });

    test('should listen for form changes', () => {
      uiEnhancer.setupRealTimeFeedback();
      const input = document.getElementById('testInput');
      input.value = 'test value';
      input.dispatchEvent(new Event('change'));
      
      // Wait for feedback to appear
      setTimeout(() => {
        const feedback = document.querySelector('.real-time-feedback');
        expect(feedback).toBeTruthy();
      }, 100);
    });
  });

  describe('Voice Assistant', () => {
    test('should create voice assistant button', () => {
      uiEnhancer.setupVoiceAssistant();
      const assistantButton = document.querySelector('.voice-assistant-btn');
      expect(assistantButton).toBeTruthy();
      expect(assistantButton.innerHTML).toContain('fa-headset');
    });

    test('should activate voice assistant', () => {
      uiEnhancer.setupVoiceAssistant();
      const assistantButton = document.querySelector('.voice-assistant-btn');
      
      // Mock the voice command feedback method
      const feedbackSpy = jest.spyOn(uiEnhancer, 'showVoiceCommandFeedback');
      
      assistantButton.click();
      expect(feedbackSpy).toHaveBeenCalledWith('Holomiш, надай допомогу!');
    });

    test('should provide contextual help', () => {
      const helpMessage = uiEnhancer.getContextualHelp();
      expect(helpMessage).toBe('Я твій арбітр. Обери Configuration для початку роботи.');
    });
  });

  describe('Undo/Redo System', () => {
    test('should create undo/redo buttons', () => {
      uiEnhancer.setupUndoRedoSystem();
      const undoButton = document.querySelector('.undo-btn');
      const redoButton = document.querySelector('.redo-btn');
      expect(undoButton).toBeTruthy();
      expect(redoButton).toBeTruthy();
      expect(undoButton.innerHTML).toContain('fa-undo');
      expect(redoButton.innerHTML).toContain('fa-redo');
    });

    test('should record actions', () => {
      uiEnhancer.setupActionRecording();
      const input = document.getElementById('testInput');
      input.value = 'test value';
      input.dispatchEvent(new Event('change'));
      
      // Check that action was recorded
      expect(uiEnhancer.actionHistory.length).toBe(1);
      expect(uiEnhancer.actionHistory[0].type).toBe('form_change');
    });

    test('should perform undo', () => {
      // Record an action first
      const input = document.getElementById('testInput');
      input.dataset.previousValue = '';
      input.value = 'test value';
      
      uiEnhancer.recordAction({
        type: 'form_change',
        element: input,
        oldValue: '',
        newValue: 'test value'
      });
      
      // Perform undo
      uiEnhancer.performUndo();
      expect(uiEnhancer.currentHistoryIndex).toBe(-1);
      expect(input.value).toBe('');
    });

    test('should perform redo', () => {
      // Record an action and undo it first
      const input = document.getElementById('testInput');
      input.dataset.previousValue = '';
      input.value = 'test value';
      
      uiEnhancer.recordAction({
        type: 'form_change',
        element: input,
        oldValue: '',
        newValue: 'test value'
      });
      
      uiEnhancer.performUndo();
      
      // Now perform redo
      uiEnhancer.performRedo();
      expect(uiEnhancer.currentHistoryIndex).toBe(0);
      expect(input.value).toBe('test value');
    });
  });

  describe('Keyboard Shortcuts', () => {
    test('should handle Ctrl+Z for undo', () => {
      const undoSpy = jest.spyOn(uiEnhancer, 'performUndo');
      
      // Simulate Ctrl+Z keypress
      const event = new KeyboardEvent('keydown', { ctrlKey: true, key: 'z' });
      document.dispatchEvent(event);
      
      expect(undoSpy).toHaveBeenCalled();
    });

    test('should handle Ctrl+Y for redo', () => {
      const redoSpy = jest.spyOn(uiEnhancer, 'performRedo');
      
      // Simulate Ctrl+Y keypress
      const event = new KeyboardEvent('keydown', { ctrlKey: true, key: 'y' });
      document.dispatchEvent(event);
      
      expect(redoSpy).toHaveBeenCalled();
    });
  });
});

// Run the tests
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { HoloMeshUIEnhancements };
}