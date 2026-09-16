const App = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            moscowMap: {
                M: 'Задължителна тема',
                S: 'Важно, но не критично',
                C: 'Пожелателно',
                W: 'Не влиза, Отпада'
            },
            listOfSpecialties: [],
            listOfSubjects: [],
            selectedGrade: 0,
            user: {},
            listOfSessions: [],
            session: {},
        }
    },
    computed: {
        filteredSubjects() {
            if (!Array.isArray(this.listOfSubjects)) return [];
            let list = this.listOfSubjects;
            if (this.selectedGrade && Number(this.selectedGrade) !== 0) {
                list = list.filter(sbj => Number(sbj.grade) === Number(this.selectedGrade));
            }
            return list.slice().sort((a, b) => {
                const nameCmp = (a?.name || '').localeCompare(b?.name || '', 'bg');
                if (nameCmp !== 0) return nameCmp;
                if (a?.subject_type === b?.subject_type) return 0;
                if (a?.subject_type === 'теория') return -1;
                if (b?.subject_type === 'теория') return 1;
                return (a?.subject_type || '').localeCompare(b?.subject_type || '', 'bg');
            });
        }
    },
    methods: {
        loadUserDetails() {
            const vm = this;
            axios.get('/api/context/')
                .then(function (response) {
                    vm.user = response.data;
                    vm.loadSpecialties(vm.user);
                    vm.loadSubjects(vm.user);
                    vm.loadSessions(vm.user);
                })
                .catch(function (error) {
                    console.error("Грешка при зареждане на потребителския контекст:", error);
                });
        },
        loadSpecialties(logged_user) {
            const vm = this;
            if (!logged_user || !logged_user.school) return;
            axios.get('/api/schools/' + logged_user.school + '/specialties/')
                .then(function (response) {
                    vm.listOfSpecialties = response.data;
                })
                .catch(function (error) {
                    console.error("Грешка при зареждане на специалности:", error);
                });
        },
        loadSubjects(logged_user) {
            const vm = this;
            if (!logged_user || !logged_user.specialty) return;
            axios.get('/api/specialty/' + logged_user.specialty + '/subjects/')
                .then(function (response) {
                    vm.listOfSubjects = response.data;
                })
                .catch(function (error) {
                    console.error("Грешка при зареждане на предмети:", error);
                });
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
                                    vm.loadSessions(vm.user);
                                }
                            } else {
                                vm.user.subject = 0;
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
                this.listOfSessions = [];
            }
        },
        setSubject(sb_id) {
            const vm = this;
            if (!sb_id) return;
            axios.get(`/api/course_set/${sb_id}/`)
                .then(res => {
                    vm.user.subject = sb_id;
                    vm.loadSessions(vm.user);
                })
                .catch(err => {
                    console.error('Грешка при избор на предмет:', err);
                    alert('Възникна грешка!');
                });
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
        moscowTextFor(topic) {
            const code = topic?.MoSCoW_cat
            return this.moscowMap[code] || code || ''
        },
        setSession(id) {
            axios.get(`/api/session_select/${id}/`)
                .then(() => {
                    window.location.href = `session_main`;
                })
                .catch(err => {
                    console.error('Грешка:', err);
                    alert('Възникна грешка!');
                });
        },
        openAIAssistant(pageKey) {
            const currentSubject = (this.listOfSubjects || []).find(s => s.id === this.user?.subject) || {};
            const currentSpec = (this.listOfSpecialties || []).find(sp => sp.id === this.user?.specialty) || {};
            const context = {
                subject: currentSubject.name || '',
                subject_name: currentSubject.name || '',
                grade: currentSubject.grade || this.user?.grade || this.selectedGrade || '',
                specialty: currentSpec.specialty_name || ''
            };
            if (window.AIPromptManager) {
                window.AIPromptManager.open(pageKey || 'session_list', context);
            }
        },
    },
    created(){
        this.loadUserDetails()
    },
}

Vue.createApp(App).mount('#main_app')
