/**
 * AI Prompts Manager for IRIDA
 * Управление на модален прозорец за AI промптове, динамично заместване на контекст и копиране в клипборда.
 */

(function () {
    const PAGE_LABELS = {
        'general': 'Общи',
        'lesson_main': 'Подготовка на урок',
        'course_goals': 'Цели на предмет',
        'course_units': 'Учебни раздели',
        'course_lessons': 'Теми за уроци',
        'session_list': 'Списък с уроци',
        'school_day': 'Учебен ден'
    };

    function getCookie(name) {
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

    function getCsrfToken() {
        return window.CSRF_TOKEN || getCookie('csrftoken') || '';
    }

    function escapeHtml(str) {
        if (!str) return '';
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    const AIPromptManager = {
        currentPageKey: 'general',
        currentContext: {},
        prompts: [],
        bsModal: null,

        init() {
            // Инициализация при зареждане на DOM
            document.addEventListener('DOMContentLoaded', () => {
                this.bindGlobalTriggers();
            });
        },

        bindGlobalTriggers() {
            document.querySelectorAll('[data-ai-page-key]').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const pageKey = btn.getAttribute('data-ai-page-key') || 'general';
                    this.open(pageKey);
                });
            });
        },

        setContext(contextObj) {
            this.currentContext = Object.assign({}, this.currentContext, contextObj);
        },

        getContextData() {
            // Ако има външен провайдър за контекст, го извикваме
            if (typeof window.getAIPageContext === 'function') {
                try {
                    const extContext = window.getAIPageContext();
                    return Object.assign({}, this.currentContext, extContext);
                } catch (e) {
                    console.error('Error fetching dynamic context:', e);
                }
            }
            return this.currentContext || {};
        },

        open(pageKey, contextData) {
            this.currentPageKey = pageKey || 'general';
            if (contextData) {
                this.setContext(contextData);
            }

            const modalEl = document.getElementById('aiPromptModal');
            if (!modalEl) {
                console.warn('aiPromptModal element not found in DOM.');
                return;
            }

            // Обновяване на значката за контекст
            const badgeEl = document.getElementById('aiPromptPageBadge');
            if (badgeEl) {
                badgeEl.textContent = PAGE_LABELS[this.currentPageKey] || this.currentPageKey;
            }

            // Задаване на подразбиращ се контекст при добавяне на нов промпт
            const selectEl = document.getElementById('aiNewPromptPageKey');
            if (selectEl) {
                selectEl.value = this.currentPageKey;
            }

            // Превключване на първия таб
            const listTabBtn = document.getElementById('ai-prompts-list-tab');
            if (listTabBtn && window.bootstrap) {
                const tab = new bootstrap.Tab(listTabBtn);
                tab.show();
            }

            // Отваряне на модала
            if (!this.bsModal && window.bootstrap) {
                this.bsModal = new bootstrap.Modal(modalEl);
            }
            if (this.bsModal) {
                this.bsModal.show();
            }

            // Зареждане на промптовете
            this.fetchPrompts(this.currentPageKey);
        },

        fetchPrompts(pageKey) {
            const container = document.getElementById('aiPromptListContainer');
            const loading = document.getElementById('aiPromptLoading');
            const emptyState = document.getElementById('aiPromptEmptyState');

            if (container) {
                container.innerHTML = `
                    <div class="text-center py-4 text-muted" id="aiPromptLoading">
                        <div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div>
                        Зареждане н�� промптове...
                    </div>
                `;
            }
            if (emptyState) emptyState.classList.add('d-none');

            axios.get(`/api/prompts/?page_key=${encodeURIComponent(pageKey)}`)
                .then(res => {
                    this.prompts = res.data || [];
                    this.renderPrompts(this.prompts);
                })
                .catch(err => {
                    console.error('Failed to load prompts:', err);
                    if (container) {
                        container.innerHTML = `
                            <div class="alert alert-danger py-2 fs-13">
                                Грешка при зареждане на промптовете. Моля, опитайте отново.
                            </div>
                        `;
                    }
                });
        },

        replacePlaceholders(text, ctx) {
            if (!text) return '';
            const context = ctx || this.getContextData();

            let result = text;
            const map = {
                '{предмет}': context.subject || context.subject_name || '',
                '{тема}': context.topic || context.topic_name || context.session_name || '',
                '{урок}': context.session_name || context.topic || '',
                '{цели}': context.goals || '',
                '{фокус}': context.focus || '',
                '{точки}': context.points || context.plan_points || '',
                '{клас}': context.grade ? `${context.grade} клас` : '',
                '{специалност}': context.specialty || context.specialty_name || ''
            };

            for (const [key, val] of Object.entries(map)) {
                const regex = new RegExp(key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
                result = result.replace(regex, val || `[не е въведено]`);
            }
            return result;
        },

        renderPrompts(promptList) {
            const container = document.getElementById('aiPromptListContainer');
            const emptyState = document.getElementById('aiPromptEmptyState');
            if (!container) return;

            if (!promptList || promptList.length === 0) {
                container.innerHTML = '';
                if (emptyState) emptyState.classList.remove('d-none');
                return;
            }

            if (emptyState) emptyState.classList.add('d-none');
            const context = this.getContextData();

            let html = '';
            promptList.forEach((p, idx) => {
                const resolvedText = this.replacePlaceholders(p.prompt_text, context);
                const isSystemBadge = p.is_system
                    ? `<span class="badge bg-primary-transparent text-primary"><i class="bi bi-patch-check me-1"></i>Системен</span>`
                    : `<span class="badge bg-success-transparent text-success"><i class="bi bi-person me-1"></i>${escapeHtml(p.created_by_name || 'Учител')}</span>`;

                const pageBadge = `<span class="badge bg-light text-muted border">${escapeHtml(p.page_key_display || p.page_key)}</span>`;

                html += `
                    <div class="card border custom-card shadow-none mb-0 prompt-card" data-prompt-id="${p.id}">
                        <div class="card-header py-2 px-3 bg-light d-flex align-items-center justify-content-between flex-wrap gap-2">
                            <div class="d-flex align-items-center gap-2 flex-wrap">
                                <strong class="fs-14 text-dark">${escapeHtml(p.title)}</strong>
                                ${isSystemBadge}
                                ${pageBadge}
                            </div>
                            <div class="d-flex gap-2">
                                <button type="button" class="btn btn-sm btn-primary label-btn" onclick="window.AIPromptManager.copyPrompt(${p.id}, this)">
                                    <i class="bi bi-clipboard label-btn-icon me-1"></i>Копирай промпта
                                </button>
                            </div>
                        </div>
                        <div class="card-body p-3">
                            ${p.instructions ? `
                                <div class="mb-2 p-2 rounded bg-warning-transparent text-warning-emphasis fs-12">
                                    <i class="bi bi-lightbulb me-1"></i><strong>Указания:</strong> ${escapeHtml(p.instructions)}
                                </div>
                            ` : ''}

                            <div class="prompt-preview bg-light p-2 rounded border fs-13 font-monospace text-secondary" style="white-space: pre-wrap; max-height: 180px; overflow-y: auto;">${escapeHtml(resolvedText)}</div>

                            <div class="d-flex justify-content-between align-items-center mt-2 pt-1 border-top">
                                <small class="text-muted fs-11">
                                    ${p.prompt_text.includes('{') ? '<i class="bi bi-magic me-1 text-primary"></i>Динамично попълнен с текущия урок' : '<i class="bi bi-file-text me-1"></i>Статичен шаблон'}
                                </small>
                                ${!p.is_system ? `
                                    <button type="button" class="btn btn-link text-danger p-0 fs-12 text-decoration-none" onclick="window.AIPromptManager.deletePrompt(${p.id})">
                                        <i class="bi bi-trash me-1"></i>Изтрий
                                    </button>
                                ` : ''}
                            </div>
                        </div>
                    </div>
                `;
            });

            container.innerHTML = html;
        },

        copyPrompt(promptId, btnEl) {
            const prompt = this.prompts.find(p => p.id === promptId);
            if (!prompt) return;

            const resolvedText = this.replacePlaceholders(prompt.prompt_text, this.getContextData());
            this.copyToClipboard(resolvedText, btnEl);
        },

        copyToClipboard(text, btnEl) {
            const doVisualFeedback = () => {
                if (!btnEl) return;
                const originalHtml = btnEl.innerHTML;
                const originalClass = btnEl.className;
                btnEl.innerHTML = '<i class="bi bi-check-lg label-btn-icon me-1"></i>Копирано!';
                btnEl.className = 'btn btn-sm btn-success label-btn';

                setTimeout(() => {
                    btnEl.innerHTML = originalHtml;
                    btnEl.className = originalClass;
                }, 2000);
            };

            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(text)
                    .then(() => doVisualFeedback())
                    .catch(() => this.fallbackCopy(text, doVisualFeedback));
            } else {
                this.fallbackCopy(text, doVisualFeedback);
            }
        },

        fallbackCopy(text, callback) {
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            try {
                document.execCommand('copy');
                if (callback) callback();
            } catch (err) {
                console.error('Fallback copy failed:', err);
                alert('Неуспешно копиране. Моля маркирайте и копирайте ръчно.');
            }
            document.body.removeChild(textArea);
        },

        filterPrompts() {
            const input = document.getElementById('aiPromptSearchInput');
            const term = (input ? input.value : '').toLowerCase().trim();

            if (!term) {
                this.renderPrompts(this.prompts);
                return;
            }

            const filtered = this.prompts.filter(p =>
                (p.title && p.title.toLowerCase().includes(term)) ||
                (p.prompt_text && p.prompt_text.toLowerCase().includes(term)) ||
                (p.instructions && p.instructions.toLowerCase().includes(term))
            );
            this.renderPrompts(filtered);
        },

        switchToNewTab() {
            const addTabBtn = document.getElementById('ai-prompts-add-tab');
            if (addTabBtn && window.bootstrap) {
                const tab = new bootstrap.Tab(addTabBtn);
                tab.show();
            }
        },

        insertPlaceholder(tag) {
            const textarea = document.getElementById('aiNewPromptText');
            if (!textarea) return;

            const start = textarea.selectionStart;
            const end = textarea.selectionEnd;
            const val = textarea.value;

            textarea.value = val.substring(0, start) + tag + val.substring(end);
            textarea.selectionStart = textarea.selectionEnd = start + tag.length;
            textarea.focus();
        },

        cancelEdit() {
            const form = document.getElementById('aiPromptCreateForm');
            if (form) form.reset();
            const idInput = document.getElementById('aiNewPromptId');
            if (idInput) idInput.value = '0';
            const errDiv = document.getElementById('aiPromptFormError');
            if (errDiv) errDiv.classList.add('d-none');
        },

        submitNewPrompt() {
            const title = (document.getElementById('aiNewPromptTitle')?.value || '').trim();
            const page_key = (document.getElementById('aiNewPromptPageKey')?.value || 'general').trim();
            const instructions = (document.getElementById('aiNewPromptInstructions')?.value || '').trim();
            const prompt_text = (document.getElementById('aiNewPromptText')?.value || '').trim();
            const id = parseInt(document.getElementById('aiNewPromptId')?.value || '0', 10);
            const errDiv = document.getElementById('aiPromptFormError');
            const submitBtn = document.getElementById('aiPromptSubmitBtn');

            if (!title || !prompt_text) {
                if (errDiv) {
                    errDiv.textContent = 'Моля, попълнете заглавие и текст на шаблона.';
                    errDiv.classList.remove('d-none');
                }
                return;
            }

            if (errDiv) errDiv.classList.add('d-none');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Записване...';
            }

            const payload = { id, title, page_key, instructions, prompt_text };
            const csrf = getCsrfToken();

            axios.post('/api/prompts/upsert/', payload, {
                headers: {
                    'X-CSRFToken': csrf,
                    'Content-Type': 'application/json'
                }
            })
            .then(res => {
                this.cancelEdit();
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="bi bi-check2 me-1"></i>Запази и сподели промпта';
                }
                // Връщане към таба със списъка и презареждане
                const listTabBtn = document.getElementById('ai-prompts-list-tab');
                if (listTabBtn && window.bootstrap) {
                    const tab = new bootstrap.Tab(listTabBtn);
                    tab.show();
                }
                this.fetchPrompts(this.currentPageKey);
            })
            .catch(err => {
                console.error('Failed to save prompt:', err);
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="bi bi-check2 me-1"></i>Запази и сподели промпта';
                }
                const msg = err.response?.data?.detail || 'Грешка при запис на промпта.';
                if (errDiv) {
                    errDiv.textContent = msg;
                    errDiv.classList.remove('d-none');
                }
            });
        },

        deletePrompt(promptId) {
            if (!confirm('Сигурни ли сте, че искате да изтриете този промпт?')) {
                return;
            }

            const csrf = getCsrfToken();
            axios.delete(`/api/prompts/${promptId}/`, {
                headers: { 'X-CSRFToken': csrf }
            })
            .then(() => {
                this.prompts = this.prompts.filter(p => p.id !== promptId);
                this.renderPrompts(this.prompts);
            })
            .catch(err => {
                console.error('Failed to delete prompt:', err);
                alert(err.response?.data?.detail || 'Грешка при изтриване на промпта.');
            });
        }
    };

    window.AIPromptManager = AIPromptManager;
    AIPromptManager.init();
})();
