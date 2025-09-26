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
            editMode: false,
            editForm: {
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
        isEditing(pointId) {
            return this.editMode && this.editForm.id === pointId;
        },
        sanitize(html) {
            // Премахни изображенията като доп. защита, ако желаеш:
            // return DOMPurify.sanitize(html, {FORBID_TAGS: ['img', 'svg']});
            return DOMPurify.sanitize(html);
        },

        // Create/Edit flow
        startCreatePoint() {
            this.editMode = true;
            this.editForm = {
                id: 0,
                session: this.session.id,
                num: (this.points?.length || 0) + 1,
                name: '',
                description: '',
                duration: 10,
                content: ''
            };
            this.mountEditor(this.editForm.content);
        },
        startEditPoint(p) {
            this.editMode = true;
            this.editForm = {
                id: p.id,
                session: p.session,           // идва от API; ако липсва, дай this.session.id
                num: p.num,
                name: p.name,
                description: p.description,
                duration: p.duration,
                content: p.content || ''
            };
            this.mountEditor(this.editForm.content);
        },

        // CKEditor mount/unmount
        // Save (create/update)

        async mountEditor(initialHtml) {
            await this.unmountEditor();
            await this.$nextTick();
            const el = document.getElementById('pointContentEditor');
            if (!el) return;
            this.isEditorMounting = true;
            try {
                const editor = await CKEDITOR.ClassicEditor.create(el, {
                    toolbar: [
                        'heading', '|',
                        'bold', 'italic', 'underline', 'subscript', 'superscript',
                        '|',
                        'bulletedList', 'numberedList', 'outdent', 'indent', '|',
                        'blockQuote', 'link', '|',
                        'undo', 'redo'
                    ],

                    removePlugins: [
                        // Collaboration / Premium
                        'RealTimeCollaborativeComments',
                        'RealTimeCollaborativeTrackChanges',
                        'RealTimeCollaborativeRevisionHistory',

                        'PresenceList',
                        'Comments',
                        'TrackChanges',
                        'TrackChangesData',
                        'RevisionHistory',
                        'Pagination',
                        'WProofreader',
                        'FormatPainter',
                        'SlashCommand',
                        'CaseChange',
                        'Template',

                        // Cloud / storage
                        'CKBox',
                        'CKFinder',
                        'EasyImage',

                        // Uploads / media
/*
                        'ImageUpload',
                        'ImageInsert',
                        'Base64UploadAdapter',
                        'MediaEmbedToolbar',
*/
                        // Ако не ти трябват таблици, можеш да махнеш и тях (по избор):
                        // 'Table', 'TableToolbar', 'TableProperties', 'TableCellProperties',

                        // Document Outline (причината за грешката)
                        'DocumentOutline',
                        'DocumentOutlineUI',
                        // Premium / Collaboration
                        'AIAssistant',                  // ai-invalid-license-key
                        'MultiLevelList',               // multi-level-list-invalid-license-key
                        'TableOfContents',              // table-of-contents-invalid-license-key
                        'PasteFromOfficeEnhanced',      // paste-from-office-enhanced-invalid-license-key
                    ],

                    link: {
                        decorators: {
                            addTargetToExternalLinks: {
                                mode: 'automatic',
                                callback: url => /^(https?:)?\/\//.test(url),
                                attributes: { target: '_blank', rel: 'noopener noreferrer' }
                            }
                        }
                    }
                });

                // Направи инстанцията нереактивна, за да избегнеш Vue proxy проблеми
                this._editor = markRaw(editor);

                // Задай началното съдържание
                this._editor.setData(initialHtml || '');
            } catch (e) {
                console.error('CKEditor init error:', e);
            } finally {
                this.isEditorMounting = false;
            }
        },
        async unmountEditor() {
            // ако още се инициализира – изчакай да приключи
            if (this.isEditorMounting) {
                // малък backoff; или цикъл за изчакване
                await new Promise(r => setTimeout(r, 50));
                if (this.isEditorMounting) {
                    // ако продължава, повтори кратко изчакване
                    await new Promise(r => setTimeout(r, 100));
                }
            }

            const editor = this._editor;
            if (editor) {
                try {
                    // обновяваме source елемента (textarea), ако е налично:
                    // някои версии се нуждаят от updateSourceElement преди destroy
                    await editor.destroy();
                } catch (e) {
                    console.warn('CKEditor destroy warning:', e);
                } finally {
                    this._editor = null;
                }
            }
        },
        async cancelEdit() {
            await this.unmountEditor(); // изчакай destroy да завърши
            this.editMode = false;
            this.editForm = {
                id: 0, session: null, num: 1, name: '', description: '', duration: 10, content: ''
            };
        },
        async savePoint() {
            if (this._editor) {
                this.editForm.content = this._editor.getData();
            }
            if (!this.editForm.session) this.editForm.session = this.session.id;
            if (!this.editForm.num) this.editForm.num = 1;
            if (!this.editForm.duration) this.editForm.duration = 10;

            try {
                await axios.post('/api/session-points/upsert/', this.editForm, {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': CSRF_TOKEN,
                    }
                });
                await this.unmountEditor();
                this.editMode = false;
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
        async saveNote() {
            if (this._noteEditor) this.noteForm.content = this._noteEditor.getData();
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
            if (this._taskCondEditor) this.taskForm.condition = this._taskCondEditor.getData();
            if (this._taskAnsEditor) this.taskForm.answer = this._taskAnsEditor.getData();
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

        // Editors (конфигурация с изображения според избрания вариант A или B)
        async mountNoteEditor(initialHtml) {
            await this.unmountNoteEditor();
            await this.$nextTick();
            const el = document.getElementById('noteContentEditor');
            if (!el) return;
            this.isNoteEditorMounting = true;
            try {
                const editor = await CKEDITOR.ClassicEditor.create(el, {
                    toolbar: [
                        'heading', '|',
                        'bold', 'italic', 'underline', 'subscript', 'superscript', '|',
                        'bulletedList', 'numberedList', 'outdent', 'indent', '|',
                        'blockQuote', 'link', '|', 'insertImage', '|',
                        'undo', 'redo'
                    ],
                    removePlugins: [
                        // Collaboration/cloud/premium only – keep upload/image plugins intact
                        'RealTimeCollaborativeComments','RealTimeCollaborativeTrackChanges','RealTimeCollaborativeRevisionHistory',
                        'PresenceList','Comments','TrackChanges','TrackChangesData','RevisionHistory',
                        'Pagination','WProofreader','FormatPainter','SlashCommand','CaseChange','Template',
                        'CKBox','CKFinder','EasyImage',
                        'MediaEmbedToolbar',
                        'DocumentOutline','DocumentOutlineUI',
                        'AIAssistant','MultiLevelList','TableOfContents','PasteFromOfficeEnhanced',
                    ],
                    /*
                    image: { insert: { integrations: [ 'insertImageViaUrl' ] } },
*/
                    image: {
                        insert: { integrations: [ 'uploadImage', 'insertImageViaUrl' ] },
                        toolbar: [
                            'imageStyle:inline', 'imageStyle:block', 'imageStyle:side',
                            '|', 'toggleImageCaption', 'imageTextAlternative'
                        ]
                    },
                    simpleUpload: {
                        uploadUrl: '/api/uploads/ckeditor-image/',
                        withCredentials: false,
                        headers: { 'X-CSRFToken': CSRF_TOKEN }
                    }
                });

// Debug: list plugins
                console.log('Has Image plugin:', !!editor.plugins.get('Image'));
                console.log('Has ImageUpload:', !!editor.plugins.get('ImageUpload'));
                console.log('Has ImageInsert:', !!editor.plugins.get('ImageInsert'));
                console.log('Has SimpleUploadAdapter:', !!editor.plugins.get('SimpleUploadAdapter'));


                this._noteEditor = markRaw(editor);
                this._noteEditor.setData(initialHtml || '');
            } finally {
                this.isNoteEditorMounting = false;
            }
        },
        async unmountNoteEditor() {
            if (this.isNoteEditorMounting) await new Promise(r=>setTimeout(r,50));
            if (this._noteEditor) {
                try { await this._noteEditor.destroy(); } catch(e) { console.warn(e); }
                this._noteEditor = null;
            }
        },

        async mountTaskEditors(initialCond, initialAns) {
            await this.unmountTaskEditors();
            await this.$nextTick();
            const condEl = document.getElementById('taskConditionEditor');
            const ansEl = document.getElementById('taskAnswerEditor');
            this.isTaskEditorsMounting = true;
            const config = {
                toolbar: [
                    'heading', '|',
                    'bold', 'italic', 'underline', 'subscript', 'superscript', '|',
                    'bulletedList', 'numberedList', 'outdent', 'indent', '|',
                    'blockQuote', 'link', '|', 'insertImage', '|',
                    'undo', 'redo'
                ],
                removePlugins: [
                    // Collaboration/cloud/premium only – keep upload/image plugins intact
                    'RealTimeCollaborativeComments','RealTimeCollaborativeTrackChanges','RealTimeCollaborativeRevisionHistory',
                    'PresenceList','Comments','TrackChanges','TrackChangesData','RevisionHistory',
                    'Pagination','WProofreader','FormatPainter','SlashCommand','CaseChange','Template',
                    'CKBox','CKFinder','EasyImage',
                    'MediaEmbedToolbar',
                    'DocumentOutline','DocumentOutlineUI',
                    'AIAssistant','MultiLevelList','TableOfContents','PasteFromOfficeEnhanced',
                ],
                image: {
                    insert: { integrations: [ 'uploadImage', 'insertImageViaUrl' ] },
                    toolbar: [
                        'imageStyle:inline', 'imageStyle:block', 'imageStyle:side',
                        '|', 'toggleImageCaption', 'imageTextAlternative'
                    ]
                },
                simpleUpload: {
                    uploadUrl: '/api/uploads/ckeditor-image/',
                    withCredentials: false,
                    headers: { 'X-CSRFToken': CSRF_TOKEN }
                }
            };
            try {
                if (condEl) {
                    this._taskCondEditor = markRaw(await CKEDITOR.ClassicEditor.create(condEl, config));
                    this._taskCondEditor.setData(initialCond || '');
                }
                if (ansEl) {
                    this._taskAnsEditor = markRaw(await CKEDITOR.ClassicEditor.create(ansEl, config));
                    this._taskAnsEditor.setData(initialAns || '');
                }
            } finally {
                this.isTaskEditorsMounting = false;
            }
        },
        async unmountTaskEditors() {
            if (this.isTaskEditorsMounting) await new Promise(r=>setTimeout(r,50));
            if (this._taskCondEditor) { try { await this._taskCondEditor.destroy(); } catch(e){} this._taskCondEditor = null; }
            if (this._taskAnsEditor)  { try { await this._taskAnsEditor.destroy(); }  catch(e){} this._taskAnsEditor  = null; }
        },

    },
    created: function(){
        this.loadUserDetails();
    }
}

Vue.createApp(App).mount('#main_app')
