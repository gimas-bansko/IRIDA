const App = {
    delimiters: ['[[', ']]'], // Променяме синтаксиса на [[ ]]
    data() {
        return {
            moscowMap: {
                M: 'Задължителна тема',
                S: 'Важно, но не критично',
                C: 'Пожелателно',
                W: 'Не влиза, Отпада'
            },
            edit:{
                editor:false, //режима на редактиране (да/не)
                index:[-1,-1], // -1 - нов; >-1 -индекс
                level:0, // ниво 0 е външно, 1 е вътрешно
            },
            listOfSpecialties: [],
            listOfSubjects: [],
            listOfGoals: [],
            listOfUnits:[],
            user:{},
            school:{},
            subject:{
                id:0,
                name: '',
                grade: 12,
                subject_type: 'теория',
                hpy: 18,
                wpy: 0,
                hpw1: 0,
                hpw2: 0,
                },
            goal:{
                id:0,
                num:0,
                name:'',
                course:0,
            },
            unit: { id: 0, num: 1, name: '', hours: 1, subject: 0 },
            topic: { id: 0, num: 1, name: '', MoSCoW_cat: 'M', MoSCoW_rem: '', unit: 0 },
            totalHours:0,
            showAddNewUnit:false,
            listOfSessions: [],
            // текущо редактиран Session и неговите SessionTopic
            editSession: null,           // { id, course, unit, num, name, focus, goals, duration, session_topics: [...] }
            editSessionTopics: [],       // копие на session_topics за редакция (локално)
            unitsList_idx:0,
            selectedGrade: 0,
            importModalInstance: null,
            importData: {
                rawJson: '',
                replaceExisting: true,
                isSubmitting: false,
                errorMessage: '',
                modalType: 'curriculum'
            },

        }
    },
    computed: {
        currentSubject() {
            if (!this.listOfSubjects || !this.user.subject) return this.subject || {};
            return this.listOfSubjects.find(s => s.id === this.user.subject) || this.subject || {};
        },
        currentSpecialty() {
            if (!this.listOfSpecialties || !this.user.specialty) return {};
            return this.listOfSpecialties.find(sp => sp.id === this.user.specialty) || {};
        },
        currentSpecialtyType() {
            const sp = this.currentSpecialty;
            return sp?.specialty_type || 'специалност';
        },
        currentTopicMoSCoWText() {
            const code = this.topic?.MoSCoW_cat || 'M'
            return this.moscowMap[code] || code
        },
        totalExistingTopicsCount() {
            if (!Array.isArray(this.listOfUnits)) return 0;
            return this.listOfUnits.reduce((acc, u) => acc + (Array.isArray(u?.topics) ? u.topics.length : 0), 0);
        },
        filteredSubjects() {
            if (!Array.isArray(this.listOfSubjects)) return [];
            if (!this.selectedGrade || Number(this.selectedGrade) === 0) {
                return this.listOfSubjects;
            }
            return this.listOfSubjects.filter(sbj => Number(sbj.grade) === Number(this.selectedGrade));
        },
        totalHours() {
            // защита при липсващ или неинициализиран списък
            if (!Array.isArray(this.listOfUnits)) return 0;

            return this.listOfUnits.reduce((sum, u) => {
                // гарантираме числова стойност, дори ако hours е string или undefined
                const h = Number(u?.hours ?? 0);
                return sum + (isNaN(h) ? 0 : h);
            }, 0);
        },
        topicsByUnitId(id) {
            // returns a function(id) -> topics array or []
            return (id) => {
                if (!Array.isArray(this.listOfUnits)) return [];
                const idx = this.indexOfUnitById(id);
                if (idx < 0) return [];
                const unit = this.listOfUnits[idx];
                return Array.isArray(unit?.topics) ? unit.topics : [];
            };
        },
    },
    methods: {
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
        sessionTypeClass(st) {
            switch (st) {
                case 'НЗ': return 'bg-info';
                case 'УПР': return 'bg-primary';
                case 'ПК': return 'bg-secondary';
                case 'ОС': return 'bg-warning';
                case 'K': return 'bg-success';
                default:  return 'bg-info';
            }
        },
        moscowClass(tpc) {
            switch (tpc.MoSCoW_cat) {
                case 'M': return 'moscow-m';
                case 'S': return 'moscow-s';
                case 'C': return 'moscow-c';
                case 'W': return 'moscow-w';
                default:  return '';
            }
        },
        moscowTextFor(topic) {
            const code = topic?.MoSCoW_cat
            return this.moscowMap[code] || code || ''
        },
        indexOfUnitById(id) {
            return this.listOfUnits.findIndex(u => u.id === id);
        },

        // методи за показване/скриване на редактора
        setEditMode(lvl, idx_l0, idx_l1 = -1) {
            this.edit.editor = true
            this.edit.index[0] = idx_l0
            this.edit.index[1] = idx_l1
            this.edit.level = lvl
        },
        clearEditMode() {
            this.edit.editor = false
        },
        showItem(lvl, idx_l0, idx_l1 = -1) {
            let result = true
            if ((this.edit.editor) && (this.edit.level === lvl)) {
                if ((lvl === 0) && (this.edit.index[0] === idx_l0)) result = false
                if ((lvl === 1) && (this.edit.index[0] === idx_l0) && (this.edit.index[1] === idx_l1)) result = false
            }
            return result
        },
        showEditor(lvl, idx_l0, idx_l1 = -1) {
            let result = false
            if ((this.edit.editor) && (this.edit.level === lvl)) {
                if ((lvl === 0) && (this.edit.index[0] === idx_l0)) result = true
                if ((lvl === 1) && (this.edit.index[0] === idx_l0) && (this.edit.index[1] === idx_l1)) result = true
            }
            return result
        },

        sendLogRecord(txt) {
            const vm = this
            axios({
                method: 'POST',
                url: '/api/SaveLogRecord/',
                headers: {
                    'X-CSRFToken': CSRF_TOKEN,
                    //'Access-Control-Allow-Origin':'*',
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                data: {
                    action: txt,
                }
            })
        },
        loadSchool(logged_user) {
            // чета всички данни за училището на влезлия потребител
            const vm = this;
            axios.get('/api/schools/' + logged_user.school + '/')
                .then(function (response) {
                    vm.school = response.data
                })
        },
        loadUserDetails() {
            const vm = this;
            axios.get('/api/context/')
                .then(function (response) {
                    vm.user = response.data
                    vm.loadSpecialties(vm.user)
                    vm.loadSchool(vm.user)
                    vm.loadSubjects(vm.user)
                    vm.loadGoals(vm.user)
                    vm.loadUnits(vm.user)
                    vm.loadSessions(vm.user)
                })
        },
        loadSpecialties(logged_user) {
            // чета списъка на всички специалности които са от същото училище, като влезлия потребител
            const vm = this;
            axios.get('/api/schools/' + logged_user.school + '/specialties/')
                .then(function (response) {
                    vm.listOfSpecialties = response.data
                })
        },
        setSpecialty(sp_id) {
            const vm = this;
            if (!sp_id) return;
            axios.get('/api/speciality_select/' + sp_id + '/')
                .then(function (response) {
                    vm.user.specialty = sp_id;
                    axios.get('/api/specialty/' + sp_id + '/subjects/')
                        .then(function (res) {
                            vm.listOfSubjects = res.data;
                            const availableSubjects = vm.filteredSubjects;
                            if (availableSubjects && availableSubjects.length > 0) {
                                const hasCurrent = availableSubjects.some(s => s.id === vm.user.subject);
                                if (!hasCurrent) {
                                    vm.setSubject(availableSubjects[0].id);
                                } else {
                                    vm.loadGoals(vm.user);
                                    vm.loadUnits(vm.user);
                                    vm.loadSessions(vm.user);
                                }
                            } else {
                                vm.user.subject = 0;
                                vm.listOfGoals = [];
                                vm.listOfUnits = [];
                                vm.listOfSessions = [];
                            }
                        });
                })
                .catch(function (error) {
                    console.error("Грешка при смяна на специалност:", error);
                    alert("Възникна грешка при смяна на специалността!");
                });
        },
        onGradeChange() {
            const availableSubjects = this.filteredSubjects;
            if (availableSubjects && availableSubjects.length > 0) {
                const hasCurrent = availableSubjects.some(s => s.id === this.user.subject);
                if (!hasCurrent) {
                    this.setSubject(availableSubjects[0].id);
                }
            } else {
                this.user.subject = 0;
                this.listOfGoals = [];
                this.listOfUnits = [];
                this.listOfSessions = [];
            }
        },
        setSubject(sb_id) {
            const vm = this;
            if (!sb_id) return;
            axios.get('/api/subject_select/' + sb_id + '/')
                .then(function (response) {
                    vm.user.subject = sb_id;
                    vm.loadGoals(vm.user);
                    vm.loadUnits(vm.user);
                    vm.loadSessions(vm.user);
                })
                .catch(function (error) {
                    console.error("Грешка при смяна на предмет:", error);
                    alert("Възникна грешка при смяна на предмета!");
                });
        },
        loadSubjects(logged_user) {
            // чета списъка на всички предмети, които са от текущо избраната специалност за влезлия потребител
            const vm = this;
            axios.get('/api/specialty/' + logged_user.specialty + '/subjects/')
                .then(function (response) {
                    vm.listOfSubjects = response.data
                })
        },
        newSubject() {
            this.subject.id = 0
            this.subject.name = ''
            this.subject.grade = 12
            this.subject.subject_type = 'теория'
            this.subject.hpy = 18
            this.subject.wpy = 0
            this.subject.hpw1 = 0
            this.subject.hpw2 = 0
            this.setEditMode(0, -1)
        },
        editSubject(itemOrIdx) {
            let sbj = null;
            let idx = -1;
            if (typeof itemOrIdx === 'object' && itemOrIdx !== null) {
                sbj = itemOrIdx;
                idx = this.listOfSubjects.findIndex(s => s.id === sbj.id);
            } else {
                idx = itemOrIdx;
                sbj = this.listOfSubjects[idx];
            }
            if (!sbj) return;
            this.subject.id = sbj.id
            this.subject.name = sbj.name
            this.subject.grade = sbj.grade
            this.subject.subject_type = sbj.subject_type
            this.subject.hpy = sbj.hpy
            this.subject.wpy = sbj.wpy
            this.subject.hpw1 = sbj.hpw1
            this.subject.hpw2 = sbj.hpw2
            this.setEditMode(0, idx)
        },
        saveSubject() {
            const vm = this
            vm.clearEditMode()
            // Изпращане на PUT заявка към API
            axios.put('/api/specialty/' + vm.user.specialty + '/subjects/' + vm.subject.id + '/', vm.subject, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN
                }
            })
                .then(function (response) {
                    vm.loadSubjects(vm.user)
                    // Показване на съобщение за успех
                    alert("Данните са записани успешно!");
                })
                .catch(function (error) {
                    console.error("Грешка при запазване на данни:", error);
                    alert("Възникна грешка при запазване на данните!");
                });
        },
        setSubjectGoal(sb_id) {
            axios.get(`/api/course_set/${sb_id}/`)
                .then(() => {
                    window.location.href = '/goals';
                })
                .catch(err => {
                    console.error('Грешка:', err);
                    alert('Възникна грешка!');
                });
        },
        setSubjectUnit(sb_id) {
            axios.get(`/api/course_set/${sb_id}/`)
                .then(() => {
                    window.location.href = '/units';
                })
                .catch(err => {
                    console.error('Грешка:', err);
                    alert('Възникна грешка!');
                });
        },
        setSubjectSession(sb_id) {
            axios.get(`/api/course_set/${sb_id}/`)
                .then(() => {
                    window.location.href = '/lessons';
                })
                .catch(err => {
                    console.error('Грешка:', err);
                    alert('Възникна грешка!');
                });
        },
        loadGoals(logged_user) {
            // чета списъка на целите на обучението по предмета по подразбиране на текущия потребител
            const vm = this;
            if (!logged_user || !logged_user.subject) {
                vm.listOfGoals = [];
                vm.clearEditMode();
                return;
            }
            axios.get('/api/course/' + logged_user.subject + '/goals/')
                .then(function (response) {
                    vm.listOfGoals = response.data
                    vm.clearEditMode()
                })
        },
        editGoal(idx) {
            this.goal.id = this.listOfGoals[idx].id
            this.goal.num = this.listOfGoals[idx].num
            this.goal.name = this.listOfGoals[idx].name
            this.goal.course = this.listOfGoals[idx].course
            this.setEditMode(0, idx)
        },
        newGoal() {
            this.goal.id = 0
            this.goal.num = this.listOfGoals.length + 1
            this.goal.name = ''
            this.goal.course = this.user.subject
            this.setEditMode(0, -1)
        },
        saveGoal() {
            const vm = this;
            vm.clearEditMode();
            if (!vm.goal.course) {
                vm.goal.course = vm.user.subject;
            }
            // Изпращане на POST заявка към API
            axios.post('/api/goals/upsert/', vm.goal, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN
                }
            })
                .then(function (response) {
                    vm.loadGoals(vm.user)
                    // Показване на съобщение за успех
                    alert("Данните са записани успешно!");
                })
                .catch(function (error) {
                    alert("Възникна грешка при запазване на данните!");
                });
        },

        loadUnits(logged_user) {
            // чета списъка на целите на обучението по предмета по подразбиране на текущия потребител
            const vm = this;
            vm.clearEditMode();
            const subjectId = (logged_user && logged_user.subject) || vm.user.subject;
            if (!subjectId) {
                vm.listOfUnits = [];
                return;
            }
            axios.get(`/api/subjects/${subjectId}/units-with-topics/`)
                .then(function (response) {
                    vm.listOfUnits = response.data;
                })
        },
        saveUnit() {
            const vm = this;
            vm.clearEditMode()
            axios.post('/api/units/upsert/', vm.unit, {
                headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}
            })
                .then(() => {
                    // презареди списъка на units+topics за избрания предмет
                    return axios.get(`/api/subjects/${vm.user.subject}/units-with-topics/`);
                })
                .then(resp => {
                    vm.listOfUnits = resp.data; // ако държиш такъв списък

                    alert('Разделът е записан успешно!');
                })
                .catch(() => alert('Грешка при запис на раздел!'));
        },
        newUnit() {
            this.unit.id = 0
            this.unit.num = this.listOfUnits.length + 1
            this.unit.name = ''
            this.unit.hours = 1
            this.unit.subject = this.user.subject
            this.setEditMode(0, -1)
        },
        handleNewUnitClick() {
            this.newUnit();
            this.showAddNewUnit = true;
            this.$nextTick(() => {
                const el = document.getElementById('idAddNewUnit');
                if (el) {
                    el.focus();
                    el.scrollIntoView({behavior: 'smooth', block: 'start'});
                }
            });
        },
        edit_Unit(idx) {
            this.unit.id = this.listOfUnits[idx].id
            this.unit.num = this.listOfUnits[idx].num
            this.unit.name = this.listOfUnits[idx].name
            this.unit.hours = this.listOfUnits[idx].hours
            this.unit.subject = this.user.subject
            this.setEditMode(0, idx)
        },

        saveTopic() {
            const vm = this;
            vm.clearEditMode();

            const payload = {
                id: Number(vm.topic.id || 0),
                num: Number(vm.topic.num),
                name: vm.topic.name,
                MoSCoW_cat: vm.topic.MoSCoW_cat,
                MoSCoW_rem: vm.topic.MoSCoW_rem ?? '',
                unit: Number(vm.topic.unit) // гарантирано число
            };

            axios.post('/api/topics/upsert/', payload, {
                headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}
            })
                .then(() => axios.get(`/api/subjects/${vm.user.subject}/units-with-topics/`))
                .then(resp => {
                    vm.listOfUnits = resp.data;
                    alert('Темата е записана успешно!');
                })
                .catch(err => {
                    console.error('saveTopic error:', err?.response?.data || err);
                    alert('Грешка при запис на тема!');
                });
        },
        newTopic(unit_idx) {
            this.topic.id = 0
            this.topic.num = this.listOfUnits[unit_idx].topics.length + 1
            this.topic.name = ''
            this.topic.MoSCoW_cat = 'M'
            this.topic.MoSCoW_rem = ''
            this.topic.unit = this.listOfUnits[unit_idx].id
            this.setEditMode(1, unit_idx, -1)
        },
        edit_Topic(unit_idx, idx) {
            const unit = this.listOfUnits[unit_idx];
            const topic = unit.topics[idx];

            this.topic.id = topic.id;
            this.topic.num = topic.num;
            this.topic.name = topic.name;
            this.topic.MoSCoW_cat = topic.MoSCoW_cat;
            this.topic.MoSCoW_rem = topic.MoSCoW_rem;

            // Ключова промяна:
            this.topic.unit = unit.id; // не topic.unit

            this.setEditMode(1, unit_idx, idx);
        },

        getTotalHours() {
            if (!Array.isArray(this.listOfUnits)) return 0;
            return this.listOfUnits.reduce((sum, u) => {
                const h = Number(u?.hours ?? 0);
                return sum + (isNaN(h) ? 0 : h);
            }, 0);
        },
        getCurrentSubjectHPY() {
            if (!Array.isArray(this.listOfSubjects)) return null;

            // Уеднаквяване на типовете за сравнение (число)
            const targetId = Number(this.user?.subject);
            if (Number.isNaN(targetId)) return null;

            const subj = this.listOfSubjects.find(s => Number(s?.id) === targetId);
            return subj?.hpy ?? null; // връща hpy или null, ако не е намерен
        },

        loadSessions(logged_user) {
            const vm = this;
            const subjectId = (logged_user && logged_user.subject) || vm.user.subject;
            if (!subjectId) {
                vm.listOfSessions = [];
                return;
            }
            axios.get(`/api/subjects/${subjectId}/sessions-with-topics/`)
                .then(res => {
                    vm.listOfSessions = res.data;
                })
                .catch(err => {
                    console.error('loadSessions error', err?.response?.data || err);
                    alert('Грешка при зареждане на занятията');
                });
        },
        newSession() {
            const subjectId = this.user.subject;
            this.setEditMode(0, -1)
            this.editSession = {
                id: null,
                course: subjectId,
                // unit: 0,
                num: (this.listOfSessions.length ? Math.max(...this.listOfSessions.map(s => s.num)) + 1 : 1),
                name: '',
                focus: '',
                goals: '',
                duration: 1,
                // session_topics: [],
                session_type: 'НЗ',
                basic_level: true,
                collapsed: true,
            };
            this.editSessionTopics = [];
        },
        editSessionOpen(session) {
            // правим дълбоко копие, за да не променяме списъка директно
            this.setEditMode(0, -1)
            this.editSession = JSON.parse(JSON.stringify(session));
            this.editSessionTopics = JSON.parse(JSON.stringify(session.session_topics || []));
        },
        addSessionTopic() {
            this.editSessionTopics.push({
                id: null,
                description: '',
                topic: this.topicsByUnitId(this.listOfUnits[this.unitsList_idx].id)[0]//null, // за UI — ще избереш през селект; при запис ще подадем topic.id
            });
        },

        removeSessionTopic(index) {
            this.editSessionTopics.splice(index, 1);
        },
        // ако UI ти дава целия topic обект, увери се че пазиш {id, ...} вътре
        async saveSession() {
            const vm = this;
            try {
                // 1) Save Session
                let sessionPayload = {
                    course: vm.editSession.course,
                    num: vm.editSession.num,
                    name: vm.editSession.name,
                    focus: vm.editSession.focus,
                    goals: vm.editSession.goals,
                    duration: vm.editSession.duration,
                    session_type:vm.editSession.session_type,
                    basic_level:vm.editSession.basic_level,
                    collapsed:vm.editSession.collapsed,
                };

                if (!vm.editSession.id) {
                    // create
                    const res = await axios.post(`/api/sessions/`, sessionPayload, {
                        headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}
                    });
                    vm.editSession.id = res.data.id || res.data.pk || res.data; // според това какъв response връща DRF
                } else {
                    // update
                    await axios.put(`/api/sessions/${vm.editSession.id}/`, sessionPayload, {
                        headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}
                    });
                }

                // 2) Sync SessionTopics
                // Натрупваме текущите id от БД (за да знаем какво да изтрием)
                const existingIds = new Set((vm.editSession.session_topics || []).map(t => t.id).filter(Boolean));

                // 2.1 POST новите
                for (const t of vm.editSessionTopics) {
                    const isNew = !t.id || t.id === null || t.id === undefined || t.id === 0 || t.id === '0';
                    const topicId = t.topic?.id ?? t.topic; // ако държиш обект или число

                    if (isNew) {
                        if (!topicId) {
                            console.warn('skip POST: missing topicId');
                            continue;
                        }
                        const payload = { session: vm.editSession.id, topic: topicId, description: t.description || '' };
                        const resT = await axios.post(`/api/session-topics/`, payload,{
                            headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}
                        });
                        t.id = resT.data?.id;
                    }
                }

                // 2.2 PUT съществуващите
                for (const t of vm.editSessionTopics) {
                    if (t.id) {
                        const topicId = t.topic?.id ?? t.topic;
                        const payload = { session: vm.editSession.id, topic: topicId, description: t.description || '' };
                        await axios.put(`/api/session-topics/${t.id}/`, payload,{
                            headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}
                        });
                    }
                }

                // 2.3 DELETE премахнатите
                const keptIds = new Set(vm.editSessionTopics.map(x => x.id).filter(Boolean));
                for (const oldId of existingIds) {
                    if (!keptIds.has(oldId)) {
                        await axios.delete(`/api/session-topics/${oldId}/`, {
                            headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}
                        });
                    }
                }

                // 3) Refresh
                await vm.loadSessions();

                alert('Занятието е записано успешно.');
                this.clearEditMode()
            } catch (err) {
                console.error('saveSession error', err?.response?.data || err);
                alert('Грешка при запис на занятие/теми.');
            }
        },
        async deleteSession(sessionId) {
            // if (!confirm('Сигурни ли сте, че искате да изтриете занятието?')) return;
            try {
                await axios.delete(`/api/sessions/${sessionId}/`, {
                    headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}
                });
                await this.loadSessions();
            } catch (err) {
                console.error('deleteSession error', err?.response?.data || err);
                alert('Грешка при изтриване на занятие.');
            }
        },
        goToLesson(sessionId) {
            window.location.href = `/lesson/${sessionId}/`;
        },
        openAIAssistant(pageKey) {
            const currentSubject = (this.listOfSubjects || []).find(s => s.id === this.user?.subject) || this.subject || {};
            const currentSpec = (this.listOfSpecialties || []).find(sp => sp.id === this.user?.specialty) || {};
            const goalsText = (this.listOfGoals || []).map(g => `${g.num}. ${g.name}`).join('; ');

            const context = {
                subject: currentSubject.name || '',
                subject_name: currentSubject.name || '',
                grade: currentSubject.grade || this.user?.grade || this.selectedGrade || '',
                specialty: currentSpec.specialty_name || '',
                goals: goalsText
            };
            if (window.AIPromptManager) {
                window.AIPromptManager.open(pageKey || 'general', context);
            }
        },
        openImportModal(modalType = 'auto') {
            const subjectId = this.user?.subject;
            if (!subjectId) {
                alert('Моля, първо изберете учебен предмет!');
                return;
            }
            this.importData.errorMessage = '';
            this.importData.isSubmitting = false;
            this.importData.rawJson = '';

            let modalId = 'curriculumImportModal';
            if (modalType === 'goals' || (modalType === 'auto' && document.getElementById('goalsImportModal'))) {
                modalId = 'goalsImportModal';
                this.importData.modalType = 'goals';
            } else {
                modalId = 'curriculumImportModal';
                this.importData.modalType = 'curriculum';
            }

            const modalEl = document.getElementById(modalId);
            if (modalEl && window.bootstrap) {
                this.importModalInstance = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
                this.importModalInstance.show();
            }
        },
        closeImportModal() {
            if (this.importModalInstance) {
                this.importModalInstance.hide();
            }
        },
        copySampleGoalsJson() {
            const sample = [
                {
                    "num": 1,
                    "name": "Дефинира и обяснява основните концепции, синтаксис и базови структури от данни в програмния език"
                },
                {
                    "num": 2,
                    "name": "Проектира, разработва и тества модулни алгоритмични решения за практически задачи"
                },
                {
                    "num": 3,
                    "name": "Прилага добри практики за дебъгване, структуриране и документиране на програмен код"
                },
                {
                    "num": 4,
                    "name": "Изгражда завършени софтуерни модули и работи съвместно в екипна среда за разработка"
                }
            ];
            const text = JSON.stringify(sample, null, 2);
            this.importData.rawJson = text;
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).catch(() => {});
            }
        },
        copySampleJson() {
            if (this.importData.modalType === 'goals' || document.getElementById('goalsImportModal')) {
                this.copySampleGoalsJson();
                return;
            }
            const sample = [
                {
                    "num": 1,
                    "name": "Въведение и основни понятия",
                    "hours": 6,
                    "topics": [
                        {
                            "num": 1,
                            "name": "Основни концепции и терминология",
                            "MoSCoW_cat": "M",
                            "MoSCoW_rem": "Фундаментална за предмета база"
                        },
                        {
                            "num": 2,
                            "name": "Среда за разработка и инструменти",
                            "MoSCoW_cat": "M",
                            "MoSCoW_rem": "Необходима за практическата работа"
                        }
                    ]
                },
                {
                    "num": 2,
                    "name": "Практически структури и алгоритми",
                    "hours": 12,
                    "topics": [
                        {
                            "num": 1,
                            "name": "Основни алгоритмични блокове",
                            "MoSCoW_cat": "S",
                            "MoSCoW_rem": "Важни умения за програмиране"
                        },
                        {
                            "num": 2,
                            "name": "Оптимизация и разширени техники",
                            "MoSCoW_cat": "C",
                            "MoSCoW_rem": "За напреднали ученици"
                        }
                    ]
                }
            ];
            const text = JSON.stringify(sample, null, 2);
            this.importData.rawJson = text;
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).catch(() => {});
            }
        },
        handleFileUpload(event) {
            const file = event.target.files?.[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = (e) => {
                this.importData.rawJson = e.target.result;
                this.importData.errorMessage = '';
            };
            reader.onerror = () => {
                this.importData.errorMessage = 'Възникна грешка при четене на файла.';
            };
            reader.readAsText(file);
        },
        async executeImport() {
            const vm = this;
            const subjectId = vm.user?.subject;
            if (!subjectId) {
                vm.importData.errorMessage = 'Моля, изберете учебен предмет!';
                return;
            }

            const raw = (vm.importData.rawJson || '').trim();
            if (!raw) {
                vm.importData.errorMessage = 'Моля, въведете или заредете JSON данни за импорт.';
                return;
            }

            let parsedData;
            try {
                let cleanJson = raw;
                if (cleanJson.startsWith('```json')) {
                    cleanJson = cleanJson.replace(/^```json\s*/i, '').replace(/\s*```$/, '');
                } else if (cleanJson.startsWith('```')) {
                    cleanJson = cleanJson.replace(/^```\s*/, '').replace(/\s*```$/, '');
                }
                parsedData = JSON.parse(cleanJson);
            } catch (err) {
                vm.importData.errorMessage = 'Невалиден JSON синтаксис: ' + err.message;
                return;
            }

            const isGoals = vm.importData.modalType === 'goals' || !!document.getElementById('goalsImportModal');

            if (isGoals) {
                let parsedGoals = parsedData;
                if (!Array.isArray(parsedGoals)) {
                    if (parsedGoals && Array.isArray(parsedGoals.goals)) {
                        parsedGoals = parsedGoals.goals;
                    } else {
                        vm.importData.errorMessage = 'Очаква се JSON масив от цели ([ {"num": 1, "name": "..."}, ... ]).';
                        return;
                    }
                }

                if (parsedGoals.length === 0) {
                    vm.importData.errorMessage = 'JSON масивът не съдържа цели.';
                    return;
                }

                vm.importData.isSubmitting = true;
                vm.importData.errorMessage = '';

                try {
                    const response = await axios.post(`/api/subjects/${subjectId}/import-goals/`, {
                        goals: parsedGoals,
                        replace_existing: vm.importData.replaceExisting
                    }, {
                        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN }
                    });

                    if (response.data && response.data.goals) {
                        vm.listOfGoals = response.data.goals;
                    } else {
                        await vm.loadGoals(subjectId);
                    }

                    vm.closeImportModal();
                    alert(response.data?.message || 'Целите бяха импортирани успешно!');
                } catch (err) {
                    console.error('Import goals error:', err);
                    const errorMsg = err.response?.data?.error || err.response?.data?.detail || 'Възникна грешка при импорта на цели.';
                    vm.importData.errorMessage = errorMsg;
                } finally {
                    vm.importData.isSubmitting = false;
                }
            } else {
                let parsedUnits = parsedData;
                if (!Array.isArray(parsedUnits)) {
                    if (parsedUnits && Array.isArray(parsedUnits.units)) {
                        parsedUnits = parsedUnits.units;
                    } else {
                        vm.importData.errorMessage = 'Очаква ��е JSON масив от раздели ([ {...}, {...} ]).';
                        return;
                    }
                }

                if (parsedUnits.length === 0) {
                    vm.importData.errorMessage = 'JSON масивът не съдържа раздели.';
                    return;
                }

                vm.importData.isSubmitting = true;
                vm.importData.errorMessage = '';

                try {
                    const response = await axios.post(`/api/subjects/${subjectId}/import-curriculum/`, {
                        units: parsedUnits,
                        replace_existing: vm.importData.replaceExisting
                    }, {
                        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN }
                    });

                    if (response.data && response.data.units) {
                        vm.listOfUnits = response.data.units;
                    } else {
                        await vm.loadUnits(vm.user);
                    }

                    vm.closeImportModal();
                    alert(response.data?.message || 'Учебната програма бе импортирана успешно!');
                } catch (err) {
                    console.error('Import curriculum error:', err);
                    const errorMsg = err.response?.data?.error || err.response?.data?.detail || 'Възникна грешка при импорта на учебната програма.';
                    vm.importData.errorMessage = errorMsg;
                } finally {
                    vm.importData.isSubmitting = false;
                }
            }
        },
    },
    created: function(){
        this.status = 0
        this.loadUserDetails();
    }
}

Vue.createApp(App).mount('#main_app')
