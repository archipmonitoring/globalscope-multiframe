// HoloMesh Achievement System
// Adds gamification elements to make the CAD AI optimization experience more engaging

class HoloMeshAchievementSystem {
    constructor() {
        this.achievements = [
            {
                id: 'first_optimization',
                title: 'Перший крок',
                description: 'Завершіть першу оптимізацію',
                icon: 'fa-flag-checkered',
                points: 10,
                unlocked: false
            },
            {
                id: 'master_optimizer',
                title: 'Майстер оптимізації',
                description: 'Завершіть 10 оптимізацій',
                icon: 'fa-trophy',
                points: 50,
                unlocked: false
            },
            {
                id: 'explorer',
                title: 'Дослідник',
                description: 'Спробуйте всі режими взаємодії',
                icon: 'fa-compass',
                points: 30,
                unlocked: false
            },
            {
                id: 'speed_demon',
                title: 'Швидкісний демон',
                description: 'Завершіть оптимізацію менше ніж за 5 секунд',
                icon: 'fa-bolt',
                points: 40,
                unlocked: false
            },
            {
                id: 'perfectionist',
                title: 'Перфекціоніст',
                description: 'Досягніть 95%+ рівня впевненості',
                icon: 'fa-star',
                points: 60,
                unlocked: false
            },
            {
                id: 'collaborator',
                title: 'Співпрацівник',
                description: 'Поділіться результатами оптимізації',
                icon: 'fa-users',
                points: 25,
                unlocked: false
            },
            {
                id: 'innovator',
                title: 'Новатор',
                description: 'Використовуйте інноваційний режим 5 разів',
                icon: 'fa-lightbulb',
                points: 35,
                unlocked: false
            },
            {
                id: 'professional',
                title: 'Професіонал',
                description: 'Використовуйте професійний режим 10 разів',
                icon: 'fa-graduation-cap',
                points: 45,
                unlocked: false
            }
        ];
        
        this.totalPoints = 0;
        this.init();
    }
    
    init() {
        this.loadAchievements();
        this.createAchievementPanel();
        this.setupEventListeners();
    }
    
    // Load achievements from localStorage
    loadAchievements() {
        const saved = localStorage.getItem('holomeshAchievements');
        if (saved) {
            const parsed = JSON.parse(saved);
            this.achievements = parsed.achievements || this.achievements;
            this.totalPoints = parsed.totalPoints || this.totalPoints;
        }
    }
    
    // Save achievements to localStorage
    saveAchievements() {
        const data = {
            achievements: this.achievements,
            totalPoints: this.totalPoints
        };
        localStorage.setItem('holomeshAchievements', JSON.stringify(data));
    }
    
    // Create achievement panel in the UI
    createAchievementPanel() {
        const panel = document.createElement('div');
        panel.className = 'achievement-panel';
        panel.innerHTML = `
            <div class="achievement-header">
                <h3><i class="fas fa-medal"></i> Досягнення</h3>
                <div class="points-display">
                    <span class="points">${this.totalPoints}</span>
                    <span class="points-label">балів</span>
                </div>
            </div>
            <div class="achievement-grid">
                ${this.achievements.map(achievement => `
                    <div class="achievement-item ${achievement.unlocked ? 'unlocked' : 'locked'}" 
                         data-achievement-id="${achievement.id}">
                        <div class="achievement-icon">
                            <i class="fas ${achievement.icon}"></i>
                        </div>
                        <div class="achievement-info">
                            <div class="achievement-title">${achievement.title}</div>
                            <div class="achievement-description">${achievement.description}</div>
                            <div class="achievement-points">+${achievement.points} балів</div>
                        </div>
                        ${achievement.unlocked ? 
                            '<div class="achievement-status unlocked"><i class="fas fa-check-circle"></i></div>' : 
                            '<div class="achievement-status locked"><i class="fas fa-lock"></i></div>'}
                    </div>
                `).join('')}
            </div>
        `;
        
        // Add to the dashboard
        const dashboard = document.querySelector('#main-content');
        if (dashboard) {
            dashboard.insertBefore(panel, dashboard.firstChild);
        }
    }
    
    // Setup event listeners for achievement tracking
    setupEventListeners() {
        // Listen for optimization completion
        document.addEventListener('optimizationComplete', (e) => {
            this.checkOptimizationAchievements(e.detail);
        });
        
        // Listen for mode changes
        document.addEventListener('modeChanged', (e) => {
            this.checkModeAchievements(e.detail);
        });
        
        // Listen for sharing actions
        document.addEventListener('resultShared', () => {
            this.unlockAchievement('collaborator');
        });
    }
    
    // Check achievements related to optimization completion
    checkOptimizationAchievements(result) {
        // First optimization
        this.unlockAchievement('first_optimization');
        
        // Speed demon - completion under 5 seconds
        if (result.execution_time < 5) {
            this.unlockAchievement('speed_demon');
        }
        
        // Perfectionist - 95%+ confidence
        if (result.confidence_score >= 0.95) {
            this.unlockAchievement('perfectionist');
        }
        
        // Master optimizer - count total optimizations
        const optimizationCount = parseInt(localStorage.getItem('optimizationCount') || '0') + 1;
        localStorage.setItem('optimizationCount', optimizationCount.toString());
        
        if (optimizationCount >= 10) {
            this.unlockAchievement('master_optimizer');
        }
    }
    
    // Check achievements related to mode usage
    checkModeAchievements(mode) {
        // Track mode usage
        const modeUsage = JSON.parse(localStorage.getItem('modeUsage') || '{}');
        modeUsage[mode] = (modeUsage[mode] || 0) + 1;
        localStorage.setItem('modeUsage', JSON.stringify(modeUsage));
        
        // Explorer - try all modes
        const allModes = ['professional', 'innovative', 'semi_automatic', 'manual'];
        const triedAll = allModes.every(m => modeUsage[m] > 0);
        if (triedAll) {
            this.unlockAchievement('explorer');
        }
        
        // Innovator - use innovative mode 5 times
        if (mode === 'innovative' && modeUsage.innovative >= 5) {
            this.unlockAchievement('innovator');
        }
        
        // Professional - use professional mode 10 times
        if (mode === 'professional' && modeUsage.professional >= 10) {
            this.unlockAchievement('professional');
        }
    }
    
    // Unlock an achievement
    unlockAchievement(achievementId) {
        const achievement = this.achievements.find(a => a.id === achievementId);
        if (achievement && !achievement.unlocked) {
            achievement.unlocked = true;
            this.totalPoints += achievement.points;
            this.saveAchievements();
            this.showAchievementNotification(achievement);
            this.updateAchievementPanel();
            return true;
        }
        return false;
    }
    
    // Show achievement notification
    showAchievementNotification(achievement) {
        const notification = document.createElement('div');
        notification.className = 'achievement-notification';
        notification.innerHTML = `
            <div class="achievement-notification-content">
                <div class="achievement-notification-icon">
                    <i class="fas ${achievement.icon}"></i>
                </div>
                <div class="achievement-notification-info">
                    <div class="achievement-notification-title">Нове досягнення!</div>
                    <div class="achievement-notification-name">${achievement.title}</div>
                    <div class="achievement-notification-points">+${achievement.points} балів</div>
                </div>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Add animation classes
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        // Remove after delay
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
    
    // Update achievement panel
    updateAchievementPanel() {
        const panel = document.querySelector('.achievement-panel');
        if (panel) {
            panel.querySelector('.points').textContent = this.totalPoints;
            
            // Update individual achievements
            this.achievements.forEach(achievement => {
                const item = panel.querySelector(`[data-achievement-id="${achievement.id}"]`);
                if (item && achievement.unlocked) {
                    item.classList.add('unlocked');
                    item.classList.remove('locked');
                    const status = item.querySelector('.achievement-status');
                    if (status) {
                        status.innerHTML = '<i class="fas fa-check-circle"></i>';
                        status.className = 'achievement-status unlocked';
                    }
                }
            });
        }
    }
    
    // Get unlocked achievements
    getUnlockedAchievements() {
        return this.achievements.filter(a => a.unlocked);
    }
    
    // Get locked achievements
    getLockedAchievements() {
        return this.achievements.filter(a => !a.unlocked);
    }
    
    // Reset all achievements (for testing)
    resetAchievements() {
        this.achievements.forEach(achievement => {
            achievement.unlocked = false;
        });
        this.totalPoints = 0;
        localStorage.removeItem('optimizationCount');
        localStorage.removeItem('modeUsage');
        this.saveAchievements();
        this.updateAchievementPanel();
    }
}

// Initialize achievement system when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.holomeshAchievements = new HoloMeshAchievementSystem();
});

// Export for use in other modules
export { HoloMeshAchievementSystem };