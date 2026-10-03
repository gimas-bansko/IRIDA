/**
 * Управление на системните броадкаст съобщения и известия (Broadcast Messages Modal).
 */

(function () {
    function getCsrfToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const BroadcastManager = {
        unreadMessages: [],
        currentIndex: 0,
        modalInstance: null,

        init: function () {
            const btn = document.getElementById('broadcastAcknowledgeBtn');
            if (btn) {
                btn.addEventListener('click', () => {
                    this.acknowledgeCurrent();
                });
            }
            this.checkUnread();
        },

        checkUnread: function () {
            axios.get('/api/broadcast-messages/unread/')
                .then(response => {
                    if (response.data && response.data.length > 0) {
                        this.unreadMessages = response.data;
                        this.currentIndex = 0;
                        this.showCurrentMessage();
                    }
                })
                .catch(error => {
                    console.error('Грешка при проверка за броадкаст съобщения:', error);
                });
        },

        showCurrentMessage: function () {
            if (!this.unreadMessages || this.currentIndex >= this.unreadMessages.length) {
                if (this.modalInstance) {
                    this.modalInstance.hide();
                }
                return;
            }

            const msg = this.unreadMessages[this.currentIndex];
            const modalEl = document.getElementById('broadcastModal');
            if (!modalEl) return;

            const titleEl = document.getElementById('broadcastTitle');
            const senderEl = document.getElementById('broadcastSender');
            const dateEl = document.getElementById('broadcastDate');
            const bodyEl = document.getElementById('broadcastMessageBody');
            const counterEl = document.getElementById('broadcastCounter');
            const badgeEl = document.getElementById('broadcastBadge');

            if (titleEl) titleEl.textContent = msg.title || 'Системно съобщение';
            if (senderEl) senderEl.innerHTML = `<i class="bi bi-person-fill me-1"></i>${msg.created_by_name || 'Администратор'}`;
            if (dateEl && msg.created_at) {
                const dateObj = new Date(msg.created_at);
                const formattedDate = dateObj.toLocaleDateString('bg-BG', {
                    day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'
                });
                dateEl.innerHTML = `<i class="bi bi-calendar3 me-1"></i>${formattedDate}`;
            }
            if (bodyEl) bodyEl.textContent = msg.message || '';
            if (badgeEl) badgeEl.textContent = msg.target_role_display || 'Всички';

            if (counterEl) {
                if (this.unreadMessages.length > 1) {
                    counterEl.textContent = `Съобщение ${this.currentIndex + 1} от ${this.unreadMessages.length}`;
                } else {
                    counterEl.textContent = '';
                }
            }

            const btn = document.getElementById('broadcastAcknowledgeBtn');
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = '<i class="bi bi-check2-circle me-1"></i>Разбрах';
            }

            if (!this.modalInstance && typeof bootstrap !== 'undefined') {
                this.modalInstance = new bootstrap.Modal(modalEl);
            }
            if (this.modalInstance) {
                this.modalInstance.show();
            }
        },

        acknowledgeCurrent: function () {
            if (!this.unreadMessages || this.currentIndex >= this.unreadMessages.length) return;

            const msg = this.unreadMessages[this.currentIndex];
            const btn = document.getElementById('broadcastAcknowledgeBtn');
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1" role="status"></span>Зареждане...';
            }

            axios.post(`/api/broadcast-messages/${msg.id}/mark-read/`, {}, {
                headers: {
                    'X-CSRFToken': getCsrfToken()
                }
            })
            .then(() => {
                this.currentIndex++;
                if (this.currentIndex < this.unreadMessages.length) {
                    this.showCurrentMessage();
                } else {
                    if (this.modalInstance) {
                        this.modalInstance.hide();
                    }
                }
            })
            .catch(error => {
                console.error('Грешка при маркиране на съобщение като прочетено:', error);
                if (btn) {
                    btn.disabled = false;
                    btn.innerHTML = '<i class="bi bi-check2-circle me-1"></i>Разбрах';
                }
            });
        }
    };

    window.BroadcastManager = BroadcastManager;

    document.addEventListener('DOMContentLoaded', function () {
        // Проверка след като DOM е готов
        setTimeout(() => {
            BroadcastManager.init();
        }, 500);
    });
})();
