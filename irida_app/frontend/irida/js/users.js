const App = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            edit: {
                editor: false,
                admin: false,
                teacher: false,
                student: false,
            },
            user: {},             // текущ логнат контекст от /api/context/
            listOfUsers: [],
            listOfSpecialties: [],
            numAdmins: 0,
            numTeachers: 0,
            numStudents: 0,

            // форма за create/update
            formMode: 'create',   // 'create' | 'edit'
            formUserId: 0,
            formChangePassword: false,
            form: {
                username: '',
                password: '',        // за edit може да е празно (без промяна)
                password2: '',       // за edit може да е празно (без промяна)
                email: '',
                first_name: '',
                last_name: '',
                userprofile: {
                    gender: true,
                    school: null,
                    access_level: 5,       // по подразбиране ученик
                    session_screen: 1,
                    session: null,
                    grade: 11,
                    section: 'а',
                    speciality: null,
                    subject: null,
                }
            },
            groupedStudents: {}, // { [grade]: { [section]: [users...] } }
        }
    },
    computed: {
        userValidation() {
            // ВРЪЩА САМО ИЗЧИСЛЕНИ ДАННИ, БЕЗ ДА ПИПА DATA
            // Казусите са за 'create'; при 'edit' паролата може да е празна (без смяна)
            if (this.form.username.trim().length < 3) {
                return { valid: false, msg: 'Потребителското име не може да бъде по-малко от 3 символа' };
            }
            if (this.formMode === 'create' && this.form.password.length < 3) {
                return { valid: false, msg: 'Паролата не може да бъде по-малко от 3 символа' };
            }
            if (this.formMode === 'create' && this.form.password !== this.form.password2) {
                return { valid: false, msg: 'Паролата и повторното ѝ изписване трябва да съвпадат' };
            }
            return { valid: true, msg: '' };
        },
        // За удобство: бързи гетъри
        userOK() {
            return this.userValidation.valid;
        },
        userErrorMsg() {
            return this.userValidation.msg;
        },
        editorHeader(){
            let txt =''
            if (this.formMode === 'create') {
                txt = 'Добавяне на '}
            else {txt = 'Редактиране на '}
            if (this.edit.admin) {txt = txt + 'администратор'}
            if (this.edit.teacher) {txt = txt + 'учител'}
            if (this.edit.student) {txt = txt + 'ученик'}
            return txt;
        }
    },
    methods: {
        loadUserDetails() {
            const vm = this;
            axios.get('/api/context/')
                .then(function (response) {
                    vm.user = response.data;
                    vm.loadSpecialties(vm.user);
                    vm.loadUsers();
                })
                .catch(function (error) {
                    console.error('Грешка при зареждане на потребителски контекст:', error);
                });
        },
        loadUsers(){
            const vm = this;
            const schoolId = (vm.user && vm.user.school) ? vm.user.school : 0;
            const levelNum = (vm.user && vm.user.user_level_num) ? vm.user.user_level_num : 1;
            axios.get('/api/users-list/' + schoolId + '/' + levelNum + '/')
                .then(function(response){
                    vm.listOfUsers = response.data || [];
                    vm.recount();
                    vm.buildGroupedStudents();
                })
                .catch(function(error) {
                    console.error('Грешка при зареждане на потребители:', error);
                });
        },
        recount(){
            const vm = this;
            vm.numAdmins = 0;
            vm.numTeachers = 0;
            vm.numStudents = 0;
            for (let i = 0; i < vm.listOfUsers.length; i++) {
                const lvl = vm.listOfUsers[i]?.userprofile?.access_level; // смени към access_level
                if (!lvl) continue;
                if (lvl < 4) vm.numAdmins += 1;
                if (lvl === 4) vm.numTeachers += 1;
                if (lvl === 5) vm.numStudents += 1;
            }
        },
        loadSpecialties(logged_user) {
            // чета списъка на всички специалности които са от същото училище, като влезлия потребител
            const vm = this;
            if (!logged_user || !logged_user.school || logged_user.school === 0) {
                vm.listOfSpecialties = [];
                return;
            }
            axios.get('/api/schools/' + logged_user.school + '/specialties/')
                .then(function (response) {
                    vm.listOfSpecialties = response.data || [];
                })
                .catch(function (error) {
                    console.error('Грешка при зареждане на специалности:', error);
                    vm.listOfSpecialties = [];
                });
        },
        buildGroupedStudents() {
            const groups = {};
            for (const u of this.listOfUsers) {
                const up = u.userprofile || {};
                if (up.access_level !== 5) continue; // само ученици

                const grade = up.grade;
                const section = up.section;

                if (grade == null || !section) continue; // пропускаме невалидни

                if (!groups[grade]) groups[grade] = {};
                if (!groups[grade][section]) groups[grade][section] = [];
                groups[grade][section].push(u);
            }

            // по желание: сортиране на секциите по азбучен ред и учениците по име
            const sortedGroups = {};
            const sortedGrades = Object.keys(groups).sort((a, b) => Number(a) - Number(b));
            for (const g of sortedGrades) {
                const sections = groups[g];
                const sortedSections = {};
                const sectionKeys = Object.keys(sections).sort((a, b) => a.localeCompare(b, 'bg'));
                for (const s of sectionKeys) {
                    // сортиране на учениците по фамилия, после собствено име
                    sortedSections[s] = sections[s].slice().sort((u1, u2) => {
                        const spec1 = u1.userprofile?.speciality?.specialty_name || '';
                        const spec2 = u2.userprofile?.speciality?.specialty_name || '';
                        const a = `${u1.first_name || ''} ${u1.last_name || ''} ${spec1}`.trim();
                        const b = `${u2.first_name || ''} ${u2.last_name || ''} ${spec2}`.trim();
                        return a.localeCompare(b, 'bg');
                    });
                }
                sortedGroups[g] = sortedSections;
            }
            this.groupedStudents = sortedGroups;
        },

        // UI helpers
        clearEditMode(){
            this.edit.editor = false
            this.edit.admin = false
            this.edit.teacher = false
            this.edit.student = false
            this.formChangePassword = false
        },
        setEditMode(lvl) {
            this.clearEditMode()
            if(lvl===3){this.edit.admin = true}
            if(lvl===4){this.edit.teacher = true}
            if(lvl===5){this.edit.student = true}
            this.edit.editor = true
        },
        resetForm(){
            this.formMode = 'create';
            this.formUserId = 0;
            this.form = {
                username: '',
                password: '',
                password2: '',
                email: '',
                first_name: '',
                last_name: '',
                userprofile: {
                    gender: true,
                    school: this.user.school ? this.user.school : null,  // по подразбиране същото училище
                    access_level: 5,
                    session_screen: 1,
                    session: null,
                    grade: 8,
                    section: 'а',
                    speciality: null,
                    subject: null,
                }
            };
        },
        startCreate(lvl){
            this.resetForm();
            this.formMode = 'create';
            this.form.userprofile.access_level = lvl;
            this.setEditMode(lvl)
        },
        startEdit(row,lvl){
            this.resetForm();
            this.formMode = 'edit';
            this.formUserId = row.id;
            this.form.username = row.username || '';
            this.form.email = row.email || '';
            this.form.first_name = row.first_name || '';
            this.form.last_name = row.last_name || '';
            // парола не пълним
            const up = row.userprofile || {};
            this.form.userprofile.gender = up.gender ?? true;
            this.form.userprofile.school = (typeof up.school === 'object' ? up.school?.id : up.school) || (this.user.school ? this.user.school : null);
            this.form.userprofile.access_level = up.access_level ?? 5;
            this.form.userprofile.session_screen = up.session_screen ?? 1;
            this.form.userprofile.session = (typeof up.session === 'object' ? up.session?.id : up.session) || null;
            this.form.userprofile.grade = up.grade ?? 8;
            this.form.userprofile.section = up.section || 'а';
            this.form.userprofile.speciality = (typeof up.speciality === 'object' ? up.speciality?.id : up.speciality) || null;
            this.form.userprofile.subject = (typeof up.subject === 'object' ? up.subject?.id : up.subject) || null;
            this.setEditMode(lvl)
        },
        saveUser(){
            const vm = this;
            const payload = JSON.parse(JSON.stringify(vm.form));
            // Ако сме в edit и паролата е празна -> премахни, да не се сменя
            if (vm.formMode === 'edit' && (!payload.password || payload.password.trim() === '')) {
                delete payload.password;
            }
            delete payload.password2;

            if (payload.userprofile) {
                for (const k of ['school', 'speciality', 'subject', 'session']) {
                    if (payload.userprofile[k] === 0 || payload.userprofile[k] === '0' || payload.userprofile[k] === '') {
                        payload.userprofile[k] = null;
                    }
                }
            }

            const request = (vm.formMode === 'create')
                ? axios.post('/api/users/', payload, {
                    headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}
                })
                : axios.put(`/api/users/${vm.formUserId}/`, payload, {
                    headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}
                });

            request
                .then(() => {
                    vm.clearEditMode();
                    vm.loadUsers();
                    vm.resetForm();
                })
                .catch((error) => {
                    console.error('Грешка при запис на потребител:', error);
                    let errorDetail = error.response?.data?.detail || error.response?.data?.error;
                    if (!errorDetail && error.response?.data && typeof error.response.data === 'object') {
                        const messages = [];
                        const extractErrors = (obj) => {
                            for (const [k, v] of Object.entries(obj)) {
                                if (Array.isArray(v)) {
                                    messages.push(`${k}: ${v.join(', ')}`);
                                } else if (typeof v === 'object' && v !== null) {
                                    extractErrors(v);
                                } else {
                                    messages.push(`${k}: ${v}`);
                                }
                            }
                        };
                        extractErrors(error.response.data);
                        if (messages.length > 0) {
                            errorDetail = messages.join('\n');
                        }
                    }
                    if (!errorDetail) {
                        errorDetail = 'Възникна грешка при записа на потребителя.';
                    }
                    alert(errorDetail);
                });
        },
        deleteUser(row){
            const vm = this;
            if (!confirm(`Изтриване на потребител ${row.username}?`)) return;
            axios.delete(`/api/users/${row.id}/`)
                .then(() => vm.loadUsers());
        },
    },
    created(){
        this.loadUserDetails();
    },
}

Vue.createApp(App).mount('#main_app')