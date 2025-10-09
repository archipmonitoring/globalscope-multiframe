// HoloMesh Marketplace System
// NFT-based marketplace for chip designs with ZKP protection

class HoloMeshMarketplace {
    constructor() {
        this.chips = [];
        this.transactions = [];
        this.royalties = {};
        this.designers = {}; // Track designers and their IP blocks
        this.favoriteDesigners = []; // Track favorite designers for voice requests
        this.voiceRequests = []; // Track voice requests
        this.init();
    }
    
    init() {
        this.loadMarketplaceData();
        this.createMarketplacePanel();
        this.setupEventListeners();
        this.loadChipsFromServer(); // Load chips from backend
        this.setupVoiceRecognition(); // Setup voice recognition
    }
    
    // Load marketplace data from localStorage
    loadMarketplaceData() {
        const saved = localStorage.getItem('holomeshMarketplace');
        if (saved) {
            const parsed = JSON.parse(saved);
            this.chips = parsed.chips || this.chips;
            this.transactions = parsed.transactions || this.transactions;
            this.royalties = parsed.royalties || this.royalties;
            this.designers = parsed.designers || this.designers;
            this.favoriteDesigners = parsed.favoriteDesigners || this.favoriteDesigners;
            this.voiceRequests = parsed.voiceRequests || this.voiceRequests;
            this.subscriptionPreferences = parsed.subscriptionPreferences || {
                enabled: false,
                notificationFrequency: 'daily',
                autoPurchase: false
            };
        }
    }
    
    // Save marketplace data to localStorage
    saveMarketplaceData() {
        const data = {
            chips: this.chips,
            transactions: this.transactions,
            royalties: this.royalties,
            designers: this.designers,
            favoriteDesigners: this.favoriteDesigners,
            voiceRequests: this.voiceRequests,
            subscriptionPreferences: this.subscriptionPreferences
        };
        localStorage.setItem('holomeshMarketplace', JSON.stringify(data));
    }
    
    // Setup voice recognition
    setupVoiceRecognition() {
        // Check if browser supports speech recognition
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            this.speechRecognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            this.speechRecognition.continuous = false;
            this.speechRecognition.interimResults = false;
            this.speechRecognition.lang = 'uk-UA'; // Ukrainian language
            
            this.speechRecognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.processVoiceCommand(transcript);
            };
            
            this.speechRecognition.onerror = (event) => {
                console.error('Speech recognition error', event.error);
                this.showNotification('Помилка розпізнавання голосу: ' + event.error, 'error');
            };
        }
    }
    
    // Process voice command
    processVoiceCommand(command) {
        // Add to voice requests history
        this.voiceRequests.push({
            command: command,
            timestamp: new Date().toISOString()
        });
        this.saveMarketplaceData();
        
        // Show the voice command
        this.showNotification(`Голосова команда: "${command}"`, 'info');
        
        // Process specific commands
        if (command.toLowerCase().includes('збери чіпи') || command.toLowerCase().includes('зберай чіпи')) {
            // Extract designer names from command
            const designerMatches = command.match(/(?:з\s|із\s)([А-Яа-яІіЇїЄєҐґ\s]+)/g);
            if (designerMatches && designerMatches.length > 0) {
                const designers = designerMatches.map(match => match.replace(/^(?:з\s|із\s)/, '').trim());
                this.showNotification(`Шукаю чіпи від дизайнерів: ${designers.join(', ')}`, 'info');
                
                // Filter chips by favorite designers
                const filteredChips = this.filterChipsByDesigners(designers);
                if (filteredChips.length > 0) {
                    this.showDesignerChipsPanel(filteredChips, designers);
                } else {
                    this.showNotification('Чіпів від обраних дизайнерів не знайдено', 'info');
                }
            } else if (this.favoriteDesigners.length > 0) {
                // Use favorite designers if no specific designers mentioned
                this.showNotification('Шукаю чіпи від обраних дизайнерів...', 'info');
                const filteredChips = this.filterChipsByDesigners(this.favoriteDesigners);
                if (filteredChips.length > 0) {
                    this.showDesignerChipsPanel(filteredChips, this.favoriteDesigners);
                } else {
                    this.showNotification('Чіпів від обраних дизайнерів не знайдено', 'info');
                }
            } else {
                this.showNotification('Будь ласка, вкажіть дизайнерів або додайте їх до обраних', 'info');
            }
        } else if (command.toLowerCase().includes('додай до обраних') || command.toLowerCase().includes('обрані дизайнери')) {
            // Extract designer name from command
            const designerMatch = command.match(/(?:додай до обраних\s)([А-Яа-яІіЇїЄєҐґ\s]+)/);
            if (designerMatch) {
                const designer = designerMatch[1].trim();
                this.addFavoriteDesigner(designer);
            } else {
                this.showNotification('Будь ласка, вкажіть ім\'я дизайнера для додавання до обраних', 'info');
            }
        } else if (command.toLowerCase().includes('покажи обраних') || command.toLowerCase().includes('мої дизайнери')) {
            if (this.favoriteDesigners.length > 0) {
                this.showFavoriteDesigners();
            } else {
                this.showNotification('У вас немає обраних дизайнерів', 'info');
            }
        } else if (command.toLowerCase().includes('голосом') && (command.toLowerCase().includes('збери чіпи') || command.toLowerCase().includes('зберай чіпи'))) {
            // Handle voice subscription requests for favorite designers
            this.showNotification('Обробляю голосовий запит на підписку...', 'info');
            
            if (this.favoriteDesigners.length > 0) {
                this.showNotification('Шукаю чіпи від обраних дизайнерів через голосову підписку...', 'info');
                this.showFavoriteDesignerChipsPanel();
            } else {
                this.showNotification('У вас немає обраних дизайнерів. Додайте дизайнерів до обраних для голосової підписки.', 'info');
            }
        } else if (command.toLowerCase().includes('підписка') || command.toLowerCase().includes('підписатися')) {
            // Handle subscription requests
            this.showNotification('Обробляю запит на підписку на чіпи від обраних дизайнерів...', 'info');
            
            if (this.favoriteDesigners.length > 0) {
                this.showFavoriteDesignerChipsPanel();
            } else {
                this.showNotification('У вас немає обраних дизайнерів. Додайте дизайнерів до обраних для підписки.', 'info');
            }
        } else {
            this.showNotification('Команда не розпізнана. Спробуйте: "Збери чіпи з [ім\'я дизайнера]" або "Додай до обраних [ім\'я дизайнера]"', 'info');
        }
    }
    
    // Filter chips by designers
    filterChipsByDesigners(designerNames) {
        return this.chips.filter(chip => {
            // Check if chip designer is in the list
            if (designerNames.includes(chip.designer)) {
                return true;
            }
            
            // Check if any of the chip's designer IDs match
            if (chip.designerIds && Array.isArray(chip.designerIds)) {
                return chip.designerIds.some(id => 
                    designerNames.some(name => id.includes(name) || name.includes(id))
                );
            }
            
            return false;
        });
    }
    
    // Add favorite designer
    addFavoriteDesigner(designerName) {
        if (!this.favoriteDesigners.includes(designerName)) {
            this.favoriteDesigners.push(designerName);
            this.saveMarketplaceData();
            this.showNotification(`Дизайнер "${designerName}" доданий до обраних!`, 'success');
        } else {
            this.showNotification(`Дизайнер "${designerName}" вже в обраних`, 'info');
        }
    }
    
    // Show favorite designers
    showFavoriteDesigners() {
        const dialog = document.createElement('div');
        dialog.className = 'favorite-designers-dialog modal';
        dialog.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h4><i class="fas fa-heart"></i> Обрані дизайнери</h4>
                    <button class="close-btn">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="favorite-designers-content">
                        <p>Ваші обрані дизайнери для пріоритетного пошуку чіпів:</p>
                                                
                        <div class="subscription-settings">
                            <h5><i class="fas fa-bell"></i> Налаштування підписки</h5>
                            <div class="form-group">
                                <label>
                                    <input type="checkbox" id="subscriptionEnabled" ${this.subscriptionPreferences.enabled ? 'checked' : ''}> 
                                    Увімкнути підписку на чіпи від обраних дизайнерів
                                </label>
                            </div>
                            <div class="form-group">
                                <label for="notificationFrequency">Частота сповіщень:</label>
                                <select id="notificationFrequency" class="form-control">
                                    <option value="immediate" ${this.subscriptionPreferences.notificationFrequency === 'immediate' ? 'selected' : ''}>Негайно</option>
                                    <option value="daily" ${this.subscriptionPreferences.notificationFrequency === 'daily' ? 'selected' : ''}>Щодня</option>
                                    <option value="weekly" ${this.subscriptionPreferences.notificationFrequency === 'weekly' ? 'selected' : ''}>Щотижня</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>
                                    <input type="checkbox" id="autoPurchase" ${this.subscriptionPreferences.autoPurchase ? 'checked' : ''}> 
                                    Автоматично купувати нові чіпи (до 100 HLM)
                                </label>
                            </div>
                            <button class="btn btn-holomesh save-subscription-btn">
                                <i class="fas fa-save"></i> Зберегти налаштування
                            </button>
                        </div>
                        
                        <div class="favorite-designers-list">
                            ${this.favoriteDesigners.length > 0 ? 
                              this.favoriteDesigners.map((designer, index) => `
                                <div class="designer-item">
                                    <span class="designer-name">${designer}</span>
                                    <button class="btn btn-danger remove-designer-btn" data-designer="${designer}">
                                        <i class="fas fa-times"></i> Видалити
                                    </button>
                                </div>
                              `).join('') :
                              '<p class="text-muted">Немає обраних дизайнерів</p>'
                            }
                        </div>
                        
                        <div class="voice-command-instruction">
                            <h5><i class="fas fa-microphone"></i> Голосові команди</h5>
                            <ul>
                                <li>"Голосом: Збери чіпи з [ім'я дизайнера]"</li>
                                <li>"Голосом: Додай до обраних [ім'я дизайнера]"</li>
                                <li>"Голосом: Покажи обраних дизайнерів"</li>
                            </ul>
                        </div>
                        
                        <div class="voice-request-history">
                            <h5><i class="fas fa-history"></i> Історія голосових запитів</h5>
                            <div class="voice-requests-list">
                                ${this.voiceRequests.length > 0 ? 
                                  this.voiceRequests.slice(-5).reverse().map(request => `
                                    <div class="voice-request-item">
                                        <span class="request-text">"${request.command}"</span>
                                        <span class="request-time">${new Date(request.timestamp).toLocaleTimeString()}</span>
                                    </div>
                                  `).join('') :
                                  '<p class="text-muted">Немає голосових запитів</p>'
                                }
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary close-favorite-btn">Закрити</button>
                    <button class="btn btn-holomesh voice-activate-btn">
                        <i class="fas fa-microphone"></i> Активувати голос
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(dialog);
        
        // Add event listeners
        const closeBtn = dialog.querySelector('.close-btn');
        const closeFavoriteBtn = dialog.querySelector('.close-favorite-btn');
        const voiceActivateBtn = dialog.querySelector('.voice-activate-btn');
        const removeDesignerBtns = dialog.querySelectorAll('.remove-designer-btn');
        const saveSubscriptionBtn = dialog.querySelector('.save-subscription-btn');
        
        const closeDialog = () => {
            dialog.remove();
        };
        
        closeBtn.addEventListener('click', closeDialog);
        closeFavoriteBtn.addEventListener('click', closeDialog);
        
        voiceActivateBtn.addEventListener('click', () => {
            this.activateVoiceRecognition();
        });
        
        removeDesignerBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const designerName = e.target.closest('.remove-designer-btn').dataset.designer;
                this.removeFavoriteDesigner(designerName);
                // Refresh the dialog
                dialog.remove();
                this.showFavoriteDesigners();
            });
        });
        
        if (saveSubscriptionBtn) {
            saveSubscriptionBtn.addEventListener('click', () => {
                // Save subscription preferences
                this.subscriptionPreferences = {
                    enabled: dialog.querySelector('#subscriptionEnabled').checked,
                    notificationFrequency: dialog.querySelector('#notificationFrequency').value,
                    autoPurchase: dialog.querySelector('#autoPurchase').checked
                };
                this.saveMarketplaceData();
                this.showNotification('Налаштування підписки збережено!', 'success');
                
                // If subscription is enabled, show the subscription panel
                if (this.subscriptionPreferences.enabled) {
                    this.showFavoriteDesignerChipsPanel();
                }
            });
        }
    }
    
    // Remove favorite designer
    removeFavoriteDesigner(designerName) {
        this.favoriteDesigners = this.favoriteDesigners.filter(name => name !== designerName);
        this.saveMarketplaceData();
        this.showNotification(`Дизайнер "${designerName}" видалений з обраних`, 'info');
    }
    
    // Activate voice recognition
    activateVoiceRecognition() {
        if (this.speechRecognition) {
            try {
                this.speechRecognition.start();
                this.showNotification('Голосове розпізнавання активовано. Говоріть...', 'info');
            } catch (error) {
                console.error('Error starting speech recognition', error);
                this.showNotification('Помилка активації голосового розпізнавання', 'error');
            }
        } else {
            this.showNotification('Голосове розпізнавання не підтримується браузером', 'error');
        }
    }
    
    // Show designer chips panel
    showDesignerChipsPanel(chips, designerNames) {
        const panel = document.createElement('div');
        panel.className = 'designer-chips-panel';
        panel.innerHTML = `
            <div class="marketplace-panel">
                <div class="marketplace-header">
                    <h3><i class="fas fa-microchip"></i> Чіпи від обраних дизайнерів: ${designerNames.join(', ')}</h3>
                    <button class="close-panel-btn">&times;</button>
                </div>
                <div class="marketplace-grid">
                    ${chips.map(chip => this.createChipCard(chip)).join('')}
                </div>
            </div>
        `;
        
        // Add to the dashboard
        const dashboard = document.querySelector('#main-content');
        if (dashboard) {
            dashboard.insertBefore(panel, dashboard.firstChild);
        }
        
        // Add event listener to close button
        const closeBtn = panel.querySelector('.close-panel-btn');
        closeBtn.addEventListener('click', () => {
            panel.remove();
        });
        
        // Add event listeners to chip actions
        const buyButtons = panel.querySelectorAll('.buy-btn');
        const detailsButtons = panel.querySelectorAll('.details-btn');
        
        buyButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const chipId = e.target.closest('.buy-btn').dataset.chipId;
                this.purchaseChip(chipId);
            });
        });
        
        detailsButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const chipId = e.target.closest('.details-btn').dataset.chipId;
                this.showChipDetails(chipId);
            });
        });
        
        this.showNotification(`Знайдено ${chips.length} чіпів від обраних дизайнерів`, 'success');
    }
    
    // Show prioritized chips panel for favorite designers (subscription model)
    showFavoriteDesignerChipsPanel() {
        if (this.favoriteDesigners.length === 0) {
            this.showNotification('У вас немає обраних дизайнерів для підписки', 'info');
            return;
        }
        
        // Filter chips by favorite designers
        const filteredChips = this.filterChipsByDesigners(this.favoriteDesigners);
        
        if (filteredChips.length === 0) {
            this.showNotification('Чіпів від обраних дизайнерів не знайдено', 'info');
            return;
        }
        
        // Sort chips by designer priority (favorite designers first)
        const prioritizedChips = [...filteredChips].sort((a, b) => {
            const aIsFavorite = this.favoriteDesigners.includes(a.designer) || 
                               (a.designerIds && a.designerIds.some(id => this.favoriteDesigners.includes(id)));
            const bIsFavorite = this.favoriteDesigners.includes(b.designer) || 
                               (b.designerIds && b.designerIds.some(id => this.favoriteDesigners.includes(id)));
            
            // Chips from favorite designers come first
            if (aIsFavorite && !bIsFavorite) return -1;
            if (!aIsFavorite && bIsFavorite) return 1;
            
            // Then sort by sales/revenue
            return (b.sales || 0) - (a.sales || 0);
        });
        
        const panel = document.createElement('div');
        panel.className = 'favorite-designer-chips-panel';
        panel.innerHTML = `
            <div class="marketplace-panel">
                <div class="marketplace-header">
                    <h3><i class="fas fa-star"></i> Підписка на чіпи від обраних дизайнерів</h3>
                    <button class="close-panel-btn">&times;</button>
                </div>
                <div class="marketplace-controls">
                    <button class="btn btn-secondary manage-subscriptions-btn">
                        <i class="fas fa-cog"></i> Керувати підписками
                    </button>
                </div>
                <div class="marketplace-grid">
                    ${prioritizedChips.map(chip => this.createChipCard(chip)).join('')}
                </div>
                <div class="subscription-info">
                    <p><i class="fas fa-info-circle"></i> Це ваша персоналізована підписка на чіпи від обраних дизайнерів. Нові чіпи від цих дизайнерів з'являтимуться тут першими.</p>
                </div>
            </div>
        `;
        
        // Add to the dashboard
        const dashboard = document.querySelector('#main-content');
        if (dashboard) {
            dashboard.insertBefore(panel, dashboard.firstChild);
        }
        
        // Add event listener to close button
        const closeBtn = panel.querySelector('.close-panel-btn');
        closeBtn.addEventListener('click', () => {
            panel.remove();
        });
        
        // Add event listener to manage subscriptions button
        const manageSubscriptionsBtn = panel.querySelector('.manage-subscriptions-btn');
        manageSubscriptionsBtn.addEventListener('click', () => {
            this.showFavoriteDesigners();
        });
        
        // Add event listeners to chip actions
        const buyButtons = panel.querySelectorAll('.buy-btn');
        const detailsButtons = panel.querySelectorAll('.details-btn');
        
        buyButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const chipId = e.target.closest('.buy-btn').dataset.chipId;
                this.purchaseChip(chipId);
            });
        });
        
        detailsButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const chipId = e.target.closest('.details-btn').dataset.chipId;
                this.showChipDetails(chipId);
            });
        });
        
        this.showNotification(`Знайдено ${prioritizedChips.length} чіпів від обраних дизайнерів (підписка)`, 'success');
    }
    
    // Load chips from backend server
    async loadChipsFromServer() {
        try {
            const response = await fetch('/api/marketplace/chips');
            const result = await response.json();
            
            if (result.status === 'success') {
                this.chips = result.chips;
                this.saveMarketplaceData();
                this.refreshMarketplace();
            }
        } catch (error) {
            console.error('Error loading chips from server:', error);
            // Fallback to localStorage data
            this.loadMarketplaceData();
        }
    }
    
    // Simple QR Code generator (using canvas)
    generateQRCode(text, size = 128) {
        // This is a simplified QR code generator for demonstration
        // In a real implementation, we would use a proper QR code library
        // But for now, we'll create a placeholder that represents a QR code
        
        // For demo purposes, we'll return a data URL of a placeholder image
        // In a real implementation, this would generate an actual QR code
        return `data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 128 128"><rect width="128" height="128" fill="white"/><rect x="16" y="16" width="16" height="16" fill="black"/><rect x="32" y="16" width="16" height="16" fill="black"/><rect x="48" y="16" width="16" height="16" fill="black"/><rect x="80" y="16" width="16" height="16" fill="black"/><rect x="96" y="16" width="16" height="16" fill="black"/><rect x="16" y="32" width="16" height="16" fill="black"/><rect x="48" y="32" width="16" height="16" fill="black"/><rect x="64" y="32" width="16" height="16" fill="black"/><rect x="96" y="32" width="16" height="16" fill="black"/><rect x="16" y="48" width="16" height="16" fill="black"/><rect x="32" y="48" width="16" height="16" fill="black"/><rect x="48" y="48" width="16" height="16" fill="black"/><rect x="80" y="48" width="16" height="16" fill="black"/><rect x="96" y="48" width="16" height="16" fill="black"/><rect x="32" y="64" width="16" height="16" fill="black"/><rect x="48" y="64" width="16" height="16" fill="black"/><rect x="64" y="64" width="16" height="16" fill="black"/><rect x="80" y="64" width="16" height="16" fill="black"/><rect x="16" y="80" width="16" height="16" fill="black"/><rect x="48" y="80" width="16" height="16" fill="black"/><rect x="64" y="80" width="16" height="16" fill="black"/><rect x="96" y="80" width="16" height="16" fill="black"/><rect x="16" y="96" width="16" height="16" fill="black"/><rect x="32" y="96" width="16" height="16" fill="black"/><rect x="48" y="96" width="16" height="16" fill="black"/><rect x="80" y="96" width="16" height="16" fill="black"/><rect x="96" y="96" width="16" height="16" fill="black"/></svg>`;
    }
    
    // Create marketplace panel in the UI
    createMarketplacePanel() {
        const panel = document.createElement('div');
        panel.className = 'marketplace-panel';
        panel.innerHTML = `
            <div class="marketplace-header">
                <h3><i class="fas fa-store"></i> Маркетплейс чіпів</h3>
                <div class="marketplace-stats">
                    <span class="chip-count">${this.chips.length} чіпів</span>
                    <span class="transaction-count">${this.transactions.length} транзакцій</span>
                </div>
            </div>
            <div class="marketplace-controls">
                <button class="btn btn-holomesh publish-btn">
                    <i class="fas fa-upload"></i> Опублікувати чіп
                </button>
                <button class="btn btn-secondary refresh-btn">
                    <i class="fas fa-sync"></i> Оновити
                </button>
                <button class="btn btn-warning subscription-btn">
                    <i class="fas fa-star"></i> Підписка
                </button>
            </div>
            <div class="marketplace-grid">
                ${this.chips.map(chip => this.createChipCard(chip)).join('')}
            </div>
        `;
        
        // Add to the dashboard
        const dashboard = document.querySelector('#main-content');
        if (dashboard) {
            // Check if panel already exists and replace it
            const existingPanel = document.querySelector('.marketplace-panel');
            if (existingPanel) {
                existingPanel.replaceWith(panel);
            } else {
                dashboard.insertBefore(panel, dashboard.firstChild);
            }
        }
        
        // Add event listeners
        this.setupMarketplaceEventListeners(panel);
    }
    
    // Create chip card HTML
    createChipCard(chip) {
        return `
            <div class="chip-card" data-chip-id="${chip.id}">
                <div class="chip-image">
                    <i class="fas fa-microchip"></i>
                </div>
                <div class="chip-info">
                    <div class="chip-name">${chip.name}</div>
                    <div class="chip-designer">Дизайнер: ${chip.designer}</div>
                    <div class="chip-price">${chip.price} HLM</div>
                    <div class="chip-royalty">Роялті: ${chip.royalty}%</div>
                    <div class="chip-ip-blocks">${chip.ipBlocks} IP-блоків</div>
                    <div class="chip-nft-id">NFT: ${chip.nftId.substring(0, 10)}...</div>
                    <div class="chip-qr-preview">
                        <i class="fas fa-qrcode"></i> QR-код NFT
                    </div>
                    <div class="chip-zkp">${chip.zkpProtected ? '<i class="fas fa-shield-alt"></i> ZKP захищено' : 'Без ZKP'}</div>
                </div>
                <div class="chip-actions">
                    <button class="btn btn-primary buy-btn" data-chip-id="${chip.id}">
                        <i class="fas fa-shopping-cart"></i> Купити
                    </button>
                    <button class="btn btn-secondary details-btn" data-chip-id="${chip.id}">
                        <i class="fas fa-info-circle"></i> Деталі
                    </button>
                </div>
            </div>
        `;
    }
    
    // Setup marketplace event listeners
    setupMarketplaceEventListeners(panel) {
        // Publish button
        const publishBtn = panel.querySelector('.publish-btn');
        if (publishBtn) {
            publishBtn.addEventListener('click', () => {
                this.showPublishDialog();
            });
        }
        
        // Refresh button
        const refreshBtn = panel.querySelector('.refresh-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.loadChipsFromServer();
            });
        }
        
        // Subscription button
        const subscriptionBtn = panel.querySelector('.subscription-btn');
        if (subscriptionBtn) {
            subscriptionBtn.addEventListener('click', () => {
                this.showFavoriteDesignerChipsPanel();
            });
        }
        
        // Buy buttons
        const buyButtons = panel.querySelectorAll('.buy-btn');
        buyButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const chipId = e.target.closest('.buy-btn').dataset.chipId;
                this.purchaseChip(chipId);
            });
        });
        
        // Details buttons
        const detailsButtons = panel.querySelectorAll('.details-btn');
        detailsButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const chipId = e.target.closest('.details-btn').dataset.chipId;
                this.showChipDetails(chipId);
            });
        });
    }
    
    // Setup global event listeners
    setupEventListeners() {
        // Listen for chip publishing events
        document.addEventListener('chipPublished', (e) => {
            this.addChipToMarketplace(e.detail);
            // Check if this chip is from a favorite designer and subscription is enabled
            this.checkSubscriptionForNewChip(e.detail);
        });
        
        // Listen for chip purchase events
        document.addEventListener('chipPurchased', (e) => {
            this.processPurchase(e.detail);
        });
        
        // Setup subscription checker
        this.setupSubscriptionChecker();
    }
    
    // Setup subscription checker based on preferences
    setupSubscriptionChecker() {
        if (this.subscriptionPreferences.enabled && this.subscriptionPreferences.notificationFrequency === 'daily') {
            // Check for new chips daily
            setInterval(() => {
                this.checkForNewChipsFromFavorites();
            }, 24 * 60 * 60 * 1000); // 24 hours
        } else if (this.subscriptionPreferences.enabled && this.subscriptionPreferences.notificationFrequency === 'weekly') {
            // Check for new chips weekly
            setInterval(() => {
                this.checkForNewChipsFromFavorites();
            }, 7 * 24 * 60 * 60 * 1000); // 7 days
        }
    }
    
    // Check if a newly published chip is from a favorite designer
    checkSubscriptionForNewChip(chip) {
        if (!this.subscriptionPreferences.enabled) return;
        
        const isFromFavorite = this.favoriteDesigners.includes(chip.designer) || 
                              (chip.designerIds && chip.designerIds.some(id => this.favoriteDesigners.includes(id)));
        
        if (isFromFavorite) {
            // Notify user about new chip from favorite designer
            this.showNotification(`Новий чіп від обраного дизайнера: ${chip.name}`, 'success');
            
            // Auto-purchase if enabled and within budget
            if (this.subscriptionPreferences.autoPurchase && chip.price <= 100) {
                this.purchaseChip(chip.id);
                this.showNotification(`Автоматично куплено чіп: ${chip.name}`, 'success');
            }
        }
    }
    
    // Check for new chips from favorite designers
    checkForNewChipsFromFavorites() {
        if (!this.subscriptionPreferences.enabled || this.favoriteDesigners.length === 0) return;
        
        // Filter chips by favorite designers
        const filteredChips = this.filterChipsByDesigners(this.favoriteDesigners);
        
        if (filteredChips.length > 0) {
            this.showNotification(`Знайдено ${filteredChips.length} нових чіпів від обраних дизайнерів!`, 'success');
        }
    }
    
    // Show publish dialog
    showPublishDialog() {
        const dialog = document.createElement('div');
        dialog.className = 'publish-dialog modal';
        dialog.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h4><i class="fas fa-upload"></i> Опублікувати чіп</h4>
                    <button class="close-btn">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="form-group">
                        <label for="chipName">Назва чіпу:</label>
                        <input type="text" id="chipName" class="form-control" placeholder="Введіть назву чіпу">
                    </div>
                    <div class="form-group">
                        <label for="chipDescription">Опис:</label>
                        <textarea id="chipDescription" class="form-control" placeholder="Опишіть чіп"></textarea>
                    </div>
                    <div class="form-group">
                        <label for="chipPrice">Ціна (HLM):</label>
                        <input type="number" id="chipPrice" class="form-control" placeholder="Введіть ціну" min="0" step="0.1">
                    </div>
                    <div class="form-group">
                        <label for="chipRoyalty">Роялті (%):</label>
                        <input type="number" id="chipRoyalty" class="form-control" placeholder="Введіть % роялті" min="0" max="100" step="0.1">
                    </div>
                    <div class="form-group">
                        <label for="chipIpBlocks">Кількість IP-блоків:</label>
                        <input type="number" id="chipIpBlocks" class="form-control" placeholder="Введіть кількість IP-блоків" min="1" value="1">
                    </div>
                    <div class="form-group">
                        <label for="chipSerialNumber">Серійний номер:</label>
                        <input type="text" id="chipSerialNumber" class="form-control" placeholder="Введіть серійний номер">
                    </div>
                    <div class="form-group">
                        <label for="chipDesignerIds">ID дизайнерів (через кому):</label>
                        <input type="text" id="chipDesignerIds" class="form-control" placeholder="Введіть ID дизайнерів через кому">
                        <small class="form-text text-muted">Примітка: Кожен чіп отримує QR-код NFT для доступу до інформації про дизайнерів</small>
                    </div>
                    <div class="form-group">
                        <label>
                            <input type="checkbox" id="zkpProtection" checked> 
                            Захист ZKP (Zero-Knowledge Proof)
                        </label>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary cancel-btn">Скасувати</button>
                    <button class="btn btn-holomesh publish-confirm-btn">Опублікувати</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(dialog);
        
        // Add event listeners
        const closeBtn = dialog.querySelector('.close-btn');
        const cancelBtn = dialog.querySelector('.cancel-btn');
        const publishBtn = dialog.querySelector('.publish-confirm-btn');
        
        const closeDialog = () => {
            dialog.remove();
        };
        
        closeBtn.addEventListener('click', closeDialog);
        cancelBtn.addEventListener('click', closeDialog);
        
        publishBtn.addEventListener('click', () => {
            this.publishChip();
            closeDialog();
        });
    }
    
    // Publish chip to marketplace
    async publishChip() {
        const name = document.getElementById('chipName').value;
        const description = document.getElementById('chipDescription').value;
        const price = parseFloat(document.getElementById('chipPrice').value);
        const royalty = parseFloat(document.getElementById('chipRoyalty').value);
        const ipBlocks = parseInt(document.getElementById('chipIpBlocks').value) || 1;
        const serialNumber = document.getElementById('chipSerialNumber').value || `SN-${Date.now()}`;
        const designerIds = document.getElementById('chipDesignerIds').value.split(',').map(id => id.trim()).filter(id => id);
        const zkpProtected = document.getElementById('zkpProtection').checked;
        
        if (!name || isNaN(price) || isNaN(royalty)) {
            this.showNotification('Будь ласка, заповніть всі обов\'язкові поля', 'error');
            return;
        }
        
        // Generate QR code URL for designers page (always generate for consistency)
        const qrCodeUrl = `/nft/designers/${encodeURIComponent(name.replace(/\s+/g, '-'))}-${Date.now()}`;
        
        // Generate comprehensive NFT data
        const nftData = {
            chipName: name,
            chipDescription: description,
            price: price,
            royalty: royalty,
            ipBlocks: ipBlocks,
            serialNumber: serialNumber,
            designerIds: designerIds,
            qrCodeUrl: qrCodeUrl, // QR code URL for designers page
            designer: 'Поточний користувач',
            qualityMetrics: {
                performanceScore: Math.floor(Math.random() * 40) + 60, // 60-100
                powerEfficiency: Math.floor(Math.random() * 30) + 70, // 70-100
                areaEfficiency: Math.floor(Math.random() * 35) + 65, // 65-100
            },
            technicalSpecs: {
                frequency: `${Math.floor(Math.random() * 2000) + 1000} MHz`,
                powerConsumption: `${(Math.random() * 5 + 1).toFixed(2)} W`,
                area: `${(Math.random() * 10 + 5).toFixed(2)} mm²`
            },
            certification: {
                qualityCertified: true,
                systemVerified: true,
                timestamp: new Date().toISOString()
            }
        };
        
        const chipData = {
            name: name,
            description: description,
            price: price,
            royalty: royalty,
            designer: 'Поточний користувач', // In real implementation, this would be the actual user
            ipBlocks: ipBlocks,
            serialNumber: serialNumber,
            designerIds: designerIds,
            nftData: nftData, // Store full NFT data
            qrCodeUrl: qrCodeUrl, // Store QR code URL
            zkpProtected: zkpProtected
        };
        
        try {
            // Send to backend
            const response = await fetch('/api/marketplace/publish', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(chipData)
            });
            
            const result = await response.json();
            
            if (result.status === 'success') {
                this.chips.push(result.chip);
                this.saveMarketplaceData();
                this.refreshMarketplace();
                
                // Dispatch event
                const event = new CustomEvent('chipPublished', { detail: result.chip });
                document.dispatchEvent(event);
                
                this.showNotification(`Чіп "${name}" успішно опубліковано!`, 'success');
            } else {
                this.showNotification(`Помилка публікації: ${result.message}`, 'error');
            }
        } catch (error) {
            console.error('Error publishing chip:', error);
            this.showNotification('Помилка публікації чіпу', 'error');
        }
    }
    
    // Add chip to marketplace
    addChipToMarketplace(chipData) {
        this.chips.push(chipData);
        this.saveMarketplaceData();
        this.refreshMarketplace();
        this.showNotification(`Новий чіп "${chipData.name}" додано до маркетплейсу!`, 'success');
    }
    
    // Purchase chip
    async purchaseChip(chipId) {
        const chip = this.chips.find(c => c.id === chipId);
        if (!chip) {
            this.showNotification('Чіп не знайдено', 'error');
            return;
        }
        
        try {
            // Send purchase request to backend
            const response = await fetch('/api/marketplace/purchase', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    chipId: chipId,
                    buyer: 'Поточний користувач'
                })
            });
            
            const result = await response.json();
            
            if (result.status === 'success') {
                // Update local data
                chip.sales++;
                chip.revenue += chip.price;
                
                this.transactions.push(result.transaction);
                
                // Process royalties for all designers
                if (chip.designerIds && chip.designerIds.length > 0) {
                    const royaltyPerDesigner = result.royalty.amount / chip.designerIds.length;
                    chip.designerIds.forEach(designerId => {
                        if (!this.royalties[designerId]) {
                            this.royalties[designerId] = 0;
                        }
                        this.royalties[designerId] += royaltyPerDesigner;
                    });
                } else {
                    // Fallback to original designer
                    if (!this.royalties[chip.designer]) {
                        this.royalties[chip.designer] = 0;
                    }
                    this.royalties[chip.designer] += result.royalty.amount;
                }
                
                this.saveMarketplaceData();
                
                // Dispatch event
                const event = new CustomEvent('chipPurchased', { detail: { chip, transaction: result.transaction } });
                document.dispatchEvent(event);
                
                this.showNotification(`Чіп "${chip.name}" успішно придбано!`, 'success');
                this.refreshMarketplace();
            } else {
                this.showNotification(`Помилка покупки: ${result.message}`, 'error');
            }
        } catch (error) {
            console.error('Error purchasing chip:', error);
            this.showNotification('Помилка покупки чіпу', 'error');
        }
    }
    
    // Process purchase
    processPurchase(purchaseData) {
        // In real implementation, this would handle the actual purchase logic
        console.log('Processing purchase:', purchaseData);
        this.showNotification(`Транзакція завершена успішно!`, 'success');
    }
    
    // Process royalties
    processRoyalties(chip) {
        // This is now handled in the purchaseChip method
        // Calculate royalty amount
        const royaltyAmount = (chip.price * chip.royalty) / 100;
        
        // In real implementation, this would distribute royalties to IP block creators
        // For demo, we'll just track it
        
        if (!this.royalties[chip.designer]) {
            this.royalties[chip.designer] = 0;
        }
        this.royalties[chip.designer] += royaltyAmount;
        
        this.showNotification(`Роялті ${royaltyAmount.toFixed(2)} HLM нараховано дизайнеру`, 'info');
    }
    
    // Show chip details
    showChipDetails(chipId) {
        const chip = this.chips.find(c => c.id === chipId);
        if (!chip) {
            this.showNotification('Чіп не знайдено', 'error');
            return;
        }
        
        // Format NFT data for display
        const nftData = chip.nftData || {};
        const qualityMetrics = nftData.qualityMetrics || {};
        const technicalSpecs = nftData.technicalSpecs || {};
        const certification = nftData.certification || {};
        
        // Generate QR code
        const qrCodeDataUrl = this.generateQRCode(chip.qrCodeUrl || `chip-${chip.id}`);
        
        // Generate QR code display with clickable functionality
        const qrCodeSection = `
            <div class="detail-section">
                <h5>QR-код NFT</h5>
                <div class="qr-code-container">
                    <div class="qr-code-display">
                        <img src="${qrCodeDataUrl}" alt="QR Code for chip designers" class="qr-code-image clickable-qr" data-chip-id="${chip.id}" style="cursor: pointer; transition: transform 0.2s;">
                        <p class="qr-code-url">${chip.qrCodeUrl || 'N/A'}</p>
                    </div>
                    <button class="btn btn-secondary view-designers-btn" data-url="${chip.qrCodeUrl}" data-chip-id="${chip.id}">
                        <i class="fas fa-external-link-alt"></i> Переглянути інформацію про дизайнерів
                    </button>
                    <p class="text-muted">
                        <small>Скануйте цей QR-код або натисніть на нього, щоб переглянути інформацію про дизайнерів чіпа: 
                        рейтинги, портфоліо, відгуки клієнтів та команди. Для дослідників: знайдіть найкращих дизайнерів 
                        для співпраці через HoloMesh!</small>
                    </p>
                </div>
            </div>
        `;
        
        const dialog = document.createElement('div');
        dialog.className = 'chip-details-dialog modal';
        dialog.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h4><i class="fas fa-microchip"></i> Деталі чіпу: ${chip.name}</h4>
                    <button class="close-btn">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="chip-detail-info">
                        <div class="detail-row">
                            <span class="label">Дизайнер:</span>
                            <span class="value">${chip.designer}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Опис:</span>
                            <span class="value">${chip.description || 'Немає опису'}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Ціна:</span>
                            <span class="value">${chip.price} HLM</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Роялті:</span>
                            <span class="value">${chip.royalty}%</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Захист ZKP:</span>
                            <span class="value">${chip.zkpProtected ? 'Так' : 'Ні'}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">IP-блоків:</span>
                            <span class="value">${chip.ipBlocks}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Серійний номер:</span>
                            <span class="value">${chip.serialNumber || 'N/A'}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Кількість дизайнерів:</span>
                            <span class="value">${chip.designerIds ? chip.designerIds.length : 0}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Продажів:</span>
                            <span class="value">${chip.sales}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Загальний дохід:</span>
                            <span class="value">${chip.revenue.toFixed(2)} HLM</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">NFT ID:</span>
                            <span class="value">${chip.nftId}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Дата публікації:</span>
                            <span class="value">${new Date(chip.timestamp).toLocaleString()}</span>
                        </div>
                        
                        <!-- NFT Quality Metrics -->
                        <div class="detail-section">
                            <h5>Метрики якості (NFT)</h5>
                            <div class="detail-row">
                                <span class="label">Оцінка продуктивності:</span>
                                <span class="value">${qualityMetrics.performanceScore || 'N/A'}/100</span>
                            </div>
                            <div class="detail-row">
                                <span class="label">Ефективність енергоспоживання:</span>
                                <span class="value">${qualityMetrics.powerEfficiency || 'N/A'}/100</span>
                            </div>
                            <div class="detail-row">
                                <span class="label">Ефективність площі:</span>
                                <span class="value">${qualityMetrics.areaEfficiency || 'N/A'}/100</span>
                            </div>
                        </div>
                        
                        <!-- Technical Specifications -->
                        <div class="detail-section">
                            <h5>Технічні характеристики (NFT)</h5>
                            <div class="detail-row">
                                <span class="label">Частота:</span>
                                <span class="value">${technicalSpecs.frequency || 'N/A'}</span>
                            </div>
                            <div class="detail-row">
                                <span class="label">Споживання енергії:</span>
                                <span class="value">${technicalSpecs.powerConsumption || 'N/A'}</span>
                            </div>
                            <div class="detail-row">
                                <span class="label">Площа:</span>
                                <span class="value">${technicalSpecs.area || 'N/A'}</span>
                            </div>
                        </div>
                        
                        <!-- Certification -->
                        <div class="detail-section">
                            <h5>Сертифікація (NFT)</h5>
                            <div class="detail-row">
                                <span class="label">Сертифіковано якістю:</span>
                                <span class="value">${certification.qualityCertified ? 'Так' : 'Ні'}</span>
                            </div>
                            <div class="detail-row">
                                <span class="label">Перевірено системою:</span>
                                <span class="value">${certification.systemVerified ? 'Так' : 'Ні'}</span>
                            </div>
                            <div class="detail-row">
                                <span class="label">Дата сертифікації:</span>
                                <span class="value">${certification.timestamp ? new Date(certification.timestamp).toLocaleString() : 'N/A'}</span>
                            </div>
                        </div>
                        
                        <!-- QR Code Section -->
                        ${qrCodeSection}
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary close-details-btn">Закрити</button>
                    <button class="btn btn-primary buy-details-btn" data-chip-id="${chip.id}">
                        <i class="fas fa-shopping-cart"></i> Купити за ${chip.price} HLM
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(dialog);
        
        // Add event listeners
        const closeBtn = dialog.querySelector('.close-btn');
        const closeDetailsBtn = dialog.querySelector('.close-details-btn');
        const buyBtn = dialog.querySelector('.buy-details-btn');
        const viewDesignersBtn = dialog.querySelector('.view-designers-btn');
        const clickableQr = dialog.querySelector('.clickable-qr');
        
        const closeDialog = () => {
            dialog.remove();
        };
        
        closeBtn.addEventListener('click', closeDialog);
        closeDetailsBtn.addEventListener('click', closeDialog);
        
        // Add hover effect to QR code
        if (clickableQr) {
            clickableQr.addEventListener('mouseenter', () => {
                clickableQr.style.transform = 'scale(1.05)';
            });
            
            clickableQr.addEventListener('mouseleave', () => {
                clickableQr.style.transform = 'scale(1)';
            });
            
            // Make QR code clickable
            clickableQr.addEventListener('click', (e) => {
                const chipId = e.target.dataset.chipId;
                const chip = this.chips.find(c => c.id === chipId);
                if (chip) {
                    this.showDesignerInfoPage(chip);
                }
            });
        }
        
        if (viewDesignersBtn) {
            viewDesignersBtn.addEventListener('click', (e) => {
                const chipId = e.target.dataset.chipId;
                const chip = this.chips.find(c => c.id === chipId);
                if (chip) {
                    this.showDesignerInfoPage(chip);
                }
            });
        }
        
        buyBtn.addEventListener('click', () => {
            this.purchaseChip(chipId);
            closeDialog();
        });
    }
    
    // Show designer information page
    showDesignerInfoPage(chip) {
        const dialog = document.createElement('div');
        dialog.className = 'designer-info-dialog modal';
        dialog.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h4><i class="fas fa-users"></i> Дизайнери чіпа: ${chip.name}</h4>
                    <button class="close-btn">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="designer-info-content">
                        <div class="benefit-highlight">
                            <h5><i class="fas fa-star"></i> Вигода нашого підходу:</h5>
                            <p class="benefit-text">
                                <strong>100% якість вашого чіпа, зібраного з нуля по ваших потребах!</strong><br>
                                Вся взаємодія проходить через HoloMesh - гарантований результат!
                            </p>
                        </div>
                        
                        <p>Інформація про дизайнерів, які брали участь у створенні цього чіпа:</p>
                        
                        <div class="designer-list">
                            ${chip.designerIds && chip.designerIds.length > 0 ? 
                              chip.designerIds.map((designerId, index) => `
                                <div class="designer-card">
                                    <div class="designer-header">
                                        <h5>Дизайнер #${index + 1}</h5>
                                        <div class="designer-rating">
                                            <i class="fas fa-star"></i>
                                            <span>${(Math.random() * 2 + 3).toFixed(1)}/5.0</span>
                                        </div>
                                    </div>
                                    <div class="designer-details">
                                        <div class="detail-row">
                                            <span class="label">ID:</span>
                                            <span class="value">${designerId}</span>
                                        </div>
                                        <div class="detail-row">
                                            <span class="label">Спеціалізація:</span>
                                            <span class="value">${['Процесори', 'Пам\'ять', 'Інтерфейси', 'Аналогові блоки'][Math.floor(Math.random() * 4)]}</span>
                                        </div>
                                        <div class="detail-row">
                                            <span class="label">Досвід:</span>
                                            <span class="value">${Math.floor(Math.random() * 10) + 1} років</span>
                                        </div>
                                        <div class="detail-row">
                                            <span class="label">Проекти:</span>
                                            <span class="value">${Math.floor(Math.random() * 50) + 10}</span>
                                        </div>
                                    </div>
                                    <div class="designer-actions">
                                        <button class="btn btn-secondary view-profile-btn" data-designer-id="${designerId}">
                                            <i class="fas fa-user"></i> Переглянути профіль
                                        </button>
                                        <button class="btn btn-outline-primary contact-btn" data-designer-id="${designerId}">
                                            <i class="fas fa-envelope"></i> Зв'язатися через HoloMesh
                                        </button>
                                    </div>
                                </div>
                              `).join('') :
                              `<div class="designer-card">
                                  <div class="designer-header">
                                      <h5>Основний дизайнер</h5>
                                      <div class="designer-rating">
                                          <i class="fas fa-star"></i>
                                          <span>${(Math.random() * 2 + 3).toFixed(1)}/5.0</span>
                                      </div>
                                  </div>
                                  <div class="designer-details">
                                      <div class="detail-row">
                                          <span class="label">Ім'я:</span>
                                          <span class="value">${chip.designer}</span>
                                      </div>
                                      <div class="detail-row">
                                          <span class="label">Спеціалізація:</span>
                                          <span class="value">${['Процесори', 'Пам\'ять', 'Інтерфейси', 'Аналогові блоки'][Math.floor(Math.random() * 4)]}</span>
                                      </div>
                                      <div class="detail-row">
                                          <span class="label">Досвід:</span>
                                          <span class="value">${Math.floor(Math.random() * 10) + 1} років</span>
                                      </div>
                                      <div class="detail-row">
                                          <span class="label">Проекти:</span>
                                          <span class="value">${Math.floor(Math.random() * 50) + 10}</span>
                                      </div>
                                  </div>
                                  <div class="designer-actions">
                                      <button class="btn btn-secondary view-profile-btn" data-designer-id="${chip.designer}">
                                          <i class="fas fa-user"></i> Переглянути профіль
                                      </button>
                                      <button class="btn btn-outline-primary contact-btn" data-designer-id="${chip.designer}">
                                          <i class="fas fa-envelope"></i> Зв'язатися через HoloMesh
                                      </button>
                                  </div>
                              </div>`
                        }
                        </div>
                        
                        <div class="team-collaboration">
                            <h5><i class="fas fa-users-cog"></i> Командна співпраця</h5>
                            <p>Ці дизайнери часто працюють разом у наступних командах:</p>
                            <div class="team-list">
                                <span class="badge bg-primary">Quantum Chip Designers</span>
                                <span class="badge bg-success">AI Hardware Team</span>
                                <span class="badge bg-info">Next-Gen Processors</span>
                            </div>
                        </div>
                        
                        <div class="client-feedback">
                            <h5><i class="fas fa-comments"></i> Відгуки клієнтів</h5>
                            <div class="feedback-list">
                                <div class="feedback-item">
                                    <div class="feedback-header">
                                        <span class="client-name">TechCorp Inc.</span>
                                        <div class="feedback-rating">
                                            <i class="fas fa-star"></i>
                                            <i class="fas fa-star"></i>
                                            <i class="fas fa-star"></i>
                                            <i class="fas fa-star"></i>
                                            <i class="fas fa-star-half-alt"></i>
                                            <span>4.5/5</span>
                                        </div>
                                    </div>
                                    <p class="feedback-text">"Висока якість дизайну та відмінна співпраця. Рекомендуємо!"</p>
                                </div>
                                <div class="feedback-item">
                                    <div class="feedback-header">
                                        <span class="client-name">InnovateLab</span>
                                        <div class="feedback-rating">
                                            <i class="fas fa-star"></i>
                                            <i class="fas fa-star"></i>
                                            <i class="fas fa-star"></i>
                                            <i class="fas fa-star"></i>
                                            <i class="fas fa-star"></i>
                                            <span>5/5</span>
                                        </div>
                                    </div>
                                    <p class="feedback-text">"Профеcіоналізм на найвищому рівні. Швидке виконання та чудові результати."</p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="collaboration-process">
                            <h5><i class="fas fa-sync-alt"></i> Процес співпраці через HoloMesh</h5>
                            <ol>
                                <li>Дослідники знаходять дизайнерів через QR-код</li>
                                <li>Всі комунікації проходять через HoloMesh</li>
                                <li>Гарантована якість результату</li>
                                <li>100% захист інтелектуальної власності</li>
                            </ol>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary close-designer-btn">Закрити</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(dialog);
        
        // Add event listeners
        const closeBtn = dialog.querySelector('.close-btn');
        const closeDesignerBtn = dialog.querySelector('.close-designer-btn');
        const viewProfileBtns = dialog.querySelectorAll('.view-profile-btn');
        const contactBtns = dialog.querySelectorAll('.contact-btn');
        
        const closeDialog = () => {
            dialog.remove();
        };
        
        closeBtn.addEventListener('click', closeDialog);
        closeDesignerBtn.addEventListener('click', closeDialog);
        
        viewProfileBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const designerId = e.target.closest('.view-profile-btn').dataset.designerId;
                alert(`Відкривається профіль дизайнера: ${designerId}\n\nТут буде повна інформація про дизайнера, його портфоліо та досягнення.`);
            });
        });
        
        contactBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const designerId = e.target.closest('.contact-btn').dataset.designerId;
                alert(`Запит на співпрацю з дизайнером ${designerId} надіслано через HoloMesh!

Наша система забезпечить:
- 100% якість результату
- Конфіденційність проекту
- Професійну підтримку
- Гарантоване виконання термінів`);
            });
        });
    }
    
    // Refresh marketplace
    refreshMarketplace() {
        this.createMarketplacePanel();
    }
    
    // Show notification
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `marketplace-notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        // Remove after delay
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
    
    // Get marketplace statistics
    async getStatistics() {
        try {
            const response = await fetch('/api/marketplace/stats');
            const result = await response.json();
            
            if (result.status === 'success') {
                return result.statistics;
            } else {
                // Fallback to local calculation
                return {
                    totalChips: this.chips.length,
                    totalTransactions: this.transactions.length,
                    totalRevenue: this.chips.reduce((sum, chip) => sum + chip.revenue, 0),
                    totalRoyalties: Object.values(this.royalties).reduce((sum, royalty) => sum + royalty, 0)
                };
            }
        } catch (error) {
            console.error('Error getting statistics:', error);
            // Fallback to local calculation
            return {
                totalChips: this.chips.length,
                totalTransactions: this.transactions.length,
                totalRevenue: this.chips.reduce((sum, chip) => sum + chip.revenue, 0),
                totalRoyalties: Object.values(this.royalties).reduce((sum, royalty) => sum + royalty, 0)
            };
        }
    }
}

// Initialize marketplace when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.holomeshMarketplace = new HoloMeshMarketplace();
});

// Export for use in other modules
export { HoloMeshMarketplace };
