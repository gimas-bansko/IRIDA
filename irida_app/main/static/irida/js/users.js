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
        },
        loadUsers(){
            const vm = this;
            axios.get('/api/users-list/'+vm.user.school+'/'+vm.user.user_level_num+'/')
                .then(function(response){
                    vm.listOfUsers = response.data;
                    vm.recount();
                })
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
            axios.get('/api/schools/' + logged_user.school + '/specialties/')
                .then(function (response) {
                    vm.listOfSpecialties = response.data
                    console.log(vm.listOfSpecialties)
                })
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
                    school: this.user.school || null,  // по подразбиране същото училище
                    access_level: 5,
                    session_screen: 1,
                    session: null,
                    grade: 8,
                    section: 'a',
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
            this.form.userprofile.school = up.school?.id || this.user.school || null;
            this.form.userprofile.access_level = up.access_level ?? 5;
            this.form.userprofile.session_screen = up.session_screen ?? 1;
            this.form.userprofile.session = up.session?.id || null;
            this.form.userprofile.grade = up.grade;
            this.form.userprofile.section = up.section;
            this.form.userprofile.speciality = up.speciality?.id || null;
            this.form.userprofile.subject = up.subject?.id || null;
            this.setEditMode(lvl)
        },
        saveUser(){
            this.clearEditMode()
            const vm = this;
            const payload = JSON.parse(JSON.stringify(vm.form));
            // Ако сме в edit и паролата е празна -> премахни, да не се сменя
            if (vm.formMode === 'edit' && (!payload.password || payload.password.trim() === '')) {
                delete payload.password;
            }

            if (vm.formMode === 'create') {
                axios.post('/api/users/', payload, {
                    headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}
                })
                    .then(() => {
                        vm.loadUsers();
                        vm.resetForm();
                    })
            } else {
                axios.put(`/api/users/${vm.formUserId}/`, payload, {
                    headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}
                })
                    .then(() => {
                        vm.loadUsers();
                        vm.resetForm();
                    })
            }
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