// ако ползваш Vue 3 от CDN, markRaw е налично на Vue.markRaw
const markRaw = (typeof Vue !== 'undefined' && Vue.markRaw) ? Vue.markRaw : (x) => x;

const App = {
    delimiters: ['[[', ']]'], // Променяме синтаксиса на [[ ]]
    data() {
        return {
            menu_item:'План - детайли',
            user:{},
            session:{},
            topics:[],
            points:[],
            // редакция/добавяне
            pointEditMode: false,
            pointForm: {
                id: 0,
                session: null,
                num: 1,
                name: '',
                description: '',
                duration: 10,
                content: ''
            },
            isEditorMounting: false,

            moscowMap: {
                M: 'Задължителна тема',
                S: 'Важно, но не критично',
                C: 'Пожелателно',
                W: 'Не влиза, Отпада'
            },
            notes: [],
            tasks: [],
            attachments: [],

            // note edit
            noteEditMode: false,
            noteForm: { id: 0, session: null, point: null, num: 1, name: '', content: '' },
            isNoteEditorMounting: false,

            // task edit
            taskEditMode: false,
            taskForm: { id: 0, session: null, point: null, num: 1, name: '', condition: '', answer: '' },
            isTaskEditorsMounting: false,

            // attachment edit
            attachmentEditMode: false,
            attachmentForm: {
                id: 0,
                session: null,
                point: null,
                num: 1,
                name: '',
                attachment_type: 'other',
                target_format: 'original',
                file: null,
                file_url: '',
                file_name: '',
                description: ''
            },
            selectedAttachmentFile: null,
            isMarkdownFileSelected: false,

            // импорт на план
            importData: {
                showModal: false,
                isSubmitting: false,
                rawJson: '',
                replaceExisting: true,
                errorMessage: ''
            },

        }
    },
    computed: {
        theoryAttachments() {
            return (this.attachments || []).filter(a => a.attachment_type === 'theory');
        },
        otherAttachments() {
            return (this.attachments || []).filter(a => a.attachment_type === 'other' || !a.attachment_type);
        }
    },
    methods: {
        loadUserDetails() {
            const vm = this;
            axios.get('/api/context/expanded/')
                .then(function (response) {
                    vm.user = response.data
                    vm.session = response.data.profile.session
                    vm.loadSessionTopics()
                    vm.loadSessionPoints()
                    vm.loadSessionNotes();
                    vm.loadSessionTasks();
                    vm.loadSessionAttachments();
                })
        },
        loadSessionTopics() {
            // чета списъка на всички теми, включени в дадено занятие
            const vm = this;
            axios.get('/api/sessions/' + vm.session.id + '/topics/')
                .then(function (response) {
                    vm.topics = response.data
                })
        },
        loadSessionPoints() {
            const vm = this;
            axios.get('/api/sessions/' + vm.session.id + '/points/')
                .then(function (response) {
                    vm.points = response.data
                })
        },
        moscowTextFor(topic) {
            const code = topic?.MoSCoW_cat
            return this.moscowMap[code] || code || ''
        },
        sessionType(st) {
            switch (st) {
                case 'НЗ': return 'Нови знания';
                case 'УПР': return 'Упражнение';
                case 'ПК': return 'Проверка и контрол';
                case 'ОС': return 'Обобщаване и систематизиране';
                case 'K': return 'Комбиниран урок';
                default:  return '';
            }
        },

        // UI helpers
        isPointEditing(pointId) {
            return this.pointEditMode && this.pointForm.id === pointId;
        },
        sanitize(html) {
            // Премахни изображенията като доп. защита, ако желаеш:
            // return DOMPurify.sanitize(html, {FORBID_TAGS: ['img', 'svg']});
            return DOMPurify.sanitize(html);
        },
        async cancelEdit() {
            await this.unmountPointEditor(); // изчакай destroy да завърши
            await this.unmountNoteEditor(); // изчакай destroy да завърши
            await this.unmountTaskEditors(); // изчакай destroy да завърши
            this.pointEditMode = false;
            this.noteEditMode = false;
            this.taskEditMode = false;
            this.attachmentEditMode = false;
            this.selectedAttachmentFile = null;
            this.pointForm = {
                id: 0, session: null, num: 1, name: '', description: '', duration: 10, content: ''
            };
        },

        // Point --- create/update/save
        startCreatePoint() {
            this.pointEditMode = true;
            this.pointForm = {
                id: 0,
                session: this.session.id,
                num: (this.points?.length || 0) + 1,
                name: '',
                description: '',
                duration: 10,
                content: ''
            };
            this.mountPointEditor(this.pointForm.content);
        },
        startEditPoint(p) {
            this.pointEditMode = true;
            this.pointForm = {
                id: p.id,
                session: p.session,           // идва от API; ако липсва, дай this.session.id
                num: p.num,
                name: p.name,
                description: p.description,
                duration: p.duration,
                content: p.content || ''
            };
            this.mountPointEditor(this.pointForm.content);
        },
        async mountPointEditor(initialHtml) {
            await this.unmountPointEditor();
            await this.$nextTick();
            const selector = '#pointContentEditor';
            this._pointEditor = await this.initTiny(selector, initialHtml, (html) => {
                this.pointForm.content = html;
            });
        },
        async unmountPointEditor() {
            if (this._pointEditor) {
                await this.destroyTiny(this._pointEditor);
                this._pointEditor = null;
            }
        },
        async savePoint() {
            if (this._pointEditor) {
                this.pointForm.content = this._pointEditor.getContent ? this._pointEditor.getContent() : this.pointForm.content;
            }
            if (!this.pointForm.session) this.pointForm.session = this.session.id;
            if (!this.pointForm.num) this.pointForm.num = 1;
            if (!this.pointForm.duration) this.pointForm.duration = 10;

            try {
                await axios.post('/api/session-points/upsert/', this.pointForm, {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': CSRF_TOKEN,
                    }
                });
                await this.unmountPointEditor();
                this.pointEditMode = false;
                await this.loadSessionPoints();
            } catch (e) {
                console.error(e);
                alert('Грешка при запис на точка');
            }
        },
        deletePoint(p) {
            if (!confirm('Сигурни ли сте, че искате да изтриете тази точка?')) return;
            axios.delete('/api/session-points/' + p.id + '/', {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN
                }
            })
                .then(() => {this.loadSessionPoints();})
                .catch(err => {
                    console.error(err);
                    alert('Грешка при изтриване');
                });
        },
        getTotalMinutes() {
            if (!Array.isArray(this.points)) return 0;
            return this.points.reduce((sum, u) => {
                const m = Number(u?.duration ?? 0);
                return sum + (isNaN(m) ? 0 : m);
            }, 0);
        },
        checkTiming(){
            console.log(this.session.duration*45-this.getTotalMinutes())
            return this.session.duration*45-this.getTotalMinutes()
        },
//*******************************************************
        // Loaders
        loadSessionNotes() {
            const vm = this;
            axios.get('/api/sessions/' + vm.session.id + '/notes/')
                .then(res => {
                    vm.notes = res.data
                    vm.addCollapsedToNotes();
                });
        },
        loadSessionTasks() {
            const vm = this;
            axios.get('/api/sessions/' + vm.session.id + '/tasks/')
                .then(res => {
                    vm.tasks = res.data;
                    vm.addCollapsedToTasks();
                });
        },
        loadSessionAttachments() {
            const vm = this;
            axios.get('/api/sessions/' + vm.session.id + '/attachments/')
                .then(res => {
                    vm.attachments = res.data;
                    vm.addCollapsedToAttachments();
                });
        },

        // Notes
        addCollapsedToNotes() {
            if (!Array.isArray(this.notes)) return;
            for (const n of this.notes) {
                if (n && typeof n === 'object' && !Object.prototype.hasOwnProperty.call(n, 'collapsed')) {
                    n.collapsed = true;
                }
            }
        },
        getPointNumNameById(id) {
            if (!Array.isArray(this.points) || id == null) return null;
            const pointId = Number(id);
            const p = this.points.find(pt => Number(pt.id) === pointId);
            if (!p) return null;
            return `към точка ${p.num}. ${p.name}`
        },
        startCreateNote(pointId = null) {
            this.noteEditMode = true;
            this.noteForm = {
                id: 0,
                session: this.session.id,
                point: pointId, num: (this.notes?.length||0)+1,
                name: '',
                content: ''
            };
            this.mountNoteEditor(this.noteForm.content);
        },
        startEditNote(n) {
            this.noteEditMode = true;
            this.noteForm = {
                id: n.id,
                session: n.session ?? this.session.id,
                point: n.point ?? null,
                num: n.num,
                name: n.name,
                content: n.content||''
            };
            this.mountNoteEditor(this.noteForm.content);
        },
        async mountNoteEditor(initialHtml) {
            console.log('Mount note start');
            await this.unmountNoteEditor();
            await this.$nextTick();
            console.log('After nextTick');

            const selector = '#noteContentEditor';
            this._noteEditor = await this.initTiny(selector, initialHtml, (html) => {
                this.noteForm.content = html;
            });
            console.log('Tiny mounted');
        },
        async unmountNoteEditor() {
            if (this._noteEditor) {
                await this.destroyTiny(this._noteEditor);
                this._noteEditor = null;
            }
        },
        async saveNote() {
            if (this._noteEditor) {
                this.noteForm.content = this._noteEditor.getContent ? this._noteEditor.getContent() : this.noteForm.content;
            }
            if (!this.noteForm.session) this.noteForm.session = this.session.id;
            try {
                await axios.post('/api/session-notes/upsert/', this.noteForm, {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': CSRF_TOKEN
                    }
                });
                await this.unmountNoteEditor();
                this.noteEditMode = false;
                await this.loadSessionNotes();
            } catch(e) {
                console.error(e);
                alert('Грешка при запис на бележка');
            }
        },
        deleteNote(n) {
            if (!confirm('Да се изтрие ли тази бележка?')) return;
            axios.delete('/api/session-notes/' + n.id + '/', {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN
                }
            })
                .then(() => {this.loadSessionNotes();})
                .catch(err => {
                    console.error(err);
                    alert('Грешка при изтриване');
                });
        },

        // Tasks
        addCollapsedToTasks() {
            if (!Array.isArray(this.notes)) return;
            for (const n of this.tasks) {
                if (n && typeof n === 'object' && !Object.prototype.hasOwnProperty.call(n, 'collapsed')) {
                    n.collapsed = true;
                }
            }
        },
        startCreateTask(pointId = null) {
            this.taskEditMode = true;
            this.taskForm = {
                id: 0,
                session: this.session.id,
                point: pointId,
                num: (this.tasks?.length||0)+1, name: '',
                condition: '',
                answer: ''
            };
            this.mountTaskEditors('', '');
        },
        startEditTask(t) {
            this.taskEditMode = true;
            this.taskForm = {
                id: t.id,
                session: t.session ?? this.session.id,
                point: t.point ?? null,
                num: t.num,
                name: t.name,
                condition: t.condition||'',
                answer: t.answer||''
            };
            this.mountTaskEditors(this.taskForm.condition, this.taskForm.answer);
        },
        async mountTaskEditors(initialCond, initialAns) {
            await this.unmountTaskEditors();
            await this.$nextTick();

            this._taskCondEditor = await this.initTiny('#taskConditionEditor', initialCond, (html) => {
                this.taskForm.condition = html;
            });

            this._taskAnsEditor = await this.initTiny('#taskAnswerEditor', initialAns, (html) => {
                this.taskForm.answer = html;
            });
        },
        async unmountTaskEditors() {
            if (this._taskCondEditor) {
                await this.destroyTiny(this._taskCondEditor);
                this._taskCondEditor = null;
            }
            if (this._taskAnsEditor) {
                await this.destroyTiny(this._taskAnsEditor);
                this._taskAnsEditor = null;
            }
        },
        async saveTask() {
            if (this._taskCondEditor) {
                this.taskForm.condition = this._taskCondEditor.getContent ? this._taskCondEditor.getContent() : this.taskForm.condition;
            }
            if (this._taskAnsEditor) {
                this.taskForm.answer = this._taskAnsEditor.getContent ? this._taskAnsEditor.getContent() : this.taskForm.answer;
            }
            if (!this.taskForm.session) this.taskForm.session = this.session.id;
            try {
                await axios.post('/api/session-tasks/upsert/', this.taskForm, {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': CSRF_TOKEN
                    }
                });
                await this.unmountTaskEditors();
                this.taskEditMode = false;
                await this.loadSessionTasks();
            } catch(e) {
                console.error(e); alert('Грешка при запис на задача');
            }
        },
        deleteTask(t) {
            if (!confirm('Да се изтрие ли тази задача?')) return;
            axios.delete('/api/session-tasks/' + t.id + '/', {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN
                }
            })
                .then(() => this.loadSessionTasks())
                .catch(err => {
                    console.error(err);
                    alert('Грешка при изтриване');
                });
        },

        // Attachments
        addCollapsedToAttachments() {
            if (!Array.isArray(this.attachments)) return;
            for (const a of this.attachments) {
                if (a && typeof a === 'object' && !Object.prototype.hasOwnProperty.call(a, 'collapsed')) {
                    a.collapsed = true;
                }
            }
        },
        startCreateAttachment(type = 'other', pointId = null) {
            this.attachmentEditMode = true;
            this.selectedAttachmentFile = null;
            this.isMarkdownFileSelected = false;
            const itemsInGroup = type === 'theory' ? this.theoryAttachments : this.otherAttachments;
            this.attachmentForm = {
                id: 0,
                session: this.session.id,
                point: pointId,
                num: (itemsInGroup?.length || 0) + 1,
                name: '',
                attachment_type: type,
                target_format: 'original',
                file: null,
                file_url: '',
                file_name: '',
                description: ''
            };
        },
        startEditAttachment(a) {
            this.attachmentEditMode = true;
            this.selectedAttachmentFile = null;
            this.isMarkdownFileSelected = false;
            this.attachmentForm = {
                id: a.id,
                session: a.session ?? this.session.id,
                point: a.point ?? null,
                num: a.num,
                name: a.name || '',
                attachment_type: a.attachment_type || 'other',
                target_format: 'original',
                file: null,
                file_url: a.file_url || '',
                file_name: a.file_name || '',
                description: a.description || ''
            };
        },
        onAttachmentFileChange(event) {
            const file = event.target.files[0];
            if (file) {
                this.selectedAttachmentFile = file;
                const isMd = file.name.toLowerCase().endsWith('.md') || file.name.toLowerCase().endsWith('.markdown');
                this.isMarkdownFileSelected = isMd;
                if (isMd) {
                    if (!this.attachmentForm.target_format || this.attachmentForm.target_format === 'original') {
                        this.attachmentForm.target_format = 'docx';
                    }
                } else {
                    this.attachmentForm.target_format = 'original';
                }

                if (!this.attachmentForm.name) {
                    const baseName = file.name.replace(/\.(md|markdown)$/i, '');
                    if (isMd && this.attachmentForm.target_format === 'docx') {
                        this.attachmentForm.name = baseName + '.docx';
                    } else if (isMd && this.attachmentForm.target_format === 'pdf') {
                        this.attachmentForm.name = baseName + '.pdf';
                    } else {
                        this.attachmentForm.name = file.name;
                    }
                } else if (isMd) {
                    this.onTargetFormatChange();
                }
            } else {
                this.selectedAttachmentFile = null;
                this.isMarkdownFileSelected = false;
                this.attachmentForm.target_format = 'original';
            }
        },
        onTargetFormatChange() {
            if (!this.attachmentForm.name) return;
            const baseName = this.attachmentForm.name.replace(/\.(md|markdown|docx|pdf)$/i, '');
            if (this.attachmentForm.target_format === 'docx') {
                this.attachmentForm.name = baseName + '.docx';
            } else if (this.attachmentForm.target_format === 'pdf') {
                this.attachmentForm.name = baseName + '.pdf';
            } else if (this.attachmentForm.target_format === 'original') {
                this.attachmentForm.name = baseName + '.md';
            }
        },
        async saveAttachment() {
            if (!this.attachmentForm.session) this.attachmentForm.session = this.session.id;
            try {
                const formData = new FormData();
                formData.append('id', this.attachmentForm.id || 0);
                formData.append('session', this.attachmentForm.session);
                if (this.attachmentForm.point !== null && this.attachmentForm.point !== undefined && this.attachmentForm.point !== '') {
                    formData.append('point', this.attachmentForm.point);
                } else {
                    formData.append('point', '');
                }
                formData.append('num', this.attachmentForm.num || 1);
                formData.append('name', this.attachmentForm.name || '');
                formData.append('attachment_type', this.attachmentForm.attachment_type || 'other');
                formData.append('description', this.attachmentForm.description || '');
                if (this.selectedAttachmentFile) {
                    formData.append('file', this.selectedAttachmentFile);
                    if (this.isMarkdownFileSelected && this.attachmentForm.target_format) {
                        formData.append('target_format', this.attachmentForm.target_format);
                    }
                }

                await axios.post('/api/session-attachments/upsert/', formData, {
                    headers: {
                        'X-CSRFToken': CSRF_TOKEN
                    }
                });
                this.attachmentEditMode = false;
                this.selectedAttachmentFile = null;
                this.isMarkdownFileSelected = false;
                await this.loadSessionAttachments();
            } catch(e) {
                console.error(e);
                let errorDetail = e.response?.data?.detail || e.response?.data?.error;
                if (!errorDetail && e.response?.data && typeof e.response.data === 'object') {
                    const errors = Object.values(e.response.data).flat();
                    if (errors.length > 0) {
                        errorDetail = errors.join('; ');
                    }
                }
                alert(errorDetail || 'Грешка при запис на файл/приложение');
            }
        },
        cancelAttachmentEdit() {
            this.attachmentEditMode = false;
            this.selectedAttachmentFile = null;
            this.isMarkdownFileSelected = false;
        },
        deleteAttachment(a) {
            if (!confirm('Да се изтрие ли този прикачен файл?')) return;
            axios.delete('/api/session-attachments/' + a.id + '/', {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN
                }
            })
                .then(() => { this.loadSessionAttachments(); })
                .catch(err => {
                    console.error(err);
                    alert('Грешка при изтриване');
                });
        },


        initTiny(targetOrSelector, initialHtml = '', onChange) {
            console.log('initTiny', targetOrSelector);
            return new Promise((resolve, reject) => {
                // 1) Resolve target element early
                const tmpConfig = typeof targetOrSelector === 'string'
                    ? { selector: targetOrSelector }
                    : { ...targetOrSelector };

                const targetEl = tmpConfig.target || null;

                const baseConfig = {
                    menubar: false,
                    plugins: 'link lists image table code',
                    toolbar: 'undo redo | styles | bold italic underline | alignleft aligncenter alignright | bullist numlist | link image | table | code',
                    height: 300,
                    branding: false,
                    id: targetEl?.id || undefined,
                    relative_urls: false,
                    remove_script_host: false,
                    convert_urls: false,
                    document_base_url: window.location.origin + '/',
                    images_upload_handler: async (blobInfo, progress) => {
                        const form = new FormData();
                        form.append('file', blobInfo.blob(), blobInfo.filename());
                        const resp = await fetch('/api/uploads/tinymce-image/', {
                            method: 'POST',
                            body: form,
                            headers: { 'X-CSRFToken': CSRF_TOKEN }
                        });
                        if (!resp.ok) throw new Error('Upload failed');
                        const data = await resp.json();
                        return data.location || data.url;
                    },
                    setup: (editor) => {
                        editor.on('init', () => {
                            editor.setContent(initialHtml || '');
                            resolve(editor);
                        });
                        editor.on('change keyup undo redo input', () => {
                            onChange && onChange(editor.getContent());
                        });
                    }
                };

                const config = typeof targetOrSelector === 'string'
                    ? { ...baseConfig, selector: targetOrSelector }
                    : { ...baseConfig, ...targetOrSelector };

                // 2) Deep cleanup before init
                try {
                    // By id
                    if (config.id) {
                        const byId = tinymce?.get?.(config.id);
                        if (byId) { try { byId.remove(); } catch {} }
                    }
                    // By matching target element (paranoid sweep)
                    if (targetEl) {
                        const editors = (tinymce?.EditorManager?.editors || []).slice();
                        for (const ed of editors) {
                            // ed.getElement() returns the original target element (textarea)
                            if (ed && !ed.destroyed && ed.getElement && ed.getElement() === targetEl) {
                                try { ed.remove(); } catch {}
                            }
                        }
                    }
                } catch (e) {
                    console.warn('Tiny pre-clean error:', e);
                }

                // 3) Let DOM settle for a frame after clone/replace
                const nextFrame = typeof requestAnimationFrame === 'function'
                    ? (cb) => requestAnimationFrame(() => cb())
                    : (cb) => setTimeout(cb, 0);

                nextFrame(() => {
                    try {
                        tinymce.init(config).catch(reject);
                    } catch (e) {
                        reject(e);
                    }
                });
            });
        },

        destroyTiny(editor) {
            return new Promise((resolve) => {
                try {
                    if (editor && !editor.destroyed) {
                        // remove() е синхронен за v8, но все пак обграждаме в try/catch
                        editor.remove();
                    }
                } catch (e) {
                    console.warn('Tiny remove error (safe to ignore):', e);
                }
                finally {
                    const eid = editor?.id;
                    if (eid) {
                        const maybe = tinymce?.get?.(eid);
                        if (maybe) { try { maybe.remove(); } catch {} }
                    }
                    resolve();
                }
            });
        },

        openAIAssistant() {
            const pointsText = (this.points || []).map(p => `${p.num}. ${p.name} (${p.duration} мин.)`).join('; ');
            const subjectObj = this.user?.profile?.subject || {};
            const specObj = this.user?.profile?.speciality || {};
            const subjectName = subjectObj.name || (document.querySelector('h1.page-title') ? document.querySelector('h1.page-title').textContent.replace('предмет:', '').trim() : '');
            const specName = specObj.specialty_name || (document.querySelector('h2.page-title') ? document.querySelector('h2.page-title').textContent.replace('специалност/професия:', '').trim() : '');
            const grade = subjectObj.grade || this.user?.profile?.grade || this.user?.grade || '';
            const durationHours = this.session?.duration || 1;
            const durationMins = durationHours * 45;
            const sessionTypeText = this.sessionType(this.session?.session_type) || this.session?.session_type || 'Нови знания';
            const topicsText = (this.topics || []).map(t => `- ${t.topic?.name || ''} [${t.topic?.MoSCoW_cat || 'M'} - ${this.moscowTextFor(t.topic)}]${t.description ? ' (' + t.description + ')' : ''}`).join('\n');

            const context = {
                subject: subjectName,
                subject_name: subjectName,
                specialty: specName,
                specialty_name: specName,
                grade: grade,
                topic: this.session?.name || '',
                session_num: this.session?.num || '',
                session_name: this.session?.name || '',
                session_type: sessionTypeText,
                duration_hours: `${durationHours} ${durationHours === 1 ? 'учебен час' : 'учебни часа'}`,
                duration_mins: `${durationMins} минути`,
                goals: this.session?.goals || '',
                focus: this.session?.focus || '',
                topics_list: topicsText || '[няма въведени теми]',
                points: pointsText || '[няма въведени точки]'
            };
            if (window.AIPromptManager) {
                window.AIPromptManager.open('lesson_main', context);
            }
        },

        // Методи за импорт на детайлен план на урок
        openPlanImportModal() {
            this.importData.showModal = true;
            this.importData.errorMessage = '';
            this.importData.rawJson = '';
            this.importData.replaceExisting = true;
            this.importData.isSubmitting = false;
        },

        closePlanImportModal() {
            this.importData.showModal = false;
            this.importData.errorMessage = '';
            this.importData.isSubmitting = false;
        },

        handleImportFileUpload(event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = (e) => {
                this.importData.rawJson = e.target.result;
            };
            reader.onerror = () => {
                this.importData.errorMessage = 'Грешка при четене на файла.';
            };
            reader.readAsText(file);
        },

        loadSamplePlanJson() {
            const sampleObj = {
                "goals": "1. Разпознава и обяснява основните концепции и синтаксис;\n2. Създава и тества работещ код по зададени изисквания;\n3. Анализира и отстранява грешки при изпълнение.",
                "focus": "Среда за разработка (PyCharm/Git), базов синтаксис, дебъгване и конзолен вход/изход.",
                "points": [
                    {
                        "num": 1,
                        "name": "Bridge-In: Въведение и софтуерен казус",
                        "description": "Въведение и мотивация",
                        "duration": 5,
                        "content": "<p>Поставяне на проблема чрез реален софтуерен казус от практиката и преговор на входните знания.</p>"
                    },
                    {
                        "num": 2,
                        "name": "Outcomes: Обявяване на очакваните резултати",
                        "description": "Цели и очаквани резултати",
                        "duration": 5,
                        "content": "<p>Обявяване на конкретните практически умения и компетентности, които ще бъдат усвоени в занятието.</p>"
                    },
                    {
                        "num": 3,
                        "name": "Презентация и демонстрация на демо код",
                        "description": "GRR: Директно обучение (Аз правя)",
                        "duration": 15,
                        "content": "<p>Преподаване на новите синтактични концепции и показване на демо код на живо в средата за разработка.</p>"
                    },
                    {
                        "num": 4,
                        "name": "Дискусия и рефлексия",
                        "description": "Въпроси за разбиране",
                        "duration": 7,
                        "content": "<p>Кратка дискусия с учениците, проверка на разбирането и отговори на възникнали въпроси.</p>"
                    },
                    {
                        "num": 5,
                        "name": "Съвместно упражнение",
                        "description": "GRR: Ръководена практика (Ние правим заедно)",
                        "duration": 8,
                        "content": "<p>Съвместно разработване на примерен софтуерен модул на дъската и екрана заедно с учениците.</p>"
                    },
                    {
                        "num": 6,
                        "name": "Самостоятелна практика",
                        "description": "GRR: Самостоятелна работа (Ти правиш сам)",
                        "duration": 25,
                        "content": "<p>Учениците работят индивидуално по поставената задача; диференцирана подкрепа от учителя.</p>"
                    },
                    {
                        "num": 7,
                        "name": "Проверка и споделяне на решения",
                        "description": "Демонстрация и анализ",
                        "duration": 10,
                        "content": "<p>Демонстрация на решения на екран от ученици, анализ на добри практики и оптимизации.</p>"
                    },
                    {
                        "num": 8,
                        "name": "Мини-викторина (Post-Assessment)",
                        "description": "Проверка на усвояването",
                        "duration": 7,
                        "content": "<p>3-4 кратки въпроса за моментална проверка на постигнатите резу��тати от занятието.</p>"
                    },
                    {
                        "num": 9,
                        "name": "Обобщение и поставяне на домашно",
                        "description": "Summary & Домашна работа",
                        "duration": 8,
                        "content": "<p>Синтезирано обобщение на ключовите изводи и възлагане на задача за самостоятелно упражнение вкъщи.</p>"
                    }
                ],
                "notes": [
                    {
                        "num": 1,
                        "name": "Теоретичен конспект и демо код",
                        "point_num": 3,
                        "content": "<p><strong>Основни концепции и синтаксис:</strong></p><pre><code># Пример за чист демо код\ndef main():\n    print('Hello, IRIDA!')\n\nif __name__ == '__main__':\n    main()</code></pre>"
                    }
                ],
                "tasks": [
                    {
                        "num": 1,
                        "name": "Съвместна задача (Ръководена практика)",
                        "point_num": 5,
                        "condition": "<p>Напишете програма съвместно с учителя, която изчислява периметър и лице на правоъгълник.</p>",
                        "answer": "<pre><code>a = float(input('a = '))\nb = float(input('b = '))\nprint('P =', 2 * (a + b))\nprint('S =', a * b)</code></pre>"
                    },
                    {
                        "num": 2,
                        "name": "Самостоятелна практическа задача",
                        "point_num": 6,
                        "condition": "<p>Разширете програмата, така че да проверява за положителни стойности на страните и да извежда форматиран резултат.</p>",
                        "answer": "<pre><code>if a > 0 and b > 0:\n    print(f'Лице: {a * b:.2f}')\nelse:\n    print('Невалидни страни!')</code></pre>"
                    },
                    {
                        "num": 3,
                        "name": "Мини-викторина за самопроверка",
                        "point_num": 8,
                        "condition": "<p>1. Кой тип данни се използва за цели числа?<br>2. Как се отпечатва текст в конзолата?</p>",
                        "answer": "<p>1. int<br>2. Чрез функцията print()</p>"
                    },
                    {
                        "num": 4,
                        "name": "Домашна работа / Предизвикателство",
                        "point_num": 9,
                        "condition": "<p>Създайте конзолен калкулатор за изчисляване на площ на триъгълник по формула на Херон.</p>",
                        "answer": "<p>Приложете формулата с math.sqrt() и валидирайте неравенството на триъгълника.</p>"
                    }
                ]
            };
            this.importData.rawJson = JSON.stringify(sampleObj, null, 2);
            this.importData.errorMessage = '';
        },

        executePlanImport() {
            const vm = this;
            if (!vm.importData.rawJson.trim()) {
                vm.importData.errorMessage = 'Моля, въведете JSON съдържание или заредете от файл.';
                return;
            }

            let parsed;
            try {
                let cleanText = vm.importData.rawJson.trim();
                if (cleanText.startsWith('```')) {
                    cleanText = cleanText.replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/, '');
                }
                parsed = JSON.parse(cleanText);
            } catch (e) {
                vm.importData.errorMessage = 'Невалиден JSON синтаксис: ' + e.message;
                return;
            }

            vm.importData.isSubmitting = true;
            vm.importData.errorMessage = '';

            const payload = {
                replace_existing: vm.importData.replaceExisting,
                plan: parsed
            };

            const csrf = window.CSRF_TOKEN || (function (name) {
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
            })('csrftoken') || '';

            axios.post('/api/sessions/' + vm.session.id + '/import-plan/', payload, {
                headers: {
                    'X-CSRFToken': csrf,
                    'Content-Type': 'application/json'
                }
            })
            .then(function (res) {
                vm.importData.isSubmitting = false;
                vm.importData.showModal = false;
                vm.importData.rawJson = '';

                if (res.data.points) vm.points = res.data.points;
                if (res.data.notes) vm.notes = res.data.notes;
                if (res.data.tasks) vm.tasks = res.data.tasks;
                if (res.data.session) {
                    vm.session.goals = res.data.session.goals;
                    vm.session.focus = res.data.session.focus;
                }

                alert(res.data.message || 'Планът на занятието беше импортиран успешно!');
            })
            .catch(function (err) {
                vm.importData.isSubmitting = false;
                console.error('Plan import error:', err);
                const msg = err.response?.data?.detail || err.response?.data?.message || 'Възникна грешка при импортирането на плана.';
                vm.importData.errorMessage = msg;
            });
        },
    },
    created: function(){
        this.loadUserDetails();
    }
}

Vue.createApp(App).mount('#main_app')
