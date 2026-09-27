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
            user: {},
            studentGrade: 0,
            specialtyName: '',
            studentSubjects: [],
            listOfSessions: [],
            loading: false,
            feedbackModal: {
                show: false,
            },
            selectedSessionForFeedback: null,
            feedbackForm: {
                session_id: null,
                first_name: '',
                last_name: '',
                attachment_type: 'task',
                file: null,
                errorMessage: '',
                successMessage: '',
                isSubmitting: false,
            },
        };
    },
    computed: {
        userSpecialtyText() {
            if (this.specialtyName) {
                return this.specialtyName;
            }
            if (this.user?.profile?.speciality) {
                const sp = this.user.profile.speciality;
                return `${sp.specialty_type || ''} ${sp.specialty_num || ''} - ${sp.specialty_name || ''}`.trim();
            }
            return '—';
        },
        userGradeText() {
            return this.studentGrade ? `${this.studentGrade} клас` : '—';
        }
    },
    methods: {
        toggleTheme() {
            const html = document.querySelector('html');
            if (html.getAttribute('data-theme-mode') === "dark") {
                html.setAttribute('data-theme-mode', 'light');
                html.setAttribute('data-header-styles', 'light');
                html.setAttribute('data-menu-styles', 'light');
                html.removeAttribute('data-bg-theme');
                html.removeAttribute('style');
                localStorage.removeItem("ynexdarktheme");
                localStorage.removeItem("ynexMenu");
                localStorage.removeItem("ynexHeader");
                localStorage.removeItem("bodylightRGB");
                localStorage.removeItem("bodyBgRGB");
            } else {
                html.setAttribute('data-theme-mode', 'dark');
                html.setAttribute('data-header-styles', 'dark');
                html.setAttribute('data-menu-styles', 'dark');
                localStorage.setItem("ynexdarktheme", "true");
                localStorage.setItem("ynexMenu", "dark");
                localStorage.setItem("ynexHeader", "dark");
                localStorage.removeItem("bodylightRGB");
                localStorage.removeItem("bodyBgRGB");
            }
        },
        sanitize(html) {
            if (!html) return '';
            if (window.DOMPurify) {
                return window.DOMPurify.sanitize(html);
            }
            return html;
        },
        sessionType(st) {
            switch (st) {
                case 'НЗ': return 'Нови знания';
                case 'УПР': return 'Упражнение';
                case 'ПК': return 'Проверка и контрол';
                case 'ОС': return 'Обобщаване и систематизиране';
                case 'K': return 'Комбиниран урок';
                default:  return st || '';
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
        moscowTextFor(tpc) {
            const code = tpc?.MoSCoW_cat || 'M';
            return this.moscowMap[code] || code;
        },
        getTheoryAttachments(session) {
            if (!session || !Array.isArray(session.session_attachments)) return [];
            return session.session_attachments.filter(a => a.attachment_type === 'theory');
        },
        getOtherAttachments(session) {
            if (!session || !Array.isArray(session.session_attachments)) return [];
            return session.session_attachments.filter(a => a.attachment_type !== 'theory' && (a.is_student_visible === undefined || a.is_student_visible === true || a.is_student_visible === 'true'));
        },
        attachmentTypeText(type) {
            switch (type) {
                case 'theory': return 'Теория';
                case 'worksheet': return 'Работен лист';
                case 'rubric': return 'Оценъчна карта / Чек-лист';
                case 'exit_ticket': return 'Изходен билет';
                case 'task': return 'Задача';
                case 'test': return 'Тест';
                case 'self_study': return 'Самостоятелна работа';
                case 'other': return 'Други';
                default: return 'Приложение';
            }
        },
        attachmentTypeBadgeClass(type) {
            switch (type) {
                case 'theory': return 'bg-primary-transparent text-primary';
                case 'worksheet': return 'bg-info-transparent text-info';
                case 'rubric': return 'bg-warning-transparent text-warning';
                case 'exit_ticket': return 'bg-purple-transparent text-purple';
                case 'task': return 'bg-success-transparent text-success';
                case 'test': return 'bg-danger-transparent text-danger';
                case 'self_study': return 'bg-teal-transparent text-teal';
                case 'other': return 'bg-secondary-transparent text-secondary';
                default: return 'bg-light text-muted';
            }
        },
        getPointNumNameById(session, pointId) {
            if (!session || !pointId || !Array.isArray(session.session_points)) return '';
            const p = session.session_points.find(x => x.id === pointId);
            if (!p) return '';
            return `Точка ${p.num}${p.name ? ('. ' + p.name) : ''}`;
        },
        loadUserDetails() {
            const vm = this;
            vm.loading = true;
            axios.get('/api/context/expanded/')
                .then(function(response) {
                    vm.user = response.data;
                    vm.studentGrade = Number(response.data.grade || response.data.profile?.grade || 0);

                    const specialtyId = response.data.specialty || response.data.profile?.speciality?.id || response.data.profile?.speciality;
                    if (response.data.profile?.speciality?.specialty_name) {
                        const sp = response.data.profile.speciality;
                        vm.specialtyName = `${sp.specialty_type || ''} ${sp.specialty_num || ''} - ${sp.specialty_name || ''}`.trim();
                    }

                    if (specialtyId) {
                        vm.loadSubjects(specialtyId);
                    } else {
                        vm.loading = false;
                    }
                })
                .catch(function(error) {
                    console.error('Error loading user details:', error);
                    vm.loading = false;
                });
        },
        loadSubjects(specialtyId) {
            const vm = this;
            axios.get(`/api/specialty/${specialtyId}/subjects/`)
                .then(function(response) {
                    const allSubjects = (response.data || []).slice().sort((a, b) => {
                        const nameCmp = (a?.name || '').localeCompare(b?.name || '', 'bg');
                        if (nameCmp !== 0) return nameCmp;
                        if (a?.subject_type === b?.subject_type) return 0;
                        if (a?.subject_type === 'теория') return -1;
                        if (b?.subject_type === 'теория') return 1;
                        return (a?.subject_type || '').localeCompare(b?.subject_type || '', 'bg');
                    });
                    if (vm.studentGrade && vm.studentGrade > 0) {
                        vm.studentSubjects = allSubjects.filter(sb => Number(sb.grade) === Number(vm.studentGrade));
                    } else {
                        vm.studentSubjects = allSubjects;
                    }

                    // Избор на предмет
                    const hasCurrent = vm.studentSubjects.some(sb => sb.id === vm.user.subject);
                    if (!hasCurrent && vm.studentSubjects.length > 0) {
                        vm.user.subject = vm.studentSubjects[0].id;
                    }

                    if (vm.user.subject) {
                        vm.loadSessions();
                    } else {
                        vm.listOfSessions = [];
                        vm.loading = false;
                    }
                })
                .catch(function(error) {
                    console.error('Error loading subjects:', error);
                    vm.loading = false;
                });
        },
        setSubject(subjectId) {
            const vm = this;
            vm.user.subject = subjectId;
            axios.get(`/api/subject_select/${subjectId}/`)
                .catch(function(err) {
                    console.log('Subject select error', err);
                });
            vm.loadSessions();
        },
        loadSessions() {
            const vm = this;
            if (!vm.user.subject) {
                vm.listOfSessions = [];
                vm.loading = false;
                return;
            }
            vm.loading = true;
            axios.get(`/api/subjects/${vm.user.subject}/sessions-with-topics/`)
                .then(function(response) {
                    const rawSessions = response.data || [];
                    vm.listOfSessions = rawSessions.map(session => {
                        session.collapsed = true;
                        // Инициализация на collapsed флаг за бележки, задачи, приложения
                        if (session.session_tasks) {
                            session.session_tasks.forEach(t => {
                                t.collapsed = true;
                            });
                        }
                        if (session.session_attachments) {
                            session.session_attachments.forEach(a => {
                                a.collapsed = true;
                            });
                        }
                        return session;
                    });
                    vm.loading = false;
                })
                .catch(function(error) {
                    console.error('Error loading sessions:', error);
                    vm.listOfSessions = [];
                    vm.loading = false;
                });
        },
        downloadFile(fileUrl, fileName) {
            if (!fileUrl) return;
            axios.get(fileUrl, { responseType: 'blob' })
                .then(function(response) {
                    const blobUrl = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement('a');
                    link.href = blobUrl;
                    link.setAttribute('download', fileName || 'attachment');
                    document.body.appendChild(link);
                    link.click();
                    link.remove();
                    window.URL.revokeObjectURL(blobUrl);
                })
                .catch(function(error) {
                    console.error('Грешка при сваляне на файла:', error);
                    const link = document.createElement('a');
                    link.href = fileUrl;
                    link.setAttribute('download', fileName || '');
                    link.target = '_blank';
                    document.body.appendChild(link);
                    link.click();
                    link.remove();
                });
        },
        openFeedbackModal(session) {
            this.selectedSessionForFeedback = session;
            let firstName = this.user?.first_name || '';
            let lastName = this.user?.last_name || '';
            if (!firstName && !lastName && this.user?.user_name) {
                const parts = this.user.user_name.trim().split(/\s+/);
                firstName = parts[0] || '';
                lastName = parts.slice(1).join(' ') || '';
            }
            this.feedbackForm = {
                session_id: session.id,
                first_name: firstName,
                last_name: lastName,
                attachment_type: 'task',
                file: null,
                errorMessage: '',
                successMessage: '',
                isSubmitting: false,
            };
            if (this.$refs.feedbackFileInput) {
                this.$refs.feedbackFileInput.value = '';
            }
            this.feedbackModal.show = true;
        },
        closeFeedbackModal() {
            this.feedbackModal.show = false;
            this.selectedSessionForFeedback = null;
            this.feedbackForm.errorMessage = '';
            this.feedbackForm.successMessage = '';
            this.feedbackForm.file = null;
            if (this.$refs.feedbackFileInput) {
                this.$refs.feedbackFileInput.value = '';
            }
        },
        onFeedbackFileChange(event) {
            const files = event.target.files;
            if (files && files.length > 0) {
                this.feedbackForm.file = files[0];
            } else {
                this.feedbackForm.file = null;
            }
        },
        submitFeedback() {
            const vm = this;
            if (!vm.feedbackForm.first_name || !vm.feedbackForm.first_name.trim()) {
                vm.feedbackForm.errorMessage = 'Моля, въведете име.';
                return;
            }
            if (!vm.feedbackForm.last_name || !vm.feedbackForm.last_name.trim()) {
                vm.feedbackForm.errorMessage = 'Моля, въведете фамилия.';
                return;
            }
            if (!vm.feedbackForm.file) {
                vm.feedbackForm.errorMessage = 'Моля, изберете файл за качване.';
                return;
            }

            const fullName = `${vm.feedbackForm.first_name.trim()} ${vm.feedbackForm.last_name.trim()}`.trim();
            const formData = new FormData();
            formData.append('id', 0);
            formData.append('session', vm.feedbackForm.session_id);
            formData.append('name', fullName);
            formData.append('attachment_type', vm.feedbackForm.attachment_type || 'task');
            formData.append('is_student_visible', 'false');
            formData.append('description', `Обратна връзка: ${fullName}`);
            formData.append('file', vm.feedbackForm.file);

            vm.feedbackForm.isSubmitting = true;
            vm.feedbackForm.errorMessage = '';
            vm.feedbackForm.successMessage = '';

            const headers = {
                'Content-Type': 'multipart/form-data',
            };
            if (window.CSRF_TOKEN) {
                headers['X-CSRFToken'] = window.CSRF_TOKEN;
            }

            axios.post('/api/session-attachments/upsert/', formData, { headers: headers })
                .then(function(response) {
                    vm.feedbackForm.isSubmitting = false;
                    vm.feedbackForm.successMessage = 'Обратната връзка и файлът бяха изпратени успешно!';
                    setTimeout(function() {
                        vm.closeFeedbackModal();
                    }, 1500);
                })
                .catch(function(error) {
                    vm.feedbackForm.isSubmitting = false;
                    console.error('Грешка при изпращане на обратна връзка:', error);
                    vm.feedbackForm.errorMessage = error.response?.data?.detail || error.response?.data?.error || 'Възникна грешка при качване на файла. Моля, опитайте отново.';
                });
        }
    },
    created() {
        this.loadUserDetails();
    }
};

Vue.createApp(App).mount('#main_app');

document.addEventListener('DOMContentLoaded', function () {
    const scrollToTop = document.querySelector('.scrollToTop');
    if (scrollToTop) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 100) {
                scrollToTop.style.display = 'flex';
            } else {
                scrollToTop.style.display = 'none';
            }
        });
        scrollToTop.onclick = () => {
            window.scrollTo(0, 0);
        };
    }
});
