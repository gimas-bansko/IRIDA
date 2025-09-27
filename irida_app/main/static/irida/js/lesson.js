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

            // note edit
            noteEditMode: false,
            noteForm: { id: 0, session: null, point: null, num: 1, name: '', content: '' },
            _noteEditor: null,
            isNoteEditorMounting: false,

            // task edit
            taskEditMode: false,
            taskForm: { id: 0, session: null, point: null, num: 1, name: '', condition: '', answer: '' },
            _taskCondEditor: null,
            _taskAnsEditor: null,
            isTaskEditorsMounting: false,

        }
    },
    computed: {
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
                    vm.loadSessionTasks();                })
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

        // Save create/update/save point
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
        async cancelEdit() {
            await this.unmountPointEditor(); // изчакай destroy да завърши
            await this.unmountNoteEditor(); // изчакай destroy да завърши
            await this.unmountTaskEditors(); // изчакай destroy да завърши
            this.pointEditMode = false;
            this.noteEditMode = false;
            this.taskEditMode = false;
            this.pointForm = {
                id: 0, session: null, num: 1, name: '', description: '', duration: 10, content: ''
            };
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
        // Delete
        deletePoint(p) {
            if (!confirm('Сигурни ли сте, че искате да изтриете тази точка?')) return;
            axios.delete('/api/session-points/' + p.id + '/', {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN
                }
            })
                .then(() => {
                    this.loadSessionPoints();
                })
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
                .then(res => vm.notes = res.data);
        },
        loadSessionTasks() {
            const vm = this;
            axios.get('/api/sessions/' + vm.session.id + '/tasks/')
                .then(res => vm.tasks = res.data);
        },

        // Notes CRUD
        startCreateNote(pointId = null) {
            this.noteEditMode = true;
            this.noteForm = { id: 0, session: this.session.id, point: pointId, num: (this.notes?.length||0)+1, name: '', content: '' };
            this.mountNoteEditor('');
        },
        startEditNote(n) {
            this.noteEditMode = true;
            this.noteForm = { id: n.id, session: n.session ?? this.session.id, point: n.point ?? null, num: n.num, name: n.name, content: n.content||'' };
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
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN }
                });
                await this.unmountNoteEditor();
                this.noteEditMode = false;
                await this.loadSessionNotes();
            } catch(e) {
                console.error(e); alert('Грешка при запис на бележка');
            }
        },
        deleteNote(n) {
            if (!confirm('Да се изтрие ли тази бележка?')) return;
            axios.delete('/api/session-notes/' + n.id + '/', {
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN }
            }).then(() => this.loadSessionNotes())
                .catch(err => { console.error(err); alert('Грешка при изтриване'); });
        },

        // Tasks CRUD
        startCreateTask(pointId = null) {
            this.taskEditMode = true;
            this.taskForm = { id: 0, session: this.session.id, point: pointId, num: (this.tasks?.length||0)+1, name: '', condition: '', answer: '' };
            this.mountTaskEditors('', '');
        },
        startEditTask(t) {
            this.taskEditMode = true;
            this.taskForm = {
                id: t.id, session: t.session ?? this.session.id, point: t.point ?? null,
                num: t.num, name: t.name, condition: t.condition||'', answer: t.answer||''
            };
            this.mountTaskEditors(this.taskForm.condition, this.taskForm.answer);
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
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN }
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
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN }
            }).then(() => this.loadSessionTasks())
                .catch(err => { console.error(err); alert('Грешка при изтриване'); });
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
    },
    created: function(){
        this.loadUserDetails();
    }
}

Vue.createApp(App).mount('#main_app')
