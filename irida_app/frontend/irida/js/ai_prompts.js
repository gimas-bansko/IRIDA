/**
 * AI Prompts Manager for IRIDA
 * Управление на модален прозорец за AI промптове, динамично заместване на контекст,
 * авторство, дублиране като собствен, компактен изглед и филтриране.
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
        expandedPromptIds: new Set(),
        currentVisibilityFilter: 'all',
        bsModal: null,

        init() {
            document.addEventListener('DOMContentLoaded', () => {
                this.bindGlobalTriggers();
            });
        },

        bindGlobalTriggers() {
            document.querySelectorAll('[data-ai-page-key]').forEach(btn => {
                btn.addEventListener('click', () => {
                    const pageKey = btn.getAttribute('data-ai-page-key') || 'general';
                    this.open(pageKey);
                });
            });
        },

        setContext(contextObj) {
            this.currentContext = Object.assign({}, this.currentContext, contextObj);
        },

        getContextData() {
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

            // Нулиране на формата към режим "Добави нов"
            this.resetFormToNewMode();

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
                    this.updateFilterCounts();
                    this.filterPrompts();
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

        updateFilterCounts() {
            const totalCount = this.prompts.length;
            const systemCount = this.prompts.filter(p => p.is_system).length;
            const mineCount = this.prompts.filter(p => p.is_author).length;

            const countAll = document.getElementById('aiCountAll');
            const countSystem = document.getElementById('aiCountSystem');
            const countMine = document.getElementById('aiCountMine');

            if (countAll) countAll.textContent = totalCount;
            if (countSystem) countSystem.textContent = systemCount;
            if (countMine) countMine.textContent = mineCount;
        },

        setVisibilityFilter(filter) {
            this.currentVisibilityFilter = filter || 'all';

            const filterGroup = document.getElementById('aiPromptVisibilityFilterGroup');
            if (filterGroup) {
                filterGroup.querySelectorAll('button[data-filter]').forEach(btn => {
                    if (btn.getAttribute('data-filter') === this.currentVisibilityFilter) {
                        btn.classList.add('active');
                    } else {
                        btn.classList.remove('active');
                    }
                });
            }

            this.filterPrompts();
        },

        clearSearch() {
            const input = document.getElementById('aiPromptSearchInput');
            if (input) {
                input.value = '';
            }
            this.filterPrompts();
        },

        filterPrompts() {
            const input = document.getElementById('aiPromptSearchInput');
            const term = (input ? input.value : '').toLowerCase().trim();

            let filtered = this.prompts;

            // Филтър по видимост (всички, системни, собствени)
            if (this.currentVisibilityFilter === 'system') {
                filtered = filtered.filter(p => p.is_system);
            } else if (this.currentVisibilityFilter === 'mine') {
                filtered = filtered.filter(p => p.is_author);
            }

            // Филтър по ключова дума / търсене
            if (term) {
                filtered = filtered.filter(p =>
                    (p.title && p.title.toLowerCase().includes(term)) ||
                    (p.prompt_text && p.prompt_text.toLowerCase().includes(term)) ||
                    (p.instructions && p.instructions.toLowerCase().includes(term)) ||
                    (p.created_by_name && p.created_by_name.toLowerCase().includes(term))
                );
            }

            this.renderPrompts(filtered);
        },

        replacePlaceholders(text, ctx) {
            if (!text) return '';
            const context = ctx || this.getContextData();

            let result = text;
            const map = {
                '{предмет}': context.subject || context.subject_name || '',
                '{тема}': context.topic || context.topic_name || context.session_name || '',
                '{урок}': context.session_name || context.topic || '',
                '{урок_номер}': context.session_num || context.session?.num || '',
                '{номер}': context.session_num || context.session?.num || '',
                '{вид_урок}': context.session_type || '',
                '{тип_урок}': context.session_type || '',
                '{продължителност}': context.duration_hours || context.duration || '',
                '{продължителност_минути}': context.duration_mins || '',
                '{цели}': context.goals || '',
                '{социално_емоционални_цели}': context.social_emotional_goals || context.sel_goals || '',
                '{сео_цели}': context.social_emotional_goals || context.sel_goals || '',
                '{фокус}': context.focus || '',
                '{точки}': context.points || context.plan_points || '',
                '{клас}': context.grade ? (String(context.grade).includes('клас') ? context.grade : `${context.grade} клас`) : '',
                '{специалност}': context.specialty || context.specialty_name || '',
                '{включени_теми}': context.topics_list || context.units_and_topics || context.curriculum_text || '',
                '{теми}': context.topics_list || context.units_and_topics || context.curriculum_text || '',
                '{списък_уроци}': context.lessons_list || context.sessions_list || context.lessons || '',
                '{уроци}': context.lessons_list || context.sessions_list || context.lessons || '',
                '{структура_часове}': context.hours_structure || context.hours_info || '',
                '{хорариум}': context.hours_structure || context.hours_info || '',
                '{раздели_и_теми}': context.units_and_topics || context.curriculum_text || '',
                '{учебна_програма}': context.units_and_topics || context.curriculum_text || ''
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
            promptList.forEach(p => {
                const isExpanded = this.expandedPromptIds.has(p.id);
                const resolvedText = this.replacePlaceholders(p.prompt_text, context);

                let authorBadge = '';
                if (p.is_system) {
                    authorBadge = `<span class="badge bg-primary-transparent text-primary"><i class="bi bi-patch-check me-1"></i>Системен</span>`;
                } else if (p.is_author) {
                    authorBadge = `<span class="badge bg-success-transparent text-success"><i class="bi bi-person-check me-1"></i>Мой авторски</span>`;
                } else {
                    authorBadge = `<span class="badge bg-info-transparent text-info"><i class="bi bi-person me-1"></i>${escapeHtml(p.created_by_name || 'Учител')}</span>`;
                }

                const pageBadge = `<span class="badge bg-secondary-transparent text-muted border">${escapeHtml(p.page_key_display || p.page_key)}</span>`;

                html += `
                    <div class="card border custom-card shadow-none mb-0 prompt-card" data-prompt-id="${p.id}">
                        <!-- Заглавен ред: компактен изглед -->
                        <div class="card-header py-2 px-3 d-flex align-items-center justify-content-between flex-wrap gap-2">
                            <div class="d-flex align-items-center gap-2 flex-wrap">
                                <strong class="fs-14 custom-black">${escapeHtml(p.title)}</strong>
                                ${authorBadge}
                                ${pageBadge}
                            </div>
                            <small class="text-muted fs-11">
                                ${p.prompt_text.includes('{') ? '<i class="bi bi-magic me-1 text-primary"></i>Динамичен' : '<i class="bi bi-file-text me-1"></i>Статичен'}
                            </small>
                        </div>

                        <!-- Тяло на промпта: свито по подразбиране, разгъва се по желание -->
                        <div class="card-body p-3 pt-2 prompt-details-body ${isExpanded ? '' : 'd-none'}" id="prompt-details-${p.id}">
                            ${p.instructions ? `
                                <div class="mb-2 p-2 rounded bg-warning-transparent text-warning-emphasis fs-12">
                                    <i class="bi bi-lightbulb me-1"></i><strong>Указания:</strong> ${escapeHtml(p.instructions)}
                                </div>
                            ` : ''}

                            <div class="prompt-preview p-2 rounded border fs-13 font-monospace" style="white-space: pre-wrap; max-height: 200px; overflow-y: auto;">${escapeHtml(resolvedText)}</div>

                            <small class="text-muted fs-11 mt-1 d-block">
                                ${p.prompt_text.includes('{') ? '<i class="bi bi-info-circle me-1"></i>Данните от урока са попълнени автоматично в текста.' : ''}
                            </small>
                        </div>

                        <!-- Ред с бутони: на отделен ред, подредени вдясно -->
                        <div class="card-footer border-top py-2 px-3 d-flex justify-content-end align-items-center gap-2 flex-wrap">
                            <!-- Бутон за разгъване/свиване на детайлите -->
                            <button type="button" class="btn btn-sm btn-outline-secondary" onclick="window.AIPromptManager.toggleDetails(${p.id}, this)" title="Преглед на съдържанието и указанията">
                                <i class="bi ${isExpanded ? 'bi-chevron-up' : 'bi-chevron-down'} me-1"></i><span>${isExpanded ? 'Свий' : 'Покажи'}</span>
                            </button>

                            <!-- Бутон за дублиране като авторски промпт -->
                            <button type="button" class="btn btn-sm btn-outline-primary" onclick="window.AIPromptManager.duplicatePrompt(${p.id})" title="Създай свое копие на този промпт с възможност за редакция">
                                <i class="bi bi-check2-all me-1"></i>Дублирай
                            </button>

                            <!-- Бутон за копиране в клипборда -->
                            <button type="button" class="btn btn-sm btn-primary label-btn" onclick="window.AIPromptManager.copyPrompt(${p.id}, this)">
                                <i class="bi bi-clipboard label-btn-icon me-1"></i>Копирай промпта
                            </button>

                            <!-- Бутон за редакция (само ако потребителят има права) -->
                            ${p.can_edit ? `
                                <button type="button" class="btn btn-sm btn-outline-warning" onclick="window.AIPromptManager.editPrompt(${p.id})" title="Редактирай този промпт">
                                    <i class="bi bi-pencil me-1"></i>Редактирай
                                </button>
                            ` : ''}

                            <!-- Бутон за изтриване (само ако потребителят има права) -->
                            ${p.can_delete ? `
                                <button type="button" class="btn btn-sm btn-outline-danger" onclick="window.AIPromptManager.deletePrompt(${p.id})" title="Изтрий този промпт">
                                    <i class="bi bi-trash me-1"></i>Изтрий
                                </button>
                            ` : ''}
                        </div>
                    </div>
                `;
            });

            container.innerHTML = html;
        },

        toggleDetails(promptId, btnEl) {
            const detailsEl = document.getElementById(`prompt-details-${promptId}`);
            if (!detailsEl) return;

            const isCurrentlyHidden = detailsEl.classList.contains('d-none');
            if (isCurrentlyHidden) {
                detailsEl.classList.remove('d-none');
                this.expandedPromptIds.add(promptId);
                if (btnEl) {
                    btnEl.innerHTML = '<i class="bi bi-chevron-up me-1"></i><span>Свий</span>';
                }
            } else {
                detailsEl.classList.add('d-none');
                this.expandedPromptIds.delete(promptId);
                if (btnEl) {
                    btnEl.innerHTML = '<i class="bi bi-chevron-down me-1"></i><span>Покажи</span>';
                }
            }
        },

        toggleAllCards() {
            const allDetailEls = document.querySelectorAll('.prompt-details-body');
            const toggleAllBtnText = document.getElementById('aiPromptToggleAllText');
            const toggleAllBtnIcon = document.querySelector('#aiPromptToggleAllBtn i');

            // Ако има поне един свит, разгъваме всички; иначе свиваме всички
            let shouldExpandAll = false;
            allDetailEls.forEach(el => {
                if (el.classList.contains('d-none')) {
                    shouldExpandAll = true;
                }
            });

            allDetailEls.forEach(el => {
                const promptId = parseInt(el.id.replace('prompt-details-', ''), 10);
                if (shouldExpandAll) {
                    el.classList.remove('d-none');
                    if (promptId) this.expandedPromptIds.add(promptId);
                } else {
                    el.classList.add('d-none');
                    if (promptId) this.expandedPromptIds.delete(promptId);
                }
            });

            // Обновяване на бутоните на всяка карта
            document.querySelectorAll('.prompt-card').forEach(card => {
                const btn = card.querySelector('.btn-outline-secondary');
                if (btn && btn.getAttribute('onclick')?.includes('toggleDetails')) {
                    if (shouldExpandAll) {
                        btn.innerHTML = '<i class="bi bi-chevron-up me-1"></i><span>Свий</span>';
                    } else {
                        btn.innerHTML = '<i class="bi bi-chevron-down me-1"></i><span>Покажи</span>';
                    }
                }
            });

            if (toggleAllBtnText) {
                toggleAllBtnText.textContent = shouldExpandAll ? 'Свий всички' : 'Разгъни всички';
            }
            if (toggleAllBtnIcon) {
                toggleAllBtnIcon.className = shouldExpandAll ? 'bi bi-arrows-collapse me-1' : 'bi bi-arrows-expand me-1';
            }
        },

        duplicatePrompt(promptId) {
            const prompt = this.prompts.find(p => p.id === promptId);
            if (!prompt) return;

            // Превключване към таб 2 за добавяне/дублиране
            this.switchToNewTab();

            // Попълване на данните от избрания промпт като нов (id=0)
            const idInput = document.getElementById('aiNewPromptId');
            const titleInput = document.getElementById('aiNewPromptTitle');
            const pageKeySelect = document.getElementById('aiNewPromptPageKey');
            const instructionsInput = document.getElementById('aiNewPromptInstructions');
            const textInput = document.getElementById('aiNewPromptText');

            if (idInput) idInput.value = '0';
            if (titleInput) titleInput.value = `${prompt.title} (копие)`;
            if (pageKeySelect) pageKeySelect.value = prompt.page_key || 'general';
            if (instructionsInput) instructionsInput.value = prompt.instructions || '';
            if (textInput) textInput.value = prompt.prompt_text || '';

            // Обновяване на заглавията и значките във формата
            const headingEl = document.getElementById('aiPromptFormHeading');
            const modeBadge = document.getElementById('aiPromptFormModeBadge');
            const submitBtn = document.getElementById('aiPromptSubmitBtn');
            const addTabLabel = document.getElementById('aiPromptAddTabLabel');
            const addTabIcon = document.getElementById('aiPromptAddTabIcon');

            if (headingEl) {
                headingEl.innerHTML = '<i class="bi bi-copy text-primary me-1"></i>Дублиране като собствен авторски промпт';
            }
            if (modeBadge) {
                modeBadge.textContent = 'Копие на #' + prompt.id;
                modeBadge.className = 'badge bg-primary-transparent text-primary fs-11';
            }
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="bi bi-check2 me-1"></i>Създай авторски промпт';
            }
            if (addTabLabel) addTabLabel.textContent = 'Нов промпт (копие)';
            if (addTabIcon) addTabIcon.className = 'bi bi-copy me-1';

            if (textInput) textInput.focus();
        },

        editPrompt(promptId) {
            const prompt = this.prompts.find(p => p.id === promptId);
            if (!prompt) return;

            if (!prompt.can_edit) {
                alert('Нямате права за редакция на този промпт.');
                return;
            }

            // Превключване към таб 2
            this.switchToNewTab();

            // Попълване на данните за редакция (id = prompt.id)
            const idInput = document.getElementById('aiNewPromptId');
            const titleInput = document.getElementById('aiNewPromptTitle');
            const pageKeySelect = document.getElementById('aiNewPromptPageKey');
            const instructionsInput = document.getElementById('aiNewPromptInstructions');
            const textInput = document.getElementById('aiNewPromptText');

            if (idInput) idInput.value = prompt.id;
            if (titleInput) titleInput.value = prompt.title;
            if (pageKeySelect) pageKeySelect.value = prompt.page_key || 'general';
            if (instructionsInput) instructionsInput.value = prompt.instructions || '';
            if (textInput) textInput.value = prompt.prompt_text || '';

            // Обновяване на заглавията и значките във формата
            const headingEl = document.getElementById('aiPromptFormHeading');
            const modeBadge = document.getElementById('aiPromptFormModeBadge');
            const submitBtn = document.getElementById('aiPromptSubmitBtn');
            const addTabLabel = document.getElementById('aiPromptAddTabLabel');
            const addTabIcon = document.getElementById('aiPromptAddTabIcon');

            if (headingEl) {
                headingEl.innerHTML = '<i class="bi bi-pencil text-warning me-1"></i>Редактиране на собствен промпт';
            }
            if (modeBadge) {
                modeBadge.textContent = 'Редакция #' + prompt.id;
                modeBadge.className = 'badge bg-warning-transparent text-warning fs-11';
            }
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="bi bi-check2 me-1"></i>Запази промените';
            }
            if (addTabLabel) addTabLabel.textContent = 'Редакция на промпт';
            if (addTabIcon) addTabIcon.className = 'bi bi-pencil me-1';

            if (titleInput) titleInput.focus();
        },

        resetFormToNewMode() {
            const form = document.getElementById('aiPromptCreateForm');
            if (form) form.reset();

            const idInput = document.getElementById('aiNewPromptId');
            if (idInput) idInput.value = '0';

            const pageKeySelect = document.getElementById('aiNewPromptPageKey');
            if (pageKeySelect) pageKeySelect.value = this.currentPageKey || 'general';

            const headingEl = document.getElementById('aiPromptFormHeading');
            const modeBadge = document.getElementById('aiPromptFormModeBadge');
            const submitBtn = document.getElementById('aiPromptSubmitBtn');
            const addTabLabel = document.getElementById('aiPromptAddTabLabel');
            const addTabIcon = document.getElementById('aiPromptAddTabIcon');
            const errDiv = document.getElementById('aiPromptFormError');

            if (headingEl) {
                headingEl.innerHTML = '<i class="bi bi-plus-circle text-primary me-1"></i>Създаване на нов авторски промпт';
            }
            if (modeBadge) {
                modeBadge.textContent = 'Нов запис';
                modeBadge.className = 'badge bg-secondary-transparent text-secondary fs-11';
            }
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="bi bi-check2 me-1"></i>Запази и сподели промпта';
            }
            if (addTabLabel) addTabLabel.textContent = 'Добави нов промпт';
            if (addTabIcon) addTabIcon.className = 'bi bi-plus-circle me-1';
            if (errDiv) errDiv.classList.add('d-none');
        },

        cancelEdit() {
            this.resetFormToNewMode();

            // Връщане към таба със списъка
            const listTabBtn = document.getElementById('ai-prompts-list-tab');
            if (listTabBtn && window.bootstrap) {
                const tab = new bootstrap.Tab(listTabBtn);
                tab.show();
            }
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
            const originalBtnHtml = submitBtn ? submitBtn.innerHTML : '';
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
            .then(() => {
                this.resetFormToNewMode();
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnHtml;
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
                    submitBtn.innerHTML = originalBtnHtml;
                }
                const msg = err.response?.data?.detail || 'Грешка при запис на промпта.';
                if (errDiv) {
                    errDiv.textContent = msg;
                    errDiv.classList.remove('d-none');
                }
            });
        },

        deletePrompt(promptId) {
            const prompt = this.prompts.find(p => p.id === promptId);
            const promptName = prompt ? `"${prompt.title}"` : 'този промпт';

            if (!confirm(`Сигурни ли сте, че искате да изтриете ${promptName}?`)) {
                return;
            }

            const csrf = getCsrfToken();
            axios.delete(`/api/prompts/${promptId}/`, {
                headers: { 'X-CSRFToken': csrf }
            })
            .then(() => {
                this.prompts = this.prompts.filter(p => p.id !== promptId);
                this.expandedPromptIds.delete(promptId);
                this.updateFilterCounts();
                this.filterPrompts();
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
