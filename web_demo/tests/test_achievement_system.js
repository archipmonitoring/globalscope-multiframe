/**
 * Test suite for achievement system
 */

// Mock DOM for testing
const mockDOM = `
  <div id="testContainer"></div>
  <div id="main-content"></div>
`;

// Setup mock DOM
document.body.innerHTML = mockDOM;

// Import the achievement system module
import { HoloMeshAchievementSystem } from '../static/js/achievement_system.js';

describe('HoloMesh Achievement System', () => {
  let achievementSystem;

  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();
    achievementSystem = new HoloMeshAchievementSystem();
  });

  afterEach(() => {
    // Clear localStorage after each test
    localStorage.clear();
  });

  describe('Initialization', () => {
    test('should create achievement system instance', () => {
      expect(achievementSystem).toBeTruthy();
      expect(achievementSystem.achievements).toHaveLength(8);
      expect(achievementSystem.totalPoints).toBe(0);
    });

    test('should create achievement panel', () => {
      const panel = document.querySelector('.achievement-panel');
      expect(panel).toBeTruthy();
      expect(panel.querySelector('.achievement-header')).toBeTruthy();
      expect(panel.querySelector('.achievement-grid')).toBeTruthy();
    });
  });

  describe('Achievement Management', () => {
    test('should unlock achievement', () => {
      const result = achievementSystem.unlockAchievement('first_optimization');
      expect(result).toBe(true);
      
      const achievement = achievementSystem.achievements.find(a => a.id === 'first_optimization');
      expect(achievement.unlocked).toBe(true);
      expect(achievementSystem.totalPoints).toBe(10);
    });

    test('should not unlock already unlocked achievement', () => {
      // Unlock achievement first
      achievementSystem.unlockAchievement('first_optimization');
      
      // Try to unlock again
      const result = achievementSystem.unlockAchievement('first_optimization');
      expect(result).toBe(false);
      
      // Points should not increase
      expect(achievementSystem.totalPoints).toBe(10);
    });

    test('should get unlocked achievements', () => {
      achievementSystem.unlockAchievement('first_optimization');
      achievementSystem.unlockAchievement('explorer');
      
      const unlocked = achievementSystem.getUnlockedAchievements();
      expect(unlocked).toHaveLength(2);
      expect(unlocked[0].id).toBe('first_optimization');
      expect(unlocked[1].id).toBe('explorer');
    });

    test('should get locked achievements', () => {
      achievementSystem.unlockAchievement('first_optimization');
      
      const locked = achievementSystem.getLockedAchievements();
      expect(locked).toHaveLength(7);
      expect(locked.some(a => a.id === 'first_optimization')).toBe(false);
      expect(locked.some(a => a.id === 'master_optimizer')).toBe(true);
    });
  });

  describe('Persistence', () => {
    test('should save achievements to localStorage', () => {
      achievementSystem.unlockAchievement('first_optimization');
      achievementSystem.saveAchievements();
      
      const saved = localStorage.getItem('holomeshAchievements');
      expect(saved).toBeTruthy();
      
      const parsed = JSON.parse(saved);
      expect(parsed.totalPoints).toBe(10);
      expect(parsed.achievements[0].unlocked).toBe(true);
    });

    test('should load achievements from localStorage', () => {
      // Save some data first
      const testData = {
        achievements: [
          { id: 'first_optimization', unlocked: true, points: 10 },
          { id: 'master_optimizer', unlocked: false, points: 50 }
        ],
        totalPoints: 10
      };
      localStorage.setItem('holomeshAchievements', JSON.stringify(testData));
      
      // Create new instance to test loading
      const newSystem = new HoloMeshAchievementSystem();
      expect(newSystem.totalPoints).toBe(10);
      expect(newSystem.achievements[0].unlocked).toBe(true);
    });
  });

  describe('Event Handling', () => {
    test('should check optimization achievements', () => {
      const result = {
        execution_time: 3,
        confidence_score: 0.95
      };
      
      achievementSystem.checkOptimizationAchievements(result);
      
      // Should unlock speed_demon and perfectionist
      const speedDemon = achievementSystem.achievements.find(a => a.id === 'speed_demon');
      const perfectionist = achievementSystem.achievements.find(a => a.id === 'perfectionist');
      
      expect(speedDemon.unlocked).toBe(true);
      expect(perfectionist.unlocked).toBe(true);
    });

    test('should check mode achievements', () => {
      // Simulate using different modes
      achievementSystem.checkModeAchievements('professional');
      achievementSystem.checkModeAchievements('innovative');
      achievementSystem.checkModeAchievements('semi_automatic');
      achievementSystem.checkModeAchievements('manual');
      
      // Should unlock explorer achievement
      const explorer = achievementSystem.achievements.find(a => a.id === 'explorer');
      expect(explorer.unlocked).toBe(true);
    });
  });

  describe('UI Updates', () => {
    test('should update achievement panel', () => {
      // Unlock an achievement
      achievementSystem.unlockAchievement('first_optimization');
      
      // Check that panel was updated
      const panel = document.querySelector('.achievement-panel');
      const pointsDisplay = panel.querySelector('.points');
      expect(pointsDisplay.textContent).toBe('10');
      
      const firstAchievement = panel.querySelector('[data-achievement-id="first_optimization"]');
      expect(firstAchievement.classList.contains('unlocked')).toBe(true);
    });

    test('should show achievement notification', () => {
      const achievement = achievementSystem.achievements[0];
      achievementSystem.showAchievementNotification(achievement);
      
      const notification = document.querySelector('.achievement-notification');
      expect(notification).toBeTruthy();
      expect(notification.querySelector('.achievement-notification-name').textContent).toBe('Перший крок');
    });
  });

  describe('Reset Functionality', () => {
    test('should reset all achievements', () => {
      // Unlock some achievements
      achievementSystem.unlockAchievement('first_optimization');
      achievementSystem.unlockAchievement('explorer');
      
      // Reset
      achievementSystem.resetAchievements();
      
      // Check that everything is reset
      expect(achievementSystem.totalPoints).toBe(0);
      expect(achievementSystem.getUnlockedAchievements()).toHaveLength(0);
      expect(achievementSystem.getLockedAchievements()).toHaveLength(8);
    });
  });
});

// Run the tests
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { HoloMeshAchievementSystem };
}